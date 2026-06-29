# #pragma nv_abi

## Overview

The `#pragma nv_abi` directive enables applications compiled in separate compilation mode to achieve performance similar to that of whole program compilation [CUDA_C_Programming_Guide:L11850-L11850]. It is part of the Custom ABI Pragmas feature set [CUDA_C_Programming_Guide:L11848-L11848].

## Syntax and Usage

The syntax for using this pragma involves specifying arguments that define the ABI properties. The arguments that follow `#pragma nv_abi` are optional and can be provided in any order; however, at least one argument is required [CUDA_C_Programming_Guide:L11858-L11858].

The general syntax is as follows, where ICE refers to any integral constant expression (ICE) [CUDA_C_Programming_Guide:L11852-L11852]:

```cpp
#pragma nv_abi <argument>
```

## Arguments

The pragma supports specific arguments to control register preservation during function calls. The `preserve_n` arguments set a limit on the number of registers preserved during a function call [CUDA_C_Programming_Guide:L11860-L11860].

### preserve_n_data

`preserve_n_data(ICE)` limits the number of data registers preserved [CUDA_C_Programming_Guide:L11862-L11862].

### preserve_n_control

`preserve_n_control(ICE)` limits the number of control registers preserved [CUDA_C_Programming_Guide:L11864-L11864].
