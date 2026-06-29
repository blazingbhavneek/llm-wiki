# Streams

Applications manage concurrent operations through **streams**. A stream is a sequence of commands (which may be issued by different host threads) that execute in order. Different streams may execute their commands out of order with respect to one another or concurrently; however, this behavior is not guaranteed and should not be relied upon for correctness, as inter-kernel communication between streams is undefined [CUDA_C_Programming_Guide:L2172-L2218].

## Execution Model

Commands issued on a stream execute when all their dependencies are met. Dependencies can include:
* Previously launched commands on the same stream.
* Dependencies from other streams [CUDA_C_Programming_Guide:L2172-L2218].

The successful completion of a synchronize call guarantees that all commands launched on the associated context or stream are completed [CUDA_C_Programming_Guide:L2172-L2218].

## Creation and Destruction

A stream is defined by creating a stream object and specifying it as the stream parameter to a sequence of kernel launches and host-to-device or device-to-host memory copies [CUDA_C_Programming_Guide:L2172-L2218].

### Lifecycle

* **Creation**: Streams are created using `cudaStreamCreate` [CUDA_C_Programming_Guide:L2172-L2218].
* **Destruction**: Streams are released using `cudaStreamDestroy` [CUDA_C_Programming_Guide:L2172-L2218].

If `cudaStreamDestroy` is called while the device is still performing work in the stream, the function returns immediately. The resources associated with the stream are released automatically once the device has completed all work in the stream [CUDA_C_Programming_Guide:L2172-L2218].

### Example Usage

The following example demonstrates creating two streams, allocating page-locked host memory, and issuing asynchronous operations bound to specific streams [CUDA_C_Programming_Guide:L2172-L2218].

```cpp
cudaStream_t stream[2];
for (int i = 0; i < 2; ++i)
    cudaStreamCreate(&stream[i]);

float* hostPtr;
cudaMallocHost(&hostPtr, 2 * size);
```

Each stream performs a sequence of one memory copy from host to device, one kernel launch, and one memory copy from device to host [CUDA_C_Programming_Guide:L2172-L2218]:

```cpp
for (int i = 0; i < 2; ++i) {
    cudaMemcpyAsync(inputDevPtr + i * size, hostPtr + i * size,
                    size, cudaMemcpyHostToDevice, stream[i]);
    MyKernel <<100, 512, 0, stream[i]>>
        (outputDevPtr + i * size, inputDevPtr + i * size, size);
    cudaMemcpyAsync(hostPtr + i * size, outputDevPtr + i * size,
                    size, cudaMemcpyDeviceToHost, stream[i]);
}
```

Each stream copies its portion of the input array `hostPtr` to `inputDevPtr` in device memory, processes it by calling `MyKernel()`, and copies the result `outputDevPtr` back to the same portion of `hostPtr` [CUDA_C_Programming_Guide:L2172-L2218].

**Note**: `hostPtr` must point to page-locked host memory for any overlap to occur [CUDA_C_Programming_Guide:L2172-L2218].

Streams are released by calling `cudaStreamDestroy` [CUDA_C_Programming_Guide:L2172-L2218]:

```cpp
for (int i = 0; i < 2; ++i)
    cudaStreamDestroy(stream[i]);
```

## Caveats

* The concurrent execution of different streams is not guaranteed. Relying on specific ordering between different streams for correctness (e.g., inter-kernel communication) is undefined behavior [CUDA_C_Programming_Guide:L2172-L2218].
* Page-locked host memory is required for overlapping memory transfers and kernel execution [CUDA_C_Programming_Guide:L2172-L2218].

## References

* [CUDA_C_Programming_Guide:L2172-L2218] CUDA C Programming Guide, Section 6.2.8.5 Streams
