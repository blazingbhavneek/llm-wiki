# Compute Capability 5.x

Architecture specifications for Compute Capability 5.x including SM components (CUDA cores, SFUs, schedulers), cache hierarchy (L1/texture, L2), global memory caching via __ldg(), and shared memory bank organization.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L19552-L19605

Citation: [CUDA_C_Programming_Guide:L19552-L19605]

````text
## 20.4. Compute Capability 5.x

## 20.4.1. Architecture

An SM consists of:

▶ 128 CUDA cores for arithmetic operations (see CUDA C++ Best Practices Guide for throughputs of arithmetic operations),

▶ 32 special function units for single-precision floating-point transcendental functions,

## ▶ 4 warp schedulers.

When an SM is given warps to execute, it first distributes them among the four schedulers. Then, at every instruction issue time, each scheduler issues one instruction for one of its assigned warps that is ready to execute, if any.

## An SM has:

▶ a read-only constant cache that is shared by all functional units and speeds up reads from the constant memory space, which resides in device memory,

▶ a unified L1/texture cache of 24 KB used to cache reads from global memory,

▶ 64 KB of shared memory for devices of compute capability 5.0 or 96 KB of shared memory for devices of compute capability 5.2.

The unified L1/texture cache is also used by the texture unit that implements the various addressing modes and data filtering mentioned in Texture and Surface Memory.

There is also an L2 cache shared by all SMs that is used to cache accesses to local or global memory, including temporary register spills. Applications may query the L2 cache size by checking the l2CacheSize device property (see Device Enumeration).

The cache behavior (e.g., whether reads are cached in both the unified L1/texture cache and L2 or in L2 only) can be partially configured on a per-access basis using modifiers to the load instruction.

## 20.4.2. Global Memory

## Global memory accesses are always cached in L2.

Data that is read-only for the entire lifetime of the kernel can also be cached in the unified L1/texture cache described in the previous section by reading it using the \_\_ldg() function (see Read-Only Data Cache Load Function). When the compiler detects that the read-only condition is satisfied for some data, it will use \_\_ldg() to read it. The compiler might not always be able to detect that the readonly condition is satisfied for some data. Marking pointers used for loading such data with both the const and \_\_restrict\_\_ qualifiers increases the likelihood that the compiler will detect the readonly condition.

Data that is not read-only for the entire lifetime of the kernel cannot be cached in the unified L1/texture cache for devices of compute capability 5.0. For devices of compute capability 5.2, it is, by default, not cached in the unified L1/texture cache, but caching may be enabled using the following mechanisms:

Perform the read using inline assembly with the appropriate modifier as described in the PTX reference manual;

▶ Compile with the -Xptxas -dlcm=ca compilation flag, in which case all reads are cached, except reads that are performed using inline assembly with a modifier that disables caching;

Compile with the -Xptxas -fscm=ca compilation flag, in which case all reads are cached, including reads that are performed using inline assembly regardless of the modifier used.

When caching is enabled using one of the three mechanisms listed above, devices of compute capability 5.2 will cache global memory reads in the unified L1/texture cache for all kernel launches except for the kernel launches for which thread blocks consume too much of the SM’s register file. These exceptions are reported by the profiler.

## 20.4.3. Shared Memory

Shared memory has 32 banks that are organized such that successive 32-bit words map to successive banks. Each bank has a bandwidth of 32 bits per clock cycle.

A shared memory request for a warp does not generate a bank conflict between two threads that access any address within the same 32-bit word (even though the two addresses fall in the same bank). In that case, for read accesses, the word is broadcast to the requesting threads and for write accesses, each address is written by only one of the threads (which thread performs the write is undefined).

Figure 39 shows some examples of strided access.

Figure 40 shows some examples of memory read accesses that involve the broadcast mechanism.
````
