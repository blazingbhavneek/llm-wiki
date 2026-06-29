# Device-side Tensor Map Encoding

Previous sections have described how to create a tensor map on the host using the CUDA driver API [CUDA_C_Programming_Guide:L10836-L10839]. This section explains how to encode a tiled-type tensor map on device [CUDA_C_Programming_Guide:L10840-L10842]. This is useful in situations where the typical way of transferring the tensor map (using const __grid_constant__ kernel parameters) is undesirable, for instance, when processing a batch of tensors of various sizes in a single kernel launch [CUDA_C_Programming_Guide:L10842-L10847].

## Recommended Pattern

The recommended pattern for device-side encoding involves the following steps [CUDA_C_Programming_Guide:L10848-L10853]:

1. Create a tensor map “template”, `template_tensor_map`, using the Driver API on the host.
2. In a device kernel, copy the `template_tensor_map`, modify the copy, store in global memory, and appropriately fence.
3. Use the tensor map in a kernel with appropriate fencing.

## High-Level Implementation

The high-level code structure for this process is as follows [CUDA_C_Programming_Guide:L10854-L10893]:

```cpp
// Initialize device context:
CUDA_CHECK(cudaDeviceSynchronize());

// Create a tensor map template using the cuTensorMapEncodeTiled driver function
CUtensorMap template_tensor_map = make_tensorsmap_template();

// Allocate tensor map and tensor in global memory
CUtensorMap* global_tensor_map;
CUDA_CHECK(cudaMalloc(&global_tensor_map, sizeof(CUtensorMap)));
char* global_buf;
CUDA_CHECK(cudaMalloc(&global_buf, 8 * 256));

// Fill global buffer with data.
fill_global_buf<<<1, 1>>>(global_buf);

// Define the parameters of the tensor map that will be created on device.
tensormap_params p{
    p.global_address     = global_buf;
    p.rank             = 2;
    p.box_dim[0]       = 128; // The box in shared memory has half the width of the full buffer
    p.box_dim[1]       = 4;   // The box in shared memory has half the height of the full buffer
    p.global_dim[0]      = 256; //
    p.global_dim[1]      = 8;   //
    p.global_stride[0]  = 256; //
    p.element_stride[0] = 1;   //
    p.element_stride[1] = 1;   Production
};

// Encode global_tensor_map on device:
encode_tensor_map<<<1, 32>>>(template_tensor_map, p, global_tensor_map);

// Use it from another kernel:
consume_tensor_map<<<1, 1>>>(global_tensor_map);

// Check for errors:
CUDA_CHECK(cudaDeviceSynchronize());
```

## Parameters Structure

Throughout the examples, the following `tensormap_params` struct contains the new values of the fields to be updated [CUDA_C_Programming_Guide:L10894-L10903]:

```c
struct tensormap_params {
    void* global_address;
    int rank;
    uint32_t box_dim[5];
    uint64_t global_dim[5];
    size_t global_stride[4];
    uint32_t element_stride[5];
};
```
