# OpenMP-API-Specification Source Lines 14766-15455

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source OpenMP-API-Specification:L14766-L15455

Citation: [OpenMP-API-Specification:L14766-L15455]

````text
## 12.1.3 Controlling OpenMP Thread Affinity

When a thread encounters a parallel directive without a proc\_bind clause, the bind-var ICV is used to determine the policy for assigning threads to places within the input place partition, as defined in the following paragraph. If the parallel directive has a proc\_bind clause then the thread afinity policy specified by the proc\_bind clause overrides the policy specified by the first element of the bind-var ICV. Once a thread in the team is assigned to a place, the OpenMP implementation should not move it to another place.

If the encountering thread is a free-agent thread that is executing an explicit task that was created in an implicit parallel region, the input place partition for all thread afinity policies is the value of the place-partition-var ICV of the initial task. If the encountering thread is a free-agent thread that is executing an explicit task that was created in an explicit parallel region, the input place partition for all thread afinity policies is the input place partition of that parallel region. If the encountering thread is not a free-agent thread, the input place partition for all thread afinity policies is the value of the place-partition-var ICV of its binding implicit task.

Under the primary and close thread afinity policies, the place-partition-var ICV of each implicit task is assigned the input place partition. As discussed below, under the spread thread afinity policy, the place-partition-var ICV of each implicit task is derived from the value of the input place partition.

TABLE 12.1: Afinity-related Symbols used in this Section

<table><tr><td>Symbol</td><td>Symbol Description</td></tr><tr><td>L</td><td>the value of the thread-limit-var ICV</td></tr><tr><td>NG</td><td>the total number of place-assignment groups</td></tr><tr><td>gi</td><td>the  $i^{th}$  place-assignment group</td></tr><tr><td>P</td><td>the number of places in the input place partition</td></tr><tr><td>T</td><td>the number of threads in the team</td></tr><tr><td>AT</td><td> $\lceil T/NG \rceil$  (&quot;above-thread&quot; count)</td></tr><tr><td>BT</td><td> $\lfloor T/NG \rfloor$  (&quot;below-thread&quot; count)</td></tr><tr><td>ET</td><td>T mod NG (&quot;excess-thread&quot; count)</td></tr></table>

The place-assignment-var ICV is a list of L place numbers, where L is the value of the thread-limit-var ICV, that defines the place assignment of threads that participate in the execution of tasks bound to a given team. Any such thread corresponds to a position in the list, meaning it will be assigned to the place given by the place number at that position. If a thread is an assigned thread of the team with thread number i, it corresponds to position i in the place-assignment-var list. If a thread is a free-agent thread, it corresponds to the first position for which another thread has not yet been assigned to the associated place. If another thread is already assigned to the place associated with that position, the place to which the free-agent thread is assigned is implementation defined.

Each thread afinity policy determines how threads are assigned to places. A policy assigns each place in the input place partition to one of N G place-assignment groups, g<sub>0</sub>, . . . , g<sub>NG−1</sub>; additionally, it assigns each position from the place-assignment-var ICV to one of these groups. In a given group, the place number of each place is then assigned to a place-assignment-var position, in round robin fashion, starting with the first place. Threads are thus assigned to places according to the resulting place-assignment-var of the policy.

Under the primary thread afinity policy, NG = 1 and place-assignment group g<sub>0</sub> is assigned the place to which the encountering thread is assigned, and all positions of place-assignment-var are assigned to the same group. Thus, the corresponding threads of all positions of the place-assignment-var ICV are assigned to the same place as the primary thread.

For the close and spread thread afinity policies, let P be the number of places in the input place partition and let T be the number of assigned threads in the team. The following paragraphs describe how places in the input place partition are subdivided into place-assignment groups for these policies. A general description of how positions in place-assignment-var are assigned to these places, and thus how place assignment for threads under the policies is determined, then

follows these descriptions.

