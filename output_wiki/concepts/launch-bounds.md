# __launch_bounds__

The `__launch_bounds__` qualifier is used in the definition of a `__global__` function to provide the compiler with additional information regarding launch constraints. This information aids the compiler's heuristics in minimizing register usage while keeping register spilling and instruction count to a minimum, thereby optimizing performance [CUDA_C_Programming_Guide:L11603-L11603].

## Parameters

The qualifier accepts the following parameters:

*   **maxThreadsPerBlock**: Specifies the maximum number of threads per block with which the application will ever launch the kernel. This compiles to the `.maxntid` PTX directive [CUDA_C_Programming_Guide:L11614-L11614].
*   **minBlocksPerMultiprocessor** (Optional): Specifies the desired minimum number of resident blocks per multiprocessor. This compiles to the `.minnctapersm` PTX directive [CUDA_C_Programming_Guide:L11616-L11616].
*   **maxBlocksPerCluster** (Optional): Specifies the desired maximum number of thread blocks per cluster with which the application will ever launch the kernel. This compiles to the `.maxclusterrank` PTX directive [CUDA_C_Programming_Guide:L11618-L11618].

## Optimization Behavior

When launch bounds are specified, the compiler derives an upper limit $L$ on the number of registers the kernel should use. This limit ensures that `minBlocksPerMultiprocessor` blocks (or a single block if `minBlocksPerMultiprocessor` is not specified) of `maxThreadsPerBlock` threads can reside on the multiprocessor [CUDA_C_Programming_Guide:L11620-L11620]. The compiler then optimizes register usage as follows:

*   If the initial register usage is higher than $L$, the compiler reduces it until it is less than or equal to $L$, usually at the expense of increased local memory usage and/or a higher number of instructions [CUDA_C_Programming_Guide:L11622-L11622].
*   If `maxThreadsPerBlock` is specified but `minBlocksPerMultiprocessor` is not, the compiler uses `maxThreadsPerBlock` to determine register usage thresholds for transitions between $n$ and $n+1$ resident blocks, applying similar heuristics as when no launch bounds are specified [CUDA_C_Programming_Guide:L11626-L11626].
*   If both `minBlocksPerMultiprocessor` and `maxThreadsPerBlock` are specified, the compiler may increase register usage up to $L$ to reduce the number of instructions and better hide single-thread instruction latency [CUDA_C_Programming_Guide:L11628-L11628].

## Constraints and Errors

Specifying launch bounds enforces runtime constraints. A kernel will fail to launch if it is executed with more threads per block than its `maxThreadsPerBlock` bound [CUDA_C_Programming_Guide:L11630-L11630]. Similarly, a kernel will fail to launch if it is executed with more thread blocks per cluster than its `maxBlocksPerCluster` bound [CUDA_C_Programming_Guide:L11632-L11632].

## Best Practices

Per-thread resources required by a CUDA kernel might limit the maximum block size in an unwanted way. To maintain forward compatibility with future hardware and toolkits, and to ensure that at least one thread block can run on a Streaming Multiprocessor (SM), developers should include the single argument `__launch_bounds__(maxThreadsPerBlock)` specifying the largest block size the kernel will be launched with [CUDA_C_Programming_Guide:L11634-L11634]. Failure to do so could lead to "too many resources requested for launch" errors [CUDA_C_Programming_Guide:L11634-L11634]. Providing the two-argument version `__launch_bounds__(maxThreadsPerBlock, minBlocksPerMultiprocessor)` can improve performance in some cases, though the right value for `minBlocksPerMultiprocessor` should be determined using detailed per-kernel analysis [CUDA_C_Programming_Guide:L11634-L11634].

Optimal launch bounds for a given kernel usually differ across major architecture revisions. Developers typically handle this in device code using the `__CUDA_ARCH__` macro [CUDA_C_Programming_Guide:L11636-L11636].

### Host Code Considerations

When invoking a kernel with the maximum number of threads per block specified in `__launch_bounds__()`, it is tempting to use the same value for the execution configuration. However, `__CUDA_ARCH__` is undefined in host code [CUDA_C_Programming_Guide:L11664-L11664]. Consequently, relying on architecture-specific macros in host code may result in incorrect launch configurations (e.g., launching with 256 threads per block regardless of the actual architecture) [CUDA_C_Programming_Guide:L11664-L11664].

The number of threads per block in the execution configuration should instead be determined:
*   At compile time using a macro that does not depend on `__CUDA_ARCH__` [CUDA_C_Programming_Guide:L11666-L11666].
*   Or at runtime based on the compute capability [CUDA_C_Programming_Guide:L11673-L11673].

## Verification

Register usage can be reported by the `--ptxas-options=-v` compiler option. The number of resident blocks can be derived from the occupancy reported by the CUDA profiler [CUDA_C_Programming_Guide:L11684-L11684].
