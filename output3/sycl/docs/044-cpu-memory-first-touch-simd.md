## Be Mindful of First Touch to Memory

Memory is stored where it is first touched (used). Since the initialization loop in our example is executed by the host thread serially, all the memory is associated with the socket that the host thread is running on. Subsequent access by other sockets will then access data from memory attached to the initial socket (used for the initialization), which is clearly undesirable for performance. We can achieve a higher performance on the STREAM Triad kernel by parallelizing the initialization loop to control the first touch effect across sockets, as shown in Figure 16-10.

```dart
template <typename T>
void init(queue& deviceQueue, T* VA, T* VB, T* VC,
        size_t array_size) {
  range<1> numOfItems{array_size};

  buffer<T, 1> bufferA(VA, numOfItems);
  buffer<T, 1> bufferB(VB, numOfItems);
  buffer<T, 1> bufferC(VC, numOfItems);

  auto queue_event = deviceQueue.submit([&](handler& cgh) {
    auto aA = bufA.template get_access<sycl_write>(cgh);
    auto aB = bufB.template get_access<sycl_write>(cgh);
    auto aC = bufC.template get_access<sycl_write>(cgh);

    cgh.parallel_for<class Init<T>>(numOfItems, [=](id<1> wi) {
      aA[wi] = 2.0;
      aB[wi] = 1.0;
      aC[wi] = 0.0;
    });
  });

  queue_event.wait();
}
```

Figure 16-10. STREAM Triad parallel initialization kernel to control first touch effects

Exploiting parallelism in the initialization code improves performance of the kernel when run on a CPU. In this instance, we achieve a \~2x performance gain on an Intel Xeon processor system.

The recent sections of this chapter have shown that by exploiting thread-level parallelism, we can utilize CPU cores and threads effectively. However, we need to exploit the SIMD vector-level parallelism in the CPU core hardware as well, to achieve peak performance.

SYCL parallel kernels benefit from thread-level parallelism across cores and hardware threads!

## SIMD Vectorization on CPU

While a well-written SYCL kernel without cross-work-item dependences can run in parallel effectively on a CPU, implementations can also apply vectorization to SYCL kernels to leverage SIMD hardware similar to the GPU support described in Chapter 15. Essentially, CPU processors may optimize memory loads, stores, and operations using SIMD instructions by leveraging the fact that most data elements are often in contiguous memory and take the same control flow paths through a data-parallel kernel. For example, in a kernel with a statement a[i] = a[i] + b[i], each data element executes with the same instruction stream load, load, add, and store by sharing hardware logic among multiple data elements and executing them as a group, which may be mapped naturally onto a hardware’s SIMD instruction set. Specifically, multiple data elements can be processed simultaneously by a single instruction.

The number of data elements that are processed simultaneously by a single instruction is sometimes referred to as the vector length (or SIMD width) of the instruction or processor executing it. In Figure 16-11, our instruction stream runs with four-way SIMD execution.

<table><tr><td colspan="4">Serial execution</td><td>SIMD execution</td></tr><tr><td>work-0</td><td>work-1</td><td>work-2</td><td>work 3</td><td>vector sub-group</td></tr><tr><td>load r0, a[0]</td><td>load r0, a[1]</td><td>load r0, a[2]</td><td>load r0, a[3]</td><td>simdload vr0, a[0...3]</td></tr><tr><td>load r1, b[0]</td><td>load r1, b[1]</td><td>load r1, b[2]</td><td>load r1, b[3]</td><td>simdload vr1, b[0...3]</td></tr><tr><td>add r0, r1</td><td>add r0, r1</td><td>add r0, r1</td><td>add r0, r1</td><td>simdadd vr0, vr1</td></tr><tr><td>store a[0], r0</td><td>store a[1], r0</td><td>store a[2], r0</td><td>store a[3], r0</td><td>simdstore a[0...3], vr0</td></tr></table>

Figure 16-11. Instruction stream for SIMD execution

