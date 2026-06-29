# Signaling and Waiting on Imported D3D12 Fence Objects

This section describes the mechanism for synchronizing CUDA streams with Direct3D 12 (D3D12) resources by signaling and waiting on imported D3D12 fence objects. These operations allow CUDA kernels to coordinate with D3D12 rendering or compute commands.

## Signaling a D3D12 Fence

An imported Direct3D 12 fence object can be signaled from CUDA. Signaling such a fence object sets its value to the one specified. This is achieved using the `cudaSignalExternalSemaphoresAsync` function.

```c
void signalExternalSemaphore(cudaExternalSemaphore_t extSem, unsigned long long value,
    cudaStream_t stream) {
    cudaExternalSemaphoreSignalParams params = {};

    memset(&params, 0, sizeof(params));

    params.params.fence.value = value;

    cudaSignalExternalSemaphoresAsync(&extSem, &params, 1, stream);
}
```

When signaling a D3D12 fence from CUDA, the corresponding wait operation that consumes this signal must be issued in Direct3D 12. Furthermore, the wait in D3D12 must be issued **after** the signal has been issued in CUDA to ensure correct synchronization ordering [CUDA_C_Programming_Guide:L5302-L5336].

## Waiting on a D3D12 Fence

An imported Direct3D 12 fence object can be waited on from CUDA. Waiting on such a fence object causes the CUDA stream to block until the fence's value becomes greater than or equal to the specified value. This is achieved using the `cudaWaitExternalSemaphoresAsync` function.

```c
void waitExternalSemaphore(cudaExternalSemaphore_t extSem, unsigned long long value,
    cudaStream_t stream) {
    cudaExternalSemaphoreWaitParams params = {};

    memset(&params, 0, sizeof(params));

    params.params.fence.value = value;

    cudaWaitExternalSemaphoresAsync(&extSem, &params, 1, stream);
}
```

When waiting on a D3D12 fence from CUDA, the corresponding signal operation that this wait is waiting on must be issued in Direct3D 12. Additionally, the signal in D3D12 must be issued **before** this wait can be issued in CUDA [CUDA_C_Programming_Guide:L5302-L5336].

## Key Constraints

1.  **Domain Separation**: Operations originating in CUDA (signaling or waiting) have corresponding requirements in D3D12. If CUDA signals, D3D12 must wait. If CUDA waits, D3D12 must signal.
2.  **Ordering**: The synchronization relies on the temporal order of operations across the two APIs. The signal must precede the wait in the logical timeline of the resource sharing.
    *   CUDA Signal -> D3D12 Wait: The D3D12 wait must be issued after the CUDA signal.
    *   D3D12 Signal -> CUDA Wait: The D3D12 signal must be issued before the CUDA wait.

## See Also

*   `cudaSignalExternalSemaphoresAsync`
*   `cudaWaitExternalSemaphoresAsync`
*   CUDA D3D12 Interoperability
