# Choosing a Data Management Strategy

Selecting the right data management strategy for our applications is largely a matter of personal preference. Indeed, we may begin with one strategy and switch to another as our program matures. However, there are a few useful guidelines to help us to pick a strategy that will serve our needs.

The first decision to make is whether we want to use explicit or implicit data movement since this greatly affects what we need to do to our program. Implicit data movement is generally an easier place to start because all the data movement is handled for us, letting us focus on expression of the computation.

If we decide that we’d rather have full control over all data movement from the beginning, then explicit data movement using USM device allocations is where we want to start. We just need to be sure to add all the necessary copies between host and devices!

When selecting an implicit data movement strategy, we still have a choice of whether to use buffers or USM host or shared pointers. Again, this choice is a matter of personal preference, but there are a few questions that could help guide us to one over the other. If we’re porting an existing C/C++ program that uses pointers, USM might be an easier path since most code won’t need to change. If data representation hasn’t guided us to a preference, another question we can ask is how we would like to express our dependences between kernels. If we prefer to think about data dependences between kernels, choose buffers. If we prefer to think about dependences as performing one computation before another and want to express that using an in-order queue or with explicit events or waiting between kernels, choose USM.

When using USM pointers (with either explicit or implicit data movement), we have a choice of which type of queue we want to use. Inorder queues are simple and intuitive, but they constrain the runtime and may limit performance. Out-of-order queues are more complex, but they give the runtime more freedom to reorder and overlap execution. The outof-order queue class is the right choice if our program will have complex dependences between kernels. If our program simply runs many kernels one after another, then an in-order queue will be a better option for us.

## Handler Class: Key Members

We have shown a number of ways to use the handler class. Figures 3-17 and 3-18 provide a more detailed explanation of the key members of this very important class. We have not yet used all these members, but they will be used later in the book. This is as good a place as any to lay them out.

A closely related class, the queue class, is similarly explained at the end of Chapter 2.

## Chapter 3 Data Managem ent

```cpp
class handler {
    ...
        // Specifies event(s) that must be complete before the
        // action defined in this command group executes.
        void depends_on({event / std::vector<event> & });

    // Enqueues a memcpy from Src to Dest.
    // Count bytes are copied.
    void memcpy(void* Dest, const void* Src, size_t Count);

    // Enqueues a memcpy from Src to Dest.
    // Count elements are copied.
    template <typename T>
    void copy(const T* Src, T* Dest, size_t Count);

    // Enqueues a memset operation on the specified pointer.
    // Writes the first byte of Value into Count bytes.
    void memset(void* Ptr, int Value, size_t Count)

        // Enques a fill operation on the specified pointer.
        // Fills Pattern into Ptr Count times.
        template <typename T>
        void fill(void* Ptr, const T& Pattern, size_t Count);

    // Submits a kernel of one work-item for execution.
    template <typename KernelName, typename KernelType>
    void single_task(KernelType KernelFunc);

    // Submits a kernel with NumWork-items work-items for
    // execution.
    template <typename KernelName, typename KernelType,
            int Dims>
    void parallel_for(range<Dims> NumWork - items,
            KernelType KernelFunc);

    // Submits a kernel for execution over the supplied
    // nd_range.
    template <typename KernelName, typename KernelType,
            int Dims>
    void parallel_for(nd_range<Dims> ExecutionRange,
            KernelType KernelFunc);
    ...
};
```

## Figure 3-17. Simplified definition of the non-accessor members of the handler class

```cpp
class handler {
...
// Specifies event(s) that must be complete before the
// action. Copy to/from an accessor.
// Valid combinations:
// Src: accessor,   Dest: shared_ptr
// Src: accessor,   Dest: pointer
// Src: shared_ptr  Dest: accessor
// Src: pointer      Dest: accessor
// Src: accessor   Dest: accessor
template <typename T_Src, typename T_Dst, int Dims,
       access::mode AccessMode,
       access::target AccessTarget,
       access::placeholder IsPlaceholder =
         access::placeholder::false_t>
void copy(accessor<T_Src, Dims, AccessMode,
           AccessTarget, IsPlaceholder> Src,
       shared_ptr_class<T_Dst> Dst);
void copy(shared_ptr_class<T_Src> Src,
       accessor<T_Dst, Dims, AccessMode, AccessTarget,
           IsPlaceholder>
           Dst);
void copy(accessor<T_Src, Dims, AccessMode, AccessTarget,
           IsPlaceholder> Src,
       T_Dst *Dst);
void copy(const T_Src *Src,
       accessor<T_Dst, Dims, AccessMode, AccessTarget,
           IsPlaceholder> Dst);
template <typename T_Src, int Dims_Src,
       access::mode AccessMode_Src,
       access::target AccessTarget_Src, typename T_Dst,
       int Dims_Dst, access::mode AccessMode_Dst,
       access::target AccessTarget_Dst,
       access::placeholder IsPlaceholder_Src =
          access::placeholder::false_t,
       access::placeholder IsPlaceholder_Dst =
          access::placeholder::false_t>
void copy(accessor<T_Src, Dims_Src, AccessMode_Src,
           AccessTarget_Src, IsPlaceholder_Src> Src,
       accessor<T_Dst, Dims_Dst, AccessMode_Dst,
           AccessTarget_Dst, IsPlaceholder_Dst> Dst);

// Provides a guarantee that the memory object accessed by
// the accessor is updated on the host after this action
// executes.
template <typename T, int Dims, access::mode AccessMode,
       access::target AccessTarget,
       access::placeholder IsPlaceholder =
         access::placeholder::false_t>
void update_host(accessor<T, Dims, AccessMode,
               AccessTarget, IsPlaceholder> Acc);
...
```

Figure 3-18. Simplified definition of the accessor members of the handler class

## Summary

In this chapter, we have introduced the mechanisms that address the problems of data management and how to order the uses of data. Managing access to different memories is a key challenge when using accelerator devices, and we have different options to suit our needs.

We provided an overview of the different types of dependences that can exist between the uses of data, and we described how to provide information about these dependences to queues so that they properly order tasks.

This chapter provided an overview of Unified Shared Memory and buffers. We explore all the modes and behaviors of USM in greater detail in Chapter 6. Chapter 7 explores buffers more deeply, including all the different ways to create buffers and control their behavior. Chapter 8 revisits the scheduling mechanisms for queues that control the ordering of kernel executions and data movements.

![](images/cf2dc683e61d8404c18cd191b29a9ff1f49210d0cceadb4df8a82dad8d009983.jpg)

Open Access This chapter is licensed under the terms of the Creative Commons Attribution 4.0 International License

(https://creativecommons.org/licenses/by/4.0/), which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license and indicate if changes were made.

The images or other third party material in this chapter are included in the chapter’s Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the chapter’s Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.
