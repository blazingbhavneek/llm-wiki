# Explicit Memory Pools

Explicit memory pools provide a mechanism for applications to request specific properties for memory allocations that go beyond the capabilities of the default or implicit pools. These pools are created using the `cudaMemPoolCreate` API, which accepts a structure defining the desired allocation characteristics [CUDA_C_Programming_Guide:L15499-L15528].

## Key Properties

Applications can configure several properties when creating an explicit pool, including:

*   **IPC Capability**: Enabling Inter-Process Communication sharing, potentially via POSIX file descriptor handles [CUDA_C_Programming_Guide:L15499-L15528].
*   **Maximum Pool Size**: Defining limits on the pool's capacity [CUDA_C_Programming_Guide:L15499-L15528].
*   **NUMA Node Residency**: Ensuring allocations reside on specific CPU NUMA nodes on supported platforms [CUDA_C_Programming_Guide:L15499-L15528].

## Usage Examples

### Device Memory Pool

The following example demonstrates creating a pool similar to the implicit pool on a specific device (device 0). The pool is configured for pinned memory allocation on the device [CUDA_C_Programming_Guide:L15499-L15528]:

```javascript
// create a pool similar to the implicit pool on device 0
int device = 0;
cudaMemPoolProps poolProps = { };
poolProps.allocType = cudaMemAllocationTypePinned;
poolProps.location.id = device;
poolProps.location.type = cudaMemLocationTypeDevice;

cudaMemPoolCreate(&memPool, &poolProps));
```

### IPC-Capable Host Pool

The following example illustrates creating an IPC-capable memory pool resident on a CPU NUMA node. This configuration uses a POSIX file descriptor handle to enable sharing [CUDA_C_Programming_Guide:L15499-L15528]:

```txt
// create a pool resident on a CPU NUMA node that is capable of IPC sharing (via a file
    descriptor).
int cpu_numa_id = 0;
cudaMemPoolProps poolProps = { };
poolProps.allocType = cudaMemcpyAllocationTypePinned;
poolProps.location.id = cpu_numa_id;
poolProps.location.type = cudaMemcpyLocationTypeHostNuma;
poolProps.handleType = cudaMemcpyHandleTypePosixFileDescriptor;

cudaMemPoolCreate(&ipcMemPool, &poolProps));
```
