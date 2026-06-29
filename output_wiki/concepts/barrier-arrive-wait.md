# barrier_arrive and barrier_wait

`barrier_arrive` and `barrier_wait` are member functions that provide a synchronization API similar to `cuda::barrier` within Cooperative Groups [CUDA_C_Programming_Guide:L12566-L12616]. These functions allow threads to perform independent work after arriving at a barrier and before waiting for the synchronization to resolve, thereby hiding synchronization latency [CUDA_C_Programming_Guide:L12566-L12616].

## API

The functions are defined as follows:

```c
T::arrival_token T::barrier_arrive();
void T::barrier_wait(T::arrival_token&&);
```

Where `T` is the group type, which can be any of the implicit groups [CUDA_C_Programming_Guide:L12566-L12616].

## Usage and Semantics

### Arrival Token
`barrier_arrive` returns an `arrival_token` object that must be passed into the corresponding `barrier_wait` call [CUDA_C_Programming_Guide:L12566-L12616]. The token is consumed upon use and cannot be used for another `barrier_wait` call [CUDA_C_Programming_Guide:L12566-L12616].

### Collective Restrictions
Due to the collective nature of these operations, all threads in the group must call both `barrier_arrive` and `barrier_wait` once per phase [CUDA_C_Programming_Guide:L12566-L12616]. Cooperative Groups automatically initializes the group barrier [CUDA_C_Programming_Guide:L12566-L12616].

### Undefined Behavior
If `barrier_arrive` is called with a group, the result of calling any collective operation or another barrier arrival with that group is undefined until the completion of the barrier phase is observed with a `barrier_wait` call [CUDA_C_Programming_Guide:L12566-L12616].

### Release Conditions
Threads blocked on `barrier_wait` might be released from the synchronization before other threads call `barrier_wait`, but only after all threads in the group have called `barrier_arrive` [CUDA_C_Programming_Guide:L12566-L12616].

## Example

The following example demonstrates using `barrier_arrive` and `barrier_wait` to synchronize the initialization of shared memory across a cluster:

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

    cluster.sync();
}
```

In this example, `barrier_arrive` is called to signal that the block has initialized its shared data. The block then performs local processing to hide the latency of waiting for other blocks. Finally, `barrier_wait` is called with the token to ensure all blocks in the cluster have arrived before accessing the distributed shared memory mapped from the next block. The example concludes with `cluster.sync()` to ensure the cluster synchronization is complete [CUDA_C_Programming_Guide:L12566-L12616].
