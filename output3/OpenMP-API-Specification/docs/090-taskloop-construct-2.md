
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

## 14.2.2 num\_tasks Clause

<table><tr><td>Name: num_tasks</td><td>Properties: taskgraph-altering, unique</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>num-tasks</td><td>expression of integer type</td><td>positive</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>prescriptiveness</td><td>num-tasks</td><td>Keyword: strict</td><td>unique</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

## taskloop

## Semantics

The num\_tasks clause specifies that the taskloop construct create as many tasks as the minimum of the num-tasks expression and the number of logical iterations. Each task must have at least one logical iteration. If prescriptiveness is specified as strict for a taskloop region with N logical iterations, the logical iterations are partitioned in a balanced manner and each partition is assigned, in order, to a generated task. The partition size is ⌈N/num-tasks⌉ until the number of remaining logical iterations divides the number of remaining tasks evenly, at which point the partition size becomes ⌊N/num-tasks⌋.

## Restrictions

Restrictions to the num\_tasks clause are as follows:

• None of the collapsed loops may be non-rectangular loops.

## Cross References

• taskloop Construct, see Section 14.2

14.2.3 task\_iteration Directive

<table><tr><td>Name: task_iterationCategory: subsidiary</td><td>Association: unassociatedProperties: default</td></tr></table>

## Enclosing directives

taskloop

## Clauses

affinity, depend, if

## Semantics

The task\_iteration directive is a subsidiary directive that controls the per-iteration task-execution attributes of the generated tasks of its associated taskloop construct, which is the innermost enclosing taskloop construct, as described below.

For each task-inherited clause specified on the task\_iteration directive, the behavior is as if each task generated by the enclosing taskloop construct is specified with a corresponding clause that has the same clause-specification, but adjusted as follows. These clauses are instantiated for each instance of the loop-iteration variables for which the if-expression of the if clause evaluates to true. If an if clause is not specified on the task\_iteration directive, the behavior is as if the if-expression evaluates to true.

## Restrictions

The restrictions to the task\_iteration directive are as follows:

• Each task\_iteration directive must appear in the loop body of one of the taskloop-afected loops and must precede all statements and directives (except other task\_iteration directives) in that loop body.

• If a task\_iteration directive appears in the loop body of one of the taskloop-afected loops, no intervening code may occur between any two collapsed loops of the taskloop-afected loops.

## Cross References

• affinity Clause, see Section 14.10

• depend Clause, see Section 17.9.5

• if Clause, see Section 5.5

• iterator Modifier, see Section 5.2.6

• task Construct, see Section 14.1

• taskloop Construct, see Section 14.2

## 14.3 taskgraph Construct
