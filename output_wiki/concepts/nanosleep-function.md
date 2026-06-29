# Nanosleep Function (__nanosleep)

The `__nanosleep` function is used to suspend the execution of a thread for a specified duration. It is part of the CUDA C++ programming interface for device code.

## Syntax

```cpp
void __nanosleep(unsigned ns);
```

## Description

Calling `__nanosleep(ns)` suspends the thread for a sleep duration of approximately `ns` nanoseconds [CUDA_C_Programming_Guide:L8825-L8825]. The maximum sleep duration supported by this function is approximately 1 millisecond [CUDA_C_Programming_Guide:L8825-L8825].

## Requirements

The `__nanosleep` function is supported on devices with compute capability 7.0 or higher [CUDA_C_Programming_Guide:L8827-L8827].

## Example Usage

The function can be used in synchronization primitives, such as implementing a mutex with exponential back-off [CUDA_C_Programming_Guide:L8831-L8831].

## See Also

- CUDA C++ Programming Guide, Section 10.23