CPU processors are not the only processors that implement SIMD instruction sets. Other processors such as GPUs implement SIMD instructions to improve efficiency when processing large sets of data. A key difference with Intel Xeon CPU processors, compared with other processor types, is having three fixed-size SIMD register widths 128-bit XMM, 256-bit YMM, and 512-bit ZMM instead of a variable length of SIMD width. When we write SYCL code with SIMD parallelism using sub-group or vector types (see Chapter 11), we need to be mindful of SIMD width and the number of SIMD vector registers in the hardware.

## Ensure SIMD Execution Legality

Semantically, the SYCL execution model ensures that SIMD execution can be applied to any kernel, and a set of work-items in each work-group (i.e., a sub-group) may be executed concurrently using SIMD instructions. Some implementations may instead choose to execute loops within a kernel using SIMD instructions, but this is possible if and only if all original data dependences are preserved, or data dependences are resolved by the compiler based on privatization and reduction semantics. Such implementation would likely report a sub-group size of one.

A single SYCL kernel execution can be transformed from processing a single work-item to a set of work-items using SIMD instructions within the work-group. Under the ND-range model, the fastest-growing (unit-stride) dimension is selected by the compiler vectorizer on which to generate SIMD code. Essentially, to enable vectorization given an ND-range, there should be no cross-work-item dependences between any two work-items in the same sub-group, or the compiler needs to preserve cross-work-item forward dependences in the same sub-group.

When the kernel execution of work-items is mapped to threads on CPUs, fine-grained synchronization is known to be costly, and the thread context switch overhead is high as well. It is therefore an important performance optimization to eliminate dependences between workitems within a work-group when writing a SYCL kernel for CPUs. Another effective approach is to restrict such dependences to the work-items within a sub-group, as shown for the read-before-write dependence in Figure 16-12. If the sub-group is executed under a SIMD execution model, the sub-group barrier in the kernel can be treated by the compiler as a noop, and no real synchronization cost is incurred at runtime.

```txt
const int n = 16, w = 16;

queue q;
range<2> G = {n, w};
range<2> L = {1, w};

int *a = malloc_shared<int>(n * (n + 1), q);

for (int i = 0; i < n; i++)
    for (int j = 0; j < n + 1; j++) a[i * n + j] = i + j;

q.parallel_for(
    nd_range<2>{G, L},
    [=](nd_item<2> it) [[sycl::reqd_sub_group_size(w)]] {
        // distribute uniform "i" over the sub-group with
        // 16-way redundant computation
        const int i = it.get_global_id(0);
        sub_group sg = it.get_sub_group();

        for (int j = sg.get_local_id()[0]; j < n; j += w) {
            // load a[i*n+j+1:16] before updating a[i*n+j:16]
            // to preserve loop-carried forward dependency
            auto va = a[i * n + j + 1];
            group_barrier(sg);
            a[i * n + j] = va + i + 2;
        }
        group_barrier(sg);
    })
    .wait();
```

## Figure 16-12. Using a sub-group to vectorize a loop with a forward dependence

The kernel is vectorized (with a vector length of 8 as an illustration), and its SIMD execution is shown in Figure 16-13. A work-group is formed with a group size of (1, 8), and the loop iterations inside the kernel are distributed over these sub-group work-items and executed with eight-way SIMD parallelism.

![](images/e7ef25c5fd8234288829c60314722097396364f51a993a2cc3055ce0866ea687.jpg)  
Figure 16-13. SIMD vectorization for a loop with a forward dependence

In this example, if the loop in the kernel dominates the performance, allowing SIMD vectorization across the sub-group will result in a significant performance improvement.

The use of SIMD instructions that process data elements in parallel is one way to let the performance of the kernel scale beyond the number of CPU cores and hardware threads.

## SIMD Masking and Cost

In real applications, we can expect conditional statements such as an if statement, conditional expressions such as a = b > a? a: b, loops with a variable number of iterations, switch statements, and so on. Anything that is conditional may lead to scalar control flows not executing the same code paths and just like on a GPU (Chapter 15) can lead to decreased performance. A SIMD mask is a set of bits with the value 1 or 0, which is generated from conditional statements in a kernel. Consider an example with A={1, 2, 3, 4}, B={3, 7, 8, 1} and the comparison expression a < b. The comparison returns a mask with four values {1, 1, 1, 0} that can be stored in a hardware mask register, to dictate which lanes of later SIMD instructions should execute the code that was guarded (enabled) by the comparison.

