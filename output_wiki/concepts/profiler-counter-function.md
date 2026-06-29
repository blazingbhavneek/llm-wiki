# Profiler Counter Function

The `__prof_trigger()` function provides a mechanism for applications to increment per-multiprocessor hardware counters using a single instruction. Each multiprocessor contains a set of sixteen hardware counters that can be accessed through this function.

## Function Signature

```c
void __prof_trigger(int counter);
```

This function increments the per-multiprocessor hardware counter of the specified index by one per warp [CUDA_C_Programming_Guide:L11089-L11101].

## Counter Allocation

The sixteen available counters are divided into application-useable and reserved ranges:

*   **Counters 0–7**: Available for application use. These counters can be incremented by calling `__prof_trigger()` with an integer argument between 0 and 7 [CUDA_C_Programming_Guide:L11089-L11101].
*   **Counters 8–15**: Reserved by the system and should not be used by applications [CUDA_C_Programming_Guide:L11089-L11101].

## Retrieving Counter Values

The values of the application counters (0–7) can be retrieved using the `nvprof` tool. The specific event names follow the pattern `prof_trigger_0x`, where `x` is the counter index (0–7) [CUDA_C_Programming_Guide:L11089-L11101].

Example usage:
```bash
nvprof --events prof_trigger_00
nvprof --events prof_trigger_01
...
nvprof --events prof_trigger_07
```

## Reset Behavior

All counters are automatically reset before each kernel launch. Users should note that when collecting counters, kernel launches behave synchronously, as described in the context of concurrent execution between host and device [CUDA_C_Programming_Guide:L11089-L11101].

## See Also

*   [CUDA Profiler Counters](concept/profiler-counter-function)
*   [__prof_trigger](concept/profiler-counter-function)
