
## 18.9.2. Derived Class

```cpp
__device__ void* operator new(size_t bytes, MemoryPool& p);
__device__ void operator delete(void*, MemoryPool& p);
class Shape {
public:
    __device__ Shape(void) { }
    __device__ void putThis(PrintBuffer *p) const;
    __device__ virtual void Draw(PrintBuffer *p) const {
        p->put("Shapeless");
    }
    __device__ virtual ~Shape() {}
};
class Point : public Shape {
public:
    __device__ Point() : x(0), y(0) {}
    __device__ Point(int ix, int iy) : x(ix), y(iy) { }
    __device__ void PutCoord(PrintBuffer *p) const;
    __device__ void Draw(PrintBuffer *p) const;
    __device__ ~Point() {}
private:
    int x, y;
};
__device__ Shape* GetPointObj(MemoryPool& pool)
{
    Shape* shape = new(pool) Point(rand(-20,10), rand(-100,-20));
    return shape;
}
```

## 18.9.3. Class Template

```cpp
template <class T>
class myValues {
    T values[MAX_VALUES];
public:
    __device__ myValues(T clear) { ... }
    __device__ void setValue(int Idx, T value) { ... }
    __device__ void putToMemory(T* valueLocation) { ... }
};

template <class T>
void __global__ useValues(T* memoryBuffer) {
    myValues<T> myLocation(0);
    ...
}

__device__ void* buffer;

int main()
{
    ...
    useValues<int><<<blocks, threads>>>(buffer);
    ...
}
```

## 18.9.4. Function Template

```c
template <typename T>
__device__ bool func(T x)
{
    ...
    return (...);
}

template <>
__device__ bool func<int>(T x) // Specialization
{
    return true;
}

// Explicit argument specification
bool result = func<double>(0.5);

// Implicit argument deduction
int x = 1;
bool result = func(x);
```

## 18.9.5. Functor Class

```cpp
class Add {
public:
    __device__ float operator() (float a, float b) const
    {
        return a + b;
    }
};

class Sub {
public:
    __device__ float operator() (float a, float b) const
    {
        return a - b;
    }
};

// Device code
template<class 0> __global__
void VectorOperation(const float * A, const float * B, float * C,
                                unsigned int N, O op)
{
    unsigned int iElement = blockDim.x * blockIdx.x + threadIdx.x;
    if (iElement < N)
        C[iElement] = op(A[iElement], B[iElement]);
}

// Host code
int main()
{
    ...
```

(continued from previous page)

VectorOperation<<<blocks, threads>>>(v1, v2, v3, N, Add());

## Chapter 19. Texture Fetching

Warning: This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA.

This section gives the formula used to compute the value returned by the texture functions of Texture Functions depending on the various attributes of the texture object (see Texture and Surface Memory).

The texture bound to the texture object is represented as an array T of

▶ N texels for a one-dimensional texture,

N x M texels for a two-dimensional texture,

▶ N x M x L texels for a three-dimensional texture.

It is fetched using non-normalized texture coordinates x, y, and z, or the normalized texture coordinates x/N, y/M, and z/L as described in Texture Memory. In this section, the coordinates are assumed to be in the valid range. Texture Memory explained how out-of-range coordinates are remapped to the valid range based on the addressing mode.

## 19.1. Nearest-Point Sampling

In this filtering mode, the value returned by the texture fetch is

▶ tex(x)=T[i] for a one-dimensional texture,

▶ tex(x,y)=T[i,j] for a two-dimensional texture,

▶ tex(x,y,z)=T[i,j,k] for a three-dimensional texture,

where i=floor(x), j=floor(y), and k=floor(z).

Figure 36 illustrates nearest-point sampling for a one-dimensional texture with N=4.

For integer textures, the value returned by the texture fetch can be optionally remapped to [0.0, 1.0] (see Texture Memory).

![](images/ad3287b3c5908ab2171c292f030ef07b01561b84fe6190e0b4bcf05ca38fff94.jpg)  
Figure 36: Nearest-Point Sampling Filtering Mode

## 19.2. Linear Filtering

In this filtering mode, which is only available for floating-point textures, the value returned by the texture fetch is

▶ $t e x ( x ) = ( 1 - \alpha ) T [ i ] + \alpha T [ i + 1 ]$ for a one-dimensional texture,

▶ $t e x ( x ) = ( 1 - \alpha ) T [ i ] + \alpha T [ i + 1 ]$ for a one-dimensional texture,

▶ $\begin{array} { r } { \varepsilon x ( x , y ) = ( 1 - \alpha ) ( 1 - \beta ) T [ i , j ] + \alpha ( 1 - \beta ) T [ i + 1 , j ] + ( 1 - \alpha ) \beta T [ i , j + 1 ] + \alpha \beta T [ i + 1 , j + 1 ] } \end{array}$ for a two-dimensional texture,

▶ tex(x, y, z) =

$$
\begin{array}{l} (1 - \alpha) (1 - \beta) (1 - \gamma) T [ i, j, k ] + \alpha (1 - \beta) (1 - \gamma) T [ i + 1, j, k ] + \\ (1 - \alpha) \beta (1 - \gamma) T [ i, j + 1, k ] + \alpha \beta (1 - \gamma) T [ i + 1, j + 1, k ] + \\ (1 - \alpha) (1 - \beta) \gamma T [ i, j, k + 1 ] + \alpha (1 - \beta) \gamma T [ i + 1, j, k + 1 ] + \\ (1 - \alpha) \beta \gamma T [ i, j + 1, k + 1 ] + \alpha \beta \gamma T [ i + 1, j + 1, k + 1 ] \end{array}
$$

for a three-dimensional texture,

where:

$$
\begin{array}{l} \blacktriangleright i = f l o o r (x B) *, \alpha = f r a c (x B) *, * x B = x - 0. 5, \\ \blacktriangleright j = f l o o r (y B) *, \beta = f r a c (y B) *, * y B = y - 0. 5, \\ \blacktriangleright k = f l o o r (z B) *, \gamma = f r a c (z B) *, * z B = z - 0. 5, \end{array}
$$

$\alpha , \beta ,$ and γ are stored in 9-bit fixed point format with 8 bits of fractional value (so 1.0 is exactly represented).

Figure 37 illustrates linear filtering of a one-dimensional texture with $N { = } 4 .$

![](images/1e8abd5f7d3dd35ce4932a9ca9bfe7b911ae56cd533b031aa567099c245b397f.jpg)  
Figure 37: Linear Filtering Mode

## 19.3. Table Lookup

A table lookup TL(x) where x spans the interval [0,R] can be implemented as $T L ( x ) { = } t e x ( ( N - l ) / R ) x { + } 0 . 5 )$ in order to ensure that $T L ( O ) = T [ O ]$ and $T L ( R ) { = } T [ N { - } l ]$

Figure 38 illustrates the use of texture filtering to implement a table lookup with R=4 or R=1 from a one-dimensional texture with N=4.

![](images/89e823f2e9056596055c9a6244f7035950127ee991ea576680a185263ab93230.jpg)  
Figure 38: One-Dimensional Table Lookup Using Linear Filtering
