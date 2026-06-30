# Asynchronous Data Copies using the Tensor Memory Accelerator (TMA)

The Tensor Memory Accelerator (TMA) is a hardware feature introduced in Compute Capability 9.0 that provides an efficient mechanism for asynchronous data transfers between global memory, shared memory, and distributed shared memory. It supports both one-dimensional contiguous arrays and multi-dimensional arrays (up to 5D) via tensor maps, reducing the need for error-prone address calculations on the device. TMA operations are asynchronous, allowing the CPU/GPU to continue computation while data is transferred, and utilize specific completion mechanisms like shared memory barriers (mbarrier) and bulk async-groups.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L10218-L10563

Citation: [CUDA_C_Programming_Guide:L10218-L10563]

````text
## 10.29. Asynchronous Data Copies using the Tensor Memory Accelerator (TMA)

Many applications require movement of large amounts of data from and to global memory. Often, the data is laid out in global memory as a multi-dimensional array with non-sequential data acess patterns. To reduce global memory usage, sub-tiles of such arrays are copied to shared memory before use in computations. The loading and storing involves address-calculations that can be error-prone and repetitive. To ofload these computations, Compute Capability 9.0 introduces the Tensor Memory Accelerator (TMA). The primary goal of TMA is to provide an eficient data transfer mechanism from global memory to shared memory for multi-dimensional arrays.

Naming. Tensor memory accelerator (TMA) is a broad term used to refer to the features described in this section. For the purpose of forward-compatibility and to reduce discrepancies with the PTX ISA, the text in this section refers to TMA operations as either bulk-asynchronous copies or bulk tensor asynchronous copies, depending on the specific type of copy used. The term “bulk” is used to contrast these operations with the asynchronous memory operations described in the previous sections.

Dimensions. TMA supports copying both one-dimensional and multi-dimensional arrays (up to 5- dimensional). The programming model for bulk-asynchronous copies of one-dimensional contiguous arrays is diferent from the programming model for bulk tensor asynchronous copies of multidimensional arrays. To perform a bulk tensor asynchronous copy of a multi-dimensional array, the hardware requires a tensor map. This object describes the layout of the multi-dimensional array in global and shared memory. A tensor map is typically created on the host using the cuTensorMapEncode API and then transferred from host to device as a const kernel parameter annotated with \_\_grid\_constant\_\_. The tensor map is transferred from host to device as a const kernel parameter annotated with \_\_grid\_constant\_\_, and can be used on the device to copy a tile of data between shared and global memory. In contrast, performing a bulk-asynchronous copy of a contiguous onedimensional array does not require a tensor map: it can be performed on-device with a pointer and size parameter.

Source and destination. The source and destination addresses of bulk-asynchronous copy operations can be in shared or global memory. The operations can read data from global to shared memory, write data from shared to global memory, and also copy from shared memory to Distributed Shared Memory of another block in the same cluster. In addition, when in a cluster, a bulk-asynchronous operation can be specified as being multicast. In this case, data can be transferred from global memory to the shared memory of multiple blocks within the cluster. The multicast feature is optimized for target architecture sm\_90a and may have significantly reduced performance on other targets. Hence, it is advised to be used with compute architecture sm\_90a.

Asynchronous. Data transfers using TMA are asynchronous. This allows the initiating thread to continue computing while the hardware asynchronously copies the data. Whether the data transfer occurs asynchronously in practice is up to the hardware implementation and may change in the future. There are several completion mechanisms that bulk-asynchronous operations can use to signal that they have completed. When the operation reads from global to shared memory, any thread in the block can wait for the data to be readable in shared memory by waiting on a Shared Memory Barrier. When the bulk-asynchronous operation writes data from shared memory to global or distributed shared memory, only the initiating thread can wait for the operation to have completed. This is accomplished using a bulk async-group based completion mechanism. A table describing the completion mechanisms can be found below and in the PTX ISA.

Table 8: Asynchronous copies with possible source and destinations memory spaces and completion mechanisms. An empty cell indicates that a source-destination pair is not supported.

