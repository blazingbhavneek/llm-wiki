# CUDA Versioning and Compatibility

When developing a CUDA application, developers must distinguish between two primary version numbers: the **Compute Capability** and the **CUDA Driver API version**.

## Compute Capability vs. Driver API Version

*   **Compute Capability**: Describes the general specifications and features of the compute device (GPU hardware) [CUDA_C_Programming_Guide:L6074-L6077].
*   **CUDA Driver API Version (`CUDA_VERSION`)**: Describes the features supported by the driver API and the CUDA runtime [CUDA_C_Programming_Guide:L6077-L6079]. This version is defined in the driver header file and allows developers to verify if their application requires a newer device driver than the one currently installed [CUDA_C_Programming_Guide:L6079-L6081].

## Compatibility Rules

The CUDA Driver API follows specific compatibility rules regarding software versions and driver installations [CUDA_C_Programming_Guide:L6081-L6083]:

### Backward and Forward Compatibility

*   **Backward Compatible**: Applications, plug-ins, and libraries (including the CUDA runtime) compiled against a specific version of the driver API will continue to work on subsequent (newer) device driver releases [CUDA_C_Programming_Guide:L6083-L6086].
*   **Not Forward Compatible**: Applications, plug-ins, and libraries compiled against a specific driver API version will **not** work on previous (older) versions of the device driver [CUDA_C_Programming_Guide:L6086-L6089].

### Installation and Mixing Constraints

Due to system limitations, the following constraints apply to version mixing [CUDA_C_Programming_Guide:L6090-L6091]:

1.  **Single Driver Installation**: Only one version of the CUDA Driver can be installed on a system at a time. Consequently, the installed driver must be of the same or higher version than the maximum Driver API version against which any application, plug-in, or library running on that system was built [CUDA_C_Programming_Guide:L6090-L6091].
2.  **Runtime Version Consistency**: All plug-ins and libraries used by an application must use the same version of the CUDA Runtime, unless they statically link to the Runtime. If statically linked, multiple versions of the runtime can coexist in the same process space [CUDA_C_Programming_Guide:L6091-L6093].
    *   By default, if `nvcc` is used to link the application, the static version of the CUDA Runtime library is used [CUDA_C_Programming_Guide:L6093-L6095].
    *   All CUDA Toolkit libraries are statically linked against the CUDA Runtime by default [CUDA_C_Programming_Guide:L6095-L6096].
3.  **Library Version Consistency**: All plug-ins and libraries used by an application must use the same version of any libraries that utilize the runtime (such as cuFFT, cuBLAS, etc.), unless those libraries are statically linked [CUDA_C_Programming_Guide:L6096-L6098].

## Forward-Compatible Upgrade Path

For Tesla GPU products, CUDA 10 introduced a new forward-compatible upgrade path for the usermode components of the CUDA Driver. This feature is described in the CUDA Compatibility documentation. The standard driver version requirements described above apply specifically to the version of the user-mode components [CUDA_C_Programming_Guide:L6098-L6101].

## References

*   Figure 26: The Driver API Is Backward but Not Forward Compatible [CUDA_C_Programming_Guide:L6099-L6100]
