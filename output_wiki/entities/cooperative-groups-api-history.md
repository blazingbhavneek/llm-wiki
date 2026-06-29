# Cooperative Groups API History

The Cooperative Groups API has evolved across several CUDA releases, with changes ranging from the removal of experimental features to the addition of new synchronization primitives and the promotion of previously experimental APIs to the main namespace.

## CUDA 13.0

In CUDA 13.0, the `multi_grid_group` feature was removed from the Cooperative Groups API [CUDA_C_Programming_Guide:L11935-L11958].

## CUDA 12.2

CUDA 12.2 introduced new synchronization capabilities for cooperative groups. Specifically, `barrier_arrive` and `barrier_wait` member functions were added for both `grid_group` and `thread_block` [CUDA_C_Programming_Guide:L11935-L11958].

## CUDA 12.1

CUDA 12.1 added the `invoke_one` and `invoke_one_broadcast` APIs to the Cooperative Groups namespace [CUDA_C_Programming_Guide:L11935-L11958].

## CUDA 12.0

CUDA 12.0 marked a significant change by moving several previously experimental APIs into the main namespace. These included:

*   Asynchronous reduce and scan update, which were originally added in CUDA 11.7.
*   Support for `thread_block_tile` larger than 32, which was originally added in CUDA 11.1.

Additionally, starting with CUDA 12.0, it is no longer required to provide memory using the `block_tile_memory` object to create these large tiles on Compute Capability 8.0 or higher hardware [CUDA_C_Programming_Guide:L11935-L11958].

## CUDA 11.x

While not detailed as a primary change in the "What's New" section for 12.0+, the history notes that asynchronous reduce and scan updates were added in CUDA 11.7, and large thread block tiles (>32) were added in CUDA 11.1, before being promoted to the main namespace in CUDA 12.0 [CUDA_C_Programming_Guide:L11935-L11958].
