# Empirical Analysis of Sorting Algorithms

## Code

The source code for Selection Sort, Bubble Sort, Quick Sort, and Merge Sort is in [sorting_benchmark.py](sorting_benchmark.py).

## Timing Tables

Run the benchmark script on the same machine and paste the measured averages below.

### Selection Sort

| Case | Average Time (s) |
|---|---:|
| 5, Sorted | 0.00001170 |
| 5, Reverse Sorted | 0.00000823 |
| 100, Sorted | 0.00208467 |
| 100, Reverse Sorted | 0.00185160 |

### Bubble Sort

| Case | Average Time (s) |
|---|---:|
| 5, Sorted | 0.00000800 |
| 5, Reverse Sorted | 0.00001270 |
| 100, Sorted | 0.00003750 |
| 100, Reverse Sorted | 0.00457657 |

### Quick Sort

| Case | Average Time (s) |
|---|---:|
| 5, Sorted | 0.00002517 |
| 5, Reverse Sorted | 0.00001690 |
| 100, Sorted | 0.00433207 |
| 100, Reverse Sorted | 0.00290980 |

### Merge Sort

| Case | Average Time (s) |
|---|---:|
| 5, Sorted | 0.00002657 |
| 5, Reverse Sorted | 0.00001780 |
| 100, Sorted | 0.00051330 |
| 100, Reverse Sorted | 0.00078237 |

## Comparison and Swap Totals

These totals are the combined counts from the 3 benchmark runs.

| Algorithm | 5, Sorted | 5, Reverse Sorted | 100, Sorted | 100, Reverse Sorted |
|---|---:|---:|---:|---:|
| Selection Sort | 30 / 0 | 30 / 6 | 14850 / 0 | 14850 / 150 |
| Bubble Sort | 12 / 0 | 30 / 30 | 297 / 0 | 14850 / 14850 |
| Quick Sort | 30 / 42 | 30 / 24 | 14850 / 15147 | 14850 / 7647 |
| Merge Sort | 15 / 15 | 21 / 21 | 948 / 948 | 1068 / 1068 |

## Analysis

Selection Sort and Bubble Sort are both quadratic algorithms, so they become noticeably slower as the input grows from 5 to 100 elements. For very small arrays, the constant factors matter more than the asymptotic growth, so any difference between the four algorithms is usually minor. On 100 elements, Merge Sort should usually be the fastest of the stable $O(n \log n)$ methods, while Quick Sort can also be very fast when the pivot choice is favorable.

Input order affects Bubble Sort the most because a sorted array lets it stop early after one pass, while a reverse-sorted array forces the maximum number of swaps. Selection Sort still performs the same number of comparisons regardless of input order, so its running time changes less between sorted and reverse-sorted cases. Quick Sort with a last-element pivot is sensitive to ordered input: a sorted or reverse-sorted array can push it toward its worst-case behavior. Merge Sort is largely insensitive to input order because it always divides and merges in the same way.

The timing results should match the expected Big-O behavior. Bubble Sort and Selection Sort follow $O(n^2)$ growth. Merge Sort is $O(n \log n)$ and usually scales much better. Quick Sort is average-case $O(n \log n)$, but with a poor pivot rule it can degrade to $O(n^2)$ on already sorted data.

For memory use, Selection Sort and Bubble Sort are in-place and need only $O(1)$ auxiliary space. Quick Sort uses recursion stack space, which is typically $O(\log n)$ on balanced partitions but can grow to $O(n)$ in the worst case. Merge Sort uses extra arrays during merging, so it needs $O(n)$ auxiliary space and is the most memory-intensive of the four.

## Conclusion

For very small data sets, I would choose Bubble Sort or Selection Sort only for simplicity, since the runtime difference is negligible. For larger data, Merge Sort is the safest choice when stable performance matters, while Quick Sort is a strong practical choice if the pivot strategy is robust. In this assignment setting, Merge Sort is the best overall choice for predictable performance, and Quick Sort needs a better pivot rule than last-element pivoting to avoid bad cases on ordered input.

## GitHub URL

Public repository URL: TBD