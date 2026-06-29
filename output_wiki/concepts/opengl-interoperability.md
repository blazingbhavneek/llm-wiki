# OpenGL Interoperability

OpenGL interoperability allows OpenGL resources to be mapped into the address space of CUDA, enabling direct read and write access from CUDA kernels or memory copy operations. The supported OpenGL resources are buffer, texture, and renderbuffer objects [CUDA_C_Programming_Guide:L4003-L4116].

## Registration and Mapping

To use an OpenGL resource in CUDA, it must first be registered with the CUDA graphics API. The method of registration depends on the resource type [CUDA_C_Programming_Guide:L4003-L4116]:

*   **Buffer Objects**: Registered using `cudaGraphicsGLRegisterBuffer()`. In CUDA, the buffer appears as a device pointer, allowing kernels to read and write to it directly or via `cudaMemcpy()` calls [CUDA_C_Programming_Guide:L4003-L4116].
*   **Texture and Renderbuffer Objects**: Registered using `cudaGraphicsGLRegisterImage()`. In CUDA, these appear as CUDA arrays. Kernels can read from the array by binding it to a texture or surface reference. Writing is possible via surface write functions if the resource is registered with the `cudaGraphicsRegisterFlagsSurfaceLoadStore` flag. Additionally, the array can be read and written via `cudaMemcpy2D()` calls [CUDA_C_Programming_Guide:L4003-L4116].

### Supported Formats

`cudaGraphicsGLRegisterImage()` supports texture formats with 1, 2, or 4 components and internal types of [CUDA_C_Programming_Guide:L4003-L4116]:

*   **Float**: e.g., `GL_RGBA_FLOAT32`
*   **Normalized Integer**: e.g., `GL_RGBA8`, `GL_INTENSITY16`
*   **Unnormalized Integer**: e.g., `GL_RGBA8UI` (requires OpenGL 3.0; these can only be written by shaders, not the fixed-function pipeline) [CUDA_C_Programming_Guide:L4003-L4116]

## Prerequisites and Constraints

### Context Currentness
The OpenGL context whose resources are being shared must be current to the host thread making any OpenGL interoperability API calls [CUDA_C_Programming_Guide:L4003-L4116].

### Bindless Textures
When an OpenGL texture is made bindless (e.g., by requesting an image or texture handle using `glGetTextureHandle*` or `glGetImageHandle*` APIs), it cannot be registered with CUDA. The application must register the texture for interop *before* requesting an image or texture handle [CUDA_C_Programming_Guide:L4003-L4116].

### Hardware and Performance
On Windows and for Quadro GPUs, `cudaWGLGetDevice()` can be used to retrieve the CUDA device associated with the handle returned by `wglEnumGpusNV()`. Quadro GPUs offer higher performance OpenGL interoperability than GeForce and Tesla GPUs in multi-GPU configurations where OpenGL rendering is performed on the Quadro GPU and CUDA computations are performed on other GPUs in the system [CUDA_C_Programming_Guide:L4003-L4116].

## Example: Modifying Vertex Buffers

The following code sample demonstrates using a kernel to dynamically modify a 2D width x height grid of vertices stored in a vertex buffer object (VBO) [CUDA_C_Programming_Guide:L4003-L4116].

### Initialization and Registration

```c
GLuint positionsVBO;
struct cudaGraphicsResource* positionsVBO_CUDA;

int main()
{
    // Initialize OpenGL and GLUT for device 0
    // and make the OpenGL context current
    ...
    glutDisplayFunc(display);

    // Explicitly set device 0
    cudaSetDevice(0);

    // Create buffer object and register it with CUDA
    glGenBuffers(1, &positionsVBO);
    glBindBuffer(GL_ARRAY_BUFFER, positionsVBO);
    unsigned int size = width * height * 4 * sizeof(float);
    glBufferData(GL_ARRAY_BUFFER, size, 0, GL_DYNAMIC_DRAW);
    glBindBuffer(GL_ARRAY_BUFFER, 0);

    cudaGraphicsGLRegisterBuffer(&positionsVBO_CUDA,
                          positionsVBO,
                          cudaGraphicsMapFlagsWriteDiscard);

    // Launch rendering loop
    glutMainLoop();

    ...
}
```

### Rendering Loop

```c
void display()
{
    // Map buffer object for writing from CUDA
    float4* positions;
    cudaGraphicsMapResources(1, &positionsVBO_CUDA, 0);
    size_t num_bytes;
    cudaGraphicsResourceGetMappedPointer((void*)&positions,
                           &num_bytes,
                           positionsVBO_CUDA));

    // Execute kernel
    dim3 dimBlock(16, 16, 1);
    dim3 dimGrid(width / dimBlock.x, height / dimBlock.y, 1);
    createVertices<<<dimGrid, dimBlock>>>(positions, time,
                           width, height);

    // Unmap buffer object
    cudaGraphicsUnmapResources(1, &positionsVBO_CUDA, 0);

    // Render from buffer object
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glBindBuffer(GL_ARRAY_BUFFER, positionsVBO);
    glVertexPointer(4, GL_FLOAT, 0, 0);
    glEnableClientState(GL_VERTEX_ARRAY);
    glDrawArrays(GL_POINTS, 0, width * height);
    glDisableClientState(GL_VERTEX_ARRAY);

    // Swap buffers
    glutSwapBuffers();
    glutPostRedisplay();
}
```

### Cleanup

```c
void deleteVBO()
{
    cudaGraphicsUnregisterResource(positionsVBO_CUDA);
    glDeleteBuffers(1, &positionsVBO);
}
```

### Kernel Implementation

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

    // calculate simple sine wave pattern
    float freq = 4.0f;
    float w = sinf(u * freq + time)
           * cosf(v * freq + time) * 0.5f;

    // Write positions
    positions[y * width + x] = make_float4(u, w, v, 1.0f);
}
```
