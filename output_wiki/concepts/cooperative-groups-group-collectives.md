# Group Collectives

Overview of collective operations provided by the Cooperative Groups library. These operations require participation of all threads in the specified group to complete, and all threads must pass the same values for corresponding arguments unless explicitly allowed otherwise.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L12561-L12564

Citation: [CUDA_C_Programming_Guide:L12561-L12564]

````text

## 11.6. Group Collectives

Cooperative Groups library provides a set of collective operations that can be performed by a group of threads. These operations require participation of all threads in the specified group in order to complete the operation. All threads in the group need to pass the same values for corresponding arguments to each collective call, unless diferent values are explicitly allowed in the argument description. Otherwise the behavior of the call is undefined.
````
