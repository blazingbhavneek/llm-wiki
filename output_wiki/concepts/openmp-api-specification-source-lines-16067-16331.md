# OpenMP-API-Specification Source Lines 16067-16331

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source OpenMP-API-Specification:L16067-L16331

Citation: [OpenMP-API-Specification:L16067-L16331]

````text

This chapter defines directives and concepts related to explicit tasks.

## 14.1 task Construct

<table><tr><td>Name: taskCategory:executable</td><td>Association: blockProperties: parallelism-generating,thread-limiting, task-generating</td></tr></table>

## Clauses

affinity, allocate, default, depend, detach, final, firstprivate, if, in\_reduction, mergeable, priority, private, replayable, shared, threadset, transparent, untied

## Clause set

<table><tr><td>Properties: exclusive</td><td>Members: detach, mergeable</td></tr></table>

## Binding

The binding thread set of the task region is the set of threads specified in the threadset clause. A task region binds to the innermost enclosing parallel region.

## Semantics

When a thread encounters a task construct, an explicit task is generated from the code for the associated structured block. The data environment of the task is created according to the data-sharing attribute clauses on the task construct, per-data environment ICVs, and any defaults that apply. The data environment of the task is destroyed when the execution code of the associated structured block is completed.

The encountering thread may immediately execute the task, or defer its execution. In the latter case, any thread of the current binding thread set may be assigned the task. Task completion of the task can be guaranteed using task synchronization constructs and clauses. If a task construct is encountered during execution of an outer task, the generated task region that corresponds to this construct is not a part of the outer task region unless the generated task is an included task.

A detachable task is completed when the execution of its associated structured block is completed and the allow-completion event is fulfilled. If no detach clause is present on a task construct, the generated task is completed when the execution of its associated structured block is completed.

A thread that encounters a task scheduling point within the task region may temporarily suspend the task region.

The task construct includes a task scheduling point in the task region of its generating task, immediately following the generation of the explicit task. Each explicit task region includes a task scheduling point at the end of its associated structured block.

When storage is shared by an explicit task region, the programmer must ensure, by adding proper synchronization, that the storage does not reach the end of its lifetime before the explicit task region completes its execution.

When an if clause is present on a task construct and the if clause expression evaluates to false, an undeferred task is generated, and the encountering thread must suspend the current task region, for which execution cannot be resumed until execution of the structured block that is associated with the generated task is completed. The use of a variable in an if clause expression of a task construct causes an implicit reference to the variable in all enclosing constructs. The if clause expression is evaluated in the context outside of the task construct.

## Execution Model Events

The task-create event occurs when a thread encounters a task-generating construct. The event occurs after the task is initialized but before its execution begins and before the encountering thread resumes execution of any task.

## Tool Callbacks

A thread dispatches a registered task\_create callback for each occurrence of a task-create event in the context of the encountering task. The flags argument of this callback indicates the task types shown in Table 14.1.

TABLE 14.1: task\_create Callback Flags Evaluation

<table><tr><td>Operation</td><td>Evaluates to true</td></tr><tr><td>(flags &amp; empt_task_explicit)</td><td>Always in the dispatched callback</td></tr><tr><td>(flags &amp; empt_task_importing)</td><td>If the task is an importing task</td></tr><tr><td>(flags &amp; empt_task_exporting)</td><td>If the task is an exporting task</td></tr><tr><td>(flags &amp; empt_task_undeferred)</td><td>If the task is an undeferred task</td></tr><tr><td>(flags &amp; empt_task_final)</td><td>If the task is a final task</td></tr><tr><td>(flags &amp; empt_task_untied)</td><td>If the task is an untied task</td></tr><tr><td>(flags &amp; empt_task_mergeable)</td><td>If the task is a mergeable task</td></tr></table>

table continued on next page

table continued from previous page

## Operation

Evaluates to true

(flags & ompt\_task\_merged)

If the task is a merged task

## Cross References

• affinity Clause, see Section 14.10

• allocate Clause, see Section 8.6

• default Clause, see Section 7.5.1

• depend Clause, see Section 17.9.5

