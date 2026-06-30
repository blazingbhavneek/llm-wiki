# Assignment Operator

Restrictions on assigning to __constant__, __shared__, and built-in variables.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L16855-L16861

Citation: [CUDA_C_Programming_Guide:L16855-L16861]

````text
## 18.5.5.1 Assignment Operator

\_\_constant\_\_ variables can only be assigned from the host code through runtime functions (Device Memory); they cannot be assigned from the device code.

\_\_shared\_\_ variables cannot have an initialization as part of their declaration.

It is not allowed to assign values to any of the built-in variables defined in Built-in Variables.
````
