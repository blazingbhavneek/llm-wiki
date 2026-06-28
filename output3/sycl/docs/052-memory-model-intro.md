
cc 1 Open Access This chapter is licensed under the terms of BY the Creative Commons Attribution 4.0 International License (https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.

# Memory Model and Atomics

Memory consistency is not an esoteric concept if we want to be parallel programmers. It helps us to ensure that data is where we need it, when we need it, and that its values are what we are expecting. This chapter brings to light key things we need to master to ensure our program hums along correctly. This topic is not unique to SYCL.

Having a basic understanding of the memory (consistency) model of a programming language is necessary for any programmer who wants to allow concurrent updates to memory (whether those updates originate from multiple work-items in the same kernel, multiple devices, or both). This is true regardless of how memory is allocated, and the content of this chapter is equally important to us whether we choose to use buffers or USM allocations.

In previous chapters, we have focused on the development of simple kernels, where work-items either operate on completely independent data or share data using structured communication patterns that can be expressed directly using language and/or library features. As we move toward writing more complex and realistic kernels, we are likely to encounter situations where work-items may need to communicate in less structured ways—understanding how the memory model relates to SYCL language features and the capabilities of the hardware we are targeting is a necessary precondition for designing correct, portable, and efficient programs.

## THREADS OF EXECUTION

C++17 introduced the concept of a “thread of execution” (often referred to simply as a “thread”) to help describe the behaviors of library features related to parallelism and concurrency (e.g., the parallel algorithms). The C++ memory consistency model and execution model are defined entirely in terms of interactions between these “threads.”

To simplify comparison between SYCL and C++, this chapter often uses the term “thread” to mean “thread of execution.” A SYCL work-item is equivalent to a C++ thread of execution with weakly parallel forward progress guarantees, and so it is safe to use these terms interchangeably— occasionally, we may still use “work-item” to highlight when we are discussing SYCL-specific concepts.

The memory consistency model of C++ is sufficient for writing applications that execute entirely on the host, but it is modified by SYCL in order to address complexities that may arise when programming heterogeneous systems. Specifically, we need to be able to

• Reason about which types of memory allocation (buffers and USM) can be accessed by which devices in the system

• Prevent unsafe concurrent memory accesses (data races) during the execution of our kernels by using barriers and atomics

• Enable safe communication between work-items using barriers, fences, atomics, memory orders, and memory scopes

Prevent optimizations that may unexpectedly alter the behavior of parallel applications—while still allowing other optimizations—using barriers, fences, atomics, memory orders, and memory scopes

Memory models are a complex topic, but for a good reason—processor architects care about making processors and accelerators execute our codes as efficiently as possible! We have worked hard in this chapter to break down this complexity and highlight the most critical concepts and language features. This chapter starts us down the path of not only knowing the memory model inside and out but also enjoying an important aspect of parallel programming that many people do not know exists. If questions remain after reading the descriptions and example codes here, we highly recommend visiting the websites listed at the end of this chapter or referring to the C++ and SYCL specifications.

## What’s in a Memory Model?

This section expands upon the motivation for programming languages to contain a memory model and introduces a few core concepts that parallel programmers should familiarize themselves with:

• Data races and synchronization

• Barriers and fences

• Atomic operations

• Memory ordering

Understanding these concepts at a high level is necessary to appreciate their expression and usage in C++ with SYCL. Readers with extensive experience in parallel programming, especially using C++, may wish to skip ahead.

## Data Races and Synchronization

The operations that we write in our programs typically do not map directly to a single hardware instruction or micro-operation. A simple addition operation such as data[i] += x may be broken down into a sequence of several instructions or micro-operations:

• Load data[i] from memory into a temporary (register).

• Compute the result of adding x to data[i].

• Store the result back to data[i].

This is not something that we need to worry about when developing sequential applications—the three stages of the addition will be executed in the order that we expect, as depicted in Figure 19-1.

![](images/187a5f1c6078b2e44728317882eece520d313ddbcdcfbaa666dba1365eacdabb.jpg)  
Figure 19-1. Sequential execution of data[i] += x broken into three separate operations

Switching to parallel application development introduces an extra level of complexity: if we have multiple operations being applied to the same data concurrently, how can we be certain that their view of that data is consistent? Consider the situation shown in Figure 19-2, where two executions of data[i] += x have been interleaved on two threads. If the two threads use different values of i, the application will execute correctly. If they use the same value of i, both load the same value from memory, and one of the results is overwritten by the other! This is just one of many ways in which their operations could be scheduled, and the behavior of our application depends on which thread gets to which data first—our application contains a data race.

![](images/2bf44b0e2bf198e40d075c32c37a93b3ea22ea67c9297812798746e317ad5a82.jpg)  
Figure 19-2. One possible interleaving of data[i] += x executed concurrently

The code in Figure 19-3 and its output in Figure 19-4 show how easily this can happen in practice. If M is greater than or equal to N, the value of j used by each thread is unique; if it is not, values of j will conflict, and updates may be lost. We say may be lost because a program containing a data race could still produce the correct answer some or all the time (depending on how work is scheduled by the implementation and hardware). Neither the compiler nor the hardware can possibly know

what this program is intended to do or what the values of N and M may be at runtime—it is our responsibility as programmers to understand whether our programs may contain data races and whether they are sensitive to execution order.

```cpp
int* data = malloc_shared<int>(N, q);
std::fill(data, data + N, 0);

q.parallel_for(N, [=](id<1> i) {
    int j = i % M;
    data[j] += 1;
}).wait();

for (int i = 0; i < N; ++i) {
    std::cout << "data [" << i << "] = " << data[i] << "\n";
}
```

Figure 19-3. Kernel containing a data race

```txt
N = 2, M = 2:
data [0] = 1
data [1] = 1

N = 2, M = 1:
data [0] = 1
data [1] = 0
```

Figure 19-4. Sample output of the code in Figure 19-3 for small values of N and M

In general, when developing massively parallel SYCL applications, we should not concern ourselves with the exact order in which individual work-items execute—there are hopefully hundreds (or thousands!) of work-items in each of our kernels, and trying to impose a specific ordering upon them will negatively impact both scalability and performance. Rather, our focus should be on developing portable applications that execute correctly, which we can achieve by providing the compiler (and hardware) with information about when work-items share data, what guarantees are needed when sharing occurs, and which execution orderings are legal.

Massively parallel applications should not be concerned with the exact order in which individual work-items execute!

## Barriers and Fences

One way to prevent data races between work-items in the same group is to introduce synchronization across different threads using work-group barriers and appropriate memory fences. We could use a work-group barrier to order our updates of data[i] as shown in Figure 19-5, and an updated version of our example kernel is given in Figure 19-6. Note that because a work-group barrier does not synchronize work-items in different groups, our simple example is only guaranteed to execute correctly if we limit ourselves to a single work-group!

![](images/4357c3cbda9e9391071396f6882f1cf534f798a10474ecbdf51e59f6eb151a1f.jpg)  
Figure 19-5. Two executions of data[i] += x separated by a barrier

## Chapt er 19 Memory Model and At omics

```cpp
int* data = malloc_shared<int>(N, q);
std::fill(data, data + N, 0);

// Launch exactly one work-group
// Number of work-groups = global / local
range<1> global{N};
range<1> local{N};

q.parallel_for(nd_range<1>{global, local},
            [=](nd_item<1> it) {
                int i = it.get_global_id(0);
                int j = i % M;
                for (int round = 0; round < N; ++round) {
                    // Allow exactly one work-item update
                    // per round
                    if (i == round) {
                        data[j] += 1;
                    }
                    group_barrier(it.get_group());
                }
            })
        .wait();

for (int i = 0; i < N; ++i) {
    std::cout << "data [" << i << "] = " << data[i] << "\n";
}
```
