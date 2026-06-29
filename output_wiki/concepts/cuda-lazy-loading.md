# CUDA Lazy Loading

CUDA Lazy Loading (also known as Lazy Kernel Loading) is a mechanism that defers the loading of device code (kernels) until they are actually invoked. This approach can improve application startup time and reduce memory footprint by avoiding the immediate loading of all device code at initialization.

## Version Support

Support for Lazy Loading depends on the versions of the CUDA Driver, Toolkit, and Compiler used:

*   **Driver**: Specific driver versions are required to support the lazy loading mechanism.
*   **Toolkit**: The CUDA Toolkit version must support the feature.
*   **Compiler**: The NVCC compiler must be configured to generate code compatible with lazy loading.

## Triggering Loading

Kernels in lazy mode are loaded upon their first invocation. The mechanism for triggering this loading differs between the CUDA Driver API and the CUDA Runtime API:

*   **CUDA Driver API**: Loading is triggered when a kernel is launched via the driver API.
*   **CUDA Runtime API**: Loading is triggered when a kernel is launched via the runtime API.

## Querying Status

Developers can query whether Lazy Loading is currently turned on for the application context. This allows for debugging and verification of the loading behavior.

## Potential Issues

Adopting Lazy Loading may introduce specific issues related to concurrent execution, memory allocators, and autotuning:

### Concurrent Execution

Care must be taken when using Lazy Loading with concurrent execution contexts. Since code is loaded on-demand, race conditions or unexpected delays may occur if multiple threads or streams attempt to load the same kernel simultaneously.

### Allocators

Memory allocation behavior may be affected. Allocators might need to handle the dynamic loading of code, potentially impacting performance or memory management strategies.

### Autotuning

Autotuning mechanisms may need to account for the time taken to load kernels. If autotuning involves launching kernels to measure performance, the initial launch may include loading overhead, skewing results.

## References

*   [CUDA_C_Programming_Guide:L724-L736]
