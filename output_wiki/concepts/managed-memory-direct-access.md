# Managed Memory Direct Access & System Allocator vs Managed Memory Behavior

Covers the difference between system-allocated memory and managed memory, and how the directManagedMemAccessFromHost hardware feature affects CPU/GPU memory migration and faulting behavior.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L21681-L21749

Citation: [CUDA_C_Programming_Guide:L21681-L21749]

````text
## System Allocator

```txt
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
CPU accesses GPU memory directly without migrations
                                // directManagedMemAccessFromHost=0:
CPU faults and triggers device-to-host migrations
    append<<< 1, 1000 >>>(ret, 10, 100);       // directManagedMemAccessFromHost=1:
GPU accesses GPU memory without migrations
    cudaDeviceSynchronize();                    // directManagedMemAccessFromHost=0:
GPU faults and triggers host-to-device migrations
    free(ret);
}
```

## Managed

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
CPU accesses GPU memory directly without migrations
                                // directedManagedMemAccessFromHost=0:
CPU faults and triggers device-to-host migrations
    append<<< 1, 1000 >>>(ret, 10, 100);       // directedManagedMemAccessFromHost=1:
GPU accesses GPU memory without migrations
    cudaDeviceSynchronize();                    // directedManagedMemAccessFromHost=0:
GPU faults and triggers host-to-device migrations
    cudaFree(ret);
}
```

After write kernel is completed, ret will be created and initialized in GPU memory. Next, the CPU will access ret followed by append kernel using the same ret memory again. This code will show diferent behavior depending on the system architecture and support of hardware coherency:

▶ On systems with directManagedMemAccessFromHost=1: CPU accesses to the managed bufer will not trigger any migrations; the data will remain resident in GPU memory and any subsequent GPU kernels can continue to access it directly without inflicting faults or migrations.

▶ On systems with directManagedMemAccessFromHost=0: CPU accesses to the managed bufer will page fault and initiate data migration; any GPU kernel trying to access the same data first time will page fault and migrate pages back to GPU memory.
````
