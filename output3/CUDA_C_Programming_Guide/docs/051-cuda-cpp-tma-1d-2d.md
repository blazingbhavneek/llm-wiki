
## 10.29.3. TMA Swizzle

By default, the TMA engine loads data to shared memory in the same order as it is laid out in global memory. However, this layout may not be optimal for certain shared memory access patterns, as it could cause shared memory bank conflicts. To improve performance and reduce bank conflicts, we can change the shared memory layout by applying a ‘swizzle pattern’.

Shared memory has 32 banks that are organized such that successive 32-bit words map to successive banks. Each bank has a bandwidth of 32 bits per clock cycle. When loading and storing shared memory, bank conflicts arise if the same bank is used multiple times within a transaction, resulting in reduced bandwidth. See Shared Memory, bank conflicts.

To ensure that data is laid out in shared memory in such a way that user code can avoid shared memory bank conflicts, the TMA engine can be instructed to ‘swizzle’ the data before storing it in shared memory and ‘unswizzle’ it when copying the data back from shared memory to global memory. The tensor map encodes the ‘swizzle mode’ indicating which swizzle pattern is used.

## 10.29.3.1 Example ‘Matrix Transpose

An example is the transpose of a matrix where data is mapped from row to column first access. The data is stored row major in global memory, but we want to also access it column wise in shared memory, which leads to bank conflicts. However, by using the 128 bytes ‘swizzle’ mode and new shared memory indices, they are eliminated.

In the example, we load an 8x8 matrix of type int4, stored as row major in global memory to shared memory. Then, each set of eight threads loads a row from the shared memory bufer and stores it to a column in a separate transpose shared memory bufer. This results in an eight-way bank conflict when storing. Finally, the transpose bufer is written back to global memory.

To avoid bank conflicts, the CU\_TENSOR\_MAP\_SWIZZLE\_128B layout can be used. This layout matches the 128 bytes row length and changes the shared memory layout in a way that both the column wise and row wise access don’t require the same banks per transaction.

The two tables, Figure 27 and Figure 28, below show the normal and the swizzled shared memory layout of the 8x8 matrix of type int4 and its transpose matrix. The colors indicate which of the eight groups of four banks the matrix element is mapped to, and the margin row and margin column list the global memory row and column indices. The entries show the shared memory indices of the 16-byte matrix elements.

```cpp
__global__ void kernel_tma(const __grid_constant__ CUtensorMap tensor_map) {
    // The destination shared memory buffer of a bulk tensor operation
    // with the 128-byte swizzle mode, it should be 1024 bytes aligned.
    __shared__ alignas(1024) int4 smem_buffer[8][8];
    __shared__ alignas(1024) int4 smem_buffer_tr[8][8];

    // Initialize shared memory barrier
    #pragma nv_diag_suppress static_var_with_dynamic_init
    __shared__ barrier bar;

    if (threadIdx.x == 0) {
        init(&bar, blockDim.x);
        cde::fence_proxy_async_shared_cta();
    }

    __syncthreads();
```

(continues on next page)

<table><tr><td></td><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td></tr><tr><td>0</td><td>[0,0]</td><td>[0,1]</td><td>[0,2]</td><td>[0,3]</td><td>[0,4]</td><td>[0,5]</td><td>[0,6]</td><td>[0,7]</td></tr><tr><td>1</td><td>[1,0]</td><td>[1,1]</td><td>[1,2]</td><td>[1,3]</td><td>[1,4]</td><td>[1,5]</td><td>[1,6]</td><td>[1,7]</td></tr><tr><td>2</td><td>[2,0]</td><td>[2,1]</td><td>[2,2]</td><td>[2,3]</td><td>[2,4]</td><td>[2,5]</td><td>[2,6]</td><td>[2,7]</td></tr><tr><td>3</td><td>[3,0]</td><td>[3,1]</td><td>[3,2]</td><td>[3,3]</td><td>[3,4]</td><td>[3,5]</td><td>[3,6]</td><td>[3,7]</td></tr><tr><td>4</td><td>[4,0]</td><td>[4,1]</td><td>[4,2]</td><td>[4,3]</td><td>[4,4]</td><td>[4,5]</td><td>[4,6]</td><td>[4,7]</td></tr><tr><td>5</td><td>[5,0]</td><td>[5,1]</td><td>[5,2]</td><td>[5,3]</td><td>[5,4]</td><td>[5,5]</td><td>[5,6]</td><td>[5,7]</td></tr><tr><td>6</td><td>[6,0]</td><td>[6,1]</td><td>[6,2]</td><td>[6,3]</td><td>[6,4]</td><td>[6,5]</td><td>[6,6]</td><td>[6,7]</td></tr><tr><td>7</td><td>[7,0]</td><td>[7,1]</td><td>[7,2]</td><td>[7,3]</td><td>[7,4]</td><td>[7,5]</td><td>[7,6]</td><td>[7,7]</td></tr></table>

