# Implicit Synchronization

Implicit synchronization is a mechanism in CUDA that restricts the concurrency of operations across different streams. Specifically, two operations from different streams cannot run concurrently if any CUDA operation on the NULL stream is submitted in between them [CUDA_C_Programming_Guide:L2243-L2246].

## Exceptions

The restriction on concurrency does not apply if the streams involved are non-blocking streams. Non-blocking streams are created using the `cudaStreamNonBlocking` flag [CUDA_C_Programming_Guide:L2246-L2247].

## Best Practices

To improve the potential for concurrent kernel execution, applications should adhere to the following guidelines:

*   **Ordering of Operations**: All independent operations should be issued before dependent operations [CUDA_C_Programming_Guide:L2249-L2250].
*   **Synchronization Timing**: Synchronization of any kind should be delayed as long as possible [CUDA_C_Programming_Guide:L2251-L2252].

## Related Concepts

*   NULL Stream
*   Non-blocking Streams
*   Stream Concurrency
