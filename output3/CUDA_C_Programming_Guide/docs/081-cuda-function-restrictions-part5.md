
## 18.5.10.5 Function Pointers

The address of a \_\_global\_\_ function taken in host code cannot be used in device code (e.g. to launch the kernel). Similarly, the address of a \_\_global\_\_ function taken in device code cannot be used in host code.

It is not allowed to take the address of a \_\_device\_\_ function in host code.

## 18.5.10.6 Function Recursion

\_\_global\_\_ functions do not support recursion.

## 18.5.10.7 Friend Functions

A \_\_global\_\_ function or function template cannot be defined in a friend declaration.

Example:

```c
struct S1_t {
  friend __global__
  void foo1(void);  // OK: not a definition
  template<typename T>
  friend __global__
  void foo2(void); // OK: not a definition

  friend __global__
  void foo3(void) { } // error: definition in friend declaration

  template<typename T>
  friend __global__
  void foo4(void) { } // error: definition in friend declaration
};
```

## 18.5.10.8 Operator Function

An operator function cannot be a \_\_global\_\_ function.

## 18.5.10.9 Allocation and Deallocation Functions

A user-defined operator new, operator new[], operator delete, or operator delete[] cannot be used to replace the corresponding \_\_host\_\_ or \_\_device\_\_ builtins provided by the compiler.

## 18.5.11. Classes

## 18.5.11.1 Data Members

Static data members are not supported except for those that are also const-qualified (see Constqualified variables).

## 18.5.11.2 Function Members

Static member functions cannot be \_\_global\_\_ functions.

## 18.5.11.3 Virtual Functions

When a function in a derived class overrides a virtual function in a base class, the execution space specifiers (i.e., \_\_host\_\_, \_\_device\_\_) on the overridden and overriding functions must match.

It is not allowed to pass as an argument to a \_\_global\_\_ function an object of a class with virtual functions.

If an object is created in host code, invoking a virtual function for that object in device code has undefined behavior.

If an object is created in device code, invoking a virtual function for that object in host code has undefined behavior.

See Windows-Specific for additional constraints when using the Microsoft host compiler.

Example:

```txt
struct S1 { virtual __host__ __device__ void foo() { } };

__managed__ S1 *ptr1, *ptr2;

__managed__ __align__(16) char buf1[128];
__global__ void kern() {
    ptr1->foo();      // error: virtual function call on a object
                        //          created in host code.
    ptr2 = new(buf1) S1();
}

int main(void) {
    void *buf;
    cudaMallocManaged(&buf, sizeof(S1), cudaMemAttachGlobal);
    ptr1 = new (buf) S1();
    kern<<<1,1>>>();
    cudaDeviceSynchronize();
    ptr2->foo();  // error: virtual function call on an object
                        //          created in device code.
}
```

## 18.5.11.4 Virtual Base Classes

It is not allowed to pass as an argument to a \_\_global\_\_ function an object of a class derived from virtual base classes.

See Windows-Specific for additional constraints when using the Microsoft host compiler.

## 18.5.11.5 Anonymous Unions

Member variables of a namespace scope anonymous union cannot be referenced in a \_\_global\_\_ or \_\_device\_\_ function.

## 18.5.11.6 Windows-Specific

The CUDA compiler follows the IA64 ABI for class layout, while the Microsoft host compiler does not. Let T denote a pointer to member type, or a class type that satisfies any of the following conditions:

▶ T has virtual functions.

▶ T has a virtual base class.

▶ T has multiple inheritance with more than one direct or indirect empty base class.

All direct and indirect base classes B of T are empty and the type of the first field F of T uses B in its definition, such that B is laid out at ofset 0 in the definition of F.

Let C denote T or a class type that has T as a field type or as a base class type. The CUDA compiler may compute the class layout and size diferently than the Microsoft host compiler for the type C.

As long as the type C is used exclusively in host or device code, the program should work correctly.

Passing an object of type C between host and device code has undefined behavior, for example, as an argument to a \_\_global\_\_ function or through cudaMemcpy\*() calls.

Accessing an object of type C or any subobject in device code, or invoking a member function in device code, has undefined behavior if the object is created in host code.

Accessing an object of type C or any subobject in host code, or invoking a member function in host code, has undefined behavior if the object is created in device code<sup>12</sup>.

## 18.5.12. Templates

A type or template cannot be used in the type, non-type or template template argument of a \_\_global\_\_ function template instantiation or a \_\_device\_\_∕\_\_constant\_\_ variable instantiation if either:

▶ The type or template is defined within a \_\_host\_\_ or \_\_host\_\_ \_\_device\_\_.

▶ The type or template is a class member with private or protected access and its parent class is not defined within a \_\_device\_\_ or \_\_global\_\_ function.

▶ The type is unnamed.

▶ The type is compounded from any of the types above.

<sup>12</sup> One way to debug suspected layout mismatch of a type C is to use printf to output the values of sizeof(C) and offsetof(C, field) in host and device code.

Example:

```cpp
template <typename T>
__global__ void myKernel(void) { }

class myClass {
private:
    struct inner_t { };
public:
    static void launch(void)
    {
        // error: inner_t is used in template argument
        // but it is private
        myKernel<inner_t><<<1,1>>>(();
    }
};

// C++14 only
template <typename T> __device__ T d1;

template <typename T1, typename T2> __device__ T1 d2;

void fn() {
    struct S1_t { };
    // error (C++14 only): S1_t is local to the function fn
    d1<S1_t> = {}

    auto lam1 = [] { };
    // error (C++14 only): a closure type cannot be used for
    // instantiating a variable template
    d2<int, decltype(lam1)> = 10;
}
```

## 18.5.13. Trigraphs and Digraphs

Trigraphs are not supported on any platform. Digraphs are not supported on Windows.

## 18.5.14. Const-qualified variables

Let ‘V’ denote a namespace scope variable or a class static member variable that has const qualified type and does not have execution space annotations (for example, \_\_device\_\_, \_\_constant\_\_, \_\_shared\_\_). V is considered to be a host code variable.

The value of V may be directly used in device code, if

V has been initialized with a constant expression before the point of use,

the type of V is not volatile-qualified, and

it has one of the following types:

▶ built-in floating point type except when the Microsoft compiler is used as the host compiler,

▶ built-in integral type.

Device source code cannot contain a reference to V or take the address of V.

Example:

```lisp
const int xxx = 10;
struct S1_t { static const int yyy = 20; };

extern const int zzz;
const float www = 5.0;
__device__ void foo(void) {
    int local1[xxx];          // OK
    int local2[S1_t::yyy];   // OK

    int val1 = xxx;                // OK

    int val2 = S1_t::yyy;   // OK

    int val3 = zzz;                 // error: zzz not initialized with constant
                                        // expression at the point of use.

    const int &val3 = xxx;     // error: reference to host variable
    const int *val4 = &xxx;   // error: address of host variable
    const float val5 = www;   // OK except when the Microsoft compiler is used as
                                        // the host compiler.
}
const int zzz = 20;
```
