from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, Dict, List, Sequence, Tuple


Array = List[int]


@dataclass
class SortMetrics:
    comparisons: int = 0
    swaps: int = 0


def selection_sort(values: Array, metrics: SortMetrics | None = None) -> Array:
    arr = values.copy()
    n = len(arr)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if metrics is not None:
                metrics.comparisons += 1
            if arr[j] < arr[min_index]:
                min_index = j
        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]
            if metrics is not None:
                metrics.swaps += 1
    return arr


def bubble_sort(values: Array, metrics: SortMetrics | None = None) -> Array:
    arr = values.copy()
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if metrics is not None:
                metrics.comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                if metrics is not None:
                    metrics.swaps += 1
        if not swapped:
            break
    return arr


def quick_sort(values: Array, metrics: SortMetrics | None = None) -> Array:
    arr = values.copy()

    def partition(low: int, high: int) -> int:
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if metrics is not None:
                metrics.comparisons += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                if metrics is not None:
                    metrics.swaps += 1
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        if metrics is not None:
            metrics.swaps += 1
        return i + 1

    def quicksort(low: int, high: int) -> None:
        if low < high:
            pivot_index = partition(low, high)
            quicksort(low, pivot_index - 1)
            quicksort(pivot_index + 1, high)

    quicksort(0, len(arr) - 1)
    return arr


def merge_sort(values: Array, metrics: SortMetrics | None = None) -> Array:
    arr = values.copy()

    def merge_sort_recursive(segment: Array) -> Array:
        if len(segment) <= 1:
            return segment

        mid = len(segment) // 2
        left = merge_sort_recursive(segment[:mid])
        right = merge_sort_recursive(segment[mid:])
        return merge(left, right)

    def merge(left: Array, right: Array) -> Array:
        merged: Array = []
        i = j = 0
        while i < len(left) and j < len(right):
            if metrics is not None:
                metrics.comparisons += 1
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
            if metrics is not None:
                metrics.swaps += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    return merge_sort_recursive(arr)


def build_input(size: int, order: str) -> Array:
    data = list(range(1, size + 1))
    if order == "reverse":
        data.reverse()
    return data


def average_time(sort_fn: Callable[[Array, SortMetrics | None], Array], data: Sequence[int], runs: int = 3) -> float:
    timings: List[float] = []
    for _ in range(runs):
        metrics = SortMetrics()
        start = time.perf_counter()
        result = sort_fn(list(data), metrics)
        elapsed = time.perf_counter() - start
        if result != sorted(data):
            raise ValueError(f"Sort failed for {sort_fn.__name__}")
        timings.append(elapsed)
    return sum(timings) / len(timings)


def benchmark() -> Tuple[Dict[str, Dict[str, float]], Dict[str, Dict[str, SortMetrics]]]:
    algorithms: Dict[str, Callable[[Array, SortMetrics | None], Array]] = {
        "Selection Sort": selection_sort,
        "Bubble Sort": bubble_sort,
        "Quick Sort": quick_sort,
        "Merge Sort": merge_sort,
    }
    cases = [
        (5, "Sorted"),
        (5, "Reverse Sorted"),
        (100, "Sorted"),
        (100, "Reverse Sorted"),
    ]

    timing_results: Dict[str, Dict[str, float]] = {name: {} for name in algorithms}
    metric_results: Dict[str, Dict[str, SortMetrics]] = {name: {} for name in algorithms}

    for algorithm_name, sort_fn in algorithms.items():
        for size, order in cases:
            label = f"{size} | {order}"
            data = build_input(size, "reverse" if order.startswith("Reverse") else "sorted")
            metrics = SortMetrics()
            timings = []
            for _ in range(3):
                run_metrics = SortMetrics()
                start = time.perf_counter()
                result = sort_fn(data, run_metrics)
                elapsed = time.perf_counter() - start
                if result != sorted(data):
                    raise ValueError(f"{algorithm_name} failed for {label}")
                timings.append(elapsed)
                metrics.comparisons += run_metrics.comparisons
                metrics.swaps += run_metrics.swaps
            timing_results[algorithm_name][label] = sum(timings) / len(timings)
            metric_results[algorithm_name][label] = metrics

    return timing_results, metric_results


def format_seconds(value: float) -> str:
    return f"{value:.8f}"


def print_tables() -> None:
    timings, metrics = benchmark()
    case_labels = ["5 | Sorted", "5 | Reverse Sorted", "100 | Sorted", "100 | Reverse Sorted"]

    print("Timing Results (average of 3 runs, seconds)")
    header = ["Algorithm"] + case_labels
    print(" | ".join(header))
    print(" | ".join(["---"] * len(header)))
    for algorithm_name, case_times in timings.items():
        row = [algorithm_name] + [format_seconds(case_times[label]) for label in case_labels]
        print(" | ".join(row))

    print()
    print("Comparison and Swap Totals (3 runs combined)")
    print(" | ".join(header))
    print(" | ".join(["---"] * len(header)))
    for algorithm_name, case_metrics in metrics.items():
        row = [algorithm_name] + [f"{case_metrics[label].comparisons} / {case_metrics[label].swaps}" for label in case_labels]
        print(" | ".join(row))


if __name__ == "__main__":
    print_tables()