The close thread afinity policy distributes assignment of places evenly across a team of threads, while ensuring threads with consecutive numbers are assigned to the same place or adjacent places. Each place in the input place partition is assigned to one place-assignment group $( \mathsf { s o } , N G = P )$ Place-assignment group $g _ { 0 }$ is assigned the place to which the encountering thread is assigned. The place assigned to group $g _ { i }$ is then the next place in the place partition of the one assigned to group $g _ { i - 1 }$ , with wrap around with respect to the input place partition.

The spread thread afinity policy creates a sparse distribution for a team of $T$ threads among the $P$ places of the input place partition. $\mathbf { A }$ sparse distribution is achieved by first subdividing the input place partition into $T$ subpartitions if $T \leq P$ (in which case $N G = T )$ , or $P$ subpartitions if $T > P$ (in which case $N G = P )$ . The subpartitions are determined as follows:

$T \leq P$ : The input place partition is split into $T$ subpartitions, where each subpartition contains $\lfloor P / T \rfloor$ or $\lceil P / T \rceil$ consecutive places; if $P m o d T$ is not zero, which subpartitions contain $\lceil P / T \rceil$ places is implementation defined;

$T > P ;$ The input place partition is split into P subpartitions, each with a single place.

In either case, the places from each subpartition are assigned to a place-assignment group that corresponds to the subpartition. The subpartition that corresponds to group $g _ { 0 }$ is the one that includes the place on which the encountering thread is executing. The subpartition that corresponds to group $g _ { i }$ is the one that includes the next place to those in the subpartition corresponding to group $g _ { i - 1 }$ , with wrap around with respect to the input place partition. For a given implicit task and corresponding place-assignment-var position to its assigned thread, the place-partition-var ICV of the implicit task is set to the subpartition that corresponds to the group that includes the position. Thus, the subpartitioning is not only a mechanism for achieving a sparse distribution, it also defines a subset of places for a thread to use when creating a nested parallel region.

Let $A T$ equal $\lceil T / N G \rceil$ , BT equal $\lfloor T / N G \rfloor$ , and $E T$ equal $T$ mod NG. The close and the spread thread afinity policies assign the positions of the place-assignment-var ICV to place-assignment groups as follows.

• For positions from 0 up to $T - 1$ : The positions are partitioned into $N G$ sets of consecutive positions, $E T$ of which have $A T$ positions and $N G - E T$ of which have only $B T$ positions (when $E T$ is not zero, which sets have which count is implementation defined unless the thread afinity policy is close and $T < P$ , in which case the first $T$ groups are assigned the sets with $A T$ positions). The sets are assigned to each group, with the first set, starting at position $0 ,$ assigned to group $g _ { 0 }$ , and with each successive set $i ,$ starting at the position immediately after the last position in the set assigned to group $g _ { i - 1 }$ , assigned to the next group $_ { g _ { i } ; }$

• If $E T \neq 0$ , for the positions from $T$ up to $\left( A T * N G \right) - 1 \colon$ Each of these positions is assigned to a group $g _ { i }$ that received only $B T$ positions in the above step, such that each such $g _ { i }$ is then assigned $A T$ positions (which positions are assigned to which group is implementation defined);

• For the remaining positions from AT ∗ NG up to L: Each position is assigned to a group in round robin fashion, starting with the first group g<sub>0</sub>.

The determination of whether the thread afinity request can be fulfilled is implementation defined. If it cannot be fulfilled, then the afinity of threads in the team is implementation defined.

Note – Wrap around is needed if the end of a place partition is reached before all thread assignments are done. For example, wrap around may be needed in the case of close and T ≤ P , if the primary thread is assigned to a place other than the first place in the place partition. In this case, thread 1 is assigned to the place after the place of the primary thread, thread 2 is assigned to the place after that, and so on. The end of the place partition may be reached before all threads are assigned. In this case, assignment of threads is resumed with the first place in the place partition.

## Cross References

• bind-var ICV, see Table 3.1

• place-assignment-var ICV, see Table 3.1

• place-partition-var ICV, see Table 3.1

• thread-limit-var ICV, see Table 3.1

• parallel Construct, see Section 12.1

• proc\_bind Clause, see Section 12.1.4

