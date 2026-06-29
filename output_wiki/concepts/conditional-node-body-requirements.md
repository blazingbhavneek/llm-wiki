# Conditional Node Body Graph Requirements

Conditional nodes in CUDA graphs require their body graphs to adhere to specific structural and operational constraints to ensure deterministic execution and correct memory management.

## General Requirements

The graph serving as the body of a conditional node must satisfy the following general conditions:

*   **Single Device Residency**: All nodes within the graph must reside on a single device [CUDA_C_Programming_Guide:L3143-L3164].
*   **Allowed Node Types**: The graph is restricted to containing only the following node types:
    *   Kernel nodes
    *   Empty nodes
    *   Memcpy nodes
    *   Memset nodes
    *   Child graph nodes
    *   Conditional nodes [CUDA_C_Programming_Guide:L3143-L3164]

## Kernel Node Constraints

Kernels executed within a conditional node body graph are subject to the following restrictions:

*   **No Dynamic Parallelism or Device Graph Launch**: The use of CUDA Dynamic Parallelism or Device Graph Launch by kernels in the graph is not permitted [CUDA_C_Programming_Guide:L3143-L3164].
*   **Cooperative Launches**: Cooperative launches are permitted, provided that Multi-Process Service (MPS) is not in use [CUDA_C_Programming_Guide:L3143-L3164].

## Memcpy and Memset Node Constraints

Memory operations within the conditional node body graph must adhere to strict memory accessibility and type rules:

*   **Supported Memory Types**: Only copies or memsets involving device memory and/or pinned device-mapped host memory are permitted [CUDA_C_Programming_Guide:L3143-L3164].
*   **CUDA Arrays**: Copies or memsets involving CUDA arrays are not permitted [CUDA_C_Programming_Guide:L3143-L3164].
*   **Accessibility**: Both operands involved in the copy or memset operation must be accessible from the current device at the time of graph instantiation [CUDA_C_Programming_Guide:L3143-L3164].
*   **Execution Context**: The copy operation will be performed from the device on which the graph resides, even if the target memory is located on another device [CUDA_C_Programming_Guide:L3143-L3164].
