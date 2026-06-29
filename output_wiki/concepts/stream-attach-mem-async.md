# Managing Data Visibility with cudaStreamAttachMemAsync

The `cudaStreamAttachMemAsync()` function provides a mechanism for finer-grained control over managed memory visibility, designed to work on all devices supporting managed memory, including older architectures where `concurrentManagedAccess` is 0 [CUDA_C_Programming_Guide:L21944-L21966].

## Background: Stream Independence and Unified Memory

The CUDA programming model uses streams to indicate dependence and independence among kernel launches. Kernels in the same stream execute consecutively, while those in different streams may execute concurrently [CUDA_C_Programming_Guide:L21944-L21966]. Unified Memory builds on this stream-independence model by allowing programs to explicitly associate managed allocations with a specific CUDA stream [CUDA_C_Programming_Guide:L21944-L21966].

## Function Signature and Behavior

The function signature is:

```cpp
cudaError_t cudaStreamAttachMemAsync(cudaStream_t stream,
                                      void *ptr,
                                      size_t length=0,
                                      unsigned int flags=0);
```

This function associates `length` bytes of memory starting from `ptr` with the specified `stream` [CUDA_C_Programming_Guide:L21944-L21966]. Currently, `length` must always be 0 to indicate that the entire region should be attached [CUDA_C_Programming_Guide:L21944-L21966].

## Visibility Rules

### Default Behavior
If an allocation is not associated with a specific stream, it is visible to all running kernels regardless of their stream [CUDA_C_Programming_Guide:L21944-L21966]. This is the default visibility for allocations created with `cudaMallocManaged()` or `__managed__` variables [CUDA_C_Programming_Guide:L21944-L21966]. Consequently, the simple-case rule applies: the CPU may not touch the data while any kernel is running [CUDA_C_Programming_Guide:L21944-L21966].

### Attached Behavior
By associating an allocation with a specific stream, the program guarantees that only kernels launched into that stream will touch that data [CUDA_C_Programming_Guide:L21944-L21966]. The Unified Memory system allows CPU access to this memory region so long as all operations in that specific stream have completed, regardless of whether other streams are active [CUDA_C_Programming_Guide:L21944-L21966].

This effectively constrains the exclusive ownership of the managed memory region by an active GPU to per-stream activity instead of whole-GPU activity [CUDA_C_Programming_Guide:L21944-L21966].

## Programmer Responsibility

No error checking is performed by the Unified Memory system to verify that only the associated stream accesses the data [CUDA_C_Programming_Guide:L21944-L21966]. It is the programmer’s responsibility to ensure that this guarantee is honored [CUDA_C_Programming_Guide:L21944-L21966].

## Performance Implications

In addition to allowing greater concurrency, the use of `cudaStreamAttachMemAsync()` can enable data transfer optimizations within the Unified Memory system, which may affect latencies and other overhead [CUDA_C_Programming_Guide:L21944-L21966].
