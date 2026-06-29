# surfCubemapLayeredread

`surfCubemapLayeredread` is a CUDA surface reference function used to read data from a cubemap layered surface object.

## Syntax

There are two overloaded templates for this function:

```cpp
template<class T>
T surfCubemapLayeredread(
        cudaSurfaceObject_t surfObj,
        int x, int y, int layerFace,
        boundaryMode = cudaBoundaryModeTrap);

template<class T>
void surfCubemapLayeredread(T data,
        cudaSurfaceObject_t surfObj,
        int x, int y, int layerFace,
        boundaryMode = cudaBoundaryModeTrap);
```

## Parameters

- **surfObj**: The cubemap layered surface object specifying the CUDA array to read from.
- **x**: The byte coordinate along the x-axis.
- **y**: The byte coordinate along the y-axis.
- **layerFace**: The index of the layer face within the cubemap layered array.
- **boundaryMode**: (Optional) The boundary mode to use when accessing coordinates outside the valid range. Defaults to `cudaBoundaryModeTrap`.

## Description

The function reads the CUDA array specified by the cubemap layered surface object `surfObj` using byte coordinates `x` and `y`, and the index `layerFace`.

The first template returns the read value of type `T`. The second template writes the read value into the variable `data` provided by the caller.

## References

- CUDA C Programming Guide, Section 10.9.1.13 [CUDA_C_Programming_Guide:L7562-L7578]
