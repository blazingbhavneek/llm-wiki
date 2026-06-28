
Surface functions are only supported by devices of compute capability 2.0 and higher.

Surface objects are described in described in Surface Object API.

In the sections below, boundaryMode specifies the boundary mode, that is how out-of-range surface coordinates are handled; it is equal to either cudaBoundaryModeClamp, in which case out-of-range coordinates are clamped to the valid range, or cudaBoundaryModeZero, in which case out-of-range reads return zero and out-of-range writes are ignored, or cudaBoundaryModeTrap, in which case outof-range accesses cause the kernel execution to fail.

## 10.9.1. Surface Object API

## 10.9.1.1 surf1Dread()

```txt
template<class T>
T surf1Dread(cudaSurfaceObject_t surfObj, int x,
        boundaryMode = cudaBoundaryModeTrap);
```

reads the CUDA array specified by the one-dimensional surface object surfObj using byte coordinate x.

## 10.9.1.2 surf1Dwrite

```txt
template<class T>
void surf1Dwrite(T data,
                       cudaSurfaceObject_t surfObj,
                       int x,
                       boundaryMode = cudaBoundaryModeTrap);
```

writes value data to the CUDA array specified by the one-dimensional surface object surfObj at byte coordinate x.

## 10.9.1.3 surf2Dread()

```txt
template<class T>
T surf2Dread(cudaSurfaceObject_t surfObj,
            int x, int y,
            boundaryMode = cudaBoundaryModeTrap);
template<class T>
void surf2Dread(T* data,
                cudaSurfaceObject_t surfObj,
                int x, int y,
                boundaryMode = cudaBoundaryModeTrap);
```

reads the CUDA array specified by the two-dimensional surface object surfObj using byte coordinates x and y.

## 10.9.1.4 surf2Dwrite()

```cpp
template<class T>
void surf2Dwrite(T data,
                       cudaSurfaceObject_t surfObj,
                       int x, int y,
                       boundaryMode = cudaBoundaryModeTrap);
```

writes value data to the CUDA array specified by the two-dimensional surface object surfObj at byte coordinate x and y.

## 10.9.1.5 surf3Dread()

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

reads the CUDA array specified by the three-dimensional surface object surfObj using byte coordinates x, y, and z.

## 10.9.1.6 surf3Dwrite()

```cpp
template<class T>
void surf3Dwrite(T data,
                       cudaSurfaceObject_t surfObj,
                       int x, int y, int z,
                       boundaryMode = cudaBoundaryModeTrap);
```

writes value data to the CUDA array specified by the three-dimensional object surfObj at byte coordinate x, y, and z.

## 10.9.1.7 surf1DLayeredread()

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

reads the CUDA array specified by the one-dimensional layered surface object surfObj using byte coordinate x and index layer.

## 10.9.1.8 surf1DLayeredwrite()

```cpp
template<class Type>
void surf1DLayeredwrite(T data,
                       cudaSurfaceObject_t surfObj,
                       int x, int layer,
                       boundaryMode = cudaBoundaryModeTrap);
```

writes value data to the CUDA array specified by the two-dimensional layered surface object surfObj at byte coordinate x and index layer.

## 10.9.1.9 surf2DLayeredread()

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

reads the CUDA array specified by the two-dimensional layered surface object surfObj using byte coordinate x and y, and index layer.

## 10.9.1.10 surf2DLayeredwrite()

```txt
template<class T>
void surf2DLayeredwrite(T data,
                           cudaSurfaceObject_t surfObj,
                           int x, int y, int layer,
                           boundaryMode = cudaBoundaryModeTrap);
```

writes value data to the CUDA array specified by the one-dimensional layered surface object surfObj at byte coordinate x and y, and index layer.

## 10.9.1.11 surfCubemapread()

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

reads the CUDA array specified by the cubemap surface object surfObj using byte coordinate x and y, and face index face.

## 10.9.1.12 surfCubemapwrite()

```cpp
template<class T>
void surfCubemapwrite(T data,
                       cudaSurfaceObject_t surfObj,
                       int x, int y, int face,
                       boundaryMode = cudaBoundaryModeTrap);
```

writes value data to the CUDA array specified by the cubemap object surfObj at byte coordinate x and y, and face index face.

## 10.9.1.13 surfCubemapLayeredread()

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

reads the CUDA array specified by the cubemap layered surface object surfObj using byte coordinate x and y, and index layerFace.

## 10.9.1.14 surfCubemapLayeredwrite()

```txt
template<class T>
void surfCubemapLayeredwrite(T data,
                       cudaSurfaceObject_t surfObj,
                       int x, int y, int layerFace,
                       boundaryMode = cudaBoundaryModeTrap);
```

writes value data to the CUDA array specified by the cubemap layered object surfObj at byte coordinate x and y, and index layerFace.

## 10.10. Read-Only Data Cache Load Function
