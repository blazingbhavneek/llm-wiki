# Formatted Output

Formatted output is supported on compute capability 2.x and higher via the in-kernel printf() function. It behaves similarly to the standard C library printf() but outputs to a host-side stream. Each thread executes printf independently. The function returns the number of arguments parsed. Limitations include host-dependent formatting, a 32-argument limit, potential output corruption on win64 with %ld, and a fixed-size circular buffer that flushes on kernel launch, synchronization, memory copies, module loading, context destruction, or stream callbacks. Thread execution order may be affected.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L11173-L11301

Citation: [CUDA_C_Programming_Guide:L11173-L11301]

````text

Formatted output is only supported by devices of compute capability 2.x and higher.

```c
int printf(const char *format[, arg, ...]);
```

prints formatted output from a kernel to a host-side output stream.

The in-kernel printf() function behaves in a similar way to the standard C-library printf() function, and the user is referred to the host system’s manual pages for a complete description of printf() behavior. In essence, the string passed in as format is output to a stream on the host, with substitutions made from the argument list wherever a format specifier is encountered. Supported format specifiers are listed below.

The printf() command is executed as any other device-side function: per-thread, and in the context of the calling thread. From a multi-threaded kernel, this means that a straightforward call to printf() will be executed by every thread, using that thread’s data as specified. Multiple versions of the output string will then appear at the host stream, once for each thread which encountered the printf().

It is up to the programmer to limit the output to a single thread if only a single output string is desired (see Examples for an illustrative example).

Unlike the C-standard printf(), which returns the number of characters printed, CUDA’s printf() returns the number of arguments parsed. If no arguments follow the format string, 0 is returned. If the format string is NULL, -1 is returned. If an internal error occurs, -2 is returned.

## 10.35.1. Format Specifiers

As for standard printf(), format specifiers take the form: %[flags][width][. precision][size]type

The following fields are supported (see widely-available documentation for a complete description of all behaviors):

```txt
▶ Flags: '#' ' ' '0' '+' '-'
```

▶ Width: '\*' '0-9'

▶ Precision: '0-9'

▶ Size: 'h' 'l' 'll

▶ Type: "%cdiouxXpeEfgGaAs"

Note that CUDA’s printf()will accept any combination of flag, width, precision, size and type, whether or not overall they form a valid format specifier. In other words, “%hd” will be accepted and printf will expect a double-precision variable in the corresponding location in the argument list.

## 10.35.2. Limitations

Final formatting of the printf()output takes place on the host system. This means that the format string must be understood by the host-system’s compiler and C library. Every efort has been made to ensure that the format specifiers supported by CUDA’s printf function form a universal subset from the most common host compilers, but exact behavior will be host-OS-dependent.

As described in Format Specifiers, printf() will accept all combinations of valid flags and types. This is because it cannot determine what will and will not be valid on the host system where the final output is formatted. The efect of this is that output may be undefined if the program emits a format string which contains invalid combinations.

The printf() command can accept at most 32 arguments in addition to the format string. Additional arguments beyond this will be ignored, and the format specifier output as-is.

Owing to the difering size of the long type on 64-bit Windows platforms (four bytes on 64-bit Windows platforms, eight bytes on other 64-bit platforms), a kernel which is compiled on a non-Windows 64-bit machine but then run on a win64 machine will see corrupted output for all format strings which include “%ld”. It is recommended that the compilation platform matches the execution platform to ensure safety.

The output bufer for printf() is set to a fixed size before kernel launch (see Associated Host-Side API). It is circular and if more output is produced during kernel execution than can fit in the bufer, older output is overwritten. It is flushed only when one of these actions is performed:

▶ Kernel launch via <<<>>> or cuLaunchKernel() (at the start of the launch, and if the CUDA\_LAUNCH\_BLOCKING environment variable is set to 1, at the end of the launch as well),

▶ Synchronization via cudaDeviceSynchronize(), cuCtxSynchronize(), cudaStreamSynchronize(), cuStreamSynchronize(), cudaEventSynchronize(), or cuEventSynchronize(),

▶ Memory copies via any blocking version of cudaMemcpy\*() or cuMemcpy\*(),

▶ Module loading/unloading via cuModuleLoad() or cuModuleUnload(),

▶ Context destruction via cudaDeviceReset() or cuCtxDestroy().

Prior to executing a stream callback added by cudaLaunchHostFunc or cuLaunchHostFunc.

Note that the bufer is not flushed automatically when the program exits. The user must call cudaDeviceReset() or cuCtxDestroy() explicitly, as shown in the examples below.

Internally printf() uses a shared data structure and so it is possible that calling printf() might change the order of execution of threads. In particular, a thread which calls printf() might take a longer execution path than one which does not call printf(), and that path length is dependent upon the parameters of the printf(). Note, however, that CUDA makes no guarantees of thread execution order except at explicit \_\_syncthreads() barriers, so it is impossible to tell whether execution order has been modified by printf() or by other scheduling behavior in the hardware.

## 10.35.3. Associated Host-Side API

The following API functions get and set the size of the bufer used to transfer the printf() arguments and internal metadata to the host (default is 1 megabyte):

▶ cudaDeviceGetLimit(size\_t\* size,cudaLimitPrintfFifoSize)

cudaDeviceSetLimit(cudaLimitPrintfFifoSize, size\_t size)

## 10.35.4. Examples

The following code sample:

```c
#include <stdio.h>

__global__ void helloCUDA(float f)
{
    printf("Hello thread %d, f=%f\n", threadIdx.x, f);
}

int main()
{
    helloCUDA<<<1, 5>>>(1.2345f);
    cudaDeviceSynchronize();
    return 0;
}
```

will output:

```txt
Hello thread 2, f=1.2345
Hello thread 1, f=1.2345
Hello thread 4, f=1.2345
Hello thread 0, f=1.2345
Hello thread 3, f=1.2345
```

Notice how each thread encounters the printf() command, so there are as many lines of output as there were threads launched in the grid. As expected, global values (i.e., float f) are common between all threads, and local values (i.e., threadIdx.x) are distinct per-thread.

The following code sample:

```c
#include <stdio.h>

__global__ void helloCUDA(float f)
{
    if (threadIdx.x == 0)
        printf("Hello thread %d, f=%f\n", threadIdx.x, f) ;
}

int main()
{
    helloCUDA<<<1, 5>>>(1.2345f);
    cudaDeviceSynchronize();
    return 0;
}
```

will output:

Hello thread 0, f=1.2345

Self-evidently, the if() statement limits which threads will call printf, so that only a single line of output is seen.
````
