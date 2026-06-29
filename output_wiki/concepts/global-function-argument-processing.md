# __global__ Function Argument Processing

The processing of arguments passed to `__global__` functions diverges from the standard C++ model depending on whether the launch originates from host or device code. User code must ensure that these specific workflows do not affect program correctness.

## Device Launches

When a `__global__` function is launched from device code, strict type requirements apply. Each argument passed to the function must be **trivially copyable** and **trivially destructible** [CUDA_C_Programming_Guide:L17031-L17035].

## Host Launches

When a `__global__` function is launched from host code, the compiler allows arguments to be non-trivially copyable or non-trivially destructible. However, the processing for such types does not follow the standard C++ model in two key areas: memcpy usage instead of copy constructors, and potential early destructor invocation [CUDA_C_Programming_Guide:L17036-L17043].

### 1. Memcpy Instead of Copy Constructor Invocation

When lowering a `__global__` function launch from host code, the compiler generates stub functions that copy parameters by value before using `memcpy` to copy the arguments to the `__global__` function’s parameter memory on the device [CUDA_C_Programming_Guide:L17044-L17050].

This process occurs even if an argument is non-trivially copyable. Consequently, the copy constructor is skipped, which may break programs where the copy constructor has side effects [CUDA_C_Programming_Guide:L17050-L17054].

**Example: Skipped Copy Constructor**

In the following example, the copy constructor initializes `ptr` to point to `x`. However, because the compiler uses `memcpy` to pass the argument to the kernel, the copy constructor is not invoked, and `in.ptr` remains uninitialized (or contains garbage) in the kernel [CUDA_C_Programming_Guide:L17055-L17073]:

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
  foo<<<1,1>>>(tmp);
  cudaDeviceSynchronize();
}
```

Similarly, if a copy constructor increments a counter, the assertion may fail because the compiler-generated stub functions may copy the argument by value more than once, but without invoking the copy constructor [CUDA_C_Programming_Guide:L17074-L17095]:

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

### 2. Destructor Timing

Kernel launches are asynchronous with host execution. As a result, if a `__global__` function argument has a non-trivial destructor, the destructor may execute in host code even before the `__global__` function has finished execution [CUDA_C_Programming_Guide:L17096-L17102].

This behavior can break programs where the destructor has side effects, such as freeing memory that the kernel is still accessing [CUDA_C_Programming_Guide:L17102-L17104].

**Example: Premature Destructor Invocation**

In the following example, the object `V` is copied by value to a compiler-generated stub function. The stub function bitwise copies the contents of the argument to kernel parameter memory. However, GPU kernel execution is asynchronous. Therefore, `S::~S()` will execute when the stub function returns, releasing allocated memory, even though the kernel may not have finished execution [CUDA_C_Programming_Guide:L17105-L17125]:

```cpp
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

## Caveats

- The behavior described above is specific to `__global__` function argument processing in CUDA C++. It does not follow the standard C++ model for host launches [CUDA_C_Programming_Guide:L17036-L17043].
- Developers must ensure that their code does not rely on copy constructors or destructors having side effects when passing objects to `__global__` functions [CUDA_C_Programming_Guide:L17043-L17044].
- For device launches, arguments must be trivially copyable and trivially destructible [CUDA_C_Programming_Guide:L17031-L17035].
