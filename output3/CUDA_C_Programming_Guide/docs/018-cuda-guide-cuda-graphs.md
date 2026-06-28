
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

## 6.2.8.7.5.3 Individual Node Update

Instantiated graph node parameters can be updated directly. This eliminates the overhead of instantiation as well as the overhead of creating a new cudaGraph\_t. If the number of nodes requiring update is small relative to the total number of nodes in the graph, it is better to update the nodes individually. The following methods are available for updating cudaGraphExec\_t nodes:

▶ cudaGraphExecKernelNodeSetParams()

▶ cudaGraphExecMemcpyNodeSetParams()

cudaGraphExecMemsetNodeSetParams()

▶ cudaGraphExecHostNodeSetParams()

▶ cudaGraphExecChildGraphNodeSetParams()

cudaGraphExecEventRecordNodeSetEvent()

▶ cudaGraphExecEventWaitNodeSetEvent()

cudaGraphExecExternalSemaphoresSignalNodeSetParams()

▶ cudaGraphExecExternalSemaphoresWaitNodeSetParams()

Please see the Graph API for more information on usage and current limitations.

## 6.2.8.7.5.4 Individual Node Enable

Kernel, memset and memcpy nodes in an instantiated graph can be enabled or disabled using the cudaGraphNodeSetEnabled() API. This allows the creation of a graph which contains a superset of the desired functionality which can be customized for each launch. The enable state of a node can be queried using the cudaGraphNodeGetEnabled() API.

A disabled node is functionally equivalent to empty node until it is reenabled. Node parameters are not afected by enabling/disabling a node. Enable state is unafected by individual node update or whole graph update with cudaGraphExecUpdate(). Parameter updates while the node is disabled will take efect when the node is reenabled.

The following methods are available for enabling/disabling cudaGraphExec\_t nodes, as well as querying their status:

▶ cudaGraphNodeSetEnabled()

▶ cudaGraphNodeGetEnabled()

Refer to the Graph API for more information on usage and current limitations.

## 6.2.8.7.6 Using Graph APIs

cudaGraph\_t objects are not thread-safe. It is the responsibility of the user to ensure that multiple threads do not concurrently access the same cudaGraph\_t.

A cudaGraphExec\_t cannot run concurrently with itself. A launch of a cudaGraphExec\_t will be ordered after previous launches of the same executable graph.

Graph execution is done in streams for ordering with other asynchronous work. However, the stream is for ordering only; it does not constrain the internal parallelism of the graph, nor does it afect where graph nodes execute.

See Graph API.

## 6.2.8.7.7 Device Graph Launch

There are many workflows which need to make data-dependent decisions during runtime and execute diferent operations depending on those decisions. Rather than ofloading this decision-making process to the host, which may require a round-trip from the device, users may prefer to perform it on the device. To that end, CUDA provides a mechanism to launch graphs from the device.

Device graph launch provides a convenient way to perform dynamic control flow from the device, be it something as simple as a loop or as complex as a device-side work scheduler. This functionality is only available on systems which support unified addressing.

Graphs which can be launched from the device will henceforth be referred to as device graphs, and graphs which cannot be launched from the device will be referred to as host graphs.

Device graphs can be launched from both the host and device, whereas host graphs can only be launched from the host. Unlike host launches, launching a device graph from the device while a previous launch of the graph is running will result in an error, returning cudaErrorInvalidValue; therefore, a device graph cannot be launched twice from the device at the same time. Launching a device graph from the host and device simultaneously will result in undefined behavior.

## 6.2.8.7.7.1 Device Graph Creation

In order for a graph to be launched from the device, it must be instantiated explicitly for device launch. This is achieved by passing the cudaGraphInstantiateFlagDeviceLaunch flag to the cudaGraphInstantiate() call. As is the case for host graphs, device graph structure is fixed at time of instantiation and cannot be updated without re-instantiation, and instantiation can only be performed on the host. In order for a graph to be able to be instantiated for device launch, it must adhere to various requirements.

## 6.2.8.7.7.2 Device Graph Requirements