<table><tr><td colspan="2">Direction</td><td colspan="2">Completion mechanism</td></tr><tr><td>Destination</td><td>Source</td><td>Asynchronous copy</td><td>Bulk-asynchronous copy (TMA)</td></tr><tr><td>Global</td><td>Global</td><td></td><td></td></tr><tr><td>Global</td><td>Shared::cta</td><td></td><td>Bulk async-group</td></tr><tr><td>Shared::cta</td><td>Global</td><td>Async-group, mbarrier</td><td>Mbarrier</td></tr><tr><td>Shared::cluster</td><td>Global</td><td></td><td>Mbarrier (multicast)</td></tr><tr><td>Shared::cta</td><td>Shared::cluster</td><td></td><td>Mbarrier</td></tr><tr><td>Shared::cta</td><td>Shared::cta</td><td></td><td></td></tr></table>

## 10.29.1. Using TMA to transfer one-dimensional arrays

This section demonstrates how to write a simple kernel that read-modify-writes a one-dimensional array using TMA. This shows how to how to load and store data using bulk-asynchronous copies, as well as how to synchronize threads of execution with those copies.

The code of the kernel is included below. Some functionality requires inline PTX assembly that is currently made available through libcu++. The availability of these wrappers can be checked with the following code:

```c
#if defined(__CUDA_MINIMUM_ARCH__) && __CUDA_MINIMUM_ARCH__ < 900
static_assert(false, "Device code is being compiled with older architectures that are
    incompatible with TMA.");
#endif // __CUDA_MINIMUM_ARCH__
```

The kernel goes through the following stages:

1. Initialize shared memory barrier.

2. Initiate bulk-asynchronous copy of a block of memory from global to shared memory.

3. Arrive and wait on the shared memory barrier.

4. Increment the shared memory bufer values.

5. Wait for shared memory writes to be visible to the subsequent bulk-asynchronous copy, i.e., order the shared memory writes in the async proxy before the next step.

6. Initiate bulk-asynchronous copy of the bufer in shared memory to global memory.

7. Wait at end of kernel for bulk-asynchronous copy to have finished reading shared memory.

```cpp
#include <cuda/barrier>
#include <cuda/ptx>
using barrier = cuda::barrier<cuda::thread_scope_block>;
namespace ptx = cuda::ptx;

static constexpr size_t buf_len = 1024;
__global__ void add_one_kernel(int* data, size_t offset)
{
    // Shared memory buffer. The destination shared memory buffer of
    // a bulk operations should be 16 byte aligned.
    __shared__ alignas(16) int smem_data[buf_len];

    // 1. a) Initialize shared memory barrier with the number of threads participating in
    the barrier.
    //   b) Make initialized barrier visible in async proxy.
    #pragma nv_diag_suppress static_var_with_dynamic_init
    __shared__ barrier bar;
    if (threadIdx.x == 0) {
        init(&bar, blockDim.x);                  // a)
        ptx::fence_proxy_async(ptx::space_shared);   // b)
    }
    __syncthreads();

    // 2. Initiate TMA transfer to copy global to shared memory.
    if (threadIdx.x == 0) {
        // 3a. cuda::memcpy_async arrives on the barrier and communicates
        //     how many bytes are expected to come in (the transaction count)
        cuda::memcpy_async(
            smem_data,
            data + offset,
            cuda::aligned_size_t<16>(sizeof(smem_data)),
            bar
        );
    }
    // 3b. All threads arrive on the barrier
    barrier::arrival_token token = bar.arrive();

    // 3c. Wait for the data to have arrived.
    bar.wait(std::move(token));

    // 4. Compute saxpy and write back to shared memory
    for (int i = threadIdx.x; i < buf_len; i += blockDim.x) {
        smem_data[i] += 1;
    }

    // 5. Wait for shared memory writes to be visible to TMA engine.
    ptx::fence_proxy_async(ptx::space_shared);   // b)
    __syncthreads();
    // After syncthreads, writes by all threads are visible to TMA engine.

    // 6. Initiate TMA transfer to copy shared memory to global memory
    if (threadIdx.x == 0) {
        ptx::cp_async_bulk(
            ptx::space_global,
            ptx::space_shared,
            data + offset, smem_data, sizeof(smem_data));
```

(continued from previous page)

```rust
// 7. Wait for TMA transfer to have finished reading shared memory.
// Create a "bulk async-group" out of the previous bulk copy operation.
    ptx::cp_async_bulk_commit_group();
    // Wait for the group to have completed reading from shared memory.
    ptx::cp_async_bulk_wait_group_read(ptx::n32_t<0>());
}
}
```

