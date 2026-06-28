
<table><tr><td>Name: atomicCategory: executable</td><td>Association: block : atomicProperties: mutual-exclusion, order-concurrent-nestable, simdizable</td></tr></table>

## Clause groups

atomic, extended-atomic, memory-order

## Clauses

hint, memscope

## Binding

The memscope clause determines the binding thread set for an atomic region. If the memscope clause is not present, the behavior is as if the memscope clause appeared on the construct with the device scope-specifier.

## Semantics

This section refers to the symbols defined for atomic structured blocks. The atomic construct ensures that a specific storage location is accessed atomically so that possible simultaneous reads and writes by multiple threads do not result in indeterminate values. An atomic region enforces exclusive access with respect to other atomic regions that access the same storage location x among all threads in the binding thread set without regard to the teams to which the threads belong.

An atomic construct with the read clause results in an atomic read of the storage location designated by x. An atomic construct with the write clause results in an atomic write of the storage location designated by x. An atomic construct with the update clause results in an atomic update of the storage location designated by x using the designated operator or intrinsic. Only the read and write of the storage location designated by x are performed mutually atomically. The evaluation of expr or expr-list need not be atomic with respect to the read or write of the storage location designated by x. No task scheduling points are allowed between the read and the write of the storage location designated by x.

If the capture clause is present, the atomic update is an atomic captured update — an atomic update to the storage location designated by x using the designated operator or intrinsic while also capturing the original or final value of the storage location designated by x with respect to the atomic update. The original or final value of the storage location designated by x is written in the storage location designated by v based on the base language semantics of atomic structured blocks of the atomic construct. Only the read and write of the storage location designated by x are performed mutually atomically. Neither the evaluation of expr or expr-list, nor the write to the storage location designated by v, need be atomic with respect to the read or write of the storage location designated by x.

If the compare clause is present, the atomic update is an atomic conditional update. For forms that use an equality comparison, the operation is an atomic compare-and-swap. It atomically compares the value of x to e and writes the value of d into the storage location designated by x if they are equal. Based on the base language semantics of the associated atomic structured block, the original or final value of the storage location designated by x is written to the storage location designated by v, which is allowed to be the same storage location as designated by e, or the result of the comparison is written to the storage location designated by r. Only the read and write of the storage location designated by x are performed mutually atomically. Neither the evaluation of either e or d nor writes to the storage locations designated by v and r need be atomic with respect to the read or write of the storage location designated by x.

## C / C++

If the compare clause is present, forms that use ordop are logically an atomic maximum or minimum, but they may be implemented with a compare-and-swap loop with short-circuiting. For forms where statement is cond-expr-stmt, if the result of the condition implies that the value of x does not change then the update may not occur.

If a memory-order clause is present, or implicitly provided by a requires directive, it specifies the efective memory ordering. Otherwise the efect is as if the relaxed memory-order clause is specified.

The atomic construct may be used to enforce memory consistency between threads, based on the guarantees provided by Section 1.3.6. A strong flush on the storage location designated by x is performed on entry to and exit from the atomic operation, ensuring that the set of all atomic operations applied to the same storage location in a race-free program has a total completion order. If the write or update clause is specified, the atomic operation is not an atomic conditional update for which the comparison fails, and the efective memory ordering is release, acq\_rel, or seq\_cst, the strong flush on entry to the atomic operation is also a release flush. If the read or update clause is specified and the efective memory ordering is acquire, acq\_rel, or seq\_cst then the strong flush on exit from the atomic operation is also an acquire flush. Therefore, if the efective memory ordering is not relaxed, release flushes and/or acquire flushes are implied and permit synchronization between the threads without the use of explicit flush directives.

For all forms of the atomic construct, any combination of two or more of these atomic constructs enforces mutually exclusive access to the storage locations designated by x among threads in the binding thread set. To avoid data races, all accesses of the storage locations designated by x that could potentially occur in parallel must be protected with an atomic construct.

atomic regions do not guarantee exclusive access with respect to any accesses outside of atomic regions to the same storage location x even if those accesses occur during a critical or ordered region, while a lock is owned by the executing task, or during the execution of a reduction clause.

However, other OpenMP synchronization can ensure the desired exclusive access. For example, a barrier that follows a series of atomic updates to x guarantees that subsequent accesses do not form a data race with the atomic accesses.

A compliant implementation may enforce exclusive access between atomic regions that update diferent storage locations. The circumstances under which this occurs are implementation defined

If the storage location designated by x is not size-aligned (that is, if the byte alignment of x is not a multiple of the size of x), then the behavior of the atomic region is implementation defined.

## Execution Model Events

