# cluster_group

The `cluster_group` class represents all threads launched in a single cluster [CUDA_C_Programming_Guide:L12111-L12113]. This API is available on all hardware with Compute Capability 9.0+ [CUDA_C_Programming_Guide:L12113]. When a non-cluster grid is launched on such hardware, the APIs assume a 1x1x1 cluster [CUDA_C_Programming_Guide:L12113].

## Construction

A `cluster_group` object is constructed via the `this_cluster()` function [CUDA_C_Programming_Guide:L12115-L12117]:

```cpp
class cluster_group;

cluster_group g = this_cluster();
```

## Public Member Functions

### Synchronization

*   `static void sync()`: Synchronizes the threads named in the group. This is equivalent to calling `g.barrier_wait(g.barrier_arrive())` [CUDA_C_Programming_Guide:L12119-L12120].
*   `static cluster_group::arrival_token barrier_arrive()`: Arrives on the cluster barrier and returns a token that must be passed into `barrier_wait()` [CUDA_C_Programming_Guide:L12121-L12122].
*   `static void barrier_wait(cluster_group::arrival_token&& t)`: Waits on the cluster barrier, taking the arrival token returned from `barrier_arrive()` as an rvalue reference [CUDA_C_Programming_Guide:L12123-L12124].

### Ranking and Dimensions

*   `static unsigned int thread_rank()`: Returns the rank of the calling thread within the range `[0, num_threads)` [CUDA_C_Programming_Guide:L12126-L12127].
*   `static unsigned int block_rank()`: Returns the rank of the calling block within the range `[0, num_blocks)` [CUDA_C_Programming_Guide:L12128-L12129].
*   `static unsigned int num_threads()`: Returns the total number of threads in the group [CUDA_C_Programming_Guide:L12130-L12131].
*   `static unsigned int num_blocks()`: Returns the total number of blocks in the group [CUDA_C_Programming_Guide:L12132-L12133].
*   `static dim3 dim_threads()`: Returns the dimensions of the launched cluster in units of threads [CUDA_C_Programming_Guide:L12134-L12135].
*   `static dim3 dim_blocks()`: Returns the dimensions of the launched cluster in units of blocks [CUDA_C_Programming_Guide:L12136-L12137].
*   `static dim3 block_index()`: Returns the 3-dimensional index of the calling block within the launched cluster [CUDA_C_Programming_Guide:L12138-L12139].

### Shared Memory

*   `static unsigned int query_shared_rank(const void *addr)`: Obtains the block rank to which a shared memory address belongs [CUDA_C_Programming_Guide:L12141-L12142].
*   `static T* map_shared_rank(T *addr, int rank)`: Obtains the address of a shared memory variable of another block in the cluster [CUDA_C_Programming_Guide:L12143-L12144].

## Legacy Aliases

*   `static unsigned int size()`: Total number of threads in the group. This is an alias for `num_threads()` [CUDA_C_Programming_Guide:L12146-L12147].

## See Also

*   [Grid Group](entity/grid-group)
