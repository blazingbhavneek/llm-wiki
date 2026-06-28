## 5.3. Memory Hierarchy

CUDA threads may access data from multiple memory spaces during their execution as illustrated by Figure 6. Each thread has private local memory. Each thread block has shared memory visible to all threads of the block and with the same lifetime as the block. Thread blocks in a thread block cluster can perform read, write, and atomics operations on each other’s shared memory. All threads have access to the same global memory.

There are also two additional read-only memory spaces accessible by all threads: the constant and texture memory spaces. The global, constant, and texture memory spaces are optimized for diferent memory usages (see Device Memory Accesses). Texture memory also ofers diferent addressing modes, as well as data filtering, for some specific data formats (see Texture and Surface Memory).

The global, constant, and texture memory spaces are persistent across kernel launches by the same application.

![](images/f56179ef6c3f5276d5d206c35260449c97976c5bff3489427fea800dbd89fd64.jpg)  
Figure 6: Memory Hierarchy

## 5.4. Heterogeneous Programming

As illustrated by Figure 7, the CUDA programming model assumes that the CUDA threads execute on a physically separate device that operates as a coprocessor to the host running the C++ program. This is the case, for example, when the kernels execute on a GPU and the rest of the C++ program executes on a CPU.

The CUDA programming model also assumes that both the host and the device maintain their own separate memory spaces in DRAM, referred to as host memory and device memory, respectively. Therefore, a program manages the global, constant, and texture memory spaces visible to kernels through calls to the CUDA runtime (described in Programming Interface). This includes device memory allocation and deallocation as well as data transfer between host and device memory.

Unified Memory provides managed memory to bridge the host and device memory spaces. Managed memory is accessible from all CPUs and GPUs in the system as a single, coherent memory image with a common address space. This capability enables oversubscription of device memory and can greatly simplify the task of porting applications by eliminating the need to explicitly mirror data on host and device. See Unified Memory Programming for an introduction to Unified Memory.

## 5.5. Asynchronous SIMT Programming Model

In the CUDA programming model a thread is the lowest level of abstraction for doing a computation or a memory operation. Starting with devices based on the NVIDIA Ampere GPU Architecture, the CUDA programming model provides acceleration to memory operations via the asynchronous programming model. The asynchronous programming model defines the behavior of asynchronous operations with respect to CUDA threads.

The asynchronous programming model defines the behavior of Asynchronous Barrier for synchronization between CUDA threads. The model also explains and defines how cuda::memcpy\_async can be used to move data asynchronously from global memory while computing in the GPU.

## 5.5.1. Asynchronous Operations

An asynchronous operation is defined as an operation that is initiated by a CUDA thread and is executed asynchronously as-if by another thread. In a well formed program one or more CUDA threads synchronize with the asynchronous operation. The CUDA thread that initiated the asynchronous operation is not required to be among the synchronizing threads.

Such an asynchronous thread (an as-if thread) is always associated with the CUDA thread that initiated the asynchronous operation. An asynchronous operation uses a synchronization object to synchronize the completion of the operation. Such a synchronization object can be explicitly managed by a user (e.g., cuda::memcpy\_async) or implicitly managed within a library (e.g., cooperative\_groups::memcpy\_async).

A synchronization object could be a cuda::barrier or a cuda::pipeline. These objects are explained in detail in Asynchronous Barrier and Asynchronous Data Copies using cuda::pipeline. These synchronization objects can be used at diferent thread scopes. A scope defines the set of threads that may use the synchronization object to synchronize with the asynchronous operation. The following table defines the thread scopes available in CUDA C++ and the threads that can be synchronized with each.

![](images/5755007a4a94054c2f6b20f13648d7ccb76195690a54441356b8050757788bb4.jpg)  
Figure 7: Heterogeneous Programming  
Note: Serial code executes on the host while parallel code executes on the device.

<table><tr><td>Thread Scope</td><td>Description</td></tr><tr><td>cuda::thread_scope::thread_scope_thread</td><td>Only the CUDA thread which initiated asynchronous operations synchronizes.</td></tr><tr><td>cuda::thread_scope::thread_scope_block</td><td>All or any CUDA threads within the same thread block as the initiating thread synchronizes.</td></tr><tr><td>cuda::thread_scope::thread_scope_device</td><td>All or any CUDA threads in the same GPU device as the initiating thread synchronizes.</td></tr><tr><td>cuda::thread_scope::thread_scope_system</td><td>All or any CUDA or CPU threads in the same system as the initiating thread synchronizes.</td></tr></table>

These thread scopes are implemented as extensions to standard C++ in the CUDA Standard C++ library.
