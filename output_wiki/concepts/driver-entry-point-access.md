# Driver Entry Point Access

The Driver Entry Point Access APIs provide a mechanism to retrieve the address of a CUDA driver function [CUDA_C_Programming_Guide:L20353-L20555]. Starting from CUDA 11.3, users can call into available CUDA driver APIs using function pointers obtained from these APIs [CUDA_C_Programming_Guide:L20353-L20555]. These APIs provide functionality similar to their counterparts, `dlsym` on POSIX platforms and `GetProcAddress` on Windows [CUDA_C_Programming_Guide:L20353-L20555].

The provided APIs enable users to:
* Retrieve the address of a driver function using the CUDA Driver API [CUDA_C_Programming_Guide:L20353-L20555].
* Retrieve the address of a driver function using the CUDA Runtime API [CUDA_C_Programming_Guide:L20353-L20555].
* Request the per-thread default stream version of a CUDA driver function [CUDA_C_Programming_Guide:L20353-L20555].
* Access new CUDA features on older toolkits but with a newer driver [CUDA_C_Programming_Guide:L20353-L20555].

## Driver Function Typedefs

To facilitate the retrieval of CUDA Driver API entry points, the CUDA Toolkit provides headers containing function pointer definitions (typedefs) for all CUDA driver APIs [CUDA_C_Programming_Guide:L20353-L20555]. These headers are installed with the CUDA Toolkit and are available in the toolkit's `include/` directory [CUDA_C_Programming_Guide:L20353-L20555].

### Typedef Header Mapping

The following table summarizes the mapping between API header files and their corresponding typedef header files [CUDA_C_Programming_Guide:L20353-L20555]:

| API header file | API Typedef header file |
| :--- | :--- |
| `cuda.h` | `cudaTypedefs.h` |
| `cudaGL.h` | `cudaGLTypedefs.h` |
| `cudaProfiler.h` | `cudaProfilerTypedefs.h` |
| `cudaVDPAU.h` | `cudaVDPAUTypedefs.h` |
| `cudaEGL.h` | `cudaEGLTypedefs.h` |
| `cudaD3D9.h` | `cudaD3D9Typedefs.h` |
| `cudaD3D10.h` | `cudaD3D10Typedefs.h` |
| `cudaD3D11.h` | `cudaD3D11Typedefs.h` |

These headers define the typedefs for function pointers but do not define the actual function pointers themselves [CUDA_C_Programming_Guide:L20353-L20555]. For example, `cudaTypedefs.h` contains typedefs for `cuMemAlloc` with different versions [CUDA_C_Programming_Guide:L20353-L20555]:

```c
typedef CUresult (CUDAAPI *PFN_cuMemAlloc_v3020)(CUdeviceptr_v2 *dptr, size_t bytesize);
typedef CUresult (CUDAAPI *PFN_cuMemAlloc_v2000)(CUdeviceptr_v1 *dptr, unsigned int bytesize);
```

### Version Naming Scheme

CUDA driver symbols use a version-based naming scheme with a `_v*` extension, except for the first version [CUDA_C_Programming_Guide:L20353-L20555]. When the signature or semantics of a specific CUDA driver API change, the version number of the corresponding driver symbol is incremented [CUDA_C_Programming_Guide:L20353-L20555].

For `cuMemAlloc`:
* The first symbol name is `cuMemAlloc` [CUDA_C_Programming_Guide:L20353-L20555].
* The next symbol name is `cuMemAlloc_v2` [CUDA_C_Programming_Guide:L20353-L20555].
* The typedef for the first version, introduced in CUDA 2.0, is `PFN_cuMemAlloc_v2000` [CUDA_C_Programming_Guide:L20353-L20555].
* The typedef for the next version, introduced in CUDA 3.2, is `PFN_cuMemAlloc_v3020` [CUDA_C_Programming_Guide:L20353-L20555].

These typedefs allow developers to easily define function pointers of the appropriate type in code [CUDA_C_Programming_Guide:L20353-L20555]:

```c
PFN_cuMemAlloc_v3020 pfn_cuMemAlloc_v2;
PFN_cuMemAlloc_v2000 pfn_cuMemAlloc_v1;
```

## Driver Function Retrieval

Using the Driver Entry Point Access APIs and the appropriate typedef, developers can obtain the function pointer to any CUDA driver API [CUDA_C_Programming_Guide:L20353-L20555].

### Using the Driver API

The driver API requires the CUDA version as an argument to retrieve the ABI-compatible version for the requested driver symbol [CUDA_C_Programming_Guide:L20353-L20555]. CUDA Driver APIs have a per-function ABI denoted with a `_v*` extension [CUDA_C_Programming_Guide:L20353-L20555].

