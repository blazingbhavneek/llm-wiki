# Runtime Detection of Unified Memory Support Level

Unified Memory support can be detected at runtime by querying device attributes. This allows applications to determine the capabilities of the GPU regarding managed memory access.

## Detection Method

The support level is determined by checking two specific device attributes using `cudaDeviceGetAttribute`:

1. **`cudaDevAttrPageableMemoryAccess`**: Indicates whether the device supports full Unified Memory support, meaning pageable memory can be accessed by both the CPU and GPU.
2. **`cudaDevAttrConcurrentManagedAccess`**: Indicates whether the device supports CUDA Managed Memory with full support, implying concurrent access capabilities.

## Example Implementation

The following C code demonstrates how to query these attributes for the current device:

```c
int main() {
    int d;
    cudaGetDevice(&d);

    int pma = 0;
    cudaDeviceGetAttribute(&pma, cudaDevAttrPageableMemoryAccess, d);
    printf("Full Unified Memory Support: %s\n", pma == 1? "YES" : "NO");

    int cma = 0;
    cudaDeviceGetAttribute(&cma, cudaDevAttrConcurrentManagedAccess, d);
    printf("CUDA Managed Memory with full support: %s\n", cma == 1? "YES" : "NO");

    return 0;
}
```

In this example, a value of `1` for the attribute indicates that the specific support level is present, while any other value indicates it is not [CUDA_C_Programming_Guide:L21168-L21188].