12.1.4 proc\_bind Clause

<table><tr><td>Name: proc_bind</td><td>Properties: unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>affinity-policy</td><td>Keyword:close,primary,spread</td><td>default</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

parallel

## Semantics

The proc\_bind clause specifies the mapping of threads to places within the input place partition. The efect of the possible values for afinity-policy are described in Section 12.1.3

## Cross References

• Controlling OpenMP Thread Afinity, see Section 12.1.3

• parallel Construct, see Section 12.1

## 12.1.5 safesync Clause

<table><tr><td>Name: safesync</td><td>Properties: unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>width</td><td>expression of integer type</td><td>positive, optional</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

## parallel

## Semantics

The safesync clause determines whether two synchronizing threads in a team can make progress (see Section 1.2). The clause specifies that threads in the new team are partitioned, in thread number order, into progress groups of size width, except for the last progress group, which may contain less than width threads. Among threads that are executing tasks in the same contention group in parallel, only threads that are in the same progress group may execute in the same progress unit. If the width argument is not specified, the behavior is as if the width argument is one.

## Restrictions

Restrictions to the safesync clause are as follows:

• The width argument must be a safesync-compatible expression.

## Cross References

• parallel Construct, see Section 12.1

12.2 teams Construct

<table><tr><td>Name: teamsCategory: executable</td><td>Association: blockProperties: parallelism-generating, team-generating, thread-limiting, context-matching</td></tr></table>

## Clauses

allocate, default, firstprivate, if, num\_teams, private, reduction, shared, thread\_limit

## Binding

The binding thread set for a teams region is the encountering thread.

## Semantics

When a thread encounters a teams construct, a league of teams is created. Each team is an initial team, and the initial thread in each team executes the teams region. The number of teams created is determined by evaluating the if and num\_teams clauses. Once the teams are created, the number of initial teams are region-invariant , thus do not change for the duration of the teams region. Within a teams region, initial team numbers uniquely identify each initial team. Initial teams numbers are consecutive non-negative integers ranging from zero to one less than the number of initial teams.

When an if clause is present on a teams construct and the if clause expression evaluates to false, the number of formed teams is one. The use of a variable in an if clause expression of a teams construct causes an implicit reference to the variable in all enclosing constructs. The if clause expression is evaluated in the context outside of the teams construct.

If a thread\_limit clause is not present on the teams construct, but the construct is closely nested inside a target construct on which the thread\_limit clause is specified, the behavior is as if that thread\_limit clause is also specified for the teams construct.

The place list, given by the place-partition-var ICV of the encountering thread, is split into subpartitions in an implementation defined manner, and each team is assigned to a subpartition by setting the place-partition-var of its initial thread to the subpartition.

The teams construct sets the default-device-var ICV for each initial thread to an implementation defined value.

After the teams have completed execution of the teams region, the encountering task resumes execution of the enclosing task region.

## Execution Model Events

The teams-begin event occurs in a thread that encounters a teams construct before any initial task is generated for the corresponding teams region.

Upon generation of each initial task, an initial-task-begin event occurs in the thread that executes the initial task after the initial task is fully initialized but before the thread begins to execute the structured block of the teams construct.

If a new native thread is created for the league of teams that executes the teams region upon encountering the construct, a native-thread-begin event occurs as the first event in the context of the new thread prior to the initial-task-begin event.

When a thread completes an initial task, an initial-task-end event occurs in the thread.

The teams-end event occurs in the thread that encounters the teams construct after the thread executes its initial-task-end event but before it resumes execution of the encountering task.

If a native thread is destroyed at the end of a teams region, a native-thread-end event occurs in the initial thread that uses the native thread as the last event prior to destruction of the native thread.

## Tool Callbacks

A thread dispatches a registered parallel\_begin callback for each occurrence of a teams-begin event in that thread. The callback occurs in the task that encounters the teams construct. In the dispatched callback, (flags & ompt\_parallel\_league) evaluates to true.

