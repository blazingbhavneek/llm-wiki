# Individual Node Update

Instantiated graph node parameters can be updated directly. This eliminates the overhead of instantiation as well as the overhead of creating a new `cudaGraph_t` [CUDA_C_Programming_Guide:L2806-L2829]. If the number of nodes requiring update is small relative to the total number of nodes in the graph, it is better to update the nodes individually [CUDA_C_Programming_Guide:L2806-L2829].

The following methods are available for updating `cudaGraphExec_t` nodes [CUDA_C_Programming_Guide:L2806-L2829]:

* `cudaGraphExecKernelNodeSetParams()`
* `cudaGraphExecMemcpyNodeSetParams()`
* `cudaGraphExecMemsetNodeSetParams()`
* `cudaGraphExecHostNodeSetParams()`
* `cudaGraphExecChildGraphNodeSetParams()`
* `cudaGraphExecEventRecordNodeSetEvent()`
* `cudaGraphExecEventWaitNodeSetEvent()`
* `cudaGraphExecExternalSemaphoresSignalNodeSetParams()`
* `cudaGraphExecExternalSemaphoresWaitNodeSetParams()`

Please see the Graph API for more information on usage and current limitations [CUDA_C_Programming_Guide:L2806-L2829].
