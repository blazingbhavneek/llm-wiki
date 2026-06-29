# CUDA Device Streams

CUDA device streams provide a mechanism for managing and executing kernels on the GPU device runtime. Both named and unnamed (NULL) streams are available for use within the device runtime environment [CUDA_C_Programming_Guide:L13858-L13867].

## Stream Scope and Usage

Named streams can be utilized by any thread within a grid. However, stream handles are not portable across kernel boundaries; they cannot be passed to other child or parent kernels. Consequently, a stream should be treated as private to the grid in which it is created [CUDA_C_Programming_Guide:L13858-L13867].

## Concurrency

Similar to host-side launches, work launched into separate device streams may run concurrently. However, actual concurrency is not guaranteed by the hardware or runtime. Programs that depend upon specific concurrency behaviors between child kernels are not supported by the CUDA programming model and will result in undefined behavior [CUDA_C_Programming_Guide:L13858-L13867].

## Stream Creation and Flags

To maintain semantic compatibility with the host runtime, all device streams must be created using the `cudaStreamCreateWithFlags()` API with the `cudaStreamNonBlocking` flag [CUDA_C_Programming_Guide:L13858-L13867].

The host-side NULL stream's cross-stream barrier semantics are not supported on the device. Additionally, the `cudaStreamCreate()` API is restricted to the host runtime and will fail to compile if used in device code [CUDA_C_Programming_Guide:L13858-L13867].

## Synchronization

The device runtime does not support the host-side synchronization APIs `cudaStreamSynchronize()` and `cudaStreamQuery()`. To determine when stream-launched child kernels have completed, applications should launch a kernel into the `cudaStreamTailLaunch` stream [CUDA_C_Programming_Guide:L13858-L13867]. This "tail launch" approach serves as the device-side equivalent for waiting on stream completion.
