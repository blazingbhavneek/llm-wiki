# CUDA Compute Modes

On Tesla solutions running Windows Server 2008 and later or Linux, any device in a system can be configured into one of three compute modes using NVIDIA’s System Management Interface (`nvidia-smi`), a tool distributed as part of the driver [CUDA_C_Programming_Guide:L6093-L6109].

## Default Compute Mode

In **Default compute mode**, multiple host threads can use the device simultaneously [CUDA_C_Programming_Guide:L6093-L6109]. Access is granted by:
*   Calling `cudaSetDevice()` on the device when using the CUDA Runtime API.
*   Making a context associated with the device current when using the CUDA Driver API [CUDA_C_Programming_Guide:L6093-L6109].

## Exclusive-Process Compute Mode

In **Exclusive-process compute mode**, only one CUDA context may be created on the device across all processes in the system [CUDA_C_Programming_Guide:L6093-L6109]. Within the process that created that context, the context may be current to as many threads as desired [CUDA_C_Programming_Guide:L6093-L6109].

## Prohibited Compute Mode

In **Prohibited compute mode**, no CUDA context can be created on the device [CUDA_C_Programming_Guide:L6093-L6109].

## Implications for Host Threads

The selected compute mode affects host thread behavior, particularly when using the CUDA Runtime API without explicitly calling `cudaSetDevice()` [CUDA_C_Programming_Guide:L6093-L6109]. In such cases, a host thread might be associated with a device other than device 0 if device 0 is in prohibited mode or in exclusive-process mode and currently used by another process [CUDA_C_Programming_Guide:L6093-L6109]. To manage device selection in these scenarios, `cudaSetValidDevices()` can be used to define a prioritized list of devices [CUDA_C_Programming_Guide:L6093-L6109].

## Compute Preemption

For devices featuring the Pascal architecture onwards (compute capability with major revision number 6 and higher), support exists for **Compute Preemption** [CUDA_C_Programming_Guide:L6093-L6109]. This feature allows compute tasks to be preempted at instruction-level granularity, rather than thread block granularity as in prior Maxwell and Kepler GPU architectures [CUDA_C_Programming_Guide:L6093-L6109].

### Benefits and Overheads

Compute Preemption prevents applications with long-running kernels from monopolizing the system or timing out [CUDA_C_Programming_Guide:L6093-L6109]. However, this capability introduces context switch overheads [CUDA_C_Programming_Guide:L6093-L6109]. Compute Preemption is automatically enabled on devices that support it [CUDA_C_Programming_Guide:L6093-L6109].

Users wishing to avoid the context switch overheads associated with different processes can ensure that only one process is active on the GPU by selecting exclusive-process mode [CUDA_C_Programming_Guide:L6093-L6109].

### Querying Support

The individual attribute query function `cudaDeviceGetAttribute()` with the attribute `cudaDevAttrComputePreemptionSupported` can be used to determine if the device in use supports Compute Preemption [CUDA_C_Programming_Guide:L6093-L6109].

## Querying Compute Mode

Applications may query the current compute mode of a device by checking the attribute `cudaDevAttrComputeMode` [CUDA_C_Programming_Guide:L6093-L6109].
