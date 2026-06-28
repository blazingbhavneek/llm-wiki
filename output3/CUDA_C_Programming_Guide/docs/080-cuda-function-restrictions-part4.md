
## 18.5.10. Functions

## 18.5.10.1 External Linkage

A call within some device code of a function declared with the extern qualifier is only allowed if the function is defined within the same compilation unit as the device code, i.e., a single file or several files linked together with relocatable device code and nvlink.

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

## 18.5.10.3 Function Parameters

\_\_global\_\_ function parameters are passed to the device via constant memory and are limited to 32,764 bytes starting with Volta, and 4 KB on older architectures.

\_\_global\_\_ functions cannot have a variable number of arguments.

\_\_global\_\_ function parameters cannot be pass-by-reference.

In separate compilation mode, if a \_\_device\_\_ or \_\_global\_\_ function is ODR-used in a particular translation unit, then the parameter and return types of the function must be complete in that translation unit.

Example:

```perl
//first.cu:
struct S;
__device__ void foo(S); // error: type 'S' is incomplete
__device__ auto *ptr = foo;

int main() { }

//second.cu:
struct S { int x; };
__device__ void foo(S) { }

//compiler invocation
\$nvcc -std=c++14 -rdc=true first.cu second.cu -o first
nvlink error : Prototype doesn't match for '_Z3foo1S' in '/tmp/tmpxft_00005c8c_00000000-18_second.o', first defined in '/tmp/tmpxft_00005c8c_00000000-18_second.o'
nvlink fatal : merge_elf failed
```

## 18.5.10.3.1 \_\_global\_\_ Function Argument Processing

When a \_\_global\_\_ function is launched from device code, each argument must be trivially copyable and trivially destructible.

When a \_\_global\_\_ function is launched from host code, each argument type is allowed to be nontrivially copyable or non-trivially-destructible, but the processing for such types does not follow the standard C++ model, as described below. User code must ensure that this workflow does not afect program correctness. The workflow diverges from standard C++ in two areas:

## 1. Memcpy instead of copy constructor invocation

When lowering a \_\_global\_\_ function launch from host code, the compiler generates stub functions that copy the parameters one or more times by value, before eventually using memcpy to copy the arguments to the \_\_global\_\_ function’s parameter memory on the device. This occurs even if an argument was non-trivially-copyable, and therefore may break programs where the copy constructor has side efects.

Example:

```cpp
#include <cassert>
struct S {
  int x;
  int *ptr;
  __host__ __device__ S() { }
  __host__ __device__ S(const S &) { ptr = &x; }
};

__global__ void foo(S in) {
  // this assert may fail, because the compiler
  // generated code will memcpy the contents of "in"
  // from host to kernel parameter memory, so the
  // "in.ptr" is not initialized to "&in.x" because
  // the copy constructor is skipped.
  assert(in.ptr == &in.x);
}

int main() {
  S tmp;
```

(continues on next page)

```typescript
foo<<<1,1>>>(tmp);
    cudaDeviceSynchronize();
}
```

(continued from previous page)

Example:

```cpp
#include <cassert>

__managed__ int counter;
struct S1 {
S1() { }
S1(const S1 &) { ++counter; }
};

__global__ void foo(S1) {

/* this assertion may fail, because
    the compiler generates stub
    functions on the host for a kernel
    launch, and they may copy the
    argument by value more than once.
*/
assert(counter == 1);
}

int main() {
S1 V;
foo<<<1,1>>>(V);
cudaDeviceSynchronize();
}
```

## 2. Destructor may be invoked before the \`\`\_\_global\_\_\`\` function has finished

Kernel launches are asynchronous with host execution. As a result, if a \_\_global\_\_ function argument has a non-trivial destructor, the destructor may execute in host code even before the \_\_global\_\_ function has finished execution. This may break programs where the destructor has side efects.

Example:

```txt
struct S {
  int *ptr;
  S() : ptr(nullptr) { }
  S(const S &) { cudaMallocManaged(&ptr, sizeof(int)); }
  ~S() { cudaFree(ptr); }
};

__global__ void foo(S in) {

    //error: This store may write to memory that has already been
    //      freed (see below).
    *(in.ptr) = 4;

}

int main() {
  S V;
```

