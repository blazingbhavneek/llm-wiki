
## 18.7. Extended Lambdas

The nvcc flag '--extended-lambda' allows explicit execution space annotations in a lambda expression<sup>23</sup>. The execution space annotations should be present after the ‘lambda-introducer’ and before the optional ‘lambda-declarator’. nvcc will define the macro \_\_CUDACC\_EXTENDED\_LAMBDA\_\_ when the '--extended-lambda' flag has been specified.

An ‘extended \_\_device\_\_ lambda’ is a lambda expression that is annotated explicitly with ‘\_\_device\_\_’, and is defined within the immediate or nested block scope of a \_\_host\_\_ or \_\_host\_\_ \_\_device\_\_ function.

An ‘extended \_\_host\_\_ \_\_device\_\_ lambda’ is a lambda expression that is annotated explicitly with both ‘\_\_host\_\_’ and ‘\_\_device\_\_’, and is defined within the immediate or nested block scope of a \_\_host\_\_ or \_\_host\_\_ \_\_device\_\_ function.

An ‘extended lambda’ denotes either an extended \_\_device\_\_ lambda or an extended \_\_host\_\_ \_\_device\_\_ lambda. Extended lambdas can be used in the type arguments of \_\_global\_\_ function template instantiation.

If the execution space annotations are not explicitly specified, they are computed based on the scopes enclosing the closure class associated with the lambda, as described in the section on C++11 support. The execution space annotations are applied to all methods of the closure class associated with the lambda.

Example:

```txt
void foo_host(void) {
  // not an extended lambda: no explicit execution space annotations
  auto lam1 = [] { };

  // extended __device__ lambda
  auto lam2 = [] __device__ { };

  // extended __host__ __device__ lambda
  auto lam3 = [] __host__ __device__ { };

  // not an extended lambda: explicitly annotated with only '__host__':
  auto lam4 = [] __host__ { };
```

(continues on next page)

(continued from previous page)

```txt
}

__host__ __device__ void foo_host_device(void) {
  // not an extended lambda: no explicit execution space annotations
  auto lam1 = [] { };

  // extended __device__ lambda
  auto lam2 = [] __device__ { };

  // extended __host__ __device__ lambda
  auto lam3 = [] __host__ __device__ { };

  // not an extended lambda: explicitly annotated with only '__host__':
  auto lam4 = [] __host__ { };
}

__device__ void foo_device(void) {
  // none of the lambdas within this function are extended lambdas,
  // because the enclosing function is not a __host__ or __host__ __device__
  // function.
  auto lam1 = [] { };
  auto lam2 = [] __device__ { };
  auto lam3 = [] __host__ __device__ { };
  auto lam4 = [] __host__ { };
}

// lam1 and lam2 are not extended lambdas because they are not defined
// within a __host__ or __host__ __device__ function.
auto lam1 = [] { };
auto lam2 = [] __host__ __device__ { };
```

## 18.7.1. Extended Lambda Type Traits

The compiler provides type traits to detect closure types for extended lambdas at compile time:

\_\_nv\_is\_extended\_device\_lambda\_closure\_type(type): If ‘type’ is the closure class created for an extended \_\_device\_\_ lambda, then the trait is true, otherwise it is false.

\_\_nv\_is\_extended\_device\_lambda\_with\_preserved\_return\_type(type): If ‘type’ is the closure class created for an extended \_\_device\_\_ lambda and the lambda is defined with trailing return type (with restriction), then the trait is true, otherwise it is false. If the trailing return type definition refers to any lambda parameter name, the return type is not preserved.

\_\_nv\_is\_extended\_host\_device\_lambda\_closure\_type(type): If ‘type’ is the closure class created for an extended \_\_host\_\_ \_\_device\_\_ lambda, then the trait is true, otherwise it is false.

These traits can be used in all compilation modes, irrespective of whether lambdas or extended lambdas are enabled<sup>24</sup>.

Example:

```c
#define IS_D_LAMBDA(X) __nv_is_extended_device_lambda_closure_type(X)
#define IS_DPRT_LAMBDA(X) __nv_is_extended_device_lambda_with_preserved_return_type(X)
```

