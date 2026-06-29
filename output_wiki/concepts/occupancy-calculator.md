# Occupancy Calculator API

The Occupancy Calculator API consists of several functions designed to assist programmers in selecting optimal thread block sizes and cluster sizes based on the register and shared memory requirements of a kernel [CUDA_C_Programming_Guide:L6241-L6243].

## Functions

### cudaOccupancyMaxActiveBlocksPerMultiprocessor

This function provides an occupancy prediction based on the block size and shared memory usage of a kernel [CUDA_C_Programming_Guide:L6244-L6245]. It reports occupancy in terms of the number of concurrent thread blocks that can run per multiprocessor [CUDA_C_Programming_Guide:L6246].

### cudaOccupancyMaxPotentialBlockSize

This is an occupancy-based launch configurator API that heuristically calculates an execution configuration to achieve maximum multiprocessor-level occupancy [CUDA_C_Programming_Guide:L6250].

### cudaOccupancyMaxPotentialBlockSizeVariableSMem

Similar to `cudaOccupancyMaxPotentialBlockSize`, this function heuristically calculates an execution configuration for maximum multiprocessor-level occupancy, specifically handling variable shared memory requirements [CUDA_C_Programming_Guide:L6250].

### cudaOccupancyMaxActiveClusters

This function provides an occupancy prediction based on the cluster size, block size, and shared memory usage of a kernel [CUDA_C_Programming_Guide:L6252]. It reports occupancy in terms of the maximum number of active clusters of a given size that can run on the GPU present in the system [CUDA_C_Programming_Guide:L6253].

## Calculating Occupancy Percentage

The value returned by `cudaOccupancyMaxActiveBlocksPerMultiprocessor` can be converted into other metrics, such as occupancy percentage [CUDA_C_Programming_Guide:L6247-L6249]. The process involves:

1.  Multiplying the number of active blocks by the number of warps per block to get the number of concurrent warps per multiprocessor [CUDA_C_Programming_Guide:L6248].
2.  Dividing the concurrent warps by the maximum warps per multiprocessor to obtain the occupancy as a percentage [CUDA_C_Programming_Guide:L6249].

### Example

The following code sample demonstrates how to calculate and print the occupancy percentage for a kernel named `MyKernel`.

```cpp
// Device code
__global__ void MyKernel(int *d, int *a, int *b)
{
    int idx = threadIdx.x + blockIdx.x * blockDim.x;
    d[idx] = a[idx] * b[idx];
}

// Host code
int main()
{
    int numBlocks;          // Occupancy in terms of active blocks
    int blockSize = 32;

    // These variables are used to convert occupancy to warps
    int device;
    cudaDeviceProp prop;
    int activeWarps;
    int maxWarps;

    cudaGetDevice(&device);
    cudaGetDeviceProperties(&prop, device);

    cudaOccupancyMaxActiveBlocksPerMultiprocessor(
        &numBlocks,
        MyKernel,
        blockSize,
        0);

    activeWarps = numBlocks * blockSize / prop.warpSize;
    maxWarps = prop.maxThreadsPerMultiProcessor / prop.warpSize;

    std::cout << "Occupancy: " << (double)activeWarps / maxWarps * 100 << "%" <<
std::endl;

    return 0;
}
```

In this example, `numBlocks` is retrieved from `cudaOccupancyMaxActiveBlocksPerMultiprocessor`. The number of active warps is calculated by multiplying `numBlocks` by the block size and dividing by the warp size. The maximum warps per multiprocessor is derived from the device properties. Finally, the occupancy percentage is printed [CUDA_C_Programming_Guide:L6255-L6296].
