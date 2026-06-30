# Runtime Detection of Unified Memory Support Level

Provides a code example demonstrating how to query device attributes (cudaDevAttrPageableMemoryAccess, cudaDevAttrConcurrentManagedAccess) at runtime to determine the level of Unified Memory support available on the system.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L21168-L21188

Citation: [CUDA_C_Programming_Guide:L21168-L21188]

````text
## 24.1.2.6 Runtime detection of Unified Memory Support Level

The following example shows how to detect the Unified Memory support level at runtime:

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
````
