
The reference manual lists all C/C++ standard library mathematical functions that are supported in device code and all intrinsic functions that are only supported in device code.

Mathematical Functions provides accuracy information for some of these functions when relevant.

## 10.8. Texture Functions

Texture objects are described in Texture Object API.

Texture fetching is described in Texture Fetching.

## 10.8.1. Texture Object API

## 10.8.1.1 tex1Dfetch()

```txt
template<class T>
T tex1Dfetch(cudaTextureObject_t texObj, int x);
```

fetches from the region of linear memory specified by the one-dimensional texture object texObj using integer texture coordinate x. tex1Dfetch() only works with non-normalized coordinates, so only the border and clamp addressing modes are supported. It does not perform any texture filtering. For integer types, it may optionally promote the integer to single-precision floating point.

## 10.8.1.2 tex1D()

```txt
template<class T>
tex1D(cudaTextureObject_t texObj, float x);
```

fetches from the CUDA array specified by the one-dimensional texture object texObj using texture coordinate x.

## 10.8.1.3 tex1DLod()

```javascript
template<class T>
T tex1DLod(cudaTextureObject_t texObj, float x, float level);
```

fetches from the CUDA array specified by the one-dimensional texture object texObj using texture coordinate x at the level-of-detail level.

## 10.8.1.4 tex1DGrad()

```cpp
template<class T>
tex1DGrad(cudaTextureObject_t texObj, float x, float dx, float dy);
```

fetches from the CUDA array specified by the one-dimensional texture object texObj using texture coordinate x. The level-of-detail is derived from the X-gradient dx and Y-gradient dy.

## 10.8.1.5 tex2D()

```javascript
template<class T>
T tex2D(cudaTextureObject_t texObj, float x, float y);
```

fetches from the CUDA array or the region of linear memory specified by the two-dimensional texture object texObj using texture coordinate (x,y).

## 10.8.1.6 tex2D() for sparse CUDA arrays

```txt
template<class T>
T tex2D(cudaTextureObject_t texObj, float x, float y, bool* isResident);
```

fetches from the CUDA array specified by the two-dimensional texture object texObj using texture coordinate (x,y). Also returns whether the texel is resident in memory via isResident pointer. If not, the values fetched will be zeros.

## 10.8.1.7 tex2Dgather()

```txt
template<class T>
T tex2Dgather(cudaTextureObject_t texObj,
                   float x, float y, int comp = 0);
```

fetches from the CUDA array specified by the 2D texture object texObj using texture coordinates x and y and the comp parameter as described in Texture Gather.

## 10.8.1.8 tex2Dgather() for sparse CUDA arrays

```javascript
template<class T>
tex2Dgather(cudaTextureObject_t texObj,
    float x, float y, bool* isResident, int comp = 0);
```

fetches from the CUDA array specified by the 2D texture object texObj using texture coordinates x and y and the comp parameter as described in Texture Gather. Also returns whether the texel is resident in memory via isResident pointer. If not, the values fetched will be zeros.

## 10.8.1.9 tex2DGrad()

```cpp
template<class T>
T tex2DGrad(cudaTextureObject_t texObj, float x, float y,
                   float2 dx, float2 dy);
```

fetches from the CUDA array specified by the two-dimensional texture object texObj using texture coordinate (x,y). The level-of-detail is derived from the dx and dy gradients.

## 10.8.1.10 tex2DGrad() for sparse CUDA arrays

```txt
template<class T>
tex2DGrad(cudaTextureObject_t texObj, float x, float y,
    float2 dx, float2 dy, bool* isResident);
```

fetches from the CUDA array specified by the two-dimensional texture object texObj using texture coordinate (x,y). The level-of-detail is derived from the dx and dy gradients. Also returns whether the texel is resident in memory via isResident pointer. If not, the values fetched will be zeros.

## 10.8.1.11 tex2DLod()

```txt
template<class T>
tex2DLod(cudaTextureObject_t texObj, float x, float y, float level);
```

fetches from the CUDA array or the region of linear memory specified by the two-dimensional texture object texObj using texture coordinate (x,y) at level-of-detail level.

