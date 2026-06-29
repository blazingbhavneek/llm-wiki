# Texture Object API

The Texture Object API allows CUDA applications to create and manage texture objects, which facilitate efficient texture sampling within device kernels. A texture object is created using the `cudaCreateTextureObject()` function, which takes a resource description and a texture description as input [CUDA_C_Programming_Guide:L3679-L3809].

## Structure Definitions

### Resource Description
The resource description is defined by the `struct cudaResourceDesc`, which specifies the underlying texture resource (such as a CUDA array) [CUDA_C_Programming_Guide:L3679-L3809].

### Texture Description
The texture description is defined by the `struct cudaTextureDesc`, which configures how the texture is sampled. The structure is defined as follows [CUDA_C_Programming_Guide:L3679-L3809]:

```txt
struct cudaTextureDesc
{
    enum cudaTextureAddressMode addressMode[3];
    enum cudaTextureFilterMode filterMode;
    enum cudaTextureReadMode readMode;
    int sRGB;
    int normalizedCoords;
    unsigned int maxAnisotropy;
    enum cudaTextureFilterMode mipmapFilterMode;
    float mipmapLevelBias;
    float minMipmapLevelClamp;
    float maxMipmapLevelClamp;
};
```

Key fields include [CUDA_C_Programming_Guide:L3679-L3809]:
*   `addressMode`: Specifies the addressing mode for texture coordinates.
*   `filterMode`: Specifies the filter mode (e.g., linear or point filtering).
*   `readMode`: Specifies the read mode (e.g., reading as the element type or as normalized integers).
*   `normalizedCoords`: Specifies whether texture coordinates are normalized (0.0 to 1.0) or not.
*   `sRGB`, `maxAnisotropy`, `mipmapFilterMode`, `mipmapLevelBias`, `minMipmapLevelClamp`, and `maxMipmapLevelClamp`: Additional parameters for advanced texture filtering and mipmap management, as detailed in the reference manual.

## Usage Example

The following code sample demonstrates how to create a texture object and use it in a transformation kernel. The kernel rotates a 2D image by applying a transformation to the texture coordinates before sampling [CUDA_C_Programming_Guide:L3679-L3809].

### Kernel Implementation

The `transformKernel` calculates normalized texture coordinates, applies a rotation transformation, and samples the texture using `tex2D` [CUDA_C_Programming_Guide:L3679-L3809]:

```lisp
// Simple transformation kernel
__global__ void transformKernel(float* output,
                             cudaTextureObject_t texObj,
                             int width, int height,
                             float theta)
{
    // Calculate normalized texture coordinates
    unsigned int x = blockIdx.x * blockDim.x + threadIdx.x;
    unsigned int y = blockIdx.y * blockDim.y + threadIdx.y;

    float u = x / (float)width;
    float v = y / (float)height;

    // Transform coordinates
    u -= 0.5f;
    v -= 0.5f;
    float tu = u * cosf(theta) - v * sinf(theta) + 0.5f;
    float tv = v * cosf(theta) + u * sinf(theta) + 0.5f;

    // Read from texture and write to global memory
    output[y * width + x] = tex2D<float>(texObj, tu, tv);
}
```

### Host Code Setup

The host code performs the following steps [CUDA_C_Programming_Guide:L3679-L3809]:

1.  **Allocate and Initialize Data**: Host data is allocated and initialized.
2.  **Create CUDA Array**: A CUDA array is allocated in device memory with a specific channel format (e.g., 32-bit float) [CUDA_C_Programming_Guide:L3679-L3809].
3.  **Copy Data**: Data is copied from host memory to the device array using `cudaMemcpy2DToArray` [CUDA_C_Programming_Guide:L3679-L3809].
4.  **Configure Resource Description**: The `cudaResourceDesc` is set up to point to the CUDA array [CUDA_C_Programming_Guide:L3679-L3809].
5.  **Configure Texture Description**: The `cudaTextureDesc` is initialized with parameters such as wrap addressing, linear filtering, and normalized coordinates [CUDA_C_Programming_Guide:L3679-L3809].
6.  **Create Texture Object**: `cudaCreateTextureObject` is called to create the texture object [CUDA_C_Programming_Guide:L3679-L3809].
7.  **Execute Kernel**: The transformation kernel is launched [CUDA_C_Programming_Guide:L3679-L3809].
8.  **Cleanup**: The texture object is destroyed, and memory is freed [CUDA_C_Programming_Guide:L3679-L3809].

```txt
// Specify texture object parameters
struct cudaTextureDesc texDesc;
memset(&texDesc, 0, sizeof(texDesc));
texDesc.addressMode[0] = cudaAddressModeWrap;
texDesc.addressMode[1] = cudaAddressModeWrap;
texDesc.filterMode = cudaFilterModeLinear;
texDesc.readMode = cudaReadModeElementType;
texDesc.normalizedCoords = 1;

// Create texture object
cudaTextureObject_t texObj = 0;
cudaCreateTextureObject(&texObj, &resDesc, &texDesc, NULL);

// ... (kernel launch and execution) ...

// Destroy texture object
cudaDestroyTextureObject(texObj);
```

## References

*   CUDA C Programming Guide: Texture Object API documentation [CUDA_C_Programming_Guide:L3679-L3809].
*   CUDA C Programming Guide: Additional texture parameters [CUDA_C_Programming_Guide:L3810-L3810].
