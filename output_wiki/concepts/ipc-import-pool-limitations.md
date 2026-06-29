# IPC Import Pool Limitations

Import pools, which allow a process to import memory pools from another process, have specific restrictions regarding allocation, trimming, and resource monitoring.

## Allocation Restrictions

Allocating new memory from an import pool is not allowed. Specifically:

*   Import pools cannot be set as the current memory pool for a context.
*   They cannot be used with the `cudaMallocFromPoolAsync` API.

Because new allocations cannot be made from these pools, the allocation reuse policy attributes are meaningless for import pools [CUDA_C_Programming_Guide:L15850-L15857].

## Trimming and Release Limitations

IPC pools currently do not support releasing physical memory blocks back to the operating system. As a result:

*   The `cudaMemPoolTrimTo` API acts as a no-op when called on an import pool.
*   The `cudaMemPoolAttrReleaseThreshold` attribute is effectively ignored [CUDA_C_Programming_Guide:L15850-L15857].

## Resource Usage Statistics

When querying resource usage statistics for an import pool, the values only reflect:

*   The allocations that were imported into the process.
*   The associated physical memory [CUDA_C_Programming_Guide:L15850-L15857].

This means that statistics do not account for memory managed by the source process or any changes made by the source process after the import occurred.
