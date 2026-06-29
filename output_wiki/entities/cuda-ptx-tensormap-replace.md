# cuda::ptx::tensormap_replace Functions

The `cuda::ptx::tensormap_replace` family of functions provides device-side mechanisms to modify the fields of a tiled-type tensor map. These functions wrap the `tensormap.replace` PTX instruction, enabling the modification of attributes such as the base address, size, stride, element type, and various layout parameters [CUDA_C_Programming_Guide:L10905-L10997].

## Overview and Usage

On-device modification is exclusively supported for **tiled-type tensor maps**; other tensor map types cannot be modified on device [CUDA_C_Programming_Guide:L10905-L10997]. The recommended process for encoding and modifying a tensor map in global memory involves the following steps [CUDA_C_Programming_Guide:L10905-L10997]:

1.  **Pass the Template**: Pass an existing tensor map, referred to as `template_tensor_map`, to the kernel. This can be done via a pointer to global memory, a kernel parameter, or a `__const__` variable [CUDA_C_Programming_Guide:L10905-L10997].
2.  **Copy to Shared Memory**: Copy-initialize a tensor map in shared memory with the value of the `template_tensor_map` [CUDA_C_Programming_Guide:L10905-L10997].
3.  **Modify Fields**: Use the `cuda::ptx::tensormap_replace` functions to modify the desired fields in the shared memory copy [CUDA_C_Programming_Guide:L10905-L10997].
4.  **Fence and Copy Back**: Use the `cuda::ptx::tensormap_copy_fenceproxy` function to copy the modified tensor map from shared memory to global memory and perform necessary fencing to make it visible to other threads [CUDA_C_Programming_Guide:L10905-L10997].

### Architecture Specifics

The `cuda::ptx::tensormap_replace` functions and the corresponding `tensormap.replace.tile` PTX instructions are specific to **sm_90a** [CUDA_C_Programming_Guide:L10905-L10997]. To use them, the code must be compiled using `nvcc -arch sm_90a` [CUDA_C_Programming_Guide:L10905-L10997].

On sm_90a, a zero-initialized buffer in shared memory may also be used as the initial tensor map value, which enables encoding a tensor map purely on device without using the driver API to encode the template value [CUDA_C_Programming_Guide:L10905-L10997].

## Available Functions

The following functions allow modification of specific fields within the tensor map structure [CUDA_C_Programming_Guide:L10905-L10997]:

*   **Address**: `tensormap_replace_global_address`
*   **Rank**: `tensormap_replace_rank`
*   **Box Dimensions**: `tensormap_replace_box_dim`
*   **Global Dimensions**: `tensormap_replace_global_dim`
*   **Global Stride**: `tensormap_replace_global_stride`
*   **Element Stride**: `tensormap_replace_element_size`
*   **Element Type**: `tensormap_replace_elemtype`
*   **Interleave Layout**: `tensormap_replace_interleave_layout`
*   **Swizzle Mode**: `tensormap_replace_swizzle_mode`
*   **Fill Mode**: `tensormap_replace_fill_mode`

## Implementation Details

### Rank Field
When modifying the `.rank` field using `tensormap_replace_rank`, the operand `new_val` must be **one less than the desired tensor rank**. This is because the field uses zero-based numbering [CUDA_C_Programming_Guide:L10905-L10997].

### Synchronization
Modifications to the tensor map in shared memory should be synchronized across the warp using `__syncwarp()` before copying the map to global memory [CUDA_C_Programming_Guide:L10905-L10997].

### Fenceproxy
The `tensormap_cp_fenceproxy` function is used to synchronize modifications with other threads in the warp and to make the updated tensor map visible to other threads on the device, particularly for use with `cp.async.bulk` instructions [CUDA_C_Programming_Guide:L10905-L10997].

## Example

The following C++ code demonstrates a kernel that follows the recommended process, modifying all fields of a tensor map [CUDA_C_Programming_Guide:L10905-L10997]:

