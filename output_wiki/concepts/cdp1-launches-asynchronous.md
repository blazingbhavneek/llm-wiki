# CDP1 Launches are Asynchronous

In CUDA Dynamic Parallelism version 1 (CDP1), device-side kernel launches behave identically to host-side launches: they are asynchronous with respect to the launching thread [CUDA_C_Programming_Guide:L14514-L14522].

## Behavior

When a device thread issues a kernel launch using the `<<<>>>` syntax, the launch command returns immediately [CUDA_C_Programming_Guide:L14514-L14522]. The launching thread continues to execute subsequent instructions without blocking [CUDA_C_Programming_Guide:L14514-L14522].

The child grid is posted to the device and executes independently of the parent thread [CUDA_C_Programming_Guide:L14514-L14522]. While the child grid may begin execution at any time after launch, it is not guaranteed to start until the launching thread reaches an explicit launch-synchronization point [CUDA_C_Programming_Guide:L14514-L14522].

## Synchronization

To ensure that a parent thread waits for child kernels to complete, explicit synchronization is required [CUDA_C_Programming_Guide:L14514-L14522]. The standard mechanism for this is `cudaDeviceSynchronize()` [CUDA_C_Programming_Guide:L14514-L14522].

### Deprecation Warning

Explicit synchronization with child kernels from a parent block (i.e., using `cudaDeviceSynchronize()` in device code) has undergone significant changes in recent CUDA versions:

*   **Deprecated**: In CUDA 11.6 [CUDA_C_Programming_Guide:L14514-L14522].
*   **Removed**: For compilation targeting compute capability 9.0 and higher [CUDA_C_Programming_Guide:L14514-L14522].
*   **Future**: Slated for full removal in a future CUDA release [CUDA_C_Programming_Guide:L14514-L14522].

Developers should be aware that relying on `cudaDeviceSynchronize()` for CDP1 synchronization is no longer supported on modern architectures and will be removed entirely in future releases [CUDA_C_Programming_Guide:L14514-L14522].

## Relation to CDP2

For the CDP2 version of this concept, see the "Launches are Asynchronous" section in the CDP2 documentation [CUDA_C_Programming_Guide:L14514-L14522].
