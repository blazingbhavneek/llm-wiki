# GPU Exclusive Access to Managed Memory (Pre-6.x)

On GPU architectures prior to Compute Capability 6.x, the GPU maintains exclusive access to managed memory while any kernel is active. This restriction applies regardless of whether the active GPU kernel actually accesses the specific managed data being touched by the CPU.

## Synchronization Requirement

On systems with pre-6.x GPU architectures, a CPU thread may not access any managed data in between performing a kernel launch and a subsequent synchronization call [CUDA_C_Programming_Guide:L21857-L21896]. The mere potential for concurrent CPU and GPU access is sufficient for a process-level exception to be raised [CUDA_C_Programming_Guide:L21857-L21896].

To safely access managed memory from the CPU after launching a kernel, the program must explicitly synchronize with the GPU using `cudaDeviceSynchronize()` [CUDA_C_Programming_Guide:L21857-L21896].

### Example

The following code demonstrates the requirement. In the first snippet, the CPU attempts to write to `y` while the kernel is still active (running on `x`). This results in an error on pre-6.x devices [CUDA_C_Programming_Guide:L21857-L21896].

```cpp
__device__ __managed__ int x, y=2;
__global__ void kernel() {
    x = 10;
}
int main() {
    kernel<<< 1, 1 >>>();
    y = 20;          // Error on GPUs not supporting concurrent access

    cudaDeviceSynchronize();
    return  0;
}
```

The correct approach requires inserting `cudaDeviceSynchronize()` before the CPU access [CUDA_C_Programming_Guide:L21857-L21896]:

```cpp
__device__ __managed__ int x, y=2;
__global__ void kernel() {
    x = 10;
}
int main() {
    kernel<<< 1, 1 >>>();
    cudaDeviceSynchronize();
    y = 20;          // Success on GPUs not supporting concurrent access
    return  0;
}
```

## Dynamic Allocation Behavior

If memory is dynamically allocated with `cudaMallocManaged()` or `cuMemAllocManaged()` while the GPU is active, the behavior of the memory is unspecified until additional work is launched or the GPU is synchronized [CUDA_C_Programming_Guide:L21857-L21896]. Attempting to access the memory on the CPU during this time may or may not cause a segmentation fault [CUDA_C_Programming_Guide:L21857-L21896].

This restriction does not apply to memory allocated using the flag `cudaMemAttachHost` or `CU_MEM_ATTACH_HOST` [CUDA_C_Programming_Guide:L21857-L21896].

## Compute Capability 6.x and Later

Starting with Compute Capability 6.x, GPUs support page faulting capabilities which lift the restrictions on simultaneous CPU and GPU access to managed memory [CUDA_C_Programming_Guide:L21857-L21896]. Consequently, the code examples above run successfully on devices of compute capability 6.x and later without explicit synchronization between the kernel launch and CPU access [CUDA_C_Programming_Guide:L21857-L21896].
