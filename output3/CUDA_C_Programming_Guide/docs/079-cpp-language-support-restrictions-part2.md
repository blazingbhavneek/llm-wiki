▶ When a CUDA program containing managed variables is run on an execution platform with multiple GPUs, the variables are allocated only once, and not per GPU.

▶ A managed variable declaration without the extern linkage is not allowed within a function that executes on the host.

▶ A managed variable declaration without the extern or static linkage is not allowed within a function that executes on the device.

Here are examples of legal and illegal uses of managed variables:

```c
__device__ __managed__ int xxx = 10;          // OK

int *ptr = &xxx;                       // error: use of managed variable
                                            // (xxx) in static initialization
struct S1_t {
    int field;
    S1_t(void) : field(xxx) { };
};
struct S2_t {
    ~S2_t(void) { xxx = 10; }
```

(continues on next page)

```lisp
};
S1_t temp1;                                // error: use of managed variable
                                // (xxx) in dynamic initialization

S2_t temp2;                                // error: use of managed variable
                                // (xxx) in the destructor of
                                // object with static storage
                                // duration

__device__ __managed__ const int yyy = 10;    // error: const qualified type

__device__ __managed__ int &zzz = xxx;      // error: reference type

template <int *addr> struct S3_t { }; S3_t<&xxx> temp;                             // error: address of managed
                                // variable(xxx) not a
                                // constant expression

__global__ void kern(int *ptr)
{
    assert(ptr == &xxx);                    // OK
    xxx = 20;                            // OK
}
int main(void)
{
    int *ptr = &xxx;                             // OK
    kern<<<1,1>>>(ptr);
    cudaDeviceSynchronize();                      // OK
    xxx++;                                   // OK
    decltype(xxx) qqq;                       // error: managed variable(xxx) used
                                // as unparenthesized argument to
                                // decltype

    decltype((xxx)) zzz = yyy;          // OK
}
```

## 18.5.3.3 Volatile Qualifier

Note: The volatile keyword is supported to maintain compatibility with ISO C++; however, few if any of its remaining non-deprecated uses apply to GPUs.

Reads and writes to volatile qualified objects are not atomic, and are compiled to one or more .volatile instructions which do NOT guarantee:

▶ ordering of memory operations, or

▶ that the number of memory operations performed by the HW matches the number of PTX instructions.

That is, CUDA C++ volatile is not suitable for:

Inter-Thread Synchronization: use atomic operations via cuda::atomic\_ref, cuda::atomic, or Atomic Functions instead. Atomic memory operations provide inter-thread synchronization guarantees and deliver much better performance than volatile operations. CUDA C++ volatile operations do not provide any inter-thread synchronization guarantees and are therefore not correct for inter-thread synchronization. The following example shows how to pass a message across two threads using atomic operations.

cuda::atomic\_ref

```cpp
__global__ void kernel(int* flag, int* data) {
    cuda::atomic_ref<int, cuda::thread_scope_device> f{*flag};
    if (threadIdx.x == 0) {
        // Consumer: blocks until flag is set by producer, then reads data
        while(f.load(cuda::memory_order_acquire) == 0);
        if (*data != 42) __trap(); // Errors if wrong data read
    } else if (threadIdx.x == 1) {
        // Producer: writes data then sets flag
        *data = 42;
        f.store(1, cuda::memory_order_release);
    }
}
```

## cuda::atomic

```cpp
__global__ void kernel(cuda::atomic<int, cuda::thread_scope_device>*
flag, int* data) {
  if (threadIdx.x == 0) {
    // Consumer: blocks until flag is set by producer, then reads data
    while(flag->load(cuda::memory_order_acquire) == 0);
    if (*data != 42) __trap(); // Errors if wrong data read
  } else if (threadIdx.x == 1) {
    // Producer: writes data then sets flag
    *data = 42;
    flag->store(1, cuda::memory_order_release);
  }
}
```

Atomic Functions (atomicAdd and atomicExch)

