# Function Parameters

## __global__ Function Parameter Restrictions

Functions decorated with the `__global__` qualifier, which are executed on the device and launched from the host, have specific limitations on their parameters due to how they are passed to the device.

### Size Limits

`__global__` function parameters are passed to the device via constant memory. This imposes a strict size limit on the total size of the parameter list:

*   **Volta and newer architectures**: The limit is **32,764 bytes** [CUDA_C_Programming_Guide:L17001-L17002].
*   **Older architectures**: The limit is **4 KB** [CUDA_C_Programming_Guide:L17002-L17003].

### Prohibited Features

*   **Variable Arguments**: `__global__` functions cannot have a variable number of arguments (varargs) [CUDA_C_Programming_Guide:L17003-L17004].
*   **Pass-by-Reference**: `__global__` function parameters cannot be passed by reference [CUDA_C_Programming_Guide:L17004-L17005].

## Separate Compilation and ODR-Use

In separate compilation mode (e.g., using `-rdc=true`), One Definition Rule (ODR) usage imposes requirements on type completeness.

If a `__device__` or `__global__` function is ODR-used in a particular translation unit, the parameter and return types of that function must be **complete** in that translation unit [CUDA_C_Programming_Guide:L17005-L17007].

### Example of ODR Violation

The following example demonstrates an error where an incomplete type is used in a `__device__` function declaration in one translation unit, while the type is defined in another:

```cpp
// first.cu
struct S;
__device__ void foo(S); // error: type 'S' is incomplete
__device__ auto *ptr = foo;

int main() { }

// second.cu
struct S { int x; };
__device__ void foo(S) { }
```

When compiled with separate compilation enabled (`nvcc -std=c++14 -rdc=true first.cu second.cu -o first`), the linker will fail because the prototype does not match, as the type `S` was incomplete in the first translation unit where the function was declared [CUDA_C_Programming_Guide:L17008-L17029].

```bash
nvlink error : Prototype doesn't match for '_Z3foo1S' in '/tmp/tmpxft_00005c8c_00000000-18_second.o', first defined in '/tmp/tmpxft_00005c8c_00000000-18_second.o'
nvlink fatal : merge_elf failed
```
