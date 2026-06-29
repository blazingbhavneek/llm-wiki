# 10.21. Warp Reduce Functions

Part of [Cuda C Programming Guide Reference](README.md). Source lines L8631-L9082.

- [Warp Reduce Functions (__reduce_sync)](../../../concepts/warp-reduce-functions.md) — Intrinsics that perform reduction operations (add, min, max, and, or, xor) on data provided by threads in a mask after synchronization.
- [Warp Shuffle Functions (__shfl_sync)](../../../concepts/warp-shuffle-functions.md) — Intrinsics that exchange a variable between threads within a warp without use of shared memory, supported by devices of compute capability 5.0 or higher.
- [Nanosleep Function (__nanosleep)](../../../concepts/nanosleep-function.md) — The __nanosleep function suspends a thread for a specified duration in nanoseconds, with a maximum sleep time of approximately 1 millisecond, and is supported on devices with compute capability 7.0 or higher.
- [Warp Matrix Functions (nvcuda::wmma)](../../../concepts/warp-matrix-functions.md) — C++ warp matrix operations leverage Tensor Cores to accelerate matrix problems of the form D=A*B+C, supported on mixed-precision floating point data for devices of compute capability 7.0 or higher.
