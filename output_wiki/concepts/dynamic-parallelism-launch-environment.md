# Dynamic Parallelism Launch Environment Configuration

In the context of CUDA dynamic parallelism, the launch environment configuration determines how resources such as shared memory, cache, and device limits are allocated for kernels launched from the device.

## Inheritance of Global Settings

When a kernel is launched from the device (a child kernel), it inherits global device configuration settings from the parent kernel's context. This includes:

*   **Cache Configuration**: Settings such as shared memory and L1 cache size, as returned by `cudaDeviceGetCacheConfig()`.
*   **Device Limits**: Limits such as stack size, which remain as-configured in the parent context.

## Host-Launch Precedence

For kernels that are launched from the host, per-kernel configurations set via the host API take precedence over the global device settings. These host-specified configurations are also applied when the same kernel is subsequently launched from the device via dynamic parallelism.

## Immutability from Device

It is not possible to reconfigure a kernel’s environment from the device. Once a kernel is launched, its configuration is fixed based on the inheritance rules and host-level overrides described above.

## References

- Global device configuration settings (shared memory, L1 cache, limits) are inherited from the parent [CUDA_C_Programming_Guide:L13853-L13857].
- Per-kernel configurations set from the host take precedence over global settings and apply to device-launched instances [CUDA_C_Programming_Guide:L13853-L13857].
- Reconfiguring a kernel’s environment from the device is not possible [CUDA_C_Programming_Guide:L13853-L13857].
