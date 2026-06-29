# CUDA Graphs

CUDA Graphs present a new model for work submission in CUDA [CUDA_C_Programming_Guide:L2405-L2418]. A graph is a series of operations, such as kernel launches, connected by dependencies, which is defined separately from its execution [CUDA_C_Programming_Guide:L2405-L2418]. This allows a graph to be defined once and then launched repeatedly [CUDA_C_Programming_Guide:L2405-L2418]. Separating out the definition of a graph from its execution enables a number of optimizations: first, CPU launch costs are reduced compared to streams, because much of the setup is done in advance; second, presenting the whole workflow to CUDA enables optimizations which might not be possible with the piecewise work submission mechanism of streams [CUDA_C_Programming_Guide:L2405-L2418].

Work submission using graphs is separated into three distinct stages: definition, instantiation, and execution [CUDA_C_Programming_Guide:L2405-L2418].

*   **Definition**: During the definition phase, a program creates a description of the operations in the graph along with the dependencies between them [CUDA_C_Programming_Guide:L2405-L2418].
*   **Instantiation**: Instantiation takes a snapshot of the graph template, validates it, and performs much of the setup and initialization of work with the aim of minimizing what needs to be done at launch [CUDA_C_Programming_Guide:L2405-L2418]. The resulting instance is known as an executable graph [CUDA_C_Programming_Guide:L2405-L2418].
*   **Execution**: An executable graph may be launched into a stream, similar to any other CUDA work [CUDA_C_Programming_Guide:L2405-L2418]. It may be launched any number of times without repeating the instantiation [CUDA_C_Programming_Guide:L2405-L2418].

## Graph Structure

An operation forms a node in a graph [CUDA_C_Programming_Guide:L2419-L2448]. The dependencies between the operations are the edges [CUDA_C_Programming_Guide:L2419-L2448]. These dependencies constrain the execution sequence of the operations [CUDA_C_Programming_Guide:L2419-L2448]. An operation may be scheduled at any time once the nodes on which it depends are complete [CUDA_C_Programming_Guide:L2419-L2448]. Scheduling is left up to the CUDA system [CUDA_C_Programming_Guide:L2419-L2448].

### Node Types

A graph node can be one of the following [CUDA_C_Programming_Guide:L2419-L2448]:

*   kernel
*   CPU function call
*   memory copy
*   memset
*   empty node
*   waiting on an event
*   recording an event
*   signalling an external semaphore
*   waiting on an external semaphore
*   conditional node
*   child graph: To execute a separate nested graph [CUDA_C_Programming_Guide:L2449-L2467]

### Edge Data

CUDA 12.3 introduced edge data on CUDA Graphs [CUDA_C_Programming_Guide:L2449-L2467]. Edge data modifies a dependency specified by an edge and consists of three parts: an outgoing port, an incoming port, and a type [CUDA_C_Programming_Guide:L2449-L2467]. An outgoing port specifies when an associated edge is triggered [CUDA_C_Programming_Guide:L2449-L2467]. An incoming port specifies what portion of a node is dependent on an associated edge [CUDA_C_Programming_Guide:L2449-L2467]. A type modifies the relation between the endpoints [CUDA_C_Programming_Guide:L2449-L2467].

Port values are specific to node type and direction, and edge types may be restricted to specific node types [CUDA_C_Programming_Guide:L2449-L2467]. In all cases, zero-initialized edge data represents default behavior [CUDA_C_Programming_Guide:L2449-L2467]. Outgoing port 0 waits on an entire task, incoming port 0 blocks an entire task, and edge type 0 is associated with a full dependency with memory synchronizing behavior [CUDA_C_Programming_Guide:L2449-L2467].

Edge data is optionally specified in various graph APIs via a parallel array to the associated nodes [CUDA_C_Programming_Guide:L2449-L2467]. If it is omitted as an input parameter, zero-initialized data is used [CUDA_C_Programming_Guide:L2449-L2467]. If it is omitted as an output (query) parameter, the API accepts this if the edge data being ignored is all zero-initialized, and returns `cudaErrorLossyQuery` if the call would discard information [CUDA_C_Programming_Guide:L2449-L2467].

