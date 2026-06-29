# Undefined Behavior in Cross-Execution Space Calls

A 'cross-execution space' call results in undefined behavior depending on the state of the `__CUDA_ARCH__` macro at the time of compilation.

## Scenarios

Undefined behavior occurs in the following specific contexts:

*   **When `__CUDA_ARCH__` is defined:** A call from within a `__global__`, `__device__`, or `__host__ __device__` function to a `__host__` function is undefined behavior [CUDA_C_Programming_Guide:L6602-L6609].
*   **When `__CUDA_ARCH__` is undefined:** A call from within a `__host__` function to a `__device__` function is undefined behavior [CUDA_C_Programming_Guide:L6602-L6609].

## References

[4] CUDA C Programming Guide, Section 10.1.4. Undefined behavior.
