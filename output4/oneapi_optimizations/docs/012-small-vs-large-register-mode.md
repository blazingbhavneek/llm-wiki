## Small Register Mode vs Large Register Mode

Intel<sup>®</sup> Data Center GPU Max Series products support two GRF modes: small GRF mode and large GRF mode. Each XVE has a total of 64 KB of register space In Small GRF mode, a single hardware thread can access 128 GRF registers, each of which is 64B wide. In this mode, 8 hardware threads are available per XVE. In Large GRF mode, a single hardware thread can access 256 GRF registers, each of which is 64B wide. In this mode, 4 hardware threads are available per XVE.

There are two ways to control how Intel<sup>®</sup> Graphics Compiler (IGC) selects between these two modes: (1) command line and (2) per-kernel specification. In this chapter, we provide a step-by-step guideline on how users can provide this control for both SYCL and OpenMP applications.

```shell
icpx -fiopenmp -fopenmp-targets=spir64_gen
-ftarget-register-alloc-mode=pvc:large
-Xopenmp-target-backend "-device pvc" test.cpp
// IGC will force large GRF mode for all kernels

icpx -fiopenmp -fopenmp-targets=spir64_gen
-ftarget-register-alloc-mode=pvc:auto
-Xopenmp-target-backend "-device pvc" test.cpp
// IGC will use compiler heuristics to pick between small and large GRF
mode on a per-kernel basis

icpx -fiopenmp -fopenmp-targets=spir64_gen
-ftarget-register-alloc-mode=pvc:small
-Xopenmp-target-backend "-device pvc" test.cpp
// IGC will automatically use small GRF mode for all kernels
```

```shell
icpx -fiopenmp -fopenmp-targets=spir64
-ftarget-register-alloc-mode=pvc:large
test.cpp
// IGC will force large GRF mode for all kernels

icpx -fiopenmp -fopenmp-targets=spir64
-ftarget-register-alloc-mode=pvc:auto
test.cpp
// IGC will use compiler heuristics to pick between small and large GRF
mode on a per-kernel basis

icpx -fiopenmp -fopenmp-targets=spir64
-ftarget-register-alloc-mode=pvc:small
test.cpp
// IGC will automatically use small GRF mode for all kernels
```
