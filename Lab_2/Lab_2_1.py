import concurrent.futures
import time


def merge_sort(arr, thread_pool_size):
    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        with concurrent.futures.ThreadPoolExecutor(max_workers=thread_pool_size) as executor:
            future_left = executor.submit(merge_sort, left, thread_pool_size)
            future_right = executor.submit(merge_sort, right, thread_pool_size)

        left = future_left.result()
        right = future_right.result()

        i, j, k = 0, 0, 0

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

    return arr


def reser_array():
    return [3, 6, 8, 10, 1, 2, 5, 7, 9, 4]


def main():
    arr = [3, 6, 8, 10, 1, 2, 5, 7, 9, 4]

    start_time = time.time()
    print(merge_sort(arr, 2))
    print(f"Threads count: 2\n Time: {time.time() - start_time}\n")

    arr = reser_array()
    start_time = time.time()
    print(merge_sort(arr, 4))
    print(f"Threads count: 4\n Time: {time.time() - start_time}\n")

    arr = reser_array()
    start_time = time.time()
    print(merge_sort(arr, 8))
    print(f"Threads count: 8\n Time: {time.time() - start_time}\n")

    arr = reser_array()
    start_time = time.time()
    print(merge_sort(arr, 16))
    print(f"Threads count: 16\n Time: {time.time() - start_time}\n")

main()