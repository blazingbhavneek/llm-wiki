# Device Graph Requirements

Device graphs in CUDA impose specific structural and operational constraints to ensure correct execution and memory consistency. These requirements govern where graphs can reside, which node types are permitted, and how memory operations are handled.

## General Requirements

### Single Device Residency
All nodes within a graph must reside on a single device. Graphs cannot span multiple devices directly through node placement [CUDA_C_Programming_Guide:L2868-L2887].

### Allowed Node Types
A device graph can only contain the following node types:
*   Kernel nodes
*   Memcpy nodes
*   Memset nodes
*   Child graph nodes [CUDA_C_Programming_Guide:L2868-L2887]

### Kernel Node Constraints
*   **CUDA Dynamic Parallelism**: Kernels launched within a graph are not permitted to use CUDA Dynamic Parallelism (i.e., they cannot launch other kernels) [CUDA_C_Programming_Guide:L2868-L2887].
*   **Cooperative Launches**: Cooperative kernel launches are permitted, provided that Multi-Process Service (MPS) is not in use [CUDA_C_Programming_Guide:L2868-L2887].

## Memcpy Node Requirements

Memcpy nodes in device graphs have strict limitations regarding the types of memory that can be involved in copy operations.

### Permitted Memory Types
Only copies involving the following memory types are permitted:
*   Device memory
*   Pinned device-mapped host memory [CUDA_C_Programming_Guide:L2868-L2887]

### Prohibited Memory Types
*   Copies involving CUDA arrays are not permitted [CUDA_C_Programming_Guide:L2868-L2887].

### Accessibility and Execution Context
*   Both the source and destination operands of a memcpy node must be accessible from the current device at the time the graph is instantiated [CUDA_C_Programming_Guide:L2868-L2887].
*   The copy operation is performed from the device on which the graph resides, even if the target memory is located on a different device [CUDA_C_Programming_Guide:L2868-L2887].

## Memset Node Requirements

While the general node type restrictions apply to memset nodes, specific constraints on memory types and accessibility parallel those of memcpy nodes, ensuring consistent memory handling across data movement operations in device graphs [CUDA_C_Programming_Guide:L2868-L2887].
