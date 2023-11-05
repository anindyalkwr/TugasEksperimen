import math
import random
import time
import tracemalloc 

def main():
    sizes = [500, 5000, 50000]
    algorithms = [counting_sort, bci_sort]

    for size in sizes:
        dataset_labels = ["sorted", "randomized", "reversed"]

        for label in dataset_labels:
            with open(f"dataset/{label}_dataset_{size}.txt", "r") as file:
                data = [int(line) for line in file.read().splitlines()]

            print(f"Dataset Size: {size}, Type: {label}")
            for algorithm in algorithms:
                measure_running_time(algorithm, data, f"{algorithm.__name__} on {label} data")
                measure_memory_usage(algorithm, data, f"{algorithm.__name__} on {label} data")
            print()


def generate_dataset(size):
    dataset = {}
    dataset["sorted"] = list(range(1, size + 1))
    dataset["randomized"] = dataset["sorted"][:]
    random.shuffle(dataset["randomized"])
    dataset["reversed"] = dataset["sorted"][::-1]
    return dataset

def measure_running_time(sort_func, data, label):
    start_time = time.time()
    if sort_func == counting_sort:
        data = sort_func(data)
    else:
        sort_func(data, 0, len(data) - 1)
    end_time = time.time()
    execution_time = (end_time - start_time) * 1000  # Execution time in milliseconds
    print(f"{label} - Execution Time: {execution_time} ms")

def measure_memory_usage(sort_func, data, label):
    tracemalloc.start() 
    if sort_func == counting_sort:
        data = sort_func(data)
    else:
        sort_func(data, 0, len(data) - 1)
    current, peak = tracemalloc.get_traced_memory() 
    tracemalloc.stop() 
    print(f"{label} - Peak Memory Usage: {peak / (1024 ** 2):.2f} MB")  # Convert to MB

# Saher Mohammed, A., Emrah Amrahov, Ş., & Çelebi, F. V. (2016). Bidirectional Conditional Insertion Sort algorithm; An efficient progress on the classical insertion sort. arXiv e-prints, arXiv-1608.
def is_equal(arr, SL, SR):
    for k in range(SL + 1, SR - 1):
        if arr[k] != arr[SL]:
            swap(arr, k, SL)
            return k
    return -1

def insert_right(arr, current_item, SR, right):
    j = SR
    while j <= right and current_item > arr[j]:
        arr[j - 1] = arr[j]
        j += 1
    arr[j - 1] = current_item

def insert_left(arr, current_item, SL, left):
    j = SL
    while j >= left and current_item < arr[j]:
        arr[j + 1] = arr[j]
        j -= 1
    arr[j + 1] = current_item

def swap(arr, i, j):
    temp = arr[i]
    arr[i] = arr[j]
    arr[j] = temp

def bci_sort(arr, left, right):
    SL = left # Sorted Left
    SR = right # Sorted Right
    while SL < SR:
        swap(arr, SR, SL + (SR - SL) // 2)
        if arr[SL] == arr[SR]:
            if is_equal(arr, SL, SR) == -1:
                return
            
        if arr[SL] > arr[SR]:
            swap(arr, SL, SR)

        i = SL + 1
        if SR - SL >= 100:
            for i in range(i, int(math.sqrt(SR - SL)) + 1):
                if arr[SR] < arr[i]:
                    swap(arr, SR, i)
                elif arr[SL] > arr[i]:
                    swap(arr, SL, i)
        else:
            i = SL + 1

        LC = arr[SL] # Left Comparator
        RC = arr[SR] # Right Comparator

        while i < SR:
            current_item = arr[i]
            if current_item >= RC:
                arr[i] = arr[SR - 1]
                insert_right(arr, current_item, SR, right)
                SR -= 1
            elif current_item <= LC:
                arr[i] = arr[SL + 1]
                insert_left(arr, current_item, SL, left)
                SL += 1
                i += 1
            else:
                i += 1
        SL += 1
        SR -= 1

# Sabili, 2023, Slide 7. "Linear" Sort, Design & Analysis of Algorithms (DAA) — Sem 1 2023/2024
def counting_sort(arr):
    max_val = max(arr)
    counter = [0] * (max_val + 1)
    output = [0] * len(arr)

    for number in arr:
        counter[number] += 1

    for i in range(1, max_val + 1):
        counter[i] += counter[i - 1]

    for num in reversed(arr):
        output[counter[num] - 1] = num
        counter[num] -= 1

    return output

if __name__ == "__main__":
    main()


