## 11.7. Grid Synchronization

Prior to the introduction of Cooperative Groups, the CUDA programming model only allowed synchronization between thread blocks at a kernel completion boundary. The kernel boundary carries with it an implicit invalidation of state, and with it, potential performance implications.

For example, in certain use cases, applications have a large number of small kernels, with each kernel representing a stage in a processing pipeline. The presence of these kernels is required by the current CUDA programming model to ensure that the thread blocks operating on one pipeline stage have produced data before the thread block operating on the next pipeline stage is ready to consume it. In such cases, the ability to provide global inter thread block synchronization would allow the application to be restructured to have persistent thread blocks, which are able to synchronize on the device when a given stage is complete.

To synchronize across the grid, from within a kernel, you would simply use the grid.sync() function:

```javascript
grid_group grid = this_grid();
grid.sync();
```

And when launching the kernel it is necessary to use, instead of the <<<...>>> execution configuration syntax, the cudaLaunchCooperativeKernel CUDA runtime launch API or the CUDA driver equivalent.

## Example:

To guarantee co-residency of the thread blocks on the GPU, the number of blocks launched needs to be carefully considered. For example, as many blocks as there are SMs can be launched as follows:

```javascript
int dev = 0;
cudaDeviceProp deviceProp;
cudaGetDeviceProperties(&deviceProp, dev);
// initialize, then launch
cudaLaunchCooperativeKernel((void*)my_kernel, deviceProp.multiProcessorCount,
→ numThreads, args);
```

Alternatively, you can maximize the exposed parallelism by calculating how many blocks can fit simultaneously per-SM using the occupancy calculator as follows:

```c
/// This will launch a grid that can maximally fill the GPU, on the default stream with
kernel arguments
int numBlocksPerSm = 0;
// Number of threads my_kernel will be launched with
int numThreads = 128;
cudaDeviceProp deviceProp;
cudaGetDeviceProperties(&deviceProp, dev);
cudaOccupancyMaxActiveBlocksPerMultiprocessor(&numBlocksPerSm, my_kernel, numThreads,
→0);
// launch
void *kernelArgs[] = { /* add kernel args */ };
dim3 dimBlock(numThreads, 1, 1);
dim3 dimGrid(deviceProp.multiProcessorCount*numBlocksPerSm, 1, 1);
cudaLaunchCooperativeKernel((void*)my_kernel, dimGrid, dimBlock, kernels);
```

It is good practice to first ensure the device supports cooperative launches by querying the device attribute cudaDevAttrCooperativeLaunch:

```javascript
int dev = 0;
int supportsCoopLaunch = 0;
cudaDeviceGetAttribute(&supportsCoopLaunch, cudaDevAttrCooperativeLaunch, dev);
```

which will set supportsCoopLaunch to 1 if the property is supported on device 0. Only devices with compute capability of 6.0 and higher are supported. In addition, you need to be running on either of these:

▶ The Linux platform without MPS

▶ The Linux platform with MPS and on a device with compute capability 7.0 or higher

The latest Windows platform

# Chapter 12. Cluster Launch Control

Warning: This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA.

## 12.1. Introduction

Compute Capability 10.0 introduces Cluster Launch Control, a new feature that provides developer with more control over thread block scheduling by cancelling thread blocks or thread block clusters.

When dealing with problems of variable size, there are two main approaches to determining the number of kernel thread blocks.

## Approach 1: Fixed Work per Thread Block:

In this approach, the number of thread blocks is determined by the problem size, while the amount of work done by each thread block remains constant or is limited.

Key advantages of this approach:

▶ Load balancing between SMs.

In particular, when thread block run-times exhibit variability and/or when the number of thread blocks is much larger than what the GPU can execute simultaneously (resulting in a low-tail effect), this approach allows the GPU scheduler to run more thread blocks on some SMs than others.

▶ Preemption.

The GPU scheduler can start executing a higher-priority kernel, even if it is launched after the execution of a lower-priority kernel has already begun, by scheduling the higher-priority kernel’s thread blocks as the currently running lower-priority kernel’s thread blocks finish. It can then return to the lower-priority kernel once the higher-priority kernel has finished.

## Approach 2: Fixed Number of Thread Blocks:

In this approach, often implemented as a block-stride or grid-stride loop, the number of thread blocks does not directly depend on the problem size. Instead, the amount of work done by each thread block is a function of the problem size. Typically, the number of thread blocks is based on the number of SMs on the GPU where the kernel is executed and the desired occupancy.