## 10.8.1.12 tex2DLod() for sparse CUDA arrays

```txt
template<class T>
tex2DLod(cudaTextureObject_t texObj, float x, float y, float level, bool* isResident);
```

fetches from the CUDA array specified by the two-dimensional texture object texObj using texture coordinate (x,y) at level-of-detail level. Also returns whether the texel is resident in memory via isResident pointer. If not, the values fetched will be zeros

## 10.8.1.13 tex3D()

```javascript
template<class T>
T tex3D(cudaTextureObject_t texObj, float x, float y, float z);
```

fetches from the CUDA array specified by the three-dimensional texture object texObj using texture coordinate (x,y,z).

## 10.8.1.14 tex3D() for sparse CUDA arrays

```txt
template<class T>
T tex3D(cudaTextureObject_t texObj, float x, float y, float z, bool* isResident);
```

fetches from the CUDA array specified by the three-dimensional texture object texObj using texture coordinate (x,y,z). Also returns whether the texel is resident in memory via isResident pointer. If not, the values fetched will be zeros.

## 10.8.1.15 tex3DLod()

```javascript
template<class T>
T tex3DLod(cudaTextureObject_t texObj, float x, float y, float z, float level);
```

fetches from the CUDA array or the region of linear memory specified by the three-dimensional texture object texObj using texture coordinate (x,y,z) at level-of-detail level.

## 10.8.1.16 tex3DLod() for sparse CUDA arrays

```cpp
template<class T>
T tex3DLod(cudaTextureObject_t texObj, float x, float y, float z, float level, bool*
→isResident);
```

fetches from the CUDA array or the region of linear memory specified by the three-dimensional texture object texObj using texture coordinate (x,y,z) at level-of-detail level. Also returns whether the texel is resident in memory via isResident pointer. If not, the values fetched will be zeros.

## 10.8.1.17 tex3DGrad()

```txt
template<class T>
T tex3DGrad(cudaTextureObject_t texObj, float x, float y, float z,
                   float4 dx, float4 dy);
```

fetches from the CUDA array specified by the three-dimensional texture object texObj using texture coordinate (x,y,z) at a level-of-detail derived from the X and Y gradients dx and dy.

## 10.8.1.18 tex3DGrad() for sparse CUDA arrays

```cpp
template<class T>
T tex3DGrad(cudaTextureObject_t texObj, float x, float y, float z,
    float4 dx, float4 dy, bool* isResident);
```

fetches from the CUDA array specified by the three-dimensional texture object texObj using texture coordinate (x,y,z) at a level-of-detail derived from the X and Y gradients dx and dy. Also returns whether the texel is resident in memory via isResident pointer. If not, the values fetched will be zeros.

## 10.8.1.19 tex1DLayered()

```txt
template<class T>
tex1DLayered(cudaTextureObject_t texObj, float x, int layer);
```

fetches from the CUDA array specified by the one-dimensional texture object texObj using texture coordinate x and index layer, as described in Layered Textures.

## 10.8.1.20 tex1DLayeredLod()

```txt
template<class T>
T tex1DLayeredLod(cudaTextureObject_t texObj, float x, int layer, float level);
```

fetches from the CUDA array specified by the one-dimensional Layered Textures at layer layer using texture coordinate x and level-of-detail level.

## 10.8.1.21 tex1DLayeredGrad()

```txt
template<class T>
T tex1DLayeredGrad(cudaTextureObject_t texObj, float x, int layer,
                   float dx, float dy);
```

fetches from the CUDA array specified by the one-dimensional layered texture at layer layer using texture coordinate x and a level-of-detail derived from the dx and dy gradients.

## 10.8.1.22 tex2DLayered()

```txt
template<class T>
T tex2DLayered(cudaTextureObject_t texObj,
                   float x, float y, int layer);
```

fetches from the CUDA array specified by the two-dimensional texture object texObj using texture coordinate (x,y) and index layer, as described in Layered Textures.

## 10.8.1.23 tex2DLayered() for Sparse CUDA Arrays

```txt
template<class T>
T tex2DLayered(cudaTextureObject_t texObj,
        float x, float y, int layer, bool* isResident);
```

