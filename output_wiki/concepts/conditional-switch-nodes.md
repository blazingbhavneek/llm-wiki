# Conditional SWITCH Nodes

Conditional SWITCH nodes are a feature introduced in CUDA 12.8 that enable the execution of one of *n* different graphs within a conditional node [CUDA_C_Programming_Guide:L3338-L3341].

## Behavior

The execution path is determined by the condition value evaluated at runtime:

*   If the condition value is equal to *n*, the *n*th graph is executed [CUDA_C_Programming_Guide:L3338-L3341].
*   If the condition value is greater than or equal to *n*, no graph is executed [CUDA_C_Programming_Guide:L3338-L3341].

## Implementation

SWITCH nodes are created using the CUDA Graph API. The condition value is typically set using an upstream kernel that writes to a `cudaGraphConditionalHandle` [CUDA_C_Programming_Guide:L3342-L3401].

### Creating the Conditional Node

To define a SWITCH node, the `cudaGraphNodeTypeConditional` node type is used with the `cudaGraphCondTypeSwitch` type specified in the node parameters [CUDA_C_Programming_Guide:L3342-L3401]. The `size` parameter indicates the number of available body graphs [CUDA_C_Programming_Guide:L3342-L3401].

```cpp
cudaGraphNodeParams cParams = { cudaGraphNodeTypeConditional };
cParams.conditional.handle = handle;
cParams.conditional.type = cudaGraphCondTypeSwitch;
cParams.conditional.size = 5;
```

### Populating Body Graphs

The API provides access to the body graphs via `cParams.conditional.phGraph_out`, which is an array of `cudaGraph_t` pointers [CUDA_C_Programming_Guide:L3342-L3401]. Developers populate these body graphs independently using standard graph API calls (e.g., `cudaGraphAddNode`) [CUDA_C_Programming_Guide:L3342-L3401].

### Setting the Condition

An upstream kernel can be added to the graph to set the condition value. This is done by passing the `cudaGraphConditionalHandle` to a kernel function that calls `cudaGraphSetConditional` [CUDA_C_Programming_Guide:L3342-L3401].

```cpp
__global__ void setHandle(cudaGraphConditionalHandle handle)
{
    ...
    cudaGraphSetConditional(handle, value);
    ...
}
```

### Execution Flow

1.  Create the main graph and the conditional handle [CUDA_C_Programming_Guide:L3342-L3401].
2.  Add the upstream kernel node that sets the condition value [CUDA_C_Programming_Guide:L3342-L3401].
3.  Add the conditional SWITCH node, linking it to the handle [CUDA_C_Programming_Guide:L3342-L3401].
4.  Populate the body graphs accessible through the handle [CUDA_C_Programming_Guide:L3342-L3401].
5.  Instantiate and launch the graph [CUDA_C_Programming_Guide:L3342-L3401].

## Example Diagram

A typical configuration involves a graph where a middle node acts as a conditional SWITCH node, branching to different body graphs based on the condition [CUDA_C_Programming_Guide:L3338-L3341].

![](images/2df151bcaf93eec571e6ab4ffd31348d9c97e94d4f586267062123814bb0f4f2.jpg)  
Figure 25: Conditional SWITCH Node

## References

*   CUDA C Programming Guide, Section 6.2.8.7.8.5 Conditional SWITCH Nodes [CUDA_C_Programming_Guide:L3338-L3341]
*   CUDA C Programming Guide, Code Example for SWITCH Node Creation [CUDA_C_Programming_Guide:L3342-L3401]
