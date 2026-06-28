
Most of the code examples so far have assumed that each instance of a kernel function corresponds to a single operation on a single piece of data. This is a straightforward way to write kernels, but such a one-to-one mapping is not dictated by SYCL or any of the kernel forms—we always have complete control over the assignment of data (and computation) to individual work-items and making this assignment parameterizable can be a good way to improve performance portability.

## One-to-One Mapping

When we write kernels such that there is a one-to-one mapping of work to work-items, those kernels must always be launched with a range or nd\_range with a size exactly matching the amount of work that needs to be done. This is the most obvious way to write kernels, and in many cases, it works very well—we can trust an implementation to map work-items to hardware efficiently.

However, when tuning for performance on a specific combination of system and implementation, it may be necessary to pay closer attention to low-level scheduling behaviors. The scheduling of work-groups to compute resources is implementation-defined and could potentially be dynamic (i.e., when a compute resource completes one work-group, the next work-group it executes may come from a shared queue). The impact of dynamic scheduling on performance is not fixed, and its significance depends upon factors including the execution time of each instance of the kernel function and whether the scheduling is implemented in software (e.g., on a CPU) or hardware (e.g., on a GPU).

## Many-to-One Mapping

The alternative is to write kernels with a many-to-one mapping of work to work-items. The meaning of the range changes subtly in this case: the range no longer describes the amount of work to be done, but rather the number of workers to use. By changing the number of workers and the amount of work assigned to each worker, we can fine-tune work distribution to maximize performance.

Writing a kernel of this form requires two changes:

1. The kernel must accept a parameter describing the total amount of work.

2. The kernel must contain a loop assigning work to work-items.

A simple example of such a kernel is given in Figure 4-22. Note that the loop inside the kernel has a slightly unusual form—the starting index is the work-item’s index in the global range, and the stride is the total number of work-items. This round-robin scheduling of data to work-items ensures that all N iterations of the loop will be executed by a work-item, but also that linear work-items access contiguous memory locations (to improve cache locality and vectorization behavior). Work can be similarly distributed across groups or the work-items in individual groups to further improve locality.

```txt
size_t N = ...;  // amount of work
size_t W = ...;  // number of workers
h.parallel_for(range{W}, [=](item<1> it) {
    for (int i = it.get_id()[0]; i < N;
        i += it.get_range()[0]) {
        output[i] = function(input[i]);
    }
});
```

## Figure 4-22. Kernel with separate data and execution ranges

These work distribution patterns are common, and we expect that future versions of SYCL will introduce syntactic sugar to simplify the expression of work distribution in ND-range kernels.

## Choosing a Kernel Form

Choosing between the different kernel forms is largely a matter of personal preference and heavily influenced by prior experience with other parallel programming models and languages.

The other main reason to choose a specific kernel form is that it is the only form to expose certain functionality required by a kernel. Unfortunately, it can be difficult to identify which functionality will be required before development begins—especially while we are still unfamiliar with the different kernel forms and their interaction with various classes.

We have constructed two guides based on our own experience to help us navigate this complex space. These guides should be considered initial suggestions and are definitely not intended to replace our own experimentation—the best way to choose between the different kernel forms will always be to spend some time writing in each of them, in order to learn which form is the best fit for our application and development style.

The first guide is the flowchart in Figure 4-23, which selects a kernel form based on

1. Whether we have previous experience with parallel programming

2. Whether we are writing a new code from scratch or are porting an existing parallel program written in a different language

3. Whether our kernel is embarrassingly parallel or reuses data between different instances of the kernel function

4. Whether we are writing a new kernel in SYCL to maximize performance, to improve the portability of our code, or because it provides a more productive means of expressing parallelism than lower-level languages

![](images/e4825e67893dda20e28e6c7b749d54deea12cf80627011e3a01eda5c4d54b8b6.jpg)  
Figure 4-23. Helping choose the right form for our kernel

The second guide is the set of features exposed to each of the kernel forms. Work-groups, sub-groups, group barriers, group-local memory, group functions (e.g., broadcast), and group algorithms (e.g., scan, reduce) are only available to ND-range kernels, and so we should prefer NDrange kernels in situations where we are interested in expressing complex algorithms or fine-tuning for performance.

The features available to each kernel form should be expected to change as the language evolves, but we expect the basic trend to remain the same: basic data-parallel kernels will not expose locality-aware features and explicit ND-range kernels will expose all performanceenabling features.

## Summary

This chapter introduced the basics of expressing parallelism in C++ with SYCL and discussed the strengths and weaknesses of each approach to writing data-parallel kernels.

SYCL provides support for many forms of parallelism, and we hope that we have provided enough information to prepare readers to dive in and start coding!

We have only scratched the surface, and a deeper dive into many of the concepts and classes introduced in this chapter is forthcoming: the usage of local memory, barriers, and communication routines are covered in Chapter 9; different ways of defining kernels besides using lambda expressions are discussed in Chapters 10 and 20; detailed mappings of the ND-range execution model to specific hardware are explored in Chapters 15, 16, and 17; and best practices for expressing common parallel patterns using SYCL are presented in Chapter 14.

![](images/00c7b1b8bc34ab706d2dfb265806f5c36c44b98613754a2233e758de2cb4654a.jpg)

cc Open Access This chapter is licensed under the terms of BY the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.
