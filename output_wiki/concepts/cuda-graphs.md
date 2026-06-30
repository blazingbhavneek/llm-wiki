# CUDA Graphs

A model for work submission separating graph definition, instantiation, and execution to reduce CPU overhead and enable optimizations. Covers node types, edge data, creation via APIs or stream capture, cross-stream dependencies, user objects, and graph update mechanisms.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L2405-L2805

Citation: [CUDA_C_Programming_Guide:L2405-L2805]

````text
## 6.2.8.7 CUDA Graphs

CUDA Graphs present a new model for work submission in CUDA. A graph is a series of operations, such as kernel launches, connected by dependencies, which is defined separately from its execution. This allows a graph to be defined once and then launched repeatedly. Separating out the definition of a graph from its execution enables a number of optimizations: first, CPU launch costs are reduced compared to streams, because much of the setup is done in advance; second, presenting the whole workflow to CUDA enables optimizations which might not be possible with the piecewise work submission mechanism of streams.

To see the optimizations possible with graphs, consider what happens in a stream: when you place a kernel into a stream, the host driver performs a sequence of operations in preparation for the execution of the kernel on the GPU. These operations, necessary for setting up and launching the kernel, are an overhead cost which must be paid for each kernel that is issued. For a GPU kernel with a short execution time, this overhead cost can be a significant fraction of the overall end-to-end execution time.

Work submission using graphs is separated into three distinct stages: definition, instantiation, and execution.

During the definition phase, a program creates a description of the operations in the graph along with the dependencies between them.

▶ Instantiation takes a snapshot of the graph template, validates it, and performs much of the setup and initialization of work with the aim of minimizing what needs to be done at launch. The resulting instance is known as an executable graph.

▶ An executable graph may be launched into a stream, similar to any other CUDA work. It may be launched any number of times without repeating the instantiation.

## 6.2.8.7.1 Graph Structure

An operation forms a node in a graph. The dependencies between the operations are the edges. These dependencies constrain the execution sequence of the operations.

An operation may be scheduled at any time once the nodes on which it depends are complete. Scheduling is left up to the CUDA system.

## 6.2.8.7.1.1 Node Types

A graph node can be one of:

▶ kernel

▶ CPU function call

▶ memory copy

▶ memset

▶ empty node

▶ waiting on an event

▶ recording an event

▶ signalling an external semaphore

▶ waiting on an external semaphore

▶ conditional node

Graph Memory Nodes

▶ child graph: To execute a separate nested graph, as shown in the following figure.

![](images/e627eb7ed5feb1d7988d83c0d75cdbf1c2132b8919c80804901019a8fa6da261.jpg)  
Figure 13: Child Graph Example

## 6.2.8.7.1.2 Edge Data

CUDA 12.3 introduced edge data on CUDA Graphs. Edge data modifies a dependency specified by an edge and consists of three parts: an outgoing port, an incoming port, and a type. An outgoing port specifies when an associated edge is triggered. An incoming port specifies what portion of a node is dependent on an associated edge. A type modifies the relation between the endpoints.

Port values are specific to node type and direction, and edge types may be restricted to specific node types. In all cases, zero-initialized edge data represents default behavior. Outgoing port 0 waits on an entire task, incoming port 0 blocks an entire task, and edge type 0 is associated with a full dependency with memory synchronizing behavior.

Edge data is optionally specified in various graph APIs via a parallel array to the associated nodes. If it is omitted as an input parameter, zero-initialized data is used. If it is omitted as an output (query) parameter, the API accepts this if the edge data being ignored is all zero-initialized, and returns cudaErrorLossyQuery if the call would discard information.

Edge data is also available in some stream capture APIs: cudaStreamBeginCaptureToGraph(), cudaStreamGetCaptureInfo(), and cudaStreamUpdateCaptureDependencies(). In these cases, there is not yet a downstream node. The data is associated with a dangling edge (half edge) which will either be connected to a future captured node or discarded at termination of stream capture. Note that some edge types do not wait on full completion of the upstream node. These edges are ignored when considering if a stream capture has been fully rejoined to the origin stream, and cannot be discarded at the end of capture. See Creating a Graph Using Stream Capture.

Currently, no node types define additional incoming ports, and only kernel nodes define additional outgoing ports. There is one non-default dependency type, cudaGraphDependencyTypeProgrammatic, which enables Programmatic Dependent Launch between two kernel nodes.