The atomic-acquiring event occurs in the thread that encounters the atomic construct on entry to the atomic region before initiating synchronization for the region. The atomic-acquired event occurs in the thread that encounters the atomic construct after it enters the region, but before it executes the atomic structured block of the atomic region. The atomic-released event occurs in the thread that encounters the atomic construct after it completes any synchronization on exit from the atomic region.

![](images/1b5e2669d0cfe185b15bbed2e3dfcd56b3820eeac0aab83ea1dd8c8d02c85b59.jpg)

## Tool Callbacks

A thread dispatches a registered mutex\_acquire callback for each occurrence of an atomic-acquiring event in that thread. A thread dispatches a registered mutex\_acquired callback for each occurrence of an atomic-acquired event in that thread. A thread dispatches a registered mutex\_released callback with ompt\_mutex\_atomic as the kind argument if practical, although a less specific kind may be used, for each occurrence of an atomic-released event in that thread. These callbacks occurs in the task that encounters the atomic construct.

## Restrictions

Restrictions to the atomic construct are as follows:

• Constructs may not be encountered during execution of an atomic region.

• If a capture or compare clause is specified, the atomic clause must be update.

• If a capture clause is specified but the compare clause is not specified, an update-capture structured block must be associated with the construct.

• If both capture and compare clauses are specified, a conditional-update-capture structured block must be associated with the construct.

• If a compare clause is specified but the capture clause is not specified, a conditional-update structured block must be associated with the construct.

• If a write clause is specified, a write structured block must be associated with the construct.

• If a read clause is specified, a read structured block must be associated with the construct.

• If the atomic clause is read then the memory-order clause must not be release.

• If the atomic clause is write then the memory-order clause must not be acquire.

• The weak clause may only appear if the resulting atomic operation is an atomic conditional update for which the comparison tests for equality.

• All atomic accesses to the storage locations designated by x throughout the OpenMP program are required to have a compatible type.

• The fail clause may only appear if the resulting atomic operation is an atomic conditional update.

C / C++

Fortran

• All atomic accesses to the storage locations designated by x throughout the OpenMP program are required to have the same type and type parameters.

• The fail clause may only appear if the resulting atomic operation is an atomic conditional update or an atomic update where intrinsic-procedure-name is either MAX or MIN.

Fortran

## Cross References

• barrier Construct, see Section 17.3.1

• critical Construct, see Section 17.2

• flush Construct, see Section 17.8.6

• Lock Routines, see Chapter 28

• OpenMP Atomic Structured Blocks, see Section 6.3.3

• hint Clause, see Section 17.1

• memscope Clause, see Section 17.8.4

• OMPT mutex Type, see Section 33.20

• mutex\_acquire Callback, see Section 34.7.8

• mutex\_acquired Callback, see Section 34.7.12

• mutex\_released Callback, see Section 34.7.13

• ordered Construct, see Section 17.10

• requires Directive, see Section 10.5

## 17.8.6 flush Construct

<table><tr><td>Name: flushCategory:executable</td><td>Association: unassociatedProperties:default</td></tr></table>

## Arguments

flush(list)

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>optional</td></tr></table>

## Clause groups

memory-order

## Clauses

memscope

## Binding

The memscope clause determines the binding thread set for a flush region. If the memscope clause is not present the behavior is as if the memscope clause appeared on the construct with the device scope-specifier.

## Semantics

The flush construct executes the flush OpenMP operation. This operation makes the temporary view of the memory of a thread consistent with the memory and enforces an order on the memory operations of the variables explicitly specified or implied. Execution of a flush region afects the memory and it afects the temporary view of the memory of the encountering thread. It does not afect the temporary view of other threads. Other threads in the thread-set must themselves execute a flush in order to be guaranteed to observe the efects of the flush of the encountering thread. See the memory model description in Section 1.3 and the memscope clause description in Section 17.8.4 for more details on thread-sets.

If neither a memory-order clause nor a list argument appears on a flush construct then the behavior is as if the memory-order clause is seq\_cst.

A flush construct with the seq\_cst clause, executed on a given thread, operates as if all storage locations that are accessible to the thread are flushed by a strong flush; that is, the flush has the strong flush property. A flush construct with a list applies a strong flush to the items in the list, and the flush does not complete until the operation is complete for all specified list items. An implementation may implement a flush construct with a list by ignoring the list and treating it the same as a flush construct with the seq\_cst clause.

If no list items are specified, the flush operation has the release flush property and/or the acquire flush property:

• If the memory-order clause is seq\_cst or acq\_rel, the flush is both a release flush and an acquire flush.

• If the memory-order clause is release, the flush is a release flush.

