# Occupancy API and Calculator

Covers the occupancy-based kernel launch API (cudaOccupancyMaxPotentialBlockSize), cluster occupancy API (cudaOccupancyMaxPotentialClusterSize, cudaOccupancyMaxActiveClusters), and the standalone Nsight Compute occupancy calculator tool.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L6298-L6370

Citation: [CUDA_C_Programming_Guide:L6298-L6370]

````text
The following code sample configures an occupancy-based kernel launch of MyKernel according to the user input.

```c
// Device code
__global__ void MyKernel(int *array, int arrayCount)
{
    int idx = threadIdx.x + blockIdx.x * blockDim.x;
    if (idx < arrayCount) {
        array[idx] *= array[idx];
    }
}

// Host code
int launchMyKernel(int *array, int arrayCount)
{
    int blockSize;      // The launch configurator returned block size
    int minGridSize;     // The minimum grid size needed to achieve the
                                   // maximum occupancy for a full device
                                   // launch
    int gridSize;       // The actual grid size needed, based on input
                                   // size

    cudaOccupancyMaxPotentialBlockSize(
        &minGridSize,
        &blockSize,
        (void*)MyKernel,
        0,
        arrayCount);

    // Round up according to array size
    gridSize = (arrayCount + blockSize - 1) / blockSize;

    MyKernel<<<gridSize, blockSize>>>(array, arrayCount);
    cudaDeviceSynchronize();

    // If interested, the occupancy can be calculated with
    // cudaOccupancyMaxActiveBlocksPerMultiprocessor

    return 0;
}
```

The following code sample shows how to use the cluster occupancy API to find the max number of active clusters of a given size. Example code below calcualtes occupancy for cluster of size 2 and 128 threads per block.

Cluster size of 8 is forward compatible starting compute capability 9.0, except on GPU hardware or MIG configurations which are too small to support 8 multiprocessors in which case the maximum cluster size will be reduced. But it is recommended that the users query the maximum cluster size before launching a cluster kernel. Max cluster size can be queried using cudaOccupancyMaxPotential-ClusterSize API.

```txt
{
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

int max_cluster_size = 0;
cudaOccupancyMaxPotentialClusterSize(&max_cluster_size, (void *)kernel, &config);

int max_active_clusters = 0;
cudaOccupancyMaxActiveClusters(&max_active_clusters, (void *)kernel, &config);

std::cout << "Max Active Clusters of size 2: " << max_active_clusters << std::endl;
}
```

The CUDA Nsight Compute User Interface also provides a standalone occupancy calculator and launch configurator implementation in <CUDA\_Toolkit\_Path>∕include∕cuda\_occupancy.h for any use cases that cannot depend on the CUDA software stack. The Nsight Compute version of the occupancy calculator is particularly useful as a learning tool that visualizes the impact of changes to the parameters that afect occupancy (block size, registers per thread, and shared memory per thread).
````