Edge data is also available in some stream capture APIs: `cudaStreamBeginCaptureToGraph()`, `cudaStreamGetCaptureInfo()`, and `cudaStreamUpdateCaptureDependencies()` [CUDA_C_Programming_Guide:L2449-L2467]. In these cases, there is not yet a downstream node [CUDA_C_Programming_Guide:L2449-L2467]. The data is associated with a dangling edge (half edge) which will either be connected to a future captured node or discarded at termination of stream capture [CUDA_C_Programming_Guide:L2449-L2467]. Note that some edge types do not wait on full completion of the upstream node [CUDA_C_Programming_Guide:L2449-L2467]. These edges are ignored when considering if a stream capture has been fully rejoined to the origin stream, and cannot be discarded at the end of capture [CUDA_C_Programming_Guide:L2449-L2467].

Currently, no node types define additional incoming ports, and only kernel nodes define additional outgoing ports [CUDA_C_Programming_Guide:L2449-L2467]. There is one non-default dependency type, `cudaGraphDependencyTypeProgrammatic`, which enables Programmatic Dependent Launch between two kernel nodes [CUDA_C_Programming_Guide:L2449-L2467].

## Creating a Graph Using Graph APIs

Graphs can be created via two mechanisms: explicit API and stream capture [CUDA_C_Programming_Guide:L2468-L2495]. The following is an example of creating and executing the below graph [CUDA_C_Programming_Guide:L2468-L2495].

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

## Creating a Graph Using Stream Capture

Stream capture provides a mechanism to create a graph from existing stream-based APIs [CUDA_C_Programming_Guide:L2496-L2518]. A section of code which launches work into streams, including existing code, can be bracketed with calls to `cudaStreamBeginCapture()` and `cudaStreamEndCapture()` [CUDA_C_Programming_Guide:L2496-L2518].

```c
cudaGraph_t graph;

cudaStreamBeginCapture(stream);

kernel_A<<< ..., stream >>>(...);
kernel_B<<< ..., stream >>>(...);
libraryCall(stream);
kernel_C<<< ..., stream >>>(...);

cudaStreamEndCapture(stream, &graph);
```

A call to `cudaStreamBeginCapture()` places a stream in capture mode [CUDA_C_Programming_Guide:L2496-L2518]. When a stream is being captured, work launched into the stream is not enqueued for execution [CUDA_C_Programming_Guide:L2496-L2518]. It is instead appended to an internal graph that is progressively being built up [CUDA_C_Programming_Guide:L2496-L2518]. This graph is then returned by calling `cudaStreamEndCapture()`, which also ends capture mode for the stream [CUDA_C_Programming_Guide:L2496-L2518]. A graph which is actively being constructed by stream capture is referred to as a capture graph [CUDA_C_Programming_Guide:L2496-L2518].

Stream capture can be used on any CUDA stream except `cudaStreamLegacy` (the “NULL stream”) [CUDA_C_Programming_Guide:L2496-L2518]. Note that it can be used on `cudaStreamPerThread` [CUDA_C_Programming_Guide:L2496-L2518]. If a program is using the legacy stream, it may be possible to redefine stream 0 to be the per-thread stream with no functional change [CUDA_C_Programming_Guide:L2496-L2518].

Whether a stream is being captured can be queried with `cudaStreamIsCapturing()` [CUDA_C_Programming_Guide:L2496-L2518].

Work can be captured to an existing graph using `cudaStreamBeginCaptureToGraph()` [CUDA_C_Programming_Guide:L2519-L2559]. Instead of capturing to an internal graph, work is captured to a graph provided by the user [CUDA_C_Programming_Guide:L2519-L2559].

### Cross-stream Dependencies and Events

Stream capture can handle cross-stream dependencies expressed with `cudaEventRecord()` and `cudaStreamWaitEvent()`, provided the event being waited upon was recorded into the same capture graph [CUDA_C_Programming_Guide:L2519-L2559].

