# cuGetProcAddress Error Handling

The `cuGetProcAddress` function can fail for two distinct reasons: API/usage errors and the inability to find the requested driver API symbol [CUDA_C_Programming_Guide:L20567-L20575].

## API/Usage Errors

The first type of error involves invalid usage of the API itself. These errors are returned directly via the `CUresult` return value of the function [CUDA_C_Programming_Guide:L20575-L20577]. Common examples include:

*   Passing `NULL` as the `pfn` variable.
*   Passing invalid flags [CUDA_C_Programming_Guide:L20577-L20578].

## Symbol Lookup Errors

The second type of error occurs when the driver cannot find the requested symbol. This status is encoded in the `CUdriverProcAddressQueryResult` pointed to by the `symbolStatus` argument [CUDA_C_Programming_Guide:L20578-L20580]. This allows developers to distinguish between different failure modes, such as version mismatches or missing symbols [CUDA_C_Programming_Guide:L20580-L20581].

### CU_GET_PROC_ADDRESS_SUCCESS

If the function returns `CUDA_SUCCESS` and `pfn` is non-NULL, the symbol was found and the function pointer is valid for use [CUDA_C_Programming_Guide:L20593-L20596].

### CU_GET_PROC_ADDRESS_VERSION_NOT_SUFFICIENT

This status indicates that the symbol was found in the CUDA driver, but it was introduced in a version later than the `cudaVersion` supplied to `cuGetProcAddress` [CUDA_C_Programming_Guide:L20587-L20590].

For example, `cuDeviceGetExecAffinitySupport` was introduced in CUDA 11.4 (version 11040) [CUDA_C_Programming_Guide:L20590-L20592]. If an application specifies a `cudaVersion` of 11.3 (11030) or lower but runs against a driver version 11.4 or higher, `cuGetProcAddress` will return `CU_GET_PROC_ADDRESS_VERSION_NOT_SUFFICIENT` [CUDA_C_Programming_Guide:L20592-L20596]. This allows the application to determine that the driver supports the feature, but the application's declared version is too old to claim it [CUDA_C_Programming_Guide:L20587-L20590].

### CU_GET_PROC_ADDRESS_SYMBOL_NOT_FOUND

This status indicates that the symbol was not found in the CUDA driver [CUDA_C_Programming_Guide:L20597-L20599]. This can occur for several reasons:

1.  **Older Driver:** The application is deployed against a CUDA driver that does not support the requested API (e.g., developing against CUDA 11.4+ but deploying to a CUDA 11.3 driver) [CUDA_C_Programming_Guide:L20599-L20603].
2.  **Typo:** The symbol string provided does not match the actual API name exactly (e.g., case sensitivity or misspelling) [CUDA_C_Programming_Guide:L20599-L20603].

## Example Usage

The following example demonstrates how to handle these different outcomes when attempting to load `cuDeviceGetExecAffinitySupport` [CUDA_C_Programming_Guide:L20581-L20596]:

```c
// cuDeviceGetExecAffinitySupport was introduced in release CUDA 11.4
#include <cuda.h>

CUdriverProcAddressQueryResult driverStatus;
cudaVersion = ...;
status = cuGetProcAddress("cuDeviceGetExecAffinitySupport", &pfn, cudaVersion, 0, &driverStatus);

if (CUDA_SUCCESS == status) {
    if (CU_GET_PROC_ADDRESS_VERSION_NOT_SUFFICIENT == driverStatus) {
        printf("We can use the new feature when you upgrade cudaVersion to 11.4, but CUDA driver is good to go!\n");
        // Indicating cudaVersion was < 11.4 but run against a CUDA driver >= 11.4
    }
    else if (CU_GET_PROC_ADDRESS_SYMBOL_NOT_FOUND == driverStatus) {
        printf("Please update both CUDA driver and cudaVersion to at least 11.4 to use the new feature!\n");
        // Indicating driver is < 11.4 since string not found, doesn't matter what cudaVersion was
    }
    else if (CU_GET_PROC_ADDRESS_SUCCESS == driverStatus && pfn) {
        printf("You're using cudaVersion and CUDA driver >= 11.4, using new feature!\n");
        pfn();
    }
}
```
