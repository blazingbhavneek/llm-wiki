# grid_group

The `grid_group` class represents all the threads launched in a single grid. It is constructed using the `this_grid()` function.

```cpp
group_group g = this_grid();
```

## Synchronization

While APIs other than `sync()` are available at all times, the ability to synchronize across the grid requires the use of the cooperative launch API [CUDA_C_Programming_Guide:L12154-L12201].

### Public Member Functions

*   `bool is_valid() const`: Returns whether the `grid_group` can synchronize [CUDA_C_Programming_Guide:L12154-L12201].
*   `void sync() const`: Synchronizes the threads named in the group. This is equivalent to `g.barrier_wait(g.barrier_arrive())` [CUDA_C_Programming_Guide:L12154-L12201].
*   `grid_group::arrival_token barrier_arrive()`: Arrives on the grid barrier and returns a token that must be passed into `barrier_wait()` [CUDA_C_Programming_Guide:L12154-L12201].
*   `void barrier_wait(grid_group::arrival_token&& t)`: Waits on the grid barrier, taking the arrival token returned from `barrier_arrive()` as an rvalue reference [CUDA_C_Programming_Guide:L12154-L12201].

### Static Member Functions

The following static functions provide information about the grid topology and thread/block/cluster ranks:

*   `static unsigned long long thread_rank()`: Rank of the calling thread within `[0, num_threads)` [CUDA_C_Programming_Guide:L12154-L12201].
*   `static unsigned long long block_rank()`: Rank of the calling block within `[0, num_blocks)` [CUDA_C_Programming_Guide:L12154-L12201].
*   `static unsigned long long cluster_rank()`: Rank of the calling cluster within `[0, num_clusters)` [CUDA_C_Programming_Guide:L12154-L12201].
*   `static unsigned long long num_threads()`: Total number of threads in the group [CUDA_C_Programming_Guide:L12154-L12201].
*   `static unsigned long long num_blocks()`: Total number of blocks in the group [CUDA_C_Programming_Guide:L12154-L12201].
*   `static unsigned long long num_clusters()`: Total number of clusters in the group [CUDA_C_Programming_Guide:L12154-L12201].
*   `static dim3 dim_blocks()`: Dimensions of the launched grid in units of blocks [CUDA_C_Programming_Guide:L12154-L12201].
*   `static dim3 dim_clusters()`: Dimensions of the launched grid in units of clusters [CUDA_C_Programming_Guide:L12154-L12201].
*   `static dim3 block_index()`: 3-dimensional index of the block within the launched grid [CUDA_C_Programming_Guide:L12154-L12201].
*   `static dim3 cluster_index()`: 3-dimensional index of the cluster within the launched grid [CUDA_C_Programming_Guide:L12154-L12201].

### Legacy Member Functions (Aliases)

*   `static unsigned long long size()`: Total number of threads in the group. This is an alias of `num_threads()` [CUDA_C_Programming_Guide:L12154-L12201].
*   `static dim3 group_dim()`: Dimensions of the launched grid. This is an alias of `dim_blocks()` [CUDA_C_Programming_Guide:L12154-L12201].

## See Also

*   [Explicit Groups](#1142-explicit-groups) [CUDA_C_Programming_Guide:L12154-L12201]
