# Compute Capability 6.x

Architecture specifications for Compute Capability 6.x (Pascal) including updated core counts, scheduler configurations, cache sizes, and memory behavior inheriting from 5.x.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L19606-L19658

Citation: [CUDA_C_Programming_Guide:L19606-L19658]

````text
## 20.5. Compute Capability 6.x

## 20.5.1. Architecture

An SM consists of:

▶ 64 (compute capability 6.0) or 128 (6.1 and 6.2) CUDA cores for arithmetic operations,

▶ 16 (6.0) or 32 (6.1 and 6.2) special function units for single-precision floating-point transcendental functions,

▶ 2 (6.0) or 4 (6.1 and 6.2) warp schedulers.

When an SM is given warps to execute, it first distributes them among its schedulers. Then, at every instruction issue time, each scheduler issues one instruction for one of its assigned warps that is ready to execute, if any.

An SM has:

▶ a read-only constant cache that is shared by all functional units and speeds up reads from the constant memory space, which resides in device memory,

▶ a unified L1/texture cache for reads from global memory of size 24 KB (6.0 and 6.2) or 48 KB (6.1),

a shared memory of size 64 KB (6.0 and 6.2) or 96 KB (6.1).

The unified L1/texture cache is also used by the texture unit that implements the various addressing modes and data filtering mentioned in Texture and Surface Memory.

There is also an L2 cache shared by all SMs that is used to cache accesses to local or global memory, including temporary register spills. Applications may query the L2 cache size by checking the l2CacheSize device property (see Device Enumeration).

The cache behavior (for example, whether reads are cached in both the unified L1/texture cache and L2 or in L2 only) can be partially configured on a per-access basis using modifiers to the load instruction.

![](images/1dcce326d13eeed54d91cb7f57d932687dd0298d6b847d712d564aee0d73e888.jpg)  
Figure 39: Strided Shared Memory Accesses in 32 bit bank size mode.  
Left Linear addressing with a stride of one 32-bit word (no bank conflict).  
Linear addressing with a stride of two 32-bit words (two-way bank conflict).  
Linear addressing with a stride of three 32-bit words (no bank conflict).

![](images/ef593d54121b2b98b7b0128d204eba30c24b38edb2d8ee83e635fd6e5a5116ef.jpg)  
Figure 40: Irregular Shared Memory Accesses.

Left Conflict-free access via random permutation.

## Middle

Conflict-free access since threads 3, 4, 6, 7, and 9 access the same word within bank 5. Right

Conflict-free broadcast access (threads access the same word within a bank).

## 20.5.2. Global Memory

Global memory behaves the same way as in devices of compute capability 5.x (See Global Memory).

## 20.5.3. Shared Memory

Shared memory behaves the same way as in devices of compute capability 5.x (See Shared Memory).
````
