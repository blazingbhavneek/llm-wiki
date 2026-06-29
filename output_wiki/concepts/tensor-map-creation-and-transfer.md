# Tensor Map Creation and Host-to-Device Transfer

The primary difference between one-dimensional and multi-dimensional transfers using Tensor Memory Accelerator (TMA) is that a tensor map must be created on the host and passed to the CUDA kernel [CUDA_C_Programming_Guide:L10352-L10355]. This section describes how to create a tensor map using the CUDA driver API, how to pass it to the device, and how to use it on the device [CUDA_C_Programming_Guide:L10352-L10355].

## Driver API Access

A tensor map is created using the `cuTensorMapEncodeTiled` driver API [CUDA_C_Programming_Guide:L10356-L10357]. This API can be accessed by linking to the driver directly (`-lcuda`) or by using the `cudaGetDriverEntryPointByVersion` API [CUDA_C_Programming_Guide:L10357-L10359]. Below is an example of how to get a pointer to the `cuTensorMapEncodeTiled` API [CUDA_C_Programming_Guide:L10360-L10373]:

```cpp
#include <cudaTypedefs.h> // PFN_cuTensorMapEncodeTiled, CUtensorMap

PFN_cuTensorMapEncodeTiled_v12000 get_cuTensorMapEncodeTiled() {
    // Get pointer to cuTensorMapEncodeTiled
    cudaDriverEntryPointQueryResult driver_status;
    void* cuTensorMapEncodeTiled_ptr = nullptr;
    CUDA_CHECK(cudaGetDriverEntryPointByVersion("cuTensorMapEncodeTiled", &
    cuTensorMapEncodeTiled_ptr, 12000, cudaEnableDefault, &driver_status));
    assert(driver_status == cudaDriverEntryPointSuccess);

    return reinterpret_cast<PFN_cuTensorMapEncodeTiled_v12000>(cuTensorMapEncodeTiled_ptr);
}
```

## Creating a Tensor Map

Creating a tensor map requires many parameters. Among them are the base pointer to an array in global memory, the size of the array (in number of elements), the stride from one row to the next (in bytes), and the size of the shared memory buffer (in number of elements) [CUDA_C_Programming_Guide:L10375-L10379].

The code below creates a tensor map to describe a two-dimensional row-major array of size `GMEM_HEIGHT x GMEM_WIDTH` [CUDA_C_Programming_Guide:L10380-L10381]. Note the order of the parameters: the fastest moving dimension comes first [CUDA_C_Programming_Guide:L10381-L10382]:

```c
CUtensorMap tensor_map{
// rank is the number of dimensions of the array.
constexpr uint32_t rank = 2;
uint64_t size[rank] = {GMEM_WIDTH, GMEM_HEIGHT};
// The stride is the number of bytes to traverse from the first element of one row to
the next.
// It must be a multiple of 16.
uint64_t stride[rank - 1] = {GMEM_WIDTH * sizeof(int)};
// The box_size is the size of the shared memory buffer that is used as the
// destination of a TMA transfer.
uint32_t box_size[rank] = {SMEM_WIDTH, SMEM_HEIGHT};
// The distance between elements in units of sizeof(element). A stride of 2
// can be used to load only the real component of a complex-valued tensor, for instance.
uint32_t elem_stride[rank] = {1, 1};

// Get a function pointer to the cuTensorMapEncodeTiled driver API.
auto cuTensorMapEncodeTiled = get_cuTensorMapEncodeTiled();

// Create the tensor descriptor.
CUresult res = cuTensorMapEncodeTiled(
    &tensor_map,            // CUtensorMap *tensorMap,
    CUtensorMapDataType::CU_TENSOR_MAP_DATA_TYPE_INT32,
    rank,                // cuuint32_t tensorRank,
    tensor_ptr,             // void *globalAddress,
    size,                // const cuuint64_t *globalDim,
    stride,                // const cuuint64_t *globalStrides,
    box_size,             // const cuuint32_t *boxDim,
    elem_stride,             // const cuuint32_t *elementStrides,
    // Interleave patterns can be used to accelerate loading of values that
    // are less than 4 bytes long.
    CUtensorMapInterleave::CU_TENSOR_MAP_INTERLEAVE_NONE,
    // Swizzling can be used to avoid shared memory bank conflicts.
    CUtensorMapSwizzle::CU_TENSOR_MAP_SWIZZLE_NONE,
    // L2 Promotion can be used to widen the effect of a cache-policy to a wider
    // set of L2 cache lines.
    CUtensorMapL2promotion::CU_TENSOR_MAP_L2_PROMOTION_NONE,
    // Any element that is outside of bounds will be set to zero by the TMA transfer.
    CUtensorMapFloatOOBfill::CU_TENSOR_MAP_FLOAT_OOB_FILL_NONE
);
```