Barrier initialization. The barrier is initialized with the number of threads participating in the block. As a result, the barrier will flip only if all threads have arrived on this barrier. Shared memory barriers are described in more detail in Asynchronous Data Copies using cuda::barrier. To make the initialized barrier visible to subsequent bulk-asynchronous copies, the fence.proxy.async.shared::cta instruction is used. This instruction ensures that subsequent bulk-asynchronous copy operations operate on the initialized barrier.

TMA read. The bulk-asynchronous copy instruction directs the hardware to copy a large chunk of data into shared memory, and to update the transaction count of the shared memory barrier after completing the read. In general, issuing as few bulk copies with as big a size as possible results in the best performance. Because the copy can be performed asynchronously by the hardware, it is not necessary to split the copy into smaller chunks.

The thread that initiates the bulk-asynchronous copy operation arrives at the barrier using mbarrier. expect\_tx. This is automatically performed by cuda::memcpy\_async. This tells the barrier that the thread has arrived and also how many bytes (tx / transactions) are expected to arrive. Only a single thread has to update the expected transaction count. If multiple threads update the transaction count, the expected transaction will be the sum of the updates. The barrier will only flip once all threads have arrived and all bytes have arrived. Once the barrier has flipped, the bytes are safe to read from shared memory, both by the threads as well as by subsequent bulk-asynchronous copies. More information about barrier transaction accounting can be found in the PTX ISA.

Barrier wait. Waiting for the barrier to flip is done using mbarrier.try\_wait. It can either return true, indicating that the wait is over, or return false, which may mean that the wait timed out. The while loop waits for completion, and retries on time-out.

SMEM write and sync. The increment of the bufer values reads and writes to shared memory. To make the writes visible to subsequent bulk-asynchronous copies, the fence.proxy.async.shared::cta instruction is used. This orders the writes to shared memory before subsequent reads from bulkasynchronous copy operations, which read through the async proxy. So each thread first orders the writes to objects in shared memory in the async proxy via the fence.proxy.async.shared::cta, and these operations by all threads are ordered before the async operation performed in thread 0 using \_\_syncthreads().

TMA write and sync. The write from shared to global memory is again initiated by a single thread. The completion of the write is not tracked by a shared memory barrier. Instead, a thread-local mechanism is used. Multiple writes can be batched into a so-called bulk async-group. Afterwards, the thread can wait for all operations in this group to have completed reading from shared memory (as in the code above) or to have completed writing to global memory, making the writes visible to the initiating thread. For more information, refer to the PTX ISA documentation of cp.async.bulk.wait\_group. Note that the bulk-asynchronous and non-bulk asynchronous copy instructions have diferent async-groups: there exist both cp.async.wait\_group and cp.async.bulk.wait\_group instructions.

The bulk-asynchronous instructions have specific alignment requirements on their source and destination addresses. More information can be found in the table below.

Table 9: Alignment requirements for one-dimensional bulkasynchronous operations in Compute Capability 9.0.

<table><tr><td>Address / Size</td><td>Alignment</td></tr><tr><td>Global memory address</td><td>Must be 16 byte aligned.</td></tr><tr><td>Shared memory address</td><td>Must be 16 byte aligned.</td></tr><tr><td>Shared memory barrier address</td><td>Must be 8 byte aligned (this is guaranteed by cuda::barrier).</td></tr><tr><td>Size of transfer</td><td>Must be a multiple of 16 bytes.</td></tr></table>

## 10.29.2. Using TMA to transfer multi-dimensional arrays

The primary diference between the one-dimensional and multi-dimensional case is that a tensor map must be created on the host and passed to the CUDA kernel. This section describes how to create a tensor map using the CUDA driver API, how to pass it to device, and how to use it on device.

Driver API. A tensor map is created using the cuTensorMapEncodeTiled driver API. This API can be accessed by linking to the driver directly (-lcuda) or by using the cudaGetDriverEntryPointByVersion API. Below, we show how to get a pointer to the cuTensorMapEncodeTiled API. For more information, refer to Driver Entry Point Access.

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

