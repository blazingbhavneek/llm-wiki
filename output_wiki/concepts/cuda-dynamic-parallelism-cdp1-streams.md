# CUDA Dynamic Parallelism (CDP1) Streams

In CUDA Dynamic Parallelism version 1 (CDP1), stream management on the device differs significantly from host-side execution. Both named and unnamed (NULL) streams are available from the device runtime, but they operate under strict scoping and synchronization rules [CUDA_C_Programming_Guide:L14532-L14546].

## Stream Scope and Uniqueness

Named streams may be used by any thread within a thread block, but stream handles are not guaranteed to be unique between blocks. Consequently, stream handles must be treated as private to the block in which they are created [CUDA_C_Programming_Guide:L14532-L14546].

- **Local Scope**: Stream handles may not be passed to other blocks or to child/parent kernels [CUDA_C_Programming_Guide:L14532-L14546].
- **Undefined Behavior**: Using a stream handle within a block that did not allocate it results in undefined behavior [CUDA_C_Programming_Guide:L14532-L14546].

## Concurrency

Similar to host-side launch, work launched into separate streams may run concurrently. However, actual concurrency is not guaranteed [CUDA_C_Programming_Guide:L14532-L14546]. Programs that depend upon concurrency between child kernels are not supported by the CUDA programming model and will have undefined behavior [CUDA_C_Programming_Guide:L14532-L14546].

## Stream Creation and Flags

The host-side NULL stream's cross-stream barrier semantic is not supported on the device [CUDA_C_Programming_Guide:L14532-L14546]. To retain semantic compatibility with the host runtime, all device streams must be created using the `cudaStreamCreateWithFlags()` API, passing the `cudaStreamNonBlocking` flag [CUDA_C_Programming_Guide:L14532-L14546].

The `cudaStreamCreate()` call is a host-runtime-only API and will fail to compile when used in device code [CUDA_C_Programming_Guide:L14532-L14546].

## Synchronization

Because `cudaStreamSynchronize()` and `cudaStreamQuery()` are unsupported by the device runtime, `cudaDeviceSynchronize()` should be used when the application needs to know that stream-launched child kernels have completed [CUDA_C_Programming_Guide:L14532-L14546].

**Deprecation Warning**: Explicit synchronization with child kernels from a parent block (i.e., using `cudaDeviceSynchronize()` in device code) is deprecated in CUDA 11.6, removed for compute_90+ compilation, and is slated for full removal in a future CUDA release [CUDA_C_Programming_Guide:L14532-L14546].

## See Also

- For the CDP2 version of this document, see the Streams section in the CDP2 documentation [CUDA_C_Programming_Guide:L14532-L14546].
- The Implicit (NULL) Stream (CDP1) [CUDA_C_Programming_Guide:L14532-L14546].