## Host-to-Device Transfer

There are three ways to make a tensor map accessible to device code [CUDA_C_Programming_Guide:L10430-L10432].

### 1. __grid_constant__ Kernel Parameter (Recommended)

The recommended approach is to pass the tensor map as a `const __grid_constant__` parameter to a kernel [CUDA_C_Programming_Guide:L10432-L10434]. When passing the tensor map as a parameter, some versions of the GCC C++ compiler issue the warning “the ABI for passing parameters with 64-byte alignment has changed in GCC 4.6” [CUDA_C_Programming_Guide:L10435-L10436]. This warning can be ignored [CUDA_C_Programming_Guide:L10436-L10437].

```c
#include <cuda.h>

__global__ void kernel(const __grid_constant__ CUtensorMap tensor_map)
{
    // Use tensor_map here.
}
int main() {
    CUtensorMap map;
    // [ ..Initialize map.. ]
    kernel<<<1, 1>>>(map);
}
```

### 2. __constant__ Memory

As an alternative to the `__grid_constant__` kernel parameter, a global constant variable can be used [CUDA_C_Programming_Guide:L10438-L10440]. The tensor map is copied into device `__constant__` memory using `cudaMemcpyToSymbol` [CUDA_C_Programming_Guide:L10432-L10433]:

```c
#include <cuda.h>

__constant__ CUtensorMap global_tensor_map;
__global__ void kernel()
{
    // Use global_tensor_map here.
}
int main() {
    CUtensorMap local_tensor_map;
    // [ ..Initialize map.. ]
    cudaMemcpyToSymbol(global_tensor_map, &local_tensor_map, sizeof(CUtensorMap));
    kernel<<<1, 1>>>();
}
```

### 3. Global Memory with Explicit Fencing

Finally, it is possible to copy the tensor map to global memory [CUDA_C_Programming_Guide:L10441-L10442]. Using a pointer to a tensor map in global device memory requires a fence in each thread block before any thread in the block uses the updated tensor map [CUDA_C_Programming_Guide:L10443-L10444]. Further uses of the tensor map by that thread block do not need to be fenced unless the tensor map is modified again [CUDA_C_Programming_Guide:L10444-L10445]. Note that this mechanism may be slower than the two mechanisms described above [CUDA_C_Programming_Guide:L10445-L10446].

```cpp
#include <cuda.h>
#include <cuda/ptx>
namespace ptx = cuda::ptx;

__device__ CUtensorMap global_tensor_map;
__global__ void kernel(CUtensorMap *tensor_map)
{
    // Fence acquire tensor map:
    ptx::n32_t<128> size_bytes;
    // Since the tensor map was modified from the host using cudaMemcpy,
    // the scope should be .sys.
    ptx::fence_proxy_tensorsmap_generic(
        ptx::sem_acquire, ptx::scope_sys, tensor_map, size_bytes
    );
    // Safe to use tensor_map after fence inside this thread..
}
int main() {
    CUtensorMap local_tensor_map;
    // [ ..Initialize map.. ]
    cudaMemcpy(&global_tensor_map, &local_tensor_map, sizeof(CUtensorMap),
    -->cudaMemcpyHostToDevice);
    kernel<<<1, 1>>>(global_tensor_map);
}
```
