# CUDA Configuration Options

Resource allocation for the device runtime system software is controlled via the `cudaDeviceSetLimit()` API from the host program [CUDA_C_Programming_Guide:L14236-L14243]. Limits must be set before any kernel is launched, and may not be changed while the GPU is actively running programs [CUDA_C_Programming_Guide:L14236-L14243].

The following named limits may be set:

## cudaLimitDevRuntimePendingLaunchCount

This limit controls the amount of memory set aside for buffering kernel launches and events which have not yet begun to execute, due either to unresolved dependencies or lack of execution resources [CUDA_C_Programming_Guide:L14236-L14243].

- **Behavior when full**: When the buffer is full, an attempt to allocate a launch slot during a device side kernel launch will fail and return `cudaErrorLaunchOutOfBoundsException`, while an attempt to allocate an event slot will fail and return `cudaMemoryAllocation` [CUDA_C_Programming_Guide:L14236-L14243].
- **Default value**: The default number of launch slots is 2048 [CUDA_C_Programming_Guide:L14236-L14243].
- **Configuration**: Applications may increase the number of launch and/or event slots by setting `cudaLimitDevRuntimePendingLaunchCount` [CUDA_C_Programming_Guide:L14236-L14243]. The number of event slots allocated is twice the value of that limit [CUDA_C_Programming_Guide:L14236-L14243].

## cudaLimitStackSize

This limit controls the stack size in bytes of each GPU thread [CUDA_C_Programming_Guide:L14236-L14243].

- **Automatic adjustment**: The CUDA driver automatically increases the per-thread stack size for each kernel launch as needed [CUDA_C_Programming_Guide:L14236-L14243].
- **Persistence**: This size isn't reset back to the original value after each launch [CUDA_C_Programming_Guide:L14236-L14243].
- **Configuration**: To set the per-thread stack size to a different value, `cudaDeviceSetLimit()` can be called to set this limit [CUDA_C_Programming_Guide:L14236-L14243].
- **Immediate effect**: The stack will be immediately resized, and if necessary, the device will block until all preceding requested tasks are complete [CUDA_C_Programming_Guide:L14236-L14243].
- **Retrieval**: `cudaDeviceGetLimit()` can be called to get the current per-thread stack size [CUDA_C_Programming_Guide:L14236-L14243].
