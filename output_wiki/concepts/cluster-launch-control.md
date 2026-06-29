# Cluster Launch Control

Cluster Launch Control is a feature introduced in Compute Capability 10.0 that provides developers with finer control over thread block scheduling by allowing the cancellation of thread blocks or thread block clusters [CUDA_C_Programming_Guide:L13272-L13314]. This mechanism enables "work-stealing," where a running thread block can cancel the launch of another thread block that has not yet started execution, effectively "stealing" its assigned work [CUDA_C_Programming_Guide:L13272-L13314].

## Overview and Scheduling Approaches

When dealing with problems of variable size, developers typically choose between two main approaches for determining the number of kernel thread blocks. Cluster Launch Control offers a third approach that combines benefits of the first two.

### Fixed Work per Thread Block
In this traditional approach, the number of thread blocks is determined by the problem size, while the amount of work done by each thread block remains constant or is limited [CUDA_C_Programming_Guide:L13272-L13314].
*   **Advantages:** Provides load balancing between Streaming Multiprocessors (SMs) and supports preemption by the GPU scheduler [CUDA_C_Programming_Guide:L13272-L13314].
*   **Disadvantages:** High overheads due to the large number of thread block launches required for large problem sizes [CUDA_C_Programming_Guide:L13272-L13314].

### Fixed Number of Thread Blocks
In this approach, often implemented using a block-stride or grid-stride loop, the number of thread blocks does not depend on the problem size but rather on the number of SMs and desired occupancy [CUDA_C_Programming_Guide:L13272-L13314].
*   **Advantages:** Significantly reduces thread block overheads, including amortized launch latency and computational overheads for shared operations (e.g., computing convolution coefficients) [CUDA_C_Programming_Guide:L13272-L13314].
*   **Disadvantages:** Lacks load balancing and preemption capabilities [CUDA_C_Programming_Guide:L13272-L13314].

### Cluster Launch Control Approach
Cluster Launch Control allows a kernel to request the cancellation of a thread block index that has not yet started execution [CUDA_C_Programming_Guide:L13272-L13314].
*   **Mechanism:** A thread block attempts to cancel the launch of another thread block. If successful, it uses the cancelled block's index to perform the task [CUDA_C_Programming_Guide:L13272-L13314].
*   **Failure Conditions:** Cancellation may fail if no thread block indices are available or if a higher-priority kernel is scheduled [CUDA_C_Programming_Guide:L13272-L13314]. If a cancellation fails, the thread block exits, allowing the scheduler to execute the higher-priority kernel before resuming the current kernel [CUDA_C_Programming_Guide:L13272-L13314].
*   **Advantages:** Combines reduced overheads (like Fixed Number of Thread Blocks) with load balancing and preemption (like Fixed Work per Thread Block) [CUDA_C_Programming_Guide:L13272-L13314].

| Feature | Fixed Work per Thread Block | Fixed Number of Thread Blocks | Cluster Launch Control |
| :--- | :---: | :---: | :---: |
| Reduced Overheads | X | V | V |
| Preemption | V | X | V |
| Load Balancing | V | X | V |

## API Details and Usage

The Cluster Launch Control API is available through `libcu++` and operates asynchronously, synchronized using a memory barrier [CUDA_C_Programming_Guide:L13315-L13326]. The API writes an encoded cancellation result into a `__shared__` variable, which can be decoded into a success/fail flag and the index of the cancelled thread block [CUDA_C_Programming_Guide:L13315-L13326].

### Thread Block Cancellation Steps
The preferred usage pattern involves a single thread submitting a request at a time [CUDA_C_Programming_Guide:L13315-L13326]. The process consists of five steps:

1.  **Declare Variables:** Declare shared memory variables for the result, a synchronization barrier, and a phase counter [CUDA_C_Programming_Guide:L13327-L13334].
    ```cpp
    __shared__ uint4 result; // Request result.
    __shared__ uint64_t bar; // Synchronization barrier.
    int phase = 0;           // Synchronization barrier phase.
    ```

2.  **Initialize Barrier:** Initialize the shared memory barrier with an arrival count of 1, typically executed by thread 0 [CUDA_C_Programming_Guide:L13335-L13342].
    ```cpp
    if (cg::thread_block::thread_rank() == 0)
        ptx::mbarrier_init(&bar, 1);
    __syncthreads();
    ```