If a kernel contains conditional code, it is vectorized with masked instructions that are executed based on the mask bits associated with each data element (lane in the SIMD instruction). The mask bit for each data element is the corresponding bit in a mask register.

Using masking may result in lower performance than corresponding non-masked code. This may be caused by

• An additional mask blend operation on each load

• Dependence on the destination

Masking has a cost, so use it only when necessary. When a kernel is an ND-range kernel with explicit groupings of work-items in the execution range, care should be taken when choosing an ND-range work-group size to maximize SIMD efficiency by minimizing masking cost. When a workgroup size is not evenly divisible by a processor’s SIMD width, part of the work-group may execute with masking for the kernel.

Figure 16-14 shows how using merge masking creates a dependence on the destination register:

• With no masking, the processor executes two multiplies (vmulps) per cycle.

With merge masking, the processor executes two multiplies every four cycles as the multiply instruction (vmulps) preserves results in the destination register as shown in Figure 16-17.

Zero masking doesn’t have a dependence on the destination register and therefore can execute two multiplies (vmulps) per cycle.

<table><tr><td>No Masking</td><td>Merge Masking</td><td>Zero Masking</td></tr><tr><td>vmulps zmm0, zmm6, zmm8</td><td>vmulps zmm0{k1}, zmm6, zmm8</td><td>vmulps zmm0{k1}{z}, zmm6, zmm8</td></tr><tr><td>vmulps zmm1, zmm7, zmm8</td><td>vmulps zmm1{k1}, zmm7, zmm8</td><td>vmulps zmm1{k1}{z}, zmm7, zmm8</td></tr><tr><td>Baseline</td><td>Slowdown 4x</td><td>Slowdown 1x</td></tr></table>

Figure 16-14. Three masking code generations for masking in kernel

Accessing cache-aligned data gives better performance than accessing nonaligned data. In many cases, the address is not known at compile time or is known and not aligned. When working with loops, a peeling on memory accesses may be implemented, to process the first few elements using masked accesses, up to the first aligned address, and then to process unmasked accesses followed by a masked remainder, through multiversioning techniques. This method increases code size, but improves data processing overall. When working with parallel kernels, we as programmers can improve performance by employing similar techniques by hand, or by ensuring that allocations are appropriately aligned to improve performance.

## Avoid Array of Struct for SIMD Efficiency

AOS (Array-of-Struct) structures lead to gathers and scatters, which can both impact SIMD efficiency and introduce extra bandwidth and latency for memory accesses. The presence of a hardware gather–scatter mechanism does not eliminate the need for this transformation—gather– scatter accesses commonly need significantly higher bandwidth and latency than contiguous loads. Given an AOS data layout of struct {float x; float y; float z; float w;} a[4], consider a kernel operating on it as shown in Figure 16-15.

```txt
cgh.parallel_for<class aos<T>>(numOfItems,=[](id<1> wi) {
  x[wi] = a[wi].x;   // lead to gather x0, x1, x2, x3
  y[wi] = a[wi].y;   // lead to gather y0, y1, y2, y3
  z[wi] = a[wi].z;   // lead to gather z0, z1, z2, z3
  w[wi] = a[wi].w;   // lead to gather w0, w1, w2, w3
});
```

## Figure 16-15. SIMD gather in a kernel

When the compiler vectorizes the kernel along a set of work-items, it leads to SIMD gather instruction generation due to the need for non-unitstride memory accesses. For example, the stride of a[0].x, a[1].x, a[2].x, and a[3].x is 4, not a more efficient unit-stride of 1.

