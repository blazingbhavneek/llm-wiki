
In the common case where MyKernel is invoked with the maximum number of threads per block (specified as the first parameter of \_\_launch\_bounds\_\_()), it is tempting to use MY\_KERNEL\_MAX\_THREADS as the number of threads per block in the execution configuration:

```txt
// Host code
MyKernel<<<blocksPerGrid, MY_KERNEL_MAX_THREADS>>>(...);
```

This will not work however since \_\_CUDA\_ARCH\_\_ is undefined in host code as mentioned in Application Compatibility, so MyKernel will launch with 256 threads per block even when \_\_CUDA\_ARCH\_\_ is greater or equal to 200. Instead the number of threads per block should be determined:

▶ Either at compile time using a macro that does not depend on \_\_CUDA\_ARCH\_\_, for example

```txt
// Host code
MyKernel<<<blocksPerGrid, THREADS_PER_BLOCK>>>(...);
```

▶ Or at runtime based on the compute capability

```c
// Host code
cudaGetDeviceProperties(&deviceProp, device);
int threadsPerBlock =
    (deviceProp.major >= 2 ?
        2 * THREADS_PER_BLOCK : THREADS_PER_BLOCK);
MyKernel<<<blocksPerGrid, threadsPerBlock>>>(...);
```

Register usage is reported by the --ptxas-options=-v compiler option. The number of resident blocks can be derived from the occupancy reported by the CUDA profiler (see Device Memory Accesses for a definition of occupancy).

# 10.39. Maximum Number of Registers per Thread

To provide a mechanism for low-level performance tuning, CUDA C++ provides the \_\_maxnreg\_\_() function qualifier to pass performance tuning information to the backend optimizing compiler. The \_maxnreg\_\_() qualifier specifies the maximum number of registers to be allocated to a single thread in a thread block. In the definition of a \_\_global\_\_ function:

```lisp
__global__ void
__maxnreg__(maxNumberRegistersPerThread)
MyKernel(...)
{
    ...
}
```

▶ maxNumberRegistersPerThread specifies the maximum number of registers to be allocated to a single thread in a thread block of the kernel MyKernel(); it compiles to the .maxnregPTX directive.

The \_\_launch\_bounds\_\_() and \_\_maxnreg\_\_() qualifiers cannot be applied to the same kernel.

Register usage can also be controlled for all \_\_global\_\_ functions in a file using the maxrregcount compiler option. The value of maxrregcount is ignored for functions with the \_\_maxnreg\_\_ qualifier.

## 10.40. #pragma unroll

By default, the compiler unrolls small loops with a known trip count. The #pragma unroll directive however can be used to control unrolling of any given loop. It must be placed immediately before the loop and only applies to that loop. It is optionally followed by an integral constant expression (ICE)<sup>6</sup>. If the ICE is absent, the loop will be completely unrolled if its trip count is constant. If the ICE evaluates to 1, the compiler will not unroll the loop. The pragma will be ignored if the ICE evaluates to a non-positive integer or to an integer greater than the maximum value representable by the int data type.

Examples:

```c
struct S1_t { static const int value = 4; };
template <int X, typename T2>
__device__ void foo(int *p1, int *p2) {

// no argument specified, loop will be completely unrolled
#pragma unroll
for (int i = 0; i < 12; ++i)
    p1[i] += p2[i]*2;

// unroll value = 8
#pragma unroll (X+1)
for (int i = 0; i < 12; ++i)
    p1[i] += p2[i]*4;

// unroll value = 1, loop unrolling disabled
```

(continues on next page)

```c
#pragma unroll 1
for (int i = 0; i < 12; ++i)
    p1[i] += p2[i]*8;

// unroll value = 4
#pragma unroll (T2::value)
for (int i = 0; i < 12; ++i)
    p1[i] += p2[i]*16;
}

__global__ void bar(int *p1, int *p2) {
foo<7, S1_t>(p1, p2);
}
```

(continued from previous page)

## 10.41. SIMD Video Instructions

PTX ISA version 3.0 includes SIMD (Single Instruction, Multiple Data) video instructions which operate on pairs of 16-bit values and quads of 8-bit values. These are available on devices of compute capability 3.0.

The SIMD video instructions are:

▶ vadd2, vadd4

▶ vsub2, vsub4

▶ vavrg2, vavrg4

▶ vabsdif2, vabsdif4

▶ vmin2, vmin4

▶ vmax2, vmax4

▶ vset2, vset4

PTX instructions, such as the SIMD video instructions, can be included in CUDA programs by way of the assembler, asm(), statement.

The basic syntax of an asm() statement is:

```javascript
asm("template-string" : "constraint"(output) : "constraint"(input)"));
```

An example of using the vabsdiff4 PTX instruction is:

```javascript
asm("vabsdiff4.u32.u32.u32.add" " %0, %1, %2, %3;": "=r" (result):"r" (A), "r" (B), "r
→" (C));
```

This uses the vabsdiff4 instruction to compute an integer quad byte SIMD sum of absolute diferences. The absolute diference value is computed for each byte of the unsigned integers A and B in SIMD fashion. The optional accumulate operation (.add) is specified to sum these diferences.

