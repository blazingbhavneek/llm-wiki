# __cluster_dims__

The `__cluster_dims__` attribute is a compile-time specifier used to define the dimensions of a thread block cluster, enabling the use of the cluster hierarchy in CUDA kernels. This feature is supported on devices with Compute Capability 9.0 and above.

## Syntax and Usage

The attribute accepts an optional list of integers representing the cluster dimensions in the X, Y, and Z axes: `__cluster_dims__([x, [y, [z]]])` [CUDA_C_Programming_Guide:L11563-L11563].

### Specifying Dimensions

Users can explicitly define the cluster size at compile time. For example, a cluster size of 2 in the X dimension and 1 in the Y and Z dimensions can be specified as:

```cpp
__cluster_dims__(2, 1, 1)
```

### Default Behavior

If no dimensions are specified (i.e., using the default form `__cluster_dims__()`), the kernel is designated to be launched as a cluster grid, but the specific dimensions are not fixed at compile time [CUDA_C_Programming_Guide:L11569-L11569]. In this case, the user is free to specify the cluster dimensions at launch time [CUDA_C_Programming_Guide:L11569-L11569].

### Launch Constraints

When using the default form where dimensions are not specified at compile time, the dimensions **must** be provided at launch time. Failure to specify the dimension at launch time will result in a launch time error [CUDA_C_Programming_Guide:L11569-L11569].

## Requirements

- **Compute Capability**: 9.0 or higher.
- **Language**: CUDA C++.