• detach Clause, see Section 14.11

• final Clause, see Section 14.7

• firstprivate Clause, see Section 7.5.4

• Task Scheduling, see Section 14.14

• if Clause, see Section 5.5

• in\_reduction Clause, see Section 7.6.12

• mergeable Clause, see Section 14.5

• omp\_fulfill\_event Routine, see Section 23.2.1

• priority Clause, see Section 14.9

• private Clause, see Section 7.5.3

• replayable Clause, see Section 14.6

• shared Clause, see Section 7.5.2

• task\_create Callback, see Section 34.5.1

• OMPT task\_flag Type, see Section 33.37

• threadset Clause, see Section 14.8

• transparent Clause, see Section 17.9.6

• untied Clause, see Section 14.4

14.2 taskloop Construct

<table><tr><td>Name: taskloopCategory:executable</td><td>Association: loop nestProperties: parallelism-generating, SIMD-partitionable, task-generating</td></tr></table>

## Subsidiary directives

## Clauses

allocate, collapse, default, final, firstprivate, grainsize, if, in\_reduction, induction, lastprivate, mergeable, nogroup, num\_tasks, priority, private, reduction, replayable, shared, threadset, transparent, untied

<table><tr><td>Properties: exclusive</td><td>Members: nogroup, reduction</td></tr></table>

<table><tr><td>Properties: exclusive</td><td>Members: grainsize, num_tasks</td></tr></table>

## Binding

The binding thread set of the taskloop region is the set of threads specified in the threadset clause. A taskloop region binds to the innermost enclosing parallel region.

## Semantics

When a thread encounters a taskloop construct, the construct partitions the collapsed iterations into chunks, each of which is assigned to an explicit task for parallel execution. The data environment of each generated task is created according to the data-sharing attribute clauses on the taskloop construct, per-data environment ICVs, and any defaults that apply. Tasks created by a taskloop directive can be afected by task\_iteration directives that are subsidiary directives of that taskloop directive. If a task\_iteration directive on which a depend clause appears is a subsidiary directive of the taskloop construct then the behavior is as if the order of the creation of the generated tasks is in increasing collapsed iteration order with respect to their assigned chunks. Otherwise, the order of the creation of the generated tasks is unspecified and programs that rely on the execution order of the logical iterations are non-conforming.

If the nogroup clause is not present, the taskloop construct executes as if it was enclosed in a taskgroup construct with no statements or directives outside of the taskloop construct. Thus, the taskloop construct creates an implicit taskgroup region. If the nogroup clause is present, no implicit taskgroup region is created.

If a reduction clause is present, the behavior is as if a task\_reduction clause with the same reduction identifier and list items was applied to the implicit taskgroup construct that encloses the taskloop construct. The taskloop construct executes as if each generated task was defined by a task construct on which an in\_reduction clause with the same reduction identifier and list items is present. Thus, the generated tasks are participants of the reduction defined by the task\_reduction clause that was applied to the implicit taskgroup construct.

If an in\_reduction clause is present, the behavior is as if each generated task was defined by a task construct on which an in\_reduction clause with the same reduction identifier and list items is present. Thus, the generated tasks are participants of a reduction previously defined by a reduction-scoping clause.

If a threadset clause is present, the behavior is as if each generated task was defined by a task construct on which a threadset clause with the same set of threads is present. Thus, the binding thread set of the generated tasks is the same as that of the taskloop region.

If a transparent clause is present, the behavior is as if each generated task was defined by a task construct on which a transparent clause with the same impex-type argument is present.

If no clause from the granularity-clause clause set is present, the number of loop tasks generated and the number of logical iterations assigned to these tasks is implementation defined.

When an if clause is present and the if clause expression evaluates to false, undeferred tasks are generated. The use of a variable in an if clause expression causes an implicit reference to the variable in all enclosing constructs.

![](images/3edb613c1eb7a56d936c8dad13f80d2dde6fd087a9cab73d3d680c9dc2de4e91.jpg)

For firstprivate variables of class type, the number of invocations of copy constructors that perform the initialization is implementation defined.

