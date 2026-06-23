"""
algorithms/searching.py — Linear Search and Binary Search implementations.
"""


def linear_search(arr, target):
    """
    Linear Search — O(n) time, O(1) space.
    Checks each element sequentially.
    Returns index if found, else -1.
    """
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1


def binary_search(arr, target):
    """
    Binary Search — O(log n) time, O(1) space.
    Array must be sorted. Repeatedly halves search space.
    Returns index if found, else -1.
    """
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


if __name__ == "__main__":
    arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    target = 23

    print(f"Array: {arr}")
    print(f"Target: {target}")
    print(f"Linear Search index: {linear_search(arr, target)}")
    print(f"Binary Search index: {binary_search(arr, target)}")
