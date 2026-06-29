# Implicitly-declared and non-virtual explicitly-defaulted functions

Let F denote a function that is either implicitly-declared or is a non-virtual function that is explicitly defaulted on its first declaration [CUDA_C_Programming_Guide:L16944-L16950]. The execution space specifiers (__host__, __device__) for F are determined by the union of the execution space specifiers of all functions that invoke it [CUDA_C_Programming_Guide:L16950-L16955].

## General Rule for Non-Virtual Functions

For non-virtual functions, the execution space is the union of the execution spaces of all callers [CUDA_C_Programming_Guide:L16950-L16955]. A specific note applies to global functions: a __global__ caller is treated as a __device__ caller for this analysis [CUDA_C_Programming_Guide:L16955-L16960].

### Example: Implicit Constructors

Consider the following class hierarchy and usage:

```cpp
class Base {
  int x;
public:
  __host__ __device__ Base(void) : x(10) {}
};

class Derived : public Base {
    int y;
};

class Other: public Base {
    int z;
};

__device__ void foo(void)
{
    Derived D1;
    Other D2;
}

__host__ void bar(void)
{
    Other D3;
}
```

In this scenario:
* The implicitly-declared constructor `Derived::Derived` is invoked only from the __device__ function `foo`. Therefore, it is treated as a __device__ function [CUDA_C_Programming_Guide:L16980-L16990].
* The implicitly-declared constructor `Other::Other` is invoked from both the __device__ function `foo` and the __host__ function `bar`. Therefore, it is treated as a __host__ __device__ function [CUDA_C_Programming_Guide:L16990-L16995].

## Virtual Functions

If F is an implicitly declared virtual function (e.g., a virtual destructor), the execution spaces of each virtual function D overridden by F are added to the set of execution spaces for F, provided that D is not implicitly declared [CUDA_C_Programming_Guide:L16995-L17000].

### Example: Implicit Virtual Destructors

```cpp
struct Base1 { virtual __host__ __device__ ~Base1() { } };
struct Derived1 : Base1 { }; // implicitly-declared virtual destructor
                             // ~Derived1 has __host__ __device__
                             // execution space specifiers

struct Base2 { virtual __device__ ~Base2() = default; };
struct Derived2 : Base2 { }; // implicitly-declared virtual destructor
                             // ~Derived2 has __device__ execution
                             // space specifiers
```

In the first case, `Derived1` inherits the __host__ __device__ specifiers from `Base1`'s virtual destructor. In the second case, `Derived2` inherits the __device__ specifier from `Base2`'s explicitly defaulted virtual destructor [CUDA_C_Programming_Guide:L16995-L17000].