A thread dispatches a registered implicit\_task callback with ompt\_scope\_begin as its endpoint argument for each occurrence of an initial-task-begin event in that thread. Similarly, a thread dispatches a registered implicit\_task callback with ompt\_scope\_end as its endpoint argument for each occurrence of an initial-task-end event in that thread. The callbacks occur in the context of the initial task. In the dispatched callback,

(flags & ompt\_task\_initial) and (flags & ompt\_task\_implicit) evaluate to true.

A thread dispatches a registered parallel\_end callback for each occurrence of a teams-end event in that thread. The callback occurs in the task that encounters the teams construct.

A thread dispatches a registered thread\_begin callback for each native-thread-begin event in that thread. The callback occurs in the context of the thread.

A thread dispatches a registered thread\_end callback for each native-thread-end event in that thread. The callback occurs in the context of the thread.

## Restrictions

Restrictions to the teams construct are as follows:

• If a reduction-modifier is specified in a reduction clause that appears on the directive then the reduction-modifier must be default.

• A teams region must be a strictly nested region of the implicit parallel region that surrounds the whole OpenMP program or a target region. If a teams region is nested inside a target region, the corresponding target construct must not contain any statements, declarations or directives outside of the corresponding teams construct.

• For a teams construct that is an immediately nested construct of a target construct, the bounds expressions of any array sections and the index expressions of any array elements used in any clause on the construct, as well as all expressions of any target-consistent clauses on the construct, must be target-consistent expressions.

• Only regions that are generated by teams-nestable constructs or teams-nestable routines may be strictly nested regions of teams regions.

## Cross References

• allocate Clause, see Section 8.6

• default Clause, see Section 7.5.1

• distribute Construct, see Section 13.7

• firstprivate Clause, see Section 7.5.4

• default-device-var ICV, see Table 3.1

• place-partition-var ICV, see Table 3.1

• if Clause, see Section 5.5

• implicit\_task Callback, see Section 34.5.3

• num\_teams Clause, see Section 12.2.1

• omp\_get\_num\_teams Routine, see Section 22.1

• omp\_get\_team\_num Routine, see Section 22.3

• parallel Construct, see Section 12.1

• parallel\_begin Callback, see Section 34.3.1

• parallel\_end Callback, see Section 34.3.2

• OMPT parallel\_flag Type, see Section 33.22

• private Clause, see Section 7.5.3

• reduction Clause, see Section 7.6.10

• OMPT scope\_endpoint Type, see Section 33.27

• shared Clause, see Section 7.5.2

• target Construct, see Section 15.8

• OMPT task\_flag Type, see Section 33.37

• thread\_begin Callback, see Section 34.1.3

• thread\_end Callback, see Section 34.1.4

• thread\_limit Clause, see Section 15.3

<table><tr><td colspan="2">Name: num_teams</td><td colspan="2">Properties: target-consistent, unique</td></tr><tr><td colspan="4">Arguments</td></tr><tr><td>Name</td><td>Type</td><td colspan="2">Properties</td></tr><tr><td>upper-bound</td><td>expression of integer type</td><td colspan="2">positive</td></tr><tr><td colspan="4">Modifiers</td></tr><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>lower-bound</td><td>upper-bound</td><td>OpenMP integer expression</td><td>positive, ultimate, unique</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

12.2.1 num\_teams Clause

## Directives

## teams

## Semantics

The num\_teams clause specifies the bounds on the number of teams formed by the construct on which it appears. lower-bound specifies the lower bound and upper-bound specifies the upper bound on the number of teams requested. If lower-bound is not specified, the efect is as if lower-bound is specified as equal to upper-bound. The number of teams formed is implementation defined, but it will be greater than or equal to the lower bound and less than or equal to the upper bound.

If the num\_teams clause is not specified on a construct then the efect is as if upper-bound was specified as follows. If the value of the nteams-var ICV is greater than zero, the efect is as if upper-bound was specified as an implementation defined value greater than zero but less than or equal to the value of the nteams-var ICV. Otherwise, the efect is as if upper-bound was specified as an implementation defined value greater than or equal to one.

