# Toolkit and Driver Compatibility

## Kernel Parameter Size Limits

To compile, launch, and debug kernels that accept parameters larger than 4KB, developers must use the CUDA 12.1 Toolkit and the r530 driver or higher [CUDA_C_Programming_Guide:L17149-L17151].

If kernels with parameters larger than 4KB are launched on older drivers, CUDA will issue the error `CUDA_ERROR_NOT_SUPPORTED` [CUDA_C_Programming_Guide:L17150-L17151].
