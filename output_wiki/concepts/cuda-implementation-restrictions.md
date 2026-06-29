# CUDA Implementation Restrictions

Dynamic Parallelism guarantees all semantics described in the CUDA documentation. However, certain hardware and software resources are implementation-dependent and limit the scale, performance, and other properties of a program which uses the device runtime [[CUDA_C_Programming_Guide:L14221-L14223]].

These restrictions mean that while the logical behavior of dynamic parallelism is consistent, the practical limits on how many kernels can be launched, the depth of the launch hierarchy, and the overall execution performance are constrained by the specific underlying hardware and software implementation details.