## General requirements:

▶ The graph’s nodes must all reside on a single device.

▶ The graph can only contain kernel nodes, memcpy nodes, memset nodes, and child graph nodes. Kernel nodes:

Use of CUDA Dynamic Parallelism by kernels in the graph is not permitted.

▶ Cooperative launches are permitted so long as MPS is not in use.

## Memcpy nodes:

▶ Only copies involving device memory and/or pinned device-mapped host memory are permitted.

▶ Copies involving CUDA arrays are not permitted.

▶ Both operands must be accessible from the current device at time of instantiation. Note that the copy operation will be performed from the device on which the graph resides, even if it is targeting memory on another device.

## 6.2.8.7.7.3 Device Graph Upload

In order to launch a graph on the device, it must first be uploaded to the device to populate the necessary device resources. This can be achieved in one of two ways.

Firstly, the graph can be uploaded explicitly, either via cudaGraphUpload() or by requesting an upload as part of instantiation via cudaGraphInstantiateWithParams().

Alternatively, the graph can first be launched from the host, which will perform this upload step implicitly as part of the launch.

Examples of all three methods can be seen below:

```txt
// Explicit upload after instantiation
cudaGraphInstantiate(&deviceGraphExec1, deviceGraph1,
→cudaGraphInstantiateFlagDeviceLaunch);
cudaGraphUpload(deviceGraphExec1, stream);

// Explicit upload as part of instantiation
cudaGraphInstantiateParams instantiateParams = {0};
```

(continues on next page)

```txt
(continued from previous page)
instantiateParams.flags = cudaGraphInstantiateFlagDeviceLaunch |
cudaGraphInstantiateFlagUpload;
instantiateParams.uploadStream = stream;
cudaGraphInstantiateWithParams(&deviceGraphExec2, deviceGraph2, &instantiateParams);

// Implicit upload via host launch
cudaGraphInstantiate(&deviceGraphExec3, deviceGraph3,
cudaGraphInstantiateFlagDeviceLaunch);
cudaGraphLaunch(deviceGraphExec3, stream);
```

## 6.2.8.7.7.4 Device Graph Update

Device graphs can only be updated from the host, and must be re-uploaded to the device upon executable graph update in order for the changes to take efect. This can be achieved using the same methods outlined in the previous section. Unlike host graphs, launching a device graph from the device while an update is being applied will result in undefined behavior.

## 6.2.8.7.7.5 Device Launch

Device graphs can be launched from both the host and the device via cudaGraphLaunch(), which has the same signature on the device as on the host. Device graphs are launched via the same handle on the host and the device. Device graphs must be launched from another graph when launched from the device.

Device-side graph launch is per-thread and multiple launches may occur from diferent threads at the same time, so the user will need to select a single thread from which to launch a given graph.

## 6.2.8.7.7.6 Device Launch Modes

Unlike host launch, device graphs cannot be launched into regular CUDA streams, and can only be launched into distinct named streams, which each denote a specific launch mode:

Table 5: Device-only Graph Launch Streams

<table><tr><td>Stream</td><td>Launch Mode</td></tr><tr><td>cudaStreamGraphFireAndForget</td><td>Fire and forget launch</td></tr><tr><td>cudaStreamGraphTailLaunch</td><td>Tail launch</td></tr><tr><td>cudaStreamGraphFireAndForgetAsSibling</td><td>Sibling launch</td></tr></table>

## 6.2.8.7.7.7 Fire and Forget Launch

As the name suggests, a fire and forget launch is submitted to the GPU immediately, and it runs independently of the launching graph. In a fire-and-forget scenario, the launching graph is the parent, and the launched graph is the child.

![](images/eef04bf20fed5754e9bd9f66389ab796dff3bafcd30024712ba2f4870535c513.jpg)  
Figure 15: Fire and forget launch

The above diagram can be generated by the sample code below:

