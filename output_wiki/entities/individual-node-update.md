# Individual Node Update

Covers updating parameters of instantiated graph nodes directly using specific setter APIs to avoid instantiation overhead. Applicable when the number of nodes to update is small relative to the total graph size.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L2806-L2829

Citation: [CUDA_C_Programming_Guide:L2806-L2829]

````text
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
````
