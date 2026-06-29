# CUDA Extended Lambda ADL Lookup

## Overview

When compiling CUDA code, the CUDA compiler processes extended lambda expressions before invoking the host compiler. To facilitate this, the CUDA compiler replaces an extended lambda expression with an instance of a placeholder type [CUDA_C_Programming_Guide:L19040-L19072]. This transformation can have unintended side effects on Argument Dependent Lookup (ADL) within the host compiler, specifically by introducing additional namespaces into the lookup scope [CUDA_C_Programming_Guide:L19040-L19072].

## Mechanism

The placeholder type used to represent an extended lambda includes specific template arguments that encode context about the lambda. One of these template arguments utilizes the address of the function enclosing the original lambda expression [CUDA_C_Programming_Guide:L19040-L19072].

Because the placeholder type's definition involves types or namespaces associated with the enclosing function, these namespaces become part of the type's definition. Consequently, when the placeholder type is passed as an argument to a host function, those namespaces participate in ADL for any function calls made within that host function, even if the call is unrelated to the lambda's capture or execution context [CUDA_C_Programming_Guide:L19040-L19072].

## Impact on Host Compilation

The primary risk of this behavior is that it may cause the host compiler to select an incorrect function or encounter ambiguity during overload resolution [CUDA_C_Programming_Guide:L19040-L19072]. This occurs when the additional namespaces introduced by the placeholder type contain function overloads that conflict with or shadow the intended functions in the current scope [CUDA_C_Programming_Guide:L19040-L19072].

### Example Scenario

Consider a scenario where an extended lambda is defined inside a function `bar` that takes an argument from namespace `N1`. The lambda is then passed to a function `doit` in namespace `N2`, which calls a function `foo` [CUDA_C_Programming_Guide:L19040-L19072].

```cpp
namespace N1 {
  struct S1_t { };
  template <typename T> void foo(T);
};

namespace N2 {
  template <typename T> int foo(T);

  template <typename T> void doit(T in) {
    foo(in); // ADL lookup occurs here
  }
}

void bar(N1::S1_t in) {
  // Extended __device__ lambda
  auto lam1 = [=] __device__ { };
  N2::doit(lam1);
}
```

In this example, the CUDA compiler replaces `lam1` with a placeholder type instantiation that involves the namespace `N1` due to the signature of `bar` [CUDA_C_Programming_Guide:L19040-L19072]. When `N2::doit` is called, ADL for the call to `foo(in)` considers namespaces associated with the argument type. Since the placeholder type involves `N1`, the compiler finds both `N1::foo` and `N2::foo` [CUDA_C_Programming_Guide:L19040-L19072]. This results in an ambiguous call, causing host compilation to fail [CUDA_C_Programming_Guide:L19040-L19072].

## Mitigation

Developers should be aware that extended lambdas can leak namespace context into ADL scopes. To avoid ambiguity:

1.  Avoid defining extended lambdas in functions that take arguments from namespaces containing functions with the same name as those called within the host code that receives the lambda.
2.  Use explicit qualification for function calls in host code that receives extended lambda placeholders to disambiguate overloads.
3.  Refactor code to separate the namespace contexts of the lambda's enclosing function and the host function receiving the lambda.

## References

- CUDA C Programming Guide, Section 18.7.5 Additional Notes [CUDA_C_Programming_Guide:L19040-L19072].
