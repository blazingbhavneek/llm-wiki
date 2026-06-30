# __global__ Function Argument Processing

Behavior of __global__ function arguments from host code: memcpy instead of copy constructors, and potential early destructor invocation due to asynchronous execution.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L17032-L17148

Citation: [CUDA_C_Programming_Guide:L17032-L17148]

````text

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
````
