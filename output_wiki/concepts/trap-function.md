# Trap Function

The __trap() function can be called from any device thread to initiate a trap operation. Execution of the kernel is aborted and an interrupt is raised in the host program.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L11156-L11164

Citation: [CUDA_C_Programming_Guide:L11156-L11164]

````text
## 10.33. Trap function

A trap operation can be initiated by calling the \_\_trap() function from any device thread.

```txt
void __trap();
```

The execution of the kernel is aborted and an interrupt is raised in the host program.
````
