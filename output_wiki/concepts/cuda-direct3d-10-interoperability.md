# CUDA Direct3D 10 Interoperability

CUDA Direct3D 10 interoperability enables applications to share graphics resources between the Direct3D 10 API and the CUDA runtime. This allows CUDA kernels to read from or write to Direct3D 10 resources, such as vertex buffers, facilitating hybrid rendering and compute workflows.

## Device Selection

To use Direct3D 10 interoperability, the application must first identify a CUDA-enabled Direct3D 10 adapter. This is typically done using the DXGI factory to enumerate adapters and checking each one with `cudaD3D10GetDevice` [CUDA_C_Programming_Guide:L4250-L4275]. Once a suitable adapter is found, the corresponding CUDA device is selected using `cudaSetDevice` [CUDA_C_Programming_Guide:L4275-L4280].

## Resource Registration

Direct3D 10 resources must be registered with the CUDA graphics interop layer before they can be accessed by CUDA. This is achieved using the `cudaGraphicsD3D10RegisterResource` function [CUDA_C_Programming_Guide:L4280-L4285]. During registration, flags can be specified to define the intended usage of the resource, such as `cudaGraphicsRegisterFlagsNone` or `cudaGraphicsMapFlagsWriteDiscard` [CUDA_C_Programming_Guide:L4285-L4290].

## Mapping and Kernel Execution

Before a CUDA kernel can access a registered resource, it must be mapped. The `cudaGraphicsMapResources` function is used to map the resource, making it available to the CUDA runtime [CUDA_C_Programming_Guide:L4290-L4295]. Once mapped, the application retrieves a pointer to the resource's memory using `cudaGraphicsResourceGetMappedPointer` [CUDA_C_Programming_Guide:L4295-L4300].

After obtaining the pointer, a CUDA kernel can be launched to process the data. For example, a kernel might generate vertex positions based on mathematical functions like sine and cosine waves [CUDA_C_Programming_Guide:L4300-L4325].

## Unmapping and Unregistration

After the CUDA kernel execution is complete, the resource must be unmapped using `cudaGraphicsUnmapResources` to release the CUDA mapping [CUDA_C_Programming_Guide:L4325-L4330]. Finally, when the resource is no longer needed, it should be unregistered from the CUDA interop layer using `cudaGraphicsUnregisterResource` to clean up the association [CUDA_C_Programming_Guide:L4330-L4335].

## Example Workflow

The following C++ code snippet illustrates the typical workflow for Direct3D 10 interoperability:

1.  **Initialize DXGI and find CUDA device:**
    ```c
    IDXGIFactory* factory;
    CreateDXGIFactory(__uuidof(IDXGIFactory), (void**)&factory);
    IDXGIAdapter* adapter = 0;
    for (unsigned int i = 0; !adapter; ++i) {
        if (FAILED(factory->EnumAdapters(i, &adapter)))
            break;
        if (cudaD3D10GetDevice(&dev, adapter) == cudaSuccess)
            break;
    }
    factory->Release();
    ```

2.  **Create Direct3D 10 device and buffer:**
    ```c
    D3D10CreateDeviceAndSwapChain(adapter,
                        D3D10_DRIVER_TYPE_HARDWARE, 0,
                        D3D10_CREATE_DEVICE_DEBUG,
                        D3D10_SDK_VERSION,
                        &swapChainDesc, &swapChain,
                        &device);
    adapter->Release();
    cudaSetDevice(dev);

    unsigned int size = width * height * sizeof(CUSTOMVERTEX);
    D3D10_BUFFER_DESC bufferDesc;
    bufferDesc.Usage          = D3D10_USAGE_DEFAULT;
    bufferDesc.ByteWidth      = size;
    bufferDesc.BindFlags     = D3D10_BIND_VERTEX_BUFFER;
    bufferDesc.CPUAccessFlags = 0;
    bufferDesc.MiscFlags     = 0;
    device->CreateBuffer(&bufferDesc, 0, &positionsVB);
    ```

3.  **Register resource with CUDA:**
    ```c
    cudaGraphicsD3D10RegisterResource(&positionsVB_CUDA,
                                   positionsVB,
                                   cudaGraphicsRegisterFlagsNone);
    cudaGraphicsResourceSetMapFlags(positionsVB_CUDA,
                                   cudaGraphicsMapFlagsWriteDiscard);
    ```

4.  **Map, Execute Kernel, Unmap:**
    ```c
    float4* positions;
    cudaGraphicsMapResources(1, &positionsVB_CUDA, 0);
    size_t num_bytes;
    cudaGraphicsResourceGetMappedPointer((void**)&positions,
                             &num_bytes,
                             positionsVB_CUDA));

    dim3 dimBlock(16, 16, 1);
    dim3 dimGrid(width / dimBlock.x, height / dimBlock.y, 1);
    createVertices<<<dimGrid, dimBlock>>>(positions, time, width, height);

    cudaGraphicsUnmapResources(1, &positionsVB_CUDA, 0);
    ```

5.  **Cleanup:**
    ```c
    cudaGraphicsUnregisterResource(positionsVB_CUDA);
    positionsVB->Release();
    ```

## Kernel Example

A typical kernel for generating vertex data might look like this:

```c
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
