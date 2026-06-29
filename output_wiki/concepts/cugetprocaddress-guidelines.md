# Guidelines for cuGetProcAddress

The `cuGetProcAddress` API provides a mechanism for loading CUDA runtime symbols dynamically. To ensure correct behavior and avoid errors or unexpected results, developers should adhere to the following guidelines when using this API.

## Version Handling

When calling `cuGetProcAddress`, the CUDA version passed to the function must match the typedef version defined in the CUDA headers. Developers should avoid using:

*   Compile-time constants such as `CUDA_VERSION`.
*   Dynamic version information returned by functions like `cuDriverGetVersion`.

Instead, use the specific version typedef associated with the symbols being loaded to ensure compatibility between the API call and the symbol definitions [CUDA_C_Programming_Guide:L20556-L20563].

## Driver Version Verification

Before invoking `cuGetProcAddress`, it is essential to verify that the current NVIDIA driver version is sufficient to support the requested CUDA version. Failing to check the driver version can result in:

*   API errors.
*   Return of unexpected or incorrect symbols.

Use `cuDriverGetVersion` to retrieve the current driver version and ensure it meets the requirements for the CUDA version being targeted [CUDA_C_Programming_Guide:L20556-L20563].