```cpp
__global__ void launchFireAndForgetGraph(cudaGraphExec_t graph) {
    cudaGraphLaunch(graph, cudaStreamGraphFireAndForget);
}

void graphSetup() {
    cudaGraphExec_t gExec1, gExec2;
    cudaGraph_t g1, g2;

    // Create, instantiate, and upload the device graph.
    create_graph(&g2);
    cudaGraphInstantiate(&gExec2, g2, cudaGraphInstantiateFlagDeviceLaunch);
    cudaGraphUpload(gExec2, stream);

    // Create and instantiate the launching graph.
    cudaStreamBeginCapture(stream, cudaStreamCaptureModeGlobal);
    launchFireAndForgetGraph<<<1, 1, 0, stream>>>(gExec2);
    cudaStreamEndCapture(stream, &g1);
    cudaGraphInstantiate(&gExec1, g1);

    // Launch the host graph, which will in turn launch the device graph.
    cudaGraphLaunch(gExec1, stream);
}
```

A graph can have up to 120 total fire-and-forget graphs during the course of its execution. This total resets between launches of the same parent graph.

## 6.2.8.7.7.8 Graph Execution Environments

In order to fully understand the device-side synchronization model, it is first necessary to understand the concept of an execution environment.

When a graph is launched from the device, it is launched into its own execution environment. The execution environment of a given graph encapsulates all work in the graph as well as all generated fire and forget work. The graph can be considered complete when it has completed execution and when all generated child work is complete.

The below diagram shows the environment encapsulation that would be generated by the fire-andforget sample code in the previous section.

![](images/eba2c691665b7cdb32be77615780eee36533c683b671247e7ec79a84185dfea3.jpg)  
Figure 16: Fire and forget launch, with execution environments

These environments are also hierarchical, so a graph environment can include multiple levels of childenvironments from fire and forget launches.

When a graph is launched from the host, there exists a stream environment that parents the execution environment of the launched graph. The stream environment encapsulates all work generated as part of the overall launch. The stream launch is complete (i.e. downstream dependent work may now run) when the overall stream environment is marked as complete.

![](images/3cf88ddfc3426b9c3c0b5f53c4fc2217b1beef5cecc17608a506157e0040fb36.jpg)

Figure 17: Nested fire and forget environments  
![](images/86b4ae5191b444b3fda6717749ac566c83fe939796ea4fd61507985f5d08a9da.jpg)  
Figure 18: The stream environment, visualized

## 6.2.8.7.7.9 Tail Launch

Unlike on the host, it is not possible to synchronize with device graphs from the GPU via traditional methods such as cudaDeviceSynchronize() or cudaStreamSynchronize(). Rather, in order to enable serial work dependencies, a diferent launch mode - tail launch - is ofered, to provide similar functionality.

A tail launch executes when a graph’s environment is considered complete - ie, when the graph and all its children are complete. When a graph completes, the environment of the next graph in the tail launch list will replace the completed environment as a child of the parent environment. Like fire-andforget launches, a graph can have multiple graphs enqueued for tail launch.

![](images/9bfe56ce7d9a640d34905fb9ed38c552e19e0a914005e5295fea7c6103c5a319.jpg)  
Figure 19: A simple tail launch

The above execution flow can be generated by the code below:

```cpp
__global__ void launchTailGraph(cudaGraphExec_t graph) {
    cudaGraphLaunch(graph, cudaStreamGraphTailLaunch);
}

void graphSetup() {
    cudaGraphExec_t gExec1, gExec2;
    cudaGraph_t g1, g2;

    // Create, instantiate, and upload the device graph.
    create_graph(&g2);
    cudaGraphInstantiate(&gExec2, g2, cudaGraphInstantiateFlagDeviceLaunch);
    cudaGraphUpload(gExec2, stream);

    // Create and instantiate the launching graph.
    cudaStreamBeginCapture(stream, cudaStreamCaptureModeGlobal);
    launchTailGraph<<<1, 1, 0, stream>>>(gExec2);
    cudaStreamEndCapture(stream, &g1);
    cudaGraphInstantiate(&gExec1, g1);

    // Launch the host graph, which will in turn launch the device graph.
    cudaGraphLaunch(gExec1, stream);
}
```
