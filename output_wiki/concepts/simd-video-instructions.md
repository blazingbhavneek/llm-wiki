# SIMD Video Instructions

PTX ISA version 3.0 includes SIMD (Single Instruction, Multiple Data) video instructions which operate on pairs of 16-bit values and quads of 8-bit values. These are available on devices of compute capability 3.0 [CUDA_C_Programming_Guide:L11751-L11751].

The SIMD video instructions are [CUDA_C_Programming_Guide:L11753-L11753]:

The basic syntax of an asm() statement is [CUDA_C_Programming_Guide:L11771-L11771]:

```javascript
[CUDA_C_Programming_Guide:L11773-L11773]
```

This uses the vabsdiff4 instruction to compute an integer quad byte SIMD sum of absolute diferences. The absolute diference value is computed for each byte of the unsigned integers A and B in SIMD fashion. The optional accumulate operation (.add) is specified to sum these diferences [CUDA_C_Programming_Guide:L11784-L11784].

Refer to the document “Using Inline PTX Assembly in CUDA” for details on using the assembly statement in your code. Refer to the PTX ISA documentation (“Parallel Thread Execution ISA Version 3.0” for example) for details on the PTX instructions for the version of PTX that you are using [CUDA_C_Programming_Guide:L11786-L11786].

## References

- CUDA_C_Programming_Guide
