# Default Stream

Kernel launches and host-to-device or device-to-host memory copies that do not specify any stream parameter, or equivalently set the stream parameter to zero, are issued to the default stream. Because operations in the default stream are executed in order, they provide a deterministic execution sequence unless specific per-thread or legacy behaviors are enabled [CUDA_C_Programming_Guide:L2219-L2230].

## Compilation Modes

The behavior of the default stream is determined by the `--default-stream` compilation flag or the `CUDA_API_PER_THREAD_DEFAULT_STREAM` macro [CUDA_C_Programming_Guide:L2219-L2230].

### Per-Thread Default Stream

When code is compiled using the `--default-stream per-thread` flag, or when the `CUDA_API_PER_THREAD_DEFAULT_STREAM` macro is defined before including CUDA headers (`cuda.h` and `cuda_runtime.h`), the default stream behaves as a regular stream [CUDA_C_Programming_Guide:L2219-L2230]. In this mode, each host thread maintains its own independent default stream [CUDA_C_Programming_Guide:L2219-L2230].

**Note on Macro Definition:**
Using `#define CUDA_API_PER_THREAD_DEFAULT_STREAM 1` directly in source code is insufficient when compiling with `nvcc`, because `nvcc` implicitly includes `cuda_runtime.h` at the top of the translation unit, potentially overriding the macro definition [CUDA_C_Programming_Guide:L2219-L2230]. To enable per-thread default stream behavior with `nvcc`, one must either:
1. Use the `--default-stream per-thread` compilation flag [CUDA_C_Programming_Guide:L2219-L2230].
2. Define the macro via the compiler command line using `-DCUDA_API_PER_THREAD_DEFAULT_STREAM=1` [CUDA_C_Programming_Guide:L2219-L2230].

### Legacy Default Stream (NULL Stream)

When code is compiled using the `--default-stream legacy` flag, the default stream is a special stream known as the NULL stream [CUDA_C_Programming_Guide:L2219-L2230]. Each device has a single NULL stream that is shared by all host threads [CUDA_C_Programming_Guide:L2219-L2230]. This NULL stream causes implicit synchronization, as described in the Implicit Synchronization documentation [CUDA_C_Programming_Guide:L2219-L2230].

### Default Behavior

If no `--default-stream` compilation flag is specified, the compiler assumes `--default-stream legacy` as the default behavior [CUDA_C_Programming_Guide:L2219-L2230].

## Related Concepts

*   **Implicit Synchronization**: The NULL stream (in legacy mode) causes implicit synchronization between host and device operations [CUDA_C_Programming_Guide:L2219-L2230].
*   **Stream Execution Model**: Understanding the order of execution in the default stream is critical for determining synchronization requirements [CUDA_C_Programming_Guide:L2219-L2230].
