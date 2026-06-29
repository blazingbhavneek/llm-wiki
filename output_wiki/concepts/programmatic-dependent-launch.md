# Programmatic Dependent Launch

Programmatic Dependent Launch (PDL) is a CUDA feature available starting with devices of compute capability 9.0 that allows a dependent secondary kernel to launch before the primary kernel it depends on in the same CUDA stream has finished executing [CUDA_C_Programming_Guide:L2320-L2348]. This technique provides performance benefits when the secondary kernel can complete significant work that does not depend on the results of the primary kernel [CUDA_C_Programming_Guide:L2320-L2348].

## Background

In typical GPU execution, a secondary kernel launched after a primary kernel waits for the primary to finish due to data dependencies [CUDA_C_Programming_Guide:L2320-L2348]. However, kernels often have preamble sections, such as zeroing buffers or loading constant values, that do not depend on the primary kernel's results [CUDA_C_Programming_Guide:L2320-L2348]. PDL enables the concurrent launch and execution of the secondary kernel's preamble, hiding launch latency and overlapping execution with the primary kernel [CUDA_C_Programming_Guide:L2320-L2348].

## API Description

PDL operates within a single CUDA stream using specific APIs and attributes [CUDA_C_Programming_Guide:L2349-L2396].

### Primary Kernel

The primary kernel must explicitly signal readiness for the secondary kernel to launch by calling `cudaTriggerProgrammaticLaunchCompletion()` [CUDA_C_Programming_Guide:L2349-L2396]. This should be done after initial work that the secondary kernel depends on has completed [CUDA_C_Programming_Guide:L2349-L2396]. Work following this trigger can execute concurrently with the secondary kernel [CUDA_C_Programming_Guide:L2349-L2396].

```cpp
__global__ void primary_kernel() {
    // Initial work that should finish before starting secondary kernel

    // Trigger the secondary kernel
    cudaTriggerProgrammaticLaunchCompletion();

    // Work that can coincide with the secondary kernel
}
```

If the primary kernel does not explicitly execute the trigger, it implicitly occurs after all thread blocks in the primary kernel exit [CUDA_C_Programming_Guide:L2349-L2396].

### Secondary Kernel

The secondary kernel must be launched using the extensible launch API (`cudaLaunchKernelEx`) with the `cudaLaunchAttributeProgrammaticStreamSerialization` attribute set to 1 [CUDA_C_Programming_Guide:L2349-L2396]. This attribute informs the CUDA driver that it is safe to launch the secondary kernel early without waiting for the primary kernel's completion and memory flush [CUDA_C_Programming_Guide:L2349-L2396].

Inside the secondary kernel, `cudaGridDependencySynchronize()` must be called to block execution until all primary kernels the secondary kernel depends on have completed and flushed results to global memory [CUDA_C_Programming_Guide:L2349-L2396]. This ensures that result data from the primary kernel is available before dependent work begins [CUDA_C_Programming_Guide:L2349-L2396].

```cpp
__global__ void secondary_kernel()
{
    // Independent work

    // Will block until all primary kernels the secondary kernel is dependent on have
    // completed and flushed results to global memory
    cudaGridDependencySynchronize();

    // Dependent work
}
```

### Launch Configuration

The secondary kernel is launched using `cudaLaunchKernelEx` with the appropriate attributes [CUDA_C_Programming_Guide:L2349-L2396].

```cpp
cudaLaunchAttribute attribute[1];
attribute[0].id = cudaLaunchAttributeProgrammaticStreamSerialization;
attribute[0].val.programmaticStreamSerializationAllowed = 1;
configSecondary.attrs = attribute;
configSecondary.numAttrs = 1;

primary_kernel<<<grid_dim, block_dim, 0, stream>>>();
cudaLaunchKernelEx(&configSecondary, secondary_kernel);
```

## Caveats

While PDL provides the opportunity for primary and secondary kernels to execute concurrently, this behavior is opportunistic and not guaranteed [CUDA_C_Programming_Guide:L2349-L2396]. Reliance on concurrent execution in this manner is unsafe and can lead to deadlock if dependencies are not correctly managed [CUDA_C_Programming_Guide:L2349-L2396].

## Use in CUDA Graphs

Programmatic Dependent Launch can be used in CUDA Graphs via stream capture or directly via edge data [CUDA_C_Programming_Guide:L2397-L2404]. To program this feature in a CUDA Graph with edge data, use a `cudaGraphDependencyType` value of `cudaGraphDependencyTypeProgrammatic` on an edge connecting two kernel nodes [CUDA_C_Programming_Guide:L2397-L2404]. This edge type makes the upstream kernel visible to a `cudaGridDependencySynchronize()` in the downstream kernel [CUDA_C_Programming_Guide:L2397-L2404].

This type must be used with an outgoing port of either `cudaGraphKernelNodePortLaunchCompletion` or `cudaGraphKernelNodePortProgrammatic` [CUDA_C_Programming_Guide:L2397-L2404].

The resulting graph equivalents for stream capture are as follows:

| Stream code (abbreviated) | Resulting graph edge |
| :--- | :--- |
| `cudaLaunchAttribute attribute; attribute.id = cudaLaunchAttributeProgrammaticStreamSerialization; attribute.val.programmaticStreamSerializationAllowed = 1;` | `cudaGraphEdgeData edgeData; edgeData.type = cudaGraphDependencyTypeProgrammatic; edgeData.from_port = cudaGraphKernelNodePortProgrammatic;` |
| `cudaLaunchAttribute attribute; attribute.id = cudaLaunchAttributeProgrammaticEvent; attribute.val.programmaticEvent.triggerAtBlockStart = 0;` | `cudaGraphEdgeData edgeData; edgeData.type = cudaGraphDependencyTypeProgrammatic; edgeData.from_port = cudaGraphKernelNodePortProgrammatic;` |
| `cudaLaunchAttribute attribute; attribute.id = cudaLaunchAttributeProgrammaticEvent; attribute.val.programmaticEvent.triggerAtBlockStart = 1;` | `cudaGraphEdgeData edgeData; edgeData.type = cudaGraphDependencyTypeProgrammatic; edgeData.from_port = cudaGraphKernelNodePortLaunchCompletion;` |

## Legacy Notice

This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA [CUDA_C_Programming_Guide:L2320-L2348].

## See Also

- `cudaTriggerProgrammaticLaunchCompletion`
- `cudaGridDependencySynchronize`
- `cudaLaunchKernelEx`
- `cudaLaunchAttributeProgrammaticStreamSerialization`
- `cudaGraphDependencyTypeProgrammatic`
