## GRF Mode Specification at Command Line

The -ftarget-register-alloc-mode=<arg> compiler option provides the ability to guide GRF mode selection in the IGC graphics compiler. The format of <arg> is Device0:Mode0[,Device1:Mode1...]. Currently the only supported Device is pvc. The supported modes are:

Provide no specification to IGC on the register file mode to select. Currently, IGC always chooses small register file mode with no specification.

Forces IGC to select small register file mode for ALL kernels

Forces IGC to select large register file mode for ALL kernels

Enables IGC to select small/large GRF mode on a per-kernel basis based on heuristics

If this option is not specified, IGC selects a GRF mode on a per-kernel basis based on heuristics on Linux for the Intel Data Center GPU Max Series and small GRF mode otherwise.

## OpenMP - GRF Mode Selection (AOT)

Following are the various commands that can be used to specify the requisite backend option during AOT compilation for OpenMP backends. Here, test.cpp can be any valid program:

## OpenMP - GRF Mode Selection (JIT)

Following are the various commands that can be used to specify the requisite backend option during JIT compilation for OpenMP backends. Here, test.cpp can be any valid program:

## SYCL – GRF Mode Selection (AOT)

Following are the various commands that can be used to specify the requisite backend option during AOT compilation for SYCL backends. Here, test.cpp can be any valid SYCL program:

```txt
icpx -fsycl -fsycl-targets=spir64_gen
-ftarget-register-alloc-mode=pvc:large
-Xsycl-target-backend "-device pvc" test.cpp
// IGC will force large GRF mode for all kernels
```

```shell
icpx -fsycl -fsycl-targets=spir64_gen
-ftarget-register-alloc-mode=pvc:auto
-Xsycl-target-backend "-device pvc" test.cpp
// IGC will use compiler heuristics to pick between small and large GRF
mode on a per-kernel basis
```

```txt
icpx -fsycl -fsycl-targets=spir64_gen
-ftarget-register-alloc-mode=pvc:small
-Xsycl-target-backend "-device pvc" test.cpp
// IGC will automatically use small GRF mode for all kernels
```

## SYCL – GRF Mode Selection (JIT)

Following are the various commands that can be used to specify the requisite backend option during JIT compilation for SYCL backends. Here, test.cpp can be any valid SYCL program:

```batch
icpx -fsycl
-ftarget-register-alloc-mode=pvc:large
test.cpp
// IGC will force large GRF mode for all kernels
```

```txt
icpx -fsycl
-ftarget-register-alloc-mode=pvc:auto
test.cpp
// IGC will use compiler heuristics to pick between small and large GRF
mode on a per-kernel basis
```

```batch
icpx -fsycl
-ftarget-register-alloc-mode=pvc:small
test.cpp
// IGC will automatically use small GRF mode for all kernels
```
