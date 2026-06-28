## 6.2.2. Device Memory

As mentioned in Heterogeneous Programming, the CUDA programming model assumes a system composed of a host and a device, each with their own separate memory. Kernels operate out of device memory, so the runtime provides functions to allocate, deallocate, and copy device memory, as well as transfer data between host memory and device memory.

Device memory can be allocated either as linear memory or as CUDA arrays.

CUDA arrays are opaque memory layouts optimized for texture fetching. They are described in Texture and Surface Memory.

Linear memory is allocated in a single unified address space, which means that separately allocated entities can reference one another via pointers, for example, in a binary tree or linked list. The size of the address space depends on the host system (CPU) and the compute capability of the used GPU:

Table 4: Linear Memory Address Space

<table><tr><td></td><td>x86_64 (AMD64)</td><td>POWER (ppc64le)</td><td>ARM64</td></tr><tr><td>up to compute capability 5.3 (Maxwell)</td><td>40bit</td><td>40bit</td><td>40bit</td></tr><tr><td>compute capability 6.0 (Pascal) or newer</td><td>up to 47bit</td><td>up to 49bit</td><td>up to 48bit</td></tr></table>

Note: On devices of compute capability 5.3 (Maxwell) and earlier, the CUDA driver creates an uncommitted 40bit virtual address reservation to ensure that memory allocations (pointers) fall into the supported range. This reservation appears as reserved virtual memory, but does not occupy any physical memory until the program actually allocates memory.

Linear memory is typically allocated using cudaMalloc() and freed using cudaFree() and data transfer between host memory and device memory are typically done using cudaMemcpy(). In the vector addition code sample of Kernels, the vectors need to be copied from host memory to device memory:

```lisp
// Device code
__global__ void VecAdd(float* A, float* B, float* C, int N)
{
    int i = blockDim.x * blockIdx.x + threadIdx.x;
    if (i < N)
        C[i] = A[i] + B[i];
}

// Host code
int main()
{
    int N = ...;
    size_t size = N * sizeof(float);

    // Allocate input vectors h_A and h_B in host memory
    float* h_A = (float*)malloc(size);
    float* h_B = (float*)malloc(size);
    float* h_C = (float*)malloc(size);

    // Initialize input vectors
    ...

    // Allocate vectors in device memory
    float* d_A;
    cudaMalloc(&d_A, size);
    float* d_B;
    cudaMalloc(&d_B, size);
    float* d_C;
    cudaMalloc(&d_C, size);

    // Copy vectors from host memory to device memory
    cudaMemcpy(d_A, h_A, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, size, cudaMemcpyHostToDevice);

    // Invoke kernel
    int threadsPerBlock = 256;
    int blocksPerGrid =
        (N + threadsPerBlock - 1) / threadsPerBlock;
```

(continued from previous page)

```c
VecAdd<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, N);

// Copy result from device memory to host memory
// h_C contains the result in host memory
cudaMemcpy(h_C, d_C, size, cudaMemcpyDeviceToHost);

// Free device memory
cudaFree(d_A);
cudaFree(d_B);
cudaFree(d_C);

// Free host memory
...
```

Linear memory can also be allocated through cudaMallocPitch() and cudaMalloc3D(). These functions are recommended for allocations of 2D or 3D arrays as it makes sure that the allocation is appropriately padded to meet the alignment requirements described in Device Memory Accesses, therefore ensuring best performance when accessing the row addresses or performing copies between 2D arrays and other regions of device memory (using the cudaMemcpy2D() and cudaMemcpy3D() functions). The returned pitch (or stride) must be used to access array elements. The following code sample allocates a width x height 2D array of floating-point values and shows how to loop over the array elements in device code:

```c
// Host code
int width = 64, height = 64;
float* devPtr;
size_t pitch;
cudaMallocPitch(&devPtr, &pitch,
                    width * sizeof(float), height);
MyKernel<<<100, 512>>>(devPtr, pitch, width, height);

// Device code
__global__ void MyKernel(float* devPtr,
                       size_t pitch, int width, int height)
{
    for (int r = 0; r < height; ++r) {
        float* row = (float*)(char*)devPtr + r * pitch);
        for (int c = 0; c < width; ++c) {
            float element = row[c];
        }
    }
}
```

The following code sample allocates a width x height x depth 3D array of floating-point values and shows how to loop over the array elements in device code:

```c
// Host code
int width = 64, height = 64, depth = 64;
cudaExtent extent = make_cudaExtent(width * sizeof(float),
                             height, depth);
cudaPitchedPtr devPitchedPtr;
cudaMalloc3D(&devPitchedPtr, extent);
MyKernel<<<100, 512>>>(devPitchedPtr, width, height, depth);

// Device code
```

