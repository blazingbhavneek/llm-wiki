# Cluster Occupancy API

The Cluster Occupancy API allows developers to query and configure cluster-based kernel launches. This includes setting cluster dimensions via the `cudaLaunchConfig_t` structure and querying the maximum number of active clusters or potential cluster sizes for a given kernel configuration.

## Configuration Structure

Kernel launches with cluster dimensions require the use of the `cudaLaunchConfig_t` structure. This structure allows setting grid dimensions, block dimensions, dynamic shared memory size, and launch attributes such as cluster dimensions.

```cpp
cudaLaunchConfig_t config = {0};
config.gridDim = number_of_blocks;
config.blockDim = 128; // threads_per_block = 128
config.dynamicSmemBytes = dynamic_shared_memory_size;

cudaLaunchAttribute attribute[1];
attribute[0].id = cudaLaunchAttributeClusterDimension;
attribute[0].val.clusterDim.x = 2; // cluster_size = 2
attribute[0].val.clusterDim.y = 1;
attribute[0].val.clusterDim.z = 1;
config.attrs = attribute;
config.numAttrs = 1;
```

## Querying Cluster Properties

Two primary functions are used to query occupancy information for cluster-based kernels:

1.  **`cudaOccupancyMaxPotentialClusterSize`**: Queries the maximum cluster size supported by the hardware for a given configuration. This is recommended before launching a cluster kernel, especially when using cluster size 8, which is forward compatible starting from compute capability 9.0. Note that on GPU hardware or MIG configurations that are too small to support 8 multiprocessors, the maximum cluster size will be reduced [CUDA_C_Programming_Guide:L6340-L6367].
2.  **`cudaOccupancyMaxActiveClusters`**: Queries the maximum number of active clusters of a specific size that can be launched [CUDA_C_Programming_Guide:L6340-L6367].

### Example Usage

The following code snippet demonstrates how to calculate occupancy for a cluster of size 2 with 128 threads per block:

```cpp
int max_cluster_size = 0;
cudaOccupancyMaxPotentialClusterSize(&max_cluster_size, (void *)kernel, &config);

int max_active_clusters = 0;
cudaOccupancyMaxActiveClusters(&max_active_clusters, (void *)kernel, &config);

std::cout << "Max Active Clusters of size 2: " << max_active_clusters << std::endl;
```

## Forward Compatibility

Cluster size 8 is forward compatible starting with compute capability 9.0. However, users should always query the maximum cluster size using `cudaOccupancyMaxPotentialClusterSize` to ensure compatibility with the specific GPU hardware or MIG configuration, as smaller configurations may result in a reduced maximum cluster size [CUDA_C_Programming_Guide:L6340-L6367].