• If the memory-order clause is acquire, the flush is an acquire flush.

![](images/8e7c8ead2ba840f39954b0c33c794959c9096b55f1ca88047b142d575977de66.jpg)

If a pointer is present in the list, the pointer itself is flushed, not the storage locations to which the pointer refers.

A flush construct without a list corresponds to a call to atomic\_thread\_fence, where the argument is given by the identifier that results from prefixing memory\_order\_ to the memory-order clause name.

For a flush construct without a list, the generated flush region implicitly performs the corresponding call to atomic\_thread\_fence. The behavior of an explicit call to atomic\_thread\_fence that occurs in an OpenMP program and does not have the argument memory\_order\_consume is as if the call is replaced by its corresponding flush construct.

## Fortran

If the list item or a subobject of the list item has the POINTER attribute, the allocation or association status of the POINTER item is flushed, but the pointer target is not. If the list item is of type C\_PTR, the variable is flushed, but the storage location that corresponds to that address is not flushed. If the list item or the subobject of the list item has the ALLOCATABLE attribute and has an allocation status of allocated, the allocated variable is flushed; otherwise the allocation status is flushed.

## Fortran

## Execution Model Events

The flush event occurs in a thread that encounters the flush construct.

## Tool Callbacks

A thread dispatches a registered flush callback for each occurrence of a flush event in that thread.

## Restrictions

Restrictions to the flush construct are as follows:

• If a memory-order clause is specified, the list argument must not be specified.

• The memory-order clause must not be relaxed.

## Cross References

• flush Callback, see Section 34.7.15

• memscope Clause, see Section 17.8.4

## 17.8.7 Implicit Flushes

Flushes implied when executing an atomic region are described in Section 17.8.5.

A flush region that corresponds to a flush directive with the release clause present is implied at the following locations:

• During a barrier region;

• At entry to a parallel region;

• At entry to a teams region;

• At exit from a critical region;

• During an omp\_unset\_lock region;

• During an omp\_unset\_nest\_lock region;

• During an omp\_fulfill\_event region;

• Immediately before every task scheduling point;

• At exit from the task region of each implicit task;

• At exit from an ordered region, if a threads clause or a doacross clause with a source task-dependence-type is present, or if no clauses are present; and

• During a cancel region, if the cancel-var ICV is true.

For a target construct, the thread-set of an implicit release flush that is performed in a target task during the generation of the target region and that is performed on exit from the initial task region that implicitly encloses the target region consists of the thread that executes the target task and the initial thread that executes the target region.

A flush region that corresponds to a flush directive with the acquire clause present is implied at the following locations:

• During a barrier region;

• At exit from a teams region;

• At entry to a critical region;

• If the region causes the lock to be set, during:

– an omp\_set\_lock region;

– an omp\_test\_lock region;

– an omp\_set\_nest\_lock region; and

– an omp\_test\_nest\_lock region;

• Immediately after every task scheduling point;

• At entry to the task region of each implicit task;

• At entry to an ordered region, if a threads clause or a doacross clause with a sink task-dependence-type is present, or if no clauses are present; and

• Immediately before a cancellation point, if the cancel-var ICV is true and cancellation has been activated.

For a target construct, the thread-set of an implicit acquire flush that is performed in a target task following the generation of the target region or that is performed on entry to the initial task region that implicitly encloses the target region consists of the thread that executes the target task and the initial thread that executes the target region.

Note – A flush region is not implied at the following locations:

• At entry to worksharing regions; and

• At entry to or exit from masked regions.

The synchronization behavior of implicit flushes is as follows:

• When a thread executes an atomic region for which the corresponding construct has the release, acq\_rel, or seq\_cst clause and specifies an atomic operation that starts a given release sequence, the release flush that is performed on entry to the atomic operation synchronizes with an acquire flush that is performed by a diferent thread and has an associated atomic operation that reads a value written by a modification in the release sequence.

• When a thread executes an atomic region for which the corresponding construct has the acquire, acq\_rel, or seq\_cst clause and specifies an atomic operation that reads a value written by a given modification, a release flush that is performed by a diferent thread and has an associated release sequence that contains that modification synchronizes with the acquire flush that is performed on exit from the atomic operation.

• When a thread executes a critical region that has a given name, the behavior is as if the release flush performed on exit from the region synchronizes with the acquire flush performed on entry to the next critical region with the same name that is performed by a diferent thread, if it exists.

• When a team executes a barrier region, the behavior is as if the release flush performed by each thread within the region, and the release flush performed by any other thread upon fulfilling the allow-completion event for a detachable task bound to the binding parallel region of the region, synchronizes with the acquire flush performed by all other threads within the region.

