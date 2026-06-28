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