<table><tr><td> $\mathbf{w}_{3}$ </td><td> $\mathbf{z}_{3}$ </td><td> $\mathbf{y}_{3}$ </td><td> $\mathbf{x}_{3}$ </td><td> $\mathbf{w}_{2}$ </td><td> $\mathbf{z}_{2}$ </td><td> $\mathbf{y}_{2}$ </td><td> $\mathbf{x}_{2}$ </td><td> $\mathbf{w}_{1}$ </td><td> $\mathbf{z}_{1}$ </td><td> $\mathbf{y}_{1}$ </td><td> $\mathbf{x}_{1}$ </td><td> $\mathbf{w}_{0}$ </td><td> $\mathbf{z}_{0}$ </td><td> $\mathbf{y}_{0}$ </td><td> $\mathbf{x}_{0}$ </td></tr></table>

In a kernel, we can often achieve a higher SIMD efficiency by eliminating the use of memory gather–scatter operations. Some code benefits from a data layout change that converts data structures written in an Array-of-Struct (AOS) representation to a Structure-of-Arrays (SOA) representation, that is, having separate arrays for each structure field to keep memory accesses contiguous when SIMD vectorization is performed. For example, consider a SOA data layout of struct {float x[4]; float y[4]; float z[4]; float w[4];} a; as shown here:

<table><tr><td> $\mathbf{w}_{3}$ </td><td> $\mathbf{w}_{2}$ </td><td> $\mathbf{w}_{1}$ </td><td> $\mathbf{w}_{0}$ </td><td> $\mathbf{z}_{3}$ </td><td> $\mathbf{z}_{2}$ </td><td> $\mathbf{z}_{1}$ </td><td> $\mathbf{z}_{0}$ </td><td> $\mathbf{y}_{3}$ </td><td> $\mathbf{y}_{2}$ </td><td> $\mathbf{y}_{1}$ </td><td> $\mathbf{y}_{0}$ </td><td> $\mathbf{x}_{3}$ </td><td> $\mathbf{x}_{2}$ </td><td> $\mathbf{x}_{1}$ </td><td> $\mathbf{x}_{0}$ </td></tr></table>

A kernel can operate on the data with unit-stride (contiguous) vector loads and stores as shown in Figure 16-16, even when vectorized!

## Chapter 16 Programming for CPUs

```javascript
cgh.parallel_for<class aos<T>>(numOfItems, [=](id<1> wi) {
  x[wi] = a.x[wi];  // lead to unit-stride vector load x[0:4]
  y[wi] = a.y[wi];  // lead to unit-stride vector load y[0:4]
  z[wi] = a.z[wi];  // lead to unit-stride vector load z[0:4]
  w[wi] = a.w[wi];  // lead to unit-stride vector load w[0:4]
});
```

## Figure 16-16. SIMD unit-stride vector load in a kernel

The SOA data layout helps prevent gathers when accessing one field of the structure across the array elements and helps the compiler to vectorize kernels over the contiguous array elements associated with work-items. Note that such AOS-to-SOA or AOSOA data layout transformations are expected to be done at the program level (by us) considering all the places where those data structures are used. Doing it at just a loop level will involve costly transformations between the formats before and after the loop. However, we may also rely on the compiler to perform vectorload-and-shuffle optimizations for AOS data layouts with some cost. When a member of SOA (or AOS) data layout has a vector type, compiler vectorization may perform either horizontal expansion or vertical expansion based on underlying hardware to generate optimal code.

## Data Type Impact on SIMD Efficiency

C++ programmers often use integer data types whenever they know that the data fits into a 32-bit signed type, often leading to code such as

```lisp
int id = get_global_id(0); a[id] = b[id] + c[id];
```

However, given that the return type of the get\_global\_id(0) is size\_t (unsigned integer, often 64-bit), the conversion may reduce the optimization that a compiler can legally perform. This can then lead to SIMD gather/scatter instructions when the compiler vectorizes the code in the kernel, for example:

• Read of a[get\_global\_id(0)] may lead to a SIMD unit-stride vector load.

• Read of a[(int)get\_global\_id(0)] may lead to a nonunit-stride gather instruction.

This nuanced situation is introduced by the wraparound behavior (unspecified behavior and/or well-defined wraparound behavior in C++ standards) of data type conversion from size\_t to int (or uint), which is mostly a historical artifact from the evolution of C-based languages. Specifically, overflow across some conversions is undefined behavior, which allows the compiler to assume that such conditions never happen and to optimize more aggressively. Figure 16-17 shows some examples for those wanting to understand the details.