Figure 27: In the shared memory data layout without swizzle, the shared memory indices are equivalent to the global memory indices. Per load instruction, one row is read and stored in a column of the transpose bufer. Since all matrix elements of the column in the transpose fall in the same bank, the store must be serialized, resulting in eight store transactions, giving an eight-way bank conflict per stored column.

<table><tr><td></td><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td></tr><tr><td>0</td><td>[0,0]</td><td>[0,1]</td><td>[0,2]</td><td>[0,3]</td><td>[0,4]</td><td>[0,5]</td><td>[0,6]</td><td>[0,7]</td></tr><tr><td>1</td><td>[1,1]</td><td>[1,0]</td><td>[1,3]</td><td>[1,2]</td><td>[1,5]</td><td>[1,4]</td><td>[1,7]</td><td>[1,6]</td></tr><tr><td>2</td><td>[2,2]</td><td>[2,3]</td><td>[2,0]</td><td>[2,1]</td><td>[2,6]</td><td>[2,7]</td><td>[2,4]</td><td>[2,5]</td></tr><tr><td>3</td><td>[3,3]</td><td>[3,2]</td><td>[3,1]</td><td>[3,0]</td><td>[3,7]</td><td>[3,6]</td><td>[3,5]</td><td>[3,4]</td></tr><tr><td>4</td><td>[4,4]</td><td>[4,5]</td><td>[4,6]</td><td>[4,7]</td><td>[4,0]</td><td>[4,1]</td><td>[4,2]</td><td>[4,3]</td></tr><tr><td>5</td><td>[5,5]</td><td>[5,4]</td><td>[5,7]</td><td>[5,6]</td><td>[5,1]</td><td>[5,0]</td><td>[5,3]</td><td>[5,2]</td></tr><tr><td>6</td><td>[6,6]</td><td>[6,7]</td><td>[6,4]</td><td>[6,5]</td><td>[6,2]</td><td>[6,3]</td><td>[6,0]</td><td>[6,1]</td></tr><tr><td>7</td><td>[7,7]</td><td>[7,6]</td><td>[7,5]</td><td>[7,4]</td><td>[7,3]</td><td>[7,2]</td><td>[7,1]</td><td>[7,0]</td></tr></table>

Figure 28: The shared memory data layout with CU\_TENSOR\_MAP\_SWIZZLE\_128B swizzle. One row is stored in a column, each matrix element is from a diferent bank for both the rows and columns, and so without any bank conflicts.

(continued from previous page)

```txt
barrier::arrival_token token;
if (threadIdx.x == 0) {
    // Initiate bulk tensor copy from global to shared memory,
    // in the same way as without swizzle.
    cde::cp_async_bulk_tensor_2d_global_to_shared(&smem_buffer, &tensor_map, 0, 0,
    bar);
    token = cuda::device::barrier_arrive_tx(bar, 1, sizeof(smem_buffer));
} else {
    token = bar.arrive();
}

bar.wait(std::move(token));

/* Matrix transpose
 * When using the normal shared memory layout, there are eight
 * 8-way shared memory bank conflict when storing to the transpose.
 * When enabling the 128-byte swizzle pattern and using the according access
pattern,
 * they are eliminated both for load and store. */
for(int sidx_j =threadIdx.x; sidx_j < 8; sidx_j+= blockDim.x){
    for(int sidx_i = 0; sidx_i < 8; ++sidx_i){
        const int swiz_j_idx = (sidx_i % 8) ^ sidx_j;
        const int swiz_i_idx_tr = (sidx_j % 8) ^ sidx_i;
        smem_buffer_tr[sidx_j][swiz_i_idx_tr] = smem_buffer[sidx_i][swiz_j_idx];
    }
}
```