## Restrictions

• lower-bound must be less than or equal to upper-bound.

## Cross References

• nteams-var ICV, see Table 3.1

• teams Construct, see Section 12.2

## 12.3 order Clause

<table><tr><td>Name: order</td><td>Properties: schedule-specification, unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>ordering</td><td>Keyword: concurrent</td><td>default</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>order-modifier</td><td>ordering</td><td>Keyword: reproducible, unconstrained</td><td>default</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

distribute, do, for, loop, simd

## Semantics

The order clause specifies an ordering of execution for the collapsed iterations of a loop-collapsing construct. If ordering is concurrent, diferent collapsed iterations may execute in any order, including in parallel, as if by the binding thread set of the region. The binding thread set may recruit or create additional native threads to participate in the parallel execution of any collapsed iterations.

The order-modifier on the order clause afects the schedule specification for the purpose of determining its consistency with other schedules (see Section 6.4.4). If order-modifier is reproducible, the loop schedule for the construct on which the clause appears is reproducible, whereas if order-modifier is unconstrained, the loop schedule is not reproducible.

## Restrictions

Restrictions to the order clause are as follows:

• The only routines for which a call may be nested inside a region that corresponds to a construct on which the order clause is specified with concurrent as the ordering argument are order-concurrent-nestable routines.

• Only regions that correspond to order-concurrent-nestable constructs or order-concurrent-nestable routines may be strictly nested regions of regions that correspond to constructs on which the order clause is specified with concurrent as the ordering argument.

• If a threadprivate variable is referenced inside a region that corresponds to a construct with an order clause that specifies concurrent, the behavior is unspecified.

## Cross References

• distribute Construct, see Section 13.7

• do Construct, see Section 13.6.2

• for Construct, see Section 13.6.1

• loop Construct, see Section 13.8

• simd Construct, see Section 12.4

## 12.4 simd Construct

<table><tr><td>Name: simdCategory: executable</td><td>Association: loop nestProperties: context-matching, order-concurrent-nestable, parallelism-generating, pure, simdizable</td></tr></table>

## Separating directives

scan

## Clauses

aligned, collapse, if, induction, lastprivate, linear, nontemporal, order, private, reduction, safelen, simdlen

## Binding

A simd region binds to the current task region. The binding thread set of the simd region is the current team.

## Semantics

The simd construct enables the execution of multiple collapsed iterations concurrently by using SIMD instructions. The number of collapsed iterations that are executed concurrently at any given time is implementation defined. Each concurrent iteration will be executed by a diferent SIMD lane. Each set of concurrent iterations is a SIMD chunk. Lexical forward dependences in the iterations of the original loop must be preserved within each SIMD chunk, unless an order clause that specifies concurrent is present.

When an if clause is present with an if-expression that evaluates to false, the preferred number of iterations to be executed concurrently is one, regardless of whether a simdlen clause is specified.

## Restrictions

Restrictions to the simd construct are as follows:

• If both simdlen and safelen clauses are specified, the value of the simdlen length must be less than or equal to the value of the safelen length.

• Only SIMDizable constructs may be encountered during execution of a simd region.

• If an order clause that specifies concurrent appears on a simd directive, the safelen clause must not also appear.

C / C++

• The simd region cannot contain calls to the longjmp or setjmp functions.

C / C++

C++

• No exceptions can be raised in the simd region.

• The only random access iterator types that are allowed for the collapsed loops are pointer types.

C++

## Cross References

• aligned Clause, see Section 7.12

• collapse Clause, see Section 6.4.5

• if Clause, see Section 5.5

• induction Clause, see Section 7.6.13

• lastprivate Clause, see Section 7.5.5

• linear Clause, see Section 7.5.6

• nontemporal Clause, see Section 12.4.1

• order Clause, see Section 12.3

• private Clause, see Section 7.5.3

• reduction Clause, see Section 7.6.10

• safelen Clause, see Section 12.4.2

• scan Directive, see Section 7.7

• simdlen Clause, see Section 12.4.3

