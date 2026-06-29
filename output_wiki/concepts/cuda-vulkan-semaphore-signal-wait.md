# Signaling and Waiting on Imported Vulkan Synchronization Objects

CUDA provides APIs to synchronize with imported Vulkan semaphore objects, allowing CUDA streams to wait on or signal Vulkan synchronization primitives. These operations are performed asynchronously using `cudaSignalExternalSemaphoresAsync` and `cudaWaitExternalSemaphoresAsync`.

## Signaling an Imported Semaphore

An imported Vulkan semaphore object can be signaled from CUDA. Signaling such a semaphore object sets it to the signaled state. The corresponding wait that waits on this signal must be issued in Vulkan. Additionally, the wait that waits on this signal must be issued after this signal has been issued.

The following example demonstrates signaling an external semaphore:

```cpp
void signalExternalSemaphore(cudaExternalSemaphore_t extSem, cudaStream_t stream) {
    cudaExternalSemaphoreSignalParams params = {};

    memset(&params, 0, sizeof(params));

    cudaSignalExternalSemaphoresAsync(&extSem, &params, 1, stream);
}
```

## Waiting on an Imported Semaphore

An imported Vulkan semaphore object can be waited on from CUDA. Waiting on such a semaphore object waits until it reaches the signaled state and then resets it back to the unsignaled state. The corresponding signal that this wait is waiting on must be issued in Vulkan. Additionally, the signal must be issued before this wait can be issued.

The following example demonstrates waiting on an external semaphore:

```cpp
void waitExternalSemaphore(cudaExternalSemaphore_t extSem, cudaStream_t stream) {
    cudaExternalSemaphoreWaitParams params = {};

    memset(&params, 0, sizeof(params));

    cudaWaitExternalSemaphoresAsync(&extSem, &params, 1, stream);
}
```

## Ordering Constraints

Proper synchronization requires strict ordering between CUDA and Vulkan operations:

1.  **Signal in CUDA, Wait in Vulkan**: If CUDA signals a Vulkan semaphore, the corresponding wait must be issued in Vulkan after the CUDA signal has been issued.
2.  **Signal in Vulkan, Wait in CUDA**: If CUDA waits on a Vulkan semaphore, the corresponding signal must be issued in Vulkan before the CUDA wait is issued.

These constraints ensure that the synchronization state is correctly managed across the CUDA and Vulkan domains.

[doc_id=CUDA_C_Programming_Guide:L4930-L4956]
