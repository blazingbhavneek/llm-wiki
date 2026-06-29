# surfCubemapread

`surfCubemapread` is a CUDA runtime function used to read data from a cubemap surface object. It accesses the CUDA array specified by the surface object using byte coordinates `x` and `y`, and a face index `face`.

## Syntax

The function is available in two template forms:

```cpp
template<class T>
T surfCubemapread(
        cudaSurfaceObject_t surfObj,
        int x, int y, int face,
        boundaryMode = cudaBoundaryModeTrap);

template<class T>
void surfCubemapread(T data,
        cudaSurfaceObject_t surfObj,
        int x, int y, int face,
        boundaryMode = cudaBoundaryModeTrap);
```

## Parameters

- **surfObj**: The cubemap surface object specifying the CUDA array to read from.
- **x**: The byte coordinate in the x-dimension.
- **y**: The byte coordinate in the y-dimension.
- **face**: The face index of the cubemap.
- **boundaryMode**: (Optional) The boundary mode to use when coordinates are out of bounds. Defaults to `cudaBoundaryModeTrap`.

## Return Value

- In the first form, the function returns the read value of type `T`.
- In the second form, the read value is written to the memory location pointed to by `data`.

## References

- CUDA C Programming Guide [CUDA_C_Programming_Guide:L7533-L7549]
