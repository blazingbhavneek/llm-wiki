# cudaGraphAddMemAllocNode

The `cudaGraphAddMemAllocNode` API is used to add a memory allocation node to a CUDA graph. This function allows applications to specify the resident device for the allocation and define access permissions for other devices through an array of access descriptors.

## Parameters and Configuration

The function takes a `cudaMemAllocNodeParams` structure that configures the allocation. Key components include:

*   **`poolProps.location`**: An embedded structure that specifies the resident device for the allocation [CUDA_C_Programming_Guide:L16254-L16293].
*   **`accessDescs`**: An array of access descriptors that defines mapping requests and access permissions [CUDA_C_Programming_Guide:L16254-L16293].
*   **`accessDescCount`**: The number of entries in the `accessDescs` array [CUDA_C_Programming_Guide:L16254-L16293].

## Access Permissions and Resident Device

When configuring the node, the application must understand the implicit access rules regarding the resident device:

1.  **Resident Device Access**: Access from the allocating GPU (the resident device) is assumed to be needed. Therefore, the application does not need to specify an entry for the resident device in the `accessDescs` array [CUDA_C_Programming_Guide:L16254-L16293].
2.  **Explicit Access**: The `accessDescs` array should only contain entries for devices other than the resident device that require access [CUDA_C_Programming_Guide:L16254-L16293].

### Supported Access Types

Only `ReadWrite` and `Device` access flags are supported by the add node API [CUDA_C_Programming_Guide:L16254-L16293].

## Example Usage

The following example demonstrates how to allocate memory resident on device 1, accessible from devices 0, 1, and 2.

```javascript
cudaMemAllocNodeParams params = {};
params.poolProps.allocType = cudaMemAllocationTypePinned;
params.poolProps.location.type = cudaMemLocationTypeDevice;
// Specify device 1 as the resident device
params.poolProps.location.id = 1;
params.bytesize = size;

// Configure access descriptors for devices 0 and 2
accessDescs[0].flags = cudaMemAccessFlagsProtReadWrite;
accessDescs[0].location.type = cudaMemLocationTypeDevice;
accessDescs[0].location.id = 0;

accessDescs[1].flags = cudaMemAccessFlagsProtReadWrite;
accessDescs[1].location.type = cudaMemLocationTypeDevice;
accessDescs[1].location.id = 2;

// Set the count of access descriptors (device 1 is implicit)
params.accessDescCount = 2;
params.accessDescs = accessDescs;

// Allocate memory resident on device 1, accessible from devices 0, 1, and 2
cudaGraphAddMemAllocNode(&allocNode, graph, NULL, 0, &params);
```

In this example, device 1 is the resident device, so its access is implicit. Devices 0 and 2 are explicitly granted `ReadWrite` access via the `accessDescs` array [CUDA_C_Programming_Guide:L16254-L16293].
