# Big-O Notation Cheat Sheet: Time and Space Complexity Guide

## Big-O Notation Explanation

Big-O notation describes the upper bound of an algorithm's runtime or space requirements as input size (n) grows. It focuses on worst-case scenarios and ignores constants/low-order terms (e.g., O(2n + 5) simplifies to O(n)).

- **O(1)**: Constant time – operations take the same amount of time regardless of input size (e.g., array access).
- **O(log n)**: Logarithmic time – time grows slowly with input size, typical for divide-and-conquer algorithms (e.g., binary search).
- **O(n)**: Linear time – time grows proportionally with input size (e.g., single loop).
- **O(n log n)**: Linearithmic time – common in efficient sorting algorithms (e.g., mergesort).
- **O(n²)**: Quadratic time – time grows with the square of the input size, inefficient for large inputs (e.g., nested loops).
- **O(2ⁿ)**: Exponential time – grows extremely fast, impractical for large inputs (e.g., recursive Fibonacci without memoization).
- **O(n!)**: Factorial time – extremely slow, only feasible for very small inputs (e.g., traveling salesman brute force).

Lower is better; aim for O(log n) or O(n) where possible.

## Common Data Structure Operations

| Data Structure     | Time Complexity (Average) |          |          |          | Time Complexity (Worst) |          |          |          | Space Complexity (Worst) |
| ------------------ | ------------------------- | -------- | -------- | -------- | ----------------------- | -------- | -------- | -------- | ------------------------ |
|                    | Access                    | Search   | Insert   | Delete   | Access                  | Search   | Insert   | Delete   |                          |
| Array              | Θ(1)                      | Θ(n)     | Θ(n)     | Θ(n)     | O(1)                    | O(n)     | O(n)     | O(n)     | O(n)                     |
| Stack              | Θ(n)                      | Θ(n)     | Θ(1)     | Θ(1)     | O(n)                    | O(n)     | O(1)     | O(1)     | O(n)                     |
| Queue              | Θ(n)                      | Θ(n)     | Θ(1)     | Θ(1)     | O(n)                    | O(n)     | O(1)     | O(1)     | O(n)                     |
| Singly-Linked List | Θ(n)                      | Θ(n)     | Θ(1)     | Θ(1)     | O(n)                    | O(n)     | O(1)     | O(1)     | O(n)                     |
| Doubly-Linked List | Θ(n)                      | Θ(n)     | Θ(1)     | Θ(1)     | O(n)                    | O(n)     | O(1)     | O(1)     | O(n)                     |
| Skip List          | Θ(log n)                  | Θ(log n) | Θ(log n) | Θ(log n) | O(n)                    | O(n)     | O(n)     | O(n)     | O(n log n)               |
| Hash Table         | N/A                       | Θ(1)     | Θ(1)     | Θ(1)     | N/A                     | O(n)     | O(n)     | O(n)     | O(n)                     |
| Binary Search Tree | Θ(log n)                  | Θ(log n) | Θ(log n) | Θ(log n) | O(n)                    | O(n)     | O(n)     | O(n)     | O(n)                     |
| B-Tree             | Θ(log n)                  | Θ(log n) | Θ(log n) | Θ(log n) | O(log n)                | O(log n) | O(log n) | O(log n) | O(n)                     |
| Red-Black Tree     | Θ(log n)                  | Θ(log n) | Θ(log n) | Θ(log n) | O(log n)                | O(log n) | O(log n) | O(log n) | O(n)                     |
| AVL Tree           | Θ(log n)                  | Θ(log n) | Θ(log n) | Θ(log n) | O(log n)                | O(log n) | O(log n) | O(log n) | O(n)                     |

## Array Sorting Algorithms

| Algorithm      | Time Complexity (Best) | (Average)  | (Worst)    | Space Complexity (Worst) |
| -------------- | ---------------------- | ---------- | ---------- | ------------------------ |
| Quicksort      | Ω(n log n)             | Θ(n log n) | O(n²)      | O(log n)                 |
| Mergesort      | Ω(n log n)             | Θ(n log n) | O(n log n) | O(n)                     |
| Timsort        | Ω(n)                   | Θ(n log n) | O(n log n) | O(n)                     |
| Heapsort       | Ω(n log n)             | Θ(n log n) | O(n log n) | O(1)                     |
| Bubble Sort    | Ω(n)                   | Θ(n²)      | O(n²)      | O(1)                     |
| Insertion Sort | Ω(n)                   | Θ(n²)      | O(n²)      | O(1)                     |
| Selection Sort | Ω(n²)                  | Θ(n²)      | O(n²)      | O(1)                     |
| Bucket Sort    | Ω(n + k)               | Θ(n + k)   | O(n²)      | O(n)                     |
| Radix Sort     | Ω(n k)                 | Θ(n k)     | O(n k)     | O(n + k)                 |
| Counting Sort  | Ω(n + k)               | Θ(n + k)   | O(n + k)   | O(k)                     |

## Other Common Algorithms

| Algorithm             | Time Complexity (Average) | (Worst)          | Space Complexity |
| --------------------- | ------------------------- | ---------------- | ---------------- |
| Binary Search         | Θ(log n)                  | O(log n)         | O(1)             |
| Depth-First Search    | Θ(V + E)                  | Θ(V + E)         | O(V)             |
| Breadth-First Search  | Θ(V + E)                  | Θ(V + E)         | O(V)             |
| Dijkstra's            | Θ((V + E) log V)          | Θ((V + E) log V) | O(V)             |
| Bellman-Ford          | Θ(V E)                    | Θ(V E)           | O(V)             |
| Floyd-Warshall        | Θ(V³)                     | Θ(V³)            | O(V²)            |
| Knapsack (0/1 DP)     | Θ(n W)                    | Θ(n W)           | O(n W)           |
| Matrix Multiplication | Θ(n³)                     | Θ(n³)            | O(n²)            |

**Notes**: V = vertices, E = edges, n = items, W = capacity, k = digits/buckets. Use this for optimizing code: Prefer hash tables for O(1) lookups; avoid O(n²) for large n (>1000). In Python, use `timeit` for benchmarking.

## Python Optimization Tips

- Use built-ins: `list comprehension` over loops for O(n).
- Data structures: `dict`/`set` for O(1) lookups vs. `list` O(n).
- Sorting: `sorted()` is Timsort (O(n log n)).
- Avoid globals; use memoization (`@lru_cache`) for recursion.
