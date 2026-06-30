# CUDA Driver Entry Point Access

Provides APIs (cuGetProcAddress, cudaGetDriverEntryPointByVersion) to retrieve driver function addresses dynamically. Covers versioned typedefs, ABI compatibility, per-thread default stream variants, and accessing newer driver features without toolkit updates.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L20353-L20555

Citation: [CUDA_C_Programming_Guide:L20353-L20555]

````text
## 21.5. Driver Entry Point Access

## 21.5.1. Introduction

The Driver Entry Point Access APIs provide a way to retrieve the address of a CUDA driver function. Starting from CUDA 11.3, users can call into available CUDA driver APIs using function pointers obtained from these APIs.

These APIs provide functionality similar to their counterparts, dlsym on POSIX platforms and GetProcAddress on Windows. The provided APIs will let users:

▶ Retrieve the address of a driver function using the CUDA Driver API.

▶ Retrieve the address of a driver function using the CUDA Runtime API.

Request per-thread default stream version of a CUDA driver function. For more details, see Retrieve Per-thread Default Stream Versions.

▶ Access new CUDA features on older toolkits but with a newer driver.

## 21.5.2. Driver Function Typedefs

To help retrieve the CUDA Driver API entry points, the CUDA Toolkit provides access to headers containing the function pointer definitions for all CUDA driver APIs. These headers are installed with the CUDA Toolkit and are made available in the toolkit’s include∕ directory. The table below summarizes the header files containing the typedefs for each CUDA API header file.

Table 29: Typedefs header files for CUDA driver APIs

<table><tr><td>API header file</td><td>API Typedef header file</td></tr><tr><td>cuda.h</td><td>cudaTypedefs.h</td></tr><tr><td>cudaGL.h</td><td>cudaGLTypedefs.h</td></tr><tr><td>cudaProfiler.h</td><td>cudaProfilerTypedefs.h</td></tr><tr><td>cudaVDPAU.h</td><td>cudaVDPAUTypedefs.h</td></tr><tr><td>cudaEGL.h</td><td>cudaEGLTypedefs.h</td></tr><tr><td>cudaD3D9.h</td><td>cudaD3D9Typedefs.h</td></tr><tr><td>cudaD3D10.h</td><td>cudaD3D10Typedefs.h</td></tr><tr><td>cudaD3D11.h</td><td>cudaD3D11Typedefs.h</td></tr></table>

The above headers do not define actual function pointers themselves; they define the typedefs for function pointers. For example, cudaTypedefs.h has the below typedefs for the driver API cuMemAlloc:

```c
typedef CUresult (CUDAAPI *PFN_cuMemAlloc_v3020)(CUdeviceptr_v2 *dptr, size_t
bytesize);
typedef CUresult (CUDAAPI *PFN_cuMemAlloc_v2000)(CUdeviceptr_v1 *dptr, unsigned int
bytesize);
```

CUDA driver symbols have a version based naming scheme with a \_v\* extension in its name except for the first version. When the signature or the semantics of a specific CUDA driver API changes, we increment the version number of the corresponding driver symbol. In the case of the cuMemAlloc driver API, the first driver symbol name is cuMemAlloc and the next symbol name is cuMemAlloc\_v2. The typedef for the first version which was introduced in CUDA 2.0 (2000) is PFN\_cuMemAlloc\_v2000. The typedef for the next version which was introduced in CUDA 3.2 (3020) is PFN\_cuMemAlloc\_v3020.

The typedefs can be used to more easily define a function pointer of the appropriate type in code:

```c
PFN_cuMemAlloc_v3020 pfn_cuMemAlloc_v2;
PFN_cuMemAlloc_v2000 pfn_cuMemAlloc_v1;
```

## 21.5.3. Driver Function Retrieval

Using the Driver Entry Point Access APIs and the appropriate typedef, we can get the function pointer to any CUDA driver API.

## 21.5.3.1 Using the Driver API

The driver API requires CUDA version as an argument to get the ABI compatible version for the requested driver symbol. CUDA Driver APIs have a per-function ABI denoted with a \_v\* extension. For example, consider the versions of cuStreamBeginCapture and their corresponding typedefs from cudaTypedefs.h:

