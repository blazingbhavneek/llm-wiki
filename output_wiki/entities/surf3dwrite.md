# surf3Dwrite

`surf3Dwrite` is a CUDA runtime function used to write value data to a CUDA array specified by a three-dimensional surface object.

## Syntax

```cpp
template<class T>
void surf3Dwrite(T data,
                 cudaSurfaceObject_t surfObj,
                 int x, int y, int z,
                 boundaryMode = cudaBoundaryModeTrap);
```

## Parameters

- **data**: The value data to be written.
- **surfObj**: The three-dimensional surface object specifying the target CUDA array.
- **x, y, z**: The byte coordinates within the surface object where the data is written.
- **boundaryMode**: An optional parameter specifying the boundary mode, defaulting to `cudaBoundaryModeTrap`.

## Description

The function writes the provided `data` to the CUDA array associated with `surfObj` at the specified byte coordinates `x`, `y`, and `z` [CUDA_C_Programming_Guide:L7463-L7474].

## See Also

- `surf3Dread`
- `cudaSurfaceObject_t`
