# Accessing and Freeing Graph Memory Outside of the Allocating Graph

Graph memory allocations do not have to be freed by the graph that created them. When a graph does not explicitly free an allocation, that allocation persists in device memory beyond the execution of the graph. This allows the memory to be accessed by subsequent CUDA operations, including those in other graphs or direct stream operations, as long as proper ordering is established.

## Accessing Allocated Memory

Allocated memory can be accessed in two primary ways outside the allocating graph:

1.  **In another graph:** The memory pointer can be passed to a kernel node in a different graph. The access must be ordered after the allocation through graph dependencies, CUDA events, or other stream ordering mechanisms.
2.  **Directly using a stream operation:** Host code or kernels launched on a stream can access the pointer returned by the allocation node, provided the operation is ordered after the allocation.

## Freeing Memory

An allocation that was not freed by its originating graph can be freed later through several mechanisms:

*   **Regular CUDA calls:** Using `cudaFree` or `cudaFreeAsync`.
*   **Another graph:** Launching a graph that contains a `cudaGraphAddMemFreeNode` targeting the specific pointer.
*   **Re-launching the allocating graph:** If the graph was instantiated with the `cudaGraphInstantiateFlagAutoFreeOnLaunch` flag, the memory will be automatically freed upon subsequent launches of that graph instance.

It is illegal to access memory after it has been freed. The free operation must be strictly ordered after all operations accessing the memory. This ordering must be guaranteed using graph dependencies, CUDA events, and other stream ordering mechanisms.

## Ordering and Synchronization

Because graph allocations may share underlying physical memory with each other, Virtual Aliasing Support rules relating to consistency and coherency must be considered. Specifically, the free operation must be ordered after the full device operation (e.g., compute kernel or memcpy) completes.

**Out-of-band synchronization is insufficient.** For example, a handshake through memory as part of a compute kernel that accesses the graph-allocated memory does not provide sufficient ordering guarantees between the memory writes to graph memory and the free operation of that graph memory.

### Methods for Establishing Ordering

#### 1. Using a Single Stream
Ordering is implicit if all operations occur on the same stream. The allocation, usage, and free must be sequenced correctly within that stream.

```c
void *dptr;
cudaGraphAddMemAllocNode(&allocNode, allocGraph, NULL, 0, &params);
dptr = params.dptr;

cudaGraphInstantiate(&allocGraphExec, allocGraph, NULL, NULL, 0);

cudaGraphLaunch(allocGraphExec, stream);
kernel<<< ..., stream >>>(dptr, ...);
cudaFreeAsync(dptr, stream);
```

#### 2. Using Events Between Streams
When accessing memory across different streams, CUDA events must be used to establish dependencies.

```c
void *dptr;

// Contents of allocating graph
cudaGraphAddMemAllocNode(&allocNode, allocGraph, NULL, 0, &params);
dptr = params.dptr;

// contents of consuming/freeing graph
nodeParams->kernelParams[0] = params.dptr;
cudaGraphAddKernelNode(&a, graph, NULL, 0, &nodeParams);
cudaGraphAddMemFreeNode(&freeNode, freeGraph, &a, 1, dptr);

cudaGraphInstantiate(&allocGraphExec, allocGraph, NULL, NULL, 0);
cudaGraphInstantiate(&freeGraphExec, freeGraph, NULL, NULL, 0);

cudaGraphLaunch(allocGraphExec, allocStream);

// establish the dependency of stream2 on the allocation node
cudaEventRecord(allocEvent, allocStream);
cudaStreamWaitEvent(stream2, allocEvent);

kernel<<< ..., stream2 >>> (dptr, ...);

// establish the dependency between the stream 3 and the allocation use
cudaStreamRecordEvent(streamUseDoneEvent, stream2);
cudaStreamWaitEvent(stream3, streamUseDoneEvent);

// it is now safe to launch the freeing graph
cudaGraphLaunch(freeGraphExec, stream3);
```

#### 3. Using Graph External Event Nodes
Events can be baked directly into the graphs using event record and wait nodes to manage dependencies between graphs.

```c
void *dptr;
cudaEvent_t allocEvent; // event indicating when the allocation will be ready for use.
cudaEvent_t streamUseDoneEvent; // event indicating when the stream operations are done with the allocation.

// Contents of allocating graph with event record node
cudaGraphAddMemAllocNode(&allocNode, allocGraph, NULL, 0, &params);
dptr = params.dptr;
// note: this event record node depends on the alloc node
cudaGraphAddEventRecordNode(&recordNode, allocGraph, &allocNode, 1, allocEvent);
cudaGraphInstantiate(&allocGraphExec, allocGraph, NULL, NULL, 0);

// contents of consuming/freeing graph with event wait nodes
cudaGraphAddEventWaitNode(&streamUseDoneEventNode, waitAndFreeGraph, NULL, 0, streamUseDoneEvent);
cudaGraphAddEventWaitNode(&allocReadyEventNode, waitAndFreeGraph, NULL, 0, allocEvent);
nodeParams->kernelParams[0] = params.dptr;

// The allocReadyEventNode provides ordering with the alloc node for use in a consuming graph.
cudaGraphAddKernelNode(&kernelNode, waitAndFreeGraph, &allocReadyEventNode, 1, &nodeParams);

// The free node has to be ordered after both external and internal users.
// Thus the node must depend on both the kernelNode and the streamUseDoneEventNode.
dependencies[0] = kernelNode;
dependencies[1] = streamUseDoneEventNode;
cudaGraphAddMemFreeNode(&freeNode, waitAndFreeGraph, &dependencies, 2, dptr);
cudaGraphInstantiate(&waitAndFreeGraphExec, waitAndFreeGraph, NULL, NULL, 0);

cudaGraphLaunch(allocGraphExec, allocStream);

// establish the dependency of stream2 on the event node satisfies the ordering requirement
cudaStreamWaitEvent(stream2, allocEvent);
kernel<<< ..., stream2 >>> (dptr, ...);
cudaStreamRecordEvent(streamUseDoneEvent, stream2);

// the event wait node in the waitAndFreeGraphExec establishes the dependency on the
// "readyForFreeEvent" that is needed to prevent the kernel running in stream two from
// accessing the allocation after the free node in execution order.
cudaGraphLaunch(waitAndFreeGraphExec, stream3);
```

## References

[CUDA_C_Programming_Guide:L16022-L16131]
