# tex1Dfetch

The `tex1Dfetch` function fetches data from the region of linear memory specified by a one-dimensional texture object using integer texture coordinates. It is designed for non-normalized coordinates, which restricts supported addressing modes to border and clamp. Unlike standard texture fetches, `tex1Dfetch` does not perform any texture filtering.

## Syntax

```cpp
template<class T>
T tex1Dfetch(cudaTextureObject_t texObj, int x);
```

## Parameters

- **texObj**: The one-dimensional texture object specifying the region of linear memory to fetch from.
- **x**: The integer texture coordinate.

## Behavior

- **Addressing Modes**: Because `tex1Dfetch` operates on non-normalized coordinates, it only supports the `cudaAddressModeBorder` and `cudaAddressModeClamp` addressing modes [CUDA_C_Programming_Guide:L7072-L7079].
- **Filtering**: No texture filtering is performed [CUDA_C_Programming_Guide:L7072-L7079].
- **Type Promotion**: For integer types, the function may optionally promote the integer to single-precision floating point [CUDA_C_Programming_Guide:L7072-L7079].

## See Also

- `tex1D`
- `cudaTextureObject_t`
