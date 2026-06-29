# surf1Dread

`surf1Dread` is a CUDA runtime function used to read data from a one-dimensional surface object.

## Signature

```cpp
template<class T>
T surf1Dread(cudaSurfaceObject_t surfObj, int x,
        boundaryMode = cudaBoundaryModeTrap);
```

## Description

The function reads the CUDA array specified by the one-dimensional surface object `surfObj` using the byte coordinate `x` [CUDA_C_Programming_Guide:L7398-L7406].

## Parameters

*   **surfObj**: The one-dimensional surface object from which to read.
*   **x**: The byte coordinate at which to read.
*   **boundaryMode**: Optional boundary mode, defaulting to `cudaBoundaryModeTrap`.

## Return Value

The function returns the value of type `T` read from the specified location in the surface object.

## See Also

*   `surf1Dwrite`
*   `surf2Dread`
*   `surf3Dread`