(continues on next page)

```lisp
__global__ void MyKernel(cudaPitchedPtr devPitchedPtr,
                          int width, int height, int depth)
{
    char* devPtr = devPitchedPtr.ptr;
    size_t pitch = devPitchedPtr.pitch;
    size_t slicePitch = pitch * height;
    for (int z = 0; z < depth; ++z) {
        char* slice = devPtr + z * slicePitch;
        for (int y = 0; y < height; ++y) {
            float* row = (float*)(slice + y * pitch);
            for (int x = 0; x < width; ++x) {
                float element = row[x];
            }
        }
    }
}
```

(continued from previous page)

Note: To avoid allocating too much memory and thus impacting system-wide performance, request the allocation parameters from the user based on the problem size. If the allocation fails, you can fallback to other slower memory types (cudaMallocHost(), cudaHostRegister(), etc.), or return an error telling the user how much memory was needed that was denied. If your application cannot request the allocation parameters for some reason, we recommend using cudaMallocManaged() for platforms that support it.

The reference manual lists all the various functions used to copy memory between linear memory allocated with cudaMalloc(), linear memory allocated with cudaMallocPitch() or cudaMalloc3D(), CUDA arrays, and memory allocated for variables declared in global or constant memory space.

The following code sample illustrates various ways of accessing global variables via the runtime API:

```lisp
__constant__ float constData[256];
float data[256];
cudaMemcpyToSymbol(constData, data, sizeof(data));
cudaMemcpyFromSymbol(data, constData, sizeof(data));

__device__ float devData;
float value = 3.14f;
cudaMemcpyToSymbol(devData, &value, sizeof(float));

__device__ float* devPointer;
float* ptr;
cudaMalloc(&ptr, 256 * sizeof(float));
cudaMemcpyToSymbol(devPointer, &ptr, sizeof(ptr));
```

cudaGetSymbolAddress() is used to retrieve the address pointing to the memory allocated for a variable declared in global memory space. The size of the allocated memory is obtained through cudaGetSymbolSize().

## 6.2.3. Device Memory L2 Access Management

When a CUDA kernel accesses a data region in the global memory repeatedly, such data accesses can be considered to be persisting. On the other hand, if the data is only accessed once, such data accesses can be considered to be streaming.

Starting with CUDA 11.0, devices of compute capability 8.0 and above have the capability to influence persistence of data in the L2 cache, potentially providing higher bandwidth and lower latency accesses to global memory.

## 6.2.3.1 L2 Cache Set-Aside for Persisting Accesses

A portion of the L2 cache can be set aside to be used for persisting data accesses to global memory. Persisting accesses have prioritized use of this set-aside portion of L2 cache, whereas normal or streaming, accesses to global memory can only utilize this portion of L2 when it is unused by persisting accesses.

The L2 cache set-aside size for persisting accesses may be adjusted, within limits:

```txt
cudaGetDeviceProperties(&prop, device_id);
size_t size = min(int(prop.l2CacheSize * 0.75), prop.persistingL2CacheMaxSize);
cudaDeviceSetLimit(cudaLimitPersistingL2CacheSize, size); /* set-aside 3/4 of L2 cache
    for persisting accesses or the max allowed*/
```

When the GPU is configured in Multi-Instance GPU (MIG) mode, the L2 cache set-aside functionality is disabled.

When using the Multi-Process Service (MPS), the L2 cache set-aside size cannot be changed by cudaDeviceSetLimit. Instead, the set-aside size can only be specified at start up of MPS server through the environment variable CUDA\_DEVICE\_DEFAULT\_PERSISTING\_L2\_CACHE\_PERCENTAGE\_LIMIT.

## 6.2.3.2 L2 Policy for Persisting Accesses

An access policy window specifies a contiguous region of global memory and a persistence property in the L2 cache for accesses within that region.

The code example below shows how to set an L2 persisting access window using a CUDA Stream.

## CUDA Stream Example

```cpp
cudaStreamAttrValue stream_attribute;
    // Stream level attributes data structure
stream_attribute.accessPolicyWindow.base_ptr = reinterpret_cast<void*>(ptr); //
    // Global Memory data pointer
stream_attribute.accessPolicyWindow.num_bytes = num_bytes;
    // Number of bytes for persistence access.
    // (Must be less than cudaDeviceProp::accessPolicyMaxWindowSize)
stream_attribute.accessPolicyWindow.hitRatio = 0.6;
    // Hint for cache hit ratio
stream_attribute.accessPolicyWindow.hitProp = cudaAccessPropertyPersisting; // Type of access property on cache hit
stream_attribute.accessPolicyWindow.missProp = cudaAccessPropertyStreaming; // Type of access property on cache miss.
```