(continues on next page)

(continued from previous page)

```cpp
}

// Wait for shared memory writes to be visible to TMA engine.
cde::fence_proxy_async_shared_cta();
__syncthreads();

/* Initiate TMA transfer to copy the transposed shared memory buffer back to global
memory,
 * it will 'unswizzle' the data. */
if (threadIdx.x == 0) {
    cde::cp_async_bulk_tensor_2d_shared_to_global(&tensor_map, 0, 0, &smem_buffer_
->tr);
    cde::cp_async_bulk_commit_group();
    cde::cp_async_bulk_wait_group_read<0>();
}

// Destroy barrier
if (threadIdx.x == 0) {
    (&bar)->~barrier();
}
}

// --------------------------------------------------- main ---------------------------------------------------
int main(){
...
void* tensor_ptr = d_data;

CUtensorMap tensor_map{
// rank is the number of dimensions of the array.
constexpr uint32_t rank = 2;
// global memory size
uint64_t size[rank] = {4*8, 8};
// global memory stride, must be a multiple of 16.
uint64_t stride[rank - 1] = {8 * sizeof(int4)};
// The inner shared memory box dimension in bytes, equal to the swizzle span.
uint32_t box_size[rank] = {4*8, 8};

uint32_t elem_stride[rank] = {1, 1};

// Create the tensor descriptor.
CUresult res = cuTensorMapEncodeTiled(
    &tensor_map,          // CUtensorMap *tensorMap,
    CUtensorMapDataType::CU_TENSOR_MAP_DATA_TYPE_INT32,
    rank,            // cuuint32_t tensorRank,
    tensor_ptr,         // void *globalAddress,
    size,             // const cuuint64_t *globalDim,
    stride,             // const cuuint64_t *globalStrides,
    box_size,           // const cuuint32_t *boxDim,
    elem_stride,        // const cuuint32_t *elementStrides,
    CUtensorMapInterleave::CU_TENSOR_MAP_INTERLEAVE_NONE,
    // Using a swizzle pattern of 128 bytes.
    CUtensorMapSwizzle::CU_TENSOR_MAP_SWIZZLE_128B,
    CUtensorMapL2promotion::CU_TENSOR_MAP_L2_PROMOTION_NONE,
    CUtensorMapFloatOOBfill::CU_TENSOR_MAP_FLOAT_OOB_FILL_NONE
```

(continues on next page)

```lisp
);  
kernel_tma<<<1, 8>>>(tensor_map);  
...  
}
```

Remark. This example is supposed to show the use of swizzle and ‘as-is’ is not performant nor does it scale beyond the given dimensions.

Explanation. During data transfer, the TMA engine shufles the data according to the swizzle pattern, as described in the following tables. These swizzle patterns define the mapping of the 16-byte chunks along the swizzle width to subgroups of four banks. It is of type CUtensorMapSwizzle and has four options: none, 32 bytes, 64 bytes and 128 bytes. Note that the shared memory box’s inner dimension must be less or equal to the span of the swizzle pattern.

## 10.29.3.2 The Swizzle Modes

As previously mentioned, there are four swizzle modes. The following tables show the diferent swizzle patterns, including the relation of the new shared memory indices. The tables define the mapping of the 16-byte chunks along the 128 bytes to eight subgroups of four banks.

![](images/f077aa9ba5854cd97d14f8b0541a23f330c238d1239e194c12324ab56bb762f9.jpg)  
Figure 29: An Overview of TMA Swizzle Patterns