```c
#define IS_HD_LAMBDA(X) __nv_is_extended_host_device_lambda_closure_type(X)

auto lam0 = [] __host__ __device__ { };

void foo(void) {
    auto lam1 = [] { };
    auto lam2 = [] __device__ { };
    auto lam3 = [] __host__ __device__ { };
    auto lam4 = [] __device__ () --> double { return 3.14; }
    auto lam5 = [] __device__ (int x) --> decltype(&x) { return 0; }

    // lam0 is not an extended lambda (since defined outside function scope)
    static_assert(!IS_D_LAMBDA(decltype(lam0)), "");
    static_assert(!IS_DPRT_LAMBDA(decltype(lam0)), "");
    static_assert(!IS_HD_LAMBDA(decltype(lam0)),;

    // lam1 is not an extended lambda (since no execution space annotations)
    static_assert(!IS_D_LAMBDA(decltype(lam1)), "");
    static_assert(!IS_DPRT_LAMBDA(decltype(lam1)), "");
    static_assert(!IS_HD_LAMBDA(decltype(lam1)),;

    // lam2 is an extended __device__ lambda
    static_assert(IS_D_LAMBDA(decltype(lam2)), "");
    static_assert(!IS_DPRT_LAMBDA(decltype(lam2)), "");
    static_assert(!IS_HD_LAMBDA(decltype(lam2)),;

    // lam3 is an extended __host__ __device__ lambda
    static_assert(!IS_D_LAMBDA(decltype(lam3)), "");
    static_assert(!IS_DPRT_LAMBDA(decltype(lam3)), "");
    static_assert(IS_HD_LAMBDA(decltype(lam3)),;

    // lam4 is an extended __device__ lambda with preserved return type
    static_assert(IS_D_LAMBDA(decltype(lam4)), "");
    static_assert(IS_DPRT_LAMBDA(decltype(lam4)), "");
    static_assert(!IS_HD_LAMBDA(decltype(lam4)),;

    // lam5 is not an extended __device__ lambda with preserved return type
    // because it references the operator()'s parameter types in the trailing return type.
    static_assert(IS_D_LAMBDA(decltype(lam5)), "");
    static_assert(!IS_DPRT_LAMBDA(decltype(lam5)), "");
    static_assert(!IS_HD_LAMBDA(decltype(lam5)),;d);
}
```

## 18.7.2. Extended Lambda Restrictions

The CUDA compiler will replace an extended lambda expression with an instance of a placeholder type defined in namespace scope, before invoking the host compiler. The template argument of the placeholder type requires taking the address of a function enclosing the original extended lambda expression. This is required for the correct execution of any \_\_global\_\_ function template whose template argument involves the closure type of an extended lambda. The enclosing function is computed as follows.

By definition, the extended lambda is present within the immediate or nested block scope of a \_\_host\_\_ or \_\_host\_\_ \_\_device\_\_ function. If this function is not the operator() of a lambda expression, then it is considered the enclosing function for the extended lambda. Otherwise, the extended lambda is defined within the immediate or nested block scope of the operator() of one or more enclosing lambda expressions. If the outermost such lambda expression is defined in the immediate or nested block scope of a function F, then F is the computed enclosing function, else the enclosing function does not exist.

Example:

```javascript
void foo(void) {
    // enclosing function for lam1 is "foo"
    auto lam1 = [] __device__ { };

    auto lam2 = [] {
        auto lam3 = [] {
            // enclosing function for lam4 is "foo"
            auto lam4 = [] __host__ __device__ { };
        };
    };
}

auto lam6 = [] {
    // enclosing function for lam7 does not exist
    auto lam7 = [] __host__ __device__ { };
};
```

Here are the restrictions on extended lambdas:

1. An extended lambda cannot be defined inside another extended lambda expression.

Example:

```txt
void foo(void) {
    auto lam1 = [] __host__ __device__  {
        // error: extended lambda defined within another extended lambda
        auto lam2 = [] __host__ __device__ { };
    };
}
```

2. An extended lambda cannot be defined inside a generic lambda expression.

Example:

```txt
void foo(void) {
    auto lam1 = [] (auto) {
        // error: extended lambda defined within a generic lambda
        auto lam2 = [] __host__ __device__ { };
    };
}
```

3. If an extended lambda is defined within the immediate or nested block scope of one or more nested lambda expression, the outermost such lambda expression must be defined inside the immediate or nested block scope of a function.

Example:

```javascript
auto lam1 = [] {
  // error: outer enclosing lambda is not defined within a
  // non-lambda-operator() function.
  auto lam2 = [] __host__ __device__ { };
};
```

4. The enclosing function for the extended lambda must be named and its address can be taken. If the enclosing function is a class member, then the following conditions must be satisfied:

▶ All classes enclosing the member function must have a name.

▶ The member function must not have private or protected access within its parent class.

▶ All enclosing classes must not have private or protected access within their respective parent classes.

## Example:

```txt
void foo(void) {
    // OK
    auto lam1 = [] __device__ { return 0; };
    {
        // OK
        auto lam2 = [] __device__ { return 0; };
        // OK
        auto lam3 = [] __device__ __host__ { return 0; };
    }
}

struct S1_t {
    S1_t(void) {
        // Error: cannot take address of enclosing function
        auto lam4 = [] __device__ { return 0; };
    }
};

class C0_t {
    void foo(void) {
        // Error: enclosing function has private access in parent class
        auto temp1 = [] __device__ { return 10; };
    }
    struct S2_t {
        void foo(void) {
            // Error: enclosing class S2_t has private access in its
            // parent class
            auto temp1 = [] __device__ { return 10; };
        }
    };
};
```

5. It must be possible to take the address of the enclosing routine unambiguously, at the point where the extended lambda has been defined. This may not be feasible in some cases e.g. when a class typedef shadows a template type argument of the same name.

Example:

```cpp
template <typename> struct A {
    typedef void Bar;
    void test();
};

template<> struct A<void> { };

template <typename Bar>
void A<Bar>::test() {
```

(continues on next page)

(continued from previous page)

```cpp
/* In code sent to host compiler, nvcc will inject an
    address expression here, of the form:
    (void (A< Bar> ::*)(void))(&A::test))

    However, the class typedef 'Bar' (to void) shadows the
    template argument 'Bar', causing the address
    expression in A<int>::test to actually refer to:
    (void (A< void> ::*)(void))(&A::test))

    ..which doesn't take the address of the enclosing
    routine 'A<int>::test' correctly.
*/
auto lam1 = [] __host__ __device__ { return 4; };
}

int main() {
    A<int> xxx;
    xxx.test();
}
```

6. An extended lambda cannot be defined in a class that is local to a function.

Example:

```txt
void foo(void) {
    struct S1_t {
        void bar(void) {
            // Error: bar is member of a class that is local to a function.
            auto lam4 = [] __host__ __device__ { return 0; };
        }
    };
}
```

7. The enclosing function for an extended lambda cannot have deduced return type.

Example:

```txt
auto foo(void) {
  // Error: the return type of foo is deduced.
  auto lam1 = [] __host__ __device__ { return 0; };
}
```

8. \_\_host\_\_ \_\_device\_\_ extended lambdas cannot be generic lambdas.

Example:

```txt
void foo(void) {
    // Error: __host__ __device__ extended lambdas cannot be
    // generic lambdas.
    auto lam1 = [] __host__ __device__ (auto i) { return i; };

    // Error: __host__ __device__ extended lambdas cannot be
    // generic lambdas.
    auto lam2 = [] __host__ __device__ (auto ...i) {
        return sizeof...(i);
        };
}
```

9. If the enclosing function is an instantiation of a function template or a member function template, and/or the function is a member of a class template, the template(s) must satisfy the following constraints:

The template must have at most one variadic parameter, and it must be listed last in the template parameter list.

▶ The template parameters must be named.

▶ The template instantiation argument types cannot involve types that are either local to a function (except for closure types for extended lambdas), or are private or protected class members.

Example:

```cpp
template <typename T>
__global__ void kern(T in) { in(); }

template <typename... T>
struct foo {}

template < template <typename...> class T, typename... P1,
        typename... P2>
void bar1(const T<P1...>, const T<P2...>) {
    // Error: enclosing function has multiple parameter packs
    auto lam1 = [] __device__ { return 10; };
}

template < template <typename...> class T, typename... P1,
        typename T2>
void bar2(const T<P1...>, T2) {
    // Error: for enclosing function, the
    // parameter pack is not last in the template parameter list.
    auto lam1 = [] __device__ { return 10; };
}

template <typename T, T>
void bar3(void) {
    // Error: for enclosing function, the second template
    // parameter is not named.
    auto lam1 = [] __device__ { return 10; };
}

int main() {
    foo<char, int, float> f1;
    foo<char, int> f2;
    bar1(f1, f2);
    bar2(f1, 10);
    bar3<int, 10>();
}
```

Example:

```c
template <typename T>
__global__ void kern(T in) { in(); }

template <typename T>
void bar4(void) {
    auto lam1 = [] __device__ { return 10; };
```

