## Registers and Performance

The register is the fastest storage in the memory hierarchy. Keeping data in registers as long as possible is critical to performance. But unfortunately, register space is limited and much smaller than memory space. The Intel<sup>®</sup> Data Center GPU Max Series product, for example, has 64KB general-purpose register file (GRF) space for each vector engine, or 128 general-purpose registers, each 64 bytes wide, for each XVE thread in small register mode.

Thus, the register space can be allocated only to a small set of variables at any point during execution. Fortunately, A given register can hold different variables at different times because different sets of variables are needed at different times.

In SYCL, the compiler allocates registers to private variables in work items. Multiple work items in a subgroup are packed into one XVE thread. The compiler aims to assign as many variables to registers as possible. By default, the compiler uses register pressure as one of the heuristics to choose SIMD width or sub-group size. High register pressures can result in smaller sub-group size (for example 16 instead of 32) if a sub-group size is not explicitly requested. It can also cause register spilling, i.e., moving some variables currently in registers to memory to make room for other variables, or cause certain variables not to be promoted to registers.

The hardware may not be fully utilized if sub-group size or SIMD width is not the maximum the hardware supports. Memory traffic can be increased if register spills or accesses to not-promoted-to-register variables occur inside hot loops. In both cases, performance can be significantly degraded.

Though the compiler uses intelligent algorithms to allocate variables in registers and to minimize register spills, optimizations by developers can help the compiler to do a better job and often make a big performance difference.

• Finding Kernels with Register Spills

• Small Register Mode vs. Large Register Mode

• Optimizing Register Spills

• Porting Code with High Register Pressure to Intel<sup>®</sup> Max GPUs

## Finding Kernels with Register Spills

The compiler outputs a warning if a kernel is compiled ahead of time and has register spills:

```shell
$ icpx -fsycl -fsycl-targets=spir64_gen -Xsycl-target-backend "-device pvc"
app.cpp
```

```txt
Compilation from IR - skipping loading of FCL

warning: kernel _ZTSZ4mainEUlt_E0_ compiled SIMD32 allocated 128 regs and spilled around 396

Build succeeded.
```

However, the compiler does not report if a kernel has one or more private variables that are not prompted to registers.

The open source tool unitrace reports both kernels with register spills and kernels with not-prompted-toregister private variable(s). Plus, it works for both ahead-of-time compilation and just-in-time compilation:

```txt
$ icpx -fsycl app.cpp
$ unitrace -d ./a.out

...

== L0 Backend ==

Kernel, Calls, Time(ns), Time(%), Average(ns), Min(ns), Max(ns)
main::{lambda(auto:1)#4}, 100, 91349596800, 99.896, 913495968, 913304160, 913975360
main::{lambda(auto:1)#3}, 100, 77196960, 0.084, 771969, 2080, 76974560
main::{lambda(auto:1)#5}, 500, 4981120, 0.005, 9962, 1440, 42880
main::{lambda(auto:1)#7}, 500, 4600000, 0.005, 9200, 1440, 38720
main::{lambda(auto:1)#6}, 500, 4590880, 0.005, 9181, 1440, 39040
main::{lambda(auto:1)#1}, 100, 3494400, 0.003, 34944, 1760, 3305120
main::{lambda(auto:1)#2}, 100, 189280, 0.000, 1892, 1440, 31360

=== Kernel Properties ===

Kernel, Private Memory Per Thread, Spill Memory Per Thread
main::{lambda(auto:1)#4}, 16384, 0
main::{lambda(auto:1)#3}, 0, 8192
main::{lambda(auto:1)#5}, 0, 0
main::{lambda(auto:1)#7}, 0, 0
main::{lambda(auto:1)#6}, 0, 0
main::{lambda(auto:1)#1}, 0, 0
main::{lambda(auto:1)#2}, 0, 0
```

A non-zero value in bytes of the Spill Memory Per Thread indicates the kernel spills registers and a nonzero value in bytes of the Private Memory Per Thread indicates the kernel has at least one private variable that is not prompted to registers.

The tool also reports timing statistics for kernels executed on the device. These statistics can be helpful to developers to evaluate the performance impact of register spills and to prioritize the kernels to be optimized.
