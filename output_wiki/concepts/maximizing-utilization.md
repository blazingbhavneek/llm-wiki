# Maximizing Utilization

To maximize utilization, an application must be structured to expose as much parallelism as possible and efficiently map this parallelism to the various components of the system to keep them busy most of the time [CUDA_C_Programming_Guide:L6195-L6239]. This involves optimizing at three distinct levels: the application level, the device level, and the multiprocessor level [CUDA_C_Programming_Guide:L6195-L6239].

## Application Level

At the high level, the application should maximize parallel execution between the host, the devices, and the bus connecting them [CUDA_C_Programming_Guide:L6195-L6239]. This is achieved by using asynchronous function calls and streams [CUDA_C_Programming_Guide:L6195-L6239]. Workloads should be assigned to the processor best suited for them: serial workloads to the host and parallel workloads to the devices [CUDA_C_Programming_Guide:L6195-L6239].

When parallelism is broken because threads need to synchronize to share data, the strategy depends on the thread grouping [CUDA_C_Programming_Guide:L6195-L6239]:
*   **Same Block:** Threads within the same block should use `__syncthreads()` and share data through shared memory within a single kernel invocation [CUDA_C_Programming_Guide:L6195-L6239].
*   **Different Blocks:** Threads belonging to different blocks must share data through global memory using two separate kernel invocations (one for writing, one for reading) [CUDA_C_Programming_Guide:L6195-L6239].

The second case is significantly less optimal due to the overhead of extra kernel invocations and global memory traffic [CUDA_C_Programming_Guide:L6195-L6239]. To minimize this, algorithms should be mapped to the CUDA programming model such that computations requiring inter-thread communication are performed within a single thread block as much as possible [CUDA_C_Programming_Guide:L6195-L6239].

## Device Level

At the device level, the goal is to maximize parallel execution between the multiprocessors of a single device [CUDA_C_Programming_Guide:L6195-L6239]. This is achieved by enabling enough kernels to execute concurrently using streams [CUDA_C_Programming_Guide:L6195-L6239].

## Multiprocessor Level

At the multiprocessor level, utilization is maximized by maximizing parallel execution between the various functional units within a multiprocessor [CUDA_C_Programming_Guide:L6195-L6239].

### Latency Hiding and Warp Residency

GPU multiprocessors primarily rely on thread-level parallelism to maximize the utilization of their functional units [CUDA_C_Programming_Guide:L6195-L6239]. Utilization is directly linked to the number of resident warps [CUDA_C_Programming_Guide:L6195-L6239]. At every instruction issue time, a warp scheduler selects an instruction that is ready to execute [CUDA_C_Programming_Guide:L6195-L6239]. This can be an independent instruction from the same warp (exploiting instruction-level parallelism) or, more commonly, an instruction from another warp (exploiting thread-level parallelism) [CUDA_C_Programming_Guide:L6195-L6239].

Full utilization is achieved when all warp schedulers always have an instruction to issue for some warp at every clock cycle during the latency period, effectively "hiding" the latency [CUDA_C_Programming_Guide:L6195-L6239]. The number of instructions required to hide a latency of $L$ clock cycles depends on the throughputs of the instructions [CUDA_C_Programming_Guide:L6195-L6239]. Assuming maximum throughput instructions, the requirements are:
*   **4L** for devices of compute capability 5.x, 6.1, 6.2, 7.x, and 8.x, as these devices issue one instruction per warp over one clock cycle for four warps at a time [CUDA_C_Programming_Guide:L6195-L6239].
*   **2L** for devices of compute capability 6.0, as these devices issue two instructions every cycle for two different warps [CUDA_C_Programming_Guide:L6195-L6239].

### Sources of Latency

The most common reason a warp is not ready to execute its next instruction is that its input operands are not available [CUDA_C_Programming_Guide:L6195-L6239].

1.  **Register Dependencies:** If all input operands are registers, latency is caused by dependencies on previous instructions that have not yet completed [CUDA_C_Programming_Guide:L6195-L6239]. For example, on compute capability 7.x devices, arithmetic instructions typically take 4 clock cycles [CUDA_C_Programming_Guide:L6195-L6239]. Hiding this latency requires 16 active warps per multiprocessor (4 cycles × 4 warp schedulers), assuming maximum throughput [CUDA_C_Programming_Guide:L6195-L6239]. If warps exhibit instruction-level parallelism, fewer warps are needed [CUDA_C_Programming_Guide:L6195-L6239].
2.  **Off-Chip Memory:** If an input operand resides in off-chip memory, latency is much higher, typically hundreds of clock cycles [CUDA_C_Programming_Guide:L6195-L6239]. The number of warps required to keep schedulers busy depends on the kernel's arithmetic intensity, defined as the ratio of instructions with no off-chip memory operands (mostly arithmetic) to instructions with off-chip memory operands [CUDA_C_Programming_Guide:L6195-L6239]. Lower arithmetic intensity requires more warps to hide the latency [CUDA_C_Programming_Guide:L6195-L6239].
3.  **Synchronization Points:** Warps may also wait at memory fences or synchronization points [CUDA_C_Programming_Guide:L6195-L6239]. Synchronization points can force the multiprocessor to idle as warps wait for others in the same block to complete [CUDA_C_Programming_Guide:L6195-L6239]. Having multiple resident blocks per multiprocessor helps reduce idling, as warps from different blocks do not need to wait for each other [CUDA_C_Programming_Guide:L6195-L6239].

### Resource Optimization

The number of blocks and warps residing on each multiprocessor depends on the execution configuration, memory resources, and the kernel's resource requirements [CUDA_C_Programming_Guide:L6195-L6239]. Register and shared memory usage can be reported by the compiler using the `--ptxas-options=-v` option [CUDA_C_Programming_Guide:L6195-L6239].

#### Shared Memory

The total shared memory required for a block is the sum of statically and dynamically allocated shared memory [CUDA_C_Programming_Guide:L6195-L6239].

#### Register Usage and Spilling

Register usage significantly impacts the number of resident warps [CUDA_C_Programming_Guide:L6195-L6239]. For example, on compute capability 6.x devices, a kernel using 64 registers with 512 threads per block and minimal shared memory can have two blocks (32 warps) resident [CUDA_C_Programming_Guide:L6195-L6239]. If the kernel uses one more register (65), only one block (16 warps) can be resident because the register file capacity is exceeded [CUDA_C_Programming_Guide:L6195-L6239].

The compiler attempts to minimize register usage while keeping register spilling and instruction count to a minimum [CUDA_C_Programming_Guide:L6195-L6239]. Register usage can be controlled using:
*   The `maxrregcount` compiler option [CUDA_C_Programming_Guide:L6195-L6239].
*   The `__launch_bounds__()` qualifier [CUDA_C_Programming_Guide:L6195-L6239].
*   The `__maxnreg__()` qualifier [CUDA_C_Programming_Guide:L6195-L6239].

The register file is organized as 32-bit registers, meaning a `double` variable uses two registers [CUDA_C_Programming_Guide:L6195-L6239].

### Execution Configuration

The effect of execution configuration on performance depends on the kernel code, so experimentation is recommended [CUDA_C_Programming_Guide:L6195-L6239]. Applications can parametrize execution configurations based on register file size, shared memory size, compute capability, number of multiprocessors, and memory bandwidth, all of which can be queried via the runtime [CUDA_C_Programming_Guide:L6195-L6239]. The number of threads per block should be chosen as a multiple of the warp size to avoid wasting computing resources with under-populated warps [CUDA_C_Programming_Guide:L6195-L6239].
