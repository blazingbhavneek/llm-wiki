# Implicitly-declared and non-virtual explicitly-defaulted functions

Rules for determining execution space specifiers (__host__, __device__) for implicitly-declared or defaulted functions based on callers.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L16944-L17000

Citation: [CUDA_C_Programming_Guide:L16944-L17000]

````text

## 18.5.10.2 Implicitly-declared and non-virtual explicitly-defaulted functions

Let F denote a function that is either implicitly-declared or is a non-virtual function that is explicitlydefaulted on its first declaration. The execution space specifiers (\_\_host\_\_, \_\_device\_\_) for F are the union of the execution space specifiers of all the functions that invoke it (note that a \_\_global\_\_ caller will be treated as a \_\_device\_\_ caller for this analysis). For example:

```txt
class Base {
  int x;
public:
  __host__ __device__ Base(void) : x(10) {}
```

(continues on next page)

```lisp
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

(continued from previous page)

Here, the implicitly-declared constructor function “Derived::Derived” will be treated as a \_\_device\_\_ function, since it is invoked only from the \_\_device\_\_ function “foo”. The implicitly-declared constructor function “Other::Other” will be treated as a \_\_host\_\_ \_\_device\_\_ function, since it is invoked both from a \_\_device\_\_ function “foo” and a \_\_host\_\_ function “bar”.

In addition, if F is an implicitly declared virtual function (e.g.,a virtual destructor), then the execution spaces of each virtual function D overridden by F are added to the set of execution spaces for F, if D is not implicitly declared.

For example:

```txt
struct Base1 { virtual __host__ __device__ ~Base1() { } };
struct Derived1 : Base1 { }; // implicitly-declared virtual destructor
                             // ~Derived1 has __host__ __device__
                             // execution space specifiers

struct Base2 { virtual __device__ ~Base2() = default; };
struct Derived2 : Base2 { }; // implicitly-declared virtual destructor
                             // ~Derived2 has __device__ execution
                             // space specifiers
```
````
