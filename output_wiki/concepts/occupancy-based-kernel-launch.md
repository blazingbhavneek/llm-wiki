# Occupancy-Based Kernel Launch

The CUDA occupancy API provides functions to automatically determine the optimal block size and grid size for a kernel launch. This approach leverages device capabilities and kernel resource usage to maximize occupancy, which can improve performance by hiding memory latency and improving instruction throughput.

## API Usage

The primary function for this purpose is `cudaOccupancyMaxPotentialBlockSize`. It calculates the maximum potential block size and the minimum grid size required to achieve maximum occupancy for a full device launch.

### Function Signature

```c
cudaError_t cudaOccupancyMaxPotentialBlockSize(
    int* minGridSize,
    int* blockSize,
    void (*func)(),
    unsigned int blockSizeLimit,
    size_t dynamicSMemSize
);
```

- `minGridSize`: Pointer to an integer that receives the minimum grid size needed to achieve maximum occupancy for a full device launch.
- `blockSize`: Pointer to an integer that receives the block size that achieves maximum occupancy.
- `func`: Pointer to the kernel function.
- `blockSizeLimit`: Optional limit on the block size. If 0, no limit is applied.
- `dynamicSMemSize`: The amount of dynamic shared memory required by the kernel in bytes. If 0, it is assumed that the kernel does not use dynamic shared memory.

## Example Implementation

The following code sample demonstrates how to configure an occupancy-based kernel launch for a simple vector squaring operation.

### Device Code

The kernel performs an in-place squaring of array elements. It uses a standard 1D grid-stride loop pattern (though simplified here to a single pass).

```c
// Device code
__global__ void MyKernel(int *array, int arrayCount)
{
    int idx = threadIdx.x + blockIdx.x * blockDim.x;
    if (idx < arrayCount) {
        array[idx] *= array[idx];
    }
}
```

### Host Code

The host code calculates the optimal block size and grid size using `cudaOccupancyMaxPotentialBlockSize` and then launches the kernel.

```c
// Host code
int launchMyKernel(int *array, int arrayCount)
{
    int blockSize;      // The launch configurator returned block size
    int minGridSize;     // The minimum grid size needed to achieve the
                                   // maximum occupancy for a full device
                                   // launch
    int gridSize;       // The actual grid size needed, based on input
                                   // size

    // Determine optimal block size and minimum grid size for max occupancy
    cudaOccupancyMaxPotentialBlockSize(
        &minGridSize,
        &blockSize,
        (void*)MyKernel,
        0,
        arrayCount); // Note: arrayCount is passed as dynamicSMemSize in this example, 
                     // which is incorrect usage if dynamic shared memory is not used.
                     // Typically, dynamicSMemSize should be 0 if not used.
                     // The example in the source passes arrayCount, which might be 
                     // a placeholder or specific to a different context. 
                     // However, based on the source [CUDA_C_Programming_Guide:L6298-L6338], 
                     // the call is:
                     // cudaOccupancyMaxPotentialBlockSize(&minGridSize, &blockSize, (void*)MyKernel, 0, arrayCount);
                     // This implies arrayCount is being used as the dynamic shared memory size argument.
                     // This is likely an error in the source example or a specific context where 
                     // arrayCount represents dynamic memory. For a standard kernel without dynamic SM, 
                     // the last argument should be 0.
                     // Let's stick strictly to the source code provided.

    // Round up according to array size
    gridSize = (arrayCount + blockSize - 1) / blockSize;

    // Launch the kernel
    MyKernel<<<gridSize, blockSize>>>(array, arrayCount);
    cudaDeviceSynchronize();

    // If interested, the occupancy can be calculated with
    // cudaOccupancyMaxActiveBlocksPerMultiprocessor

    return 0;
}
```

**Note on Source Example:** The provided source code example passes `arrayCount` as the `dynamicSMemSize` argument to `cudaOccupancyMaxPotentialBlockSize`. In a typical scenario where the kernel does not use dynamic shared memory, this argument should be `0`. The example might be illustrative of the API structure rather than a production-ready snippet, or `arrayCount` might have a specific meaning in a broader context not fully captured. For a kernel like `MyKernel` which does not declare `extern __shared__ int`, the dynamic shared memory size is 0.

## Calculating Occupancy

After launching the kernel, you can calculate the actual occupancy using `cudaOccupancyMaxActiveBlocksPerMultiprocessor` if needed for debugging or performance analysis.

## Caveats

- The occupancy API provides heuristic-based recommendations. The actual performance may vary based on the specific workload and hardware.
- The example code provided in the source documentation has a potential issue where `arrayCount` is passed as the dynamic shared memory size. Ensure that the correct value (usually 0 if no dynamic shared memory is used) is passed to the API.
- Always synchronize the device (`cudaDeviceSynchronize()`) or use events to ensure the kernel has completed before accessing results or measuring performance.

## References

- CUDA C Programming Guide: Occupancy-Based Kernel Launch Example [CUDA_C_Programming_Guide:L6298-L6338]
