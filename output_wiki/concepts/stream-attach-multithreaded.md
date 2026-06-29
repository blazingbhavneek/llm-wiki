# Stream Attach with Multithreaded Host Programs

The primary use for `cudaStreamAttachMemAsync()` is to enable independent task parallelism using CPU threads [CUDA_C_Programming_Guide:L22014-L22016]. In a typical multithreaded program, each CPU thread creates its own stream for all work it generates to avoid dependencies that would arise if CUDA’s NULL stream were used [CUDA_C_Programming_Guide:L22016-L22018].

## Problem: Global Visibility

The default global visibility of managed data to any GPU stream can make it difficult to avoid interactions between CPU threads in a multi-threaded program [CUDA_C_Programming_Guide:L22019-L22021]. Without explicit attachment, the system conservatively assumes that a kernel might access data not explicitly associated with a stream, potentially preventing CPU access to that data [CUDA_C_Programming_Guide:L22009-L22013].

## Solution: Stream Attachment

The function `cudaStreamAttachMemAsync()` is used to associate a thread’s managed allocations with that thread’s own stream [CUDA_C_Programming_Guide:L22021-L22023]. This association is typically not changed for the life of the thread [CUDA_C_Programming_Guide:L22023].

### Implementation Example

A program can use unified memory for data accesses by adding a single call to `cudaStreamAttachMemAsync()` after allocation [CUDA_C_Programming_Guide:L22024-L22025]. The following example demonstrates a function that performs a task in its own private stream:

```aidl
// This function performs some task, in its own private stream.
void run_task(int *in, int *out, int length) {
    // Create a stream for us to use.
    cudaStream_t stream;
    cudaStreamCreate(&stream);
    // Allocate some managed data and associate with our stream.
    // Note the use of the host-attach flag to cudaMallocManaged();
    // we then associate the allocation with our stream so that
    // our GPU kernel launches can access it.
    int *data;
    cudaMallocManaged((void **)&data, length, cudaMemcpyAttachHost);
    cudaStreamAttachMemAsync(stream, data);
    cudaStreamSynchronize(stream);
    // Iterate on the data in some way, using both Host & Device.
    for(int i=0; i<N; i++) {
        transform<<< 100, 256, 0, stream >>>(in, data, length);
        cudaStreamSynchronize(stream);
        host_process(data, length);      // CPU uses managed data.
        convert<<< 100, 256, 0, stream >>>(out, data, length);
    }
    cudaStreamSynchronize(stream);
    cudaStreamDestroy(stream);
    cudaFree(data);
}
```

In this example, the allocation-stream association is established just once, and then data is used repeatedly by both the host and device [CUDA_C_Programming_Guide:L22039-L22041]. This results in much simpler code than explicitly copying data between host and device, while achieving the same result [CUDA_C_Programming_Guide:L22041-L22043].

## Key Considerations

*   **Stream Creation**: Each thread should create its own `cudaStream_t` to ensure independence [CUDA_C_Programming_Guide:L22016-L22018].
*   **Allocation Flags**: The example uses `cudaMallocManaged` with the `cudaMemcpyAttachHost` flag, which is then associated with the stream via `cudaStreamAttachMemAsync` [CUDA_C_Programming_Guide:L22029-L22031].
*   **Synchronization**: `cudaStreamSynchronize` is used to ensure the stream is idle before accessing data from the CPU or before destroying the stream [CUDA_C_Programming_Guide:L22032, L22034, L22036, L22038].
*   **Resource Cleanup**: The stream must be destroyed and the memory freed after use [CUDA_C_Programming_Guide:L22039-L22040].
