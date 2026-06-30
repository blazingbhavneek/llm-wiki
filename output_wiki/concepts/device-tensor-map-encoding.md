# Device-Side Tensor Map Encoding and Modification

Details the process of creating, copying, and modifying tiled-type tensor maps on the device using `cuda::ptx::tensormap_replace` functions. Covers the release-acquire synchronization pattern for using modified tensor maps across thread blocks.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L10837-L11088

Citation: [CUDA_C_Programming_Guide:L10837-L11088]

````text

Previous sections have described how to create a tensor map on the host using the CUDA driver API.

This section explains how to encode a tiled-type tensor map on device. This is useful in situations where the typical way of transferring the tensor map (using const \_\_grid\_constant\_\_ kernel parameters) is undesirable, for instance, when processing a batch of tensors of various sizes in a single kernel launch.

The recommended pattern is as follows:

1. Create a tensor map “template”, template\_tensor\_map, using the Driver API on the host.

2. In a device kernel, copy the template\_tensor\_map, modify the copy, store in global memory, and appropriately fence.

3. Use the tensor map in a kernel with appropriate fencing.

The high-level code structure is as follows:

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
p.box_dim[0]       = 128; // The box in shared memory has half the width of the full
buffer
p.box_dim[1]       = 4;   // The box in shared memory has half the height of the full
buffer
p.global_dim[0]      = 256; //
p.global_dim[1]      = 8;   //
p.global_stride[0]  = 256; //
p.element_stride[0] = 1;   //
p.element_stride[1] = 1;   Production

// Encode global_tensor_map on device:
encode_tensor_map<<<1, 32>>>(template_tensor_map, p, global_tensor_map);

// Use it from another kernel:
consume_tensor_map<<<1, 1>>>(global_tensor_map);

// Check for errors:
CUDA_CHECK(cudaDeviceSynchronize());
```

The following sections describe the high-level steps. Throughout the examples, the following tensormap\_params struct contains the new values of the fields to be updated. It is included here to reference when reading the examples.

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

## 10.30.1. Device-side Encoding and Modification of a Tensor Map

The recommended process of encoding a tensor map in global memory proceeds as follows.

1. Pass an existing tensor map, the template\_tensor\_map, to the kernel. In contrast to kernels that use the tensor map in a cp.async.bulk.tensor instruction, this may be done in any way: a pointer to global memory, kernel parameter, a \_\_const\_\_\_ variable, and so on.

2. Copy-initialize a tensor map in shared memory with the template\_tensor\_map value.

3. Modify the tensor map in shared memory using the cuda::ptx::tensormap\_replace functions. These functions wrap the tensormap.replace PTX instruction, which can be used to modify any field of a tiled-type tensor map, including the base address, size, stride, and so on.

4. Using the cuda::ptx::tensormap\_copy\_fenceproxy function, copy the modified tensor map from shared memory to global memory and perform any necessary fencing.

The following code contains a kernel that follows these steps. For completeness, it modifies all the fields of the tensor map. Typically, a kernel will modify just a few fields.

In this kernel, template\_tensor\_map is passed as a kernel parameter. This is the preferred way of moving template\_tensor\_map from the host to the device. If the kernel is intended to update an existing tensor map in device memory, it can take a pointer to the existing tensor map to modify.

Note: The format of the tensor map may change over time. Therefore, the cuda::ptx::tensormap\_replace functions and corresponding tensormap.replace.tile PTX instructions are marked as specific to sm\_90a. To use them, compile using nvcc -arch sm\_90a .....

Tip: On sm\_90a, a zero-initialized bufer in shared memory may also be used as the initial tensor map value. This enables encoding a tensor map purely on device, without using the driver API to encode the template\_tensor\_map value.

Note: On-device modification is only supported for tiled-type tensor maps; other tensor map types cannot be modified on device. For more information on the tensor map types, refer to the Driver API reference.

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
```

