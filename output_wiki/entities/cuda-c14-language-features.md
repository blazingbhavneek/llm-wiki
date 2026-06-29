# CUDA C++14 Language Features

The CUDA C++ compiler (`nvcc`) supports a subset of the C++14 language standard for device code. The following table lists the new language features accepted into the C++14 standard, their corresponding proposal numbers, and the `nvcc` version in which they became available for device code execution [CUDA_C_Programming_Guide:L16514-L16521].

## Supported Features

All features listed below with a version number are available in `nvcc` device code starting from that version. Features with an empty version column are not supported in device code [CUDA_C_Programming_Guide:L16514-L16521].

| Language Feature | C++14 Proposal | Available in nvcc (device code) |
| :--- | :--- | :--- |
| Tweak to certain C++ contextual conversions | N3323 | 9.0 |
| Binary literals | N3472 | 9.0 |
| Functions with deduced return type | N3638 | 9.0 |
| Generalized lambda capture (init-capture) | N3648 | 9.0 |
| Generic (polymorphic) lambda expressions | N3649 | 9.0 |
| Variable templates | N3651 | 9.0 |
| Relaxing requirements on constexpr functions | N3652 | 9.0 |
| Member initializers and aggregates | N3653 | 9.0 |
| Clarifying memory allocation | N3664 | |
| Sized deallocation | N3778 | |
| [[deprecated]] attribute | N3760 | 9.0 |
| Single-quotation-mark as a digit separator | N3781 | 9.0 |

## Notes

- **Device Code Support**: The "Available in nvcc (device code)" column specifically indicates support for code compiled for execution on the GPU. Host-side compilation may support additional features or different versions.
- **Unlisted Features**: Features such as "Clarifying memory allocation" (N3664) and "Sized deallocation" (N3778) are part of the C++14 standard but are not currently supported in nvcc device code [CUDA_C_Programming_Guide:L16514-L16521].
- **Version Requirement**: All supported features listed above require `nvcc` version 9.0 or later for device code compilation [CUDA_C_Programming_Guide:L16514-L16521].
