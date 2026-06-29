# Hardware Multithreading and Resources

Hardware multithreading in CUDA is managed at the level of warps and thread blocks within a multiprocessor (SM). The architecture is designed to hide latency by maintaining multiple execution contexts simultaneously, allowing the processor to switch between them without performance penalty.

## Context Switching and Warp Scheduling

The execution context for each warp—including program counters, registers, and other state—is maintained on-chip for the entire lifetime of the warp [CUDA_C_Programming_Guide:L6158-L6176]. Because these contexts reside in fast on-chip memory, switching from one execution context to another incurs no cost [CUDA_C_Programming_Guide:L6158-L6176].

At every instruction issue time, a warp scheduler selects a warp that has threads ready to execute its next instruction (i.e., the active threads of the warp) and issues the instruction to those threads [CUDA_C_Programming_Guide:L6158-L6176]. This mechanism ensures that the multiprocessor remains busy as long as there are warps with ready threads.

## Resource Partitioning

Multiprocessors have finite resources that are partitioned among the active execution units:

*   **Registers**: Each multiprocessor has a set of 32-bit registers that are partitioned among the warps [CUDA_C_Programming_Guide:L6158-L6176].
*   **Shared Memory**: A parallel data cache or shared memory is partitioned among the thread blocks [CUDA_C_Programming_Guide:L6158-L6176].

The number of blocks and warps that can reside and be processed together on a multiprocessor for a given kernel depends on:
1.  The amount of registers and shared memory used by the kernel.
2.  The amount of registers and shared memory available on the multiprocessor [CUDA_C_Programming_Guide:L6158-L6176].

## Limits on Resident Blocks and Warps

There are maximum limits on the number of resident blocks and the number of resident warps per multiprocessor [CUDA_C_Programming_Guide:L6158-L6176]. These limits, along with the total amount of registers and shared memory available, are functions of the device's compute capability [CUDA_C_Programming_Guide:L6158-L6176].

If there are not enough registers or shared memory available per multiprocessor to process at least one block, the kernel will fail to launch [CUDA_C_Programming_Guide:L6158-L6176].

## Warp Size Formula

The total number of warps in a block is calculated using the following formula:

$$ \text{Total Warps} = \text{ceil} \left( \frac { T } { W _ { s i z e } } , 1 \right) $$

Where:
*   $T$ is the number of threads per block.
*   $W_{size}$ is the warp size, which is equal to 32.
*   $\text{ceil}(x, y)$ is equal to $x$ rounded up to the nearest multiple of $y$ [CUDA_C_Programming_Guide:L6158-L6176].

## Occupancy Calculation

The total number of registers and total amount of shared memory allocated for a block are documented in the CUDA Occupancy Calculator provided in the CUDA Toolkit [CUDA_C_Programming_Guide:L6158-L6176]. Developers should use this tool to determine optimal block configurations that maximize occupancy without exceeding hardware limits.
