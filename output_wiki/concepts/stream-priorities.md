# Stream Priorities

Stream priorities allow applications to influence the order in which tasks are executed by the GPU scheduler. Priorities are specified at stream creation and serve as hints to the scheduler rather than strict guarantees of execution order [CUDA_C_Programming_Guide:L2299-L2319].

## API Reference

### Retrieving Priority Range

The range of allowable priorities for a device can be queried using `cudaDeviceGetStreamPriorityRange()`. The function returns the least and greatest priority values, ordered as `[ greatest priority, least priority ]` [CUDA_C_Programming_Guide:L2299-L2319].

```cpp
int leastPriority, greatestPriority;
cudaDeviceGetStreamPriorityRange(&leastPriority, &greatestPriority);
```

### Creating Streams with Priority

Streams are created with a specific priority using `cudaStreamCreateWithPriority()`. This function takes the stream pointer, flags, and the priority value [CUDA_C_Programming_Guide:L2299-L2319].

```cpp
cudaStream_t st_high, st_low;
cudaStreamCreateWithPriority(&st_high, cudaStreamNonBlocking, greatestPriority);
cudaStreamCreateWithPriority(&st_low, cudaStreamNonBlocking, leastPriority);
```

## Execution Behavior

The GPU scheduler utilizes stream priorities to determine task execution order among pending tasks [CUDA_C_Programming_Guide:L2299-L2319].

*   **Precedence**: When selecting work to launch, pending tasks in higher-priority streams take precedence over those in lower-priority streams [CUDA_C_Programming_Guide:L2299-L2319].
*   **No Preemption**: Higher-priority tasks do not preempt already running lower-priority tasks [CUDA_C_Programming_Guide:L2299-L2319].
*   **Static Scheduling**: The GPU does not reassess work queues during task execution. Consequently, increasing a stream’s priority will not interrupt ongoing work [CUDA_C_Programming_Guide:L2299-L2319].

Stream priorities influence task execution without enforcing strict ordering, allowing users to leverage priorities to bias scheduling decisions while relying on the scheduler's heuristic nature [CUDA_C_Programming_Guide:L2299-L2319].

## See Also

*   `cudaStreamCreateWithPriority`
*   `cudaDeviceGetStreamPriorityRange`
