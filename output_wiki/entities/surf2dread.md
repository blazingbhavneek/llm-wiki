# surf2Dread

The `surf2Dread` function reads from a two-dimensional surface object specified by a `cudaSurfaceObject_t`. It retrieves data from the underlying CUDA array using byte coordinates `x` and `y` [[CUDA_C_Programming_Guide:L7419-L7433]].

## Function Signatures

There are two template overloads for `surf2Dread`:

1.  **Return value overload:**
    ```cpp
    template<class T>
    T surf2Dread(cudaSurfaceObject_t surfObj,
                 int x, int y,
                 boundaryMode = cudaBoundaryModeTrap);
    ```
    This version returns the read value directly as type `T` [[CUDA_C_Programming_Guide:L7419-L7433]].

2.  **Pointer output overload:**
    ```cpp
    template<class T>
    void surf2Dread(T* data,
                    cudaSurfaceObject_t surfObj,
                    int x, int y,
                    boundaryMode = cudaBoundaryModeTrap);
    ```
    This version writes the read value to the memory location pointed to by `data` [[CUDA_C_Programming_Guide:L7419-L7433]].

## Parameters

*   **surfObj**: The two-dimensional surface object specifying the CUDA array to read from [[CUDA_C_Programming_Guide:L7419-L7433]].
*   **x**: The byte coordinate along the x-axis [[CUDA_C_Programming_Guide:L7419-L7433]].
*   **y**: The byte coordinate along the y-axis [[CUDA_C_Programming_Guide:L7419-L7433]].
*   **boundaryMode**: Optional boundary mode, defaulting to `cudaBoundaryModeTrap` [[CUDA_C_Programming_Guide:L7419-L7433]].

## Notes

*   The coordinates `x` and `y` are specified in bytes [[CUDA_C_Programming_Guide:L7419-L7433]].
*   The research report for this entity encountered a context length error during automated generation; this content is derived directly from the source documentation [[CUDA_C_Programming_Guide:L7419-L7433]].