When an event is recorded in a stream that is in capture mode, it results in a captured event [CUDA_C_Programming_Guide:L2519-L2559]. A captured event represents a set of nodes in a capture graph [CUDA_C_Programming_Guide:L2519-L2559].

When a captured event is waited on by a stream, it places the stream in capture mode if it is not already, and the next item in the stream will have additional dependencies on the nodes in the captured event [CUDA_C_Programming_Guide:L2519-L2559]. The two streams are then being captured to the same capture graph [CUDA_C_Programming_Guide:L2519-L2559].

When cross-stream dependencies are present in stream capture, `cudaStreamEndCapture()` must still be called in the same stream where `cudaStreamBeginCapture()` was called; this is the origin stream [CUDA_C_Programming_Guide:L2519-L2559]. Any other streams which are being captured to the same capture graph, due to event-based dependencies, must also be joined back to the origin stream [CUDA_C_Programming_Guide:L2519-L2559]. This is illustrated below [CUDA_C_Programming_Guide:L2519-L2559]. All streams being captured to the same capture graph are taken out of capture mode upon `cudaStreamEndCapture()` [CUDA_C_Programming_Guide:L2519-L2559]. Failure to rejoin to the origin stream will result in failure of the overall capture operation [CUDA_C_Programming_Guide:L2519-L2559].

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

Note: When a stream is taken out of capture mode, the next non-captured item in the stream (if any) will still have a dependency on the most recent prior non-captured item, despite intermediate items having been removed [CUDA_C_Programming_Guide:L2519-L2559].

### Prohibited and Unhandled Operations

It is invalid to synchronize or query the execution status of a stream which is being captured or a captured event, because they do not represent items scheduled for execution [CUDA_C_Programming_Guide:L2560-L2573]. It is also invalid to query the execution status of or synchronize a broader handle which encompasses an active stream capture, such as a device or context handle when any associated stream is in capture mode [CUDA_C_Programming_Guide:L2560-L2573].

When any stream in the same context is being captured, and it was not created with `cudaStreamNonBlocking`, any attempted use of the legacy stream is invalid [CUDA_C_Programming_Guide:L2560-L2573]. This is because the legacy stream handle at all times encompasses these other streams; enqueueing to the legacy stream would create a dependency on the streams being captured, and querying it or synchronizing it would query or synchronize the streams being captured [CUDA_C_Programming_Guide:L2560-L2573].

It is therefore also invalid to call synchronous APIs in this case [CUDA_C_Programming_Guide:L2560-L2573]. Synchronous APIs, such as `cudaMemcpy()`, enqueue work to the legacy stream and synchronize it before returning [CUDA_C_Programming_Guide:L2560-L2573].

Note: As a general rule, when a dependency relation would connect something that is captured with something that was not captured and instead enqueued for execution, CUDA prefers to return an error rather than ignore the dependency [CUDA_C_Programming_Guide:L2560-L2573]. An exception is made for placing a stream into or out of capture mode; this severs a dependency relation between items added to the stream immediately before and after the mode transition [CUDA_C_Programming_Guide:L2560-L2573].

It is invalid to merge two separate capture graphs by waiting on a captured event from a stream which is being captured and is associated with a different capture graph than the event [CUDA_C_Programming_Guide:L2560-L2573]. It is invalid to wait on a non-captured event from a stream which is being captured without specifying the `cudaEventWaitExternal` flag [CUDA_C_Programming_Guide:L2560-L2573].

A small number of APIs that enqueue asynchronous operations into streams are not currently supported in graphs and will return an error if called with a stream which is being captured, such as `cudaStreamAttachMemAsync()` [CUDA_C_Programming_Guide:L2560-L2573].

### Invalidation

When an invalid operation is attempted during stream capture, any associated capture graphs are invalidated [CUDA_C_Programming_Guide:L2574-L2576]. When a capture graph is invalidated, further use of any streams which are being captured or captured events associated with the graph is invalid and will return an error, until stream capture is ended with `cudaStreamEndCapture()` [CUDA_C_Programming_Guide:L2574-L2576]. This call will take the associated streams out of capture mode, but will also return an error value and a NULL graph [CUDA_C_Programming_Guide:L2574-L2576].
