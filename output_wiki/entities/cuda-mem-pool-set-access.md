# cudaMemPoolSetAccess

The `cudaMemPoolSetAccess` function is used to control accessibility of imported memory pools across different GPUs within a process. This is particularly relevant when importing memory pools from other processes or devices, as the default accessibility rules restrict access to the resident device.

## Default Accessibility

When a memory pool is imported, it is initially only accessible from its resident device. The imported memory pool does not inherit any accessibility settings that were configured by the exporting process [CUDA_C_Programming_Guide:L15756-L15761].

## Enabling Access

To allow a GPU to access an imported memory pool, the importing process must explicitly enable access using `cudaMemPoolSetAccess` for any GPU it plans to use to access the memory [CUDA_C_Programming_Guide:L15756-L15761].

This step is mandatory if the imported memory pool belongs to a device that is not visible to the importing process by default. In such cases, the user must use the `cudaMemPoolSetAccess` API to enable access from the specific GPUs where the allocations will be used [CUDA_C_Programming_Guide:L15756-L15761].
