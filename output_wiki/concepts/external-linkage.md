# External Linkage

In CUDA device code, the `extern` qualifier imposes specific constraints on function linkage and definition. A call within device code to a function declared with the `extern` qualifier is only permitted if the function is defined within the same compilation unit as the device code making the call.

A compilation unit is defined as either a single source file or several files linked together using relocatable device code and `nvlink` [CUDA_C_Programming_Guide:L16942-L16943]. This restriction ensures that the device code can resolve the function definition locally without relying on external dynamic linking mechanisms that are not supported for device functions in this context.

## Key Constraints

- **Declaration**: The function must be declared with the `extern` qualifier in the device code.
- **Definition Location**: The actual definition of the function must reside in the same compilation unit. This includes:
  - A single source file containing both the declaration and definition.
  - Multiple files that are linked together using relocatable device code (RDC) and the `nvlink` tool [CUDA_C_Programming_Guide:L16942-L16943].

## Implications

Developers must ensure that any device function marked `extern` is fully defined within the compilation unit before linking. Failure to meet this requirement will result in compilation or linking errors, as the device code cannot reference external definitions outside the specified compilation scope.

## Related Concepts

- **Relocatable Device Code (RDC)**: Enables linking of device code across multiple compilation units, which is a prerequisite for defining `extern` device functions in separate files that are then linked via `nvlink`.
- **nvlink**: A tool used to link relocatable device code files together into a single executable or library.

## References

- [CUDA_C_Programming_Guide:L16942-L16943] CUDA C++ Programming Guide, section on External Linkage rules.