```c
// cuda.h
CUresult CUDAAPI cuStreamBeginCapture(CUstream hStream);
CUresult CUDAAPI cuStreamBeginCapture_v2(CUstream hStream, CUstreamCaptureMode mode);

// cudaTypedefs.h
typedef CUresult (CUDAAPI *PFN_cuStreamBeginCapture_v10000)(CUstream hStream);
typedef CUresult (CUDAAPI *PFN_cuStreamBeginCapture_v10010)(CUstream hStream,
    CUStreamCaptureMode mode);
```

From the above typedefs in the code snippet, version sufixes \_v10000 and \_v10010 indicate that the above APIs were introduced in CUDA 10.0 and CUDA 10.1 respectively.

```c
#include <cudaTypedefs.h>

// Declare the entry points for cuStreamBeginCapture
PFN_cuStreamBeginCapture_v10000 pfn_cuStreamBeginCapture_v1;
PFN_cuStreamBeginCapture_v10010 pfn_cuStreamBeginCapture_v2;

// Get the function pointer to the cuStreamBeginCapture driver symbol
cuGetProcAddress("cuStreamBeginCapture", &pfn_cuStreamBeginCapture_v1, 10000, CU_GET_
PROC_ADDRESS_DEFAULT, &driverStatus);
// Get the function pointer to the cuStreamBeginCapture_v2 driver symbol
cuGetProcAddress("cuStreamBeginCapture", &pfn_cuStreamBeginCapture_v2, 10010, CU_GET_
PROC_ADDRESS_DEFAULT, &driverStatus);
```

Referring to the code snippet above, to retrieve the address to the \_v1 version of the driver API cuStreamBeginCapture, the CUDA version argument should be exactly 10.0 (10000). Similarly, the CUDA version for retrieving the address to the \_v2 version of the API should be 10.1 (10010). Specifying a higher CUDA version for retrieving a specific version of a driver API might not always be portable. For example, using 11030 here would still return the $\_ \mathsf { v } 2$ symbol, but if a hypothetical \_v3 version is released in CUDA 11.3, the cuGetProcAddress API would start returning the newer \_v3 symbol instead when paired with a CUDA 11.3 driver. Since the ABI and function signatures of the $\_ \mathsf { v } 2$ and \_v3 symbols might difer, calling the \_v3 function using the \_v10010 typedef intended for the $\_ \mathsf { v } 2$ symbol would exhibit undefined behavior.

Note that requesting a driver API with an invalid CUDA version will return an error CUDA\_ERROR\_NOT\_FOUND. In the above code examples, passing in a version less than 10000 (CUDA 10.0) would be invalid.

## 21.5.3.2 Using the Runtime API

The runtime API cudaGetDriverEntryPointByVersion uses the provided CUDA version to get the ABI compatible version for the requested driver symbol in the same way cuGetProcAddress does. In the below code snippet, the minimum CUDA version required would be CUDA 11.2 as cuMemAllocAsync was introduced then.

```c
#include <cudaTypedefs.h>

int cudaVersion;
// Ensure a CUDA driver >= 11.2 is installed or we will get an error from
cuGetProcAddress
status = cuDriverGetVersion(&cudaVersion);
if (cudaVersion >= 11020) {

    // Declare the entry point
    PFN_cuMemAllocAsync_v11020 pfn_cuMemAllocAsync;

    // Initialize the entry point
    cudaGetDriverEntryPointByVersion("cuMemAllocAsync", &pfn_cuMemAllocAsync, 11020,
cudaEnableDefault, &driverStatus);

    // Call the entry point
    if(driverStatus == cudaDriverEntryPointSuccess && pfn_cuMemAllocAsync) {
        pfn_cuMemAllocAsync(...);
    }
}
```

## 21.5.3.3 Retrieve Per-thread Default Stream Versions

Some CUDA driver APIs can be configured to have default stream or per-thread default stream semantics. Driver APIs having per-thread default stream semantics are sufixed with \_ptsz or \_ptds in their name. For example, cuLaunchKernel has a per-thread default stream variant named cuLaunchKernel\_ptsz. With the Driver Entry Point Access APIs, users can request for the per-thread default stream version of the driver API cuLaunchKernel instead of the default stream version. Configuring the CUDA driver APIs for default stream or per-thread default stream semantics afects the synchronization behavior. More details can be found here.

