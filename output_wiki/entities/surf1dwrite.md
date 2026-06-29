# surf1Dwrite

`surf1Dwrite` is a CUDA runtime function used to write value data to a one-dimensional surface object.

## Syntax

```cpp
template<class T>
void surf1Dwrite(T data,
                 cudaSurfaceObject_t surfObj,
                 int x,
                 boundaryMode = cudaBoundaryModeTrap);
```

## Description

The function writes the value `data` of type `T` to the CUDA array specified by the one-dimensional surface object `surfObj` at the byte coordinate `x`. The `boundaryMode` parameter specifies the behavior when the write operation accesses memory outside the bounds of the surface object, defaulting to `cudaBoundaryModeTrap`.

## References

- [CUDA_C_Programming_Guide:L7407-L7418]
