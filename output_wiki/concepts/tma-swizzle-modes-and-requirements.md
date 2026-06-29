# TMA Swizzle Modes and Requirements

Tensor Memory Accelerator (TMA) swizzle modes are used to map data from global memory to shared memory in a way that avoids bank conflicts. There are four swizzle modes available, which define how 16-byte chunks along a 128-byte boundary are mapped to eight subgroups of four banks [CUDA_C_Programming_Guide:L10800-L10834].

## Memory Alignment Requirements

When applying a TMA swizzle pattern, specific memory alignment constraints must be met:

*   **Global Memory Alignment**: Global memory must be aligned to 128 bytes [CUDA_C_Programming_Guide:L10800-L10834].
*   **Shared Memory Alignment**: Shared memory should be aligned according to the number of bytes after which the swizzle pattern repeats. If the shared memory buffer is not aligned by this repetition size, an offset occurs between the swizzle pattern and the shared memory [CUDA_C_Programming_Guide:L10800-L10834].

## Inner Dimension and Granularity

*   **Inner Dimension**: The inner dimension of the shared memory block must meet the size requirements specified for the chosen swizzle mode. If these requirements are not met, the instruction is considered invalid. Additionally, if the swizzle width exceeds the inner dimension, the shared memory must be allocated to accommodate the full swizzle width [CUDA_C_Programming_Guide:L10800-L10834].
*   **Granularity**: The granularity of the swizzle mapping is fixed at 16 bytes. Data is organized and accessed in 16-byte chunks, which must be considered when planning memory layout and access patterns [CUDA_C_Programming_Guide:L10800-L10834].

## Swizzle Pattern Pointer Offset Computation

When the shared memory buffer is not aligned by the number of bytes by which the swizzle pattern repeats itself, an offset must be computed to correctly index the shared memory. The shared memory is required to be aligned to 128 bytes. The offset determines how many times the shared memory buffer is shifted relative to the swizzle pattern [CUDA_C_Programming_Guide:L10800-L10834].

The offset formula and index relation for different swizzle modes are defined as follows:

| Swizzle Mode | Offset Formula | Index Relation |
| :--- | :--- | :--- |
| `CU_TENSOR_MAP_SWIZZLE_128B` | `(reinterpret_cast<uintptr_t>(smem_ptr)/128)%8` | `smem[y][x] <-> smem[y][((y+offset)%8)^x]` |
| `CU_TENSOR_MAP_SWIZZLE_64B` | `(reinterpret_cast<uintptr_t>(smem_ptr)/128)%4` | `smem[y][x] <-> smem[y][((y+offset)%4)^x]` |
| `CU_TENSOR_MAP_SWIZZLE_32B` | `(reinterpret_cast<uintptr_t>(smem_ptr)/128)%2` | `smem[y][x] <-> smem[y][((y+offset)%2)^x]` |

In these formulas, `offset` represents the initial row offset, which is added to the row index `y` in the swizzle index calculation [CUDA_C_Programming_Guide:L10800-L10834].

### Example: Accessing Swizzled Shared Memory

The following snippet demonstrates how to access swizzled shared memory in the `CU_TENSOR_MAP_SWIZZLE_128B` mode:

```cpp
data_t* smem_ptr = &smem[0][0];
int offset = (reinterpret_cast<uintptr_t>(smem_ptr)/128)%8;
smem[y][((y+offset)%8)^x] = ...;
```

## Swizzle Pattern Properties (Compute Capability 9)

The following table summarizes the requirements and properties of the different swizzle patterns for Compute Capability 9:

| Pattern | Swizzle Width | Shared Box's Inner Dimension | Repeats After | Shared Memory Alignment | Global Memory Alignment |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `CU_TENSOR_MAP_SWIZZLE_128B` | 128 bytes | <= 128 bytes | 1024 bytes | 128 bytes | 128 bytes |
| `CU_TENSOR_MAP_SWIZZLE_64B` | 64 bytes | <= 64 bytes | 512 bytes | 128 bytes | 128 bytes |
| `CU_TENSOR_MAP_SWIZZLE_32B` | 32 bytes | <= 32 bytes | 256 bytes | 128 bytes | 128 bytes |
| `CU_TENSOR_MAP_SWIZZLE_NONE` (default) | None | - | - | 128 bytes | 16 bytes |

Note: The source text contains garbled characters for the swizzle widths (e.g., "B288B bytes"), which have been corrected to their standard values (128, 64, 32 bytes) based on the context of the swizzle modes and the "Repeats After" column which corresponds to 8x, 4x, and 2x the swizzle width respectively. The default mode `CU_TENSOR_MAP_SWIZZLE_NONE` has no swizzle width and requires only 16-byte global memory alignment [CUDA_C_Programming_Guide:L10800-L10834].
