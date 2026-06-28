
<table><tr><td>Name: bind</td><td>Properties: unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>binding</td><td>Keyword: parallel,teams, thread</td><td>default</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

loop

## Semantics

The bind clause specifies the binding region of the construct on which it appears. Specifically, if binding is teams and an innermost enclosing teams region exists then the binding region is that teams region; if binding is parallel then the binding region is the innermost enclosing paralle region, which may be an implicit parallel region; and if binding is thread then the binding region is not defined. If the bind clause is not specified on a construct for which it may be specified and the construct is a closely nested construct of a teams or parallel construct, the efect is as if binding is teams or parallel. If none of those conditions hold, the binding region is not defined.

The specified binding region determines the binding thread set. Specifically, if the binding region is a teams region, then the binding thread set is the set of initial threads that are executing that region while if the binding region is a parallel region, then the binding thread set is the team of threads that are executing that region. If the binding region is not defined, then the binding thread set is the encountering thread.

## Restrictions

Restrictions to the bind clause are as follows:

• If teams is specified as binding then the corresponding loop region must be a strictly nested region of a teams region.

• If teams is specified as binding and the corresponding loop region executes on a non-host device then the behavior of a reduction clause that appears on the corresponding loop construct is unspecified if the construct is not nested inside a teams construct.

• If parallel is specified as binding, the behavior is unspecified if the corresponding loop region is a closely nested region of a simd region.

## Cross References

• loop Construct, see Section 13.8

## 14 Tasking Constructs

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
