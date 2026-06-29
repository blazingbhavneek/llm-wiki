# surf2DLayeredwrite

The `surf2DLayeredwrite` function writes value data to a CUDA array specified by a one-dimensional layered surface object at specific byte coordinates and layer index.

## Syntax

```cpp
template<class T>
void surf2DLayeredwrite(T data,
                        cudaSurfaceObject_t surfObj,
                        int x, int y, int layer,
                        boundaryMode = cudaBoundaryModeTrap);
```

## Parameters

- **data**: The value data to write.
- **surfObj**: The one-dimensional layered surface object specifying the CUDA array.
- **x**: The x-coordinate (byte) where the data is written.
- **y**: The y-coordinate (byte) where the data is written.
- **layer**: The index of the layer in the layered surface.
- **boundaryMode**: The boundary mode to use, defaulting to `cudaBoundaryModeTrap`.

## Description

This function performs a write operation to a 2D layered surface. It targets the CUDA array identified by `surfObj`, placing the provided `data` at the specified byte coordinates `x` and `y` within the layer indicated by `layer`.

## References

- [CUDA_C_Programming_Guide:L7521-L7532]
