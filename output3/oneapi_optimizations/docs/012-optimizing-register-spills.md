## Optimizing Register Spills

The following techniques can reduce register pressure:

• Keep live ranges of private variables as short as possible.

Though the compiler schedules instructions and optimizes the distances, in some cases moving the loading and using the same variable closer or removing certain dependencies in the source can help the compiler do a better job.

• Avoid excessive loop unrolling.

Loop unrolling exposes opportunities for instruction scheduling optimization by the compiler and thus can improve performance. However, temporary variables introduced by unrolling may increase pressure on register allocation and cause register spilling. It is always a good idea to compare the performance with and without loop unrolling and different times of unrolls to decide if a loop should be unrolled or how many times to unroll it.

• Prefer USM pointers.

A buffer accessor takes more space than a USM pointer. If you can choose between USM pointers and buffer accessors, choose USM pointers.

• Recompute cheap-to-compute values on-demand that otherwise would be held in registers for a long time.

• Avoid big arrays or large structures, or break an array of big structures into multiple arrays of small structures.

For example, an array of sycl::float4:

```txt
``sycl::float4 v[8];
```

can be broken into 4 arrays of float:

```txt
``float x[8];
float y[8];
float z[8];
float w[8];``
```

All or part of the 4 arrays of float have a better chance to be allocated in registers than the array of sycl::float4.

• Break a large loop into multiple small loops to reduce the number of simultaneously live variables.

• Choose smaller sized data types if possible.

• Do not declare private variables as volatile.

• Do not take address of a private variable and later dereference the pointer

• Share registers in a sub-group.

• Use sub-group block load/store if possible.

• Use shared local memory.

The list here is not exhaustive.

The rest of this chapter shows how to apply these techniques, especially the last five, in real examples.