<table><tr><td>get_global_id(0)</td><td>a[(int)get_global_id(0)]</td><td>get_global_id(0)</td><td>a((uint)get_global_id(0)]</td></tr><tr><td>0x7FFFFFFFE</td><td>a[MAX_INT-1]</td><td>0xFFFFFFFE</td><td>a[MAX_UINT-1]</td></tr><tr><td>0x7FFFFFFF</td><td>a[MAX_INT (big positive)]</td><td>0xFFFFFFF</td><td>a[MAX_UINT]</td></tr><tr><td>0x80000000</td><td>a[MIN_INT (big negative)]</td><td>0x100000000</td><td>a[0]</td></tr><tr><td>0x80000001</td><td>a[MIN_INT+1]</td><td>0x100000001</td><td>a[1]</td></tr></table>

Figure 16-17. Examples of integer type value wraparound

SIMD gather/scatter instructions are slower than SIMD unit-stride vector load/store operations. To achieve an optimal SIMD efficiency, avoiding gathers/scatters can be critical for an application regardless of which programming language is used.

Most SYCL get\_\*\_id() family functions have the same detail, although many cases fit within MAX\_INT because the possible return values are bounded (e.g., the maximum id within a work-group). Thus, whenever legal, SYCL compilers can assume unit-stride memory addresses across the chunk of neighboring work-items to avoid gathers/scatters. For cases

that the compiler can’t safely generate linear unit-stride vector memory loads/stores because of possible overflow from the value of global IDs and/ or derivative value from global IDs, the compiler will generate gathers/ scatters.

Under the philosophy of delivering optimal performance for users, the DPC++ compiler assumes no overflow, and captures the reality almost all of the time in practice, so the compiler can generate optimal SIMD code to achieve good performance. However, a compiler option -fnosycl-id-queries-fit-in-int is provided by the DPC++ compiler for us to tell the compiler that there will be an overflow and that vectorized accesses derived from the id queries may not be safe. This can have large performance impact and should be used whenever unsafe to assume no overflow. The key takeaway is that a programmer should ensure the value of global ID fit in 32-bit int. Otherwise, the compiler option -fno-sycl-idqueries-fit-in-int should be used to guarantee program correctness, which may result in a lower performance.

## SIMD Execution Using single\_task

Under a single-task execution model, there are no work-items to vectorize over. Optimizations related to the vector types and functions may be possible, but this will depend on the compiler. The compiler and runtime are given a freedom either to enable explicit SIMD execution or to choose scalar execution within the single\_task kernel, and the result will depend on the compiler implementation.

C++ compilers may map vector types occurring inside of a single\_ task to SIMD instructions when compiling to CPU. The vec load, store, and swizzle functions perform operations directly on vector variables, informing the compiler that data elements are accessing contiguous data starting from the same (uniform) location in memory and enabling us to request optimized loads/stores of contiguous data. As discussed in

Chapter 11, this interpretation of vec is valid—however, we should expect this functionality to be deprecated, eventually, in favor of a more explicit vector type (e.g., std::simd) once available.

```cpp
queue q;

bool *resArray = malloc_shared<bool>(1, q);
resArray[0] = true;

q.single_task([=]) {
    sycl::vec<int, 4> old_v =
        sycl::vec<int, 4>(0, 100, 200, 300);
    sycl::vec<int, 4> new_v = sycl::vec<int, 4>();

    new_v.rgba() = old_v.abgr();
    int vals[] = {300, 200, 100, 0};

    if (new_v.r() != vals[0] || new_v.g() != vals[1] ||
        new_v.b() != vals[2] || new_v.a() != vals[3]) {
        resArray[0] = false;
    }
}).wait();
```

Figure 16-18. Using vector types and swizzle operations in the single\_task kernel

In the example shown in Figure 16-18, under single-task execution, a vector with three data elements is declared. A swizzle operation is performed with old\_v.abgr(). If a CPU provides SIMD hardware instructions for some swizzle operations, we may achieve some performance benefits of using swizzle operations in applications.

## SIMD VECTORIZATION GUIDELINES
