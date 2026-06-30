# External Resource Interoperability

Introduces the framework for importing external memory and synchronization objects (semaphores) from other APIs using OS-native handles or NVIDIA SWI. Covers cudaImportExternalMemory(), cudaExternalMemoryGetMappedBuffer(), cudaImportExternalSemaphore(), and their lifecycle management.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L4519-L4526

Citation: [CUDA_C_Programming_Guide:L4519-L4526]

````text

## 6.2.16. External Resource Interoperability

External resource interoperability allows CUDA to import certain resources that are explicitly exported by other APIs. These objects are typically exported by other APIs using handles native to the Operating System, like file descriptors on Linux or NT handles on Windows. They could also be exported using other unified interfaces such as the NVIDIA Software Communication Interface. There are two types of resources that can be imported: memory objects and synchronization objects.

Memory objects can be imported into CUDA using cudaImportExternalMemory(). An imported memory object can be accessed from within kernels using device pointers mapped onto the memory object via cudaExternalMemoryGetMappedBuffer()or CUDA mipmapped arrays mapped via cudaExternalMemoryGetMappedMipmappedArray(). Depending on the type of memory object, it may be possible for more than one mapping to be setup on a single memory object. The mappings must match the mappings setup in the exporting API. Any mismatched mappings result in undefined behavior. Imported memory objects must be freed using cudaDestroyExternalMemory(). Freeing a memory object does not free any mappings to that object. Therefore, any device pointers mapped onto that object must be explicitly freed using cudaFree() and any CUDA mipmapped arrays mapped onto that object must be explicitly freed using cudaFreeMipmappedArray(). It is illegal to access mappings to an object after it has been destroyed.

Synchronization objects can be imported into CUDA using cudaImportExternalSemaphore(). An imported synchronization object can then be signaled using cudaSignalExternalSemaphoresAsync() and waited on using cudaWaitExternalSemaphoresAsync(). It is illegal to issue a wait before the corresponding signal has been issued. Also, depending on the type of the imported synchronization object, there may be additional constraints imposed on how they can be signaled and waited on, as described in subsequent sections. Imported semaphore objects must be freed using cudaDestroyExternalSemaphore(). All outstanding signals and waits must have completed before the semaphore object is destroyed.
````
