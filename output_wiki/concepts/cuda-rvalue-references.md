# Rvalue References in CUDA

In CUDA C++, rvalue reference utilities such as `std::move` and `std::forward` are treated specially by the compiler regarding execution space specifiers.

## Default Behavior

By default, the CUDA compiler implicitly considers the `std::move` and `std::forward` function templates to have `__host__ __device__` execution space specifiers. This allows these functions to be invoked directly from device code [CUDA_C_Programming_Guide:L17615-L17618].

## Disabling Device Support

The default behavior can be disabled using the `--no-host-device-move-forward` compiler flag. When this flag is enabled, `std::move` and `std::forward` are considered as `__host__` functions only and will not be directly invokable from device code [CUDA_C_Programming_Guide:L17615-L17618].

## Related Concepts

- CUDA std::move
- CUDA std::forward
