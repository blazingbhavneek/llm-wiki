# 10.44. CUDA C++ Memory Model

Part of [Cuda C Programming Guide Reference](README.md). Source lines L11917-L12503.

- [Cooperative Groups](../../../concepts/cooperative-groups.md) — Cooperative Groups is an extension to the CUDA programming model introduced in CUDA 9 that allows developers to organize and synchronize communicating threads at granularities beyond the single thread block barrier.
- [Cooperative Groups API History](../../../entities/cooperative-groups-api-history.md) — This page documents the history of changes to the Cooperative Groups API across CUDA versions, including the removal of multi_grid_group in CUDA 13.0, the addition of barrier functions in CUDA 12.2, and the promotion of experimental APIs in CUDA 12.0.
- [Implicit Groups](../../../concepts/implicit-groups.md) — Implicit groups represent the kernel's launch configuration (threads, blocks, grid) and serve as the starting point for group decomposition, requiring early, collective initialization to avoid deadlocks.
- [thread_block Group](../../../entities/thread-block-group.md) — The thread_block datatype explicitly represents the thread block group within the Cooperative Groups extension, providing synchronization and indexing utilities derived from thread_group.
- [cluster_group](../../../entities/cluster-group.md) — The cluster_group class represents all threads in a single cluster (Compute Capability 9.0+) and provides synchronization, ranking, and shared memory mapping APIs.
- [grid_group](../../../entities/grid-group.md) — The grid_group class represents all threads in a single grid, providing methods for querying grid topology and performing synchronization via the cooperative launch API.
- [thread_block_tile](../../../entities/thread-block-tile.md) — A templated tiled group where size is known at compile time for optimization, constructed via tiled_partition() with size constraints and specific memory requirements on older hardware.
- [Single Thread Group](../../../entities/single-thread-group.md) — The single thread group represents the current thread via the this_thread() function, returning a thread_block_tile<1> object used in cooperative group APIs like memcpy_async.
- [coalesced_group](../../../entities/coalesced-group.md) — Represents the set of active (coalesced) threads in a warp at a specific point in time, constructed via coalesced_threads() to enable cooperative operations on dynamically active thread subsets.
- [tiled_partition](../../../entities/tiled-partition.md) — A collective operation that partitions a parent group (thread_block or thread_block_tile) into a 1D row-major tiling of subgroups.
