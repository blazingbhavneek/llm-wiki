# 10.18.4 __builtin_expect()

Compiler optimization hint. Indicates expected value of expression for branch prediction. Returns value of exp.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8517-L8533

Citation: [CUDA_C_Programming_Guide:L8517-L8533]

````text

## 10.18.4. \_\_builtin\_expect()

```txt
long __builtin_expect (long exp, long c)
```

Indicates to the compiler that it is expected that exp == c, and returns the value of exp. Typically used to indicate branch prediction information to the compiler.

Example:

```txt
// indicate to the compiler that likely "var == 0",
// so the body of the if-block is unlikely to be
// executed at run time.
if (__builtin_expect (var, 0))
    doit ();
````
