# Signaling and Waiting on Imported Synchronization Objects

This page describes the mechanism for signaling and waiting on imported NvSciSyncObj objects using CUDA external semaphores. These operations allow synchronization between CUDA streams and external synchronization objects backed by NvSciSync.

## Signaling Imported Semaphores

An imported NvSciSyncObj object can be signaled using `cudaSignalExternalSemaphoresAsync`. The signaling operation initializes the fence parameter passed as input. This fence parameter is then waited upon by a corresponding wait operation.

### Requirements
- The wait operation that waits on this signal must be issued **after** the signal has been issued [CUDA_C_Programming_Guide:L6039-L6072].

### Parameters and Flags
The signal operation is configured via a `cudaExternalSemaphoreSignalParams` structure. Key aspects include:
- **Fence**: The `fence` field within `params.nvSciSync` is set to the pointer of the imported fence object [CUDA_C_Programming_Guide:L6039-L6072].
- **Flags**: By default, memory synchronization operations over all imported NvSciBuf objects in the process are executed as part of the signal operation. The flag `cudaExternalSemaphoreSignalSkipNvSciBufMemSync` can be used to skip these memory synchronization operations [CUDA_C_Programming_Guide:L6039-L6072].
  - This flag should be set when `NvsciBufGeneralAttrKey_GpuSwNeedCacheCoherency` is FALSE [CUDA_C_Programming_Guide:L6039-L6072].

### Example
```c
void signalExternalSemaphore(cudaExternalSemaphore_t extSem, cudaStream_t stream,
    void *fence) {
    cudaExternalSemaphoreSignalParams signalParams = {};

    memset(&signalParams, 0, sizeof(signalParams));

    signalParams.params.nvSciSync.fence = (void*)fence;
    signalParams.flags = 0; // OR cudaExternalSemaphoreSignalSkipNvSciBufMemSync

    cudaSignalExternalSemaphoresAsync(&extSem, &signalParams, 1, stream);
}
```

## Waiting on Imported Semaphores

An imported NvSciSyncObj object can be waited upon using `cudaWaitExternalSemaphoresAsync`. The wait operation blocks until the input fence parameter is signaled by the corresponding signaler.

### Requirements
- The signal must be issued **before** the wait can be issued [CUDA_C_Programming_Guide:L6039-L6072].

### Parameters and Flags
The wait operation is configured via a `cudaExternalSemaphoreWaitParams` structure. Key aspects include:
- **Fence**: The `fence` field within `params.nvSciSync` is set to the pointer of the imported fence object [CUDA_C_Programming_Guide:L6039-L6072].
- **Flags**: Similar to signaling, the flag `cudaExternalSemaphoreWaitSkipNvSciBufMemSync` can be used to skip memory synchronization operations over all imported NvSciBuf objects in the process [CUDA_C_Programming_Guide:L6039-L6072].
  - This flag should be set when `NvsciBufGeneralAttrKey_GpuSwNeedCacheCoherency` is FALSE [CUDA_C_Programming_Guide:L6039-L6072].

### Example
```c
void waitExternalSemaphore(cudaExternalSemaphore_t extSem, cudaStream_t stream, void
    *fence) {
    cudaExternalSemaphoreWaitParams waitParams = {};

    memset(&waitParams, 0, sizeof(waitParams));

    waitParams.params.nvSciSync.fence = (void*)fence;
    waitParams.flags = 0; // OR cudaExternalSemaphoreWaitSkipNvSciBufMemSync

    cudaWaitExternalSemaphoresAsync(&extSem, &waitParams, 1, stream);
}
```

## Related Functions
- `cudaSignalExternalSemaphoresAsync`
- `cudaWaitExternalSemaphoresAsync`
- `cudaExternalSemaphoreSignalSkipNvSciBufMemSync`
- `cudaExternalSemaphoreWaitSkipNvSciBufMemSync`
