# Distributed Shared Memory

Distributed Shared Memory (DSM) is a feature introduced in compute capability 9.0 that allows threads in a thread block cluster to access the shared memory of all participating thread blocks within that cluster [CUDA_C_Programming_Guide:L1851-L1971]. It provides a partitioned shared memory address space where threads can read, write, or perform atomics on local or remote block memory [CUDA_C_Programming_Guide:L1851-L1971]. The total size of the distributed shared memory is the number of blocks per cluster multiplied by the shared memory size per block [CUDA_C_Programming_Guide:L1851-L1971].

## Overview and Address Space

Thread block clusters provide the ability for threads within a cluster to access the shared memory of all participating thread blocks [CUDA_C_Programming_Guide:L1851-L1971]. This partitioned shared memory is called Distributed Shared Memory, and the corresponding address space is called the Distributed shared memory address space [CUDA_C_Programming_Guide:L1851-L1971]. Threads that belong to a thread block cluster can read, write, or perform atomics in the distributed address space, regardless of whether the address belongs to the local thread block or a remote thread block [CUDA_C_Programming_Guide:L1851-L1971].

While DSM allows access to remote block memory, shared memory size specifications (static or dynamic) remain per thread block [CUDA_C_Programming_Guide:L1851-L1971]. The size of the distributed shared memory is calculated as the number of thread blocks per cluster multiplied by the size of shared memory per thread block [CUDA_C_Programming_Guide:L1851-L1971].

## Synchronization and Lifecycle

Accessing data in distributed shared memory requires all the thread blocks in the cluster to exist [CUDA_C_Programming_Guide:L1851-L1971]. A user can guarantee that all thread blocks have started executing using `cluster.sync()` from the Cluster Group API [CUDA_C_Programming_Guide:L1851-L1971]. 

Users must ensure that distributed shared memory operations complete before any thread block exits to prevent race conditions with remote readers [CUDA_C_Programming_Guide:L1851-L1971]. For example, if a remote thread block is trying to read a given thread block’s shared memory, the user needs to ensure that the shared memory read by the remote thread block is completed before the local thread block exits [CUDA_C_Programming_Guide:L1851-L1971].

## Use Cases: Histogram Computation

DSM provides an intermediate optimization step between local shared memory and global memory for operations like histogram computation [CUDA_C_Programming_Guide:L1851-L1971]. A standard way of computing histograms is to perform the computation in the shared memory of each thread block and then perform global memory atomics [CUDA_C_Programming_Guide:L1851-L1971]. A limitation of this approach is shared memory capacity; once the histogram bins no longer fit in the shared memory, the user needs to directly compute histograms and perform atomics in global memory [CUDA_C_Programming_Guide:L1851-L1971]. With distributed shared memory, CUDA provides an intermediate step where, depending on the histogram bins size, the histogram can be computed in shared memory, distributed shared memory, or global memory directly [CUDA_C_Programming_Guide:L1851-L1971].

### Example Kernel

The following example demonstrates computing histograms using DSM. The kernel initializes shared memory, synchronizes the cluster, performs atomic updates to distributed shared memory bins, and then reduces the results to global memory [CUDA_C_Programming_Guide:L1851-L1971].

```cpp
#include <cooperative_groups.h>

// Distributed Shared memory histogram kernel
__global__ void clusterHist_kernel(int *bins, const int nbins, const int bins_per_block, const int *__restrict__ input,
size_t array_size)
{
    extern __shared__ int smem[];
    namespace cg = cooperative_groups;
    int tid = cg::this_grid().thread_rank();

    // Cluster initialization, size and calculating local bin offsets.
    cg::cluster_group cluster = cg::this_cluster();
    unsigned int clusterBlockRank = cluster.block_rank();
    int cluster_size = cluster.dim_blocks().x;

    for (int i = threadIdx.x; i < bins_per_block; i += blockDim.x)
    {
        smem[i] = 0; //Initialize shared memory histogram to zeros
    }

    // cluster synchronization ensures that shared memory is initialized to zero in
    // all thread blocks in the cluster. It also ensures that all thread blocks
    // have started executing and they exist concurrently.
    cluster.sync();

    for (int i = tid; i < array_size; i += blockDim.x * gridDim.x)
    {
        int ldata = input[i];

        //Find the right histogram bin.
        int binid = ldata;
        if (ldata < 0)
            binid = 0;
        else if (ldata >= nbins)
            binid = nbins - 1;

        //Find destination block rank and offset for computing
        //distributed shared memory histogram
        int dst_block_rank = (int)(binid / bins_per_block);
        int dst_offset = binid % bins_per_block;

        //Pointer to target block shared memory
        int *dst_smem = cluster.map_shared_rank(smem, dst_block_rank);

        //Perform atomic update of the histogram bin
        atomicAdd(dst_smem + dst_offset, 1);
    }

    // cluster synchronization is required to ensure all distributed shared
    // memory operations are completed and no thread block exits while
    // other thread blocks are still accessing distributed shared memory
    cluster.sync();

    // Perform global memory histogram, using the local distributed memory histogram
    int *lbins = bins + cluster.block_rank() * bins_per_block;
    for (int i = threadIdx.x; i < bins_per_block; i += blockDim.x)
    {
        atomicAdd(&lbins[i], smem[i]);
    }
}
```

## Launch Configuration

Launching a DSM kernel involves configuring `cudaLaunchConfig_t` with dynamic shared memory size per block and setting the cluster dimension via `cudaLaunchAttributeClusterDimension` [CUDA_C_Programming_Guide:L1851-L1971]. The cluster size depends on the amount of distributed shared memory required [CUDA_C_Programming_Guide:L1851-L1971]. If the histogram is small enough to fit in the shared memory of just one block, the user can launch the kernel with a cluster size of 1 [CUDA_C_Programming_Guide:L1851-L1971].

```cpp
// Launch via extensible launch
{
    cudaLaunchConfig_t config = {0};
    config.gridDim = array_size / threads_per_block;
    config.blockDim = threads_per_block;

    // cluster_size depends on the histogram size.
    // ( cluster_size == 1 ) implies no distributed shared memory, just thread block
    // local shared memory
    int cluster_size = 2; // size 2 is an example here
    int nbins_per_block = nbins / cluster_size;

    //dynamic shared memory size is per block.
    //Distributed shared memory size = cluster_size * nbins_per_block * sizeof(int)
    config.dynamicSmemBytes = nbins_per_block * sizeof(int);

    CUDA_CHECK(::cudaFuncSetAttribute((void *)clusterHist_kernel,
        cudaFuncAttributeMaxDynamicSharedMemorySize, config.dynamicSmemBytes));

    cudaLaunchAttribute attribute[1];
    attribute[0].id = cudaLaunchAttributeClusterDimension;
    attribute[0].val.clusterDim.x = cluster_size;
    attribute[0].val.clusterDim.y = 1;
    attribute[0].val.clusterDim.z = 1;

    config.numAttrs = 1;
    config.attrs = attribute;

    cudaLaunchKernelEx(&config, clusterHist_kernel, bins, nbins, bins_per_block, input,
        array_size);
}
```
