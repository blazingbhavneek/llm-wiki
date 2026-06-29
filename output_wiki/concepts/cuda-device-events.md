# CUDA Device Events

CUDA device runtime events offer a restricted subset of the host-side CUDA event API, primarily designed for synchronization between streams executing on the device.

## Supported Operations

Only the inter-stream synchronization capabilities of CUDA events are supported in the device runtime [CUDA_C_Programming_Guide:L13949-L13954]. Specifically:

*   **Supported**: `cudaStreamWaitEvent()` allows a stream to wait for the completion of an event [CUDA_C_Programming_Guide:L13949-L13954].
*   **Unsupported**: Host-side query and synchronization functions are not available. This includes `cudaEventSynchronize()`, `cudaEventElapsedTime()`, and `cudaEventQuery()` [CUDA_C_Programming_Guide:L13949-L13954].

## Timing Restrictions

Because `cudaEventElapsedTime()` is not supported, timing measurements cannot be performed using events within the device runtime [CUDA_C_Programming_Guide:L13949-L13954]. Consequently, events must be created with the `cudaEventDisableTiming` flag to ensure compatibility [CUDA_C_Programming_Guide:L13949-L13954].

## Scope and Lifetime

Event objects created in the device runtime follow specific scoping rules similar to named streams [CUDA_C_Programming_Guide:L13949-L13954]:

*   **Visibility**: Event objects may be shared between all threads within the grid that created them [CUDA_C_Programming_Guide:L13949-L13954].
*   **Local Scope**: Events are local to the grid that created them and cannot be passed to other kernels outside that grid [CUDA_C_Programming_Guide:L13949-L13954].
*   **Handle Uniqueness**: Event handles are not guaranteed to be unique between different grids. Using an event handle within a grid that did not create it results in undefined behavior [CUDA_C_Programming_Guide:L13949-L13954].
