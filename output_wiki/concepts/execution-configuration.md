# 10.37. Execution Configuration

Covers the execution configuration syntax for __global__ functions, including grid/block dimensions, shared memory allocation, stream association, and cluster dimensions (CC 9.0+).

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L11533-L11599

Citation: [CUDA_C_Programming_Guide:L11533-L11599]

````text
## 10.37. Execution Configuration

Any call to a \_\_global\_\_ function must specify the execution configuration for that call. The execution configuration defines the dimension of the grid and blocks that will be used to execute the function on the device, as well as the associated stream (see CUDA Runtime for a description of streams).

The execution configuration is specified by inserting an expression of the form <<< Dg, Db, Ns, S >>> between the function name and the parenthesized argument list, where:

▶ Dg is of type dim3 (see dim3) and specifies the dimension and size of the grid, such that Dg.x \* Dg.y \* Dg.z equals the number of blocks being launched;

Db is of type dim3 (see dim3) and specifies the dimension and size of each block, such that Db.x \* Db.y \* Db.z equals the number of threads per block;

Ns is of type size\_t and specifies the number of bytes in shared memory that is dynamically allocated per block for this call in addition to the statically allocated memory; this dynamically allocated memory is used by any of the variables declared as an external array as mentioned in \_\_shared\_\_; Ns is an optional argument which defaults to 0;

S is of type cudaStream\_t and specifies the associated stream; S is an optional argument which defaults to 0.

As an example, a function declared as

```txt
__global__ void Func(float* parameter);
```

must be called like this:

```txt
Func<<< Dg, Db, Ns >>>(parameter);
```

The arguments to the execution configuration are evaluated before the actual function arguments.

The function call will fail if Dg or Db are greater than the maximum sizes allowed for the device as specified in Compute Capabilities, or if Ns is greater than the maximum amount of shared memory available on the device, minus the amount of shared memory required for static allocation.

Compute capability 9.0 and above allows users to specify compile time thread block cluster dimensions, so that the kernel can use the cluster hierarchy in CUDA. Compile time cluster dimension can be specified using \_\_cluster\_dims\_\_([x, [y, [z]]]). The example below shows compile time cluster size of 2 in X dimension and 1 in Y and Z dimension.

```javascript
__global__ void __cluster_dims__(2, 1, 1) Func(float* parameter);
```

The default form of \_\_cluster\_dims\_\_() specifies that a kernel is to be launched as a cluster grid. By not specifying a cluster dimension, the user is free to specify the dimension at launch time. Not specifying a dimension at launch time will result in a launch time error.

Thread block cluster dimensions can also be specified at runtime and kernel with the cluster can be launched using cudaLaunchKernelEx API. The API takes a configuration argument of type cudaLaunchConfig\_t, kernel function pointer and kernel arguments. Runtime kernel configuration is shown in the example below.

```lisp
__global__ void Func(float* parameter);

// Kernel invocation with runtime cluster size
{
    cudaLaunchConfig_t config = {0};
    // The grid dimension is not affected by cluster launch, and is still enumerated
    // using number of blocks.
    // The grid dimension should be a multiple of cluster size.
    config.gridDim = Dg;
    config.blockDim = Db;
    config.dynamicSmemBytes = Ns;

    cudaLaunchAttribute attribute[1];
    attribute[0].id = cudaLaunchAttributeClusterDimension;
    attribute[0].val.clusterDim.x = 2; // Cluster size in X-dimension
    attribute[0].val.clusterDim.y = 1;
    attribute[0].val.clusterDim.z = 1;
    config.attrs = attribute;
    config.numAttrs = 1;

    float* parameter;
    cudaLaunchKernelEx(&config, Func, parameter);
}
```

## 10.38. Launch Bounds
````
