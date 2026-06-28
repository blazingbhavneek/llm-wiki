
Figure 14-12. Using a user-defined reduction to find the location of the minimum value

## Group Algorithms

Support for parallel patterns in SYCL device code is provided by a separate library of group algorithms. These functions exploit the parallelism of a specific group of work-items (i.e., a work-group or a sub-group) to implement common parallel algorithms at limited scope and can be used as building blocks to construct other more complex algorithms.

The syntax of the group algorithms in SYCL is based on that of the algorithm library in C++, and any restrictions from the C++ algorithms apply. However, there is a critical difference: whereas the STL’s algorithms are called from sequential (host) code and indicate an opportunity for a library to employ parallelism, SYCL’s group algorithms are designed to be called within (device) code that is already executing in parallel. To ensure that this difference cannot be overlooked, the group algorithms have slightly different syntax and semantics to their C++ counterparts.

SYCL distinguishes between two different kinds of parallel algorithm. If an algorithm is performed collaboratively by all work-items in a group but otherwise behaves identically to an algorithm from the STL, the algorithm is named with a “joint” prefix (because the members of the group “join” together to perform the algorithm). Such algorithms read their inputs from memory and write their results to memory and can only operate on data in memory locations visible to all work-items in a given group. If an algorithm instead operates over an implicit range reflecting the group itself, with inputs and outputs stored in work-item private memory, the algorithm name is modified to include the word “group” (because the algorithm is performed directly on data owned to the group).

The code examples in Figure 14-13 demonstrate these two different kinds of algorithm, comparing the behavior of std::reduce to the behaviors of sycl::joint\_reduce and sycl::reduce\_over\_group.

## Chapter 14 Common Parallel Patterns

```txt
// std::reduce
// Each work-item reduces over a given input range
q.parallel_for(number_of_reductions, [=](size_t i) {
    output1[i] = std::reduce(
        input + i * elements_per_reduction,
        input + (i + 1) * elements_per_reduction);
}).wait();

// sycl::joint_reduce
// Each work-group reduces over a given input range
// The elements are automatically distributed over
// work-items in the group
q.parallel_for(nd_range<1>{number_of_reductions *
            elements_per_reduction,
            elements_per_reduction},
        [=](nd_item<1> it) {
            auto g = it.get_group();
            int sum = joint_reduce(
                g,
                input + g.get_group_id() *
                    elements_per_reduction,
                input + (g.get_group_id() + 1) *
                    elements_per_reduction,
                plus<>());
            if (g.leader()) {
                output2[g.get_group_id()] = sum;
            }
        })
    .wait();

// sycl::reduce_over_group
// Each work-group reduces over data held in work-item
// private memory. Each work-item is responsible for
// loading and contributing one value
q.parallel_for(
    nd_range<1>{
        number_of_reductions * elements_per_reduction,
        elements_per_reduction},
    [=](nd_item<1> it) {
        auto g = it.get_group();
        int x = input[g.get_group_id() *
                    elements_per_reduction +
                    g.get_local_id()];
        int sum = reduce_over_group(g, x, plus<>());
        if (g.leader()) {
            output3[g.get_group_id()] = sum;
        }
    })
    .wait();
```

Note that in both cases, the first argument to each group algorithm accepts a group or sub\_group object in place of an execution policy, to describe the set of work-items that should be used to perform the algorithm. Since algorithms are performed collaboratively by all the workitems in the specified group, they must also be treated similarly to a group barrier—all work-items in the group must encounter the same algorithm in converged control flow (i.e., all work-items in the group must similarly encounter or not encounter the algorithm call), and the arguments provided by all work-items must be such that all work-items agree on the operation being performed. For example, sycl::joint\_reduce requires all arguments to be the same for all work-items, to ensure that all workitems in the group operate on the same data and use the same operator to accumulate results.

The table in Figure 14-14 shows how the parallel algorithms available in the STL relate to the group algorithms, and whether there are any restrictions on the type of group that can be used. Note that in some cases, a group algorithm can only be used with sub-groups; these cases correspond to the “shuffle” operations introduced in earlier chapters.

<table><tr><td>C++ Algorithm</td><td>SYCL &quot;Joint&quot; Algorithm</td><td>SYCL &quot;Group&quot; Algorithm</td><td>Group Types</td></tr><tr><td>std::any of</td><td>sycl::joint any of</td><td>sycl::any of group</td><td>All</td></tr><tr><td>std::all of</td><td>sycl::joint all of</td><td>sycl::all of group</td><td>All</td></tr><tr><td>std::none_of</td><td>sycl::joint none_of</td><td>sycl::none_of_group</td><td>All</td></tr><tr><td>std::shift_left</td><td>N/A</td><td>sycl::shift_group_left</td><td>sub group</td></tr><tr><td>std::shift_right</td><td>N/A</td><td>sycl::shift_group_right</td><td>sub group</td></tr><tr><td>N/A</td><td>N/A</td><td>sycl::permute_group_by_xor</td><td>sub_group</td></tr><tr><td>N/A</td><td>N/A</td><td>sycl::select_from_group</td><td>sub group</td></tr><tr><td>std::reduce</td><td>sycl::joint_reduce</td><td>sycl::reduce_over_group</td><td>All</td></tr><tr><td>std::exclusive_scan</td><td>sycl::joint_exclusive_scan</td><td>sycl::exclusive_scan_over_group</td><td>All</td></tr><tr><td>std::inclusive_scan</td><td>sycl::joint_inclusive_scan</td><td>sycl::inclusive_scan_over_group</td><td>All</td></tr></table>

Figure 14-14. Mapping between C++ algorithms and SYCL group algorithms

## Chapter 14 Common Parallel Patterns

At the time of writing, the group algorithms are limited to supporting only primitive data types and a set of built-in operators recognized by SYCL (i.e., plus, multiplies, bit\_and, bit\_or, bit\_xor, logical\_and, logical\_or, minimum, and maximum). This is enough to cover most common use cases, but future versions of SYCL are expected to extend collective support to user-defined types and operators.

## Direct Programming

Although we recommend leveraging libraries wherever possible, we can learn a lot by looking at how each pattern could be implemented using “native” SYCL kernels.

The kernels in the remainder of this chapter should not be expected to reach the same level of performance as highly tuned libraries but are useful in developing a greater understanding of the capabilities of SYCL—and may even serve as a starting point for prototyping new library functionality.

## USE VENDOR-PROVIDED LIBRARIES!

When a vendor provides a library implementation of a function, it is almost always beneficial to use it rather than reimplementing the function as a kernel!
