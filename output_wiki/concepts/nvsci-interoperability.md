# NVIDIA Software Communication Interface (NVSCI) Interoperability

Allocates, configures, and imports NvSciBuf memory objects into CUDA, including cache and compression attribute handling.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L5790-L5933

Citation: [CUDA_C_Programming_Guide:L5790-L5933]

````text

## 6.2.16.5 NVIDIA Software Communication Interface Interoperability (NVSCI)

NvSciBuf and NvSciSync are interfaces developed for serving the following purposes:

▶ NvSciBuf: Allows applications to allocate and exchange bufers in memory

NvSciSync: Allows applications to manage synchronization objects at operation boundaries

More details on these interfaces are available at: https://docs.nvidia.com/drive.

## 6.2.16.5.1 Importing Memory Objects

For allocating an NvSciBuf object compatible with a given CUDA device, the corresponding GPU id must be set with NvSciBufGeneralAttrKey\_GpuId in the NvSciBuf attribute list as shown below. Optionally, applications can specify the following attributes -

▶ NvSciBufGeneralAttrKey\_NeedCpuAccess: Specifies if CPU access is required for the bufer

NvSciBufRawBufferAttrKey\_Align: Specifies the alignment requirement of NvSciBufType\_RawBuffer

NvSciBufGeneralAttrKey\_RequiredPerm: Diferent access permissions can be configured for diferent UMDs per NvSciBuf memory object instance. For example, to provide the GPU with read-only access permissions to the bufer, create a duplicate NvSciBuf object using NvSciBufObjDupWithReducePerm() with NvSciBufAccessPerm\_Readonly as the input parameter. Then import this newly created duplicate object with reduced permission into CUDA as shown

▶ NvSciBufGeneralAttrKey\_EnableGpuCache: To control GPU L2 cacheability

▶ NvSciBufGeneralAttrKey\_EnableGpuCompression: To specify GPU compression

Note: For more details on these attributes and their valid input options, refer to NvSciBuf Documentation.

The following code snippet illustrates their sample usage.

```txt
NvSciBufObj createNvSciBufObject() {
    // Raw Buffer Attributes for CUDA
    NvSciBufType bufType = NvSciBufType_RawBuffer;
    uint64_t rawsize = SIZE;
    uint64_t align = 0;
    bool cpuaccess_flag = true;
    NvSciBufAttrValAccessPerm perm = NvSciBufAccessPerm_ReadWrite;

    NvSciRmGpuId gpuid[] = {};
    CUuuid uuid;
    cuDeviceGetUuid(&uuid, dev));

    memcpy(&gpuid[0].bytes, &uuid.bytes, sizeof(uuid.bytes));
    // Disable cache on dev
    NvSciBufAttrValGpuCache gpuCache[] = {{gpuid[0], false}};
    NvSciBufAttrValGpuCompression gpuCompression[] = {{gpuid[0],
NvSciBufCompressionType_GenericCompressible}};
    // Fill in values
    NvSciBufAttrKeyValuePair rawbuffattrs[] = {
        { NvSciBufGeneralAttrKey_Types, &bufType, sizeof(bufType) },
        { NvSciBufRawBufferAttrKey_Size, &rawsize, sizeof(rawsize) },
```

```txt
{ NvSciBufRawBufferAttrKey_Align, &align, sizeof(align) },
{ NvSciBufGeneralAttrKey_NeedCpuAccess, &cpuaccess_flag, sizeof(cpuaccess_flag) },
{ NvSciBufGeneralAttrKey_RequiredPerm, &perm, sizeof(perm) },
{ NvSciBufGeneralAttrKey_GpuId, &gpuid, sizeof(gpuid) },
{ NvSciBufGeneralAttrKey_EnableGpuCache &gpuCache, sizeof(gpuCache) },
{ NvSciBufGeneralAttrKey_EnableGpuCompression &gpuCompression,
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

```c
NvSciBufObj bufferObjRo; // ReadOnly NvSciBuf memory obj
// Create a duplicate handle to the same memory buffer with reduced permissions
NvSciBufObjDupWithReducePerm(bufferObjRaw, NvSciBufAccessPerm_Readonly, &bufferObjRo);
return bufferObjRo;
```

The allocated NvSciBuf memory object can be imported in CUDA using the NvSciBufObj handle as shown below. Application should query the allocated NvSciBufObj for attributes required for filling CUDA External Memory Descriptor. Note that the attribute list and NvSciBuf objects should be maintained by the application. If the NvSciBuf object imported into CUDA is also mapped by other drivers, then based on NvSciBufGeneralAttrKey\_GpuSwNeedCacheCoherency output attribute value the application must use NvSciSync objects (refer to Importing Synchronization Objects) as appropriate barriers to maintain coherence between CUDA and the other drivers.

Note: For more details on how to allocate and maintain NvSciBuf objects refer to NvSciBuf API Documentation.

```c
cudaExternalMemory_t importNvSciBufObject (NvSciBufObj bufferObjRaw) {

    /***************** Query NvSciBuf Object **********/
    NvSciBufAttrKeyValuePair bufattrs[] = {
        { NvSciBufRawBufferAttrKey_Size, NULL, 0 },
        { NvSciBufGeneralAttrKey_GpuSwNeedCacheCoherency, NULL, 0 },
        { NvSciBufGeneralAttrKey_EnableGpuCompression, NULL, 0 }
    };
    NvSciBufAttrListGetAttrs(retList, bufattrs,
        sizeof(bufattrs)/sizeof(NvSciBufAttrKeyValuePair)));
        ret_size = *(static_cast<const uint64_t*>(bufattrs[0].value));

    // Note cache and compression are per GPU attributes, so read values for specific
    gpu by comparing UUID
    // Read cacheability granted by NvSciBuf
```

(continues on next page)

```c
int numGpus = bufattrs[1].len / sizeof(NvSciBufAttrValGpuCache);
NvSciBufAttrValGpuCache[] cacheVal = (NvSciBufAttrValGpuCache *)bufattrs[1].value;
bool ret_cacheVal;
for (int i = 0; i < numGpus; i++) {
    if (memcmp(gpuid[0].bytes, cacheVal[i].gpuId.bytes, sizeof(CUuuid)) == 0) {
        ret_cacheVal = cacheVal[i].cacheability);
    }
}

// Read compression granted by NvSciBuf
numGpus = bufattrs[2].len / sizeof(NvSciBufAttrValGpuCompression);
NvSciBufAttrValGpuCompression[] compVal = (NvSciBufAttrValGpuCompression
*)bufattrs[2].value;
NvSciBufCompressionType ret_compVal;
for (int i = 0; i < numGpus; i++) {
    if (memcmp(gpuid[0].bytes, compVal[i].gpuId.bytes, sizeof(CUuuid)) == 0) {
        ret_compVal = compVal[i].compressionType);
    }
}

/************ NvSciBuf Registration With CUDA ************/

// Fill up CUDA_EXTERNAL_MEMORY_HANDLE_DESC
cudaExternalMemoryHandleDesc memHandleDesc;
memset(&memHandleDesc, 0, sizeof(memHandleDesc));
memHandleDesc.type = cudaExternalMemoryHandleTypeNvSciBuf;
memHandleDesc.handle.nvSciBufObject = bufferObjRaw;
// Set the NvSciBuf object with required access permissions in this step
memHandleDesc.handle.nvSciBufObject = bufferObjRo;
memHandleDesc.size = ret_size;
cudaImportExternalMemory(&extMemBuffer, &memHandleDesc);
return extMemBuffer;
}
```
````
