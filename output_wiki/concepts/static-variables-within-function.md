# Static Variables within Function

Rules for memory space specifiers of static variables in device/host functions, including initialization restrictions and __CUDA_ARCH__ conditions.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L17156-L17232

Citation: [CUDA_C_Programming_Guide:L17156-L17232]

````text

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
````
