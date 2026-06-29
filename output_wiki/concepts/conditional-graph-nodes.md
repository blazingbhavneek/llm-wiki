# Conditional Graph Nodes

Conditional nodes allow conditional execution and looping of a graph contained within the conditional node. This allows dynamic and iterative workflows to be represented completely within a graph and frees up the host CPU to perform other work in parallel [CUDA_C_Programming_Guide:L3115-L3119].

## Overview

Evaluation of the condition value is performed on the device when the dependencies of the conditional node have been met [CUDA_C_Programming_Guide:L3119-L3120]. A condition value is accessed by a conditional handle, which must be created before the node [CUDA_C_Programming_Guide:L3126-L3127]. The condition value can be set by device code using `cudaGraphSetConditional()` [CUDA_C_Programming_Guide:L3127]. A default value, applied on each graph launch, can also be specified when the handle is created [CUDA_C_Programming_Guide:L3127].

## Types

Conditional nodes can be one of the following types [CUDA_C_Programming_Guide:L3120-L3125]:

* **Conditional IF nodes**: Execute their body graph once if the condition value is non-zero when the node is executed. An optional second body graph can be provided and this will be executed once if the condition value is zero when the node is executed [CUDA_C_Programming_Guide:L3121-L3123].
* **Conditional WHILE nodes**: Execute their body graph if the condition value is non-zero when the node is executed and will continue to execute their body graph until the condition value is zero [CUDA_C_Programming_Guide:L3123-L3124].
* **Conditional SWITCH nodes**: Execute the nth body graph once if the condition value is equal to n. If the condition value does not correspond to a body graph, no body graph is launched [CUDA_C_Programming_Guide:L3124-L3125].

## Creation and Population

When the conditional node is created, an empty graph is created and the handle is returned to the user so that the graph can be populated. This conditional body graph can be populated using either the graph APIs or `cudaStreamBeginCaptureToGraph()` [CUDA_C_Programming_Guide:L3128-L3130].

Conditional nodes can be nested [CUDA_C_Programming_Guide:L3131].

## See Also

* `cudaGraphSetConditional`
* `cudaStreamBeginCaptureToGraph`
