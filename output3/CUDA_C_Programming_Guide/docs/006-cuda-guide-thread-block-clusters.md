
In GPUs with compute capability 9.0, all the thread blocks in the cluster are guaranteed to be coscheduled on a single GPU Processing Cluster (GPC) and allow thread blocks in the cluster to perform hardware-supported synchronization using the Cluster Group API cluster.sync(). Cluster group also provides member functions to query cluster group size in terms of number of threads or number of blocks using num\_threads() and num\_blocks() API respectively. The rank of a thread or block in the cluster group can be queried using dim\_threads() and dim\_blocks() API respectively.

Thread blocks that belong to a cluster have access to the Distributed Shared Memory. Thread blocks in a cluster have the ability to read, write, and perform atomics to any address in the distributed shared memory. Distributed Shared Memory gives an example of performing histograms in distributed shared memory.

## 5.2.2. Blocks as Clusters

With \_\_cluster\_dims\_\_, the number of launched clusters is kept implicit and can only be calculated manually.

```lisp
__cluster_dims__((2, 2, 2)) __global__ void foo();

// 8x8x8 clusters each with 2x2x2 thread blocks.
foo<<<dim3(16, 16, 16), dim3(1024, 1, 1)>>();
```

In the above example, the kernel is launched as a grid of 16x16x16 thread blocks, or in fact a grid of 8x8x8 clusters. Alternatively, with another compile-time kernel attribute \_\_block\_size\_\_, one is allowed to launch a grid explicitly configured with the number of thread block clusters.

```txt
// Implementation detail of how many threads per block and blocks per cluster
// is handled as an attribute of the kernel.
__block_size__((1024, 1, 1), (2, 2, 2)) __global__ void foo();

// 8x8x8 clusters.
foo<<<dim3(8, 8, 8)>>();
```

\_block\_size\_\_ requires two fields each being a tuple of 3 elements. The first tuple denotes block dimension and second cluster size. The second tuple is assumed to be (1,1,1) if it’s not passed. To specify the stream, one must pass 1 and 0 as the second and third arguments within <<<>>> and lastly the stream. Passing other values would lead to undefined behavior.

Note that it is illegal for the second tuple of \_\_block\_size\_\_ and \_\_cluster\_dims\_\_ to be specified at the same time. It’s also illegal to use \_\_block\_size\_\_ with an empty \_\_cluster\_dims\_\_. When the second tuple of \_\_block\_size\_\_ is specified, it implies the “Blocks as Clusters” being enabled and the compiler would recognize the first argument inside <<<>>> as the number of clusters instead of thread blocks.
