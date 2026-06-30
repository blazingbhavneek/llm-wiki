# CUDA Versioning and Compatibility

Explains the two key version numbers in CUDA development: compute capability (device features) and driver API version. Details backward compatibility (applications compiled against older API versions work on newer drivers) and lack of forward compatibility. Outlines rules for mixing driver/runtime versions and static linking of CUDA Toolkit libraries.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L6074-L6091

Citation: [CUDA_C_Programming_Guide:L6074-L6091]

````text
## 6.3. Versioning and Compatibility

There are two version numbers that developers should care about when developing a CUDA application: The compute capability that describes the general specifications and features of the compute device (see Compute Capability) and the version of the CUDA driver API that describes the features supported by the driver API and runtime.

The version of the driver API is defined in the driver header file as CUDA\_VERSION. It allows developers to check whether their application requires a newer device driver than the one currently installed. This is important, because the driver API is backward compatible, meaning that applications, plug-ins, and libraries (including the CUDA runtime) compiled against a particular version of the driver API will continue to work on subsequent device driver releases as illustrated in Figure 26. The driver API is not forward compatible, which means that applications, plug-ins, and libraries (including the CUDA runtime) compiled against a particular version of the driver API will not work on previous versions of the device driver.

It is important to note that there are limitations on the mixing and matching of versions that is supported:

▶ Since only one version of the CUDA Driver can be installed at a time on a system, the installed driver must be of the same or higher version than the maximum Driver API version against which any application, plug-ins, or libraries that must run on that system were built.

All plug-ins and libraries used by an application must use the same version of the CUDA Runtime unless they statically link to the Runtime, in which case multiple versions of the runtime can coexist in the same process space. Note that if nvcc is used to link the application, the static version of the CUDA Runtime library will be used by default, and all CUDA Toolkit libraries are statically linked against the CUDA Runtime.

▶ All plug-ins and libraries used by an application must use the same version of any libraries that use the runtime (such as cuFFT, cuBLAS, …) unless statically linking to those libraries.

![](images/41d1a47f290e3660757ade7c72c0559d2d09a7b17f0ee2bac8193b2d806bb163.jpg)  
Figure 26: The Driver API Is Backward but Not Forward Compatible

For Tesla GPU products, CUDA 10 introduced a new forward-compatible upgrade path for the usermode components of the CUDA Driver. This feature is described in CUDA Compatibility. The requirements on the CUDA Driver version described here apply to the version of the user-mode components.
````
