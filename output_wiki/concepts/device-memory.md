# Device Memory

In the CUDA programming model, the system is composed of a host (CPU) and a device (GPU), each possessing its own separate memory [CUDA_C_Programming_Guide:L1249-L1253]. Kernels execute on the device and operate directly out of device memory [CUDA_C_Programming_Guide:L1253]. The CUDA runtime provides functions to allocate, deallocate, and copy device memory, as well as to transfer data between host memory and device memory [CUDA_C_Programming_Guide:L1253].

## Allocation Types

Device memory can be allocated in two primary forms: linear memory and CUDA arrays [CUDA_C_Programming_Guide:L1255].

### Linear Memory

Linear memory is allocated in a single unified address space [CUDA_C_Programming_Guide:L1260]. This allows separately allocated memory entities to reference one another via pointers, enabling structures such as binary trees or linked lists [CUDA_C_Programming_Guide:L1260].

#### Address Space Size

The size of the linear memory address space depends on the host system architecture and the compute capability of the GPU [CUDA_C_Programming_Guide:L1262].

| Compute Capability | x86_64 (AMD64) | POWER (ppc64le) | ARM64 |
| :--- | :--- | :--- | :--- |
| Up to 5.3 (Maxwell) | 40-bit | 40-bit | 40-bit |
| 6.0 (Pascal) or newer | Up to 47-bit | Up to 49-bit | Up to 48-bit |

On devices with compute capability 5.3 (Maxwell) and earlier, the CUDA driver creates an uncommitted 40-bit virtual address reservation to ensure that memory allocations fall within the supported range [CUDA_C_Programming_Guide:L1270]. This reservation appears as reserved virtual memory but does not occupy physical memory until the program actually allocates memory [CUDA_C_Programming_Guide:L1272].

#### Allocation Functions

Linear memory is typically allocated using `cudaMalloc()` and freed using `cudaFree()` [CUDA_C_Programming_Guide:L1274]. For 2D or 3D arrays, `cudaMallocPitch()` and `cudaMalloc3D()` are recommended [CUDA_C_Programming_Guide:L1315]. These functions ensure that allocations are appropriately padded to meet alignment requirements, ensuring best performance when accessing row addresses or performing copies between 2D/3D arrays and other regions of device memory [CUDA_C_Programming_Guide:L1315].

*   **`cudaMallocPitch`**: Allocates a 2D array with a specified pitch (stride) [CUDA_C_Programming_Guide:L1320]. The returned pitch must be used to access array elements in device code [CUDA_C_Programming_Guide:L1320].
*   **`cudaMalloc3D`**: Allocates a 3D array using a `cudaExtent` structure [CUDA_C_Programming_Guide:L1335]. It returns a `cudaPitchedPtr` containing the pointer, pitch, and slice pitch [CUDA_C_Programming_Guide:L1340].

#### Best Practices

To avoid impacting system-wide performance by allocating excessive memory, applications should request allocation parameters based on the problem size [CUDA_C_Programming_Guide:L1350]. If an allocation fails, the application should fallback to other slower memory types (e.g., `cudaMallocHost()`, `cudaHostRegister()`) or return an error indicating the required memory size [CUDA_C_Programming_Guide:L1350]. For platforms supporting it, `cudaMallocManaged()` is recommended if allocation parameters cannot be determined in advance [CUDA_C_Programming_Guide:L1352].

### CUDA Arrays

CUDA arrays are opaque memory layouts optimized for texture fetching [CUDA_C_Programming_Guide:L1257]. They are described in detail in the Texture and Surface Memory documentation [CUDA_C_Programming_Guide:L1259].

## Data Transfer

Data transfer between host memory and device memory is typically performed using `cudaMemcpy()` [CUDA_C_Programming_Guide:L1274]. Specific functions exist for transferring data to and from linear memory allocated with `cudaMallocPitch()` or `cudaMalloc3D()`, such as `cudaMemcpy2D()` and `cudaMemcpy3D()` [CUDA_C_Programming_Guide:L1315].

## Global and Constant Memory Variables

Global (`__device__`) and constant (`__constant__`) variables declared in device code can be accessed from the host using the CUDA runtime API [CUDA_C_Programming_Guide:L1355].

*   **`cudaMemcpyToSymbol`**: Copies data from host memory to a global or constant variable [CUDA_C_Programming_Guide:L1360].
*   **`cudaMemcpyFromSymbol`**: Copies data from a global or constant variable to host memory [CUDA_C_Programming_Guide:L1360].
*   **`cudaGetSymbolAddress`**: Retrieves the address pointing to the memory allocated for a variable declared in global memory space [CUDA_C_Programming_Guide:L1375].
*   **`cudaGetSymbolSize`**: Obtains the size of the allocated memory for a symbol [CUDA_C_Programming_Guide:L1375].

### Example: Accessing Global Variables

```c
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

The reference manual lists all various functions used to copy memory between linear memory, CUDA arrays, and memory allocated for variables in global or constant memory space [CUDA_C_Programming_Guide:L1355].