Refer to the document “Using Inline PTX Assembly in CUDA” for details on using the assembly statement in your code. Refer to the PTX ISA documentation (“Parallel Thread Execution ISA Version 3.0” for example) for details on the PTX instructions for the version of PTX that you are using.

## 10.42. Diagnostic Pragmas

The following pragmas may be used to control the error severity used when a given diagnostic message is issued.

```c
#pragma nv_diag_suppress
#pragma nv_diag_warning
#pragma nv_diag_error
#pragma nv_diag_default
#pragma nv_diag_once
```

Uses of these pragmas have the following form:

```python
#pragma nv_diag_xxx error_number, error_number ...
```

The diagnostic afected is specified using an error number showed in a warning message. Any diagnostic may be overridden to be an error, but only warnings may have their severity suppressed or be restored to a warning after being promoted to an error. The nv\_diag\_default pragma is used to return the severity of a diagnostic to the one that was in efect before any pragmas were issued (i.e., the normal severity of the message as modified by any command-line options). The following example suppresses the "declared but never referenced" warning on the declaration of foo:

```c
#pragma nv_diag_suppress 177
void foo()
{
    int i=0;
}
#pragma nv_diag_default 177
void bar()
{
    int i=0;
}
```

The following pragmas may be used to save and restore the current diagnostic pragma state:

```txt
#pragma nv_diagnostic push
#pragma nv_diagnostic pop
```

Examples:

```c
#pragma nv_diagnostic push
#pragma nv_diag_suppress 177
void foo()
{
    int i=0;
}
#pragma nv_diagnostic pop
void bar()
{
    int i=0;
}
```

Note that the pragmas only afect the nvcc CUDA frontend compiler; they have no efect on the host compiler.

Removal Notice: The support of diagnostic pragmas without nv\_ prefix are removed from CUDA 12.0, if the pragmas are inside the device code, warning unrecognized #pragma in device code will be emitted, otherwise they will be passed to the host compiler. If they are intended for CUDA code, use the pragmas with nv\_ prefix instead.

## 10.43. Custom ABI Pragmas

The #pragma nv\_abi directive enables applications compiled in separate compilation mode to achieve performance similar to that of whole program compilation.

The syntax for using this pragma is as follows, where ICE refers to any integral constant expression (ICE):<sup>Page</sup> <sup>276,</sup> <sup>6</sup>.

```c
#pragma nv_abi preserve_n_data(ICE) preserve_n_control(ICE)
```

Note, the arguments that follow #pragma nv\_abi are optional and can be provided in any order; however, at least one argument is required.

The preserve\_n arguments set a limit on the number of registers preserved during a function call:

▶ preserve\_n\_data(ICE) limits the number of data registers, and

▶ preserve\_n\_control(ICE) limits the number of control registers.

#pragma nv\_abi can be placed immediately before a device function declaration or definition. Alternatively, it can be placed directly before an indirect function call within a C++ expression statement inside a device function. Note, indirect function calls to free functions are supported, but indirect calls through function argument references or class member functions are not.

When the pragma is applied to a device function declaration or definition, it modifies the custom ABI properties for any calls to that function. When placed at an indirect function call site, the pragma afects the ABI properties for that indirect function call. The key point is that unlike direct function calls, where you can place the pragma before a function declaration or definition, #pragma nv\_abi only afects indirect function calls when the pragma is placed before a call site.

As shown in the following example, we have two device functions, foo() and bar(). In this example the pragma is placed before the call site of the function pointer fptr to modify the ABI properties of the indirect function call. Notice that placing the pragma before the direct call does not afect the ABI properties of the call. To alter the ABI properties of a direct function call, the pragma must be placed before the function declaration or definition.

```c
__device__ int foo()
{
    int value{0};
    ...
    return value;
}

__device__ int bar()
{
    int value{0};
    ...
    return value;
}

__device__ void baz()
{
    int result{0};
```

(continues on next page)

```c
int (*fptr() = foo;  // function pointer

#pragma nv_abi preserve_n_data(16) preserve_n_control(8)
result = fptr();      // The pragma affects the indirect call to foo() via fptr

#pragma nv_abi preserve_n_data(16) preserve_n_control(8)
result = (*fptr();   // Alternate syntax for the indirect call to foo()

#pragma nv_abi preserve_n_data(16) preserve_n_control(8)
result += bar();      // The pragma does NOT affect the direct call to bar()
}
```

As shown in the following example, to modify direct function calls, you must apply the pragma to the function declaration or definition.

```c
#pragma nv_abi preserve_n_data(16)
__device__ void foo();
```

Note that a program is ill-formed if the pragma arguments for a function declaration and its corresponding definition do not match.

## 10.44. CUDA C++ Memory Model

The CUDA C++ Memory Model extends the ISO C++ Memory Model as documented in the CUDA C++ Memory Model documentation.

## 10.45. CUDA C++ Execution Model

The CUDA C++ Exeuction Model extends the ISO C++ execution model as documented in the CUDA C++ Execution Model documentation.
