# CUDA ECC Errors

CUDA Error Correction Code (ECC) errors are handled differently depending on whether the code is running on the host or within a device kernel.

## Kernel-Side Visibility

No notification of ECC errors is available to code executing within a CUDA kernel [CUDA_C_Programming_Guide:L14254-L14258]. Kernel code cannot directly detect or handle memory corruption caused by ECC failures during execution.

## Host-Side Reporting

ECC errors are reported at the host side once the entire launch tree has completed [CUDA_C_Programming_Guide:L14254-L14258]. This means that error detection is deferred until the host synchronizes with the device or queries the status of the launch.

## Nested Program Execution

When ECC errors arise during the execution of a nested program, the system behavior depends on the specific error and configuration settings [CUDA_C_Programming_Guide:L14254-L14258]. The execution may either generate an exception or continue, allowing the program to proceed despite the underlying hardware error [CUDA_C_Programming_Guide:L14254-L14258].
