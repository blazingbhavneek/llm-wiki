# cudaLaunchKernelEx

The `cudaLaunchKernelEx` API is used to launch a kernel with runtime configuration, specifically allowing for the specification of thread block cluster dimensions.

## Functionality

This API enables the launch of a kernel with a cluster configuration defined at runtime. It accepts three primary arguments:

1. A configuration argument of type `cudaLaunchConfig_t`.
2. A pointer to the kernel function.
3. The kernel arguments.

## Usage

Thread block cluster dimensions can be specified at runtime, and the kernel with the cluster can be launched using the `cudaLaunchKernelEx` API [CUDA_C_Programming_Guide:L11571-L11571].

## References

- [CUDA_C_Programming_Guide:L11571-L11571]
