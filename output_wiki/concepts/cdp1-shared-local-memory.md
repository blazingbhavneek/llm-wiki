# CDP1 Shared and Local Memory

In the context of CUDA Dynamic Parallelism version 1 (CDP1), memory accessibility rules differ significantly from those in CDP2. Shared and local memory are strictly scoped to the execution context that created them.

## Memory Scope and Visibility

Shared memory and local memory are private to a thread block or thread, respectively [CUDA_C_Programming_Guide:L14431-L14440]. They are not visible or coherent between parent and child kernels [CUDA_C_Programming_Guide:L14431-L14440]. This means that a child kernel cannot access shared or local memory allocated by its parent, nor can it access shared or local memory allocated by sibling kernels [CUDA_C_Programming_Guide:L14431-L14440].

## Undefined Behavior

Referencing an object located in shared or local memory outside of the scope within which it belongs results in undefined behavior [CUDA_C_Programming_Guide:L14431-L14440]. This may cause runtime errors [CUDA_C_Programming_Guide:L14431-L14440]. Specifically, passing pointers to local or shared memory as arguments to a kernel launch is illegal [CUDA_C_Programming_Guide:L14431-L14440].

## Compiler and Runtime Checks

The NVIDIA compiler attempts to warn developers if it can detect that a pointer to local or shared memory is being passed as an argument to a kernel launch [CUDA_C_Programming_Guide:L14431-L14440]. At runtime, programmers can use the `__isGlobal()` intrinsic to determine whether a pointer references global memory, which is safe to pass to a child launch [CUDA_C_Programming_Guide:L14431-L14440].

## Interaction with Asynchronous Memory Operations

Calls to `cudaMemcpy*Async()` or `cudaMemset*Async()` may invoke new child kernels on the device to preserve stream semantics [CUDA_C_Programming_Guide:L14431-L14440]. Consequently, passing shared or local memory pointers to these APIs is illegal and will return an error [CUDA_C_Programming_Guide:L14431-L14440].

## Note on CDP2

For the CDP2 version of these rules, see the "Shared and Local Memory" section in the CDP2 documentation [CUDA_C_Programming_Guide:L14431-L14440].