```txt
(continues on next page)
```

(continued from previous page)

```txt
//Set the attributes to a CUDA stream of type cudaStream_t
cudaStreamSetAttribute(stream, cudaStreamAttributeAccessPolicyWindow, &stream_
attribute);
```

When a kernel subsequently executes in CUDA stream, memory accesses within the global memory extent [ptr..ptr+num\_bytes) are more likely to persist in the L2 cache than accesses to other global memory locations.

L2 persistence can also be set for a CUDA Graph Kernel Node as shown in the example below:

## CUDA GraphKernelNode Example

```cpp
cudaKernelNodeAttrValue node_attribute; // Kernel
level attributes data structure
node_attribute.accessPolicyWindow.base_ptr = reinterpret_cast<void*>(ptr); // Global
Memory data pointer
node_attribute.accessPolicyWindow.num_bytes = num_bytes; // Number
of bytes for persistence access.
// (Must
be less than cudaDeviceProp::accessPolicyMaxWindowSize)
node_attribute.accessPolicyWindow.hitRatio = 0.6; // Hint
for cache hit ratio
node_attribute.accessPolicyWindow.hitProp = cudaAccessPropertyPersisting; // Type of
access property on cache hit
node_attribute.accessPolicyWindow.missProp = cudaAccessPropertyStreaming; // Type of
access property on cache miss.

//Set the attributes to a CUDA Graph Kernel node of type cudaGraphNode_t
cudaGraphKernelNodeSetAttribute(node, cudaKernelNodeAttributeAccessPolicyWindow, &
node_attribute);
```

The hitRatio parameter can be used to specify the fraction of accesses that receive the hitProp property. In both of the examples above, 60% of the memory accesses in the global memory region [ptr..ptr+num\_bytes) have the persisting property and 40% of the memory accesses have the streaming property. Which specific memory accesses are classified as persisting (the hitProp) is random with a probability of approximately hitRatio; the probability distribution depends upon the hardware architecture and the memory extent.

For example, if the L2 set-aside cache size is 16KB and the num\_bytes in the accessPolicyWindow is 32KB:

▶ With a hitRatio of 0.5, the hardware will select, at random, 16KB of the 32KB window to be designated as persisting and cached in the set-aside L2 cache area.

With a hitRatio of 1.0, the hardware will attempt to cache the whole 32KB window in the setaside L2 cache area. Since the set-aside area is smaller than the window, cache lines will be evicted to keep the most recently used 16KB of the 32KB data in the set-aside portion of the L2 cache.

The hitRatio can therefore be used to avoid thrashing of cache lines and overall reduce the amount of data moved into and out of the L2 cache.

A hitRatio value below 1.0 can be used to manually control the amount of data diferent accessPolicyWindows from concurrent CUDA streams can cache in L2. For example, let the L2 set-aside cache size be 16KB; two concurrent kernels in two diferent CUDA streams, each with a 16KB accessPolicyWindow, and both with hitRatio value 1.0, might evict each others’ cache lines when competing for the shared L2 resource. However, if both accessPolicyWindows have a hitRatio value of 0.5, they will be less likely to evict their own or each others’ persisting cache lines.

## 6.2.3.3 L2 Access Properties

Three types of access properties are defined for diferent global memory data accesses:

1. cudaAccessPropertyStreaming: Memory accesses that occur with the streaming property are less likely to persist in the L2 cache because these accesses are preferentially evicted.

2. cudaAccessPropertyPersisting: Memory accesses that occur with the persisting property are more likely to persist in the L2 cache because these accesses are preferentially retained in the set-aside portion of L2 cache.

3. cudaAccessPropertyNormal: This access property forcibly resets previously applied persisting access property to a normal status. Memory accesses with the persisting property from previous CUDA kernels may be retained in L2 cache long after their intended use. This persistenceafter-use reduces the amount of L2 cache available to subsequent kernels that do not use the persisting property. Resetting an access property window with the cudaAccessPropertyNormal property removes the persisting (preferential retention) status of the prior access, as if the prior access had been without an access property.

## 6.2.3.4 L2 Persistence Example

The following example shows how to set-aside L2 cache for persistent accesses, use the set-aside L2 cache in CUDA kernels via CUDA Stream and then reset the L2 cache.

