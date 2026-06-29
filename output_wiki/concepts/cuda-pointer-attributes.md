# CUDA Pointer Attributes

CUDA pointer attributes provide metadata about how a specific memory pointer was allocated or registered, rather than indicating the physical location where the memory resides [CUDA_C_Programming_Guide:L21105-L21167]. This distinction is critical for understanding memory management behavior in CUDA applications [CUDA_C_Programming_Guide:L21105-L21167].

## Checking Pointer Types

Programs can determine the type of memory a pointer addresses by calling `cudaPointerGetAttributes()` and inspecting the `type` field of the returned `cudaPointerAttributes` structure [CUDA_C_Programming_Guide:L21105-L21167].

The API returns one of the following memory type enumerations:

*   **`cudaMemoryTypeManaged`**: Indicates the pointer addresses a CUDA Managed Memory allocation [CUDA_C_Programming_Guide:L21105-L21167].
*   **`cudaMemoryTypeHost`**: Indicates the pointer addresses System-Allocated Memory that has been explicitly registered with `cudaHostRegister()` [CUDA_C_Programming_Guide:L21105-L21167].
*   **`cudaMemoryTypeDevice`**: Indicates the pointer addresses device memory (typically allocated via `cudaMalloc`) [CUDA_C_Programming_Guide:L21105-L21167].
*   **`cudaMemoryTypeUnregistered`**: Indicates the pointer addresses System-Allocated Memory that CUDA is unaware of (e.g., standard `malloc` or stack variables) [CUDA_C_Programming_Guide:L21105-L21167].

## Runtime Detection Example

The following example demonstrates how to detect the type of pointer at runtime and determine if the memory is "Unified" based on device attributes [CUDA_C_Programming_Guide:L21105-L21167].

```c
char const* kind(cudaPointerAttributes a, bool pma, bool cma) {
    switch(a.type) {
        case cudaMemoryTypeHost: return pma?
            "Unified: CUDA Host or Registered Memory" :
            "Not Unified: CUDA Host or Registered Memory";
        case cudaMemoryTypeDevice: return "Not Unified: CUDA Device Memory";
        case cudaMemoryTypeManaged: return cma?
            "Unified: CUDA Managed Memory" : "Not Unified: CUDA Managed Memory";
        case cudaMemoryTypeUnregistered: return pma?
            "Unified: System-Allocated Memory" :
            "Not Unified: System-Allocated Memory";
        default: return "unknown";
    }
}

void check_pointer(int i, void* ptr) {
    cudaPointerAttributes attr;
    cudaPointerGetAttributes(&attr, ptr);
    int pma = 0, cma = 0, device = 0;
    cudaGetDevice(&device);
    cudaDeviceGetAttribute(&pma, cudaDevAttrPageableMemoryAccess, device);
    cudaDeviceGetAttribute(&cma, cudaDevAttrConcurrentManagedAccess, device);
    printf("Pointer %d: memory is %s\n", i, kind(attr, pma, cma));
}

__managed__ int managed_var = 5;

int main() {
    int* ptr[5];
    ptr[0] = (int*)malloc(sizeof(int));
    cudaMallocManaged(&ptr[1], sizeof(int));
    cudaMallocHost(&ptr[2], sizeof(int));
    cudaMalloc(&ptr[3], sizeof(int));
    ptr[4] = &managed_var;

    for (int i = 0; i < 5; ++i) check_pointer(i, ptr[i]);

    cudaFree(ptr[3]);
    cudaFreeHost(ptr[2]);
    cudaFree(ptr[1]);
    free(ptr[0]);
    return 0;
}
```

In this example:
*   `ptr[0]` is standard system memory (`malloc`), resulting in `cudaMemoryTypeUnregistered` [CUDA_C_Programming_Guide:L21105-L21167].
*   `ptr[1]` is managed memory (`cudaMallocManaged`), resulting in `cudaMemoryTypeManaged` [CUDA_C_Programming_Guide:L21105-L21167].
*   `ptr[2]` is host memory registered with CUDA (`cudaMallocHost`), resulting in `cudaMemoryTypeHost` [CUDA_C_Programming_Guide:L21105-L21167].
*   `ptr[3]` is device memory (`cudaMalloc`), resulting in `cudaMemoryTypeDevice` [CUDA_C_Programming_Guide:L21105-L21167].
*   `ptr[4]` is a managed variable, resulting in `cudaMemoryTypeManaged` [CUDA_C_Programming_Guide:L21105-L21167].

The `kind` function further refines the output by checking device attributes `cudaDevAttrPageableMemoryAccess` and `cudaDevAttrConcurrentManagedAccess` to determine if the memory access is unified [CUDA_C_Programming_Guide:L21105-L21167].
