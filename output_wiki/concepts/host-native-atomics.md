# Host Native Atomics

Host native atomics refer to hardware-accelerated atomic accesses to CPU-resident memory. This capability is supported by specific devices, particularly those connected via NVLink in hardware coherent systems [CUDA_C_Programming_Guide:L21750-L21752].

## Key Characteristics

*   **Hardware Acceleration**: The atomic operations are performed directly by the hardware rather than through software emulation [CUDA_C_Programming_Guide:L21750-L21752].
*   **No Page Fault Emulation**: Because the hardware supports these operations natively, atomic accesses to host memory do not need to be emulated using page faults [CUDA_C_Programming_Guide:L21750-L21752].

## Detection

To determine if a device supports host native atomics, query the device attribute `cudaDevAttrHostNativeAtomicSupported`. This attribute is set to `1` for devices that support this feature [CUDA_C_Programming_Guide:L21750-L21752].
