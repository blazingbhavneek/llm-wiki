# Managed Memory (CUDA)

Managed memory in CUDA allows for unified memory access between the CPU and GPU, simplifying memory management by eliminating the need for explicit data transfers. The primary API for allocating managed memory is `cudaMallocManaged`.

## Allocation and Advice

Managed memory is allocated using `cudaMallocManaged`, which returns a pointer accessible by both the host (CPU) and device (GPU). To optimize performance, developers can use `cudaMemAdvise` to provide hints to the CUDA runtime about memory access patterns. For example, specifying that a memory range is accessed by the host can influence how the runtime handles page faults and migrations.

```cpp
int *ret;
cudaMallocManaged(&ret, 1000 * sizeof(int));
cudaMemLocation location = {.type = cudaMemLocationTypeHost};
cudaMemAdvise(ret, 1000 * sizeof(int), cudaMemAdviseSetAccessedBy, location);  // set direct access hint
```

## Behavior and Hardware Coherency

The behavior of managed memory, specifically regarding page faults and data migration, depends on the system's hardware coherency support, indicated by the property `directManagedMemAccessFromHost`.

### Systems with `directManagedMemAccessFromHost=1`
On systems with hardware coherency support:
- CPU accesses to the managed buffer do not trigger migrations; the data remains resident in GPU memory.
- Subsequent GPU kernels can access the data directly without incurring faults or migrations.

### Systems with `directManagedMemAccessFromHost=0`
On systems without hardware coherency support:
- CPU accesses to the managed buffer cause page faults and initiate data migration from GPU to host memory.
- When a GPU kernel accesses the same data, it triggers a page fault and migrates the pages back to GPU memory.

## Example Workflow

The following code snippet demonstrates the lifecycle of managed memory, including allocation, kernel execution, and host access.

```cpp
__global__ void write(int *ret, int a, int b) {
    ret[threadIdx.x] = a + b + threadIdx.x;
}

__global__ void append(int *ret, int a, int b) {
    ret[threadIdx.x] += a + b + threadIdx.x;
}

void test_managed() {
    int *ret;
    cudaMallocManaged(&ret, 1000 * sizeof(int));
    cudaMemLocation location = {.type = cudaMemLocationTypeHost};
    cudaMemAdvise(ret, 1000 * sizeof(int), cudaMemAdviseSetAccessedBy, location);  // set direct access hint

    write<<< 1, 1000 >>>(ret, 10, 100);          // pages populated in GPU memory
    cudaDeviceSynchronize();
    for(int i = 0; i < 1000; i++)
        printf("%d: A+B = %d\n", i, ret[i]);      // directedManagedMemAccessFromHost=1:
    // CPU accesses GPU memory directly without migrations
                                // directedManagedMemAccessFromHost=0:
    // CPU faults and triggers device-to-host migrations
    append<<< 1, 1000 >>>(ret, 10, 100);       // directedManagedMemAccessFromHost=1:
    // GPU accesses GPU memory without migrations
    cudaDeviceSynchronize();                    // directedManagedMemAccessFromHost=0:
    // GPU faults and triggers host-to-device migrations
    cudaFree(ret);
}
```

In this example, after the `write` kernel completes, `ret` is created and initialized in GPU memory. When the CPU subsequently accesses `ret`, the behavior diverges based on the system architecture. Finally, the `append` kernel accesses the same memory, again with behavior dependent on `directManagedMemAccessFromHost`.

[CUDA_C_Programming_Guide:L21712-L21749]
