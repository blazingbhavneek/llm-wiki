# surfCubemapwrite

The `surfCubemapwrite` function writes value data to a CUDA array specified by a cubemap surface object at specific byte coordinates and face index.

## Syntax

```cpp
template<class T>
void surfCubemapwrite(T data,
                      cudaSurfaceObject_t surfObj,
                      int x, int y, int face,
                      boundaryMode = cudaBoundaryModeTrap);
```

## Parameters

- **data**: The value data to write.
- **surfObj**: The cubemap surface object specifying the target CUDA array.
- **x**: The byte coordinate along the x-axis.
- **y**: The byte coordinate along the y-axis.
- **face**: The face index of the cubemap.
- **boundaryMode**: Optional boundary mode, defaulting to `cudaBoundaryModeTrap`.

## Description

This function performs a write operation to a cubemap surface. It takes the input data and writes it to the location defined by the byte coordinates `x` and `y` on the specified `face` of the cubemap surface object `surfObj`.

## References

- [CUDA_C_Programming_Guide:L7550-L7561]