(continued from previous page)

```cpp
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

10. With Visual Studio host compilers, the enclosing function must have external linkage. The restriction is present because this host compiler does not support using the address of non-extern linkage functions as template arguments, which is needed by the CUDA compiler transformations to support extended lambdas.

11. With Visual Studio host compilers, an extended lambda shall not be defined within the body of an ‘if-constexpr’ block.

12. An extended lambda has the following restrictions on captured variables:

▶ In the code sent to the host compiler, the variable may be passed by value to a sequence of helper functions before being used to direct-initialize the field of the class type used to represent the closure type for the extended lambda<sup>25</sup>.

1 A variable can only be captured by value.

▶ A variable of array type cannot be captured if the number of array dimensions is greater than 7.

▶ For a variable of array type, in the code sent to the host compiler, the closure type’s array field is first default-initialized, and then each element of the array field is copy-assigned from the corresponding element of the captured array variable. Therefore, the array element type must be default-constructible and copy-assignable in host code.

▶ A function parameter that is an element of a variadic argument pack cannot be captured.

The type of the captured variable cannot involve types that are either local to a function (except for closure types of extended lambdas), or are private or protected class members.

For a \_\_host\_\_ \_\_device\_\_ extended lambda, the types used in the return or parameter types of the lambda expression’s operator() cannot involve types that are either local to a function (except for closure types of extended lambdas), or are private or protected class members.

▶ Init-capture is not supported for \_\_host\_\_ \_\_device\_\_ extended lambdas. Init-capture is supported for \_\_device\_\_ extended lambdas, except when the init-capture is of array type or of type std::initializer\_list.

▶ The function call operator for an extended lambda is not constexpr. The closure type for an extended lambda is not a literal type. The constexpr and consteval specifier cannot be used in the declaration of an extended lambda.

<sup>25</sup> In contrast, the C++ standard specifies that the captured variable is used to direct-initialize the field of the closure type.

▶ A variable cannot be implicitly captured inside an if-constexpr block lexically nested inside an extended lambda, unless it has already been implicitly captured earlier outside the ifconstexpr block or appears in the explicit capture list for the extended lambda (see example below).

## Example

```txt
void foo(void) {
  // OK: an init-capture is allowed for an
  // extended __device__ lambda.
  auto lam1 = [x = 1] __device__ () { return x; };

  // Error: an init-capture is not allowed for
  // an extended __host__ __device__ lambda.
  auto lam2 = [x = 1] __host__ __device__ () { return x; };

  int a = 1;
  // Error: an extended __device__ lambda cannot capture
  // variables by reference.
  auto lam3 = [&a] __device__ () { return a; };

  // Error: by-reference capture is not allowed
  // for an extended __device__ lambda.
  auto lam4 = [&x = a] __device__ () { return x; };

  struct S1_t { };
  S1_t s1;
  // Error: a type local to a function cannot be used in the type
  // of a captured variable.
  auto lam6 = [s1] __device__ () { };

  // Error: an init-capture cannot be of type std::initializer_list.
  auto lam7 = [x = {11}] __device__ () { };

  std::initializer_list<int> b = {11,22,33};
  // Error: an init-capture cannot be of type std::initializer_list.
  auto lam8 = [x = b] __device__ () { };

  // Error scenario (lam9) and supported scenarios (lam10, lam11)
  // for capture within 'if-constexpr' block
  int yyy = 4;
  auto lam9 = [=] __device__ {
    int result = 0;
    if constexpr(false) {
      //Error: An extended __device__ lambda cannot first-capture
      //     'yyy' in constexpr-if context
      result += yyy;
    }
    return result;
  };

  auto lam10 = [yyy] __device__ {
    int result = 0;
    if constexpr(false) {
      //OK: 'yyy' already listed in explicit capture list for the extended lambda
      result += yyy;
    }
    return result;
```

(continued from previous page)

```txt
};
auto lam11 = [=] __device__ {
    int result = yyy;
    if constexpr(false) {
        //OK: 'yyy' already implicit captured outside the 'if-constexpr' block
        result += yyy;
    }
    return result;
};
}
```

13. When parsing a function, the CUDA compiler assigns a counter value to each extended lambda within that function. This counter value is used in the substituted named type passed to the host compiler. Hence, whether or not an extended lambda is defined within a function should not depend on a particular value of \_\_CUDA\_ARCH\_\_, or on \_\_CUDA\_ARCH\_\_ being undefined.
