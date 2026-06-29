# CUDA Dynamic Parallelism (CDP1) Events

In CUDA Dynamic Parallelism version 1 (CDP1), support for CUDA events is limited compared to the host-side or CDP2 capabilities. Only inter-stream synchronization is supported, meaning that `cudaStreamWaitEvent()` is the only supported event-related function for synchronization purposes.

## Supported and Unsupported Operations

The following event functions are **not supported** within device code under CDP1:
*   `cudaEventSynchronize()`
*   `cudaEventElapsedTime()`
*   `cudaEventQuery()`

Because `cudaEventElapsedTime()` is unsupported, timing measurements cannot be performed on events created in device code. Consequently, all events must be created using `cudaEventCreateWithFlags()` with the `cudaEventDisableTiming` flag [CUDA_C_Programming_Guide:L14550-L14559].

## Scope and Lifetime

Event objects in CDP1 follow the same scoping rules as other device runtime objects:
*   **Block-Local Scope:** Events are local to the thread block that created them. They cannot be passed to other kernels or between different blocks within the same kernel [CUDA_C_Programming_Guide:L14550-L14559].
*   **Intra-Block Sharing:** Events may be shared among all threads within the thread block that created them [CUDA_C_Programming_Guide:L14550-L14559].
*   **Handle Uniqueness:** Event handles are not guaranteed to be unique across different blocks. Using an event handle within a block that did not create it results in undefined behavior [CUDA_C_Programming_Guide:L14550-L14559].

## Stream Context

The device runtime provides a single implicit, unnamed stream shared between all threads in a block. While the host-side NULL stream has additional barrier synchronization semantics with other streams, work launched into the NULL stream from device code does not insert an implicit dependency on pending work in any other streams (including NULL streams of other thread blocks) because all named streams must be created with the `cudaStreamNonBlocking` flag [CUDA_C_Programming_Guide:L14550-L14559].

For the CDP2 version of event support, see the Events section in the CDP2 documentation.
