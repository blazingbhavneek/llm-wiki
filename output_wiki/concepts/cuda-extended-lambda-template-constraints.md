# CUDA Extended Lambda Template Constraints

When an extended lambda is defined within a function that is an instantiation of a function template or a member function template, and/or the function is a member of a class template, specific constraints apply to the template parameters. These rules ensure that the lambda's context is well-defined and accessible during compilation and execution [CUDA_C_Programming_Guide:L18559-L18637].

## Template Parameter Constraints

The enclosing template must satisfy the following conditions:

1. **Variadic Parameters**: The template must have at most one variadic parameter (parameter pack). If present, this variadic parameter must be listed last in the template parameter list [CUDA_C_Programming_Guide:L18559-L18637].
2. **Named Parameters**: All template parameters must be explicitly named [CUDA_C_Programming_Guide:L18559-L18637].
3. **Type Accessibility**: The template instantiation argument types cannot involve types that are:
   - Local to a function (with the exception of closure types for extended lambdas)
   - Private or protected members of a class [CUDA_C_Programming_Guide:L18559-L18637]

## Examples of Invalid Configurations

The following examples illustrate violations of these constraints:

### Multiple Parameter Packs
Defining an extended lambda inside a function with multiple parameter packs results in an error [CUDA_C_Programming_Guide:L18559-L18637]:

```cpp
template < template <typename...> class T, typename... P1,
        typename... P2>
void bar1(const T<P1...>, const T<P2...>) {
    // Error: enclosing function has multiple parameter packs
    auto lam1 = [] __device__ { return 10; };
}
```

### Variadic Parameter Not Last
If the variadic parameter is not the last in the template parameter list, an error occurs [CUDA_C_Programming_Guide:L18559-L18637]:

```cpp
template < template <typename...> class T, typename... P1,
        typename T2>
void bar2(const T<P1...>, T2) {
    // Error: for enclosing function, the
    // parameter pack is not last in the template parameter list.
    auto lam1 = [] __device__ { return 10; };
}
```

### Unnamed Template Parameters
Template parameters must be named. Using an unnamed parameter (e.g., a non-type template parameter without a name) causes an error [CUDA_C_Programming_Guide:L18559-L18637]:

```cpp
template <typename T, T>
void bar3(void) {
    // Error: for enclosing function, the second template
    // parameter is not named.
    auto lam1 = [] __device__ { return 10; };
}
```

## Type Accessibility Constraints

Extended lambdas cannot be instantiated with types that are local to a function or private/protected class members [CUDA_C_Programming_Guide:L18559-L18637].

### Local Types
Using a type local to a function (other than the lambda's own closure type) results in an error [CUDA_C_Programming_Guide:L18559-L18637]:

```cpp
template <typename T>
void bar4(void) {
    auto lam1 = [] __device__ { return 10; };
    kern<<<1,1>>>(lam1);
}

struct C1_t { struct S1_t { }; friend int main(void); };
int main() {
    struct S1_t { };
    // Error: enclosing function for device lambda in bar4
    // is instantiated with a type local to main.
    bar4<S1_t>();

    // Error: enclosing function for device lambda in bar4
    // is instantiated with a type that is a private member
    // of a class.
    bar4<C1_t::S1_t>();
}
```

### Private/Protected Members
Instantiating a template with a private or protected class member also results in an error [CUDA_C_Programming_Guide:L18559-L18637].

## Valid Configuration

A valid configuration involves a template with a single named variadic parameter at the end, and instantiation with accessible types [CUDA_C_Programming_Guide:L18559-L18637]:

```cpp
template <typename T>
__global__ void kern(T in) { in(); }

template <typename T>
void bar4(void) {
    auto lam1 = [] __device__ { return 10; };
    kern<<<1,1>>>(lam1);
}
```
