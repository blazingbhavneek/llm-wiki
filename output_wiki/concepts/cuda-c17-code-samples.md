# CUDA C++17 Code Samples: Classes, Templates, and Functors

This page provides code samples illustrating the use of C++17 features within CUDA device code, specifically focusing on data aggregation, inheritance, templates, and functors.

## Data Aggregation Class

The `PixelRGBA` class demonstrates how to define a simple data aggregation class with device-accessible members and operators.

```cpp
class PixelRGBA {
public:
    __device__ PixelRGBA(): r_(0), g_(0), b_(0), a_(0) { }

    __device__ PixelRGBA(unsigned char r, unsigned char g,
                    unsigned char b, unsigned char a = 255):
                    r_(r), g_(g), b_(b), a_(a) { }

private:
    unsigned char r_, g_, b_, a_;

    friend PixelRGBA operator+(const PixelRGBA&, const PixelRGBA&);
};

__device__
PixelRGBA operator+(const PixelRGBA& p1, const PixelRGBA& p2)
{
    return PixelRGBA(p1.r_ + p2.r_, p1.g_ + p2.g_,
                   p1.b_ + p2.b_, p1.a_ + p2.a_);
}

__device__ void func(void)
{
    PixelRGBA p1, p2;
    // ...      // Initialization of p1 and p2 here
    PixelRGBA p3 = p1 + p2;
}
```

The class uses `__device__` constructors and a friend operator function to allow addition of two `PixelRGBA` instances within device code [CUDA_C_Programming_Guide:L19207-L19363].

## Derived Class

This example shows inheritance in CUDA, including custom memory management and virtual functions.

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

The `Shape` base class defines a virtual `Draw` method and destructor. The `Point` class inherits from `Shape` and overrides `Draw`. Custom placement new and delete operators are declared for `MemoryPool` integration [CUDA_C_Programming_Guide:L19207-L19363].

## Class Template

This sample demonstrates a class template used within a CUDA kernel.

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

The `myValues` template class is instantiated inside the `useValues` global kernel. The example shows explicit instantiation with `int` in the host code [CUDA_C_Programming_Guide:L19207-L19363].

## Function Template

This example illustrates function templates, explicit specialization, and argument deduction.

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

The code shows a generic `func` template, an explicit specialization for `int`, and usage examples for both explicit and implicit type deduction [CUDA_C_Programming_Guide:L19207-L19363].

## Functor Class

Functors are used to pass operations as arguments to CUDA kernels.

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
    VectorOperation<<<blocks, threads>>>(v1, v2, v3, N, Add());
}
```

The `Add` and `Sub` classes define `operator()` to perform arithmetic. The `VectorOperation` kernel takes a functor `op` and applies it to vector elements `A` and `B`, storing the result in `C`. The host code invokes the kernel with an instance of `Add` [CUDA_C_Programming_Guide:L19207-L19363].

## See Also

- Chapter 19. Texture Fetching [CUDA_C_Programming_Guide:L19207-L19363]
