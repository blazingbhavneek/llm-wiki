# CUDA Context

A CUDA context is analogous to a CPU process, encapsulating all driver API resources and actions. It maintains a distinct address space, manages current context per host thread via a stack, and tracks usage counts for interoperability.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L20155-L20171

Citation: [CUDA_C_Programming_Guide:L20155-L20171]

````text
## 21.1. Context

A CUDA context is analogous to a CPU process. All resources and actions performed within the driver API are encapsulated inside a CUDA context, and the system automatically cleans up these resources when the context is destroyed. Besides objects such as modules and texture or surface references, each context has its own distinct address space. As a result, CUdeviceptr values from diferent contexts reference diferent memory locations.

A host thread may have only one device context current at a time. When a context is created with cuCtxCreate(), it is made current to the calling host thread. CUDA functions that operate in a context (most functions that do not involve device enumeration or context management) will return CUDA\_ERROR\_INVALID\_CONTEXT if a valid context is not current to the thread.

Each host thread has a stack of current contexts. cuCtxCreate() pushes the new context onto the top of the stack. cuCtxPopCurrent() may be called to detach the context from the host thread. The context is then “floating” and may be pushed as the current context for any host thread. cuCtx-PopCurrent() also restores the previous current context, if any.

A usage count is also maintained for each context. cuCtxCreate() creates a context with a usage count of 1. cuCtxAttach() increments the usage count and cuCtxDetach() decrements it. A context is destroyed when the usage count goes to 0 when calling cuCtxDetach() or cuCtxDestroy().

The driver API is interoperable with the runtime and it is possible to access the primary context (see Initialization) managed by the runtime from the driver API via cuDevicePrimaryCtxRetain().

Usage count facilitates interoperability between third party authored code operating in the same context. For example, if three libraries are loaded to use the same context, each library would call cuCtxAttach() to increment the usage count and cuCtxDetach() to decrement the usage count when the library is done using the context. For most libraries, it is expected that the application will have created a context before loading or initializing the library; that way, the application can create the context using its own heuristics, and the library simply operates on the context handed to it. Libraries that wish to create their own contexts - unbeknownst to their API clients who may or may not have created contexts of their own - would use cuCtxPushCurrent() and cuCtxPopCurrent() as illustrated in the following figure.

![](images/5d203754ad02283a35f8c4158d8af7a34015378feb9638f4298b44d09aa72d85.jpg)  
Figure 41: Library Context Management
````
