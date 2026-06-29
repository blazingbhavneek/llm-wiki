# EGM: Single-Node, Multi-GPU

In a single-node, multi-GPU system, the user must provide host information for placement. EGM follows the approach of using NUMA node IDs to express this information naturally.

To determine the appropriate placement, the user can use the `cuDeviceGetAttribute` function to learn the closest NUMA node ID [CUDA_C_Programming_Guide:L22258-L22258]. Once the NUMA topology is identified, the user can allocate and manage EGM memory using either the VMM (Virtual Memory Management) API or the CUDA Memory Pool [CUDA_C_Programming_Guide:L22258-L22258].

## See Also

- Socket Identifiers: What are they? How to access them?
