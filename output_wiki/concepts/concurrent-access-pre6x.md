# Coherency and Concurrency Constraints on Pre-6.x

Explains that simultaneous CPU/GPU access is not possible on pre-6.x GPUs due to coherency guarantees, the role of the concurrentManagedAccess property, and the requirement for explicit synchronization.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L21848-L21897

Citation: [CUDA_C_Programming_Guide:L21848-L21897]

````text
## 24.3.2.4 Coherency and Concurrency

Simultaneous access to managed memory on devices of compute capability lower than 6.0 is not possible, because coherence could not be guaranteed if the CPU accessed a Unified Memory allocation while a GPU kernel was active.

## 24.3.2.4.1 GPU Exclusive Access To Managed Memory

To ensure coherency on pre-6.x GPU architectures, the Unified Memory programming model puts constraints on data accesses while both the CPU and GPU are executing concurrently. In efect, the GPU has exclusive access to all managed data while any kernel operation is executing, regardless of whether the specific kernel is actively using the data. When managed data is used with cudaMemcpy\*() or cudaMemset\*(), the system may choose to access the source or destination from the host or the device, which will put constraints on concurrent CPU access to that data while the cudaMemcpy\*() or cudaMemset\*() is executing. See Memcpy()/Memset() Behavior With Unified Memory for further details.

It is not permitted for the CPU to access any managed allocations or variables while the GPU is active for devices with concurrentManagedAccess property set to 0. On these systems concurrent CPU/GPU accesses, even to diferent managed memory allocations, will cause a segmentation fault because the page is considered inaccessible to the CPU.

```txt
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

In example above, the GPU program kernel is still active when the CPU touches y. (Note how it occurs before cudaDeviceSynchronize().) The code runs successfully on devices of compute capability 6.x due to the GPU page faulting capability which lifts all restrictions on simultaneous access. However, such memory access is invalid on pre-6.x architectures even though the CPU is accessing diferent data than the GPU. The program must explicitly synchronize with the GPU before accessing y:

```txt
__device__ __managed__ int x, y=2;
__global__ void kernel() {
    x = 10;
}
int main() {
    kernel<<< 1, 1 >>>();
```

(continues on next page)

(continued from previous page)

```txt
cudaDeviceSynchronize();
y = 20;          // Success on GPUs not supporting concurrent access
return  0;
}
```

As this example shows, on systems with pre-6.x GPU architectures, a CPU thread may not access any managed data in between performing a kernel launch and a subsequent synchronization call, regardless of whether the GPU kernel actually touches that same data (or any managed data at all). The mere potential for concurrent CPU and GPU access is suficient for a process-level exception to be raised.

Note that if memory is dynamically allocated with cudaMallocManaged() or cuMemAllocManaged() while the GPU is active, the behavior of the memory is unspecified until additional work is launched or the GPU is synchronized. Attempting to access the memory on the CPU during this time may or may not cause a segmentation fault. This does not apply to memory allocated using the flag cudaMemAttachHost or CU\_MEM\_ATTACH\_HOST.
````
