# Stream Association Examples

Associating data with a stream allows fine-grained control over CPU + GPU concurrency. However, developers must keep in mind what data is visible to which streams, particularly when using devices of compute capability lower than 6.0 [CUDA_C_Programming_Guide:L21967-L22008].

## Associating Data with the Host

Explicitly associating a variable with host accessibility enables access from the CPU at all times, even while a kernel is running on the GPU. This is achieved using `cudaStreamAttachMemAsync` with the `cudaMemcpyAttachHost` flag [CUDA_C_Programming_Guide:L21967-L22008].

```cpp
__device__ __managed__ int x, y=2;
__global__ void kernel() {
    x = 10;
}
int main() {
    cudaStream_t stream1;
    cudaStreamCreate(&stream1);
    cudaStreamAttachMemAsync(stream1, &y, 0, cudaMemcpyAttachHost);
    cudaDeviceSynchronize();          // Wait for Host attachment to occur.
    kernel<<< 1, 1, 0, stream1 >>>(); // Note: Launches into stream1.
    y = 20;                               // Success - a kernel is running but "y"
                                // has been associated with no stream.
    return  0;
}
```

In this example, `y` is associated with the host, allowing the CPU to write `y = 20` concurrently with the kernel execution. Note that there is no `cudaDeviceSynchronize()` before the access to `y` [CUDA_C_Programming_Guide:L21967-L22008]. However, because `y` is accessible by the CPU while the GPU kernel is running, accesses to `y` by the GPU will produce undefined results [CUDA_C_Programming_Guide:L21967-L22008].

## Associating Data with a Specific Stream

Associating a variable with a specific stream restricts its accessibility to that stream. Crucially, associating one variable with a stream does not change the association status of other variables [CUDA_C_Programming_Guide:L21967-L22008].

```cpp
__device__ __managed__ int x, y=2;
__global__ void kernel() {
    x = 10;
}
int main() {
    cudaStream_t stream1;
    cudaStreamCreate(&stream1);
    cudaStreamAttachMemAsync(stream1, &x); // Associate "x" with stream1.
    cudaDeviceSynchronize();          // Wait for "x" attachment to occur.
    kernel<<< 1, 1, 0, stream1 >>>();
    y = 20;                                // ERROR: "y" is still associated globally
                                        // with all streams by default
    return  0;
}
```

In this code, `x` is associated with `stream1`. However, `y` remains associated globally with all streams by default. Consequently, attempting to access `y` from the host while a kernel is running in `stream1` causes an error, because `y` is still considered accessible by the GPU via that stream [CUDA_C_Programming_Guide:L21967-L22008].

## Key Takeaways

1.  **Host Association**: Use `cudaMemcpyAttachHost` to allow concurrent CPU access to managed memory while GPU kernels run. Be aware that this leads to undefined behavior if the GPU also accesses the same memory concurrently [CUDA_C_Programming_Guide:L21967-L22008].
2.  **Stream Association**: Associating a variable with a stream restricts its visibility to that stream. Other variables remain globally accessible unless explicitly associated [CUDA_C_Programming_Guide:L21967-L22008].
3.  **Independence**: Stream association is per-variable. Associating `x` with a stream does not automatically associate `y` with the same stream or restrict `y`'s accessibility [CUDA_C_Programming_Guide:L21967-L22008].
4.  **Synchronization**: When attaching memory, use `cudaDeviceSynchronize()` to ensure the attachment operation completes before proceeding, ensuring the new association rules are in effect [CUDA_C_Programming_Guide:L21967-L22008].
5.  **Compute Capability**: These behaviors are particularly relevant for devices with compute capability lower than 6.0 [CUDA_C_Programming_Guide:L21967-L22008].
