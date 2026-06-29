# CUDA Direct3D 11 Synchronization Signaling and Waiting

CUDA allows synchronization with Direct3D 11 (D3D11) resources through imported external semaphore objects. These semaphores can wrap either a D3D11 fence or a keyed mutex, enabling CUDA kernels to signal or wait on these objects asynchronously.

## Fence Synchronization

An imported Direct3D 11 fence object can be signaled from CUDA. Signaling such a fence object sets its value to the one specified [CUDA_C_Programming_Guide:L5730-L5730].

### Signaling a Fence

To signal a fence, use `cudaSignalExternalSemaphoresAsync` with the `fence.value` parameter set in `cudaExternalSemaphoreSignalParams` [CUDA_C_Programming_Guide:L5732-L5743].

```cpp
void signalExternalSemaphore(cudaExternalSemaphore_t extSem, unsigned long long value,
    cudaStream_t stream) {
    cudaExternalSemaphoreSignalParams params = {};
    memset(&params, 0, sizeof(params));
    params.params.fence.value = value;
    cudaSignalExternalSemaphoresAsync(&extSem, &params, 1, stream);
}
```

### Waiting on a Fence

To wait on a fence, use `cudaWaitExternalSemaphoresAsync` with the `fence.value` parameter [CUDA_C_Programming_Guide:L5747-L5758].

```cpp
void waitExternalSemaphore(cudaExternalSemaphore_t extSem, unsigned long long value,
    cudaStream_t stream) {
    cudaExternalSemaphoreWaitParams params = {};
    memset(&params, 0, sizeof(params));
    params.params.fence.value = value;
    cudaWaitExternalSemaphoresAsync(&extSem, &params, 1, stream);
}
```

### Ordering Constraints for Fences

When using imported fence semaphores, specific ordering constraints apply:

1. The corresponding wait that waits on the signal must be issued in Direct3D 11 [CUDA_C_Programming_Guide:L5730-L5730].
2. The wait issued in Direct3D 11 must occur after the signal has been issued in CUDA [CUDA_C_Programming_Guide:L5730-L5730].

## Keyed Mutex Synchronization

CUDA also supports signaling and waiting on imported keyed mutex objects. This is particularly useful for synchronizing access to resources shared between CUDA and D3D11.

### Signaling a Keyed Mutex

To signal a keyed mutex, use `cudaSignalExternalSemaphoresAsync` with the `keyedmutex.key` parameter [CUDA_C_Programming_Guide:L5762-L5773].

```cpp
void signalExternalSemaphore(cudaExternalSemaphore_t extSem, unsigned long long key,
    cudaStream_t stream) {
    cudaExternalSemaphoreSignalParams params = {};
    memset(&params, 0, sizeof(params));
    params.params.keyedmutex.key = key;
    cudaSignalExternalSemaphoresAsync(&extSem, &params, 1, stream);
}
```

### Waiting on a Keyed Mutex

To wait on a keyed mutex, use `cudaWaitExternalSemaphoresAsync` with the `keyedmutex.key` and `keyedmutex.timeoutMs` parameters [CUDA_C_Programming_Guide:L5777-L5789].

```cpp
void waitExternalSemaphore(cudaExternalSemaphore_t extSem, unsigned long long key,
    unsigned int timeoutMs, cudaStream_t stream) {
    cudaExternalSemaphoreWaitParams params = {};
    memset(&params, 0, sizeof(params));
    params.params.keyedmutex.key = key;
    params.params.keyedmutex.timeoutMs = timeoutMs;
    cudaWaitExternalSemaphoresAsync(&extSem, &params, 1, stream);
}
```

The `timeoutMs` parameter allows the CUDA wait operation to specify a maximum time to wait for the keyed mutex to become available, providing a mechanism to handle potential deadlocks or long waits in the D3D11 domain.
