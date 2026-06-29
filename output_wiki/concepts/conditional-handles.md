# Conditional Handles

A condition value in a CUDA graph is represented by the `cudaGraphConditionalHandle` type. These handles are created using the `cudaGraphConditionalHandleCreate()` function [CUDA_C_Programming_Guide:L3133-L3142].

## Key Properties

*   **Association**: A handle must be associated with a single conditional node [CUDA_C_Programming_Guide:L3133-L3142].
*   **Lifetime**: Handles cannot be destroyed [CUDA_C_Programming_Guide:L3133-L3142].
*   **Updates**: The default value and flags associated with a handle are updated during whole graph updates [CUDA_C_Programming_Guide:L3133-L3142].

## Initialization and Execution Behavior

When creating a handle, the `cudaGraphCondAssignDefault` flag can be specified [CUDA_C_Programming_Guide:L3133-L3142].

*   **With `cudaGraphCondAssignDefault`**: The condition value is initialized to the specified default value at the beginning of each graph execution [CUDA_C_Programming_Guide:L3133-L3142].
*   **Without `cudaGraphCondAssignDefault`**: The condition value is undefined at the start of each graph execution. Code must not assume that the condition value persists across executions [CUDA_C_Programming_Guide:L3133-L3142].

## Related Terms

*   `cudaGraphConditionalHandle`
*   `cudaGraphConditionalHandleCreate`
*   `cudaGraphCondAssignDefault`