3.  **Submit Request:** Submit an asynchronous cancellation request using `cg::invoke_one` to optimize the compiler's peeling loop, followed by `ptx::mbarrier_arrive_expect_tx` to set the transaction count [CUDA_C_Programming_Guide:L13343-L13355].
    ```cpp
    if (cg::thread_block::thread_rank() == 0) {
        cg::invoke_one(cg::coalesced_threads(), ptx::clusterlaunchcontrol_try_cancel,
            &result, &bar);
        ptx::mbarrier_arrive_expect_tx(ptx::sem_relaxed, ptx::scope_cta, ptx::space_shared,
            &bar, sizeof(uint4));
    }
    ```

4.  **Synchronize:** Wait for the asynchronous request to complete using `ptx::mbarrier_try_wait_parity` [CUDA_C_Programming_Guide:L13356-L13362].
    ```cpp
    while (!ptx::mbarrier_try_wait_parity(&bar, phase)) {}
    phase ^= 1;
    ```

5.  **Retrieve Status:** Query the result to determine if the cancellation was successful and retrieve the cancelled thread block's index [CUDA_C_Programming_Guide:L13363-L13375].
    ```cpp
    bool success = ptr::clusterlaunchcontrol_query_cancel_is_canceled(result);
    if (success) {
        int bx = ptr::clusterlaunchcontrol_query_cancel_get_first_ctaid_x(result);
        int by = ptr::clusterlaunchcontrol_query_cancel_get_first_ctaid_y(result);
        int bz = ptr::clusterlaunchcontrol_query_cancel_get_first_ctaid_z(result);
    }
    ```

### Important Constraints
*   **Undefined Behavior:** Submitting a new cancellation request after observing a previously failed request is undefined behavior [CUDA_C_Programming_Guide:L13382-L13415]. Requests must be submitted in batches or without intermediate observation of failure [CUDA_C_Programming_Guide:L13382-L13415].
*   **Multiple Threads:** Submitting cancellation requests from multiple threads is not recommended as it cancels multiple thread blocks and requires unique shared memory result pointers and adjusted barrier counts to avoid data races [CUDA_C_Programming_Guide:L13418-L13445].

## Kernel Example: Vector-Scalar Multiplication

The following example demonstrates the Cluster Launch Control approach for vector-scalar multiplication (`v := αv`), integrating the initialization, prologue, and work-stealing loop [CUDA_C_Programming_Guide:L13466-L13542].

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

    // Prologue:
    float alpha = compute_scalar(); // Device function not shown

    // Work-stealing loop:
    int bx = blockIdx.x; // Assuming 1D x-axis thread blocks

    while (true) {
        // Protect result from overwrite in the next iteration,
        // (also ensure barrier initialization at 1st iteration):
        __syncthreads();

        // Cancellation request:
        if (cg::thread_block::thread_rank() == 0) {
            // Acquire write of result in the async proxy:
            ptx::fence_proxy_async_generic_sync_restrict(ptx::sem_acquire,
                ptx::space_cluster, ptx::scope_cluster);

            cg::invoke_one(cg::coalesced_threads(), [&]() {
                ptx::clusterlaunchcontrol_try_cancel(&result, &bar);
            });
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

## Cluster Launch Control for Thread Block Clusters

When using thread block clusters, the cancellation steps are similar but require adjustments for cluster-level synchronization and indexing [CUDA_C_Programming_Guide:L13543-L13627].

*   **Submission:** Cancellation is submitted by a single cluster thread using `ptx::clusterlaunchcontrol_try_cancel_multicast` [CUDA_C_Programming_Guide:L13543-L13627].
*   **Synchronization:** Each cluster's thread block uses a local `__shared__` memory barrier with `ptx::scope_cluster` [CUDA_C_Programming_Guide:L13543-L13627]. All thread blocks must exist, which can be guaranteed using `cg::cluster_group::sync()` [CUDA_C_Programming_Guide:L13543-L13627].
*   **Indexing:** The shared memory result is multicast to all thread blocks in the cluster. The retrieved index corresponds to the local block index `{0, 0, 0}` within the cluster, so thread blocks must add their local block index to the result [CUDA_C_Programming_Guide:L13543-L13627].

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
    float alpha = compute_scalar(); // Device function not shown

    // Work-stealing loop:
    int bx = blockIdx.x; // Assuming 1D x-axis thread blocks

    while (true) {
        // Protect result from overwrite in the next iteration,
        // (also ensure all thread blocks have started at 1st iteration):
        cg::cluster_group::sync();

        // Cancellation request by a single cluster thread:
        if (cg::cluster_group::thread_rank() == 0) {
            // Acquire write of result in the async proxy:
            ptx::fence_proxy_async_generic_sync_restrict(ptx::sem_acquire, ptx::space_cluster, ptx::scope_cluster);

            cg::invoke_one(cg::coalesced_threads(), [&](){
                ptx::clusterlaunchcontrol_try_cancel_multicast(&result, &bar);
            });
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
