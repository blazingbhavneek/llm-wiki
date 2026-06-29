# Grid Synchronization

Grid synchronization allows for inter-thread block synchronization within a single kernel execution, a capability introduced with Cooperative Groups. Prior to this feature, the CUDA programming model only permitted synchronization between thread blocks at the kernel completion boundary [CUDA_C_Programming_Guide:L13206-L13220].

## Motivation and Use Cases

Synchronizing at the kernel boundary carries implicit state invalidation and potential performance implications [CUDA_C_Programming_Guide:L13206-L13220]. In applications structured as a processing pipeline with many small kernels, each stage typically requires the previous stage to complete before the next begins [CUDA_C_Programming_Guide:L13206-L13220]. Grid synchronization allows such applications to be restructured into persistent thread blocks that synchronize on the device when a specific stage is complete, rather than launching separate kernels [CUDA_C_Programming_Guide:L13206-L13220].

## Implementation

To synchronize across the grid from within a kernel, the `grid.sync()` function is used within a grid group [CUDA_C_Programming_Guide:L13206-L13220].

```javascript
grid_group grid = this_grid();
grid.sync();
```

### Launch Requirements

Grid synchronization requires the use of the `cudaLaunchCooperativeKernel` CUDA runtime launch API or the equivalent CUDA driver API, rather than the standard `<<<...>>>` execution configuration syntax [CUDA_C_Programming_Guide:L13206-L13220].

To guarantee co-residency of the thread blocks on the GPU, the number of blocks launched must be carefully considered [CUDA_C_Programming_Guide:L13221-L13231]. Two common strategies include:

1.  **Launching one block per SM:**
    ```javascript
    int dev = 0;
    cudaDeviceProp deviceProp;
    cudaGetDeviceProperties(&deviceProp, dev);
    // initialize, then launch
    cudaLaunchCooperativeKernel((void*)my_kernel, deviceProp.multiProcessorCount,
      → numThreads, args);
    ```
    [CUDA_C_Programming_Guide:L13221-L13231]

2.  **Maximizing parallelism using the occupancy calculator:**
    ```c
    /// This will launch a grid that can maximally fill the GPU, on the default stream with
    kernel arguments
    int numBlocksPerSm = 0;
    // Number of threads my_kernel will be launched with
    int numThreads = 128;
    cudaDeviceProp deviceProp;
    cudaGetDeviceProperties(&deviceProp, dev);
    cudaOccupancyMaxActiveBlocksPerMultiprocessor(&numBlocksPerSm, my_kernel, numThreads,
      →0);
    // launch
    void *kernelArgs[] = { /* add kernel args */ };
    dim3 dimBlock(numThreads, 1, 1);
    dim3 dimGrid(deviceProp.multiProcessorCount*numBlocksPerSm, 1, 1);
    cudaLaunchCooperativeKernel((void*)my_kernel, dimGrid, dimBlock, kernels);
    ```
    [CUDA_C_Programming_Guide:L13232-L13250]

## Device Support and Prerequisites

It is good practice to verify that the device supports cooperative launches by querying the `cudaDevAttrCooperativeLaunch` attribute [CUDA_C_Programming_Guide:L13251-L13267].

```javascript
int dev = 0;
int supportsCoopLaunch = 0;
cudaDeviceGetAttribute(&supportsCoopLaunch, cudaDevAttrCooperativeLaunch, dev);
```

This attribute returns 1 if the property is supported on the specified device [CUDA_C_Programming_Guide:L13251-L13267].

### Hardware and Software Requirements

*   **Compute Capability:** Only devices with compute capability 6.0 and higher are supported [CUDA_C_Programming_Guide:L13251-L13267].
*   **Operating System Constraints:**
    *   **Linux without MPS:** Supported for devices with compute capability 6.0 or higher [CUDA_C_Programming_Guide:L13251-L13267].
    *   **Linux with MPS:** Supported only for devices with compute capability 7.0 or higher [CUDA_C_Programming_Guide:L13251-L13267].
    *   **Windows:** Supported on the latest Windows platform [CUDA_C_Programming_Guide:L13251-L13267].

[ CUDA_C_Programming_Guide:L13251-L13267]
