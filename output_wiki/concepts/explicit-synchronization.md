# Explicit Synchronization

Explicit synchronization allows applications to control the execution order between host threads and CUDA streams, or between different streams on the device. These methods are essential for ensuring that data dependencies are met and that the host is aware of device completion status.

## Host-to-Device Synchronization

The `cudaDeviceSynchronize` function provides a global synchronization point for the host and the device.

*   **`cudaDeviceSynchronize()`**: This function blocks the calling host thread until all preceding commands in all streams of all host threads have completed [CUDA_C_Programming_Guide:L2234-L2235]. It is the most comprehensive synchronization method, ensuring that no work remains pending on the device across the entire context.

## Stream-Specific Synchronization

For finer-grained control, CUDA provides functions that target specific streams, allowing other streams to continue executing on the device while the host waits for a particular stream.

*   **`cudaStreamSynchronize()`**: This function takes a stream as a parameter and blocks the host thread until all preceding commands in the given stream have completed [CUDA_C_Programming_Guide:L2237-L2239]. It is used to synchronize the host with a specific stream, allowing other streams to continue executing on the device concurrently [CUDA_C_Programming_Guide:L2239-L2240].

## Stream Ordering and Events

Synchronization can also be achieved by inserting dependencies between streams using events.

*   **`cudaStreamWaitEvent()`**: This function takes a stream and an event as parameters. It modifies the execution order of the specified stream such that all commands added to the stream after the call to `cudaStreamWaitEvent()` delay their execution until the given event has completed [CUDA_C_Programming_Guide:L2241-L2242]. This allows for explicit ordering of operations between streams based on event completion.

## Non-Blocking Status Checks

For scenarios where blocking is not desired, CUDA provides a query mechanism.

*   **`cudaStreamQuery()`**: This function provides applications with a way to check if all preceding commands in a stream have completed without blocking the host thread [CUDA_C_Programming_Guide:L2243]. It returns a status indicating whether the stream is still executing or has finished.

## Summary of Functions

| Function | Scope | Behavior |
| :--- | :--- | :--- |
| `cudaDeviceSynchronize` | Global (All Streams/Hosts) | Blocks host until all device work is complete. |
| `cudaStreamSynchronize` | Specific Stream | Blocks host until specific stream is complete; others continue. |
| `cudaStreamWaitEvent` | Specific Stream | Delays stream execution until an event is signaled. |
| `cudaStreamQuery` | Specific Stream | Non-blocking check for stream completion status. |

## See Also

*   [Events](concept/events) - For details on `cudaEvent_t` and event-based synchronization.
*   [CUDA Stream Synchronization](concept/explicit-synchronization) - Aliases include `cudaDeviceSynchronize`, `cudaStreamSynchronize`, `cudaStreamWaitEvent`, and `cudaStreamQuery`.