## 6.2.8.7.2 Creating a Graph Using Graph APIs

Graphs can be created via two mechanisms: explicit API and stream capture. The following is an example of creating and executing the below graph.

```c
// Create the graph - it starts out empty
cudaGraphCreate(&graph, 0);

// For the purpose of this example, we'll create
// the nodes separately from the dependencies to
// demonstrate that it can be done in two stages.
// Note that dependencies can also be specified
// at node creation.
cudaGraphAddKernelNode(&a, graph, NULL, 0, &nodeParams);
cudaGraphAddKernelNode(&b, graph, NULL, 0, &nodeParams);
cudaGraphAddKernelNode(&c, graph, NULL, 0, &nodeParams);
cudaGraphAddKernelNode(&d, graph, NULL, 0, &nodeParams);

// Now set up dependencies on each node
cudaGraphAddDependencies(graph, &a, &b, NULL, 1);      // A->B
cudaGraphAddDependencies(graph, &a, &c, NULL, 1);     // A->C
cudaGraphAddDependencies(graph, &b, &d, NULL, 1);    // B->D
cudaGraphAddDependencies(graph, &c, &d, NULL, 1);     // C->D
```

![](images/8160529a4759d9ed714c25e730bb15b5976eab54d9a3f45003a614f802a977dd.jpg)  
Figure 14: Creating a Graph Using Graph APIs Example

## 6.2.8.7.3 Creating a Graph Using Stream Capture

Stream capture provides a mechanism to create a graph from existing stream-based APIs. A section of code which launches work into streams, including existing code, can be bracketed with calls to cudaStreamBeginCapture() and cudaStreamEndCapture(). See below.

```c
cudaGraph_t graph;

cudaStreamBeginCapture(stream);

kernel_A<<< ..., stream >>>(...);
kernel_B<<< ..., stream >>>(...);
libraryCall(stream);
kernel_C<<< ..., stream >>>(...);

cudaStreamEndCapture(stream, &graph);
```

A call to cudaStreamBeginCapture() places a stream in capture mode. When a stream is being captured, work launched into the stream is not enqueued for execution. It is instead appended to an internal graph that is progressively being built up. This graph is then returned by calling cudaStreamEndCapture(), which also ends capture mode for the stream. A graph which is actively being constructed by stream capture is referred to as a capture graph.

Stream capture can be used on any CUDA stream except cudaStreamLegacy (the “NULL stream”). Note that it can be used on cudaStreamPerThread. If a program is using the legacy stream, it may be possible to redefine stream 0 to be the per-thread stream with no functional change. See Default Stream.

Whether a stream is being captured can be queried with cudaStreamIsCapturing().

Work can be captured to an existing graph using cudaStreamBeginCaptureToGraph(). Instead of capturing to an internal graph, work is captured to a graph provided by the user.

## 6.2.8.7.3.1 Cross-stream Dependencies and Events

Stream capture can handle cross-stream dependencies expressed with cudaEventRecord() and cudaStreamWaitEvent(), provided the event being waited upon was recorded into the same capture graph.

When an event is recorded in a stream that is in capture mode, it results in a captured event. A captured event represents a set of nodes in a capture graph.

When a captured event is waited on by a stream, it places the stream in capture mode if it is not already, and the next item in the stream will have additional dependencies on the nodes in the captured event. The two streams are then being captured to the same capture graph.

When cross-stream dependencies are present in stream capture, cudaStreamEndCapture() must still be called in the same stream where cudaStreamBeginCapture() was called; this is the origin stream. Any other streams which are being captured to the same capture graph, due to event-based dependencies, must also be joined back to the origin stream. This is illustrated below. All streams being captured to the same capture graph are taken out of capture mode upon cudaStreamEndCapture(). Failure to rejoin to the origin stream will result in failure of the overall capture operation.

```txt
// stream1 is the origin stream
cudaStreamBeginCapture(stream1);

kernel_A<<< ..., stream1 >>>(...);

// Fork into stream2
cudaEventRecord(event1, stream1);
cudaStreamWaitEvent(stream2, event1);

kernel_B<<< ..., stream1 >>>(...);
kernel_C<<< ..., stream2 >>>(...);

// Join stream2 back to origin stream (stream1)
cudaEventRecord(event2, stream2);
cudaStreamWaitEvent(stream1, event2);

kernel_D<<< ..., stream1 >>>(...);

// End capture in the origin stream
cudaStreamEndCapture(stream1, &graph);

// stream1 and stream2 no longer in capture mode
```

