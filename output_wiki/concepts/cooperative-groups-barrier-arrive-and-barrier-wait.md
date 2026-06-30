# barrier_arrive and barrier_wait

Synchronization API functions that provide a barrier mechanism for cooperative groups. barrier_arrive returns an arrival_token, and barrier_wait consumes it to synchronize threads. Allows independent work between arrive and wait to hide synchronization latency.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L12565-L12616

Citation: [CUDA_C_Programming_Guide:L12565-L12616]

````text

## 11.6.1. Synchronization

11.6.1.1 barrier\_arrive and barrier\_wait

```c
T::arrival_token T::barrier_arrive();
void T::barrier_wait(T::arrival_token&&);
```

barrier\_arrive and barrier\_wait member functions provide a synchronization API similar to cuda::barrier (read more). Cooperative Groups automatically initializes the group barrier, but arrive and wait operations have an additional restriction resulting from collective nature of those operations: All threads in the group must arrive and wait at the barrier once per phase. When barrier\_arrive is called with a group, result of calling any collective operation or another barrier arrival with that group is undefined until completion of the barrier phase is observed with barrier\_wait call. Threads blocked on barrier\_wait might be released from the synchronization before other threads call barrier\_wait, but only after all threads in the group called barrier\_arrive. Group type T can be any of the implicit groups.This allows threads to do independent work after they arrive and before they wait for the synchronization to resolve, allowing to hide some of the synchronization latency. barrier\_arrive returns an arrival\_token object that must be passed into the corresponding barrier\_wait. Token is consumed this way and can not be used for another barrier\_wait call.

Example of barrier\_arrive and barrier\_wait used to synchronize initalization of shared memory across the cluster:

```cpp
#include <cooperative_groups.h>

using namespace cooperative_groups;

void __device__ init_shared_data(const thread_block& block, int *data);
void __device__ local_processing(const thread_block& block);
void __device__ process_shared_data(const thread_block& block, int *data);

__global__ void cluster_kernel() {
    extern __shared__ int array[];
    auto cluster = this_cluster();
    auto block = this_thread_block();

    // Use this thread block to initialize some shared state
    init_shared_data(block, &array[0]);

    auto token = cluster.barrier_arrive(); // Let other blocks know this block is running and data was initialized

    // Do some local processing to hide the synchronization latency
    local_processing(block);

    // Map data in shared memory from the next block in the cluster
    int *dsmem = cluster.map_shared_rank(&array[0], (cluster.block_rank() + 1) % cluster.num_blocks());

    // Make sure all other blocks in the cluster are running and initialized shared data before accessing dsmem
    cluster.barrier_wait(std::move(token));

    // Consume data in distributed shared memory
    process_shared_data(block, dsmem);
```

(continues on next page)

```txt
cluster.sync();
}
```
````
