## 13.6 Worksharing-Loop Constructs

## Binding

The binding thread set for a worksharing-loop region is the current team. A worksharing-loop region binds to the innermost enclosing parallel region. Only those threads participate in execution of the collapsed iterations and the implied barrier of the worksharing-loop region when that barrier is not eliminated by a nowait clause.

## Semantics

The worksharing-loop construct is a worksharing construct that specifies that the collapsed iterations will be executed in parallel by threads in the team in the context of their implicit tasks. The collapsed iterations are distributed across the assigned threads of the team that is executing the parallel region to which the worksharing-loop region binds. Each thread executes its assigned chunks in the context of its implicit task. The execution of the collapsed iterations of a given chunk is consistent with their sequential order.

At the beginning of each collapsed iteration, the loop iteration variable or the variable declared by range-decl of each collapsed loop has the value that it would have if the collapsed loops were executed sequentially.

The loop schedule is reproducible if one of the following conditions is true:

• The order clause is specified with the reproducible order-modifier modifier; or

• The schedule clause is specified with static as the kind argument but not with the simd ordering-modifier and the order clause is not specified with the unconstrained order-modifier.

## Execution Model Events

The ws-loop-begin event occurs after an implicit task encounters a worksharing-loop construct but before the task starts execution of the structured block of the worksharing-loop region. The ws-loop-end event occurs after a worksharing-loop region finishes execution but before resuming execution of the encountering task.

The ws-loop-iteration-begin event occurs at the beginning of each collapsed iteration of a worksharing-loop region. The ws-loop-chunk-begin event occurs for each scheduled chunk of a worksharing-loop region before the implicit task executes any of the collapsed iterations.

## Tool Callbacks

A thread dispatches a registered work callback with ompt\_scope\_begin as its endpoint argument for each occurrence of a ws-loop-begin event in that thread. Similarly, a thread dispatches a registered work callback with ompt\_scope\_end as its endpoint argument for each occurrence of a ws-loop-end event in that thread. The callbacks occur in the context of the implicit task. The work\_type argument indicates the schedule type as shown in Table 13.1.

A thread dispatches a registered dispatch callback for each occurrence of a ws-loop-iteration-begin or ws-loop-chunk-begin event in that thread. The callback occurs in the context of the implicit task.

TABLE 13.1: work OMPT types for Worksharing-Loop

<table><tr><td>Value of work_type</td><td>If determined schedule is</td></tr><tr><td>ompt_work_loop</td><td>unknown at runtime</td></tr><tr><td>ompt_work_loop_static</td><td>static</td></tr><tr><td>ompt_work_loop_dynamic</td><td>dynamic</td></tr><tr><td>ompt_work_loop_guided</td><td>guided</td></tr><tr><td>ompt_work_loop_other</td><td>implementation defined</td></tr></table>

## Restrictions

Restrictions to the worksharing-loop construct are as follows:

• The collapsed iteration space must be the same for all threads in the team.

• The value of the run-sched-var ICV must be the same for all threads in the team.

## Cross References

• dispatch Callback, see Section 34.4.2

• run-sched-var ICV, see Table 3.1

• nowait Clause, see Section 17.6

• order Clause, see Section 12.3

• schedule Clause, see Section 13.6.3

• OMPT scope\_endpoint Type, see Section 33.27

• work Callback, see Section 34.4.1

• OMPT work Type, see Section 33.41

## 13.6.1 for Construct

<table><tr><td>Name: forCategory: executable</td><td>Association: loop nestProperties: work-distribution, team-executed, partitioned, SIMD-partitionable, worksharing, worksharing-loop, cancellable, context-matching</td></tr></table>

## Separating directives

scan

## Clauses

allocate, collapse, firstprivate, induction, lastprivate, linear, nowait, order, ordered, private, reduction, schedule

## Semantics

The for construct is a worksharing-loop construct.

## Cross References

• allocate Clause, see Section 8.6

• collapse Clause, see Section 6.4.5

• firstprivate Clause, see Section 7.5.4

• Worksharing-Loop Constructs, see Section 13.6

• induction Clause, see Section 7.6.13

• lastprivate Clause, see Section 7.5.5

• linear Clause, see Section 7.5.6

• nowait Clause, see Section 17.6

• order Clause, see Section 12.3

• ordered Clause, see Section 6.4.6

• private Clause, see Section 7.5.3

• reduction Clause, see Section 7.6.10

• scan Directive, see Section 7.7

• schedule Clause, see Section 13.6.3

C / C++

## 13.6.2 do Construct

<table><tr><td>Name: doCategory: executable</td><td>Association: loop nestProperties: work-distribution, team-executed, partitioned, SIMD-partitionable, worksharing, worksharing-loop, cancellable, context-matching</td></tr></table>

## Separating directives

scan

## Clauses

allocate, collapse, firstprivate, induction, lastprivate, linear, nowait, order, ordered, private, reduction, schedule

## Semantics

The do construct is a worksharing-loop construct.

## Cross References

• allocate Clause, see Section 8.6

• collapse Clause, see Section 6.4.5

• firstprivate Clause, see Section 7.5.4

• Worksharing-Loop Constructs, see Section 13.6

• induction Clause, see Section 7.6.13

• lastprivate Clause, see Section 7.5.5

• linear Clause, see Section 7.5.6

• nowait Clause, see Section 17.6

• order Clause, see Section 12.3

• ordered Clause, see Section 6.4.6

• private Clause, see Section 7.5.3

• reduction Clause, see Section 7.6.10

• scan Directive, see Section 7.7

• schedule Clause, see Section 13.6.3

Fortran
