## Expressing Parallelism

To improve the performance of this kernel for both CPUs and GPUs, we can instead submit a range of data elements to process in parallel, by converting one of the loops to a parallel\_for. For the matrix multiplication kernel, we can choose to submit a range of data elements representing either of the two outermost loops. In Figure 15-5, we’ve chosen to process rows of the result matrix in parallel.

```c
h.parallel_for(range{M}, [=](id<1> idx) {
  int m = idx[0];

  for (int n = 0; n < N; n++) {
    T sum = 0;
    for (int k = 0; k < K; k++) {
      sum += matrixA[m * K + k] * matrixB[k * N + n];
    }
    matrixC[m * N + n] = sum;
  }
});
```  
Figure 15-5. Somewhat-parallel matrix multiplication

## CHOOSING HOW TO PARALLELIZE

Choosing which dimension to parallelize is one very important way to tune an application for both GPUs and other device types. Subsequent sections in this chapter will describe some of the reasons why parallelizing in one dimension may perform better than parallelizing in a different dimension.

Even though the somewhat-parallel kernel is very similar to the singletask kernel, it should run better on a CPU and much better on a GPU. As shown in Figure 15-6, the parallel\_for enables work-items representing rows of the result matrix to be processed on multiple processor resources in parallel, so all execution resources stay busy.

![](images/6affaa78ea0de9bcae091cb7bba4bc2bf1d3e1ac060879c65358f72fada1d6c4.jpg)  
Figure 15-6. Somewhat-parallel kernel keeps more processor resources busy

Note that the exact way that the rows are partitioned and assigned to different processor resources is not specified, giving an implementation flexibility to choose how best to execute the kernel on a device. For example, instead of executing individual rows on a processor, an implementation may choose to execute consecutive rows on the same processor to gain locality benefits.

## Expressing More Parallelism

We can parallelize the matrix multiplication kernel even more by choosing to process both outer loops in parallel. Because parallel\_for can express parallel loops over up to three dimensions, this is straightforward, as shown in Figure 15-7. In Figure 15-7, note that both the range passed to parallel\_for and the item representing the index in the parallel execution space are now two-dimensional.

```c
h.parallel_for(range{M, N}, [=](id<2> idx) {
  int m = idx[0];
  int n = idx[1];

  T sum = 0;
  for (int k = 0; k < K; k++) {
    sum += matrixA[m * K + k] * matrixB[k * N + n];
  }

  matrixC[m * N + n] = sum;
});
```

## Figure 15-7. Even more parallel matrix multiplication

Exposing additional parallelism will likely improve the performance of the matrix multiplication kernel when run on a GPU. This is likely to be true even when the number of matrix rows exceeds the number of GPU processors. The next few sections describe possible reasons why this may be the case.

## Simplified Control Logic (SIMD Instructions)

Many GPU processors optimize control logic by leveraging the fact that most data elements tend to take the same control flow path through a kernel. For example, in the matrix multiplication kernel, each data element executes the innermost loop the same number of times since the loop bounds are invariant.

When data elements take the same control flow path through a kernel, a processor may reduce the costs of managing an instruction stream by sharing control logic among multiple data elements and executing them as a group. One way to do this is to implement a single instruction, multiple data, or SIMD, instruction set, where multiple data elements are processed simultaneously by a single instruction.

## THREADS VS. INSTRUCTION STREAMS

In many parallel programming contexts and GPU literature, the term “thread” is used to mean an “instruction stream.” In these contexts, a “thread” is different than a traditional operating system thread and is typically much more lightweight. This isn’t always the case, though, and in some cases, a “thread” is used to describe something completely different.

Since the term “thread” is overloaded and easily misunderstood, even among different GPU vendors, this chapter uses the term “instruction stream” instead.

![](images/1d2b1e2df17785cc6ec3484359f09127ea6f095b110197cb31c463aca2e2a283.jpg)  
Figure 15-8. Four-wide SIMD processor: the four ALUs share fetch/ decode logic

The number of data elements that are processed simultaneously by a single instruction is sometimes referred to as the SIMD width of the instruction or the processor executing the instruction. In Figure 15-8, the four ALUs share the same control logic, so this may be described as a fourwide SIMD processor.

GPU processors are not the only processors that implement SIMD instruction sets. Other processor types also implement SIMD instruction sets to improve efficiency when processing large sets of data. The main difference between GPU processors and other processor types is that GPU processors rely on executing multiple data elements in parallel to achieve good performance and that GPU processors may support wider SIMD widths than other processor types. For example, it is not uncommon for GPU processors to support SIMD widths of 16, 32, or more data elements.

## PROGRAMMING MODELS: SPMD AND SIMD

Although GPU processors implement SIM D instruction sets with varying widths, this is usually an implementation detail and is transparent to the application executing data-parallel kernels on the GPU processor. This is because many GPU compilers and runtime APIs implement a single program, multiple data, or SPMD, programming model, where the GPU compiler and runtime API determine the most efficient group of data elements to process with a SIM D instruction stream, rather than expressing the SIM D instructions explicitly. The “Sub-Groups” section of Chapter 9 explores cases where the grouping of data elements is visible to applications.

In Figure 15-9, we have widened each of our execution resources to support four-wide SIMD, allowing us to process four times as many matrix rows in parallel.

![](images/ef2ea5513279aad48a006ba95b84370e66f9b2867c02b4426ef2f5f79e478631.jpg)  
Figure 15-9. Executing a somewhat-parallel kernel on SIMD processors

The use of SIMD instructions that process multiple data elements in parallel is one of the ways that the performance of the parallel matrix multiplication kernels in Figures 15-5 and 15-7 is able to scale beyond the number of processors alone. The use of SIMD instructions also provides natural locality benefits in many cases, including matrix multiplication, by executing consecutive data elements on the same processor.

Kernels benefit from parallelism across processors and parallelism within processors!
