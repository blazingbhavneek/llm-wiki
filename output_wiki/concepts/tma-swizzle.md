# TMA Swizzle for Shared Memory Bank Conflict Avoidance

TMA swizzle is a feature of the Tensor Memory Accelerator (TMA) engine that rearranges data in shared memory to optimize access patterns and avoid shared memory bank conflicts [[CUDA_C_Programming_Guide:L10647-L10799]]. By default, the TMA engine loads data to shared memory in the same order as it is laid out in global memory, which may cause bank conflicts if the subsequent access pattern in shared memory does not match the global memory layout [[CUDA_C_Programming_Guide:L10647-L10799]].

## Shared Memory Architecture

Shared memory consists of 32 banks, where successive 32-bit words map to successive banks, and each bank provides a bandwidth of 32 bits per clock cycle [[CUDA_C_Programming_Guide:L10647-L10799]]. Bank conflicts occur when multiple threads in a warp access different addresses that map to the same bank within the same transaction, resulting in serialized access and reduced bandwidth [[CUDA_C_Programming_Guide:L10647-L10799]].

## Swizzle Modes

The TMA engine can be instructed to 'swizzle' data before storing it in shared memory and 'unswizzle' it when copying data back from shared memory to global memory [[CUDA_C_Programming_Guide:L10647-L10799]]. The swizzle mode is encoded in the tensor map using the `CUtensorMapSwizzle` type, which offers four options [[CUDA_C_Programming_Guide:L10647-L10799]]:

*   `CU_TENSOR_MAP_SWIZZLE_NONE`
*   `CU_TENSOR_MAP_SWIZZLE_32B`
*   `CU_TENSOR_MAP_SWIZZLE_64B`
*   `CU_TENSOR_MAP_SWIZZLE_128B`

These patterns define the mapping of 16-byte chunks along the swizzle width to subgroups of four banks [[CUDA_C_Programming_Guide:L10647-L10799]]. A key requirement is that the shared memory box's inner dimension must be less than or equal to the span of the selected swizzle pattern [[CUDA_C_Programming_Guide:L10647-L10799]].

## Example: Matrix Transpose with 128B Swizzle

A common use case for TMA swizzle is matrix transpose, where data is stored row-major in global memory but accessed column-wise in shared memory, leading to bank conflicts [[CUDA_C_Programming_Guide:L10647-L10799]]. Using the `CU_TENSOR_MAP_SWIZZLE_128B` layout matches the 128-byte row length and changes the shared memory layout so that both column-wise and row-wise accesses do not require the same banks per transaction [[CUDA_C_Programming_Guide:L10647-L10799]].

### Implementation Details

To use 128B swizzle, the shared memory buffer must be 1024-byte aligned [[CUDA_C_Programming_Guide:L10647-L10799]]. The tensor map is configured with the swizzle mode and appropriate box dimensions [[CUDA_C_Programming_Guide:L10647-L10799]].

```cpp
// Example tensor map configuration for 128B swizzle
CUtensorMap tensor_map{
    // ... other fields ...
    // Using a swizzle pattern of 128 bytes.
    CUtensorMapSwizzle::CU_TENSOR_MAP_SWIZZLE_128B,
    // ... other fields ...
};
```

When accessing the swizzled shared memory, the indices must be transformed to match the new layout. For an 8x8 matrix of `int4`, the access pattern involves XOR operations on the indices to align with the swizzled banks [[CUDA_C_Programming_Guide:L10647-L10799]]:

```cpp
for(int sidx_j = threadIdx.x; sidx_j < 8; sidx_j+= blockDim.x){
    for(int sidx_i = 0; sidx_i < 8; ++sidx_i){
        const int swiz_j_idx = (sidx_i % 8) ^ sidx_j;
        const int swiz_i_idx_tr = (sidx_j % 8) ^ sidx_i;
        smem_buffer_tr[sidx_j][swiz_i_idx_tr] = smem_buffer[sidx_i][swiz_j_idx];
    }
}
```

Without swizzle, storing a row from shared memory to a column in a transpose buffer results in an eight-way bank conflict [[CUDA_C_Programming_Guide:L10647-L10799]]. With 128B swizzle, each matrix element is mapped to a different bank for both rows and columns, eliminating bank conflicts for both load and store operations [[CUDA_C_Programming_Guide:L10647-L10799]].

### Data Flow

1.  **Global to Shared**: The TMA engine loads data from global memory to shared memory, applying the swizzle pattern [[CUDA_C_Programming_Guide:L10647-L10799]].
2.  **Shared Memory Processing**: Threads access the swizzled shared memory using transformed indices to avoid conflicts [[CUDA_C_Programming_Guide:L10647-L10799]].
3.  **Shared to Global**: The TMA engine copies data back from shared memory to global memory, automatically 'unswizzling' the data to restore the original global memory layout [[CUDA_C_Programming_Guide:L10647-L10799]].

## References

*   CUDA C++ Programming Guide, Section 10.29.3: TMA Swizzle [[CUDA_C_Programming_Guide:L10647-L10799]]
