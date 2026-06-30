# Guidelines for cuGetProcAddress

Provides guidelines for using cuGetProcAddress, including version matching and driver version checks, and explains how to determine failure reasons using CUdriverProcAddressQueryResult.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L20556-L20604

Citation: [CUDA_C_Programming_Guide:L20556-L20604]

````text
## 21.5.4. Guidelines for cuGetProcAddress

Below are guidelines to keep in mind when using cuGetProcAddress.

▶ Code the CUDA version passed to cuGetProcAddress to match the typedef version (do not use a compile time constant such as CUDA\_VERSION or a dynamic version such as returned from cuDriverGetVersion)

Check the current driver version (such as from cuDriverGetVersion) is suficient before calling cuGetProcAddress or an error is expected or an unexpected symbol may be returned

## 21.5.4.1 Guidelines for Runtime API Usage

Unless specified otherwise, the CUDA runtime API cudaGetDriverEntryPointByVersion will have similar guidelines as the driver entry point cuGetProcAddress since it allows for the user to request a specific CUDA driver version

## 21.5.5. Determining cuGetProcAddress Failure Reasons

There are two types of errors with cuGetProcAddress. Those are (1) API/usage errors and (2) inability to find the driver API requested. The first error type will return error codes from the API via the CUresult return value. Things like passing NULL as the pfn variable or passing invalid flags.

The second error type encodes in the CUdriverProcAddressQueryResult \*symbolStatus and can be used to help distinguish potential issues with the driver not being able to find the symbol requested. Take the following example:

```txt
// cuDeviceGetExecAffinitySupport was introduced in release CUDA 11.4
#include <cuda.h>
CUdriverProcAddressQueryResult driverStatus;
cudaVersion = ...;
status = cuGetProcAddress("cuDeviceGetExecAffinitySupport", &pfn, cudaVersion, 0, &
driverStatus);
if (CUDA_SUCCESS == status) {
    if (CU_GET_PROC_ADDRESS_VERSION_NOT_SUFFICIENT == driverStatus) {
        printf("We can use the new feature when you upgrade cudaVersion to 11.4, but
CUDA driver is good to go!\n");
        // Indicating cudaVersion was < 11.4 but run against a CUDA driver >= 11.4
    }
    else if (CU_GET_PROC_ADDRESS_SYMBOL_NOT_FOUND == driverStatus) {
        printf("Please update both CUDA driver and cudaVersion to at least 11.4 to
use the new feature!\n");
        // Indicating driver is < 11.4 since string not found, doesn't matter what
cudaVersion was
    }
    else if (CU_GET_PROC_ADDRESS_SUCCESS == driverStatus && pfn) {
        printf("You're using cudaVersion and CUDA driver >= 11.4, using new feature!\n
");
        pfn();
    }
}
```

The first case with the return code CU\_GET\_PROC\_ADDRESS\_VERSION\_NOT\_SUFFICIENT indicates that the symbol was found when searching in the CUDA driver but it was added later than the cudaVersion supplied. In the example, specifying cudaVersion as anything 11030 or less and when running against a CUDA driver >= CUDA 11.4 would give this result of CU\_GET\_PROC\_ADDRESS\_VERSION\_NOT\_SUFFICIENT. This is because cuDeviceGetExecAffinitySupport was added in CUDA 11.4 (11040).

The second case with the return code CU\_GET\_PROC\_ADDRESS\_SYMBOL\_NOT\_FOUND indicates that the symbol was not found when searching in the CUDA driver. This can be due to a few reasons such as unsupported CUDA function due to older driver as well as just having a typo. In the latter, similar to the last example if the user had put symbol as CUDeviceGetExecAfinitySupport - notice the capital CU to start the string - cuGetProcAddress would not be able to find the API because the string doesn’t match. In the former case an example might be the user developing an application against a CUDA driver supporting the new API, and deploying the application against an older CUDA driver. Using the last example, if the developer developed against CUDA 11.4 or later but was deployed against a CUDA 11.3 driver, during their development they may have had a succesful cuGetProcAddress, but when deploying an application running against a CUDA 11.3 driver the call would no longer work with the CU\_GET\_PROC\_ADDRESS\_SYMBOL\_NOT\_FOUND returned in driverStatus.
````