```txt
cudaStream_t stream;
cudaStreamCreate(&stream);
    // Create CUDA stream

cudaDeviceProp prop;
    // CUDA device properties variable
cudaGetDeviceProperties( &prop, device_id);
    // Query GPU properties
size_t size = min( int(prop.l2CacheSize * 0.75) , prop.persistingL2CacheMaxSize );
cudaDeviceSetLimit( cudaLimitPersistingL2CacheSize, size);
    // set-aside 3/4 of L2 cache for persisting accesses or the max allowed

size_t window_size = min(prop.accessPolicyMaxWindowSize, num_bytes);
    // Select minimum of user defined num_bytes and max window size.

cudaStreamAttrValue stream_attribute;
    // Stream level attributes data structure
stream_attribute.accessPolicyWindow.base_ptr = reinterpret_cast<void*>(data1);
    // Global Memory data pointer
stream_attribute.accessPolicyWindow.num_bytes = window_size;
    // Number of bytes for persistence access
stream_attribute.accessPolicyWindow.hitRatio = 0.6;
    // Hint for cache hit ratio
stream_attribute.accessPolicyWindow.hitProp = cudaAccessPropertyPersisting;
    // Persistence Property
stream_attribute.accessPolicyWindow.missProp = cudaAccessPropertyStreaming;
    // Type of access property on cache miss

cudaStreamSetAttribute(stream, cudaStreamAttributeAccessPolicyWindow, &stream_
attribute);   // Set the attributes to a CUDA Stream

for(int i = 0; i < 10; i++) {
```

(continues on next page)

```cpp
cuda_kernelA<<<grid_size,block_size,0,stream>>>(data1);
// This data1 is used by a kernel multiple times
}
// [data1 + num_bytes) benefits from L2 persistence
cuda_kernelB<<<grid_size,block_size,0,stream>>>(data1);
// A different kernel in the same stream can also benefit

// from the persistence of data1

stream_attribute.accessPolicyWindow.num_bytes = 0;
// Setting the window size to 0 disable it
cudaStreamSetAttribute(stream, cudaStreamAttributeAccessPolicyWindow, &stream_
attribute); // Overwrite the access policy attribute to a CUDA Stream
cudaCtxResetPersistingL2Cache();
// Remove any persistent lines in L2

cuda_kernelC<<<grid_size,block_size,0,stream>>>(data2);
// data2 can now benefit from full L2 in normal mode
```

## 6.2.3.5 Reset L2 Access to Normal

A persisting L2 cache line from a previous CUDA kernel may persist in L2 long after it has been used. Hence, a reset to normal for L2 cache is important for streaming or normal memory accesses to utilize the L2 cache with normal priority. There are three ways a persisting access can be reset to normal status.

1. Reset a previous persisting memory region with the access property, cudaAccessPropertyNormal.

2. Reset all persisting L2 cache lines to normal by calling cudaCtxResetPersistingL2Cache().

3. Eventually untouched lines are automatically reset to normal. Reliance on automatic reset is strongly discouraged because of the undetermined length of time required for automatic reset to occur.

## 6.2.3.6 Manage Utilization of L2 set-aside cache

Multiple CUDA kernels executing concurrently in diferent CUDA streams may have a diferent access policy window assigned to their streams. However, the L2 set-aside cache portion is shared among all these concurrent CUDA kernels. As a result, the net utilization of this set-aside cache portion is the sum of all the concurrent kernels’ individual use. The benefits of designating memory accesses as persisting diminish as the volume of persisting accesses exceeds the set-aside L2 cache capacity.

To manage utilization of the set-aside L2 cache portion, an application must consider the following:

Size of L2 set-aside cache.

CUDA kernels that may concurrently execute.

▶ The access policy window for all the CUDA kernels that may concurrently execute.

▶ When and how L2 reset is required to allow normal or streaming accesses to utilize the previously set-aside L2 cache with equal priority.

## 6.2.3.7 Query L2 cache Properties

Properties related to L2 cache are a part of cudaDeviceProp struct and can be queried using CUDA runtime API cudaGetDeviceProperties

CUDA Device Properties include:

l2CacheSize: The amount of available L2 cache on the GPU.

persistingL2CacheMaxSize: The maximum amount of L2 cache that can be set-aside for persisting memory accesses.

▶ accessPolicyMaxWindowSize: The maximum size of the access policy window.

## 6.2.3.8 Control L2 Cache Set-Aside Size for Persisting Memory Access

The L2 set-aside cache size for persisting memory accesses is queried using CUDA runtime API cudaDeviceGetLimit and set using CUDA runtime API cudaDeviceSetLimit as a cudaLimit. The maximum value for setting this limit is cudaDeviceProp::persistingL2CacheMaxSize.

```txt
enum cudaLimit {
    /* other fields not shown */
    cudaLimitPersistingL2CacheSize
};
```
