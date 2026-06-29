# Concurrent Access Rules and Examples

Concurrent access rules govern how the CPU and GPU interact with memory while the GPU is active. These rules distinguish between non-managed zero-copy data, managed memory, and multi-GPU scenarios.

## CPU and GPU Concurrent Access

### Non-Managed Zero-Copy Data
It is always permitted for the CPU to access non-managed zero-copy data while the GPU is active [CUDA_C_Programming_Guide:L21907-L21943]. The GPU is considered active when it is running any kernel, even if that kernel does not make use of managed data [CUDA_C_Programming_Guide:L21907-L21943].

### Managed Memory
Access to managed memory by the CPU while the GPU is active is subject to specific constraints:

*   **General Rule:** If a kernel might use data, CPU access to that managed data is forbidden while the GPU is active [CUDA_C_Programming_Guide:L21907-L21943].
*   **Exception:** CPU access is permitted if the device property `concurrentManagedAccess` is set to 1 [CUDA_C_Programming_Guide:L21907-L21943].

## GPU Concurrent Access

### Inter-Kernel Access
There are no constraints on concurrent GPU kernels accessing managed data [CUDA_C_Programming_Guide:L21907-L21943]. This behavior mirrors the handling of non-managed GPU memory, as managed memory functions identically to non-managed memory from the perspective of the GPU [CUDA_C_Programming_Guide:L21907-L21943]. Consequently, races between GPU kernels accessing the same managed data are possible [CUDA_C_Programming_Guide:L21907-L21943].

### Multi-GPU Access
There are no constraints on concurrent inter-GPU access of managed memory, other than those that apply to multi-GPU access of non-managed memory [CUDA_C_Programming_Guide:L21907-L21943].

## Code Example

The following code example illustrates these points:

```cpp
int main() {
    cudaStream_t stream1, stream2;
    cudaStreamCreate(&stream1);
    cudaStreamCreate(&stream2);
    int *non_managed, *managed, *also_managed;
    cudaMallocHost(&non_managed, 4);      // Non-managed, CPU-accessible memory
    cudaMallocManaged(&managed, 4);
    cudaMallocManaged(&also_managed, 4);
    // Point 1: CPU can access non-managed data.
    kernel<<< 1, 1, 0, stream1 >>>(managed);
    *non_managed = 1;
    // Point 2: CPU cannot access any managed data while GPU is busy,
    //          unless concurrentManagedAccess = 1
    // Note we have not yet synchronized, so "kernel" is still active.
    *also_managed = 2;          // Will issue segmentation fault
    // Point 3: Concurrent GPU kernels can access the same data.
    kernel<<< 1, 1, 0, stream2 >>>(managed);
    // Point 4: Multi-GPU concurrent access is also permitted.
    cudaSetDevice(1);
    kernel<<< 1, 1 >>>(managed);
    return   0;
}
```

*   **Point 1:** The CPU accesses `non_managed` while the GPU is running `kernel` on `managed`. This is permitted because `non_managed` is non-managed zero-copy data [CUDA_C_Programming_Guide:L21907-L21943].
*   **Point 2:** The CPU attempts to access `also_managed` (managed memory) while the GPU is still active. This will issue a segmentation fault unless `concurrentManagedAccess` is 1 [CUDA_C_Programming_Guide:L21907-L21943].
*   **Point 3:** A second kernel runs concurrently on a different stream, accessing the same `managed` data. This is permitted [CUDA_C_Programming_Guide:L21907-L21943].
*   **Point 4:** A kernel is launched on a different GPU (Device 1) accessing the same managed memory. This is permitted subject to standard multi-GPU non-managed memory constraints [CUDA_C_Programming_Guide:L21907-L21943].
