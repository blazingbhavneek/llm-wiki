# C++17 Features (constexpr host/device rules)

Details on how constexpr __host__ and __device__ functions are handled during device and host code generation, including ODR-use restrictions and unsupported patterns like exceptions and RTTI.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L19117-L19206

Citation: [CUDA_C_Programming_Guide:L19117-L19206]

````text
## 2. Otherwise:

a. During device code generation, device code is generated for the body of a \_\_host\_\_-only constexpr function H, unless H is not used or is only called in a constexpr context. Example:

```c
// NOTE: "H" is emitted in generated device code because it is
// called from device code in a non-constexpr context
constexpr __host__ int H(int x) { return x+1; }

__device__ int doit(int in) {
  in = H(in);  // OK, even though argument is not a constant expression
  return in;
}
```

b. All code restrictions applicable to a \`\`\_\_device\_\_\`\` function are also applicable to the \`\`constexpr host\`\`-only function \`\`H\`\` that is called from device code. However, compiler may not emit any build time diagnostics for \`\`H\`\` for these restrictions<sup>8</sup> .

For example, the following code patterns are unsupported in the body of H (as with any \_\_device\_\_ function), but no compiler diagnostic may be generated:

▶ ODR-use of a host variable or \_\_host\_\_-only non-constexpr function. Example:

```txt
int qqq, www;
constexpr __host__ int* H(bool b) { return b ? &qqq : &www; };
__device__ int doit(bool flag) {
```

```txt
int *ptr;
ptr = H(flag); // ERROR: H() attempts to refer to host
variables 'qqq' and 'www'.
// code will compile, but will NOT execute
correctly.
return *ptr;
}
```

▶ Use of exceptions (throw∕catch) and RTTI (typeid, dynamic\_cast). Example:

```c
struct Base { };
struct Derived : public Base { };

// NOTE: "H" is emitted in generated device code
constexpr int H(bool b, Base *ptr) {
  if (b) {
    return 1;
  } else if (typeid(ptr) == typeid(Derived)) { // ERROR: use of
typeid in code executing on the GPU
    return 2;
  } else {
    throw int{4}; // ERROR: use of throw in code executing on
the GPU
  }
}
__device__ void doit(bool flag) {
  int val;
  Derived d;
  val = H(flag, &d); //ERROR: H() attempts use typeid and
throw(), which are not allowed in code that executes on the GPU
}
```

c. During host code generation, the body of a \_\_device\_\_-only constexpr function D is preserved in the code sent to the host compiler. If the body of D attempts to ODR-use a namespace scope device variable or a \_\_device\_\_-only non-constexpr function, then the call to D from host code is not supported (code may build without compiler diagnostics, but may behave incorrectly at run time). Example:

```c
__device__ int qqq, www;
constexpr __device__ int* D(bool b) { return b ? &qqq : &www; };

int doit(bool flag) {
    int *ptr;
    ptr = D(flag); // ERROR: D() attempts to refer to device variables
    'qqq' and 'www'
        // code will compile, but will NOT execute correctly.
    return *ptr;
}
```

d. Note: Given above restrictions and lack of compiler diagnostics for incorrect usage, be careful when calling a constexpr \_\_host\_\_ function in the standard C++ headers from device code, since the implementation of the function will vary depending on the host platform, e.g., based on the libstdc++ version for gcc host compiler. Such code may break silently when being ported to a diferent platform or host compiler version (if the target C++ library implementation odr-uses a host code variable or function, as described earlier).

```cpp
__device__ int get(int in) {
    int val = std::foo(in); // "std::foo" is constexpr function defined in
    the host compiler's standard library header
        // WARNING: if std::foo implementation ODR-
    uses host variables or functions,
        // code will not work correctly
}
```
````
