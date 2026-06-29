# Stream Capture Graph Memory

Graph memory nodes can be created by capturing the corresponding stream-ordered allocation and free calls, specifically `cudaMallocAsync` and `cudaFreeAsync` [CUDA_C_Programming_Guide:L15987-L16021].

When these APIs are captured, the virtual addresses returned by the allocation API can be used by other operations inside the graph [CUDA_C_Programming_Guide:L15987-L16021]. Since stream-ordered dependencies are captured into the graph, the ordering requirements of the stream-ordered allocation APIs guarantee that the graph memory nodes will be properly ordered with respect to the captured stream operations, provided the stream code is correctly written [CUDA_C_Programming_Guide:L15987-L16021].

## Example Usage

The following code snippet demonstrates how to use stream capture to create a graph involving memory allocation, kernel execution across multiple streams, and memory freeing [CUDA_C_Programming_Guide:L15987-L16021]:

```txt
cudaMallocAsync(&dptr, size, stream1);
kernel_A<<< ..., stream1 >>>(dptr, ...);

// Fork into stream2
cudaEventRecord(event1, stream1);
cudaStreamWaitEvent(stream2, event1);

kernel_B<<< ..., stream1 >>>(dptr, ...);
// event dependencies translated into graph dependencies, so the kernel node created
// by the capture of kernel C will depend on the allocation node created by capturing
// the cudaMallocAsync call.
kernel_C<<< ..., stream2 >>>(dptr, ...);

// Join stream2 back to origin stream (stream1)
cudaEventRecord(event2, stream2);
cudaStreamWaitEvent(stream1, event2);

// Free depends on all work accessing the memory.
cudaFreeAsync(dptr, stream1);

// End capture in the origin stream
cudaStreamEndCapture(stream1, &graph);
```

In this example, `kernel_C` depends on the allocation node created by capturing the `cudaMallocAsync` call due to the translation of event dependencies into graph dependencies [CUDA_C_Programming_Guide:L15987-L16021]. The `cudaFreeAsync` call ensures that the memory is freed only after all work accessing the memory has completed [CUDA_C_Programming_Guide:L15987-L16021].