For example, consider the versions of `cuStreamBeginCapture` and their corresponding typedefs from `cudaTypedefs.h` [CUDA_C_Programming_Guide:L20353-L20555]:

```c
// cuda.h
CUresult CUDAAPI cuStreamBeginCapture(CUstream hStream);
CUresult CUDAAPI cuStreamBeginCapture_v2(CUstream hStream, CUstreamCaptureMode mode);

// cudaTypedefs.h
typedef CUresult (CUDAAPI *PFN_cuStreamBeginCapture_v10000)(CUstream hStream);
typedef CUresult (CUDAAPI *PFN_cuStreamBeginCapture_v10010)(CUstream hStream,
    CUStreamCaptureMode mode);
```

The version suffixes `_v10000` and `_v10010` indicate that the APIs were introduced in CUDA 10.0 and CUDA 10.1, respectively [CUDA_C_Programming_Guide:L20353-L20555].

To retrieve the address of these functions, `cuGetProcAddress` is used [CUDA_C_Programming_Guide:L20353-L20555]:

```c
#include <cudaTypedefs.h>

// Declare the entry points for cuStreamBeginCapture
PFN_cuStreamBeginCapture_v10000 pfn_cuStreamBeginCapture_v1;
PFN_cuStreamBeginCapture_v10010 pfn_cuStreamBeginCapture_v2;

// Get the function pointer to the cuStreamBeginCapture driver symbol
cuGetProcAddress("cuStreamBeginCapture", &pfn_cuStreamBeginCapture_v1, 10000, CU_GET_PROC_ADDRESS_DEFAULT, &driverStatus);
// Get the function pointer to the cuStreamBeginCapture_v2 driver symbol
cuGetProcAddress("cuStreamBeginCapture", &pfn_cuStreamBeginCapture_v2, 10010, CU_GET_PROC_ADDRESS_DEFAULT, &driverStatus);
```

When retrieving the address of the `_v1` version, the CUDA version argument must be exactly 10.0 (10000) [CUDA_C_Programming_Guide:L20353-L20555]. Similarly, the CUDA version for retrieving the `_v2` version should be 10.1 (10010) [CUDA_C_Programming_Guide:L20353-L20555].

**Portability Warning:** Specifying a higher CUDA version for retrieving a specific version of a driver API might not always be portable [CUDA_C_Programming_Guide:L20353-L20555]. For example, using 11030 in the above example would still return the `_v2` symbol, but if a hypothetical `_v3` version is released in CUDA 11.3, `cuGetProcAddress` would start returning the newer `_v3` symbol when paired with a CUDA 11.3 driver [CUDA_C_Programming_Guide:L20353-L20555]. Since the ABI and function signatures of `_v2` and `_v3` might differ, calling the `_v3` function using the `_v10010` typedef intended for the `_v2` symbol would exhibit undefined behavior [CUDA_C_Programming_Guide:L20353-L20555].

Requesting a driver API with an invalid CUDA version will return an error `CUDA_ERROR_NOT_FOUND` [CUDA_C_Programming_Guide:L20353-L20555]. For instance, passing in a version less than 10000 (CUDA 10.0) for `cuStreamBeginCapture` would be invalid [CUDA_C_Programming_Guide:L20353-L20555].

### Using the Runtime API

The runtime API `cudaGetDriverEntryPointByVersion` uses the provided CUDA version to get the ABI-compatible version for the requested driver symbol, functioning similarly to `cuGetProcAddress` [CUDA_C_Programming_Guide:L20353-L20555].

For example, to use `cuMemAllocAsync`, which was introduced in CUDA 11.2, the minimum CUDA version required is 11.2 [CUDA_C_Programming_Guide:L20353-L20555]:

```c
#include <cudaTypedefs.h>

int cudaVersion;
// Ensure a CUDA driver >= 11.2 is installed or we will get an error from
// cuGetProcAddress
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

### Retrieve Per-thread Default Stream Versions

Some CUDA driver APIs can be configured to have default stream or per-thread default stream semantics [CUDA_C_Programming_Guide:L20353-L20555]. Driver APIs having per-thread default stream semantics are suffixed with `_ptsz` or `_ptds` in their name [CUDA_C_Programming_Guide:L20353-L20555]. For example, `cuLaunchKernel` has a per-thread default stream variant named `cuLaunchKernel_ptsz` [CUDA_C_Programming_Guide:L20353-L20555].

With the Driver Entry Point Access APIs, users can request the per-thread default stream version of a driver API instead of the default stream version [CUDA_C_Programming_Guide:L20353-L20555]. Configuring the CUDA driver APIs for default stream or per-thread default stream semantics affects synchronization behavior [CUDA_C_Programming_Guide:L20353-L20555].

The default stream or per-thread default stream versions of a driver API can be obtained by one of the following methods [CUDA_C_Programming_Guide:L20353-L20555]:
* Use the compilation flag `--default-stream per-thread` or define the macro `CUDA_API_PER_THREAD_DEFAULT_STREAM` to get per-thread default stream behavior [CUDA_C_Programming_Guide:L20353-L20555].
* Force default stream or per-thread default stream behavior using the flags `CU_GET_PROC_ADDRESS_LEGACY_STREAM`/`cudaEnableLegacyStream` or `CU_GET_PROC_ADDRESS_PER_THREAD_DEFAULT_STREAM`/`cudaEnablePerThreadDefaultStream`, respectively [CUDA_C_Programming_Guide:L20353-L20555].

### Access New CUDA Features

It is recommended to install the latest CUDA toolkit to access new CUDA driver features [CUDA_C_Programming_Guide:L20353-L20555]. However, if a user does not want to update or does not have access to the latest toolkit, the API can be used to access new CUDA features with only an updated CUDA driver [CUDA_C_Programming_Guide:L20353-L20555].

For example, assume a user is on CUDA 12.3 and wants to use a new driver API `cuFoo` available in the CUDA 12.5 driver [CUDA_C_Programming_Guide:L20353-L20555]. Since `cudaTypedefs.h` in CUDA 12.3 does not have the `cuFoo` typedef, the prototype must be manually defined [CUDA_C_Programming_Guide:L20353-L20555]:

```c
int main()
{
    // Manually define the prototype as cudaTypedefs.h in CUDA 12.3 does not have the
    // cuFoo typedef
    typedef CUresult (CUDAAPI *PFN_cuFoo_v12050)(...);
    PFN_cuFoo_v12050 pfn_cuFoo = NULL;
    CUdriverProcAddressQueryResult driverStatus;
    int cudaVersion;

    // Ensure a CUDA driver >= 12.5 is installed or we will get an error from
    // cuGetProcAddress
    status = cuDriverGetVersion(&cudaVersion);
    if (cudaVersion >= 12050) {
        // Get the address for cuFoo API using cuGetProcAddress. Specify CUDA version as
        // 12050 since cuFoo was introduced then
        CUresult status = cuGetProcAddress("cuFoo", &pfn_cuFoo, 12050, CU_GET_PROC_ADDRESS_DEFAULT, &driverStatus);

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

In cases where a new version of an API is released in a minor version of the CUDA Toolkit, note that the version macro in `cuda.h` that bumps an API to `_v2` is not done until a major boundary [CUDA_C_Programming_Guide:L20353-L20555]. For example, during CUDA 11.4+ releases, the `_v2` version of `cuDeviceGetUuid` can be retrieved as follows [CUDA_C_Programming_Guide:L20353-L20555]:

The original (not the `_v2` version) typedef looks like [CUDA_C_Programming_Guide:L20353-L20555]:

```c
typedef CUresult (CUDAAPI *PFN_cuDeviceGetUuid_v9020)(CUuuid *uuid, CUdevice_v1 dev);
```

But the `_v2` version typedef looks like [CUDA_C_Programming_Guide:L20353-L20555]:

```c
typedef CUresult (CUDAAPI *PFN_cuDeviceGetUuid_v11040)(CUuuid *uuid, CUdevice_v1 dev);
```

The code to retrieve and use this version is [CUDA_C_Programming_Guide:L20353-L20555]:

```c
#include <cudaTypedefs.h>

CUuuid uuid;
CUdevice dev;
CUresult status;
int cudaVersion;
CUdriverProcAddressQueryResult driverStatus;

status = cuDeviceGet(&dev, 0); // Get device 0
// handle status

status = cuDriverGetVersion(&cudaVersion);
// handle status

// Ensure a CUDA driver >= 11.4 is installed or we will get an error from
// cuGetProcAddress
status = cuDriverGetVersion(&cudaVersion);
if (cudaVersion >= 11040) {
    PFN_cuDeviceGetUuid_v11040 pfn_cuDeviceGetUuid;
    status = cuGetProcAddress("cuDeviceGetUuid", &pfn_cuDeviceGetUuid, 11040, CU_GET_PROC_ADDRESS_DEFAULT, &driverStatus);
    if(CUDA_SUCCESS == status && pfn_cuDeviceGetUuid) {
        pfn_cuDeviceGetUuid(&uuid, dev);
    }
}
```
