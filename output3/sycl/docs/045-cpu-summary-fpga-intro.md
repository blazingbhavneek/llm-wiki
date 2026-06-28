
CPU processors implement SIM D instruction sets with different SIM D widths. In many cases, this is an implementation detail and is transparent to the application executing kernels on the CPU, as the compiler can determine an efficient group of data elements to process with a specific SIM D size rather than requiring us to use the SIM D instructions explicitly. Sub-groups may be used to more directly express cases where the grouping of data elements should be subject to SIM D execution in kernels.

Given computational complexity, selecting the code and data layouts that are most amenable to vectorization may ultimately result in higher performance. While selecting data structures, try to choose a data layout, alignment, and data width such that the most frequently executed calculation can access memory in a SIM D-friendly manner with maximum parallelism, as described in this chapter.

## Summary

To get the most out of thread-level parallelism and SIMD vector-level parallelism on CPUs, we need to keep the following goals in mind:

• Be familiar with all types of SYCL parallelism and the underlying CPU architectures that we wish to target.

• Exploit the right amount of parallelism—not more and not less—at a thread level that best matches hardware resources. Use vendor tooling, such as analyzers and profilers, to help guide our tuning work to achieve this.

• Be mindful of thread affinity and memory first touch impact on program performance.

Design data structures with a data layout, alignment, and data width such that the most frequently executed calculations can access memory in a SIMD-friendly manner with maximum SIMD parallelism.

• Be mindful of balancing the cost of masking vs. code branches.

• Use a clear programming style that minimizes potential memory aliasing and side effects.

Be aware of the scalability limitations of using vector types and interfaces. If a compiler implementation maps them to hardware SIMD instructions, a fixed vector size may not match the SIMD width of SIMD registers well across multiple generations of CPUs and CPUs from different vendors.

![](images/868235066d8e7e2264449cd4881213e1de8d6a1d21c1d417b7739516fa6b9a0f.jpg)

cc Open Access This chapter is licensed under the terms of BY the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.

# Programming for FPGAs

Kernel-based programming originally became popular as a way to access GPUs. Since it has now been generalized across many types of accelerators, it is important to understand how our style of programming affects the mapping of code to an FPGA as well.

Field-programmable gate arrays (FPGAs) are unfamiliar to the majority of software developers, in part because most desktop computers don’t include an FPGA alongside the typical CPU and GPU. But FPGAs are worth knowing about because they offer advantages in many applications. The same questions need to be asked as we would of other accelerators, such as “When should I use an FPGA?”, “What parts of my applications should be offloaded to FPGA?”, and “How do I write code that performs well on an FPGA?”

This chapter gives us the knowledge to start answering those questions, at least to the point where we can decide whether an FPGA is interesting for our applications, and to know which constructs are commonly used to achieve performance. This chapter is the launching point from which we can then read vendor documentation to fill in details for specific products and toolchains. We begin with an overview of how programs can map to spatial architectures such as FPGAs, followed by discussion of some properties that make FPGAs a good choice as an accelerator, and we finish by introducing the programming constructs used to achieve performance.

The “How to Think About FPGAs” section in this chapter is applicable to thinking about any FPGA. SYCL allows vendors to specify devices beyond CPUs and GPUs but does not specifically say how to support an FPGA. The specific vendor support for FPGAs described in this chapter is currently unique to DPC++, namely, FPGA selectors and pipes. FPGA selectors and pipes are the only DPC++ extensions used in this chapter. It is hoped that vendors will converge on similar or compatible means of supporting FPGAs, and this is encouraged by DPC++ as an open source project.

## Performance Caveats

As with any processor or accelerator, FPGA devices differ from vendor to vendor or even from product generation to product generation; therefore, best practices for one device may not be best practices for a different device. The advice in this chapter is likely to benefit many FPGA devices, both now and in the future, however…

…to achieve optimal performance for a particular FPGA, always consult the vendor’s documentation!
