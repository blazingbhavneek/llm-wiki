# Lazy Loading Issues: Autotuning

In applications that launch several kernels implementing the same functionality to determine the fastest one, accurate timing is critical. While running at least one warmup iteration is generally advisable, it becomes especially important when using Lazy Loading [CUDA_C_Programming_Guide:L22189-L22199].

## The Problem

With Lazy Loading, the time taken to load the kernel is included in the measurement if not handled correctly. This inclusion skews the benchmark results, making it difficult to accurately compare kernel performance [CUDA_C_Programming_Guide:L22189-L22199].

## Solutions

To mitigate the impact of lazy loading on autotuning benchmarks, the following approaches are recommended:

*   **Warmup Iterations**: Perform at least one warmup iteration prior to the actual measurement to ensure the kernel is loaded and ready [CUDA_C_Programming_Guide:L22189-L22199].
*   **Preloading**: Explicitly preload the benchmarked kernel prior to launching it for measurement [CUDA_C_Programming_Guide:L22189-L22199].
