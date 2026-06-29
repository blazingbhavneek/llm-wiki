# cudaMallocAsync and cudaFreeAsync

`cudaMallocAsync` and `cudaFreeAsync` form the core of the Stream Ordered Memory Allocator in CUDA. These APIs allow for asynchronous memory allocation and deallocation, improving performance by decoupling memory management from the CPU execution thread. Both functions accept a stream argument to define when the allocation becomes available or when the memory is freed.

## API Fundamentals

### cudaMallocAsync
`cudaMallocAsync` returns an allocation pointer. The pointer value is determined synchronously and is immediately available for constructing future work on the CPU side. However, the actual allocation on the GPU is asynchronous and depends on the specified stream.

*   **Device Determination**: `cudaMallocAsync` ignores the current device/context when determining where the allocation resides. Instead, it determines the resident device based on the specified memory pool or the supplied stream [CUDA_C_Programming_Guide:L15429-L15484].
*   **Simplest Use Pattern**: The most common usage involves allocating, using, and freeing memory within the same stream, such as the per-thread stream [CUDA_C_Programming_Guide:L15429-L15484].

```cpp
void *ptr;
size_t size = 512;
cudaMallocAsync(&ptr, size, cudaStreamPerThread);
// do work using the allocation
kernel<<<..., cudaStreamPerThread>>>(ptr, ...);
```

### cudaFreeAsync
`cudaFreeAsync` inserts a free operation into the specified stream. This allows the CPU to continue execution without waiting for the GPU to complete the deallocation [CUDA_C_Programming_Guide:L15429-L15484].

```cpp
cudaFreeAsync(ptr, cudaStreamPerThread);
```

## Synchronization and Safety

Because allocations are asynchronous, strict synchronization guarantees are required to avoid undefined behavior when sharing memory across streams or mixing allocation APIs.

### Cross-Stream Access
When an allocation is used in a stream other than the one it was allocated in, the user must guarantee that access happens only after the allocation operation is complete. This can be achieved by:
1.  Synchronizing the allocating stream.
2.  Using CUDA events to synchronize the producing and consuming streams [CUDA_C_Programming_Guide:L15429-L15484].

Example of cross-stream usage with events:
```cpp
cudaMallocAsync(&ptr, size, stream1);
cudaEventRecord(event1, stream1);
// stream2 must wait for the allocation to be ready before accessing
cudaStreamWaitEvent(stream2, event1);
kernel<<<..., stream2>>>(ptr, ...);
cudaEventRecord(event2, stream2);
// stream3 must wait for stream2 to finish accessing the allocation before
// freeing the allocation
cudaStreamWaitEvent(stream3, event2);
cudaFreeAsync(ptr, stream3);
```

### Freeing Allocations
*   **Freeing with `cudaFreeAsync`**: The user must guarantee that the free operation happens after the allocation operation and any use of the allocation. Any use of the allocation after the free operation starts results in undefined behavior. Events and/or stream synchronization should be used to ensure all accesses on other streams are complete before the freeing stream begins [CUDA_C_Programming_Guide:L15429-L15484].
*   **Freeing `cudaMalloc` with `cudaFreeAsync`**: Users can free memory allocated with `cudaMalloc` using `cudaFreeAsync`. The same guarantees regarding access completion must be maintained [CUDA_C_Programming_Guide:L15429-L15484].

```cpp
cudaMalloc(&ptr, size);
kernel<<<..., stream>>>(ptr, ...);
cudaFreeAsync(ptr, stream);
```

*   **Freeing `cudaMallocAsync` with `cudaFree`**: Users can free memory allocated with `cudaMallocAsync` using the standard `cudaFree` API. When using `cudaFree`, the driver assumes all accesses to the allocation are complete and performs no further synchronization. The user must explicitly synchronize (e.g., `cudaStreamSynchronize`, `cudaEventSynchronize`, or `cudaDeviceSynchronize`) to guarantee that asynchronous work is complete before the memory is freed [CUDA_C_Programming_Guide:L15429-L15484].

```cpp
cudaMallocAsync(&ptr, size, stream);
kernel<<<..., stream>>>(ptr, ...);
// synchronize is needed to avoid prematurely freeing the memory
cudaStreamSynchronize(stream);
cudaFree(ptr);
```
