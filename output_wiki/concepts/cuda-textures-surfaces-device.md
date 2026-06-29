# CUDA Textures and Surfaces on Device

CUDA supports dynamically created texture and surface objects, which allow for flexible management of texture resources across host and device boundaries. These objects enable a workflow where a texture object is created on the host, passed to a kernel, used by that kernel, and then destroyed from the host.

## Dynamic Texture Objects

Dynamically created texture objects offer specific capabilities regarding their lifecycle and usage:

*   **Host-Created, Device-Used**: A texture object may be created on the host, passed to a kernel, used by that kernel, and then destroyed from the host [CUDA_C_Programming_Guide:L13971-L13976].
*   **Device Runtime Restrictions**: The device runtime does not allow the creation or destruction of texture or surface objects from within device code [CUDA_C_Programming_Guide:L13971-L13976].
*   **Device Usage**: Texture and surface objects created from the host may be used and passed around freely on the device [CUDA_C_Programming_Guide:L13971-L13976].
*   **Child Kernel Support**: Regardless of where they are created, dynamically created texture objects are always valid and may be passed to child kernels from a parent [CUDA_C_Programming_Guide:L13971-L13976].

## Legacy Module-Scope Textures

The device runtime imposes restrictions on legacy module-scope (i.e., Fermi-style) textures and surfaces:

*   **No Device-Side Launch Support**: The device runtime does not support legacy module-scope textures and surfaces within a kernel launched from the device [CUDA_C_Programming_Guide:L13971-L13976].
*   **Top-Level Kernel Only**: Module-scope (legacy) textures may be created from the host and used in device code as for any kernel, but may only be used by a top-level kernel (i.e., the one which is launched from the host) [CUDA_C_Programming_Guide:L13971-L13976].
