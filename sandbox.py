"""
sandbox.py — Safe Python code execution in a subprocess.
Restricts dangerous modules and enforces a timeout.
"""

import subprocess
import sys
import os
import tempfile


def run_code(code: str, timeout: int = 5) -> dict:
    """
    Execute user-supplied Python code safely in a subprocess.
    Returns dict with stdout, stderr, exit_code.
    """
    tmpdir = tempfile.mkdtemp()
    wrapper_path = os.path.join(tmpdir, 'runner.py')
    user_path = os.path.join(tmpdir, 'user_code.py')

    try:
        # Write user code to a separate file
        with open(user_path, 'w', encoding='utf-8') as f:
            f.write(code)

        # Wrapper: runs user code with limited dangerous module access.
        # Note: heapq, collections, math etc. are allowed for DSA algorithms.
        user_path_repr = repr(user_path)
        simple_wrapper = f'''import sys
import builtins as _builtins

# Pre-import safe stdlib modules so they survive the module block
import heapq as _heapq
import collections as _collections
import math as _math
import itertools as _itertools
import functools as _functools
sys.modules["heapq"] = _heapq
sys.modules["collections"] = _collections
sys.modules["math"] = _math
sys.modules["itertools"] = _itertools
sys.modules["functools"] = _functools

# Block dangerous stdlib modules AFTER pre-importing safe ones
_blocked = [
    "subprocess", "socket", "shutil", "pathlib",
    "importlib", "ctypes", "multiprocessing", "threading",
    "signal", "winreg", "msvcrt",
]
for _m in _blocked:
    sys.modules[_m] = None

# Override open to prevent arbitrary file I/O
_real_open = _builtins.open
def _safe_open(file, mode="r", *args, **kwargs):
    allowed = {user_path_repr}
    if str(file) == allowed:
        return _real_open(file, mode, *args, **kwargs)
    raise PermissionError("File access is not allowed in the sandbox.")
_builtins.open = _safe_open

# Run the user code
with _real_open({user_path_repr}, "r", encoding="utf-8") as _f:
    _src = _f.read()

exec(compile(_src, "<sandbox>", "exec"))
'''

        with open(wrapper_path, 'w', encoding='utf-8') as f:
            f.write(simple_wrapper)

        # Copy environment and clean dangerous/unneeded Python variables
        env = os.environ.copy()
        env.update({
            "PYTHONPATH": "",
            "PYTHONNOUSERSITE": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONINSPECT": "0",
        })

        result = subprocess.run(
            [sys.executable, wrapper_path],
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
        # Filter benign internal Python shutdown warnings
        stderr = result.stderr
        filtered_lines = [
            line for line in stderr.splitlines()
            if 'Exception ignored on threading shutdown' not in line
            and "NoneType' object has no attribute '_shutdown'" not in line
        ]
        stderr = '\n'.join(filtered_lines).strip()

        return {
            "stdout": result.stdout,
            "stderr": stderr,
            "exit_code": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": f"TimeoutError: Code execution exceeded {timeout}s limit.",
            "exit_code": 1,
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": f"ExecutionError: {str(e)}",
            "exit_code": 1,
        }
    finally:
        import shutil as _shutil
        try:
            _shutil.rmtree(tmpdir, ignore_errors=True)
        except Exception:
            pass
