# surfCubemapLayeredwrite

The `surfCubemapLayeredwrite` function writes value data to a CUDA array specified by a cubemap layered surface object at byte coordinates `x` and `y`, and index `layerFace`.

## Syntax

```cpp
template<class T>
void surfCubemapLayeredwrite(T data,
                       cudaSurfaceObject_t surfObj,
                       int x, int y, int layerFace,
                       boundaryMode = cudaBoundaryModeTrap);
```

## Parameters

- **data**: The value data to write.
- **surfObj**: The cubemap layered surface object specifying the target CUDA array.
- **x**: The byte coordinate for the x-axis.
- **y**: The byte coordinate for the y-axis.
- **layerFace**: The index of the layer face within the cubemap layered array.
- **boundaryMode**: Optional boundary mode, defaulting to `cudaBoundaryModeTrap`.

## Description

This function performs a write operation to a layered cubemap surface. It targets a specific face (`layerFace`) of the cubemap array and writes the provided `data` at the specified byte coordinates (`x`, `y`). The function is templated on the type `T` of the data being written.

## References

- [CUDA_C_Programming_Guide:L7579-L7590]
