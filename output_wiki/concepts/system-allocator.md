# System Allocator

The system allocator in CUDA allows for the allocation of memory using standard C library functions like `malloc`, rather than CUDA-specific allocation APIs like `cudaMalloc`. This approach is particularly relevant in systems with shared page tables, where the operating system manages memory mapping for both CPU and GPU.

## Usage and Memory Advice

When using `malloc` to allocate memory that is accessed by both the host (CPU) and device (GPU), it is often necessary to provide explicit memory hints to the CUDA runtime. This is done using the `cudaMemAdvise` function.

For example, to indicate that a memory region allocated via `malloc` will be accessed by the host, one can set the `cudaMemAdviseSetAccessedBy` advice:

```c
int *ret = (int*)malloc(1000 * sizeof(int));
cudaMemLocation location = {.type = cudaMemLocationTypeHost};
cudaMemAdvise(ret, 1000 * sizeof(int), cudaMemAdviseSetAccessedBy, location);
```

In systems with shared page tables, this hint may not be strictly necessary, but it ensures correct behavior across different hardware configurations.

## Hardware Coherency and Memory Migration

The behavior of memory access when using system-allocated memory depends heavily on the hardware's support for direct managed memory access from the host, controlled by the `directManagedMemAccessFromHost` setting.

### Host Access to GPU Memory

When the host reads from memory that has been populated in GPU memory (e.g., after a kernel write):

*   **If `directManagedMemAccessFromHost=1`**: The CPU accesses the GPU memory directly without triggering any migrations. This implies hardware-level coherency or direct addressing capabilities.
*   **If `directManagedMemAccessFromHost=0`**: The CPU encounters a fault, which triggers a device-to-host memory migration. The data is copied from the GPU to the CPU's accessible memory space before the read completes.

### Device Access to Host Memory

When the GPU accesses memory that resides in host memory:

*   **If `directManagedMemAccessFromHost=1`**: The GPU accesses the memory directly without migrations.
*   **If `directManagedMemAccessFromHost=0`**: The GPU encounters a fault, triggering a host-to-device memory migration. The data is copied from the host to the GPU's memory space before the write or read operation proceeds.

## Example Workflow

The following code snippet illustrates the lifecycle of a system-allocated buffer used in a CUDA kernel:

1.  **Allocation**: Memory is allocated using `malloc`.
2.  **Advice**: `cudaMemAdvise` is called to inform the runtime about host access patterns.
3.  **Kernel Execution**: A kernel (`write`) populates the buffer in GPU memory.
4.  **Synchronization**: `cudaDeviceSynchronize()` ensures the kernel completes.
5.  **Host Access**: The host iterates over the buffer. Depending on `directManagedMemAccessFromHost`, this either accesses GPU memory directly or triggers a migration.
6.  **Kernel Execution**: A second kernel (`append`) modifies the buffer. Depending on the coherency setting, this may or may not trigger a migration.
7.  **Deallocation**: The memory is freed using `free`.

```c
__global__ void write(int *ret, int a, int b) {
    ret[threadIdx.x] = a + b + threadIdx.x;
}

__global__ void append(int *ret, int a, int b) {
    ret[threadIdx.x] += a + b + threadIdx.x;
}

void test_malloc() {
    int *ret = (int*)malloc(1000 * sizeof(int));
    // for shared page table systems, the following hint is not necessary
    cudaMemLocation location = {.type = cudaMemLocationTypeHost};
    cudaMemAdvise(ret, 1000 * sizeof(int), cudaMemAdviseSetAccessedBy, location);

    write<<< 1, 1000 >>>(ret, 10, 100);          // pages populated in GPU memory
    cudaDeviceSynchronize();
    for(int i = 0; i < 1000; i++)
        printf("%d: A+B = %d\n", i, ret[i]);      // directManagedMemAccessFromHost=1:
                                                    // CPU accesses GPU memory directly without migrations
                                                    // directManagedMemAccessFromHost=0:
                                                    // CPU faults and triggers device-to-host migrations
    append<<< 1, 1000 >>>(ret, 10, 100);       // directManagedMemAccessFromHost=1:
                                                // GPU accesses GPU memory without migrations
    cudaDeviceSynchronize();                    // directManagedMemAccessFromHost=0:
                                                // GPU faults and triggers host-to-device migrations
    free(ret);
}
```

## References

[CUDA_C_Programming_Guide:L21681-L21710]
