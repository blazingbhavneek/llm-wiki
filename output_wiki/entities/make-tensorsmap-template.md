# make_tensorsmap_template

The `make_tensorsmap_template` function provides an example of how to create a minimal tiled-type tensor map that can be subsequently modified on device. It utilizes the `cuTensorMapEncodeTiled` Driver API function to initialize the `CUtensorMap` structure.

## Implementation

The function initializes a `CUtensorMap` object and configures it with specific parameters for rank, dimensions, strides, and data type. The implementation assumes the availability of a helper function `get_cuTensorMapEncodeTiled` to retrieve the API function pointer.

### Key Configuration Parameters

*   **Tensor Rank**: Set to 1.
*   **Data Type**: `CU_TENSOR_MAP_DATA_TYPE_UINT8`.
*   **Global Address**: `nullptr` (indicating a template that can be updated).
*   **Dimensions and Strides**: Configured using `uint64_t` arrays (`dims_strides_64`) with a value of 16.
*   **Box Dimensions**: Configured using `uint32_t` (`dims_32`) with a value of 16.
*   **Element Strides**: Set to 1.
*   **Interleave**: `CU_TENSOR_MAP_INTERLEAVE_NONE`.
*   **Swizzle**: `CU_TENSOR_MAP_SWIZZLE_NONE`.
*   **L2 Promotion**: `CU_TENSOR_MAP_L2_PROMOTION_NONE`.
*   **Float OOB Fill**: `CU_TENSOR_MAP_FLOAT_OOB_FILL_NONE`.

### Code Example

```c
CUtensorMap make_tensorsmap_template() {
  CUtensorMap template_tensor_map {};
  auto cuTensorMapEncodeTiled = get_cuTensorMapEncodeTiled();

  uint32_t dims_32          = 16;
  uint64_t dims_strides_64 = 16;
  uint32_t elem_strides    = 1;

  // Create the tensor descriptor.
  CUresult res = cuTensorMapEncodeTiled(
      &template_tensor_map, // CUtensorMap *tensorMap,
      CUtensorMapDataType::CU_TENSOR_MAP_DATA_TYPE_UINT8,
      1,             // cuuint32_t tensorRank,
      nullptr,         // void *globalAddress,
      &dims_strides_64, // const cuuint64_t *globalDim,
      &dims_strides_64, // const cuuint64_t *globalStrides,
      &dims_32,          // const cuuint32_t *boxDim,
      &elem_strides,     // const cuuint32_t *elementStrides,
      CUtensorMapInterleave::CU_TENSOR_MAP_INTERLEAVE_NONE,
      CUtensorMapSwizzle::CU_TENSOR_MAP_SWIZZLE_NONE,
      CUtensorMapL2promotion::CU_TENSOR_MAP_L2_PROMOTION_NONE,
      CUtensorMapFloatOOBfill::CU_TENSOR_MAP_FLOAT_OOB_FILL_NONE);

  CU_CHECK(res);
  return template_tensor_map;
}
```

## References

*   CUDA C Programming Guide: Creating a Template Tensor Map Value Using the Driver API [CUDA_C_Programming_Guide:L11050-L11088]
