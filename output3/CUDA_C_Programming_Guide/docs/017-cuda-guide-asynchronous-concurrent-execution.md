## 6.2.8. Asynchronous Concurrent Execution

CUDA exposes the following operations as independent tasks that can operate concurrently with one another:

▶ Computation on the host;

▶ Computation on the device;

▶ Memory transfers from the host to the device;

▶ Memory transfers from the device to the host;

▶ Memory transfers within the memory of a given device;

▶ Memory transfers among devices.

The level of concurrency achieved between these operations will depend on the feature set and compute capability of the device as described below.

## 6.2.8.1 Concurrent Execution between Host and Device

Concurrent host execution is facilitated through asynchronous library functions that return control to the host thread before the device completes the requested task. Using asynchronous calls, many device operations can be queued up together to be executed by the CUDA driver when appropriate device resources are available. This relieves the host thread of much of the responsibility to manage the device, leaving it free for other tasks. The following device operations are asynchronous with respect to the host:

▶ Kernel launches;

▶ Memory copies within a single device’s memory;

Memory copies from host to device of a memory block of 64 KB or less;

Memory copies performed by functions that are sufixed with Async;

▶ Memory set function calls.

Programmers can globally disable asynchronicity of kernel launches for all CUDA applications running on a system by setting the CUDA\_LAUNCH\_BLOCKING environment variable to 1. This feature is provided for debugging purposes only and should not be used as a way to make production software run reliably.

Kernel launches are synchronous if hardware counters are collected via a profiler (Nsight Compute) unless concurrent kernel profiling is enabled. Async memory copies might also be synchronous if they involve host memory that is not page-locked

## 6.2.8.2 Concurrent Kernel Execution

Some devices of compute capability 2.x and higher can execute multiple kernels concurrently. Applications may query this capability by checking the concurrentKernels device property (see Device Enumeration), which is equal to 1 for devices that support it.

The maximum number of kernel launches that a device can execute concurrently depends on its compute capability and is listed in Table 27.

A kernel from one CUDA context cannot execute concurrently with a kernel from another CUDA context. The GPU may time slice to provide forward progress to each context. If a user wants to run kernels from multiple process simultaneously on the SM, one must enable MPS.

Kernels that use many textures or a large amount of local memory are less likely to execute concurrently with other kernels.

## 6.2.8.3 Overlap of Data Transfer and Kernel Execution

Some devices can perform an asynchronous memory copy to or from the GPU concurrently with kernel execution. Applications may query this capability by checking the asyncEngineCount device property (see Device Enumeration), which is greater than zero for devices that support it. If host memory is involved in the copy, it must be page-locked.

It is also possible to perform an intra-device copy simultaneously with kernel execution (on devices that support the concurrentKernels device property) and/or with copies to or from the device (for devices that support the asyncEngineCount property). Intra-device copies are initiated using the standard memory copy functions with destination and source addresses residing on the same device.

## 6.2.8.4 Concurrent Data Transfers

Some devices of compute capability 2.x and higher can overlap copies to and from the device. Applications may query this capability by checking the asyncEngineCount device property (see Device Enumeration), which is equal to 2 for devices that support it. In order to be overlapped, any host memory involved in the transfers must be page-locked.

## 6.2.8.5 Streams

Applications manage the concurrent operations described above through streams. A stream is a sequence of commands (possibly issued by diferent host threads) that execute in order. Diferent streams, on the other hand, may execute their commands out of order with respect to one another or concurrently; this behavior is not guaranteed and should therefore not be relied upon for correctness (for example, inter-kernel communication is undefined). The commands issued on a stream may execute when all the dependencies of the command are met. The dependencies could be previously launched commands on same stream or dependencies from other streams. The successful completion of synchronize call guarantees that all the commands launched are completed.

## 6.2.8.5.1 Creation and Destruction of Streams

A stream is defined by creating a stream object and specifying it as the stream parameter to a sequence of kernel launches and host <-> device memory copies. The following code sample creates two streams and allocates an array hostPtr of float in page-locked memory.

```matlab
cudaStream_t stream[2];
for (int i = 0; i < 2; ++i)
    cudaStreamCreate(&stream[i]);
float* hostPtr;
cudaMallocHost(&hostPtr, 2 * size);
```

Each of these streams is defined by the following code sample as a sequence of one memory copy from host to device, one kernel launch, and one memory copy from device to host:

```cpp
for (int i = 0; i < 2; ++i) {
    cudaMemcpyAsync(inputDevPtr + i * size, hostPtr + i * size,
                    size, cudaMemcpyHostToDevice, stream[i]);
    MyKernel <<100, 512, 0, stream[i]>>
        (outputDevPtr + i * size, inputDevPtr + i * size, size);
    cudaMemcpyAsync(hostPtr + i * size, outputDevPtr + i * size,
```

