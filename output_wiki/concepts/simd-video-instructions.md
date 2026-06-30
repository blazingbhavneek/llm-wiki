# 10.41. SIMD Video Instructions

Covers PTX ISA 3.0 SIMD video instructions, their availability on CC 3.0+, and the syntax for inline assembly using the asm() statement.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L11747-L11787

Citation: [CUDA_C_Programming_Guide:L11747-L11787]

````text
(continued from previous page)

## 10.41. SIMD Video Instructions

PTX ISA version 3.0 includes SIMD (Single Instruction, Multiple Data) video instructions which operate on pairs of 16-bit values and quads of 8-bit values. These are available on devices of compute capability 3.0.

The SIMD video instructions are:

▶ vadd2, vadd4

▶ vsub2, vsub4

▶ vavrg2, vavrg4

▶ vabsdif2, vabsdif4

▶ vmin2, vmin4

▶ vmax2, vmax4

▶ vset2, vset4

PTX instructions, such as the SIMD video instructions, can be included in CUDA programs by way of the assembler, asm(), statement.

The basic syntax of an asm() statement is:

```javascript
asm("template-string" : "constraint"(output) : "constraint"(input)"));
```

An example of using the vabsdiff4 PTX instruction is:

```javascript
asm("vabsdiff4.u32.u32.u32.add" " %0, %1, %2, %3;": "=r" (result):"r" (A), "r" (B), "r
→" (C));
```

This uses the vabsdiff4 instruction to compute an integer quad byte SIMD sum of absolute diferences. The absolute diference value is computed for each byte of the unsigned integers A and B in SIMD fashion. The optional accumulate operation (.add) is specified to sum these diferences.

Refer to the document “Using Inline PTX Assembly in CUDA” for details on using the assembly statement in your code. Refer to the PTX ISA documentation (“Parallel Thread Execution ISA Version 3.0” for example) for details on the PTX instructions for the version of PTX that you are using.
````