```rust
if (3 < p.rank) { ptr::tensormap_replace_element_size(space_shared, &smem_tmap,
ptx::n32_t<3>{}, p.element_stride[3]); }
if (4 < p.rank) { ptr::tensormap_replace_element_size(space_shared, &smem_tmap,
ptx::n32_t<4>{}, p.element_stride[4]); }

// These constants are documented in this table:
// https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#tensormap-
new-val-validity
auto u8_elem_type = ptr::n32_t<0>{};
ptr::tensormap_replace_elemtype(space_shared, &smem_tmap, u8_elem_type);
auto no_interleave = ptr::n32_t<0>{};
ptr::tensormap_replace_interleave_layout(space_shared, &smem_tmap, no_
interleave);
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

## 10.30.2. Usage of a Modified Tensor Map

In contrast to using a tensor map that is passed as a const \_\_grid\_constant\_\_ kernel parameter, using a tensor map in global memory requires explicitly establishing a release-acquire pattern in the tensor map proxy between the threads that modify the tensor map and the threads that use it.

The release part of the pattern was shown in the previous section. It is accomplished using the cuda::ptx::tensormap.cp\_fenceproxy function.

The acquire part is accomplished using the cuda::ptx::fence\_proxy\_tensormap\_generic function that wraps the fence.proxy.tensormap::generic.acquire instruction. If the two threads participating in the release-acquire pattern are on the same device, the .gpu scope sufices. If the threads are on diferent devices, the .sys scope must be used. Once a tensor map has been acquired by one thread, it can be used by other threads in the block after suficient synchronization, for example, using \_\_syncthreads(). The thread that uses the tensor map and the thread that performs the fence must be in the same block. That is, if the threads are in, for example, two diferent thread blocks of the same cluster, the same grid, or a diferent kernel, synchronization APIs such as cooperative\_groups::cluster or grid\_group::sync() or stream-order synchronization do not sufice to establish ordering for tensor map updates, that is, threads in these other thread blocks still need to acquire the tensor map proxy at the right scope before using the updated tensor map. If there are no intermediate modifications, the fence does not have to be repeated before each cp.async.bulk. tensor instruction.

The fence and subsequent use of the tensor map is shown in the following example.

```cpp
// Consumer of tensor map in global memory:
__global__ void consume_tensor_map(CUtensorMap* tensor_map) {
    // Fence acquire tensor map:
    ptx::n32_t<128> size_bytes;
    ptx::fence_proxy_tensorsgammaGeneric(ptx::sem_acquire, ptx::scope_sys, tensor_map,
size_bytes);
    // Safe to use tensor_map after fence..

    __shared__ uint64_t bar;
    __shared__ alignas(128) char smem_buf[4][128];

    if (threadIdx.x == 0) {
        // Initialize barrier
        ptx::mbarrier_init(&bar, 1);
        // Make barrier init visible in async proxy, i.e., to TMA engine
        ptx::fence_proxy_async(ptx::space_shared);
        // Issue TMA request
        ptx::cp_async_bulk_tensor(ptx::space_cluster, ptx::space_global, smem_buf, tensor_
map, {0, 0}, &bar);

        // Arrive on barrier. Expect 4 * 128 bytes.
        ptx::mbarrier_arrive_expect_tx(ptx::sem_release, ptx::scope_cta, ptx::space_
shared, &bar, sizeof(smem_buf));
    }
    const int parity = 0;
    // Wait for load to have completed
    while (!ptx::mbarrier_try_wait_parity(&bar, parity)) {}

    // print items:
    printf("Got:\n\n");
    for (int j = 0; j < 4; ++j) {
        for (int i = 0; i < 128; ++i) {
            printf("%3d ", smem_buf[j][i]);
            if (i % 32 == 31) { printf("\n"); };
        }
        printf("\n");
    }
}
```

## 10.30.3. Creating a Template Tensor Map Value Using the Driver API

The following code creates a minimal tiled-type tensor map that can be subsequently modified on device.

```c
CUtensorMap make_tensorsmap_template() {
  CUtensorMap template_tensor_map {};
  auto cuTensorMapEncodeTiled = get_cuTensorMapEncodeTiled();

  uint32_t dims_32          = 16;
  uint64_t dims_strides_64 = 16;
  uint32_t elem_strides    = 1;
```

(continues on next page)

(continued from previous page)

```cpp
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
````
