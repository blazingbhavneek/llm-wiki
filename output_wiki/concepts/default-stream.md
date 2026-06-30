# Default Stream

Kernel launches and memory copies without a stream parameter use the default stream, executing in order. Compilation flags like --default-stream per-thread or legacy alter whether the default stream is per-thread or a shared NULL stream.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L2219-L2230

Citation: [CUDA_C_Programming_Guide:L2219-L2230]

````text
## 6.2.8.5.2 Default Stream

Kernel launches and host <-> device memory copies that do not specify any stream parameter, or equivalently that set the stream parameter to zero, are issued to the default stream. They are therefore executed in order.

For code that is compiled using the --default-stream per-thread compilation flag (or that defines the CUDA\_API\_PER\_THREAD\_DEFAULT\_STREAM macro before including CUDA headers (cuda.h and cuda\_runtime.h)), the default stream is a regular stream and each host thread has its own default stream.

Note: #define CUDA\_API\_PER\_THREAD\_DEFAULT\_STREAM 1 cannot be used to enable this behavior when the code is compiled by nvcc as nvcc implicitly includes cuda\_runtime.h at the top of the translation unit. In this case the --default-stream per-thread compilation flag needs to be used or the CUDA\_API\_PER\_THREAD\_DEFAULT\_STREAM macro needs to be defined with the -DCUDA\_API\_PER\_THREAD\_DEFAULT\_STREAM=1 compiler flag.

For code that is compiled using the --default-stream legacy compilation flag, the default stream is a special stream called the NULL stream and each device has a single NULL stream used for all host threads. The NULL stream is special as it causes implicit synchronization as described in Implicit Synchronization.

For code that is compiled without specifying a --default-stream compilation flag, --default-stream legacy is assumed as the default.
````
