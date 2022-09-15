def binary_search(arr, x):
    start = 0
    end = len(arr)-1
    mid = 0
    while start <= end:
        mid = (start+end) // 2
        if arr[mid] < x:
            start = mid + 1
        elif arr[mid] > x:
            end = mid - 1
        else:
            return mid
    return -1

#Example
arr = [1, 7, 3, -4, 5, -12, 66]
index = binary_search(arr, -4)
print("Phan tu can tim o vi tri " + str(index) if index != -1 else "Khong tim thay phan tu")
