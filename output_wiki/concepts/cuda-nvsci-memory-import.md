# CUDA NVSCI Memory Import

This process involves creating an `NvSciBuf` object compatible with a specific CUDA device, configuring its attributes, and subsequently importing it into the CUDA runtime as an external memory object.

## Allocating NvSciBuf Objects

To allocate an `NvSciBuf` object compatible with a given CUDA device, the corresponding GPU identifier must be set using `NvSciBufGeneralAttrKey_GpuId` in the attribute list [CUDA_C_Programming_Guide:L5803-L5803]. Applications can optionally specify several other attributes to control memory behavior, including CPU access requirements, alignment, access permissions, GPU cache settings, and compression [CUDA_C_Programming_Guide:L5803-L5803].

### Setting Attributes

The following attributes are typically configured during the creation of a raw buffer object for CUDA:

*   **Type**: `NvSciBufType_RawBuffer` [CUDA_C_Programming_Guide:L5819-L5872].
*   **Size and Alignment**: Defined via `NvSciBufRawBufferAttrKey_Size` and `NvSciBufRawBufferAttrKey_Align` [CUDA_C_Programming_Guide:L5819-L5872].
*   **CPU Access**: Controlled by `NvSciBufGeneralAttrKey_NeedCpuAccess` [CUDA_C_Programming_Guide:L5819-L5872].
*   **Access Permissions**: Set via `NvSciBufGeneralAttrKey_RequiredPerm` (e.g., `NvSciBufAccessPerm_ReadWrite`) [CUDA_C_Programming_Guide:L5819-L5872].
*   **GPU Identifier**: Set via `NvSciBufGeneralAttrKey_GpuId` using the device's UUID [CUDA_C_Programming_Guide:L5819-L5872].
*   **GPU Cache**: Controlled by `NvSciBufGeneralAttrKey_EnableGpuCache` [CUDA_C_Programming_Guide:L5819-L5872].
*   **GPU Compression**: Controlled by `NvSciBufGeneralAttrKey_EnableGpuCompression` [CUDA_C_Programming_Guide:L5819-L5872].

### Example Allocation Code

The following example demonstrates how to create an `NvSciBuf` object with these attributes:

```c
NvSciBufObj createNvSciBufObject() {
    // Raw Buffer Attributes for CUDA
    NvSciBufType bufType = NvSciBufType_RawBuffer;
    uint64_t rawsize = SIZE;
    uint64_t align = 0;
    bool cpuaccess_flag = true;
    NvSciBufAttrValAccessPerm perm = NvSciBufAccessPerm_ReadWrite;

    NvSciRmGpuId gpuid[] = {};
    CUuuid uuid;
    cuDeviceGetUuid(&uuid, dev);

    memcpy(&gpuid[0].bytes, &uuid.bytes, sizeof(uuid.bytes));
    // Disable cache on dev
    NvSciBufAttrValGpuCache gpuCache[] = {{gpuid[0], false}};
    NvSciBufAttrValGpuCompression gpuCompression[] = {{gpuid[0],
    NvSciBufCompressionType_GenericCompressible}};
    // Fill in values
    NvSciBufAttrKeyValuePair rawbuffattrs[] = {
        { NvSciBufGeneralAttrKey_Types, &bufType, sizeof(bufType) },
        { NvSciBufRawBufferAttrKey_Size, &rawsize, sizeof(rawsize) },
        { NvSciBufRawBufferAttrKey_Align, &align, sizeof(align) },
        { NvSciBufGeneralAttrKey_NeedCpuAccess, &cpuaccess_flag, sizeof(cpuaccess_flag) },
        { NvSciBufGeneralAttrKey_RequiredPerm, &perm, sizeof(perm) },
        { NvSciBufGeneralAttrKey_GpuId, &gpuid, sizeof(gpuid) },
        { NvSciBufGeneralAttrKey_EnableGpuCache, &gpuCache, sizeof(gpuCache) },
        { NvSciBufGeneralAttrKey_EnableGpuCompression, &gpuCompression,
        sizeof(gpuCompression) }
    };

    // Create list by setting attributes
    err = NvSciBufAttrListSetAttrs(attrListBuffer, rawbuffattrs,
        sizeof(rawbuffattrs)/sizeof(NvSciBufAttrKeyValuePair));

    NvSciBufAttrListCreate(NvSciBufModule, &attrListBuffer);

    // Reconcile And Allocate
    NvSciBufAttrListReconcile(&attrListBuffer, 1, &attrListReconciledBuffer,
            &attrListConflictBuffer)
    NvSciBufObjAlloc(attrListReconciledBuffer, &bufferObjRaw);
    return bufferObjRaw;
}
```

It is also possible to create a duplicate handle to the same memory buffer with reduced permissions, such as read-only access, using `NvSciBufObjDupWithReducePerm` [CUDA_C_Programming_Guide:L5819-L5872].

## Importing into CUDA

Once the `NvSciBuf` object is created, it can be imported into CUDA as an external memory object. This involves querying the object's attributes and then registering it with the CUDA external memory API.

### Querying Attributes

Before importing, the application should query the `NvSciBuf` object for relevant attributes, such as size, software cache coherency requirements, and compression status [CUDA_C_Programming_Guide:L5878-L5931].

```c
NvSciBufAttrKeyValuePair bufattrs[] = {
    { NvSciBufRawBufferAttrKey_Size, NULL, 0 },
    { NvSciBufGeneralAttrKey_GpuSwNeedCacheCoherency, NULL, 0 },
    { NvSciBufGeneralAttrKey_EnableGpuCompression, NULL, 0 }
};
NvSciBufAttrListGetAttrs(retList, bufattrs,
    sizeof(bufattrs)/sizeof(NvSciBufAttrKeyValuePair)));
    ret_size = *(static_cast<const uint64_t*>(bufattrs[0].value));
```

Since cache and compression settings are per-GPU attributes, the application must read the values for the specific GPU by comparing UUIDs [CUDA_C_Programming_Guide:L5878-L5931].

### Registration with CUDA

The `NvSciBuf` object is registered with CUDA by filling a `cudaExternalMemoryHandleDesc` structure and calling `cudaImportExternalMemory` [CUDA_C_Programming_Guide:L5878-L5931].

```c
// Fill up CUDA_EXTERNAL_MEMORY_HANDLE_DESC
cudaExternalMemoryHandleDesc memHandleDesc;
memset(&memHandleDesc, 0, sizeof(memHandleDesc));
memHandleDesc.type = cudaExternalMemoryHandleTypeNvSciBuf;
memHandleDesc.handle.nvSciBufObject = bufferObjRaw;
// Set the NvSciBuf object with required access permissions in this step
memHandleDesc.handle.nvSciBufObject = bufferObjRo;
memHandleDesc.size = ret_size;
cudaImportExternalMemory(&extMemBuffer, &memHandleDesc);
```

Note that the `nvSciBufObject` handle in the descriptor can be set to a specific object instance (e.g., `bufferObjRo`) that has the required access permissions for the CUDA context [CUDA_C_Programming_Guide:L5878-L5931].
