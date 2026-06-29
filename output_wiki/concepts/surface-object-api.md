# Surface Object API

The Surface Object API provides mechanisms to create and manage surface objects, which enable read and write access to CUDA arrays. This API is distinct from the Texture Object API, primarily in how memory addresses are calculated.

## Creating Surface Objects

A surface object is created using the `cudaCreateSurfaceObject()` function. This function takes a resource description of type `struct cudaResourceDesc` as input [CUDA_C_Programming_Guide:L3879-L3974].

## Addressing: Byte vs. Element

Unlike texture memory, which uses element-based addressing, surface memory uses **byte addressing** [CUDA_C_Programming_Guide:L3879-L3974]. This distinction requires careful coordinate calculation when accessing elements:

*   **1D Arrays**: To access the element at texture coordinate `x` via a surface function, the x-coordinate must be multiplied by the byte size of the element [CUDA_C_Programming_Guide:L3879-L3974].
    *   *Example*: For a one-dimensional floating-point CUDA array, reading the element at coordinate `x` via a texture object `texObj` uses `tex1d(texObj, x)`. The same element is read via a surface object `surfObj` using `surf1Dread(surfObj, 4*x)`, assuming a 4-byte float [CUDA_C_Programming_Guide:L3879-L3974].

*   **2D Arrays**: For a two-dimensional floating-point CUDA array, the x-coordinate must be multiplied by the element size, while the y-coordinate is used directly [CUDA_C_Programming_Guide:L3879-L3974].
    *   *Example*: Accessing the element at texture coordinates `(x, y)` via `texObj` uses `tex2d(texObj, x, y)`. Via `surfObj`, it uses `surf2Dread(surfObj, 4*x, y)` [CUDA_C_Programming_Guide:L3879-L3974]. The byte offset for the y-coordinate is internally calculated from the underlying line pitch of the CUDA array [CUDA_C_Programming_Guide:L3879-L3974].

## Code Example: Surface Read/Write

The following code sample demonstrates a simple copy kernel that reads from an input surface and writes to an output surface. It illustrates the byte addressing requirement for `surf2Dread` and `surf2Dwrite`.

```cpp
// Simple copy kernel
__global__ void copyKernel(cudaSurfaceObject_t inputSurfObj,
                           cudaSurfaceObject_t outputSurfObj,
                           int width, int height)
{
    // Calculate surface coordinates
    unsigned int x = blockIdx.x * blockDim.x + threadIdx.x;
    unsigned int y = blockIdx.y * blockDim.y + threadIdx.y;
    if (x < width && y < height) {
        uchar4 data;
        // Read from input surface
        // Note: x * 4 is used because the element is uchar4 (4 bytes)
        surf2Dread(&data, inputSurfObj, x * 4, y);
        // Write to output surface
        surf2Dwrite(data, outputSurfObj, x * 4, y);
    }
}
```

### Host Code Setup

The host code allocates CUDA arrays with the `cudaArraySurfaceLoadStore` flag, creates the surface objects, and invokes the kernel [CUDA_C_Programming_Guide:L3879-L3974].

```c
// Host code
int main()
{
    const int height = 1024;
    const int width = 1024;

    // Allocate and set some host data
    unsigned char *h_data =
        (unsigned char *)std::malloc(sizeof(unsigned char) * width * height * 4);
    for (int i = 0; i < height * width * 4; ++i)
        h_data[i] = i;

    // Allocate CUDA arrays in device memory
    cudaChannelFormatDesc channelDesc =
        cudaCreateChannelDesc(8, 8, 8, 8, cudaChannelFormatKindUnsigned);
    cudaArray_t cuInputArray;
    cudaMallocArray(&cuInputArray, &channelDesc, width, height,
                             cudaArraySurfaceLoadStore);
    cudaArray_t cuOutputArray;
    cudaMallocArray(&cuOutputArray, &channelDesc, width, height,
                             cudaArraySurfaceLoadStore);

    // Set pitch of the source (the width in memory in bytes of the 2D array
    // pointed to by src, including padding), we dont have any padding
    const size_t spitch = 4 * width * sizeof(unsigned char);
    // Copy data located at address h_data in host memory to device memory
    cudaMemcpy2DToArray(cuInputArray, 0, 0, h_data, spitch,
                          4 * width * sizeof(unsigned char), height,
                          cudaMemcpyHostToDevice);

    // Specify surface
    struct cudaResourceDesc resDesc;
    memset(&resDesc, 0, sizeof(resDesc));
    resDesc.resType = cudaResourceTypeArray;

    // Create the surface objects
    resDesc.res.array.array = cuInputArray;
    cudaSurfaceObject_t inputSurfObj = 0;
    cudaCreateSurfaceObject(&inputSurfObj, &resDesc);
    resDesc.res.array.array = cuOutputArray;
    cudaSurfaceObject_t outputSurfObj = 0;
    cudaCreateSurfaceObject(&outputSurfObj, &resDesc);

    // Invoke kernel
    dim3 threadsperBlock(16, 16);
    dim3 numBlocks((width + threadsperBlock.x - 1) / threadsperBlock.x,
                         (height + threadsperBlock.y - 1) / threadsperBlock.y);
    copyKernel<<<numBlocks, threadsperBlock>>>(inputSurfObj, outputSurfObj, width,
                             height);

    // Copy data from device back to host
    cudaMemcpy2DFromArray(h_data, spitch, cuOutputArray, 0, 0,
                           4 * width * sizeof(unsigned char), height,
                           cudaMemcpyDeviceToHost);

    // Destroy surface objects
    cudaDestroySurfaceObject(inputSurfObj);
    cudaDestroySurfaceObject(outputSurfObj);

    // Free device memory
    cudaFreeArray(cuInputArray);
    cudaFreeArray(cuOutputArray);

    // Free host memory
    free(h_data);

    return 0;
}
```

## Caveats

*   The research report for this page was a deterministic fallback due to an input token limit error in the subagent. The content above is derived strictly from the assigned source evidence [CUDA_C_Programming_Guide:L3879-L3974].
*   When converting from texture coordinates to surface coordinates, always account for the byte size of the data type being accessed [CUDA_C_Programming_Guide:L3879-L3974].

## See Also

*   `cudaCreateSurfaceObject`
*   `cudaDestroySurfaceObject`
*   `surf1Dread`, `surf1Dwrite`
*   `surf2Dread`, `surf2Dwrite`
*   Texture Object API
