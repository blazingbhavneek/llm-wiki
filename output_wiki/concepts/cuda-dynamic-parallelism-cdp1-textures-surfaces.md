# CUDA Dynamic Parallelism (CDP1) Textures and Surfaces

In the context of CUDA Dynamic Parallelism version 1 (CDP1), support for textures and surfaces differs from later versions (CDP2) and standard host-device interactions. The primary distinction lies in the lifecycle management of these objects and their availability across kernel launch hierarchies.

## Dynamic Texture and Surface Objects

CUDA supports dynamically created texture and surface objects in CDP1 [CUDA_C_Programming_Guide:L14594-L14601]. These objects follow a specific lifecycle and usage pattern:

*   **Creation and Destruction**: Texture and surface objects must be created and destroyed on the host. The device runtime does not allow the creation or destruction of texture or surface objects from within device code [CUDA_C_Programming_Guide:L14594-L14601].
*   **Usage**: Once created on the host, these objects may be passed to a kernel, used by that kernel, and then destroyed from the host [CUDA_C_Programming_Guide:L14594-L14601].
*   **Device Scope**: Although created on the host, texture and surface objects created from the host may be used and passed around freely on the device [CUDA_C_Programming_Guide:L14594-L14601].
*   **Child Kernels**: Regardless of where they are created, dynamically created texture objects are always valid and may be passed to child kernels from a parent kernel [CUDA_C_Programming_Guide:L14594-L14601].

## Legacy Module-Scope Textures

A significant limitation in CDP1 concerns legacy module-scope textures, also referred to as Fermi-style textures and surfaces [CUDA_C_Programming_Guide:L14594-L14601].

*   **Restriction**: The device runtime does not support legacy module-scope textures and surfaces within a kernel launched from the device [CUDA_C_Programming_Guide:L14594-L14601].
*   **Top-Level Only**: Module-scope (legacy) textures may be created from the host and used in device code, but they may only be used by a top-level kernel (i.e., the one which is launched from the host) [CUDA_C_Programming_Guide:L14594-L14601].

For details on texture and surface support in CDP2, refer to the corresponding CDP2 documentation sections [CUDA_C_Programming_Guide:L14594-L14601].
