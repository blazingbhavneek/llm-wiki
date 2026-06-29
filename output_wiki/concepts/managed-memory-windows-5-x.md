# Managed Memory on Windows or Compute Capability 5.x

Devices with compute capability lower than 6.0 or Windows platforms support CUDA Managed Memory v1.0 with limited support for data migration and coherency as well as memory oversubscription [CUDA_C_Programming_Guide:L21822-L21828]. The following sub-sections describe in more detail how to use and optimize Managed Memory on these platforms [CUDA_C_Programming_Guide:L21822-L21828].

## Key Limitations

*   **Data Migration**: Support for automatic data migration between host and device memory is limited [CUDA_C_Programming_Guide:L21822-L21828].
*   **Coherency**: Hardware/software coherency support is limited [CUDA_C_Programming_Guide:L21822-L21828].
*   **Oversubscription**: Support for memory oversubscription is limited [CUDA_C_Programming_Guide:L21822-L21828].

## Platform Specifics

### Windows Platforms

On Windows, the Unified Memory implementation is restricted to version 1.0 of the Managed Memory API [CUDA_C_Programming_Guide:L21822-L21828]. Developers must account for the limited coherency and migration capabilities when optimizing applications [CUDA_C_Programming_Guide:L21822-L21828].

### Compute Capability 5.x Devices

Devices with compute capability lower than 6.0 (including Compute Capability 5.x) also support Managed Memory v1.0 but with the same limitations regarding data migration, coherency, and oversubscription [CUDA_C_Programming_Guide:L21822-L21828]. Optimization strategies specific to these hardware constraints are detailed in the associated sub-sections of the programming guide [CUDA_C_Programming_Guide:L21822-L21828].