• When a thread executes a taskwait region that does not result in the creation of a dependent task and the task that encounters the corresponding taskwait construct has at least one child task, the behavior is as if each thread that executes a child task that is generated before the taskwait region performs a release flush upon completion of the associated structured block of the child task that synchronizes with an acquire flush performed in the taskwait region. If the child task is a detachable task, the thread that fulfills its allow-completion event performs a release flush upon fulfilling the event that synchronizes with the acquire flush performed in the taskwait region.

• When a thread executes a taskgroup region, the behavior is as if each thread that executes a remaining descendent task performs a release flush upon completion of the associated structured block of the descendent task that synchronizes with an acquire flush performed on exit from the taskgroup region. If the descendent task is a detachable task, the thread that fulfills its allow-completion event performs a release flush upon fulfilling the event that synchronizes with the acquire flush performed in the taskgroup region.

• When a thread executes an ordered region that does not arise from a stand-alone ordered directive, the behavior is as if the release flush performed on exit from the region synchronizes with the acquire flush performed on entry to an ordered region encountered in the next collapsed iteration to be executed by a diferent thread, if it exists.

• When a thread executes an ordered region that arises from a stand-alone ordered directive, the behavior is as if the release flush performed in the ordered region from a given source doacross iteration synchronizes with the acquire flush performed in all ordered regions executed by a diferent thread that are waiting for dependences on that doacross iteration to be satisfied.

• When a team begins execution of a parallel region, the behavior is as if the release flush performed by the primary thread on entry to the parallel region synchronizes with the acquire flush performed on entry to each implicit task that is assigned to a diferent thread.

• When an initial thread begins execution of a target region that is generated by a diferent thread from a target task, the behavior is as if the release flush performed by the generating thread in the target task synchronizes with the acquire flush performed by the initial thread on entry to its initial task region.

• When an initial thread completes execution of a target region that is generated by a diferent thread from a target task, the behavior is as if the release flush performed by the initial thread on exit from its initial task region synchronizes with the acquire flush performed by the generating thread in the target task.

• When a thread encounters a teams construct, the behavior is as if the release flush performed by the thread on entry to the teams region synchronizes with the acquire flush performed on entry to each initial task that is executed by a diferent initial thread that participates in the execution of the teams region.

• When a thread that encounters a teams construct reaches the end of the teams region, the behavior is as if the release flush performed by each diferent participating initial thread at exit from its initial task synchronizes with the acquire flush performed by the thread at exit from the teams region.

• When a task generates an explicit task that begins execution on a diferent thread, the behavior is as if the thread that is executing the generating task performs a release flush that synchronizes with the acquire flush performed by the thread that begins to execute the explicit task.

• When an undeferred task completes execution on a given thread that is diferent from the thread on which its generating task is suspended, the behavior is as if a release flush performed by the thread that completes execution of the associated structured block of the undeferred task synchronizes with an acquire flush performed by the thread that resumes execution of the generating task.

• When a dependent task with one or more antecedent tasks begins execution on a given thread, the behavior is as if each release flush performed by a diferent thread on completion of the associated structured block of a antecedent task synchronizes with the acquire flush performed by the thread that begins to execute the dependent task. If the antecedent task is a detachable task, the thread that fulfills its allow-completion event performs a release flush upon fulfilling the event that synchronizes with the acquire flush performed when the

dependent task begins to execute.

• When a task begins execution on a given thread and it is mutually exclusive with respect to another dependence-compatible task that is executed by a diferent thread, the behavior is as if each release flush performed on completion of the dependence-compatible task synchronizes with the acquire flush performed by the thread that begins to execute the task.

• When a thread executes a cancel region, the cancel-var ICV is true, and cancellation is not already activated for the specified region, the behavior is as if the release flush performed during the cancel region synchronizes with the acquire flush performed by a diferent thread immediately before a cancellation point in which that thread observes cancellation was activated for the region.

• When a thread executes an omp\_unset\_lock region that causes the specified lock to be unset, the behavior is as if a release flush is performed during the omp\_unset\_lock region that synchronizes with an acquire flush that is performed during the next omp\_set\_lock or omp\_test\_lock region to be executed by a diferent thread that causes the specified lock to be set.

• When a thread executes an omp\_unset\_nest\_lock region that causes the specified nestable lock to be unset, the behavior is as if a release flush is performed during the omp\_unset\_nest\_lock region that synchronizes with an acquire flush that is performed during the next omp\_set\_nest\_lock or omp\_test\_nest\_lock region to be executed by a diferent thread that causes the specified nestable lock to be set.

## 17.9 OpenMP Dependences
