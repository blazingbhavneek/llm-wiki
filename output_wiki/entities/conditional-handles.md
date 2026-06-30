# Conditional Handles

Covers `cudaGraphConditionalHandle` creation and lifecycle. Handles are tied to a single node, cannot be destroyed, and can be initialized with a default value using `cudaGraphCondAssignDefault`. Defaults update during whole-graph updates.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L3133-L3142

Citation: [CUDA_C_Programming_Guide:L3133-L3142]

````text
## 6.2.8.7.8.1 Conditional Handles

A condition value is represented by cudaGraphConditionalHandle and is created by cudaGraph-ConditionalHandleCreate().

The handle must be associated with a single conditional node. Handles cannot be destroyed.

If cudaGraphCondAssignDefault is specified when the handle is created, the condition value will be initialized to the specified default at the beginning of each graph execution. If this flag is not provided, the condition value is undefined at the start of each graph execution and code should not assume that the condition value persists across executions.

The default value and flags associated with a handle will be updated during whole graph update.
````