## 12.4.1 nontemporal Clause

<table><tr><td>Name: nontemporal</td><td>Properties: default</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

simd

## Semantics

The nontemporal clause specifies that accesses to the storage locations to which the list items refer have low temporal locality across the logical iterations in which those storage locations are accessed. The list items of the nontemporal clause may also appear as list items of data-environment attribute clauses.

## Cross References

• simd Construct, see Section 12.4

## 12.4.2 safelen Clause

<table><tr><td>Name: safelen</td><td>Properties: unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>length</td><td>expression of integer type</td><td>positive, constant</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

simd

## Semantics

The safelen clause specifies that no two concurrent logical iterations within a SIMD chunk can have a distance in the collapsed iteration space that is greater than or equal to the length argument.

## Cross References

• simd Construct, see Section 12.4

## 12.4.3 simdlen Clause

<table><tr><td>Name: simdlen</td><td>Properties: unique</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>length</td><td>expression of integer type</td><td>positive, constant</td></tr></table>

## Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

declare\_simd, simd

## Semantics

When the simdlen clause appears on a simd construct, length is treated as a hint that specifies the preferred number of collapsed iterations to be executed concurrently. When the simdlen clause appears on a declare\_simd directive, if a SIMD version of the associated procedure is created, length corresponds to the number of concurrent arguments of the procedure.

Cross References

• declare\_simd Directive, see Section 9.8

• simd Construct, see Section 12.4

## 12.5 masked Construct

<table><tr><td>Name: maskedCategory: executable</td><td>Association: blockProperties: thread-limiting, thread-selecting</td></tr></table>

## Clauses

filter

## Binding

The binding thread set for a masked region is the current team. A masked region binds to the innermost enclosing parallel region.

## Semantics

The masked construct specifies a structured block that is executed by a subset of the threads of the current team. The filter clause selects a subset of the threads of the team that executes the binding parallel region to execute the structured block of the masked region. Other threads in the team do not execute the associated structured block. No implied barrier occurs either on entry to or exit from the masked construct. The result of evaluating the thread\_num argument of the filter clause may vary across threads.

If more than one thread in the team executes the structured block of a masked region, the structured block must include any synchronization required to ensure that data races do not occur.

## Execution Model Events

The masked-begin event occurs in any thread of a team that executes the masked region on entry to the region. The masked-end event occurs in any thread of a team that executes the masked region on exit from the region.

## Tool Callbacks

A thread dispatches a registered masked callback with ompt\_scope\_begin as its endpoint argument for each occurrence of a masked-begin event in that thread. Similarly, a thread dispatches a registered masked callback with ompt\_scope\_end as its endpoint argument for each occurrence of a masked-end event in that thread. These callbacks occur in the context of the task executed by the encountering thread.

## Cross References

• filter Clause, see Section 12.5.1

• masked Callback, see Section 34.3.3

• OMPT scope\_endpoint Type, see Section 33.27

## 12.5.1 filter Clause

<table><tr><td>Name: filter</td><td>Properties: unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>thread_num</td><td>expression of integer type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

## masked

## Semantics

If thread\_num specifies the thread number of the encountering thread in the current team then the filter clause selects the encountering thread. If the filter clause is not specified, the efect is as if the clause is specified with thread\_num equal to zero, so that the filter clause selects the primary thread. The use of a variable in a thread\_num argument expression causes an implicit reference to the variable in all enclosing constructs.

## Cross References

• masked Construct, see Section 12.5

# 13 Work-Distribution Constructs

A work-distribution construct distributes the execution of the corresponding region among the threads in its binding thread set. Threads execute portions of the region in the context of the implicit tasks that each thread is executing.

A work-distribution construct is a worksharing construct if the binding thread set is a team. A worksharing region has no barrier on entry. However, an implied barrier exists at the end of the worksharing region, unless a nowait clause is specified with do\_not\_synchronize specified as true, in which case an implementation may omit the barrier at the end of the worksharing region. In this case, threads that finish early may proceed straight to the instructions that follow the worksharing region without waiting for the other members of the team to finish the worksharing region, and without performing a flush operation.

