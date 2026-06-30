# Memcpy()/Memset() Behavior With Stream-associated Unified Memory

Details the rules for cudaMemcpy*() and cudaMemset*() operations on stream-associated unified memory, including coherency checks, stream activity constraints, and error conditions.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L22057-L22075

Citation: [CUDA_C_Programming_Guide:L22057-L22075]

````text
## 24.3.2.4.7 Memcpy()/Memset() Behavior With Stream-associated Unified Memory

See Memcpy()/Memset() Behavior With Unified Memory for a general overview of cudaMemcpy\* / cudaMemset\* behavior on devices with concurrentManagedAccess set. On devices where concurrentManagedAccess is not set, the following rules apply:

If cudaMemcpyHostTo\* is specified and the source data is unified memory, then it will be accessed from the host if it is coherently accessible from the host in the copy stream (1); otherwise it will be accessed from the device. Similar rules apply to the destination when cudaMemcpy\*ToHost is specified and the destination is unified memory.

If cudaMemcpyDeviceTo\* is specified and the source data is unified memory, then it will be accessed from the device. The source must be coherently accessible from the device in the copy stream (2); otherwise, an error is returned. Similar rules apply to the destination when cudaMemcpy\*ToDevice is specified and the destination is unified memory.

If cudaMemcpyDefault is specified, then unified memory will be accessed from the host either if it cannot be coherently accessed from the device in the copy stream (2) or if the preferred location for the data is cudaCpuDeviceId and it can be coherently accessed from the host in the copy stream (1); otherwise, it will be accessed from the device.

When using cudaMemset\*() with unified memory, the data must be coherently accessible from the device in the stream being used for the cudaMemset() operation (2); otherwise, an error is returned.

When data is accessed from the device either by cudaMemcpy\* or cudaMemset\*, the stream of operation is considered to be active on the GPU. During this time, any CPU access of data that is associated with that stream or data that has global visibility, will result in a segmentation fault if the GPU has a zero value for the device attribute concurrentManagedAccess. The program must synchronize appropriately to ensure the operation has completed before accessing any associated data from the CPU.

1. Coherently accessible from the host in a given stream means that the memory neither has global visibility nor is it associated with the given stream.

2. Coherently accessible from the device in a given stream means that the memory either has global visibility or is associated with the given stream.

# Chapter 25. Lazy Loading
````
