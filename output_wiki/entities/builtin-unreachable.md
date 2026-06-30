# 10.18.5 __builtin_unreachable()

Compiler optimization hint. Indicates control flow never reaches this point. Undefined behavior if reached at runtime.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8534-L8553

Citation: [CUDA_C_Programming_Guide:L8534-L8553]

````text
```

## 10.18.5. \_\_builtin\_unreachable()

```txt
void __builtin_unreachable(void)
```

Indicates to the compiler that control flow never reaches the point where this function is being called from. The program has undefined behavior if the control flow does actually reach this point at run time.

Example:

```txt
// indicates to the compiler that the default case label is never reached.
switch (in) {
case 1: return 4;
case 2: return 10;
default: __builtin_unreachable();
}
```
````
