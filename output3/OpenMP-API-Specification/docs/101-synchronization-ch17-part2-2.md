17.4 taskgroup Construct

<table><tr><td>Name: taskgroupCategory: executable</td><td>Association: blockProperties: cancellable</td></tr></table>

## Clauses

allocate, task\_reduction

## Binding

The binding task set of a taskgroup region is all tasks of the current team that are generated in the region. A taskgroup region binds to the innermost enclosing parallel region.

## Semantics

The taskgroup construct specifies a wait on completion of the taskgroup set associated with the taskgroup region. When a thread encounters a taskgroup construct, it starts executing the region. An implicit task scheduling point occurs at the end of the taskgroup region. The current task is suspended at the task scheduling point until all tasks in the taskgroup set complete execution.

## Execution Model Events

The taskgroup-begin event occurs in each thread that encounters the taskgroup construct on entry to the taskgroup region. The taskgroup-wait-begin event occurs when a task begins a waiting interval in a taskgroup region. The taskgroup-wait-end event occurs when a task ends a waiting interval and resumes execution in a taskgroup region. The taskgroup-end event occurs in each thread that encounters the taskgroup construct after the taskgroup synchronization on exit from the taskgroup region.

## Tool Callbacks

A thread dispatches a registered sync\_region callback with

ompt\_sync\_region\_taskgroup as its kind argument and ompt\_scope\_begin as its endpoint argument for each occurrence of a taskgroup-begin event in the task that encounters the taskgroup construct. Similarly, a thread dispatches a registered sync\_region callback with ompt\_sync\_region\_taskgroup as its kind argument and ompt\_scope\_end as its endpoint argument for each occurrence of a taskgroup-end event in the task that encounters the taskgroup construct. These callbacks occur in the task that encounters the taskgroup construct.

A thread dispatches a registered sync\_region\_wait callback with

ompt\_sync\_region\_taskgroup as its kind argument and ompt\_scope\_begin as its endpoint argument for each occurrence of a taskgroup-wait-begin event. Similarly, a thread dispatches a registered sync\_region\_wait callback with

ompt\_sync\_region\_taskgroup as its kind argument and ompt\_scope\_end as its endpoint argument for each occurrence of a taskgroup-wait-end event. These callbacks occur in the context of the task that encounters the taskgroup construct.

## Cross References

• allocate Clause, see Section 8.6

• Task Scheduling, see Section 14.14

• OMPT scope\_endpoint Type, see Section 33.27

• sync\_region Callback, see Section 34.7.4

• OMPT sync\_region Type, see Section 33.33

• sync\_region\_wait Callback, see Section 34.7.5

• task\_reduction Clause, see Section 7.6.11

## 17.5 taskwait Construct

<table><tr><td>Name: taskwaitCategory: executable</td><td>Association: unassociatedProperties: default</td></tr></table>

## Clauses

depend, nowait, replayable

## Binding

The binding thread set of the taskwait region is the current team. The taskwait region binds to the current task region.

## Semantics

The taskwait construct specifies a wait on the completion of child tasks of the current task.

If no depend clause is present on the taskwait construct, the current task region is suspended at an implicit task scheduling point associated with the construct. The current task region remains suspended until all child tasks that it generated before the taskwait region complete execution.

If one or more depend clauses are present on the taskwait construct and the nowait clause is not also present, the behavior is as if these clauses were applied to a task construct with an empty associated structured block that generates a mergeable task and included task. Thus, the current task region is suspended until the predecessor tasks of this task complete execution.

If one or more depend clauses are present on the taskwait construct and the nowait clause is also present, the behavior is as if these clauses were applied to a task construct with an empty associated structured block that generates a task for which execution may be deferred. Thus, all predecessor tasks of this task must complete execution before any subsequently generated task that depends on this task starts its execution.

## Execution Model Events

The taskwait-begin event occurs in a thread when it encounters a taskwait construct with no depend clause on entry to the taskwait region. The taskwait-wait-begin event occurs when a task begins a waiting interval in a region that corresponds to a taskwait construct with no depend clause. The taskwait-wait-end event occurs when a task ends a waiting interval and resumes execution from a region that corresponds to a taskwait construct with no depend clause. The taskwait-end event occurs in a thread when it encounters a taskwait construct with no depend clause after the taskwait synchronization on exit from the taskwait region.

The taskwait-init event occurs in a thread when it encounters a taskwait construct with one or more depend clauses on entry to the taskwait region. The taskwait-complete event occurs on completion of the dependent task that results from a taskwait construct with one or more depend clauses, in the context of the thread that executes the dependent task and before any subsequently generated task that depends on the dependent task starts its execution.

## Tool Callbacks

## A thread dispatches a registered sync\_region callback with

ompt\_sync\_region\_taskwait as its kind argument and ompt\_scope\_begin as its endpoint argument for each occurrence of a taskwait-begin event in the task that encounters the taskwait construct. Similarly, a thread dispatches a registered sync\_region callback with ompt\_sync\_region\_taskwait as its kind argument and ompt\_scope\_end as its endpoint argument for each occurrence of a taskwait-end event in the task that encounters the taskwait construct. These callbacks occur in the task that encounters the taskwait construct.

A thread dispatches a registered sync\_region\_wait callback with

ompt\_sync\_region\_taskwait as its kind argument and ompt\_scope\_begin as its endpoint argument for each occurrence of a taskwait-wait-begin event. Similarly, a thread dispatches a registered sync\_region\_wait callback with ompt\_sync\_region\_taskwait as its kind argument and ompt\_scope\_end as its endpoint argument for each occurrence of a taskwait-wait-end event. These callbacks occur in the context of the task that encounters the taskwait construct.

A thread dispatches a registered task\_create callback for each occurrence of a taskwait-init event in the context of the encountering task. In the dispatched callback, (flags & ompt\_task\_taskwait) always evaluates to true. If the nowait clause is not present, (flags & ompt\_task\_undeferred) also evaluates to true.

A thread dispatches a registered task\_schedule callback for each occurrence of a taskwait-complete event. This callback has ompt\_taskwait\_complete as its prior\_task\_status argument.

## Restrictions

Restrictions to the taskwait construct are as follows:

• The mutexinoutset task-dependence-type may not appear in a depend clause on a taskwait construct.

• If the task-dependence-type of a depend clause is depobj then the depend objects may not represent dependences of the mutexinoutset dependence type.

• The nowait clause may only appear on a taskwait directive if the depend clause is present.

• The replayable clause may only appear on a taskwait directive if the depend clause is present.

## Cross References

• depend Clause, see Section 17.9.5

• nowait Clause, see Section 17.6

• replayable Clause, see Section 14.6

• OMPT scope\_endpoint Type, see Section 33.27

• sync\_region Callback, see Section 34.7.4

• OMPT sync\_region Type, see Section 33.33

• sync\_region\_wait Callback, see Section 34.7.5

• task Construct, see Section 14.1

• OMPT task\_flag Type, see Section 33.37

• task\_schedule Callback, see Section 34.5.2

• OMPT task\_status Type, see Section 33.38

## 17.6 nowait Clause
