# surf1DLayeredwrite

The `surf1DLayeredwrite` function writes value data to a CUDA array specified by a two-dimensional layered surface object.

## Signature

```cpp
template<class Type>
void surf1DLayeredwrite(T data,
                       cudaSurfaceObject_t surfObj,
                       int x, int layer,
                       boundaryMode = cudaBoundaryModeTrap);
```

## Parameters

- **data**: The value data to write.
- **surfObj**: The two-dimensional layered surface object specifying the CUDA array.
- **x**: The byte coordinate where the data is written.
- **layer**: The index of the layer within the layered surface.
- **boundaryMode**: The boundary mode, defaulting to `cudaBoundaryModeTrap`.

## Description

This function performs a write operation on a 1D layered surface. It targets a specific byte coordinate `x` and a specific layer index `layer` within the surface object `surfObj`.

## References

- [CUDA_C_Programming_Guide:L7492-L7503]
