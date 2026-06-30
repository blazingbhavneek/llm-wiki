# Programmatic Dependent Launch

A mechanism (compute capability 9.0+) allowing a secondary kernel to launch before its primary kernel finishes in the same stream. Uses cudaTriggerProgrammaticLaunchCompletion() and cudaGridDependencySynchronize() for safe concurrent execution. Supported in CUDA Graphs via edge data.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L2321-L2404

Citation: [CUDA_C_Programming_Guide:L2321-L2404]

````text
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
````
