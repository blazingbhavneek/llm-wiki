# Implicit Groups

Implicit groups represent the launch configuration of the kernel. Regardless of how the kernel is written, it always possesses a defined set of threads, blocks, block dimensions, a single grid, and grid dimensions [CUDA_C_Programming_Guide:L12050-L12058]. If the multi-device cooperative launch API is used, the kernel can have multiple grids, with one grid per device [CUDA_C_Programming_Guide:L12050-L12058].

These groups provide the starting point for decomposition into finer-grained groups, which are typically hardware-accelerated and more specialized for the problem the developer is solving [CUDA_C_Programming_Guide:L12050-L12058].

## Usage and Safety

Although an implicit group handle can be created anywhere in the code, doing so is dangerous [CUDA_C_Programming_Guide:L12050-L12058]. Creating a handle for an implicit group is a collective operation, meaning all threads in the group must participate [CUDA_C_Programming_Guide:L12050-L12058]. If the group is created in a conditional branch that not all threads reach, this can lead to deadlocks or data corruption [CUDA_C_Programming_Guide:L12050-L12058].

For this reason, it is recommended to create a handle for the implicit group upfront, as early as possible and before any branching has occurred, and use that handle throughout the kernel [CUDA_C_Programming_Guide:L12050-L12058]. Group handles must be initialized at declaration time because there is no default constructor [CUDA_C_Programming_Guide:L12050-L12058]. Copy-constructing them is discouraged [CUDA_C_Programming_Guide:L12050-L12058].
