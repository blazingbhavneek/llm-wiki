# surf1DLayeredread

`surf1DLayeredread` is a CUDA runtime function used to read data from a one-dimensional layered surface object.

## Syntax

The function is available in two template forms:

```cpp
template<class T>
T surf1DLayeredread(
        cudaSurfaceObject_t surfObj,
        int x, int layer,
        boundaryMode = cudaBoundaryModeTrap);

template<class T>
void surf1DLayeredread(T data,
        cudaSurfaceObject_t surfObj,
        int x, int layer,
        boundaryMode = cudaBoundaryModeTrap);
```

## Description

The function reads the CUDA array specified by the one-dimensional layered surface object `surfObj` using byte coordinate `x` and index `layer` [CUDA_C_Programming_Guide:L7475-L7491].

## Parameters

- **surfObj**: The one-dimensional layered surface object from which to read.
- **x**: The byte coordinate within the layer.
- **layer**: The index of the layer within the layered surface.
- **boundaryMode**: (Optional) Specifies the boundary mode behavior. Defaults to `cudaBoundaryModeTrap`.

## Return Value

- In the first form, the function returns the read value of type `T`.
- In the second form, the read value is stored in the `data` parameter.
