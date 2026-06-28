
1. ADL Lookup: As described earlier, the CUDA compiler will replace an extended lambda expression with an instance of a placeholder type, before invoking the host compiler. One template argument of the placeholder type uses the address of the function enclosing the original lambda expression. This may cause additional namespaces to participate in argument dependent lookup (ADL), for any host function call whose argument types involve the closure type of the extended lambda expression. This may cause an incorrect function to be selected by the host compiler.

Example:

```cpp
namespace N1 {
  struct S1_t { };
  template <typename T> void foo(T);
};

namespace N2 {
  template <typename T> int foo(T);

  template <typename T> void doit(T in) {     foo(in); }
}

void bar(N1::S1_t in) {
  /* extended __device__ lambda. In the code sent to the host compiler, this
    is replaced with the placeholder type instantiation expression
    ' __nv_dl_wrapper_t< __nv_d1_tag<void (*)(N1::S1_t in),(&bar),1> > { }'

    As a result, the namespace 'N1' participates in ADL lookup of the
    call to "foo" in the body of N2::doit, causing ambiguity.
  */
  auto lam1 = [=] __device__ { };
  N2::doit(lam1);
}
```

In the example above, the CUDA compiler replaced the extended lambda with a placeholder type that involves the N1 namespace. As a result, the namespace N1 participates in the ADL lookup for foo(in) in the body of N2::doit, and host compilation fails because multiple overload candidates N1::foo and N2::foo are found.

## 18.8. Relaxed Constexpr(-expt-relaxed-constexpr)

By default, the following cross-execution space calls are not supported:

1. Calling a \_\_device\_\_-only constexpr function from a \_\_host\_\_ function during host code generation phase (i.e, when \_\_CUDA\_ARCH\_\_ macro is undefined). Example:

```javascript
constexpr __device__ int D() { return 0; }
int main() {
    int x = D();  //ERROR: calling a __device__-only constexpr function
    from host code
}
```

2. Calling a \_\_host\_\_-only constexpr function from a \_\_device\_\_ or \_\_global\_\_ function, during device code generation phase (i.e. when \_\_CUDA\_ARCH\_\_ macro is defined). Example:

```txt
constexpr int H() { return 0; }
__device__ void dmain()
{
    int x = H();  //ERROR: calling a __host__-only constexpr function from
    device code
}
```

The experimental flag -expt-relaxed-constexpr can be used to relax this constraint. When this flag is specified, the compiler will support cross execution space calls described above, as follows:

1. A cross-execution space call to a constexpr function is supported if it occurs in a context that requires constant evaluation, e.g., in the initializer of a constexpr variable. Example:

```lisp
constexpr __host__ int H(int x) { return x+1; };
__global__ void doit() {
constexpr int val = H(1); // OK: call is in a context that
                                      // requires constant evaluation.
}

constexpr __device__ int D(int x) { return x+1; }
int main() {
constexpr int val = D(1); // OK: call is in a context that
                                      // requires constant evaluation.
}
```

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

## 18.9. Code Samples

## 18.9.1. Data Aggregation Class

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