```lisp
__global__ void kernel(int* flag, int* data) {
    if (threadIdx.x == 0) {
        // Consumer: blocks until flag is set by producer, then reads data
        while(atomicAdd(flag, 0) == 0); // Load with Relaxed Read-Modify-Write
        __threadfence();                  // SequentiallyConsistent fence
        if (*data != 42) __trap();      // Errors if wrong data read
    } else if (threadIdx.x == 1) {
        // Producer: writes data then sets flag
        *data = 42;
        __threadfence();      // SequentiallyConsistent fence
        atomicExch(flag, 1); // Store with Relaxed Read-Modify-Write
    }
}
```

Memory Mapped IO (MMIO): use PTX MMIO operations via inline PTX instead. PTX MMIO operations strictly preserve the number of memory accesses performed. CUDA C++ volatile operations do not preserve the number of memory accesses performed, and may perform more or less accesses than requested in a non-deterministic way, making them incorrect for MMIO. The following example shows how to read and write from a register using PTX mmio operations.

```javascript
__global__ void kernel(int* mmio_reg0, int* mmio_reg1) {
    // Write to MMIO register:
    int value = 13;
    asm volatile("st.relaxed.mmio.sys.u32 [%0], %1;" :: "l"(mmio_reg0), "r
    "value) : "memory");

    // Read MMIO register:
    asm volatile("ld.relaxed.mmio.sys.u32 %0, [%1];" : "=r"(value) : "l
    "mmio_reg1) : "memory");

    if (value != 42) __trap(); // Errors if wrong data read
}
```

## 18.5.4. Pointers

Dereferencing a pointer either to global or shared memory in code that is executed on the host, or to host memory in code that is executed on the device results in an undefined behavior, most often in a segmentation fault and application termination.

The address obtained by taking the address of a \_\_device\_\_, \_\_shared\_\_ or \_\_constant\_\_ variable can only be used in device code. The address of a \_\_device\_\_ or \_\_constant\_\_ variable obtained through cudaGetSymbolAddress() as described in Device Memory can only be used in host code.

## 18.5.5. Operators

## 18.5.5.1 Assignment Operator

\_\_constant\_\_ variables can only be assigned from the host code through runtime functions (Device Memory); they cannot be assigned from the device code.

\_\_shared\_\_ variables cannot have an initialization as part of their declaration.

It is not allowed to assign values to any of the built-in variables defined in Built-in Variables.

## 18.5.5.2 Address Operator

It is not allowed to take the address of any of the built-in variables defined in Built-in Variables.

## 18.5.6. Run Time Type Information (RTTI)

The following RTTI-related features are supported in host code, but not in device code.

▶ typeid operator

▶ std::type\_info

▶ dynamic\_cast operator

## 18.5.7. Exception Handling

Exception handling is only supported in host code, but not in device code.

Exception specification is not supported for \_\_global\_\_ functions.

## 18.5.8. Standard Library

Standard libraries are only supported in host code, but not in device code, unless specified otherwise.

## 18.5.9. Namespace Reservations

Unless an exception is otherwise noted, it is undefined behavior to add any declarations or definitions to cuda::, nv::, cooperative\_groups:: or any namespace nested within.

Examples:

```cpp
namespace cuda{
    // Bad: class declaration added to namespace cuda
    struct foo{};

    // Bad: function definition added to namespace cuda
```

(continues on next page)

(continued from previous page)

```cpp
cudaStream_t make_stream(){
    cudaStream_t s;
    cudaStreamCreate(&s);
    return s;
}
} // namespace cuda

namespace cuda{
    namespace utils{
        // Bad: function definition added to namespace nested within cuda
        cudaStream_t make_stream(){
            cudaStream_t s;
            cudaStreamCreate(&s);
            return s;
        }
    } // namespace utils
} // namespace cuda

namespace utils{
    namespace cuda{
        // Okay: namespace cuda may be used nested within a non-reserved namespace
        cudaStream_t make_stream(){
            cudaStream_t s;
            cudaStreamCreate(&s);
            return s;
        }
    } // namespace cuda
} // namespace utils

// Bad: Equivalent to adding symbols to namespace cuda at global scope
using namespace utils;
```
