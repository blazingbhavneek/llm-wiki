# Host Functions (Callbacks)

Host functions, also known as stream callbacks, provide a mechanism to insert a CPU function call at any point within a CUDA stream execution order. They are executed on the host once all commands issued to the stream prior to the callback have completed.

## Usage

The runtime API function `cudaLaunchHostFunc()` is used to enqueue a host function into a specific stream. The function signature typically follows the `CUDART_CB` calling convention.

### Example

The following code demonstrates adding a host function `MyCallback` to two streams after issuing a sequence of operations (host-to-device copy, kernel launch, and device-to-host copy). The callback executes on the host after the device-to-host memory copy completes for each stream.

```c
void CUDART_CB MyCallback(void *data){
    printf("Inside callback %d\n", (size_t)data);
}

// ... setup streams and pointers ...

for (size_t i = 0; i < 2; ++i) {
    cudaMemcpyAsync(devPtrIn[i], hostPtr[i], size, cudaMemcpyHostToDevice, stream[i]);
    MyKernel<<<100, 512, 0, stream[i]>>>(devPtrOut[i], devPtrIn[i], size);
    cudaMemcpyAsync(hostPtr[i], devPtrOut[i], size, cudaMemcpyDeviceToHost, stream[i]);
    cudaLaunchHostFunc(stream[i], MyCallback, (void*)i);
}
```

## Execution Order

Host functions enforce ordering constraints within a stream:

1.  **Preceding Commands**: The callback executes only after all commands issued to the stream before the `cudaLaunchHostFunc` call have completed.
2.  **Succeeding Commands**: Commands issued to the stream *after* a host function will not start executing on the device until the host function has completed [CUDA_C_Programming_Guide:L2275-L2298].

## Constraints and Caveats

Host functions enqueued into a stream **must not make CUDA API calls**, either directly or indirectly. Doing so can lead to a deadlock situation where the host function waits for a CUDA operation that cannot proceed because the host is blocked waiting for the host function to complete [CUDA_C_Programming_Guide:L2275-L2298].
