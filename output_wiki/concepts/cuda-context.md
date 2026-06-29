# CUDA Context

A CUDA context is analogous to a CPU process. All resources and actions performed within the driver API are encapsulated inside a CUDA context, and the system automatically cleans up these resources when the context is destroyed [CUDA_C_Programming_Guide:L20155-L20171].

## Key Characteristics

### Address Space
Besides objects such as modules and texture or surface references, each context has its own distinct address space [CUDA_C_Programming_Guide:L20155-L20171]. As a result, `CUdeviceptr` values from different contexts reference different memory locations [CUDA_C_Programming_Guide:L20155-L20171].

### Thread Affinity and Stack
A host thread may have only one device context current at a time [CUDA_C_Programming_Guide:L20155-L20171]. When a context is created with `cuCtxCreate()`, it is made current to the calling host thread [CUDA_C_Programming_Guide:L20155-L20171]. CUDA functions that operate in a context (most functions that do not involve device enumeration or context management) will return `CUDA_ERROR_INVALID_CONTEXT` if a valid context is not current to the thread [CUDA_C_Programming_Guide:L20155-L20171].

Each host thread has a stack of current contexts [CUDA_C_Programming_Guide:L20155-L20171]. `cuCtxCreate()` pushes the new context onto the top of the stack [CUDA_C_Programming_Guide:L20155-L20171]. `cuCtxPopCurrent()` may be called to detach the context from the host thread [CUDA_C_Programming_Guide:L20155-L20171]. The context is then “floating” and may be pushed as the current context for any host thread [CUDA_C_Programming_Guide:L20155-L20171]. `cuCtxPopCurrent()` also restores the previous current context, if any [CUDA_C_Programming_Guide:L20155-L20171].

### Usage Count and Interoperability
A usage count is also maintained for each context [CUDA_C_Programming_Guide:L20155-L20171]. `cuCtxCreate()` creates a context with a usage count of 1 [CUDA_C_Programming_Guide:L20155-L20171]. `cuCtxAttach()` increments the usage count and `cuCtxDetach()` decrements it [CUDA_C_Programming_Guide:L20155-L20171]. A context is destroyed when the usage count goes to 0 when calling `cuCtxDetach()` or `cuCtxDestroy()` [CUDA_C_Programming_Guide:L20155-L20171].

The driver API is interoperable with the runtime and it is possible to access the primary context (see Initialization) managed by the runtime from the driver API via `cuDevicePrimaryCtxRetain()` [CUDA_C_Programming_Guide:L20155-L20171].

Usage count facilitates interoperability between third party authored code operating in the same context [CUDA_C_Programming_Guide:L20155-L20171]. For example, if three libraries are loaded to use the same context, each library would call `cuCtxAttach()` to increment the usage count and `cuCtxDetach()` to decrement the usage count when the library is done using the context [CUDA_C_Programming_Guide:L20155-L20171]. For most libraries, it is expected that the application will have created a context before loading or initializing the library; that way, the application can create the context using its own heuristics, and the library simply operates on the context handed to it [CUDA_C_Programming_Guide:L20155-L20171]. Libraries that wish to create their own contexts - unbeknownst to their API clients who may or may not have created contexts of their own - would use `cuCtxPushCurrent()` and `cuCtxPopCurrent()` [CUDA_C_Programming_Guide:L20155-L20171].
