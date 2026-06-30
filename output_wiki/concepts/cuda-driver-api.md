# CUDA Driver API

Overview of the low-level handle-based imperative API (cu* prefix), object model (devices, contexts, modules, kernels, memory, streams, events), initialization requirements, PTX vs binary loading, and a complete host code example for kernel execution.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L20059-L20154

Citation: [CUDA_C_Programming_Guide:L20059-L20154]

````text
# Chapter 21. Driver API

Warning: This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA.

This section assumes knowledge of the concepts described in CUDA Runtime.

The driver API is implemented in the cuda dynamic library (cuda.dll or cuda.so) which is copied on the system during the installation of the device driver. All its entry points are prefixed with cu.

It is a handle-based, imperative API: Most objects are referenced by opaque handles that may be specified to functions to manipulate the objects.

The objects available in the driver API are summarized in Table 28.

Table 28: Objects Available in the CUDA Driver API

<table><tr><td>Object</td><td>Handle</td><td>Description</td></tr><tr><td>Device</td><td>CUdevice</td><td>CUDA-enabled device</td></tr><tr><td>Context</td><td>CUcontext</td><td>Roughly equivalent to a CPU process</td></tr><tr><td>Module</td><td>CUmodule</td><td>Roughly equivalent to a dynamic library</td></tr><tr><td>Function</td><td>CUfunction</td><td>Kernel</td></tr><tr><td>Heap memory</td><td>CUdevi-ceptr</td><td>Pointer to device memory</td></tr><tr><td>CUDA array</td><td>CUarray</td><td>Opaque container for one-dimensional or two-dimensional data on the device, readable via texture or surface references</td></tr><tr><td>Texture object</td><td>CUtexref</td><td>Object that describes how to interpret texture memory data</td></tr><tr><td>Surface reference</td><td>CUsurfref</td><td>Object that describes how to read or write CUDA arrays</td></tr><tr><td>Stream</td><td>CUs-stream</td><td>Object that describes a CUDA stream</td></tr><tr><td>Event</td><td>CUevent</td><td>Object that describes a CUDA event</td></tr></table>

The driver API must be initialized with cuInit() before any function from the driver API is called. A CUDA context must then be created that is attached to a specific device and made current to the calling host thread as detailed in Context.

Within a CUDA context, kernels are explicitly loaded as PTX or binary objects by the host code as described in Module. Kernels written in C++ must therefore be compiled separately into PTX or binary objects. Kernels are launched using API entry points as described in Kernel Execution.

Any application that wants to run on future device architectures must load PTX, not binary code. This is because binary code is architecture-specific and therefore incompatible with future architectures, whereas PTX code is compiled to binary code at load time by the device driver.

Here is the host code of the sample from Kernels written using the driver API:

```c
int main()
{
    int N = ...;
    size_t size = N * sizeof(float);

    // Allocate input vectors h_A and h_B in host memory
    float* h_A = (float*)malloc(size);
    float* h_B = (float*)malloc(size);

    // Initialize input vectors
    ...

    // Initialize
    cuInit(0);

    // Get number of devices supporting CUDA
    int deviceCount = 0;
    cuDeviceGetCount(&deviceCount);
    if (deviceCount == 0) {
        printf("There is no device supporting CUDA.\n");
        exit (0);
    }

    // Get handle for device 0
    CUdevice cuDevice;
    cuDeviceGet(&cuDevice, 0);

    // Create context
    CUcontext cuContext;
    cuCtxCreate(&cuContext, NULL, 0, cuDevice);

    // Create module from binary file
    CUmodule cuModule;
    cuModuleLoad(&cuModule, "VecAdd.ptx");

    // Allocate vectors in device memory
    CUdeviceptr d_A;
    cuMemAlloc(&d_A, size);
    CUdeviceptr d_B;
    cuMemAlloc(&d_B, size);
    CUdeviceptr d_C;
    cuMemAlloc(&d_C, size);

    // Copy vectors from host memory to device memory
    cuMemcpyHtoD(d_A, h_A, size);
```

(continued from previous page)

```txt
cuMemcpyHtoD(d_B, h_B, size);

// Get function handle from module
CUfunction vecAdd;
cuModuleGetFunction(&vecAdd, cuModule, "VecAdd");

// Invoke kernel
int threadsPerBlock = 256;
int blocksPerGrid =
    (N + threadsPerBlock - 1) / threadsPerBlock;
void* args[] = { &d_A, &d_B, &d_C, &N };
cuLaunchKernel(vecAdd,
              blocksPerGrid, 1, 1, threadsPerBlock, 1, 1,
              0, 0, args, 0);

...
}
```

Full code can be found in the vectorAddDrv CUDA sample.
````