If a work-distribution construct is a partitioned construct then all user code encountered in the region, but not in a nested region that is not a closely nested region, is executed by one thread from the binding thread set.

For loop-nest-associated constructs, the loop schedule is determined by a schedule specification for the construct, which is defined by schedule-specification clauses and (where applicable) the run-sched-var ICV. OpenMP programs can only depend on which thread executes a particular collapsed iteration if the construct specifies a reproducible schedule. Schedule reproducibility also determines whether constructs with the same schedule specification will have consistent schedules (see Section 6.4.4).

## Restrictions

The following restrictions apply to work-distribution constructs:

• Each work-distribution region must be encountered by all threads in the binding thread set or by none at all unless cancellation has been requested for the innermost enclosing parallel region.

• The sequence of encountered work-distribution regions that have the same binding thread set must be the same for every thread in the binding thread set.

• The sequence of encountered worksharing regions and barrier regions that bind to the same team must be the same for every thread in the team.

Fortran

• A variable must not be private within a teams or parallel region if it has either LOCAL\_INIT or SHARED locality in a DO CONCURRENT loop that is associated with a work-distribution construct, where the teams or parallel region is a binding region of the corresponding work-distribution region.

Fortran

## 13.1 single Construct

<table><tr><td>Name: singleCategory: executable</td><td>Association: blockProperties: work-distribution, team-executed, partitioned, worksharing, thread-limiting, thread-selecting</td></tr></table>

## Clauses

allocate, copyprivate, firstprivate, nowait, private

## Clause set

<table><tr><td>Properties: exclusive</td><td>Members: copyprivate, nowait</td></tr></table>

## Binding

The binding thread set for a single region is the current team. A single region binds to the innermost enclosing parallel region. Only the threads of the team that executes the binding paralle region participate in the execution of the structured block and the implied barrier of the single region if the barrier is not eliminated by a nowait clause.

## Semantics

The single construct specifies that the associated structured block is executed by only one of the threads in the team (not necessarily the primary thread), in the context of its implicit task. The method of choosing a thread to execute the structured block each time the team encounters the construct is implementation defined. An implicit barrier occurs at the end of a single region if the nowait clause does not specify otherwise.

## Execution Model Events

The single-begin event occurs after an implicit task encounters a single construct but before the task starts to execute the structured block of the single region. The single-end event occurs after an implicit task finishes execution of a single region but before it resumes execution of the enclosing region.

## Tool Callbacks

A thread dispatches a registered work callback with ompt\_scope\_begin as its endpoint argument for each occurrence of a single-begin event in that thread. Similarly, a thread dispatches a registered work callback with ompt\_scope\_end as its endpoint argument for each occurrence of a single-end event in that thread. For each of these callbacks, the work\_type argument is ompt\_work\_single\_executor if the thread executes the structured block associated with the single region; otherwise, the work\_type argument is ompt\_work\_single\_other.

## Cross References

• allocate Clause, see Section 8.6

• copyprivate Clause, see Section 7.8.2

• firstprivate Clause, see Section 7.5.4

• nowait Clause, see Section 17.6

• private Clause, see Section 7.5.3

• OMPT scope\_endpoint Type, see Section 33.27

• work Callback, see Section 34.4.1

• OMPT work Type, see Section 33.41

## 13.2 scope Construct

<table><tr><td>Name: scopeCategory: executable</td><td>Association: blockProperties: work-distribution, team-executed, worksharing, thread-limiting</td></tr></table>

## Clauses

allocate, firstprivate, nowait, private, reduction

## Binding

The binding thread set for a scope region is the current team. A scope region binds to the innermost enclosing parallel region. Only the threads of the team that executes the binding paralle region participate in the execution of the structured block and the implied barrier of the scope region if the barrier is not eliminated by a nowait clause.

## Semantics

The scope construct specifies that all threads in a team execute the associated structured block and any additionally specified OpenMP operations. An implicit barrier occurs at the end of a scope region if the nowait clause does not specify otherwise.

