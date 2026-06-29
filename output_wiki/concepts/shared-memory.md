# Shared Memory

Shared memory is a user-managed cache located on the GPU device that is significantly faster than global memory [CUDA_C_Programming_Guide:L1626-L1650]. It is allocated using the `__shared__` memory space specifier and serves as scratchpad memory to minimize global memory accesses from a CUDA block [CUDA_C_Programming_Guide:L1626-L1650].

## Usage and Performance

Shared memory allows threads within a thread block to cooperate by sharing data. By loading data from global memory into shared memory, threads can reuse that data multiple times without incurring the latency and bandwidth costs of repeated global memory accesses [CUDA_C_Programming_Guide:L1626-L1650].

A common example of this optimization is matrix multiplication. In a naive implementation where each thread reads directly from global memory, matrix A is read `B.width` times and matrix B is read `A.height` times [CUDA_C_Programming_Guide:L1652-L1660]. By utilizing shared memory, the computation is blocked such that each thread block computes a sub-matrix of the result. The required sub-matrices of A and B are loaded into shared memory once per block [CUDA_C_Programming_Guide:L1690-L1700]. This reduces the number of global memory reads for A to `(B.width / block_size)` and for B to `(A.height / block_size)`, saving significant global memory bandwidth [CUDA_C_Programming_Guide:L1700-L1705].

## Synchronization

Because shared memory is accessible by all threads in a block, synchronization is required to ensure data consistency. The `__syncthreads()` function is used to synchronize all threads in a block [CUDA_C_Programming_Guide:L1730-L1735]. 

In the optimized matrix multiplication kernel, `__syncthreads()` is called after threads have loaded their respective elements from the sub-matrices of A and B into shared memory. This ensures that all threads have finished writing to shared memory before any thread begins reading from it for computation [CUDA_C_Programming_Guide:L1730-L1735]. Another synchronization point is often placed after the computation phase to ensure that the preceding computation is complete before the block loads new sub-matrices for the next iteration of the loop [CUDA_C_Programming_Guide:L1735-L1740].

## Implementation Details

Shared memory arrays are declared with the `__shared__` qualifier. For example, in a matrix multiplication kernel with a block size of 16, shared memory arrays might be declared as:

```cpp
__shared__ float As[BLOCK_SIZE][BLOCK_SIZE];
__shared__ float Bs[BLOCK_SIZE][BLOCK_SIZE];
```

Each thread within the block is responsible for loading one element of each sub-matrix into these shared memory arrays [CUDA_C_Programming_Guide:L1725-L1730]. After synchronization, each thread computes its assigned element of the result by iterating over the shared memory arrays [CUDA_C_Programming_Guide:L1735-L1740]. Finally, each thread writes its computed result back to global memory [CUDA_C_Programming_Guide:L1740-L1745].

## References

- CUDA C Programming Guide, Section 6.2.4 Shared Memory [CUDA_C_Programming_Guide:L1626-L1850]