Key advantage of this approach:

▶ Reduced thread block overheads.

This approach not only reduces amortized thread block launch latency but also minimizes the computational overhead associated with shared operations across all thread blocks. These overheads can be significantly higher than launch latency overheads.

For example, in convolution kernels, a prologue for calculating convolution coeficients – independent of the thread block index – can be computed fewer times due to the fixed number of thread blocks, thus reducing redundant computations.

## Cluster Launch Control Approach:

Cluster Launch Control allows a kernel to request (cancel) the thread block index of a block that has not yet started execution.

This mechanism enables work-stealing among thread blocks: a thread block attempts to cancel the launch of another thread block that has not started running yet. If cancellation succeeds, it “steals” the other thread block’s work by using cancelled block index to perform the task.

The cancellation will fail if there are no more thread block indices available and may fail for other reasons, such as a higher-priority kernel being scheduled. In the latter case, if a thread block exits after a cancellation failure, the scheduler can start executing the higher-priority kernel, after which it will continue scheduling the remaining thread blocks of the current kernel for execution.

The table below summarizes advantages and disadvantages of the three approaches:

<table><tr><td></td><td>Fixed Work per Thread Block</td><td>Fixed Number of Thread Blocks</td><td>Cluster Launch Control</td></tr><tr><td>Reduced overheads</td><td>X</td><td>V</td><td>V</td></tr><tr><td>Preemption</td><td>V</td><td>X</td><td>V</td></tr><tr><td>Load balancing</td><td>V</td><td>X</td><td>V</td></tr></table>

## 12.2. Cluster Launch Control API Details

Cancelling a thread block via the Cluster Launch Control API is done asynchronously and synchronized using a memory barrier, following a programming pattern similar to asynchronous data copies.

The API, currently available through libcu++, provides a request instruction that writes the encoded cancellation result into a \_\_shared\_\_ variable, along with instructions to decode the result into a Success/Fail flag and the index of the cancelled thread block in case of Success.

## 12.2.1. Thread block cancellation steps

The preferred way to use Cluster Launch Control is from a single thread, i.e., one request at a time.

The following are the five steps of the thread block cancellation process. The first two steps are declarations and initialization of cancellation result and synchronization variables, which are done before the work-stealing. The last three steps are typically executed inside a work-stealing loop over thread block indices.

1. Declare variables for thread block cancellation:

```txt
__shared__ uint4 result; // Request result.
__shared__ uint64_t bar; // Synchronization barrier.
int phase = 0;          // Synchronization barrier phase.
```

2. Initialize shared memory barrier with a single arrival count:

```txt
if (cg::thread_block::thread_rank() == 0)
    ptx::mbarrier_init(&bar, 1);
__syncthreads();
```

3. Submit asynchronous cancellation request by a single thread and set transaction count:

```cpp
if (cg::thread_block::thread_rank() == 0) {
    cg::invoke_one(cg::coalesced_threads(), ptx::clusterlaunchcontrol_try_cancel,
        &result, &bar);
    ptx::mbarrier_arrive_expect_tx(ptx::sem_relaxed, ptx::scope_cta, ptx::space_
        shared, &bar, sizeof(uint4));
}
```

Note: Since thread block cancellation is a uniform instruction, it is recommended to submit it inside invoke\_one thread selector. This allows the compliler to optimize out the peeling loop.

4. Synchronize (complete) asynchronous cancellation request:

```txt
while (!ptx::mbarrier_try_wait_parity(&bar, phase))
{}
phase ^= 1;
```

5. Retrieve cancellation status and cancelled thread block index:

```cpp
bool success = ptr::clusterlaunchcontrol_query_cancel_is_canceled(result);
if (success) {
    // Don't need all three for 1D/2D thread blocks:
    int bx = ptr::clusterlaunchcontrol_query_cancel_get_first_ctaid_x(result);
    int by = ptr::clusterlaunchcontrol_query_cancel_get_first_ctaid_y(result);
    int bz = ptr::clusterlaunchcontrol_query_cancel_get_first_ctaid_z(result);
}
```

6. Ensure visibility of shared memory operations between async and generic proxies, and protect against data races between iterations of the work-stealing loop.

## 12.2.2. Thread block cancellation constraints

