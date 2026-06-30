# Function Parameters

Limits on __global__ function parameters (32,764 bytes on Volta+, 4 KB older), restrictions on variable arguments and pass-by-reference, and ODR requirements.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L17001-L17029

Citation: [CUDA_C_Programming_Guide:L17001-L17029]

````text
## 18.5.10.3 Function Parameters

\_\_global\_\_ function parameters are passed to the device via constant memory and are limited to 32,764 bytes starting with Volta, and 4 KB on older architectures.

\_\_global\_\_ functions cannot have a variable number of arguments.

\_\_global\_\_ function parameters cannot be pass-by-reference.

In separate compilation mode, if a \_\_device\_\_ or \_\_global\_\_ function is ODR-used in a particular translation unit, then the parameter and return types of the function must be complete in that translation unit.

Example:

```perl
//first.cu:
struct S;
__device__ void foo(S); // error: type 'S' is incomplete
__device__ auto *ptr = foo;

int main() { }

//second.cu:
struct S { int x; };
__device__ void foo(S) { }

//compiler invocation
\$nvcc -std=c++14 -rdc=true first.cu second.cu -o first
nvlink error : Prototype doesn't match for '_Z3foo1S' in '/tmp/tmpxft_00005c8c_00000000-18_second.o', first defined in '/tmp/tmpxft_00005c8c_00000000-18_second.o'
nvlink fatal : merge_elf failed
```
````
