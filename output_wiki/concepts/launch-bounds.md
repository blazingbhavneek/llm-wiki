# 10.38. Launch Bounds

Covers the __launch_bounds__() qualifier, its parameters, compiler heuristics for register usage optimization, and architecture-specific handling via __CUDA_ARCH__.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L11600-L11685

Citation: [CUDA_C_Programming_Guide:L11600-L11685]

````text

As discussed in detail in Multiprocessor Level, the fewer registers a kernel uses, the more threads and thread blocks are likely to reside on a multiprocessor, which can improve performance.

Therefore, the compiler uses heuristics to minimize register usage while keeping register spilling (see Device Memory Accesses) and instruction count to a minimum. An application can optionally aid these heuristics by providing additional information to the compiler in the form of launch bounds that are specified using the \_\_launch\_bounds\_\_() qualifier in the definition of a \_\_global\_\_ function:

```lisp
__global__ void
__launch_bounds__(maxThreadsPerBlock, minBlocksPerMultiprocessor, maxBlocksPerCluster)
MyKernel(...)
{
    ...
}
```

maxThreadsPerBlock specifies the maximum number of threads per block with which the application will ever launch MyKernel(); it compiles to the .maxntidPTX directive.

▶ minBlocksPerMultiprocessor is optional and specifies the desired minimum number of resident blocks per multiprocessor; it compiles to the .minnctapersmPTX directive.

maxBlocksPerCluster is optional and specifies the desired maximum number thread blocks per cluster with which the application will ever launch MyKernel(); it compiles to the . maxclusterrankPTX directive.

If launch bounds are specified, the compiler first derives from them the upper limit L on the number of registers the kernel should use to ensure that minBlocksPerMultiprocessor blocks (or a single block if minBlocksPerMultiprocessor is not specified) of maxThreadsPerBlock threads can reside on the multiprocessor (see Hardware Multithreading for the relationship between the number of registers used by a kernel and the number of registers allocated per block). The compiler then optimizes register usage in the following way:

▶ If the initial register usage is higher than L, the compiler reduces it further until it becomes less or equal to L, usually at the expense of more local memory usage and/or higher number of instructions;

▶ If the initial register usage is lower than L

▶ If maxThreadsPerBlock is specified and minBlocksPerMultiprocessor is not, the compiler uses maxThreadsPerBlock to determine the register usage thresholds for the transitions between n and n+1 resident blocks (i.e., when using one less register makes room for an additional resident block as in the example of Multiprocessor Level) and then applies similar heuristics as when no launch bounds are specified;

▶ If both minBlocksPerMultiprocessor and maxThreadsPerBlock are specified, the compiler may increase register usage as high as L to reduce the number of instructions and better hide single thread instruction latency.

A kernel will fail to launch if it is executed with more threads per block than its launch bound max-ThreadsPerBlock.

A kernel will fail to launch if it is executed with more thread blocks per cluster than its launch bound maxBlocksPerCluster.

Per thread resources required by a CUDA kernel might limit the maximum block size in an unwanted way. In order to maintain forward compatibility to future hardware and toolkits and to ensure that at least one thread block can run on an SM, developers should include the single argument \_\_launch\_bounds\_\_(maxThreadsPerBlock) which specifies the largest block size that the kernel will be launched with. Failure to do so could lead to “too many resources requested for launch” errors. Providing the two argument version of \_\_launch\_bounds\_\_(maxThreadsPerBlock, minBlocksPerMultiprocessor) can improve performance in some cases. The right value for min-BlocksPerMultiprocessor should be determined using a detailed per kernel analysis.

Optimal launch bounds for a given kernel will usually difer across major architecture revisions. The sample code below shows how this is typically handled in device code using the \_\_CUDA\_ARCH\_\_ macro introduced in Application Compatibility.

```lisp
#define THREADS_PER_BLOCK          256
#if __CUDA_ARCH__ >= 200
    #define MY_KERNEL_MAX_THREADS (2 * THREADS_PER_BLOCK)
    #define MY_KERNEL_MIN_BLOCKS 3
#else
    #define MY_KERNEL_MAX_THREADS THREADS_PER_BLOCK
    #define MY_KERNEL_MIN_BLOCKS 2
#endif

// Device code
__global__ void
__launch_bounds__(MY_KERNEL_MAX_THREADS, MY_KERNEL_MIN_BLOCKS)
MyKernel(...)
{
    ...
}
```

In the common case where MyKernel is invoked with the maximum number of threads per block (specified as the first parameter of \_\_launch\_bounds\_\_()), it is tempting to use MY\_KERNEL\_MAX\_THREADS as the number of threads per block in the execution configuration:

```txt
// Host code
MyKernel<<<blocksPerGrid, MY_KERNEL_MAX_THREADS>>>(...);
```

This will not work however since \_\_CUDA\_ARCH\_\_ is undefined in host code as mentioned in Application Compatibility, so MyKernel will launch with 256 threads per block even when \_\_CUDA\_ARCH\_\_ is greater or equal to 200. Instead the number of threads per block should be determined:

▶ Either at compile time using a macro that does not depend on \_\_CUDA\_ARCH\_\_, for example

```txt
// Host code
MyKernel<<<blocksPerGrid, THREADS_PER_BLOCK>>>(...);
```

▶ Or at runtime based on the compute capability

```c
// Host code
cudaGetDeviceProperties(&deviceProp, device);
int threadsPerBlock =
    (deviceProp.major >= 2 ?
        2 * THREADS_PER_BLOCK : THREADS_PER_BLOCK);
MyKernel<<<blocksPerGrid, threadsPerBlock>>>(...);
```

Register usage is reported by the --ptxas-options=-v compiler option. The number of resident blocks can be derived from the occupancy reported by the CUDA profiler (see Device Memory Accesses for a definition of occupancy).
````
