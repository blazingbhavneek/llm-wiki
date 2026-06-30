# CUDA Events

Events provide a mechanism to monitor device progress and perform accurate timing by asynchronously recording events at any program point. Events complete when all preceding tasks or commands in a stream finish. The section covers event creation, destruction, and measuring elapsed time between events.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L3403-L3448

Citation: [CUDA_C_Programming_Guide:L3403-L3448]

````text
## 6.2.8.8 Events

The runtime also provides a way to closely monitor the device’s progress, as well as perform accurate timing, by letting the application asynchronously record events at any point in the program, and query when these events are completed. An event has completed when all tasks - or optionally, all commands in a given stream - preceding the event have completed. Events in stream zero are completed after all preceding tasks and commands in all streams are completed.

## 6.2.8.8.1 Creation and Destruction of Events

The following code sample creates two events:

```txt
cudaEvent_t start, stop;
cudaEventCreate(&start);
cudaEventCreate(&stop);
```

They are destroyed this way:

```javascript
cudaEventDestroy(start);
cudaEventDestroy(stop);
```

## 6.2.8.8.2 Elapsed Time

The events created in Creation and Destruction of Events can be used to time the code sample of Creation and Destruction of Streams the following way:

```txt
cudaEventRecord(start, 0);
for (int i = 0; i < 2; ++i) {
    cudaMemcpyAsync(inputDev + i * size, inputHost + i * size,
                    size, cudaMemcpyHostToDevice, stream[i]);
    MyKernel<<<100, 512, 0, stream[i]>>>
        (outputDev + i * size, inputDev + i * size, size);
```

(continues on next page)

```txt
cudaMemcpyAsync(outputHost + i * size, outputDev + i * size,
                    size, cudaMemcpyDeviceToHost, stream[i]);
}
cudaEventRecord(stop, 0);
cudaEventSynchronize(stop);
float elapsedTime;
cudaEventElapsedTime(&elapsedTime, start, stop);
```
````
