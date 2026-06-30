# Profiler Counter Function

Each multiprocessor has sixteen hardware counters that applications can increment via the __prof_trigger() function. Counters 0-7 are available for applications, while 8-15 are reserved. Values can be retrieved using nvprof --events prof_trigger_0x. Counters reset before each kernel launch.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L11089-L11099

Citation: [CUDA_C_Programming_Guide:L11089-L11099]

````text
## 10.31. Profiler Counter Function

Each multiprocessor has a set of sixteen hardware counters that an application can increment with a single instruction by calling the \_\_prof\_trigger() function.

```javascript
void __prof_trigger(int counter);
```

increments by one per warp the per-multiprocessor hardware counter of index counter. Counters 8 to 15 are reserved and should not be used by applications.

The value of counters 0, 1, …, 7 can be obtained via nvprof by nvprof --events prof\_trigger\_0x where x is 0, 1, …, 7. All counters are reset before each kernel launch (note that when collecting counters, kernel launches are synchronous as mentioned in Concurrent Execution between Host and Device).
````
