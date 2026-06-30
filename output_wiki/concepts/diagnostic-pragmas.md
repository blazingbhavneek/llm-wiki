# 10.42. Diagnostic Pragmas

Covers pragmas for controlling compiler diagnostic severity, state management (push/pop), and deprecation notices for non-nv_ prefixed pragmas in CUDA 12.0+.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L11788-L11847

Citation: [CUDA_C_Programming_Guide:L11788-L11847]

````text
## 10.42. Diagnostic Pragmas

The following pragmas may be used to control the error severity used when a given diagnostic message is issued.

```c
#pragma nv_diag_suppress
#pragma nv_diag_warning
#pragma nv_diag_error
#pragma nv_diag_default
#pragma nv_diag_once
```

Uses of these pragmas have the following form:

```python
#pragma nv_diag_xxx error_number, error_number ...
```

The diagnostic afected is specified using an error number showed in a warning message. Any diagnostic may be overridden to be an error, but only warnings may have their severity suppressed or be restored to a warning after being promoted to an error. The nv\_diag\_default pragma is used to return the severity of a diagnostic to the one that was in efect before any pragmas were issued (i.e., the normal severity of the message as modified by any command-line options). The following example suppresses the "declared but never referenced" warning on the declaration of foo:

```c
#pragma nv_diag_suppress 177
void foo()
{
    int i=0;
}
#pragma nv_diag_default 177
void bar()
{
    int i=0;
}
```

The following pragmas may be used to save and restore the current diagnostic pragma state:

```txt
#pragma nv_diagnostic push
#pragma nv_diagnostic pop
```

Examples:

```c
#pragma nv_diagnostic push
#pragma nv_diag_suppress 177
void foo()
{
    int i=0;
}
#pragma nv_diagnostic pop
void bar()
{
    int i=0;
}
```

Note that the pragmas only afect the nvcc CUDA frontend compiler; they have no efect on the host compiler.

Removal Notice: The support of diagnostic pragmas without nv\_ prefix are removed from CUDA 12.0, if the pragmas are inside the device code, warning unrecognized #pragma in device code will be emitted, otherwise they will be passed to the host compiler. If they are intended for CUDA code, use the pragmas with nv\_ prefix instead.
````