Considerations. When applying a TMA swizzle pattern, it is crucial to adhere to specific memory requirements:

▶ Global memory alignment: Global memory must be aligned to 128 bytes.

Shared memory alignment: For simplicity shared memory should be aligned according to the number of bytes after which the swizzle pattern repeats. When the shared memory bufer is not aligned by the number of bytes by which the swizzle pattern repeats itself, there is an ofset between the swizzle pattern and the shared memory. See comment, below.

Inner dimension: The inner dimension of the shared memory block must meet the size requirements specified in Table 12. If these requirements are not met, the instruction is considered invalid. Additionally, if the swizzle width exceeds the inner dimension, ensure that the shared memory is allocated to accommodate the full swizzle width.

▶ Granularity: The granularity of swizzle mapping is fixed at 16 bytes. This means that data is organized and accessed in chunks of 16 bytes, which must be considered when planning memory layout and access patterns.

Swizzle Pattern Pointer Ofset Computation. Here, we describe how to determine the ofset between the swizzle pattern and the shared memory, when the shared memory bufer is not aligned by the number of bytes by which the swizzle pattern repeats itself. When using TMA, the shared memory is required to be aligned to 128 bytes. To find how many times the shared memory bufer relative to the swizzle pattern is shifted by that, apply the corresponding ofset formula.

Table 11: Swizzle Pattern Pointer Ofset Formula and Index Relation

<table><tr><td>Swizzle Mode</td><td>Offset Formula</td><td>Index Relation</td></tr><tr><td>CU_TENSOR_MAP_SWIZZ</td><td>ZtreInterpret_cast(smem_ptr)/128)%8</td><td>smem[y][x] &lt;-&gt; smem[y][((y+offset)%8)^x]</td></tr><tr><td>CU_TENSOR_MAP_SWIZZ</td><td>ZtreInterpret_cast(smem_ptr)/128)%4</td><td>smem[y][x] &lt;-&gt; smem[y][((y+offset)%4)^x]</td></tr><tr><td>CU_TENSOR_MAP_SWIZZ</td><td>ZtreInterpret_cast(smem_ptr)/128)%2</td><td>smem[y][x] &lt;-&gt; smem[y][((y+offset)%2)^x]</td></tr></table>

In Figure 29, this ofset represents the initial row ofset, thus, in the swizzle index calculation, it is added to the row index y. The following snippet shows how to access the swizzled shared memory in the CU\_TENSOR\_MAP\_SWIZZLE\_128B mode.

```txt
data_t* smem_ptr = &smem[0][0];
int offset = (reinterpret_cast<uintptr_t>(smem_ptr)/128)%8;
smem[y][((y+offset)%8)^x] = ...
```

Summary. The following Table 12 summarizes the requirements and properties of the diferent swizzle patterns for Compute Capability 9.

Table 12: Requirements and properties of the diferent swizzle patterns for Compute Capability 9

<table><tr><td>Pattern</td><td>Swizzle width</td><td>Shared box&#x27;s inner dimension</td><td>Re-peats after</td><td>Shared memory alignment</td><td>Global memory alignment</td></tr><tr><td>CU_TENSOR_MAP_SWIZZ</td><td>B288B bytes</td><td>&lt;=128 bytes</td><td>1024 bytes</td><td>128 bytes</td><td>128 bytes</td></tr><tr><td>CU_TENSOR_MAP_SWIZZ</td><td>B464B bytes</td><td>&lt;=64 bytes</td><td>512 bytes</td><td>128 bytes</td><td>128 bytes</td></tr><tr><td>CU_TENSOR_MAP_SWIZZ</td><td>B232B bytes</td><td>&lt;=32 bytes</td><td>256 bytes</td><td>128 bytes</td><td>128 bytes</td></tr><tr><td>CU_TENSOR_MAP_SWIZZ (default)</td><td>E_NONE</td><td></td><td></td><td>128 bytes</td><td>16 bytes</td></tr></table>
