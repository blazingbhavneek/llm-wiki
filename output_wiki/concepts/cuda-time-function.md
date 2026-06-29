# CUDA Time Function (clock/clock64)

The `clock()` and `clock64()` functions provide a mechanism for measuring execution time at the thread level within CUDA device code. These functions return the value of a per-multiprocessor counter that is incremented every clock cycle [CUDA_C_Programming_Guide:L7628-L7636].

## Function Signatures

The available functions are defined as follows [CUDA_C_Programming_Guide:L7628-L7636]:

```cpp
clock_t clock();
long long int clock64();
```

## Usage and Measurement

To measure the execution time of a kernel or a specific section of code, the counter should be sampled at the beginning and at the end of the execution scope. The difference between these two samples, recorded per thread, provides a measure of the number of clock cycles taken by the device to completely execute the thread [CUDA_C_Programming_Guide:L7628-L7636].

## Characteristics and Limitations

It is important to distinguish between the measured value and the actual instruction execution time. The value returned by `clock()` or `clock64()` represents the total time the thread was scheduled on the multiprocessor, which includes time-slicing overhead [CUDA_C_Programming_Guide:L7628-L7636]. Consequently, this number is greater than the number of clock cycles the device actually spent executing thread instructions [CUDA_C_Programming_Guide:L7628-L7636].

## Related Concepts

- **Time Slicing**: The phenomenon where threads are preempted and scheduled on the hardware, contributing to the difference between total execution time and active instruction execution time.
- **Per-Multiprocessor Counter**: The underlying hardware mechanism that tracks the clock cycles, ensuring that the counter is local to the multiprocessor executing the thread.