(continues on next page)

(continued from previous page)

```javascript
size, cudaMemcpyDeviceToHost, stream[i]);
```

Each stream copies its portion of input array hostPtr to array inputDevPtr in device memory, processes inputDevPtr on the device by calling MyKernel(), and copies the result outputDevPtr back to the same portion of hostPtr. Overlapping Behavior describes how the streams overlap in this example depending on the capability of the device. Note that hostPtr must point to page-locked host memory for any overlap to occur.

Streams are released by calling cudaStreamDestroy().

```javascript
for (int i = 0; i < 2; ++i)
    cudaStreamDestroy(stream[i]);
```

In case the device is still doing work in the stream when cudaStreamDestroy() is called, the function will return immediately and the resources associated with the stream will be released automatically once the device has completed all work in the stream.

## 6.2.8.5.2 Default Stream

Kernel launches and host <-> device memory copies that do not specify any stream parameter, or equivalently that set the stream parameter to zero, are issued to the default stream. They are therefore executed in order.

For code that is compiled using the --default-stream per-thread compilation flag (or that defines the CUDA\_API\_PER\_THREAD\_DEFAULT\_STREAM macro before including CUDA headers (cuda.h and cuda\_runtime.h)), the default stream is a regular stream and each host thread has its own default stream.

Note: #define CUDA\_API\_PER\_THREAD\_DEFAULT\_STREAM 1 cannot be used to enable this behavior when the code is compiled by nvcc as nvcc implicitly includes cuda\_runtime.h at the top of the translation unit. In this case the --default-stream per-thread compilation flag needs to be used or the CUDA\_API\_PER\_THREAD\_DEFAULT\_STREAM macro needs to be defined with the -DCUDA\_API\_PER\_THREAD\_DEFAULT\_STREAM=1 compiler flag.

For code that is compiled using the --default-stream legacy compilation flag, the default stream is a special stream called the NULL stream and each device has a single NULL stream used for all host threads. The NULL stream is special as it causes implicit synchronization as described in Implicit Synchronization.

For code that is compiled without specifying a --default-stream compilation flag, --default-stream legacy is assumed as the default.

## 6.2.8.5.3 Explicit Synchronization

There are various ways to explicitly synchronize streams with each other.

cudaDeviceSynchronize() waits until all preceding commands in all streams of all host threads have completed.

cudaStreamSynchronize()takes a stream as a parameter and waits until all preceding commands in the given stream have completed. It can be used to synchronize the host with a specific stream, allowing other streams to continue executing on the device.

cudaStreamWaitEvent()takes a stream and an event as parameters (see Events for a description of events)and makes all the commands added to the given stream after the call to cudaStreamWait-Event()delay their execution until the given event has completed.

cudaStreamQuery()provides applications with a way to know if all preceding commands in a stream have completed.

## 6.2.8.5.4 Implicit Synchronization

Two operations from diferent streams cannot run concurrently if any CUDA operation on the NULL stream is submitted in-between them, unless the streams are non-blocking streams (created with the cudaStreamNonBlocking flag).

Applications should follow these guidelines to improve their potential for concurrent kernel execution:

▶ All independent operations should be issued before dependent operations,

▶ Synchronization of any kind should be delayed as long as possible.

## 6.2.8.5.5 Overlapping Behavior

The amount of execution overlap between two streams depends on the order in which the commands are issued to each stream and whether or not the device supports overlap of data transfer and kernel execution (see Overlap of Data Transfer and Kernel Execution), concurrent kernel execution (see Concurrent Kernel Execution), and/or concurrent data transfers (see Concurrent Data Transfers).

For example, on devices that do not support concurrent data transfers, the two streams of the code sample of Creation and Destruction of Streams do not overlap at all because the memory copy from host to device is issued to stream[1] after the memory copy from device to host is issued to stream[0], so it can only start once the memory copy from device to host issued to stream[0] has completed. If the code is rewritten the following way (and assuming the device supports overlap of data transfer and kernel execution)

```txt
for (int i = 0; i < 2; ++i)
    cudaMemcpyAsync(inputDevPtr + i * size, hostPtr + i * size,
                   size, cudaMemcpyHostToDevice, stream[i]);
for (int i = 0; i < 2; ++i)
    MyKernel<<<100, 512, 0, stream[i]>>>
        (outputDevPtr + i * size, inputDevPtr + i * size, size);
for (int i = 0; i < 2; ++i)
    cudaMemcpyAsync(hostPtr + i * size, outputDevPtr + i * size,
                   size, cudaMemcpyDeviceToHost, stream[i]);
```

