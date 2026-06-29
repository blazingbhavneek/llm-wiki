# Formatted Output (printf) in CUDA

CUDA supports formatted output from device kernels using the `printf()` function. This feature is available on devices with compute capability 2.x and higher [CUDA_C_Programming_Guide:L11173-L11190]. The in-kernel `printf()` behaves similarly to the standard C-library `printf()`, but outputs to a host-side stream rather than the device console [CUDA_C_Programming_Guide:L11173-L11190].

## Basic Usage

The function signature is:

```c
int printf(const char *format[, arg, ...]);
```

When called from a kernel, the format string is processed and the resulting output is sent to the host [CUDA_C_Programming_Guide:L11173-L11190]. The command is executed per-thread in the context of the calling thread [CUDA_C_Programming_Guide:L11173-L11190]. Consequently, if a kernel launches multiple threads, each thread will execute the `printf()` call, potentially generating multiple lines of output [CUDA_C_Programming_Guide:L11173-L11190].

### Return Values

Unlike the standard C `printf()`, which returns the number of characters printed, CUDA's `printf()` returns the number of arguments parsed [CUDA_C_Programming_Guide:L11173-L11190].
- Returns `0` if no arguments follow the format string.
- Returns `-1` if the format string is `NULL`.
- Returns `-2` if an internal error occurs [CUDA_C_Programming_Guide:L11173-L11190].

## Format Specifiers

Format specifiers follow the standard form: `%[flags][width][. precision][size]type` [CUDA_C_Programming_Guide:L11191-L11209].

Supported fields include:
- **Flags**: `#`, ` `, `0`, `+`, `-` [CUDA_C_Programming_Guide:L11191-L11209]
- **Width**: `*`, `0-9` [CUDA_C_Programming_Guide:L11191-L11209]
- **Precision**: `0-9` [CUDA_C_Programming_Guide:L11191-L11209]
- **Size**: `h`, `l`, `ll` [CUDA_C_Programming_Guide:L11191-L11209]
- **Type**: `%c`, `%d`, `%i`, `%o`, `%u`, `%x`, `%X`, `%e`, `%E`, `%f`, `%g`, `%G`, `%a`, `%A`, `%s` [CUDA_C_Programming_Guide:L11191-L11209]

CUDA's `printf()` accepts any combination of these flags, widths, precisions, sizes, and types, even if they do not form a valid format specifier for the host system [CUDA_C_Programming_Guide:L11191-L11209]. For example, `%hd` is accepted, and `printf` will expect a double-precision variable in the corresponding argument list position [CUDA_C_Programming_Guide:L11191-L11209].

## Limitations and Behavior

### Host-Side Formatting
Final formatting of the output takes place on the host system [CUDA_C_Programming_Guide:L11210-L11238]. The format string must be understood by the host-system's compiler and C library [CUDA_C_Programming_Guide:L11210-L11238]. While CUDA aims to support a universal subset of format specifiers, exact behavior is host-OS-dependent [CUDA_C_Programming_Guide:L11210-L11238].

### Argument Limits
`printf()` can accept at most 32 arguments in addition to the format string [CUDA_C_Programming_Guide:L11210-L11238]. Additional arguments beyond this limit are ignored, and the format specifier is output as-is [CUDA_C_Programming_Guide:L11210-L11238].

### Platform Compatibility
Due to differences in the `long` type size on 64-bit Windows (4 bytes) versus other 64-bit platforms (8 bytes), kernels compiled on non-Windows 64-bit machines may produce corrupted output for format strings including `%ld` when run on Windows 64-bit [CUDA_C_Programming_Guide:L11210-L11238]. It is recommended that the compilation platform matches the execution platform [CUDA_C_Programming_Guide:L11210-L11238].

### Buffer Management
The output buffer is circular and has a fixed size before kernel launch [CUDA_C_Programming_Guide:L11210-L11238]. If more output is produced than the buffer can hold, older output is overwritten [CUDA_C_Programming_Guide:L11210-L11238]. The buffer is flushed only when specific actions occur:
- Kernel launch via `<<<>>>` or `cuLaunchKernel()` (at the start, and at the end if `CUDA_LAUNCH_BLOCKING` is set to 1) [CUDA_C_Programming_Guide:L11210-L11238].
- Synchronization via `cudaDeviceSynchronize()`, `cuCtxSynchronize()`, `cudaStreamSynchronize()`, `cuStreamSynchronize()`, `cudaEventSynchronize()`, or `cuEventSynchronize()` [CUDA_C_Programming_Guide:L11210-L11238].
- Memory copies via any blocking version of `cudaMemcpy*()` or `cuMemcpy*()` [CUDA_C_Programming_Guide:L11210-L11238].
- Module loading/unloading via `cuModuleLoad()` or `cuModuleUnload()` [CUDA_C_Programming_Guide:L11210-L11238].
- Context destruction via `cudaDeviceReset()` or `cuCtxDestroy()` [CUDA_C_Programming_Guide:L11210-L11238].
- Prior to executing a stream callback added by `cudaLaunchHostFunc` or `cuLaunchHostFunc` [CUDA_C_Programming_Guide:L11210-L11238].

The buffer is **not** flushed automatically when the program exits; the user must call `cudaDeviceReset()` or `cuCtxDestroy()` explicitly [CUDA_C_Programming_Guide:L11210-L11238].

### Thread Execution Order
Internally, `printf()` uses a shared data structure, which may alter the order of thread execution [CUDA_C_Programming_Guide:L11210-L11238]. A thread calling `printf()` may take a longer execution path than one that does not [CUDA_C_Programming_Guide:L11210-L11238]. However, CUDA makes no guarantees of thread execution order except at explicit `__syncthreads()` barriers, so it is impossible to determine if execution order was modified by `printf()` or by other hardware scheduling behavior [CUDA_C_Programming_Guide:L11210-L11238].

## Buffer Size Configuration

The size of the buffer used to transfer `printf()` arguments and metadata to the host defaults to 1 megabyte [CUDA_C_Programming_Guide:L11239-L11245]. This can be configured using the following API functions:

- `cudaDeviceGetLimit(size_t* size, cudaLimitPrintfFifoSize)` [CUDA_C_Programming_Guide:L11239-L11245]
- `cudaDeviceSetLimit(cudaLimitPrintfFifoSize, size_t size)` [CUDA_C_Programming_Guide:L11239-L11245]

## Examples

### Basic Output
The following kernel prints output for every thread:

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

This produces output similar to:

```txt
Hello thread 2, f=1.2345
Hello thread 1, f=1.2345
Hello thread 4, f=1.2345
Hello thread 0, f=1.2345
Hello thread 3, f=1.2345
```

Each thread encounters the `printf()` command, resulting in one line of output per thread [CUDA_C_Programming_Guide:L11246-L11303]. Global values (e.g., `float f`) are common to all threads, while local values (e.g., `threadIdx.x`) are distinct per-thread [CUDA_C_Programming_Guide:L11246-L11303].

### Limited Output
To restrict output to a single thread, an `if` statement can be used:

```c
#include <stdio.h>

__global__ void helloCUDA(float f)
{
    if (threadIdx.x == 0)
        printf("Hello thread %d, f=%f\n", threadIdx.x, f);
}

int main()
{
    helloCUDA<<<1, 5>>>(1.2345f);
    cudaDeviceSynchronize();
    return 0;
}
```

This produces only:

```txt
Hello thread 0, f=1.2345
```

The `if()` statement limits which threads call `printf()`, ensuring only a single line of output is seen [CUDA_C_Programming_Guide:L11246-L11303].