Creation. Creating a tensor map requires many parameters. Among them are the base pointer to an array in global memory, the size of the array (in number of elements), the stride from one row to the next (in bytes), the size of the shared memory bufer (in number of elements). The code below creates a tensor map to describe a two-dimensional row-major array of size GMEM\_HEIGHT x GMEM\_WIDTH. Note the order of the parameters: the fastest moving dimension comes first.

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
```

(continues on next page)

```c
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

Host-to-device transfer. There are three ways to make a tensor map accessible to device code. The recommended approach is to pass the tensor map as a const \_\_grid\_constant\_\_ parameter to a kernel. The other possibilities are copying the tensor map into device \_\_constant\_\_ memory using cudaMemcpyToSymbol or accessing it via global memory. When passing the tensor map as a parameter, some versions of the GCC C++ compiler issue the warning “the ABI for passing parameters with 64-byte alignment has changed in GCC 4.6”. This warning can be ignored.

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

As an alternative to the \_\_grid\_constant\_\_ kernel parameter, a global constant variable can be used. An example is included below.

```c
#include <cuda.h>

__constant__ CUtensorMap global_tensor_map;
__global__ void kernel()
```

(continues on next page)

(continued from previous page)

```rust
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

Finally, it is possible to copy the tensor map to global memory. Using a pointer to a tensor map in global device memory requires a fence in each thread block before any thread in the block uses the updated tensor map. Further uses of the tensor map by that thread block do not need to be fenced unless the tensor map is modified again. Note that this mechanism may be slower than the two mechanisms described above.

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

Use. The kernel below loads a 2D tile of size SMEM\_HEIGHT x SMEM\_WIDTH from a larger 2D array. The top-left corner of the tile is indicated by the indices x and y. The tile is loaded into shared memory, modified, and written back to global memory.

```cpp
#include <cuda.h>          // CUtensormap
#include <cuda/barrier>
using barrier = cuda::barrier<cuda::thread_scope_block>;
namespace cde = cuda::device::experimental;

__global__ void kernel(const __grid_constant__ CUtensorMap tensor_map, int x, int y) {
  // The destination shared memory buffer of a bulk tensor operation should be
  // 128 byte aligned.
  __shared__ alignas(128) int smem_buffer[SMEM_HEIGHT][SMEM_WIDTH];

  // Initialize shared memory barrier with the number of threads participating in the
  barrier.
```

(continues on next page)

```cpp
#pragma nv_diag_suppress static_var_with_dynamic_init
__shared__ barrier bar;

if (threadIdx.x == 0) {
    // Initialize barrier. All `blockDim.x` threads in block participate.
    init(&bar, blockDim.x);
    // Make initialized barrier visible in async proxy.
    cde::fence_proxy_async_shared_cta();
}
// Syncthreads so initialized barrier is visible to all threads.
__syncthreads();

barrier::arrival_token token;
if (threadIdx.x == 0) {
    // Initiate bulk tensor copy.
    cde::cp_async_bulk_tensor_2d_global_to_shared(&smem_buffer, &tensor_map, x, y,
    bar);
    // Arrive on the barrier and tell how many bytes are expected to come in.
    token = cuda::device::barrier_arrive_tx(bar, 1, sizeof(smem_buffer));
} else {
    // Other threads just arrive.
    token = bar.arrive();
}
// Wait for the data to have arrived.
bar.wait(std::move(token));

// Symbolically modify a value in shared memory.
smem_buffer[0][threadIdx.x] += threadIdx.x;

// Wait for shared memory writes to be visible to TMA engine.
cde::fence_proxy_async_shared_cta();
__syncthreads();
// After syncthreads, writes by all threads are visible to TMA engine.

// Initiate TMA transfer to copy shared memory to global memory
if (threadIdx.x == 0) {
    cde::cp_async_bulk_tensor_2d_shared_to_global(&tensor_map, x, y, &smem_buffer);
    // Wait for TMA transfer to have finished reading shared memory.
    // Create a "bulk async-group" out of the previous bulk copy operation.
    cde::cp_async_bulk_commit_group();
    // Wait for the group to have completed reading from shared memory.
    cde::cp_async_bulk_wait_group_read<0>();
}

// Destroy barrier. This invalidates the memory region of the barrier. If
// further computations were to take place in the kernel, this allows the
// memory location of the shared memory barrier to be reused.
if (threadIdx.x == 0) {
    (&bar)->~barrier();
}
}
```
````