fetches from the CUDA array specified by the two-dimensional texture object texObj using texture coordinate (x,y) and index layer, as described in Layered Textures. Also returns whether the texel is resident in memory via isResident pointer. If not, the values fetched will be zeros.

## 10.8.1.24 tex2DLayeredLod()

```txt
template<class T>
T tex2DLayeredLod(cudaTextureObject_t texObj, float x, float y, int layer,
                   float level);
```

fetches from the CUDA array specified by the two-dimensional layered texture at layer layer using texture coordinate (x,y).

## 10.8.1.25 tex2DLayeredLod() for sparse CUDA arrays

```cpp
template<class T>
tex2DLayeredLod(cudaTextureObject_t texObj, float x, float y, int layer,
    float level, bool* isResident);
```

fetches from the CUDA array specified by the two-dimensional layered texture at layer layer using texture coordinate (x,y). Also returns whether the texel is resident in memory via isResident pointer. If not, the values fetched will be zeros.

## 10.8.1.26 tex2DLayeredGrad()

```txt
template<class T>
T tex2DLayeredGrad(cudaTextureObject_t texObj, float x, float y, int layer,
                   float2 dx, float2 dy);
```

fetches from the CUDA array specified by the two-dimensional layered texture at layer layer using texture coordinate (x,y) and a level-of-detail derived from the dx and dy gradients.

## 10.8.1.27 tex2DLayeredGrad() for sparse CUDA arrays

```txt
template<class T>
tex2DLayeredGrad(cudaTextureObject_t texObj, float x, float y, int layer,
    float2 dx, float2 dy, bool* isResident);
```

fetches from the CUDA array specified by the two-dimensional layered texture at layer layer using texture coordinate (x,y) and a level-of-detail derived from the dx and dy gradients. Also returns whether the texel is resident in memory via isResident pointer. If not, the values fetched will be zeros.

## 10.8.1.28 texCubemap()

```cpp
template<class T>
T texCubemap(cudaTextureObject_t texObj, float x, float y, float z);
```

fetches the CUDA array specified by the cubemap texture object texObj using texture coordinate (x,y,z), as described in Cubemap Textures.

## 10.8.1.29 texCubemapGrad()

```txt
template<class T>
T texCubemapGrad(cudaTextureObject_t texObj, float x, float, y, float z,
                   float4 dx, float4 dy);
```

fetches from the CUDA array specified by the cubemap texture object texObj using texture coordinate (x,y,z) as described in Cubemap Textures. The level-of-detail used is derived from the dx and dy gradients.

## 10.8.1.30 texCubemapLod()

```txt
template<class T>
T texCubemapLod(cudaTextureObject_t texObj, float x, float, y, float z,
                   float level);
```

fetches from the CUDA array specified by the cubemap texture object texObj using texture coordinate (x,y,z) as described in Cubemap Textures. The level-of-detail used is given by level.

## 10.8.1.31 texCubemapLayered()

```txt
template<class T>
T texCubemapLayered(cudaTextureObject_t texObj,
                   float x, float y, float z, int layer);
```

fetches from the CUDA array specified by the cubemap layered texture object texObj using texture coordinates (x,y,z), and index layer, as described in Cubemap Layered Textures.

## 10.8.1.32 texCubemapLayeredGrad()

```cpp
template<class T>
T texCubemapLayeredGrad(cudaTextureObject_t texObj, float x, float y, float z,
                   int layer, float4 dx, float4 dy);
```

fetches from the CUDA array specified by the cubemap layered texture object texObj using texture coordinate (x,y,z) and index layer, as described in Cubemap Layered Textures, at level-of-detail derived from the dx and dy gradients.

## 10.8.1.33 texCubemapLayeredLod()

```txt
template<class T>
T texCubemapLayeredLod(cudaTextureObject_t texObj, float x, float y, float z,
                   int layer, float level);
```

fetches from the CUDA array specified by the cubemap layered texture object texObj using texture coordinate (x,y,z) and index layer, as described in Cubemap Layered Textures, at level-of-detail level level.

## 10.9. Surface Functions
