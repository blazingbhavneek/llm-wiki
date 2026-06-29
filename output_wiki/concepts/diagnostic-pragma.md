# Diagnostic Pragmas

Diagnostic pragmas are compiler directives used to control the severity of diagnostic messages issued by the `nvcc` CUDA frontend compiler [CUDA_C_Programming_Guide:L11790-L11790]. These pragmas allow developers to suppress, warn, or error on specific diagnostics, or revert to default behavior [CUDA_C_Programming_Guide:L11788-L11788].

## Syntax and Usage

The general form for using these pragmas is:

```python
#pragma nv_diagnostic <directive> [arguments]
```

[CUDA_C_Programming_Guide:L11800-L11802]

## State Management

The compiler provides specific pragmas to save and restore the current diagnostic pragma state, allowing for localized changes to diagnostic behavior that can be reverted later [CUDA_C_Programming_Guide:L11821-L11821].

## Scope and Limitations

Diagnostic pragmas affect only the `nvcc` CUDA frontend compiler and have no effect on the host compiler [CUDA_C_Programming_Guide:L11844-L11844].

### Prefix Requirement and Removal Notice

Starting with CUDA 12.0, support for diagnostic pragmas without the `nv_` prefix is removed [CUDA_C_Programming_Guide:L11846-L11846].

- If such pragmas are used inside device code, the compiler will emit a warning for an unrecognized `#pragma` in device code [CUDA_C_Programming_Guide:L11846-L11846].
- If used outside device code, they may be passed to the host compiler [CUDA_C_Programming_Guide:L11846-L11846].

Developers intending to use these pragmas for CUDA code must use the version with the `nv_` prefix [CUDA_C_Programming_Guide:L11846-L11846].
