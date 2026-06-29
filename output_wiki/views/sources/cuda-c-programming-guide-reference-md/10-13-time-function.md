# 10.13. Time Function

Part of [Cuda C Programming Guide Reference](README.md). Source lines L7628-L7954.

- [CUDA Time Function (clock/clock64)](../../../concepts/cuda-time-function.md) — The `clock()` and `clock64()` functions return a per-multiprocessor counter incremented every clock cycle, allowing developers to measure the total wall-clock time a thread spends executing on the device, including time-slicing overhead.
- [CUDA Atomic Functions Overview](../../../concepts/cuda-atomic-functions.md) — CUDA atomic functions perform read-modify-write operations on 32-bit, 64-bit, or 128-bit words in global or shared memory, supporting various scopes and memory orders.
- [CUDA Atomic Arithmetic Functions](../../../concepts/cuda-atomic-arithmetic-functions.md) — Section 10.14.1 of the CUDA C Programming Guide introduces arithmetic atomic operations, including atomicAdd, atomicSub, atomicMin, atomicMax, atomicInc, and atomicDec.
- [atomicAdd()](../../../entities/cuda-atomicadd.md) — Performs an atomic addition on a value at a given memory address, returning the old value.
- [atomicSub()](../../../entities/cuda-atomicsub.md) — Performs an atomic subtraction on a 32-bit integer value in global or shared memory, returning the original value.
- [atomicExch()](../../../entities/cuda-atomicexch.md) — Performs an atomic exchange operation on global or shared memory, reading the old value, storing a new value, and returning the old value.
- [atomicMin()](../../../entities/cuda-atomicmin.md) — Performs an atomic minimum operation on global or shared memory, returning the old value.
- [atomicMax()](../../../entities/cuda-atomicmax.md) — Performs an atomic maximum operation on 32-bit or 64-bit integers in global or shared memory, returning the previous value.
- [atomicInc()](../../../entities/cuda-atomicinc.md) — Performs an atomic increment on a 32-bit unsigned integer in global or shared memory, wrapping to zero if the value exceeds a limit.
- [atomicDec()](../../../entities/cuda-atomicdec.md) — Performs an atomic decrement on a 32-bit unsigned integer in global or shared memory, returning the old value.
- [atomicCAS()](../../../entities/cuda-atomiccas.md) — Performs an atomic Compare And Swap operation on 16-bit, 32-bit, 64-bit, or 128-bit values in global or shared memory, returning the old value.
