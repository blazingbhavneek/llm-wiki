# cudaMemPoolReuseFollowEventDependencies

`cudaMemPoolReuseFollowEventDependencies` is a memory pool attribute that modifies the behavior of the CUDA asynchronous memory allocator (`cudaMallocAsync`/`cudaFreeAsync`). When enabled, the allocator examines dependency information established by CUDA events to determine if memory freed in one stream can be safely reused for allocations in another stream.

## Mechanism

By default, the allocator may restrict reuse of freed memory across streams to ensure correctness. However, when this policy is active, the allocator leverages event dependencies to relax these restrictions. Specifically, if a stream waits on an event that was recorded after a `cudaFreeAsync` call in another stream, the allocator recognizes that the memory has been freed and is no longer in use. This allows the allocator to reuse that memory block to satisfy a new allocation request in the waiting stream, improving memory utilization and reducing the need for additional physical GPU memory allocations.

## Example Usage

The following code snippet demonstrates how `cudaMemPoolReuseFollowEventDependencies` enables memory reuse across streams:

```cpp
cudaMallocAsync(&ptr, size, originalStream);
kernel<<<..., originalStream>>>(ptr, ...);
cudaFreeAsync(ptr, originalStream);
cudaEventRecord(event, originalStream);

// waiting on the event that captures the free in another stream
// allows the allocator to reuse the memory to satisfy
// a new allocation request in the other stream when
// cudaMemPoolReuseFollowEventDependencies is enabled.
cudaStreamWaitEvent(otherStream, event);
cudaMallocAsync(&ptr2, size, otherStream);
```

In this example:
1. Memory `ptr` is allocated and used in `originalStream`.
2. The memory is freed asynchronously in `originalStream`.
3. An event is recorded in `originalStream` after the free operation.
4. `otherStream` waits on this event.
5. When `cudaMallocAsync` is called in `otherStream`, the allocator sees that the event dependency confirms the previous memory is free, allowing `ptr2` to potentially reuse the same physical memory block as `ptr`.

## References

- [CUDA_C_Programming_Guide:L15613-L15630] CUDA C++ Programming Guide, Section 15.9.1. cudaMemPoolReuseFollowEventDependencies
