# Importing NvSciSync Objects

NvSciSync attributes that are compatible with a given CUDA device can be generated using `cudaDeviceGetNvSciSyncAttributes()`. The returned attribute list can be used to create a `NvSciSyncObj` that is guaranteed compatibility with a given CUDA device.

## Creating Compatible Attributes

To create a synchronization object, attribute lists must be generated for both the signaler and waiter sides, reconciled, and then used to allocate the object. Ownership of the `NvSciSyncObj` handle continues to lie with the application even after it is imported.

### 1. Generate Attributes

Generate the attribute lists for the specific CUDA devices and roles (signal or wait). For example, to create attributes for device 0 as a signaler and device 1 as a waiter:

```c
NvSciSyncAttrList signalerAttrList = NULL;
NvSciSyncAttrList waiterAttrList = NULL;

NvSciSyncAttrListCreate(module, &signalerAttrList);
NvSciSyncAttrListCreate(module, &waiterAttrList);

cudaDeviceGetNvSciSyncAttributes(signalerAttrList, cudaDev0, CUDA_NVSCISYNC_ATTR_SIGNAL);
cudaDeviceGetNvSciSyncAttributes(waiterAttrList, cudaDev1, CUDA_NVSCISYNC_ATTR_WAIT);
```

### 2. Reconcile Attributes

The unreconciled attribute lists must be reconciled to ensure they are compatible with each other. This step produces a reconciled list and potentially a conflict list if incompatibilities are found.

```c
NvSciSyncAttrList unreconciledList[2] = {NULL, NULL};
unreconciledList[0] = signalerAttrList;
unreconciledList[1] = waiterAttrList;

NvSciSyncAttrList reconciledList = NULL;
NvSciSyncAttrList newConflictList = NULL;

NvSciSyncAttrListReconcile(unreconciledList, 2, &reconciledList, &newConflictList);
```

### 3. Allocate the Object

Use the reconciled attribute list to allocate the `NvSciSyncObj`.

```c
NvSciSyncObj nvSciSyncObj;
NvSciSyncObjAlloc(reconciledList, &nvSciSyncObj);
```

## Importing into CUDA

An `NvSciSync` object can be imported into CUDA using the `NvSciSyncObj` handle. This is done by configuring a `cudaExternalSemaphoreHandleDesc` structure and calling `cudaImportExternalSemaphore`.

```c
cudaExternalSemaphore_t importNvSciSyncObject(void* nvSciSyncObj) {
    cudaExternalSemaphore_t extSem = NULL;
    cudaExternalSemaphoreHandleDesc desc = {};

    memset(&desc, 0, sizeof(desc));

    desc.type = cudaExternalSemaphoreHandleTypeNvSciSync;
    desc.handle.nvSciSyncObj = nvSciSyncObj;

    cudaImportExternalSemaphore(&extSem, &desc);

    return extSem;
}
```

### Important Note on Ownership and Lifecycle

After importing the `NvSciSyncObj` into CUDA, the application must not delete or free the `nvSciSyncObj` handle. Doing so will lead to undefined behavior in CUDA, as the CUDA runtime may still be using the underlying object. The application retains ownership of the handle, but its lifecycle is tied to the CUDA external semaphore's usage.

## References

- [CUDA_C_Programming_Guide:L5984-L6037]