![](images/cff68d8b96f60fbcd2a8b4896f7934f0583c7dbf15f105c0aadcec9b65843742.jpg)

When storage is shared by a taskloop region, the programmer must ensure, by adding proper synchronization, that the storage does not reach the end of its lifetime before the taskloop region and its descendent tasks complete their execution.

## Execution Model Events

The taskloop-begin event occurs upon entering the taskloop region. A taskloop-begin will precede any task-create events for the generated tasks. The taskloop-end event occurs upon completion of the taskloop region.

Events for an implicit taskgroup region that surrounds the taskloop region are the same as for the taskgroup construct.

The taskloop-iteration-begin event occurs at the beginning of each logical-iteration of a taskloop region before an explicit task executes the logical iteration. The taskloop-chunk-begin event occurs before an explicit task executes any of its associated logical iterations in a taskloop region.

## Tool Callbacks

A thread dispatches a registered work callback for each occurrence of a taskloop-begin and taskloop-end event in that thread. The callback occurs in the context of the encountering task. The callback receives ompt\_scope\_begin or ompt\_scope\_end as its endpoint argument, as appropriate, and ompt\_work\_taskloop as its work\_type argument.

A thread dispatches a registered dispatch callback for each occurrence of a taskloop-iteration-begin or taskloop-chunk-begin event in that thread. The callback binds to the explicit task executing the logical iterations.

## Restrictions

Restrictions to the taskloop construct are as follows:

• The reduction-modifier must be default.

• The conditional lastprivate-modifier must not be specified.

• If the taskloop construct is associated with a task\_iteration directive, none of the taskloop-afected loops may be the generated loop of a loop-transforming construct.

## Cross References

• allocate Clause, see Section 8.6

• collapse Clause, see Section 6.4.5

• default Clause, see Section 7.5.1

• dispatch Callback, see Section 34.4.2

• final Clause, see Section 14.7

• firstprivate Clause, see Section 7.5.4

• Canonical Loop Nest Form, see Section 6.4.1

• grainsize Clause, see Section 14.2.1

• if Clause, see Section 5.5

• in\_reduction Clause, see Section 7.6.12

• induction Clause, see Section 7.6.13

• lastprivate Clause, see Section 7.5.5

• mergeable Clause, see Section 14.5

• nogroup Clause, see Section 17.7

• num\_tasks Clause, see Section 14.2.2

• priority Clause, see Section 14.9

• private Clause, see Section 7.5.3

• reduction Clause, see Section 7.6.10

• replayable Clause, see Section 14.6

• OMPT scope\_endpoint Type, see Section 33.27

• shared Clause, see Section 7.5.2

• task Construct, see Section 14.1

• task\_iteration Directive, see Section 14.2.3

• taskgroup Construct, see Section 17.4

• threadset Clause, see Section 14.8

• transparent Clause, see Section 17.9.6

• untied Clause, see Section 14.4

• work Callback, see Section 34.4.1

• OMPT work Type, see Section 33.41

## 14.2.1 grainsize Clause

<table><tr><td>Name: grainsize</td><td>Properties: taskgraph-altering, unique</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>grain-size</td><td>expression of integer type</td><td>positive</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>prescriptiveness</td><td>grain-size</td><td>Keyword: strict</td><td>unique</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

taskloop

## Semantics

The grainsize clause specifies the number of logical iterations, $L _ { t }$ , that are assigned to each generated task t. If prescriptiveness is not specified as strict, other than possibly for the generated task that contains the sequentially last iteration, $L _ { t }$ is greater than or equal to the minimum of the value of the grain-size expression and the number of logical iterations, but less than two times the value of the grain-size expression. If prescriptiveness is specified as strict, other

## Arguments

than possibly for the generated task that contains the sequentially last iteration, $L _ { t }$ is equal to the value of the grain-size expression. In both cases, the generated task that contains the sequentially last iteration may have fewer logical iterations than the value of the grain-size expression.

## Restrictions

Restrictions to the grainsize clause are as follows:

• None of the collapsed loops may be non-rectangular loops.

## Cross References

• taskloop Construct, see Section 14.2
````