The constraints are related to failed cancellation requests:

▶ Submitting another cancellation request after observing a previously failed request is Undefined Behavior.

In the two code examples below, assuming the first cancellation request fails, only the first example exhibits undefined behavior. The second example is correct because there is no observation between the cancellation requests:

## Invalid code:

```cpp
// First request:
ptx::clusterlaunchcontrol_try_cancel(&result0, &bar0);

// First request query:
[Synchronize bar0 code here."]
bool success0 = ptx::clusterlaunchcontrol_query_cancel_is_canceled(result0);
assert(!success0); // Observed failure; second cancellation will be invalid.

// Second request - next line is Undefined Behavior:
ptx::clusterlaunchcontrol_try_cancel(&result1, &bar1);
```

## Valid code:

```cpp
// First request:
ptx::clusterlaunchcontrol_try_cancel(&result0, &bar0);

// Second request:
ptx::clusterlaunchcontrol_try_cancel(&result1, &bar1);

// First request query:
[Synchronize bar0 code here."]
bool success0 = ptx::clusterlaunchcontrol_query_cancel_is_canceled(result0);
assert(!success0); // Observed failure; second cancellation was valid.
```

▶ Retrieving the thread block index of a failed cancellation request is Undefined Behavior.

▶ Submitting a cancellation request from multiple threads is not recommended. It results in the cancellation of multiple thread blocks and requires careful handling, such as:

▶ Each submitting thread must proivde a unique \_\_shared\_\_ result pointer to avoid data races.

If the same barrier is used for synchronization, the arrival and transaction counts must be adjusted accordingly.

## 12.2.3. Kernel Example: Vector-Scalar Multiplication

The three kernels below demonstrate the Fixed Work per Thread Block, Fixed Number of Thread Blocks, and Cluster Launch Control approaches for vector-scalar multiplication v := αv.

## ▶ Fixed Work per Thread Block:

```c
__global__
void kernel_fixed_work (float* data, int n)
{
    // Prologue:
    float alpha = compute_scalar();

    // Computation:
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n)
        data[i] *= alpha;
}

// Launch: kernel_fixed_work<<<1024, (n + 1023) / 1024>>>(data, n);
```

## ▶ Fixed Number of Thread Blocks:

```cpp
__global__
void kernel_fixed_blocks (float* data, int n)
{
    // Prologue:
    float alpha = compute_scalar();

    // Computation:
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    while (i < n) {
        data[i] *= alpha;
        i += gridDim.x * blockDim.x;
    }
}

// Launch: kernel_fixed_blocks<<<1024, SM_COUNT>>>(data, n);
```

## Cluster Launch Control:

```cpp
#include <cooperative_groups.h>
#include <cuda/ptx>

namespace cg = cooperative_groups;
namespace ptx = cuda::ptx;

__global__
void kernel_cluster_launch_control (float* data, int n)
{
    // Cluster launch control initialization:
    __shared__ uint4 result;
    __shared__ uint64_t bar;
    int phase = 0;

    if (cg::thread_block::thread_rank() == 0)
        ptx::mbarrier_init(&bar, 1);
```

(continues on next page)

```cpp
// Prologue:
float alpha = compute_scalar(); // Device function not shown in this code
snippet.

// Work-stealing loop:
int bx = blockIdx.x; // Assuming 1D x-axis thread blocks.

while (true) {
    // Protect result from overwrite in the next iteration,
    // (also ensure barrier initialization at 1st iteration):
    __syncthreads();

    // Cancellation request:
    if (cg::thread_block::thread_rank() == 0) {
        // Acquire write of result in the async proxy:
        ptx::fence_proxy_async_generic_sync_restrict(ptx::sem_acquire,
            ptx::space_cluster, ptx::scope_cluster);

        cg::invoke_one(cg::coalesced_threads(), [&]()
        {ptx::clusterlaunchcontrol_try_cancel(&result, &bar);});
        ptx::mbarrier_arrive_expect_tx(ptx::sem_relaxed, ptx::scope_cta,
            ptx::space_shared, &bar, sizeof(uint4));
    }

    // Computation:
    int i = bx * blockDim.x + threadIdx.x;
    if (i < n)
        data[i] *= alpha;

    // Cancellation request synchronization:
    while (!ptx::mbarrier_try_wait_parity(ptx::sem_acquire, ptx::scope_cta, &
            bar, phase))
    {}
    phase ^= 1;

    // Cancellation request decoding:
    bool success = ptx::clusterlaunchcontrol_query_cancel_is_canceled(result);
    if (!success)
        break;

    bx = ptx::clusterlaunchcontrol_query_cancel_get_first_ctaid_x<int>
        (result);

    // Release read of result to the async proxy:
    ptx::fence_proxy_async_generic_sync_restrict(ptx::sem_release, ptx::space_
            shared, ptx::scope_cluster);
}
}

// Launch: kernel_cluster_launch_control<<<1024, (n + 1023) / 1024>>>(data, n);
```