The default stream or per-thread default stream versions of a driver API can be obtained by one of the following ways:

▶ Use the compilation flag --default-stream per-thread or define the macro CUDA\_API\_PER\_THREAD\_DEFAULT\_STREAM to get per-thread default stream behavior.

▶ Force default stream or per-thread default stream behavior using the flags CU\_GET\_PROC\_ADDRESS\_LEGACY\_STREAM∕cudaEnableLegacyStream or CU\_GET\_PROC\_ADDRESS\_PER\_THREAD\_DEFAULT\_STREAM∕cudaEnablePerThreadDefaultStream respectively.

## 21.5.3.4 Access New CUDA features

It is always recommended to install the latest CUDA toolkit to access new CUDA driver features, but if for some reason, a user does not want to update or does not have access to the latest toolkit, the API can be used to access new CUDA features with only an updated CUDA driver. For discussion, let us assume the user is on CUDA 12.3 and wants to use a new driver API cuFoo available in the CUDA 12.5 driver. The below code snippet illustrates this use-case:

```c
int main()
{
    // Manually define the prototype as cudaTypedefs.h in CUDA 12.3 does not have the
    cuFoo typedef
    typedef CUresult (CUDAAPI *PFN_cuFoo_v12050)(...);
    PFN_cuFoo_v12050 pfn_cuFoo = NULL;
    CUdriverProcAddressQueryResult driverStatus;
    int cudaVersion;

    // Ensure a CUDA driver >= 12.5 is installed or we will get an error from
    cuGetProcAddress
    status = cuDriverGetVersion(&cudaVersion);
    if (cudaVersion >= 12050) {
        // Get the address for cuFoo API using cuGetProcAddress. Specify CUDA version as
        // 12050 since cuFoo was introduced then
        CUresult status = cuGetProcAddress("cuFoo", &pfn_cuFoo, 12050, CU_GET_PROC_
        ADDRESS_DEFAULT, &driverStatus);

        if (status == CUDA_SUCCESS && pfn_cuFoo) {
            pfn_cuFoo(...);
        }
        else {
            printf("Cannot retrieve the address to cuFoo - driverStatus = %d\n",
        driverStatus);
            assert(0);
        }
    }

    // rest of code here
}
```

In the next example, we discuss how to get a new version of an API released in a minor version of the CUDA Toolkit. Note that in the cuda.h header the version macro that would bump cuDeviceGetUuid to \_v2 is not done until a major boundary. So during the 11.4+ releases the following example illustrates how to get the \_v2 version.

Note in this case the original (not the \_v2 version) typedef looks like:

```c
typedef CUresult (CUDAAPI *PFN_cuDeviceGetUuid_v9020)(CUuuid *uuid, CUdevice_v1 dev);
```

But the \_v2 version typedef looks like:

```txt
typedef CUresult (CUDAAPI *PFN_cuDeviceGetUuid_v11040)(CUuuid *uuid, CUdevice_v1 dev);
```

```c
#include <cudaTypedefs.h>

CUuuid uuid;
CUdevice dev;
CUresult status;
```

(continues on next page)

```txt
int cudaVersion;
CUdriverProcAddressQueryResult driverStatus;

status = cuDeviceGet(&dev, 0); // Get device 0
// handle status

status = cuDriverGetVersion(&cudaVersion);
// handle status

// Ensure a CUDA driver >= 11.4 is installed or we will get an error from
cuGetProcAddress
status = cuDriverGetVersion(&cudaVersion);
if (cudaVersion >= 11040) {
    PFN_cuDeviceGetUuid_v11040 pfn_cuDeviceGetUuid;
    status = cuGetProcAddress("cuDeviceGetUuid", &pfn_cuDeviceGetUuid, 11040, CU_GET_
PROC_ADDRESS_DEFAULT, &driverStatus);
    if(CUDA_SUCCESS == status && pfn_cuDeviceGetUuid) {
        pfn_cuDeviceGetUuid(&uuid, dev);
    }
}
```
````