Graph returned by the above code is shown in Figure 14.

Note: When a stream is taken out of capture mode, the next non-captured item in the stream (if any) will still have a dependency on the most recent prior non-captured item, despite intermediate items having been removed.

## 6.2.8.7.3.2 Prohibited and Unhandled Operations

It is invalid to synchronize or query the execution status of a stream which is being captured or a captured event, because they do not represent items scheduled for execution. It is also invalid to query the execution status of or synchronize a broader handle which encompasses an active stream capture, such as a device or context handle when any associated stream is in capture mode.

When any stream in the same context is being captured, and it was not created with cudaStream-NonBlocking, any attempted use of the legacy stream is invalid. This is because the legacy stream handle at all times encompasses these other streams; enqueueing to the legacy stream would create a dependency on the streams being captured, and querying it or synchronizing it would query or synchronize the streams being captured.

It is therefore also invalid to call synchronous APIs in this case. Synchronous APIs, such as cudaMemcpy(), enqueue work to the legacy stream and synchronize it before returning.

Note: As a general rule, when a dependency relation would connect something that is captured with something that was not captured and instead enqueued for execution, CUDA prefers to return an error rather than ignore the dependency. An exception is made for placing a stream into or out of capture mode; this severs a dependency relation between items added to the stream immediately before and after the mode transition.

It is invalid to merge two separate capture graphs by waiting on a captured event from a stream which is being captured and is associated with a diferent capture graph than the event. It is invalid to wait on a non-captured event from a stream which is being captured without specifying the cudaEventWaitExternal flag.

A small number of APIs that enqueue asynchronous operations into streams are not currently supported in graphs and will return an error if called with a stream which is being captured, such as cudaStreamAttachMemAsync().

## 6.2.8.7.3.3 Invalidation

When an invalid operation is attempted during stream capture, any associated capture graphs are invalidated. When a capture graph is invalidated, further use of any streams which are being captured or captured events associated with the graph is invalid and will return an error, until stream capture is ended with cudaStreamEndCapture(). This call will take the associated streams out of capture mode, but will also return an error value and a NULL graph.

## 6.2.8.7.4 CUDA User Objects

CUDA User Objects can be used to help manage the lifetime of resources used by asynchronous work in CUDA. In particular, this feature is useful for CUDA Graphs and stream capture.

Various resource management schemes are not compatible with CUDA graphs. Consider for example an event-based pool or a synchronous-create, asynchronous-destroy scheme.

```txt
// Library API with pool allocation
void libraryWork(cudaStream_t stream) {
    auto &resource = pool_claimTemporaryResource();
    resource.waitForReadyEventInStream(stream);
    launchWork(stream, resource);
```

(continues on next page)

```javascript
resource.recordReadyEvent(stream);
}
```

(continued from previous page)

```cpp
// Library API with asynchronous resource deletion
void libraryWork(cudaStream_t stream) {
    Resource *resource = new Resource(...);
    launchWork(stream, resource);
    cudaLaunchHostFunc(
        stream,
        [](void *resource) {
            delete static_cast<Resource *>(resource);
        },
        resource,
        0);
    // Error handling considerations not shown
}
```

These schemes are dificult with CUDA graphs because of the non-fixed pointer or handle for the resource which requires indirection or graph update, and the synchronous CPU code needed each time the work is submitted. They also do not work with stream capture if these considerations are hidden from the caller of the library, and because of use of disallowed APIs during capture. Various solutions exist such as exposing the resource to the caller. CUDA user objects present another approach.

A CUDA user object associates a user-specified destructor callback with an internal refcount, similar to C++ shared\_ptr. References may be owned by user code on the CPU and by CUDA graphs. Note that for user-owned references, unlike C++ smart pointers, there is no object representing the reference; users must track user-owned references manually. A typical use case would be to immediately move the sole user-owned reference to a CUDA graph after the user object is created.

