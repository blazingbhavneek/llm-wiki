# Texture Memory

Texture memory is a read-only memory space optimized for spatial locality and specific access patterns in CUDA kernels. It is accessed using device functions described in the Texture Functions section, a process known as a **texture fetch** [CUDA_C_Programming_Guide:L3649-L3652].

## Texture Object API

Modern texture memory access utilizes the **Texture Object API**. A texture object is created at runtime and encapsulates the configuration of the texture memory being accessed [CUDA_C_Programming_Guide:L3652-L3655]. Each texture fetch specifies a texture object parameter [CUDA_C_Programming_Guide:L3652].

A texture object specifies the following properties:

### 1. The Texture
The texture object identifies the specific piece of texture memory to be fetched [CUDA_C_Programming_Guide:L3655-L3657].

### 2. Dimensionality
The dimensionality defines how the texture is addressed:
*   **1D**: Addressed using one texture coordinate.
*   **2D**: Addressed using two texture coordinates.
*   **3D**: Addressed using three texture coordinates [CUDA_C_Programming_Guide:L3657-L3661].

Elements of the array are called **texels** (texture elements). The width, height, and depth refer to the size of the array in each dimension. Maximum dimensions depend on the device's compute capability [CUDA_C_Programming_Guide:L3661-L3663].

### 3. Texel Type
The type of a texel is restricted to:
*   Basic integer types.
*   Single-precision floating-point types.
*   1-, 2-, and 4-component vector types derived from the above [CUDA_C_Programming_Guide:L3663-L3666].

### 4. Read Mode
The read mode determines how the value is returned by the texture fetch [CUDA_C_Programming_Guide:L3666-L3668]:
*   **`cudaReadModeNormalizedFloat`**: If the texel is an 8-bit or 16-bit integer, the value is returned as a floating-point type. The full range of the integer type is mapped to:
    *   `[0.0, 1.0]` for unsigned integers.
    *   `[-1.0, 1.0]` for signed integers.
    *   Example: An unsigned 8-bit texture element with value `0xf` reads as `1.0` [CUDA_C_Programming_Guide:L3668-L3673].
*   **`cudaReadModeElementType`**: No conversion is performed; the raw element type is returned [CUDA_C_Programming_Guide:L3673-L3674].

### 5. Coordinate Normalization
*   **Non-normalized**: Coordinates are in the range `[0, N-1]` where `N` is the size of the texture in that dimension. For example, a 64x32 texture uses x-coordinates `[0, 63]` and y-coordinates `[0, 31]` [CUDA_C_Programming_Guide:L3674-L3679].
*   **Normalized**: Coordinates are in the range `[0.0, 1.0 - 1/N]`. This makes coordinates independent of texture size, which is useful for applications requiring size-independent addressing. For a 64x32 texture, normalized coordinates would be in `[0, 1-1/64]` for both x and y [CUDA_C_Programming_Guide:L3679-L3684].

### 6. Addressing Mode
The addressing mode defines the behavior when texture coordinates are out of range. The default is **Clamp** [CUDA_C_Programming_Guide:L3684-L3686]:
*   **`cudaAddressModeClamp`**: Coordinates are clamped to the valid range (`[0, N)` for non-normalized, `[0.0, 1.0)` for normalized) [CUDA_C_Programming_Guide:L3686-L3688].
*   **`cudaAddressModeBorder`**: Out-of-range coordinates return zero [CUDA_C_Programming_Guide:L3688-L3689].
*   **`cudaAddressModeWrap`**: Available only for normalized coordinates. Each coordinate `x` is converted to `frac(x) = x - floor(x)` [CUDA_C_Programming_Guide:L3689-L3692].
*   **`cudaAddressModeMirror`**: Available only for normalized coordinates. Each coordinate `x` is converted to `frac(x)` if `floor(x)` is even, and `1 - frac(x)` if `floor(x)` is odd [CUDA_C_Programming_Guide:L3692-L3695].

The addressing mode is specified as an array of size three, corresponding to the first, second, and third texture coordinates [CUDA_C_Programming_Guide:L3695-L3697].

### 7. Filtering Mode
The filtering mode specifies how the returned value is computed based on input coordinates [CUDA_C_Programming_Guide:L3697-L3699]:
*   **`cudaFilterModePoint`**: Returns the texel whose coordinates are closest to the input coordinates [CUDA_C_Programming_Guide:L3699-L3701].
*   **`cudaFilterModeLinear`**: Performs low-precision interpolation between neighboring texels. This mode is **only valid for floating-point data** [CUDA_C_Programming_Guide:L3699-L3701].
    *   **1D**: Simple linear interpolation between two texels [CUDA_C_Programming_Guide:L3701-L3703].
    *   **2D**: Bilinear interpolation between four texels [CUDA_C_Programming_Guide:L3703-L3705].
    *   **3D**: Trilinear interpolation between eight texels [CUDA_C_Programming_Guide:L3705-L3707].

## Related Topics
*   **Texture Object API**: Detailed introduction to the API [CUDA_C_Programming_Guide:L3707-L3708].
*   **16-Bit Floating-Point Textures**: Handling 16-bit float textures [CUDA_C_Programming_Guide:L3708-L3709].
*   **Layered Textures**: Textures organized in layers [CUDA_C_Programming_Guide:L3709-L3710].
*   **Cubemap Textures**: Special cubemap and layered cubemap textures [CUDA_C_Programming_Guide:L3710-L3711].
*   **Texture Gather**: A special texture fetch operation [CUDA_C_Programming_Guide:L3711-L3712].

## References
*   [CUDA_C_Programming_Guide:L3649-L3678] CUDA C Programming Guide: Texture Memory section.
