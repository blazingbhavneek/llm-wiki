# surf3Dread

The `surf3Dread` function reads data from a CUDA array specified by a three-dimensional surface object using byte coordinates.

## Syntax

There are two overloaded templates for `surf3Dread`:

```cpp
template<class T>
T surf3Dread(cudaSurfaceObject_t surfObj,
            int x, int y, int z,
            boundaryMode = cudaBoundaryModeTrap);

template<class T>
void surf3Dread(T* data,
                cudaSurfaceObject_t surfObj,
                int x, int y, int z,
                boundaryMode = cudaBoundaryModeTrap);
```

## Parameters

- **surfObj**: The three-dimensional surface object specifying the CUDA array to read from.
- **x, y, z**: The byte coordinates within the surface object from which to read.
- **boundaryMode**: Specifies the boundary mode to use if the coordinates are out of bounds. Defaults to `cudaBoundaryModeTrap`.

## Return Value

- In the first template, the function returns the value read from the surface object.
- In the second template, the value is written to the memory location pointed to by `data`.

## References

- CUDA C Programming Guide, Section 10.9.1.5 [CUDA_C_Programming_Guide:L7447-L7462]
