# Individual Node Enable

Covers enabling or disabling specific kernel, memset, and memcpy nodes within an instantiated graph using `cudaGraphNodeSetEnabled()`. Disabled nodes act as empty nodes until re-enabled, and parameter updates while disabled apply upon re-enablement.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L2830-L2843

Citation: [CUDA_C_Programming_Guide:L2830-L2843]

````text
## 6.2.8.7.5.4 Individual Node Enable

Kernel, memset and memcpy nodes in an instantiated graph can be enabled or disabled using the cudaGraphNodeSetEnabled() API. This allows the creation of a graph which contains a superset of the desired functionality which can be customized for each launch. The enable state of a node can be queried using the cudaGraphNodeGetEnabled() API.

A disabled node is functionally equivalent to empty node until it is reenabled. Node parameters are not afected by enabling/disabling a node. Enable state is unafected by individual node update or whole graph update with cudaGraphExecUpdate(). Parameter updates while the node is disabled will take efect when the node is reenabled.

The following methods are available for enabling/disabling cudaGraphExec\_t nodes, as well as querying their status:

▶ cudaGraphNodeSetEnabled()

▶ cudaGraphNodeGetEnabled()

Refer to the Graph API for more information on usage and current limitations.
````
