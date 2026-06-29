# 6.2.16.4 Direct3D 11 Interoperability

Part of [Cuda C Programming Guide Reference](README.md). Source lines L5337-L5933.

- [CUDA Direct3D 11 Device LUID Matching](../../../concepts/cuda-d3d11-device-luid-matching.md) — Explains that CUDA and Direct3D 11 devices must match via LUID comparison to import memory/synchronization objects. Provides code to query IDXGIDevice, IDXGIAdapter, and CUDA device properties to find the matching CUDA device.
- [CUDA Direct3D 11 Memory Import](../../../concepts/cuda-d3d11-memory-import.md) — This page details the creation of shareable Direct3D 11 resources and their subsequent import into CUDA using `cudaImportExternalMemory` with dedicated memory flags.
- [CUDA Direct3D 11 Buffer Mapping](../../../concepts/cuda-d3d11-buffer-mapping.md) — This page explains how to map a device pointer onto an imported Direct3D 11 memory object using cudaExternalMemoryGetMappedBuffer, ensuring offset and size constraints are met and resources are properly freed.
- [CUDA Direct3D 11 Mipmapped Array Mapping](../../../concepts/cuda-d3d11-mipmapped-array-mapping.md) — This page details the process of mapping CUDA mipmapped arrays onto imported Direct3D 11 memory objects, including parameter conversion and resource flag handling.
- [CUDA Direct3D 11 Synchronization Object Import](../../../concepts/cuda-d3d11-sync-import.md) — This page describes how to import shareable Direct3D 11 fence and keyed mutex synchronization objects into CUDA using NT handles, named handles, or KMT handles via the CUDA External Memory/Semaphore API.
- [CUDA Direct3D 11 Synchronization Signaling and Waiting](../../../concepts/cuda-d3d11-sync-signaling-waiting.md) — This page details the mechanisms for signaling and waiting on imported Direct3D 11 fence and keyed mutex objects using CUDA external semaphores, including API usage and ordering constraints.
- [CUDA NVSCI Interoperability](../../../concepts/cuda-nvsci-interoperability.md) — Introduces NvSciBuf and NvSciSync interfaces for buffer allocation/exchange and synchronization management in CUDA interoperability.
- [CUDA NVSCI Memory Import](../../../concepts/cuda-nvsci-memory-import.md) — This page describes the process of allocating NvSciBuf objects with specific CUDA-compatible attributes and importing them into CUDA as external memory.
