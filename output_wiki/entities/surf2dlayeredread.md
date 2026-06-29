# surf2DLayeredread

The `surf2DLayeredread` function is used to read data from a CUDA array specified by a two-dimensional layered surface object.

## Syntax

There are two overloads for this function:

```cpp
template<class T>
T surf2DLayeredread(
        cudaSurfaceObject_t surfObj,
        int x, int y, int layer,
        boundaryMode = cudaBoundaryModeTrap);

template<class T>
void surf2DLayeredread(T data,
                       cudaSurfaceObject_t surfObj,
                       int x, int y, int layer,
                       boundaryMode = cudaBoundaryModeTrap);
```

## Parameters

- **surfObj**: The two-dimensional layered surface object specifying the CUDA array to read from.
- **x**: The x-coordinate in bytes.
- **y**: The y-coordinate in bytes.
- **layer**: The index of the layer within the layered surface.
- **boundaryMode**: (Optional) The boundary mode to use, defaulting to `cudaBoundaryModeTrap`.
- **data**: (Second overload only) A reference to the variable where the read data will be stored.

## Description

The function reads the CUDA array specified by the two-dimensional layered surface object `surfObj` using byte coordinates `x` and `y`, and the index `layer` [CUDA_C_Programming_Guide:L7504-L7520].

## Return Value

- In the first overload, the function returns the read value of type `T`.
- In the second overload, the function returns `void` and stores the result in the `data` parameter.
