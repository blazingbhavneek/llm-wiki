# Conditional Graph Nodes Overview

Covers conditional nodes (IF, WHILE, SWITCH) that enable dynamic control flow and looping within graphs. Evaluation happens on-device after dependencies are met. Uses condition handles created before the node, with values set via `cudaGraphSetConditional()` or defaults.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L3115-L3132

Citation: [CUDA_C_Programming_Guide:L3115-L3132]

````text
## 6.2.8.7.8 Conditional Graph Nodes

Conditional nodes allow conditional execution and looping of a graph contained within the conditional node. This allows dynamic and iterative workflows to be represented completely within a graph and frees up the host CPU to perform other work in parallel.

Evaluation of the condition value is performed on the device when the dependencies of the conditional node have been met. Conditional nodes can be one of the following types:

▶ Conditional IF nodes execute their body graph once if the condition value is non-zero when the node is executed. An optional second body graph can be provided and this will be executed once if the condition value is zero when the node is executed.

▶ Conditional WHILE nodes execute their body graph if the condition value is non-zero when the node is executed and will continue to execute their body graph until the condition value is zero.

▶ Conditional SWITCH nodes execute the nth body graph once if the condition value is equal to n. If the condition value does not correspond to a body graph, no body graph is launched.

A condition value is accessed by a conditional handle , which must be created before the node. The condition value can be set by device code using cudaGraphSetConditional(). A default value, applied on each graph launch, can also be specified when the handle is created.

When the conditional node is created, an empty graph is created and the handle is returned to the user so that the graph can be populated. This conditional body graph can be populated using either the graph APIs or cudaStreamBeginCaptureToGraph().

Conditional nodes can be nested.
````
