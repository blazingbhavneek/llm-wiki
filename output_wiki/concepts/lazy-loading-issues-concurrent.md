# Lazy Loading Issues: Concurrent Execution

Lazy Loading is designed to require no modifications to applications, but caveats exist for programs not fully compliant with the CUDA Programming Model [CUDA_C_Programming_Guide:L22159-L22175].

## Concurrent Execution Risks

Loading kernels may require context synchronization. Programs that incorrectly treat the possibility of concurrent kernel execution as a guarantee may encounter deadlocks [CUDA_C_Programming_Guide:L22159-L22175]. A deadlock occurs if a program assumes two kernels will execute concurrently, but one kernel will not return without the other executing [CUDA_C_Programming_Guide:L22159-L22175].

### Example Scenario

A specific anti-pattern involves a scenario where:
1. Kernel A spins in an infinite loop until Kernel B is executing [CUDA_C_Programming_Guide:L22159-L22175].
2. Launching Kernel B triggers the lazy loading of Kernel B [CUDA_C_Programming_Guide:L22159-L22175].
3. If loading Kernel B requires context synchronization, the system deadlocks [CUDA_C_Programming_Guide:L22159-L22175].

In this deadlock, Kernel A is waiting for Kernel B to execute, but the loading of Kernel B is stuck waiting for Kernel A to finish so the context can be synchronized [CUDA_C_Programming_Guide:L22159-L22175].

## Mitigation Strategies

While this program structure is an anti-pattern, it can be maintained by applying one of the following solutions [CUDA_C_Programming_Guide:L22159-L22175]:

*   **Preload Kernels**: Preload all kernels that are expected to execute concurrently prior to launching them [CUDA_C_Programming_Guide:L22159-L22175].
*   **Eager Loading**: Run the application with `CUDA_MODULE_DATA_LOADING=EAGER` to force loading data eagerly, without forcing each function to load eagerly [CUDA_C_Programming_Guide:L22159-L22175].
