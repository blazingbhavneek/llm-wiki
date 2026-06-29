# cudaMemPoolExportPointer / cudaMemPoolImportPointer

`cudaMemPoolExportPointer` and `cudaMemPoolImportPointer` are CUDA API functions used to share memory allocations made from a memory pool across different processes. This mechanism allows an exporting process to share allocations created with `cudaMallocAsync()` with one or more importing processes that have imported the same memory pool.

## Overview

Once a memory pool has been shared, allocations made from it in the exporting process can be accessed by importing processes. The security policy for these allocations is established and verified at the pool level, meaning the operating system does not require extra bookkeeping for individual allocations [CUDA_C_Programming_Guide:L15762-L15846].

To share a specific allocation, the exporting process calls `cudaMemPoolExportPointer` to generate an opaque `cudaMemPoolPtrExportData` structure. This data can be transmitted to the importing process using any inter-process communication (IPC) mechanism, such as shared memory, sockets, or message queues [CUDA_C_Programming_Guide:L15762-L15846]. The importing process then uses `cudaMemPoolImportPointer` to associate the allocation with its local memory pool [CUDA_C_Programming_Guide:L15762-L15846].

## Stream Ordering and Synchronization

While the export and import operations themselves do not require synchronization with the allocating stream, strict adherence to stream ordering is required when accessing the shared allocation [CUDA_C_Programming_Guide:L15762-L15846].

### Access Rules

The importing process must follow the same synchronization rules as the exporting process. Specifically, access to the allocation in the importing process must occur after the stream ordering of the allocation operation in the allocating stream [CUDA_C_Programming_Guide:L15762-L15846].

To guarantee that the allocation is ready before use, CUDA IPC events are commonly employed. The typical workflow involves:
1.  Creating an IPC event with the `cudaEventInterprocess` flag [CUDA_C_Programming_Guide:L15762-L15846].
2.  Recording the event on the stream after the `cudaMallocAsync` call [CUDA_C_Programming_Guide:L15762-L15846].
3.  Exporting the pointer and the IPC event handle to the importing process [CUDA_C_Programming_Guide:L15762-L15846].
4.  In the importing process, opening the IPC event handle and waiting on it via `cudaStreamWaitEvent` before accessing the memory [CUDA_C_Programming_Guide:L15762-L15846].

### Deallocation Rules

When freeing the allocation, the order of operations is critical. The allocation must be freed in the importing process **before** it is freed in the exporting process [CUDA_C_Programming_Guide:L15762-L15846].

This is typically managed by:
1.  Performing the last access in the importing process.
2.  Calling `cudaFreeAsync` (or `cudaFree`) in the importing process [CUDA_C_Programming_Guide:L15762-L15846].
3.  Recording an IPC event in the importing process after the free operation completes [CUDA_C_Programming_Guide:L15762-L15846].
4.  In the exporting process, waiting on this IPC event before performing its own `cudaFreeAsync` or `cudaFree` [CUDA_C_Programming_Guide:L15762-L15846].

Note that `cudaFree` can be used instead of `cudaFreeAsync` in both processes, and other stream synchronization APIs may be used in place of IPC events if appropriate for the application's synchronization model [CUDA_C_Programming_Guide:L15762-L15846].

## Example Workflow

### Exporting Process

```c
// preparing an allocation in the exporting process
cudaMemPoolPtrExportData exportData;
cudaEvent_t readyIpcEvent;
cudaIpcEventHandle_t readyIpcEventHandle;

// ipc event for coordinating between processes
// cudaEventInterprocess flag makes the event an ipc event
// cudaEventDisableTiming is set for performance reasons
cudaEventCreate(
    &readyIpcEvent, cudaEventDisableTiming | cudaEventInterprocess);

// allocate from the exporting mem pool
cudaMallocAsync(&ptr, size, exportMemPool, stream);

// event for sharing when the allocation is ready.
cudaEventRecord(readyIpcEvent, stream);
cudaMemPoolExportPointer(&exportData, ptr);
cudaIpcGetEventHandle(&readyIpcEventHandle, readyIpcEvent);

// Share IPC event and pointer export data with the importing process using
// any mechanism. Here we copy the data into shared memory
shmem->ptrData = exportData;
shmem->readyIpcEventHandle = readyIpcEventHandle;
// signal consumers data is ready
```

### Importing Process

```c
// Importing an allocation
cudaMemPoolPtrExportData *importData = &shmem->ptrData;
cudaEvent_t readyIpcEvent;
cudaIpcEventHandle_t *readyIpcEventHandle = &shmem->readyIpcEventHandle;

// Need to retrieve the ipc event handle and the export data from the
// exporting process using any mechanism. Here we are using shmem and just
// need synchronization to make sure the shared memory is filled in.

cudaIpcOpenEventHandle(&readyIpcEvent, readyIpcEventHandle);

// import the allocation. The operation does not block on the allocation being ready.
cudaMemPoolImportPointer(&ptr, importedMemPool, importData);

// Wait for the prior stream operations in the allocating stream to complete before
// using the allocation in the importing process.
cudaStreamWaitEvent(stream, readyIpcEvent);
kernel<<<..., stream>>>(ptr, ...);
```

### Freeing the Allocation

```c
// The free must happen in importing process before the exporting process
kernel<<<..., stream>>>(ptr, ...);

// Last access in importing process
cudaFreeAsync(ptr, stream);

// Access not allowed in the importing process after the free
cudaIpcEventRecord(finishedIpcEvent, stream);

// Exporting process
// The exporting process needs to coordinate its free with the stream order
// of the importing process's free.
cudaStreamWaitEvent(stream, finishedIpcEvent);
kernel<<<..., stream>>>(ptrInExportingProcess, ...);

// The free in the importing process doesn't stop the exporting process
// from using the allocation.
cudaFreeAsync(ptrInExportingProcess, stream);
```

## References
- [CUDA_C_Programming_Guide:L15762-L15846]
