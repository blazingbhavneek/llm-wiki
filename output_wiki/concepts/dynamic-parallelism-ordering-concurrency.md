# Dynamic Parallelism Ordering and Concurrency

Dynamic parallelism allows kernels to launch other kernels (child grids) from within the device runtime. However, the device runtime does not introduce new concurrency guarantees beyond the standard CUDA execution model. Understanding the ordering and concurrency semantics is critical for correct program behavior.

## Ordering Semantics

The ordering of kernel launches from the device runtime follows **CUDA Stream ordering semantics** [CUDA_C_Programming_Guide:L13714-L13725].

### Within a Grid

*   **Named Streams:** All kernel launches into the same named stream (with the exception of the fire-and-forget stream) are executed in-order [CUDA_C_Programming_Guide:L13714-L13725].
*   **Thread Scheduling:** When multiple threads in the same grid launch into the same stream, the ordering within that stream depends on the thread scheduling within the grid. This ordering can be controlled using synchronization primitives such as `__syncthreads()` [CUDA_C_Programming_Guide:L13714-L13725].

### Implicit (NULL) Stream Behavior

Named streams are shared by all threads within a grid, but the implicit NULL stream has different scoping rules [CUDA_C_Programming_Guide:L13714-L13725]:

1.  **Within a Thread Block:** The implicit stream is shared by all threads within a single thread block. If multiple threads in the same thread block launch into the implicit stream, these launches are executed in-order [CUDA_C_Programming_Guide:L13714-L13725].
2.  **Across Thread Blocks:** If multiple threads in *different* thread blocks launch into the implicit stream, these launches may be executed concurrently [CUDA_C_Programming_Guide:L13714-L13725].

To achieve concurrency for launches by multiple threads within a single thread block, explicit named streams must be used [CUDA_C_Programming_Guide:L13714-L13725].

## Concurrency Guarantees

Dynamic parallelism enables concurrency to be expressed more easily within a program, but it does not guarantee concurrent execution [CUDA_C_Programming_Guide:L13714-L13725].

### No Guarantee Between Thread Blocks

There is no guarantee of concurrent execution between any number of different thread blocks on a device [CUDA_C_Programming_Guide:L13714-L13725]. While concurrency may often be achieved, it can vary as a function of:
*   Device configuration
*   Application workload
*   Runtime scheduling

Therefore, it is unsafe to depend upon any concurrency between different thread blocks [CUDA_C_Programming_Guide:L13714-L13725].

### Parent and Child Grid Concurrency

The lack of concurrency guarantee extends to the relationship between a parent grid and its child grids [CUDA_C_Programming_Guide:L13714-L13725].

*   **Execution Start:** A child grid may start to execute once stream dependencies are satisfied and hardware resources are available to host the child [CUDA_C_Programming_Guide:L13714-L13725].
*   **No Execution Guarantee:** The child is **not** guaranteed to begin execution until the parent grid reaches an implicit synchronization point [CUDA_C_Programming_Guide:L13714-L13725].

Programmers should not assume that a child grid will execute concurrently with the parent grid's remaining operations unless explicit synchronization and stream management ensure the desired ordering and resource availability.
