# CUDA Direct3D 11 Interoperability

CUDA Direct3D 11 interoperability enables the integration of CUDA compute capabilities with Direct3D 11 rendering pipelines. This allows applications to share resources, such as vertex buffers, between the GPU compute context (CUDA) and the graphics context (Direct3D 11).

## Device Selection

To establish interoperability, a CUDA device must be associated with a specific Direct3D 11 adapter. This is typically achieved by enumerating available adapters using the DXGI factory and identifying the one that supports CUDA.

1.  Create a DXGI factory using `CreateDXGIFactory` [CUDA_C_Programming_Guide:L4377-L4506].
2.  Enumerate adapters using `IDXGIFactory::EnumAdapters` [CUDA_C_Programming_Guide:L4377-L4506].
3.  For each adapter, call `cudaD3D11GetDevice` to check if it corresponds to a valid CUDA device [CUDA_C_Programming_Guide:L4377-L4506].
4.  Once a compatible adapter is found, create the Direct3D 11 device and swap chain using `D3D11CreateDeviceAndSwapChain` [CUDA_C_Programming_Guide:L4377-L4506].
5.  Set the current CUDA device using `cudaSetDevice` with the device ID obtained from the adapter [CUDA_C_Programming_Guide:L4377-L4506].

## Resource Registration

Before a Direct3D 11 resource (e.g., a buffer, texture, or surface) can be accessed by CUDA, it must be registered with the CUDA graphics interoperability API. This creates a CUDA graphics resource handle that manages the lifecycle and synchronization of the underlying D3D11 resource.

*   Use `cudaGraphicsD3D11RegisterResource` to register the D3D11 resource [CUDA_C_Programming_Guide:L4377-L4506].
*   Specify registration flags, such as `cudaGraphicsRegisterFlagsNone`, to define how the resource is handled [CUDA_C_Programming_Guide:L4377-L4506].
*   Optionally, set mapping flags using `cudaGraphicsResourceSetMapFlags` to control memory behavior during mapping, such as `cudaGraphicsMapFlagsWriteDiscard` for buffers that will be overwritten [CUDA_C_Programming_Guide:L4377-L4506].

## Mapping and Kernel Execution

To access the registered resource from CUDA kernels, the resource must be mapped into the CUDA address space. This process synchronizes the resource between the D3D11 and CUDA contexts.

1.  **Map Resources**: Call `cudaGraphicsMapResources` to map the registered CUDA graphics resource [CUDA_C_Programming_Guide:L4377-L4506].
2.  **Get Pointer**: Use `cudaGraphicsResourceGetMappedPointer` to retrieve the device pointer to the mapped resource [CUDA_C_Programming_Guide:L4377-L4506].
3.  **Execute Kernel**: Launch the CUDA kernel using the obtained pointer. For example, a kernel might update vertex positions based on time and grid coordinates [CUDA_C_Programming_Guide:L4377-L4506].
4.  **Unmap Resources**: Call `cudaGraphicsUnmapResources` to unmap the resource, making it available for the D3D11 device to use [CUDA_C_Programming_Guide:L4377-L4506].

## Unregistration

When the resource is no longer needed, it must be unregistered from the CUDA graphics API to release associated resources and prevent leaks.

*   Call `cudaGraphicsUnregisterResource` with the CUDA graphics resource handle [CUDA_C_Programming_Guide:L4377-L4506].
*   Release the Direct3D 11 resource using its `Release` method [CUDA_C_Programming_Guide:L4377-L4506].

## Example Implementation

The following code snippet illustrates the typical workflow for creating a vertex buffer, registering it with CUDA, mapping it, updating it via a kernel, and cleaning up.

### Setup and Registration

```c
// Define vertex structure
struct CUSTOMVERTEX {
    FLOAT x, y, z;
    DWORD color;
};

// Declare D3D11 and CUDA resources
ID3D11Buffer* positionsVB;
struct cudaGraphicsResource* positionsVB_CUDA;

// ... (Device creation and selection code) ...

// Create vertex buffer
unsigned int size = width * height * sizeof(CUSTOMVERTEX);
D3D11_BUFFER_DESC bufferDesc;
bufferDesc.Usage          = D3D11_USAGE_DEFAULT;
bufferDesc.ByteWidth      = size;
bufferDesc.BindFlags       = D3D11_BIND_VERTEX_BUFFER;
bufferDesc.CPUAccessFlags = 0;
bufferDesc.MiscFlags     = 0;
device->CreateBuffer(&bufferDesc, 0, &positionsVB);

// Register with CUDA
cudaGraphicsD3D11RegisterResource(&positionsVB_CUDA,
                                   positionsVB,
                                   cudaGraphicsRegisterFlagsNone);
cudaGraphicsResourceSetMapFlags(positionsVB_CUDA,
                                   cudaGraphicsMapFlagsWriteDiscard);
```

### Rendering Loop

```cpp
void Render()
{
    // Map vertex buffer for writing from CUDA
    float4* positions;
    cudaGraphicsMapResources(1, &positionsVB_CUDA, 0);
    size_t num_bytes;
    cudaGraphicsResourceGetMappedPointer((void**)&positions,
                                         &num_bytes,
                                         positionsVB_CUDA));

    // Execute kernel
    dim3 dimBlock(16, 16, 1);
    dim3 dimGrid(width / dimBlock.x, height / dimBlock.y, 1);
    createVertices<<<dimGrid, dimBlock>>>(positions, time,
                                          width, height);

    // Unmap vertex buffer
    cudaGraphicsUnmapResources(1, &positionsVB_CUDA, 0);

    // Draw and present
    // ...
}
```

### Kernel Definition

```cpp
__global__ void createVertices(float4* positions, float time,
                               unsigned int width, unsigned int height)
{
    unsigned int x = blockIdx.x * blockDim.x + threadIdx.x;
    unsigned int y = blockIdx.y * blockDim.y + threadIdx.y;

    // Calculate uv coordinates
    float u = x / (float)width;
    float v = y / (float)height;
    u = u * 2.0f - 1.0f;
    v = v * 2.0f - 1.0f;

    // Calculate simple sine wave pattern
    float freq = 4.0f;
    float w = sinf(u * freq + time)
              * cosf(v * freq + time) * 0.5f;

    // Write positions
    positions[y * width + x] =
        make_float4(u, w, v, __int_as_float(0xff00ff00));
}
```

### Cleanup

```cpp
void releaseVB()
{
    cudaGraphicsUnregisterResource(positionsVB_CUDA);
    positionsVB->Release();
}
```
