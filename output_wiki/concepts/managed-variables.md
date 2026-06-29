# __managed__ Variables

CUDA `__managed__` variables behave as if they were allocated via `cudaMallocManaged()` [[CUDA_C_Programming_Guide:L21038-L21043]]. They simplify programs with global variables, making it particularly easy to exchange data between host and device without manual allocations or copying [[CUDA_C_Programming_Guide:L21038-L21043]].

## Syntax and Semantics

A `__managed__` variable implies `__device__` and is equivalent to `__managed__ __device__`, which is also allowed [[CUDA_C_Programming_Guide:L21088-L21099]]. Variables marked `__constant__` may not be marked as `__managed__` [[CUDA_C_Programming_Guide:L21088-L21099]].

## Behavior and Visibility

Accessing `__managed__` variables can trigger CUDA context creation if a context for the current device hasn’t already been created [[CUDA_C_Programming_Guide:L21088-L21099]]. For example, accessing a managed variable before a kernel launch triggers context creation on the default device; in the absence of that access, the kernel launch would have triggered context creation [[CUDA_C_Programming_Guide:L21088-L21099]].

A valid CUDA context is necessary for the correct operation of `__managed__` variables [[CUDA_C_Programming_Guide:L21088-L21099]].

On systems with full CUDA Unified Memory support, file-scope or global-scope variables cannot be directly accessed by device code [[CUDA_C_Programming_Guide:L21038-L21043]]. However, a pointer to these variables may be passed to the kernel as an argument [[CUDA_C_Programming_Guide:L21038-L21043]]. The written value is visible on both CPU and GPU without explicit `cudaMemcpy()` commands [[CUDA_C_Programming_Guide:L21088-L21099]].

## C++ Constraints

C++ objects declared as `__managed__` are subject to certain specific constraints, particularly where static initializers are concerned [[CUDA_C_Programming_Guide:L21088-L21099]]. Please refer to C++ Language Support for a list of these constraints [[CUDA_C_Programming_Guide:L21088-L21099]].

## Partial Support

For devices with CUDA Managed Memory without full support, visibility of `__managed__` variables for asynchronous operations executing in CUDA streams is discussed in the section on Managing Data Visibility and Concurrent CPU + GPU Access with Streams [[CUDA_C_Programming_Guide:L21088-L21099]].
