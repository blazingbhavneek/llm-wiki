# surf2Dwrite

The `surf2Dwrite` function writes value data to a CUDA array specified by a two-dimensional surface object at byte coordinates x and y.

## Syntax

```cpp
template<class T>
void surf2Dwrite(T data,
                 cudaSurfaceObject_t surfObj,
                 int x, int y,
                 boundaryMode = cudaBoundaryModeTrap);
```

## Parameters

- **data**: The value data to write.
- **surfObj**: The two-dimensional surface object specifying the target CUDA array.
- **x**: The x-coordinate in bytes.
- **y**: The y-coordinate in bytes.
- **boundaryMode**: The boundary mode, defaulting to `cudaBoundaryModeTrap`.

## Description

This function is part of the CUDA Surface Object API, specifically under section 10.9.1.4. It allows kernel code to write data directly to a surface object, which is bound to a CUDA array. The coordinates `x` and `y` are specified in bytes.

[CUDA_C_Programming_Guide:L7434-L7446]
