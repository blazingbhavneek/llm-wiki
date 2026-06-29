# CUDA Events

CUDA events allow applications to closely monitor the device's progress and perform accurate timing. They function by letting the application asynchronously record events at any point in the program and query when these events are completed [CUDA_C_Programming_Guide:L3403-L3407].

## Completion Semantics

An event is considered completed when all tasks—or optionally, all commands in a given stream—preceding the event have completed [CUDA_C_Programming_Guide:L3403-L3407].

*   **Stream Zero**: Events recorded in stream zero complete only after all preceding tasks and commands in **all** streams have completed [CUDA_C_Programming_Guide:L3403-L3407].

## Creation and Destruction

Events are managed using the `cudaEvent_t` type. They must be created before use and destroyed when no longer needed.

### Creating Events

Two events, `start` and `stop`, can be created as follows:

```txt
cudaEvent_t start, stop;
cudaEventCreate(&start);
cudaEventCreate(&stop);
```
[CUDA_C_Programming_Guide:L3408-L3423]

### Destroying Events

Events are destroyed using `cudaEventDestroy`:

```javascript
cudaEventDestroy(start);
cudaEventDestroy(stop);
```
[CUDA_C_Programming_Guide:L3408-L3423]

## Elapsed Time Measurement

Events can be used to measure the time elapsed between specific points in execution. This typically involves recording an event before and after a sequence of operations, synchronizing the end event, and then calculating the difference.

### Example Workflow

1.  **Record Start**: Record the start event in stream 0.
2.  **Execute Work**: Perform asynchronous operations (e.g., memory copies and kernel launches) in specific streams.
3.  **Record Stop**: Record the stop event in stream 0.
4.  **Synchronize**: Synchronize the stop event to ensure it has completed.
5.  **Calculate**: Use `cudaEventElapsedTime` to get the duration in milliseconds.

```txt
cudaEventRecord(start, 0);
for (int i = 0; i < 2; ++i) {
    cudaMemcpyAsync(inputDev + i * size, inputHost + i * size,
                    size, cudaMemcpyHostToDevice, stream[i]);
    MyKernel<<<100, 512, 0, stream[i]>>>
        (outputDev + i * size, inputDev + i * size, size);
    cudaMemcpyAsync(outputHost + i * size, outputDev + i * size,
                    size, cudaMemcpyDeviceToHost, stream[i]);
}
cudaEventRecord(stop, 0);
cudaEventSynchronize(stop);
float elapsedTime;
cudaEventElapsedTime(&elapsedTime, start, stop);
```
[CUDA_C_Programming_Guide:L3424-L3448]