then the memory copy from host to device issued to stream[1] overlaps with the kernel launch issued to stream[0].

On devices that do support concurrent data transfers, the two streams of the code sample of Creation and Destruction of Streams do overlap: The memory copy from host to device issued to stream[1] overlaps with the memory copy from device to host issued to stream[0] and even with the kernel launch issued to stream[0] (assuming the device supports overlap of data transfer and kernel execution).

## 6.2.8.5.6 Host Functions (Callbacks)

The runtime provides a way to insert a CPU function call at any point into a stream via cudaLaunch-HostFunc(). The provided function is executed on the host once all commands issued to the stream before the callback have completed.

The following code sample adds the host function MyCallback to each of two streams after issuing a host-to-device memory copy, a kernel launch and a device-to-host memory copy into each stream. The function will begin execution on the host after each of the device-to-host memory copies completes.

```c
void CUDART_CB MyCallback(void *data){
    printf("Inside callback %d\n", (size_t)data);
}
...
for (size_t i = 0; i < 2; ++i) {
    cudaMemcpyAsync(devPtrIn[i], hostPtr[i], size, cudaMemcpyHostToDevice, stream[i]);
    MyKernel<<<100, 512, 0, stream[i]>>>(devPtrOut[i], devPtrIn[i], size);
    cudaMemcpyAsync(hostPtr[i], devPtrOut[i], size, cudaMemcpyDeviceToHost,
stream[i]);
    cudaLaunchHostFunc(stream[i], MyCallback, (void*)i);
}
```

The commands that are issued in a stream after a host function do not start executing before the function has completed.

A host function enqueued into a stream must not make CUDA API calls (directly or indirectly), as it might end up waiting on itself if it makes such a call leading to a deadlock.

## 6.2.8.5.7 Stream Priorities

The relative priorities of streams can be specified at creation using cudaStreamCreateWithPriority(). The range of allowable priorities, ordered as [ greatest priority, least priority ] can be obtained using the cudaDeviceGetStreamPriorityRange() function. At runtime, the GPU scheduler utilizes stream priorities to determine task execution order, but these priorities serve as hints rather than guarantees. When selecting work to launch, pending tasks in higher-priority streams take precedence over those in lower-priority streams. Higher-priority tasks do not preempt already running lower-priority tasks. The GPU does not reassess work queues during task execution, and increasing a stream’s priority will not interrupt ongoing work. Stream priorities influence task execution without enforcing strict ordering, so users can leverage stream priorities to influence task execution without relying on strict ordering guarantees.

The following code sample obtains the allowable range of priorities for the current device, and creates streams with the highest and lowest available priorities.

```cpp
// get the range of stream priorities for this device
int leastPriority, greatestPriority;
cudaDeviceGetStreamPriorityRange(&leastPriority, &greatestPriority);
// create streams with highest and lowest available priorities
cudaStream_t st_high, st_low;
```

(continues on next page)

```txt
(continued from previous page)
cudaStreamCreateWithPriority(&st_high, cudaStreamNonBlocking, greatestPriority));
cudaStreamCreateWithPriority(&st_low, cudaStreamNonBlocking, leastPriority);
```

## 6.2.8.6 Programmatic Dependent Launch and Synchronization

Warning: This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA.

The Programmatic Dependent Launch mechanism allows for a dependent secondary kernel to launch before the primary kernel it depends on in the same CUDA stream has finished executing. Available starting with devices of compute capability 9.0, this technique can provide performance benefits when the secondary kernel can complete significant work that does not depend on the results of the primary kernel.

## 6.2.8.6.1 Background

A CUDA application utilizes the GPU by launching and executing multiple kernels on it. A typical GPU activity timeline is shown in Figure 10.

<table><tr><td></td><td>primary kernel</td><td></td><td>secondary kernel</td><td></td><td>other kernel</td><td></td></tr></table>

Figure 10: GPU activity timeline

Here, secondary\_kernel is launched after primary\_kernel finishes its execution. Serialized execution is usually necessary because secondary\_kernel depends on result data produced by primary\_kernel. If secondary\_kernel has no dependency on primary\_kernel, both of them can be launched concurrently by using Streams. Even if secondary\_kernel is dependent on primary\_kernel, there is some potential for concurrent execution. For example, almost all the kernels have some sort of preamble section during which tasks such as zeroing bufers or loading constant values are performed.

![](images/e55c03e658ca23f9eb81649865dbb141c85e0a121d64bdc31535edf2d9c691dc.jpg)  
Figure 11: Preamble section of secondary\_kernel

Figure 11 demonstrates the portion of secondary\_kernel that could be executed concurrently without impacting the application. Note that concurrent launch also allows us to hide the launch latency of secondary\_kernel behind the execution of primary\_kernel.

