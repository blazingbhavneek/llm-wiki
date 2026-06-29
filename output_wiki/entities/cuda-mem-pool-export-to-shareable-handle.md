# cudaMemPoolExportToShareableHandle / cudaMemPoolImportFromShareableHandle

Sharing access to a memory pool involves retrieving an OS native handle to the pool (with the `cudaMemPoolExportToShareableHandle()` API), transferring the handle to the importing process using the usual OS native IPC mechanisms, and creating an imported memory pool (with the `cudaMemPoolImportFromShareableHandle()` API). For `cudaMemPoolExportToShareableHandle` to succeed, the memory pool had to be created with the requested handle type specified in the pool properties structure. Please reference samples for the appropriate IPC mechanisms to transfer the OS native handle between processes.

## Prerequisites

To create a pool that can be exported, the `cudaMemPoolProps` structure must be configured with specific attributes:

*   **Allocation Type**: The `allocType` should typically be set to `cudaMemAllocationTypePinned`.
*   **Location**: The `location` must specify the device ID and type (e.g., `cudaMemLocationTypeDevice`).
*   **Handle Types**: The `handleTypes` field must be set to a non-zero value to make the pool exportable (IPC capable). For example, `CU_MEM_HANDLE_TYPE_POSIX_FILE_DESCRIPTOR` can be used for file descriptor-based handles.

## Procedure

### 1. Exporting Process

In the exporting process, a memory pool is created with the appropriate properties, and then the shareable handle is retrieved.

```c
// Create an exportable IPC capable pool on device 0
cudaMemPoolProps poolProps = { };
poolProps.allocType = cudaMemAllocationTypePinned;
poolProps.location.id = 0;
poolProps.location.type = cudaMemLocationTypeDevice;

// Setting handleTypes to a non zero value will make the pool exportable (IPC capable)
poolProps.handleTypes = CU_MEM_HANDLE_TYPE_POSIX_FILE_DESCRIPTOR;

cudaMemPoolCreate(&memPool, &poolProps);

// FD based handles are integer types
int fdHandle = 0;

// Retrieve an OS native handle to the pool.
// Note that a pointer to the handle memory is passed in here.
cudaMemPoolExportToShareableHandle(&fdHandle,
            memPool,
            CU_MEM_HANDLE_TYPE_POSIX_FILE_DESCRIPTOR,
            0);

// The handle must be sent to the importing process with the appropriate
// OS specific APIs.
```

### 2. Importing Process

In the importing process, the handle is retrieved from the exporting process using OS-specific APIs, and then used to create an imported memory pool.

```c
// in importing process
int fdHandle;
// The handle needs to be retrieved from the exporting process with the
// appropriate OS specific APIs.

// Create an imported pool from the shareable handle.
// Note that the handle is passed by value here.
cudaMemPoolImportFromShareableHandle(&importedMemPool,
            (void*)fdHandle,
            CU_MEM_HANDLE_TYPE_POSIX_FILE_DESCRIPTOR,
            0);
```

## References

- CUDA C Programming Guide: Creating and Sharing IPC Memory Pools [CUDA_C_Programming_Guide:L15711-L15755]
