# Breakpoint Function

The `__brkpt()` function is used to suspend the execution of a kernel function. It can be called from any device thread to trigger a breakpoint [CUDA_C_Programming_Guide:L11166-L11168].

## Syntax

```c
void __brkpt();
```

## Related Functions

### __trap()

A related function, `__trap()`, can be used to initiate a trap operation. Like `__brkpt()`, it can be called from any device thread [CUDA_C_Programming_Guide:L11158-L11160]. However, while `__brkpt()` suspends execution, calling `__trap()` causes the execution of the kernel to be aborted and an interrupt to be raised in the host program [CUDA_C_Programming_Guide:L11161-L11162].

```c
void __trap();
```
