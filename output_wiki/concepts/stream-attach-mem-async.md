# Managing Data Visibility with cudaStreamAttachMemAsync

Explains how cudaStreamAttachMemAsync() associates managed allocations with specific streams to enable finer-grained CPU/GPU concurrency and data transfer optimizations.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L21944-L21967

Citation: [CUDA_C_Programming_Guide:L21944-L21967]

````text

## 24.3.2.4.3 Managing Data Visibility and Concurrent CPU + GPU Access with Streams

Until now it was assumed that for SM architectures before 6.x: 1) any active kernel may use any managed memory, and 2) it was invalid to use managed memory from the CPU while a kernel is active. Here we present a system for finer-grained control of managed memory designed to work on all devices supporting managed memory, including older architectures with concurrentManagedAccess equal to 0.

The CUDA programming model provides streams as a mechanism for programs to indicate dependence and independence among kernel launches. Kernels launched into the same stream are guaranteed to execute consecutively, while kernels launched into diferent streams are permitted to execute concurrently. Streams describe independence between work items and hence allow potentially greater eficiency through concurrency.

Unified Memory builds upon the stream-independence model by allowing a CUDA program to explicitly associate managed allocations with a CUDA stream. In this way, the programmer indicates the use of data by kernels based on whether they are launched into a specified stream or not. This enables opportunities for concurrency based on program-specific data access patterns. The function to control this behavior is:

```txt
cudaError_t cudaStreamAttachMemAsync(cudaStream_t stream,
                                      void *ptr,
                                      size_t length=0,
                                      unsigned int flags=0);
```

The cudaStreamAttachMemAsync() function associates length bytes of memory starting from ptr with the specified stream. (Currently, length must always be 0 to indicate that the entire region should be attached.) Because of this association, the Unified Memory system allows CPU access to this memory region so long as all operations in stream have completed, regardless of whether other streams are active. In efect, this constrains exclusive ownership of the managed memory region by an active GPU to per-stream activity instead of whole-GPU activity.

Most importantly, if an allocation is not associated with a specific stream, it is visible to all running kernels regardless of their stream. This is the default visibility for a cudaMallocManaged() allocation or a \_\_managed\_\_ variable; hence, the simple-case rule that the CPU may not touch the data while any kernel is running.

By associating an allocation with a specific stream, the program makes a guarantee that only kernels launched into that stream will touch that data. No error checking is performed by the Unified Memory system: it is the programmer’s responsibility to ensure that guarantee is honored.

In addition to allowing greater concurrency, the use of cudaStreamAttachMemAsync() can (and typically does) enable data transfer optimizations within the Unified Memory system that may afect latencies and other overhead.
````
