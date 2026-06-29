# cudaMemcpyAsync Current Context/Device Sensitivity

## Overview
When using asynchronous memory copy operations in CUDA, the handling of device contexts differs based on the specific API function and the memory allocation method used. Specifically, `cudaMemcpyAsync` has strict requirements regarding the current context of the calling thread, while `cudaMemcpyPeerAsync` operates differently by referencing explicit device contexts.

## cudaMemcpyAsync and cudaMallocAsync
In the current CUDA driver, any asynchronous memory copy (`cudaMemcpyAsync`) that involves memory allocated via `cudaMallocAsync` must be performed using the specified stream’s context as the calling thread’s current context [CUDA_C_Programming_Guide:L15864-L15867]. This ensures that the operation is correctly associated with the context in which the memory was allocated.

## cudaMemcpyPeerAsync Behavior
The requirement to set the current context does not apply to `cudaMemcpyPeerAsync`. This is because `cudaMemcpyPeerAsync` references the device primary contexts that are explicitly specified in the API call, rather than relying on the calling thread's current context [CUDA_C_Programming_Guide:L15864-L15867].

## Key Distinctions
- **cudaMemcpyAsync**: Requires the calling thread's current context to match the stream's context, particularly when dealing with memory from `cudaMallocAsync`.
- **cudaMemcpyPeerAsync**: Uses explicitly specified device primary contexts, making the current context of the calling thread irrelevant for context resolution.

## References
- CUDA C Programming Guide, Section 15.13.1: cudaMemcpyAsync Current Context/Device Sensitivity [CUDA_C_Programming_Guide:L15864-L15867]