When a reference is associated to a CUDA graph, CUDA will manage the graph operations automatically. A cloned cudaGraph\_t retains a copy of every reference owned by the source cudaGraph\_t, with the same multiplicity. An instantiated cudaGraphExec\_t retains a copy of every reference in the source cudaGraph\_t. When a cudaGraphExec\_t is destroyed without being synchronized, the references are retained until the execution is completed.

Here is an example use.

```txt
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
```

(continues on next page)

```cpp
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

References owned by graphs in child graph nodes are associated to the child graphs, not the parents. If a child graph is updated or deleted, the references change accordingly. If an executable graph or child graph is updated with cudaGraphExecUpdate or cudaGraphExecChildGraphNodeSetParams, the references in the new source graph are cloned and replace the references in the target graph. In either case, if previous launches are not synchronized, any references which would be released are held until the launches have finished executing.

There is not currently a mechanism to wait on user object destructors via a CUDA API. Users may signal a synchronization object manually from the destructor code. In addition, it is not legal to call CUDA APIs from the destructor, similar to the restriction on cudaLaunchHostFunc. This is to avoid blocking a CUDA internal shared thread and preventing forward progress. It is legal to signal another thread to perform an API call, if the dependency is one way and the thread doing the call cannot block forward progress of CUDA work.

User objects are created with cudaUserObjectCreate, which is a good starting point to browse related APIs.

## 6.2.8.7.5 Updating Instantiated Graphs

Work submission using graphs is separated into three distinct stages: definition, instantiation, and execution. In situations where the workflow is not changing, the overhead of definition and instantiation can be amortized over many executions, and graphs provide a clear advantage over streams.

A graph is a snapshot of a workflow, including kernels, parameters, and dependencies, in order to replay it as rapidly and eficiently as possible. In situations where the workflow changes the graph becomes out of date and must be modified. Major changes to graph structure such as topology or types of nodes will require re-instantiation of the source graph because various topology-related optimization techniques must be re-applied.

The cost of repeated instantiation can reduce the overall performance benefit from graph execution, but it is common for only node parameters, such as kernel parameters and cudaMemcpy addresses, to change while graph topology remains the same. For this case, CUDA provides a lightweight mechanism known as “Graph Update,” which allows certain node parameters to be modified in-place without having to rebuild the entire graph. This is much more eficient than re-instantiation.

Updates will take efect the next time the graph is launched, so they will not impact previous graph launches, even if they are running at the time of the update. A graph may be updated and relaunched repeatedly, so multiple updates/launches can be queued on a stream.

CUDA provides two mechanisms for updating instantiated graph parameters, whole graph update and individual node update. Whole graph update allows the user to supply a topologically identical cudaGraph\_t object whose nodes contain updated parameters. Individual node update allows the user to explicitly update the parameters of individual nodes. Using an updated cudaGraph\_t is more convenient when a large number of nodes are being updated, or when the graph topology is unknown to the caller (i.e., The graph resulted from stream capture of a library call). Using individual node update is preferred when the number of changes is small and the user has the handles to the nodes requiring updates. Individual node update skips the topology checks and comparisons for unchanged nodes, so it can be more eficient in many cases.

CUDA also provides a mechanism for enabling and disabling individual nodes without afecting their current parameters.

The following sections explain each approach in more detail.

## 6.2.8.7.5.1 Graph Update Limitations

Kernel nodes:

▶ The owning context of the function cannot change.

▶ A node whose function originally did not use CUDA dynamic parallelism cannot be updated to a function which uses CUDA dynamic parallelism.

cudaMemset and cudaMemcpy nodes:

▶ The CUDA device(s) to which the operand(s) was allocated/mapped cannot change.

▶ The source/destination memory must be allocated from the same context as the original source/destination memory.

▶ Only 1D cudaMemset/cudaMemcpy nodes can be changed.

Additional memcpy node restrictions:

Changing either the source or destination memory type (i.e., cudaPitchedPtr, cudaArray\_t, etc.), or the type of transfer (i.e., cudaMemcpyKind) is not supported.

External semaphore wait nodes and record nodes:

▶ Changing the number of semaphores is not supported.

## Conditional nodes:

▶ The order of handle creation and assignment must match between the graphs.

▶ Changing node parameters is not supported (i.e. number of graphs in the conditional, node context, etc).

▶ Changing parameters of nodes within the conditional body graph is subject to the rules above.

## Memory nodes:

▶ It is not possible to update a cudaGraphExec\_t with a cudaGraph\_t if the cudaGraph\_t is currently instantiated as a diferent cudaGraphExec\_t.

There are no restrictions on updates to host nodes, event record nodes, or event wait nodes.

## 6.2.8.7.5.2 Whole Graph Update

cudaGraphExecUpdate() allows an instantiated graph (the “original graph”) to be updated with the parameters from a topologically identical graph (the “updating” graph). The topology of the updating graph must be identical to the original graph used to instantiate the cudaGraphExec\_t. In addition, the order in which the dependencies are specified must match. Finally, CUDA needs to consistently order the sink nodes (nodes with no dependencies). CUDA relies on the order of specific api calls to achieve consistent sink node ordering.

More explicitly, following the following rules will cause cudaGraphExecUpdate() to pair the nodes in the original graph and the updating graph deterministically:

1. For any capturing stream, the API calls operating on that stream must be made in the same order, including event wait and other api calls not directly corresponding to node creation.

2. The API calls which directly manipulate a given graph node’s incoming edges (including captured stream APIs, node add APIs, and edge addition / removal APIs) must be made in the same order. Moreover, when dependencies are specified in arrays to these APIs, the order in which the dependencies are specified inside those arrays must match.

3. Sink nodes must be consistently ordered. Sink nodes are nodes without dependent nodes / outgoing edges in the final graph at the time of the cudaGraphExecUpdate() invocation. The following operations afect sink node ordering (if present) and must (as a combined set) be made in the same order:

▶ Node add APIs resulting in a sink node.

▶ Edge removal resulting in a node becoming a sink node.

▶ cudaStreamUpdateCaptureDependencies(), if it removes a sink node from a capturing stream’s dependency set.

▶ cudaStreamEndCapture().

The following example shows how the API could be used to update an instantiated graph:

```c
cudaGraphExec_t graphExec = NULL;

