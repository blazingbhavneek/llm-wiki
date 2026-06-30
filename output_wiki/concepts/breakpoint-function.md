# Breakpoint Function

The __brkpt() function can be called from any device thread to suspend the execution of a kernel function.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L11166-L11171

Citation: [CUDA_C_Programming_Guide:L11166-L11171]

````text
## 10.34. Breakpoint Function

Execution of a kernel function can be suspended by calling the \_\_brkpt() function from any device thread.

void \_\_brkpt();
````
