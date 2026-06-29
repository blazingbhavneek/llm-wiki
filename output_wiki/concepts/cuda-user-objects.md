# CUDA User Objects

CUDA User Objects are a feature designed to manage the lifetime of resources used by asynchronous work in CUDA, particularly within the context of CUDA Graphs and stream capture [CUDA_C_Programming_Guide:L2577-L2669]. They address compatibility issues where traditional resource management schemes, such as event-based pools or synchronous-create/asynchronous-destroy patterns, fail when used with graphs due to non-fixed pointers or the need for synchronous CPU code during submission [CUDA_C_Programming_Guide:L2577-L2669].

## Concept and Mechanism

A CUDA user object associates a user-specified destructor callback with an internal reference count, functioning similarly to a C++ `shared_ptr` [CUDA_C_Programming_Guide:L2577-L2669]. References can be owned by user code on the CPU and by CUDA graphs [CUDA_C_Programming_Guide:L2577-L2669]. Unlike C++ smart pointers, there is no object representing the reference for user-owned references; users must track these manually [CUDA_C_Programming_Guide:L2577-L2669]. A typical workflow involves immediately transferring the sole user-owned reference to a CUDA graph after creation [CUDA_C_Programming_Guide:L2577-L2669].

### Reference Management

When a reference is associated with a CUDA graph, CUDA manages the graph operations automatically [CUDA_C_Programming_Guide:L2577-L2669]. The retention rules are as follows:

*   **Cloning:** A cloned `cudaGraph_t` retains a copy of every reference owned by the source `cudaGraph_t`, with the same multiplicity [CUDA_C_Programming_Guide:L2577-L2669].
*   **Instantiation:** An instantiated `cudaGraphExec_t` retains a copy of every reference in the source `cudaGraph_t` [CUDA_C_Programming_Guide:L2577-L2669].
*   **Execution and Destruction:** When a `cudaGraphExec_t` is destroyed without being synchronized, the references are retained until the execution is completed [CUDA_C_Programming_Guide:L2577-L2669].

References owned by graphs in child graph nodes are associated with the child graphs, not the parents [CUDA_C_Programming_Guide:L2577-L2669]. If a child graph is updated or deleted, the references change accordingly [CUDA_C_Programming_Guide:L2577-L2669]. If an executable graph or child graph is updated via `cudaGraphExecUpdate` or `cudaGraphExecChildGraphNodeSetParams`, the references in the new source graph are cloned and replace the references in the target graph [CUDA_C_Programming_Guide:L2577-L2669]. In either case, if previous launches are not synchronized, any references that would be released are held until the launches have finished executing [CUDA_C_Programming_Guide:L2577-L2669].

## Usage Example

The following example demonstrates the lifecycle of a CUDA User Object:

1.  **Creation:** The object is created using `cudaUserObjectCreate`, specifying an initial reference count and flags [CUDA_C_Programming_Guide:L2577-L2669]. The `cudaUserObjectNoDestructorSync` flag acknowledges that the callback cannot be waited on via CUDA [CUDA_C_Programming_Guide:L2577-L2669].
2.  **Graph Retention:** The reference is transferred to a graph using `cudaGraphRetainUserObject` with the `cudaGraphUserObjectMove` flag, which transfers ownership without modifying the total reference count [CUDA_C_Programming_Guide:L2577-L2669].
3.  **Instantiation:** The graph is instantiated into a `cudaGraphExec_t`, which retains a new reference [CUDA_C_Programming_Guide:L2577-L2669].
4.  **Launch and Destruction:** The graph is launched asynchronously. When the executable graph is destroyed, the reference is not immediately released because the launch is not synchronized [CUDA_C_Programming_Guide:L2577-L2669].
5.  **Synchronization:** After synchronizing the stream, the remaining reference is released, and the destructor executes asynchronously [CUDA_C_Programming_Guide:L2577-L2669].

```cpp
cudaGraph_t graph;  // Preexisting graph

Object *object = new Object;  // C++ object with possibly nontrivial destructor
cudaUserObject_t cuObject;
cudaUserObjectCreate(
    &cuObject,
    object,  // Here we use a CUDA-provided template wrapper for this API,
                   // which supplies a callback to delete the C++ object pointer
    1,  // Initial refcount
    cudaUserObjectNoDestructorSync  // Acknowledge that the callback cannot be
                              // waited on via CUDA
);
cudaGraphRetainUserObject(
    graph,
    cuObject,
    1,  // Number of references
    cudaGraphUserObjectMove  // Transfer a reference owned by the caller (do
                             // not modify the total reference count)
);

// No more references owned by this thread; no need to call release API
cudaGraphExec_t graphExec;
cudaGraphInstantiate(&graphExec, graph, nullptr, nullptr, 0); // Will retain a
// new reference
cudaGraphDestroy(graph); // graphExec still owns a reference
cudaGraphLaunch(graphExec, 0); // Async launch has access to the user objects
cudaGraphExecDestroy(graphExec); // Launch is not synchronized; the release
// will be deferred if needed
cudaStreamSynchronize(0); // After the launch is synchronized, the remaining
// reference is released and the destructor will
// execute. Note this happens asynchronously.
// If the destructor callback had signaled a synchronization object, it would
// be safe to wait on it at this point.
```

## Constraints and Best Practices

There is no mechanism to wait on user object destructors via a CUDA API [CUDA_C_Programming_Guide:L2577-L2669]. Users may signal a synchronization object manually from the destructor code [CUDA_C_Programming_Guide:L2577-L2669].

It is not legal to call CUDA APIs from the destructor, similar to the restriction on `cudaLaunchHostFunc` [CUDA_C_Programming_Guide:L2577-L2669]. This restriction exists to avoid blocking a CUDA internal shared thread and preventing forward progress [CUDA_C_Programming_Guide:L2577-L2669]. It is legal to signal another thread to perform an API call, provided the dependency is one-way and the thread performing the call cannot block the forward progress of CUDA work [CUDA_C_Programming_Guide:L2577-L2669].

`cudaUserObjectCreate` is the primary entry point for creating user objects and serves as a starting point for browsing related APIs [CUDA_C_Programming_Guide:L2577-L2669].
