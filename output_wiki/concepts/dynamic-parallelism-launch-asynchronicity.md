# Dynamic Parallelism Launch Asynchronicity

Identical to host-side launches, all device-side kernel launches are asynchronous with respect to the launching thread [CUDA_C_Programming_Guide:L13846-L13851].

## Behavior

When a kernel is launched from within a device-side kernel using the `<<<>>>` launch command, the command returns immediately [CUDA_C_Programming_Guide:L13846-L13851]. The launching thread continues its execution without waiting for the child grid to complete [CUDA_C_Programming_Guide:L13846-L13851].

The child grid launch is posted to the device and executes independently of the parent thread [CUDA_C_Programming_Guide:L13846-L13851]. The child grid may begin execution at any time after launch, but is not guaranteed to begin execution until the launching thread reaches an implicit launch-synchronization point [CUDA_C_Programming_Guide:L13846-L13851].

## Implicit Synchronization

The launching thread continues to execute until it hits an implicit launch-synchronization point [CUDA_C_Programming_Guide:L13846-L13851]. An example of such a point is a kernel launched into the `cudaStreamTailLaunch` stream [CUDA_C_Programming_Guide:L13846-L13851].

## Related Concepts

- **Dynamic Parallelism**: The ability of a CUDA kernel to launch other kernels.
- **Implicit Synchronization**: Points in execution where the host or device thread waits for previous operations to complete.
