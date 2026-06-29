# Explicit Synchronization and Logical GPU Activity

In the CUDA programming model, explicit synchronization is required even if a kernel runs quickly and finishes before the CPU accesses the data (e.g., touching a variable like `y`). This requirement exists because Unified Memory uses **logical activity** to determine whether the GPU is idle [CUDA_C_Programming_Guide:L21897-L21906].

## Logical Activity and Kernel Completion

The concept of logical activity aligns with the CUDA programming model specification, which states that a kernel can run at any time following a launch. Consequently, a kernel is not guaranteed to have finished executing until the host issues a synchronization call [CUDA_C_Programming_Guide:L21897-L21906].

## Functions Guaranteeing GPU Completion

Any function call that logically guarantees the GPU completes its work is valid for synchronization purposes [CUDA_C_Programming_Guide:L21897-L21906]. These include:

*   `cudaDeviceSynchronize()`
*   `cudaStreamSynchronize()`
*   `cudaStreamQuery()`: Valid provided it returns `cudaSuccess` and not `cudaErrorNotReady`, and the specified stream is the only stream still executing on the GPU.
*   `cudaEventSynchronize()` and `cudaEventQuery()`: Valid in cases where the specified event is not followed by any device work.
*   `cudaMemcpy()` and `cudaMemset()`: Valid when documented as being fully synchronous with respect to the host [CUDA_C_Programming_Guide:L21897-L21906].

## Stream Dependencies

Dependencies created between streams allow the system to infer the completion of other streams by synchronizing on a stream or event. These dependencies can be created explicitly via `cudaStreamWaitEvent()` or implicitly when using the default (`NULL`) stream [CUDA_C_Programming_Guide:L21897-L21906].

## CPU Access and Callbacks

It is legal for the CPU to access managed data from within a stream callback, provided that no other stream that could potentially be accessing managed data is active on the GPU [CUDA_C_Programming_Guide:L21897-L21906].

Additionally, a callback that is not followed by any device work can be used for synchronization, such as by signaling a condition variable from inside the callback. In other cases, CPU access to managed data is valid only for the duration of the callback(s) [CUDA_C_Programming_Guide:L21897-L21906].
