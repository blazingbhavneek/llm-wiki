# CUDA Occupancy Header (cuda_occupancy.h)

The `cuda_occupancy.h` header provides a standalone implementation of an occupancy calculator and launch configurator. This tool is part of the CUDA Nsight Compute User Interface and is located in the `<CUDA_Toolkit_Path>/include/` directory.

## Use Cases

This standalone implementation is designed for use cases where the full CUDA software stack cannot be depended upon [CUDA_C_Programming_Guide:L6369-L6369].

## Educational Value

The Nsight Compute version of the occupancy calculator serves as a particularly useful learning tool. It visualizes the impact of changes to key parameters that affect occupancy, including:

*   Block size
*   Registers per thread
*   Shared memory per thread [CUDA_C_Programming_Guide:L6369-L6369]
