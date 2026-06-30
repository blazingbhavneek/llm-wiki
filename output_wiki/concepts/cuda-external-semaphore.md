# Importing and Signaling/Waiting on Imported Synchronization Objects

Covers importing NvSciSync objects into CUDA as external semaphores using `cudaImportExternalSemaphore`, and signaling/waiting on them using `cudaSignalExternalSemaphoresAsync` and `cudaWaitExternalSemaphoresAsync`. Details attribute reconciliation, fence parameters, and the `cudaExternalSemaphoreSignalSkipNvSciBufMemSync`/`cudaExternalSemaphoreWaitSkipNvSciBufMemSync` flags for cache coherency control.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L5984-L6072

Citation: [CUDA_C_Programming_Guide:L5984-L6072]

````text
## 6.2.16.5.4 Importing Synchronization Objects

NvSciSync attributes that are compatible with a given CUDA device can be generated using cudaDeviceGetNvSciSyncAttributes(). The returned attribute list can be used to create a NvSciSyncObj that is guaranteed compatibility with a given CUDA device.

```c
NvSciSyncObj createNvSciSyncObject() {
    NvSciSyncObj nvSciSyncObj
    int cudaDev0 = 0;
    int cudaDev1 = 1;
    NvSciSyncAttrList signalerAttrList = NULL;
    NvSciSyncAttrList waiterAttrList = NULL;
    NvSciSyncAttrList reconciledList = NULL;
    NvSciSyncAttrList newConflictList = NULL;

    NvSciSyncAttrListCreate(module, &signalerAttrList);
    NvSciSyncAttrListCreate(module, &waiterAttrList);
    NvSciSyncAttrList unreconciledList[2] = {NULL, NULL};
    unreconciledList[0] = signalerAttrList;
    unreconciledList[1] = waiterAttrList;

    cudaDeviceGetNvSciSyncAttributes(signalerAttrList, cudaDev0, CUDA_NVSCISYNC_ATTR_SIGNAL);
```

```txt
(continued from previous page)
    cudaDeviceGetNvSciSyncAttributes(waiterAttrList, cudaDev1, CUDA_NVSCISYNC_ATTR_WAIT);

    NvSciSyncAttrListReconcile(unreconciledList, 2, &reconciledList, &newConflictList);

    NvSciSyncObjAlloc(reconciledList, &nvSciSyncObj);

    return nvSciSyncObj;
}
```

An NvSciSync object (created as above) can be imported into CUDA using the NvSciSyncObj handle as shown below. Note that ownership of the NvSciSyncObj handle continues to lie with the application even after it is imported.

```txt
cudaExternalSemaphore_t importNvSciSyncObject(void* nvSciSyncObj) {
    cudaExternalSemaphore_t extSem = NULL;
    cudaExternalSemaphoreHandleDesc desc = {}

    memset(&desc, 0, sizeof(desc));

    desc.type = cudaExternalSemaphoreHandleTypeNvSciSync;
    desc.handle.nvSciSyncObj = nvSciSyncObj;

    cudaImportExternalSemaphore(&extSem, &desc);

    // Deleting/Freeing the nvSciSyncObj beyond this point will lead to undefined behavior in CUDA

    return extSem;
}
```

## 6.2.16.5.5 Signaling/Waiting on Imported Synchronization Objects

An imported NvSciSyncObj object can be signaled as outlined below. Signaling NvSciSync backed semaphore object initializes the fence parameter passed as input. This fence parameter is waited upon by a wait operation that corresponds to the aforementioned signal. Additionally, the wait that waits on this signal must be issued after this signal has been issued. If the flags are set to cudaExternalSemaphoreSignalSkipNvSciBufMemSync then memory synchronization operations (over all the imported NvSciBuf in this process) that are executed as a part of the signal operation by default are skipped. When NvsciBufGeneralAttrKey\_GpuSwNeedCacheCoherency is FALSE, this flag should be set.

```javascript
void signalExternalSemaphore(cudaExternalSemaphore_t extSem, cudaStream_t stream,
    void *fence) {
    cudaExternalSemaphoreSignalParams signalParams = {}

    memset(&signalParams, 0, sizeof(signalParams));

    signalParams.params.nvSciSync.fence = (void*)fence;
    signalParams.flags = 0; //OR cudaExternalSemaphoreSignalSkipNvSciBufMemSync

    cudaSignalExternalSemaphoresAsync(&extSem, &signalParams, 1, stream);
```

(continued from previous page)

An imported NvSciSyncObj object can be waited upon as outlined below. Waiting on NvSciSync backed semaphore object waits until the input fence parameter is signaled by the corresponding signaler. Additionally, the signal must be issued before the wait can be issued. If the flags are set to cudaExternalSemaphoreWaitSkipNvSciBufMemSync then memory synchronization operations (over all the imported NvSciBuf in this process) that are executed as a part of the signal operation by default are skipped. When NvsciBufGeneralAttrKey\_GpuSwNeedCacheCoherency is FALSE, this flag should be set.

```javascript
void waitExternalSemaphore(cudaExternalSemaphore_t extSem, cudaStream_t stream, void
    *fence) {
    cudaExternalSemaphoreWaitParams waitParams = {}

    memset(&waitParams, 0, sizeof(waitParams));

    waitParams.params.nvSciSync.fence = (void*)fence;
    waitParams.flags = 0; //OR cudaExternalSemaphoreWaitSkipNvSciBufMemSync

    cudaWaitExternalSemaphoresAsync(&extSem, &waitParams, 1, stream);
}
```
````