## Execution Model Events

The scope-begin event occurs after an implicit task encounters a scope construct but before the task starts to execute the structured block of the scope region. The scope-end event occurs after an implicit task finishes execution of a scope region but before it resumes execution of the enclosing region.

## Tool Callbacks

A thread dispatches a registered work callback with ompt\_scope\_begin as its endpoint argument and ompt\_work\_scope as its work\_type argument for each occurrence of a scope-begin event in that thread. Similarly, a thread dispatches a registered work callback with ompt\_scope\_end as its endpoint argument and ompt\_work\_scope as its work\_type argument for each occurrence of a scope-end event in that thread. The callbacks occur in the context of the implicit task.

## Cross References

• allocate Clause, see Section 8.6

• firstprivate Clause, see Section 7.5.4

• nowait Clause, see Section 17.6

• private Clause, see Section 7.5.3

• reduction Clause, see Section 7.6.10

• OMPT scope\_endpoint Type, see Section 33.27

• work Callback, see Section 34.4.1

• OMPT work Type, see Section 33.41

## 13.3 sections Construct

<table><tr><td>Name: sectionsCategory: executable</td><td>Association: blockProperties: work-distribution, team-executed, partitioned, worksharing, thread-limiting, cancellable</td></tr></table>

## Separating directives

section

## Clauses

allocate, firstprivate, lastprivate, nowait, private, reduction

## Binding

The binding thread set for a sections region is the current team. A sections region binds to the innermost enclosing parallel region. Only the threads of the team that executes the binding parallel region participate in the execution of the structured block sequences and the implied barrier of the sections region if the barrier is not eliminated by a nowait clause.

## Semantics

The sections construct is a non-iterative worksharing construct that contains a structured block that consists of a set of structured block sequences that are to be distributed among and executed by the threads in a team. Each structured block sequence is executed by one of the threads in the team in the context of its implicit task. An implicit barrier occurs at the end of a sections region if the nowait clause does not specify otherwise.

Each structured block sequence in the sections construct is preceded by a section subsidiary directive except possibly the first sequence, for which a preceding section subsidiary directive is optional. The method of scheduling the structured block sequences among the threads in the team is implementation defined.

## Execution Model Events

The sections-begin event occurs after an implicit task encounters a sections construct but before the task executes any structured block sequences of the sections region. The sections-end event occurs after an implicit task finishes execution of a sections region but before it resumes execution of the enclosing context.

## Tool Callbacks

A thread dispatches a registered work callback with ompt\_scope\_begin as its endpoint argument and ompt\_work\_sections as its work\_type argument for each occurrence of a sections-begin event in that thread. Similarly, a thread dispatches a registered work callback with ompt\_scope\_end as its endpoint argument and ompt\_work\_sections as its work\_type argument for each occurrence of a sections-end event in that thread. The callbacks occur in the context of the implicit task.

## Cross References

• allocate Clause, see Section 8.6

• firstprivate Clause, see Section 7.5.4

• lastprivate Clause, see Section 7.5.5

• nowait Clause, see Section 17.6

• private Clause, see Section 7.5.3

• reduction Clause, see Section 7.6.10

• OMPT scope\_endpoint Type, see Section 33.27

• section Directive, see Section 13.3.1

• work Callback, see Section 34.4.1

• OMPT work Type, see Section 33.41

## 13.3.1 section Directive

<table><tr><td>Name: sectionCategory: subsidiary</td><td>Association: separatingProperties: default</td></tr></table>

Separated directives sections

## Semantics

The section directive splits a structured block sequence that is associated with a sections construct into two structured block sequences.

## Execution Model Events

The section-begin event occurs before an implicit task starts to execute a structured block sequence in the sections construct for each of those structured block sequences that the task executes.

## Tool Callbacks

A thread dispatches a registered dispatch callback for each occurrence of a section-begin event in that thread. The callback occurs in the context of the implicit task.

## Cross References

• dispatch Callback, see Section 34.4.2

• sections Construct, see Section 13.3

Fortran
````
