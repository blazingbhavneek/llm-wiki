# CUDA Asynchronous Programming

In the CUDA programming model, a thread is the lowest level of abstraction for performing computation or memory operations. Starting with devices based on the NVIDIA Ampere GPU Architecture, the CUDA programming model provides acceleration to memory operations via the asynchronous programming model [CUDA_C_Programming_Guide:L1057-L1059].

## Core Concepts

### Asynchronous Operations
An asynchronous operation is defined as an operation that is initiated by a CUDA thread and is executed asynchronously as-if by another thread [CUDA_C_Programming_Guide:L1063-L1065]. This "as-if thread" is always associated with the CUDA thread that initiated the asynchronous operation [CUDA_C_Programming_Guide:L1063-L1065].

In a well-formed program, one or more CUDA threads synchronize with the asynchronous operation [CUDA_C_Programming_Guide:L1063-L1065]. The CUDA thread that initiated the asynchronous operation is not required to be among the threads that synchronize [CUDA_C_Programming_Guide:L1063-L1065].

### Synchronization
The asynchronous programming model defines the behavior of Asynchronous Barriers for synchronization between CUDA threads [CUDA_C_Programming_Guide:L1057-L1059]. An asynchronous operation uses a synchronization object to synchronize the completion of the operation [CUDA_C_Programming_Guide:L1063-L1065]. These synchronization objects can be:
*   Explicitly managed by a user (e.g., `cuda::memcpy_async`) [CUDA_C_Programming_Guide:L1063-L1065].
*   Implicitly managed within a library (e.g., `cooperative_groups::memcpy_async`) [CUDA_C_Programming_Guide:L1063-L1065].

## Thread Scopes

Synchronization behavior is defined relative to specific thread scopes [CUDA_C_Programming_Guide:L1070-L1073]. The following table outlines the available scopes for asynchronous operations:

| Thread Scope | Description |
| :--- | :--- |
| `cuda::thread_scope::thread_scope_thread` | Only the CUDA thread which initiated asynchronous operations synchronizes. |
| `cuda::thread_scope::thread_scope_block` | All or any CUDA threads within the same thread block as the initiating thread synchronizes. |
| `cuda::thread_scope::thread_scope_device` | All or any CUDA threads in the same GPU device as the initiating thread synchronizes. |
| `cuda::thread_scope::thread_scope_system` | All or any CUDA or CPU threads in the same system as the initiating thread synchronizes. |

## Usage

The model explains and defines how `cuda::memcpy_async` can be used to move data asynchronously from global memory while computing in the GPU [CUDA_C_Programming_Guide:L1057-L1059].

## References

*   CUDA C++ Programming Guide: Asynchronous Programming Model [CUDA_C_Programming_Guide:L1057-L1059] [CUDA_C_Programming_Guide:L1063-L1065] [CUDA_C_Programming_Guide:L1070-L1073]
