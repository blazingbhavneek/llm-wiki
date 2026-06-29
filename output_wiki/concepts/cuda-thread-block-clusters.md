# CUDA Thread Block Clusters

Thread Block Clusters are an optional hierarchical level in the CUDA programming model introduced with NVIDIA Compute Capability 9.0 [CUDA_C_Programming_Guide:L934-L936]. They group multiple thread blocks together to ensure that all blocks within a cluster are co-scheduled on a single GPU Processing Cluster (GPC) [CUDA_C_Programming_Guide:L934-L936]. This grouping allows for hardware-supported synchronization and communication between thread blocks within the same cluster [CUDA_C_Programming_Guide:L1006-L1008].

## Hierarchy and Scheduling

Similar to how threads within a thread block are guaranteed to be co-scheduled on a Streaming Multiprocessor (SM), thread blocks within a cluster are guaranteed to be co-scheduled on a GPC [CUDA_C_Programming_Guide:L934-L936]. Clusters are organized into a one-dimensional, two-dimensional, or three-dimensional grid, mirroring the structure of thread block grids [CUDA_C_Programming_Guide:L934-L936].

### Cluster Size Limits

The number of thread blocks in a cluster is user-defined, but a maximum of 8 thread blocks per cluster is supported as a portable size in CUDA [CUDA_C_Programming_Guide:L934-L936]. On GPU hardware or MIG configurations that cannot support 8 multiprocessors, the maximum cluster size is reduced accordingly [CUDA_C_Programming_Guide:L934-L936]. Larger configurations or specific smaller configurations can be queried using the `cudaOccupancyMaxPotentialClusterSize` API [CUDA_C_Programming_Guide:L934-L936].

## Synchronization and Communication

Thread blocks belonging to a cluster can perform hardware-supported synchronization using the Cluster Group API [CUDA_C_Programming_Guide:L1006-L1008]. Key features include:

*   **Synchronization:** `cluster.sync()` allows all thread blocks in the cluster to synchronize [CUDA_C_Programming_Guide:L1006-L1008].
*   **Querying Size:** Member functions `num_threads()` and `num_blocks()` allow querying the cluster group size in terms of threads or blocks, respectively [CUDA_C_Programming_Guide:L1006-L1008].
*   **Rank Querying:** `dim_threads()` and `dim_blocks()` allow querying the rank of a specific thread or block within the cluster group [CUDA_C_Programming_Guide:L1006-L1008].
*   **Distributed Shared Memory (DSM):** Thread blocks in a cluster have access to Distributed Shared Memory, enabling them to read, write, and perform atomic operations on any address within the DSM [CUDA_C_Programming_Guide:L1006-L1008].

## Configuration

Clusters can be configured at compile time or runtime. The grid dimension (number of blocks) is still enumerated using the number of blocks, but the grid dimension must be a multiple of the cluster size [CUDA_C_Programming_Guide:L945-L967] [CUDA_C_Programming_Guide:L971-L1004].

### Compile-Time Configuration

The `__cluster_dims__` attribute specifies the cluster dimensions at compile time [CUDA_C_Programming_Guide:L945-L967].

```cpp
// Kernel definition with compile-time cluster size (2, 1, 1)
__global__ void __cluster_dims__(2, 1, 1) cluster_kernel(float *input, float* output)
{
}

int main()
{
    float *input, *output;
    dim3 threadsPerBlock(16, 16);
    dim3 numBlocks(N / threadsPerBlock.x, N / threadsPerBlock.y);

    // Grid dimension must be a multiple of cluster size
    cluster_kernel<<<numBlocks, threadsPerBlock>>>(input, output);
}
```

Alternatively, the `__block_size__` attribute can specify both the block dimension and the cluster size [CUDA_C_Programming_Guide:L1023-L1030].

```cpp
// Block size (1024, 1, 1) and cluster size (2, 2, 2)
__block_size__((1024, 1, 1), (2, 2, 2)) __global__ void foo();

// Launch with 8x8x8 clusters
foo<<<dim3(8, 8, 8)>>();
```

When using `__block_size__` with a non-default cluster size, the first argument in the launch configuration `<<<>>>` is interpreted as the number of clusters, not the number of thread blocks [CUDA_C_Programming_Guide:L1032-L1034]. It is illegal to specify the cluster size in both `__block_size__` and `__cluster_dims__` simultaneously [CUDA_C_Programming_Guide:L1032-L1034].

### Runtime Configuration

Clusters can be configured at runtime using the `cudaLaunchConfig_t` structure and `cudaLaunchKernelEx` [CUDA_C_Programming_Guide:L971-L1004].

```cpp
__global__ void cluster_kernel(float *input, float* output)
{
}

int main()
{
    float *input, *output;
    dim3 threadsPerBlock(16, 16);
    dim3 numBlocks(N / threadsPerBlock.x, N / threadsPerBlock.y);

    cudaLaunchConfig_t config = {0};
    config.gridDim = numBlocks;
    config.blockDim = threadsPerBlock;

    cudaLaunchAttribute attribute[1];
    attribute[0].id = cudaLaunchAttributeClusterDimension;
    attribute[0].val.clusterDim.x = 2; // Cluster size in X-dimension
    attribute[0].val.clusterDim.y = 1;
    attribute[0].val.clusterDim.z = 1;
    config.attrs = attribute;
    config.numAttrs = 1;

    cudaLaunchKernelEx(&config, cluster_kernel, input, output);
}
```

## Examples

A 3D cluster configuration with 2x2x2 blocks per cluster results in 8 blocks per cluster (2*2*2) [CUDA_C_Programming_Guide:L1014-L1019].

```cpp
__cluster_dims__((2, 2, 2)) __global__ void foo();

// Launch 16x16x16 blocks, forming 8x8x8 clusters
foo<<<dim3(16, 16, 16), dim3(1024, 1, 1)>>();
```

## Implementation Details

When using the `__block_size__` attribute, it requires two fields, each being a tuple of 3 elements: the first tuple denotes the block dimension, and the second denotes the cluster size [CUDA_C_Programming_Guide:L1032-L1034]. If the cluster size tuple is not passed, it is assumed to be `(1,1,1)` [CUDA_C_Programming_Guide:L1032-L1034].

To specify a stream when using `__block_size__`, one must pass `1` and `0` as the second and third arguments within the launch configuration `<<<>>>`, followed by the stream pointer [CUDA_C_Programming_Guide:L1032-L1034]. Passing other values leads to undefined behavior [CUDA_C_Programming_Guide:L1032-L1034].

Using `__block_size__` with a specified cluster size enables "Blocks as Clusters" mode, where the compiler interprets the launch configuration's first argument as the number of clusters rather than thread blocks [CUDA_C_Programming_Guide:L1032-L1034]. It is illegal to use `__block_size__` with an empty `__cluster_dims__` [CUDA_C_Programming_Guide:L1032-L1034].
