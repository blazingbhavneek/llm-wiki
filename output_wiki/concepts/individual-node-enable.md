# Individual Node Enable/Disable

Kernel, memset, and memcpy nodes within an instantiated graph can be individually enabled or disabled using the `cudaGraphNodeSetEnabled()` API [CUDA_C_Programming_Guide:L2830-L2833]. This capability allows developers to create a graph containing a superset of desired functionality, which can then be customized for each specific launch by selectively enabling or disabling nodes [CUDA_C_Programming_Guide:L2833-L2835].

The enable state of a node can be queried using the `cudaGraphNodeGetEnabled()` API [CUDA_C_Programming_Guide:L2835-L2836].

## Behavior of Disabled Nodes

A disabled node is functionally equivalent to an empty node until it is re-enabled [CUDA_C_Programming_Guide:L2837]. Key characteristics of this state include:

*   **Parameter Stability**: Node parameters are not affected by the act of enabling or disabling a node [CUDA_C_Programming_Guide:L2838].
*   **Update Persistence**: The enable state is unaffected by individual node updates or whole graph updates performed via `cudaGraphExecUpdate()` [CUDA_C_Programming_Guide:L2838-L2839].
*   **Deferred Execution**: Parameter updates made while a node is disabled will take effect when the node is re-enabled [CUDA_C_Programming_Guide:L2839-L2840].

## API Reference

The following methods are available for managing the enable/disable state of `cudaGraphExec_t` nodes:

*   `cudaGraphNodeSetEnabled()`: Enables or disables a specific node.
*   `cudaGraphNodeGetEnabled()`: Queries the current enable status of a node.

For more information on usage and current limitations, refer to the Graph API documentation [CUDA_C_Programming_Guide:L2841-L2843].