(continues on next page)

(continued from previous page)

```txt
/* The object 'V' is first copied by value to a compiler-generated
 * stub function that does the kernel launch, and the stub function
 * bitwise copies the contents of the argument to kernel parameter
 * memory.
 * However, GPU kernel execution is asynchronous with host
 * execution.
 * As a result, S::~S() will execute when the stub function  returns, releasing
 allocated memory, even though the kernel may not have finished execution.
 */
foo<<<1,1>>>(V);
cudaDeviceSynchronize();
}
```

## 18.5.10.3.2 Toolkit and Driver Compatibility

Developers must use the 12.1 Toolkit and r530 driver or higher to compile, launch, and debug kernels that accept parameters larger than 4KB. If such kernels are launched on older drivers, CUDA will issue the error CUDA\_ERROR\_NOT\_SUPPORTED.

## 18.5.10.3.3 Link Compatibility across Toolkit Revisions

When linking device objects, if at least one device object contains a kernel with a parameter larger than 4KB, the developer must recompile all objects from their respective device sources with the 12.1 toolkit or higher before linking them together. Failure to do so will result in a linker error.

## 18.5.10.4 Static Variables within Function

Variable memory space specifiers are allowed in the declaration of a static variable V within the immediate or nested block scope of a function F where:

▶ F is a \_\_global\_\_ or \_\_device\_\_-only function.

▶ F is a \_\_host\_\_ \_\_device\_\_ function and \_\_CUDA\_ARCH\_\_ is defined<sup>11</sup>.

If no explicit memory space specifier is present in the declaration of V, an implicit \_\_device\_\_ specifier is assumed during device compilation.

V has the same initialization restrictions as a variable with the same memory space specifiers declared in namespace scope for example a \_\_device\_\_ variable cannot have a ‘non-empty’ constructor (see Device Memory Space Specifiers).

Examples of legal and illegal uses of function-scope static variables are shown below.

```txt
struct S1_t {
  int x;
};

struct S2_t {
  int x;
```

(continues on next page)

<sup>11</sup> The intent is to allow variable memory space specifiers for static variables in a \_\_host\_\_ \_\_device\_\_ function during device compilation, but disallow it during host compilation

```lisp
__device__ S2_t(void) { x = 10; }
};

struct S3_t {
  int x;
  __device__ S3_t(int p) : x(p) { }
};

__device__ void f1() {
  static int i1;                 // OK, implicit __device__ memory space specifier
  static int i2 = 11;         // OK, implicit __device__ memory space specifier
  static __managed__ int m1;   // OK
  static __device__ int d1;    // OK
  static __constant__ int c1; // OK

  static S1_t i3;             // OK, implicit __device__ memory space specifier
  static S1_t i4 = {22};       // OK, implicit __device__ memory space specifier

  static __shared__ int i5;   // OK

  int x = 33;
  static int i6 = x;           // error: dynamic initialization is not allowed
  static S1_t i7 = {x};        // error: dynamic initialization is not allowed

  static S2_t i8;             // error: dynamic initialization is not allowed
  static S3_t i9(44);       // error: dynamic initialization is not allowed
}

__host__ __device__ void f2() {
  static int i1;               // OK, implicit __device__ memory space specifier
                                          // during device compilation.
#ifdef __CUDA_ARCH__
  static __device__ int d1;   // OK, declaration is only visible during device
                                          // compilation (__CUDA_ARCH__ is defined)
#else
  static int d0;                // OK, declaration is only visible during host
                                          // compilation (__CUDA_ARCH__ is not defined)
#endif

  static __device__ int d2;   // error: __device__ variable inside
                                          // a host function during host compilation
                                          // i.e. when __CUDA_ARCH__ is not defined

  static __shared__ int i2;   // error: __shared__ variable inside
                                          // a host function during host compilation
                                          // i.e. when __CUDA_ARCH__ is not defined
}
```