```cpp
#include <cuda/ptx>

namespace ptx = cuda::ptx;

// launch with 1 warp.
__launch_bounds__(32)
__global__ void encode_tensor_map(const __grid_constant__ CUtensorMap template_tensor_map, tensormap_params p, CUtensorMap* out) {
    __shared__ alignas(128) CUtensorMap smem_tmap;
    if (threadIdx.x == 0) {
        // Copy template to shared memory:
        smem_tmap = template_tensor_map;

        const auto space_shared = ptx::space_shared;
        ptx::tensormap_replace_global_address(space_shared, &smem_tmap, p.global_address);
        // For field .rank, the operand new_val must be ones less than the desired
        // tensor rank as this field uses zero-based numbering.
        ptx::tensormap_replace_rank(space_shared, &smem_tmap, p.rank - 1);

        // Set box dimensions:
        if (0 < p.rank) { ptx::tensormap_replace_box_dim(space_shared, &smem_tmap, ptx::n32_t<0>{}, p.box_dim[0]); }
        if (1 < p.rank) { ptx::tensormap_replace_box_dim(space_shared, &smem_tmap, ptx::n32_t<1>{}, p.box_dim[1]); }
        if (2 < p.rank) { ptx::tensormap_replace_box_dim(space_shared, &smem_tmap, ptx::n32_t<2>{}, p.box_dim[2]); }
        if (3 < p.rank) { ptx::tensormap_replace_box_dim(space_shared, &smem_tmap, ptx::n32_t<3>{}, p.box_dim[3]); }
        if (4 < p.rank) { ptx::tensormap_replace_box_dim(space_shared, &smem_tmap, ptx::n32_t<4>{}, p.box_dim[4]); }
        // Set global dimensions:
        if (0 < p.rank) { ptx::tensormap_replace_global_dim(space_shared, &smem_tmap, ptx::n32_t<0>{}, (uint32_t) p.global_dim[0]); }
        if (1 < p.rank) { ptx::tensormap_replace_global_dim(space_shared, &smem_tmap, ptx::n32_t<1>{}, (uint32_t) p.global_dim[1]); }
        if (2 < p.rank) { ptx::tensormap_replace_global_dim(space_shared, &smem_tmap, ptx::n32_t<2>{}, (uint32_t) p.global_dim[2]); }
        if (3 < p.rank) { ptx::tensormap_replace_global_dim(space_shared, &smem_tmap, ptx::n32_t<3>{}, (uint32_t) p.global_dim[3]); }
        if (4 < p.rank) { ptx::tensormap_replace_global_dim(space_shared, &smem_tmap, ptx::n32_t<4>{}, (uint32_t) p.global_dim[4]); }
        // Set global stride:
        if (1 < p.rank) { ptx::tensormap_replace_global_stride(space_shared, &smem_tmap, ptx::n32_t<0>{}, p.global_stride[0]); }
        if (2 < p.rank) { ptx::tensormap_replace_global_stride(space_shared, &smem_tmap, ptx::n32_t<1>{}, p.global_stride[1]); }
        if (3 < p.rank) { ptx::tensormap_replace_global_stride(space_shared, &smem_tmap, ptx::n32_t<2>{}, p.global_stride[2]); }
        if (4 < p.rank) { ptx::tensormap_replace_global_stride(space_shared, &smem_tmap, ptx::n32_t<3>{}, p.global_stride[3]); }
        // Set element stride:
        if (0 < p.rank) { ptx::tensormap_replace_element_size(space_shared, &smem_tmap, ptx::n32_t<0>{}, p.element_stride[0]); }
        if (1 < p.rank) { ptx::tensormap_replace_element_size(space_shared, &smem_tmap, ptx::n32_t<1>{}, p.element_stride[1]); }
        if (2 < p.rank) { ptx::tensormap_replace_element_size(space_shared, &smem_tmap, ptx::n32_t<2>{}, p.element_stride[2]); }
        if (3 < p.rank) { ptx::tensormap_replace_element_size(space_shared, &smem_tmap, ptx::n32_t<3>{}, p.element_stride[3]); }
        if (4 < p.rank) { ptx::tensormap_replace_element_size(space_shared, &smem_tmap, ptx::n32_t<4>{}, p.element_stride[4]); }

        // These constants are documented in this table:
        // https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#tensormap-
        // new-val-validity
        auto u8_elem_type = ptr::n32_t<0>{};
        ptr::tensormap_replace_elemtype(space_shared, &smem_tmap, u8_elem_type);
        auto no_interleave = ptr::n32_t<0>{};
        ptr::tensormap_replace_interleave_layout(space_shared, &smem_tmap, no_interleave);
        auto no_swizzle = ptr::n32_t<0>{};
        ptr::tensormap_replace_swizzle_mode(space_shared, &smem_tmap, no_swizzle);
        auto zero_fill = ptr::n32_t<0>{};
        ptr::tensormap_replace_fill_mode(space_shared, &smem_tmap, zero_fill);
    }
    // Synchronize the modifications with other threads in warp
    __syncwarp();
    // Copy the tensor map to global memory collectively with threads in the warp.
    // In addition: make the updated tensor map visible to other threads on device that
    // for use with cp.async.bulk.
    ptr::n32_t<128> bytes_128;
    ptr::tensormap_cp_fenceproxy(ptx::sem_release, ptr::scope_gpu, out, &smem_tmap,
    bytes_128);
}
```