for (int i = 0; i < 10; i++) {
    cudaGraph_t graph;
    cudaGraphExecUpdateResult updateResult;
    cudaGraphNode_t errorNode;

    // In this example we use stream capture to create the graph.
    // You can also use the Graph API to produce a graph.
    cudaStreamBeginCapture(stream, cudaStreamCaptureModeGlobal);

    // Call a user-defined, stream based workload, for example
    do_cuda_work(stream);

    cudaStreamEndCapture(stream, &graph);

    // If we've already instantiated the graph, try to update it directly
    // and avoid the instantiation overhead
    if (graphExec != NULL) {
        // If the graph fails to update, errorNode will be set to the
        // node causing the failure and updateResult will be set to a
        // reason code.
        cudaGraphExecUpdate(graphExec, graph, &errorNode, &updateResult);
```

(continued from previous page)

```cpp
}

// Instantiate during the first iteration or whenever the update
// fails for any reason
if (graphExec == NULL || updateResult != cudaGraphExecUpdateSuccess) {

    // If a previous update failed, destroy the cudaGraphExec_t
    // before re-instantiating it
    if (graphExec != NULL) {
        cudaGraphExecDestroy(graphExec);
    }
    // Instantiate graphExec from graph. The error node and
    // error message parameters are unused here.
    cudaGraphInstantiate(&graphExec, graph, NULL, NULL, 0);
}

cudaGraphDestroy(graph);
cudaGraphLaunch(graphExec, stream);
cudaStreamSynchronize(stream);
}
```

A typical workflow is to create the initial cudaGraph\_t using either the stream capture or graph API. The cudaGraph\_t is then instantiated and launched as normal. After the initial launch, a new cudaGraph\_t is created using the same method as the initial graph and cudaGraphExecUpdate() is called. If the graph update is successful, indicated by the updateResult parameter in the above example, the updated cudaGraphExec\_t is launched. If the update fails for any reason, the cudaGraphExecDestroy() and cudaGraphInstantiate() are called to destroy the original cuda-GraphExec\_t and instantiate a new one.

It is also possible to update the cudaGraph\_t nodes directly (i.e., Using cudaGraphKernelNodeSet-Params()) and subsequently update the cudaGraphExec\_t, however it is more eficient to use the explicit node update APIs covered in the next section.

Conditional handle flags and default values are updated as part of the graph update.

Please see the Graph API for more information on usage and current limitations.
````