![](images/923eb9e33dd2e096270aff7a470d9e2a69cbb88182ad523a233e1a74097d20af.jpg)  
Figure 12: Concurrent execution of primary\_kernel and secondary\_kernel

The concurrent launch and execution of secondary\_kernel shown in Figure 12 is achievable using Programmatic Dependent Launch.

Programmatic Dependent Launch introduces changes to the CUDA kernel launch APIs as explained in following section. These APIs require at least compute capability 9.0 to provide overlapping execution.

## 6.2.8.6.2 API Description

In Programmatic Dependent Launch, a primary and a secondary kernel are launched in the same CUDA stream. The primary kernel should execute cudaTriggerProgrammaticLaunchCompletion with all thread blocks when it’s ready for the secondary kernel to launch. The secondary kernel must be launched using the extensible launch API as shown.

```javascript
__global__ void primary_kernel() {
    // Initial work that should finish before starting secondary kernel

    // Trigger the secondary kernel
    cudaTriggerProgrammaticLaunchCompletion();

    // Work that can coincide with the secondary kernel
}

__global__ void secondary_kernel()
{
    // Independent work

    // Will block until all primary kernels the secondary kernel is dependent on have
    completed and flushed results to global memory
    cudaGridDependencySynchronize();

    // Dependent work
}

cudaLaunchAttribute attribute[1];
attribute[0].id = cudaLaunchAttributeProgrammaticStreamSerialization;
attribute[0].val.programmaticStreamSerializationAllowed = 1;
configSecondary.attrs = attribute;
```

(continued from previous page)

```txt
configSecondary.numAttrs = 1;

primary_kernel<<<grid_dim, block_dim, 0, stream>>>();
cudaLaunchKernelEx(&configSecondary, secondary_kernel);
```

When the secondary kernel is launched using the cudaLaunchAttributeProgrammaticStreamSerialization attribute, the CUDA driver is safe to launch the secondary kernel early and not wait on the completion and memory flush of the primary before launching the secondary.

The CUDA driver can launch the secondary kernel when all primary thread blocks have launched and executed cudaTriggerProgrammaticLaunchCompletion. If the primary kernel doesn’t execute the trigger, it implicitly occurs after all thread blocks in the primary kernel exit.

In either case, the secondary thread blocks might launch before data written by the primary kernel is visible. As such, when the secondary kernel is configured with Programmatic Dependent Launch, it must always use cudaGridDependencySynchronize or other means to verify that the result data from the primary is available.

Please note that these methods provide the opportunity for the primary and secondary kernels to execute concurrently, however this behavior is opportunistic and not guaranteed to lead to concurrent kernel execution. Reliance on concurrent execution in this manner is unsafe and can lead to deadlock.

## 6.2.8.6.3 Use in CUDA Graphs

Programmatic Dependent Launch can be used in CUDA Graphs via stream capture or directly via edge data. To program this feature in a CUDA Graph with edge data, use a cudaGraphDependencyType value of cudaGraphDependencyTypeProgrammatic on an edge connecting two kernel nodes. This edge type makes the upstream kernel visible to a cudaGridDependencySynchronize() in the downstream kernel. This type must be used with an outgoing port of either cudaGraphKernelNodePort-LaunchCompletion or cudaGraphKernelNodePortProgrammatic.

The resulting graph equivalents for stream capture are as follows:

<table><tr><td>Stream code (abbreviated)</td><td>Resulting graph edge</td></tr><tr><td>cudaLaunchAttribute attribute;attribute.id =→cudaLaunchAttributeProgrammaticStreamSeril→attribute.val.→programmaticStreamSerializationAllowed→= 1;</td><td>cudaGraphEdgeData edgeData;edgeData.type =→cudaGraphDependencyTypeProgrammatic;edgeData.from_port =→cudaGraphKernelNodePortProgrammatic;</td></tr><tr><td>cudaLaunchAttribute attribute;attribute.id =→cudaLaunchAttributeProgrammaticEvent;attribute.val.programmaticEvent.→triggerAtBlockStart = 0;</td><td>cudaGraphEdgeData edgeData;edgeData.type =→cudaGraphDependencyTypeProgrammatic;edgeData.from_port =→cudaGraphKernelNodePortProgrammatic;</td></tr><tr><td>cudaLaunchAttribute attribute;attribute.id =→cudaLaunchAttributeProgrammaticEvent;attribute.val.programmaticEvent.→triggerAtBlockStart = 1;</td><td>cudaGraphEdgeData edgeData;edgeData.type =→cudaGraphDependencyTypeProgrammatic;edgeData.from_port =→cudaGraphKernelNodePortLaunchCompletion;</td></tr></table>

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
