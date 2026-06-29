# CDP1 Launch Environment Configuration

In the Contextual Data Parallelism version 1 (CDP1) model, the launch environment configuration is inherited by child kernels from their parent kernel. This ensures that global device settings remain consistent across the execution hierarchy unless explicitly overridden by host-side configurations.

## Inheritance of Global Settings

All global device configuration settings are inherited from the parent kernel. This includes:

*   **Cache Configuration**: Settings such as shared memory and L1 cache size, as returned by `cudaDeviceGetCacheConfig()`.
*   **Device Limits**: Limits retrieved via `cudaDeviceGetLimit()`, including stack size, which remain as-configured.

## Host-Launched Kernel Precedence

For kernels launched from the host, per-kernel configurations set from the host take precedence over the global device settings. These host-specified configurations are preserved and used when the kernel is subsequently launched from the device (i.e., by a parent kernel).

## Immutability from Device

It is not possible to reconfigure a kernel’s environment from the device. Child kernels must operate within the constraints and configurations established by their parent or the initial host launch.

## See Also

*   Launch Environment Configuration (CDP2 version)

[doc_id:CUDA_C_Programming_Guide:L14523-L14531]