## 12.2.4. Cluster Launch Control for Thread Block Clusters

In the case of a thread block clusters, the thread block cancellation steps are the same as in a noncluster setting, with minor adjustments. As in the non-cluster case, submitting a cancellation request from multiple threads within a cluster is not recommended, as this will attempt to cancel multiple clusters.

▶ The cancellation is submitted by a single cluster thread.

The shared memory result of each cluster’s thread block will receive the same (encoded) value of the cancelled thread block index (i.e., the result value is multicasted). The result received by all thread blocks corresponds to the local block index {0, 0, 0} within a cluster. Therefore, thread blocks within the cluster need to add the local block index.

Synchronization is performed by each cluster’s thread block using a local \_\_shared\_\_ memory barrier. Barrier operations must be performed with the ptx::scope\_cluster scope.

▶ Cancelling in the cluster case requires all the thread blocks to exist. A user can guarantee that all thread blocks are running by using cg::cluster\_group::sync() from Cluster Group API.

The kernel below demonstrates Cluster Launch Control approach in a thread block cluster case:

```cpp
#include <cooperative_groups.h>
#include <cuda/ptx>

namespace cg = cooperative_groups;
namespace ptx = cuda::ptx;

__global__ __cluster_dims__(2, 1, 1)
void kernel_cluster_launch_control (float* data, int n)
{
    // Cluster launch control initialization:
    __shared__ uint4 result;
    __shared__ uint64_t bar;
    int phase = 0;

    if (cg::thread_block::thread_rank() == 0) {
        ptx::mbarrier_init(&bar, 1);
        ptx::fence_mbarrier_init(ptx::sem_release, ptx::scope_cluster); // CGA-level fence.
    }

    // Prologue:
    float alpha = compute_scalar(); // Device function not shown in this code snippet.

    // Work-stealing loop:
    int bx = blockIdx.x; // Assuming 1D x-axis thread blocks.

    while (true) {
        // Protect result from overwrite in the next iteration,
        // (also ensure all thread blocks have started at 1st iteration):
        cg::cluster_group::sync();

        // Cancellation request by a single cluster thread:
        if (cg::cluster_group::thread_rank() == 0) {
            // Acquire write of result in the async proxy:
            ptx::fence_proxy_async_generic_sync_restrict(ptx::sem_acquire, ptx::space_cluster, ptx::scope_cluster);
```

```cpp
cg::invoke_one(cg::coalesced_threads(), [&](){ptx::clusterlaunchcontrol_try_cancel_multicast(&result, &bar);});
    }

    // Cancellation completion tracked by each thread block:
    if (cg::thread_block::thread_rank() == 0)
        ptx::mbarrier_arrive_expect_tx(ptx::sem_relaxed, ptx::scope_cluster, ptx::space_shared, &bar, sizeof(uint4));

    // Computation:
    int i = bx * blockDim.x + threadIdx.x;
    if (i < n)
        data[i] *= alpha;

    // Cancellation request synchronization:
    while (!ptx::mbarrier_try_wait_parity(ptx::sem_acquire, ptx::scope_cluster, &bar, phase))
    {}
    phase ^= 1;

    // Cancellation request decoding:
    bool success = ptx::clusterlaunchcontrol_query_cancel_is_canceled(result);
    if (!success)
        break;

    bx = ptx::clusterlaunchcontrol_query_cancel_get_first_ctaid_x<int>(result);
    bx += cg::cluster_group::block_index().x; // Add local offset.

    // Release read of result to the async proxy:
    ptx::fence_proxy_async_generic_sync_restrict(ptx::sem_release, ptx::space_shared, ptx::scope_cluster);
    }
}

// Launch: kernel_cluster_launch_control<<<1024, (n + 1023) / 1024>>>(data, n);
```
