# Direct3D 9 Interoperability

Direct3D 9 interoperability enables CUDA applications to access and modify Direct3D 9 resources, such as vertex buffers, allowing for dynamic geometry updates driven by GPU kernels. This process involves initializing a Direct3D device, identifying a CUDA-enabled adapter, registering the Direct3D resource with the CUDA graphics interop layer, and mapping the resource for kernel execution.

## Initialization and Adapter Selection

To establish interoperability, the application must first initialize the Direct3D 9 API and identify an adapter that supports CUDA. This is typically done by iterating through available adapters and checking for CUDA support using `cudaD3D9GetDevice` [CUDA_C_Programming_Guide:L4129-L4249].

```c
IDirect3D9* D3D;
IDirect3DDevice9* device;

int main()
{
    int dev;
    // Initialize Direct3D
    D3D = Direct3DCreate9Ex(D3D_SDK_VERSION);

    // Get a CUDA-enabled adapter
    unsigned int adapter = 0;
    for (; adapter < g_pD3D->GetAdapterCount(); adapter++) {
        D3DADAPTER_IDENTIFIER9 adapterId;
        g_pD3D->GetAdapterIdentifier(adapter, 0, &adapterId);
        if (cudaD3D9GetDevice(&dev, adapterId.DeviceName)
            == cudaSuccess)
            break;
    }
    // ... create device ...
}
```

Once a suitable adapter is found, the Direct3D device is created using `CreateDeviceEx`, and the corresponding CUDA device is set using `cudaSetDevice` [CUDA_C_Programming_Guide:L4129-L4249].

```c
// Create device
D3D->CreateDeviceEx(adapter, D3DDEVTYPE_HAL, hWnd,
                    D3DCREATE_HARDWARE_VERTEXPROCESSING,
                    &params, NULL, &device);

// Use the same device
cudaSetDevice(dev);
```

## Vertex Buffer Registration

Direct3D 9 vertex buffers can be registered with CUDA to allow kernel access. The buffer is created using the Direct3D device, and then registered using `cudaGraphicsD3D9RegisterResource` [CUDA_C_Programming_Guide:L4129-L4249].

```c
struct CUSTOMVERTEX {
    FLOAT x, y, z;
    DWORD color;
};

IDirect3DVertexBuffer9* positionsVB;
struct cudaGraphicsResource* positionsVB_CUDA;

// Create vertex buffer and register it with CUDA
unsigned int size = width * height * sizeof(CUSTOMVERTEX);
device->CreateVertexBuffer(size, 0, D3DFVF_CUSTOMVERTEX,
                           D3DPOOL_DEFAULT, &positionsVB, 0);
cudaGraphicsD3D9RegisterResource(&positionsVB_CUDA,
                           positionsVB,
                           cudaGraphicsRegisterFlagsNone);
cudaGraphicsResourceSetMapFlags(positionsVB_CUDA,
                           cudaGraphicsMapFlagsWriteDiscard);
```

## Mapping and Kernel Execution

To modify the vertex buffer from CUDA, the resource must be mapped using `cudaGraphicsMapResources`. This provides a pointer to the memory that can be passed to a CUDA kernel. After the kernel execution, the resource is unmapped using `cudaGraphicsUnmapResources` [CUDA_C_Programming_Guide:L4129-L4249].

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
}
```

### Kernel Example

The following kernel demonstrates how to calculate and write vertex positions based on a sine wave pattern. It calculates UV coordinates, applies a time-based frequency shift, and writes the resulting position and color to the buffer [CUDA_C_Programming_Guide:L4129-L4249].

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

## Cleanup

When the application terminates or the resource is no longer needed, the CUDA resource must be unregistered, and the Direct3D vertex buffer released [CUDA_C_Programming_Guide:L4129-L4249].

```cpp
void releaseVB()
{
    cudaGraphicsUnregisterResource(positionsVB_CUDA);
    positionsVB->Release();
}
```
