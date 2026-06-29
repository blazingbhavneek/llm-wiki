# CUDA Dynamic Parallelism (CDP1) ECC Errors

In the context of CUDA Dynamic Parallelism version 1 (CDP1), error handling for Error Correcting Code (ECC) memory errors follows a specific protocol distinct from CDP2.

## Notification and Reporting

Code executing within a CUDA kernel does not receive direct notification of ECC errors [CUDA_C_Programming_Guide:L14978-L14983]. Instead, these errors are reported at the host side once the entire launch tree has completed [CUDA_C_Programming_Guide:L14978-L14983].

## Execution Behavior

When ECC errors arise during the execution of a nested program, the system's response depends on the specific error and configuration settings [CUDA_C_Programming_Guide:L14978-L14983]. The execution will either generate an exception or continue, rather than failing immediately or silently ignoring the error within the kernel context [CUDA_C_Programming_Guide:L14978-L14983].

## Comparison with CDP2

For details regarding ECC error handling in the CDP2 version of dynamic parallelism, refer to the separate ECC Errors section for CDP2 [CUDA_C_Programming_Guide:L14978-L14983].
