# 18 Cancellation Constructs

This chapter defines constructs related to cancellation of OpenMP regions.

## 18.1 cancel-directive-name Clauses

## Clause groups

Modifiers

<table><tr><td>Properties: exclusive, required, unique</td><td>Members:Clausesdo, for, parallel, sections, taskgroup</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

cancel, cancellation\_point

## Semantics

For each directive that has the cancellable property (i.e., the directive may subject to cancellation and is a cancellable construct), a corresponding clause for which clause-name is the directive-name of that directive is a member of the cancel-directive-name clause group. Each member of the cancel-directive-name clause group takes an optional argument, apply-to-directive, that must be a constant expression of logical OpenMP type. For each member of the clause group, if apply\_to\_directive evaluates to true then the semantics of the construct on which the clause appears are applied for the directive with the directive-name specified by the clause. If apply\_to\_directive evaluates to false, the efect is equivalent to specifying an if clause for which if-expression evaluates to false. If apply\_to\_directive is not specified, the efect is as if apply\_to\_directive evaluates to true.

## Restrictions

Restrictions to any clauses in the cancel-directive-name clause group are as follows:

• If apply\_to\_directive evaluates to false and an if clause is specified for the same constituent construct, if-expression must evaluate to false.

## Cross References

• cancel Construct, see Section 18.2

• cancellation\_point Construct, see Section 18.3

• do Construct, see Section 13.6.2

• for Construct, see Section 13.6.1

• parallel Construct, see Section 12.1

• sections Construct, see Section 13.3

• taskgroup Construct, see Section 17.4

## 18.2 cancel Construct

<table><tr><td>Name: cancelCategory: executable</td><td>Association: unassociatedProperties: default</td></tr></table>

## Clause groups

cancel-directive-name

## Clauses

## Binding

The binding thread set of the cancel region is the current team. The binding region of the cancel region is the innermost enclosing region of the type that corresponds to cancel-directive-name.

## Semantics

The cancel construct activates cancellation of the innermost enclosing region of the type specified by cancel-directive-name, which must be the directive-name of a cancellable construct. Cancellation of the binding region is activated only if the cancel-var ICV is true, in which case the cancel construct causes the encountering task to continue execution at the end of the binding region if cancel-directive-name is not taskgroup. If the cancel-var ICV is true and cancel-directive-name is taskgroup, the encountering task continues execution at the end of the current task region. If the cancel-var ICV is false, the cancel construct is ignored.

Threads check for active cancellation only at cancellation points that are implied at the following locations:

• cancel regions;

• cancellation\_point regions;

• barrier regions;

• at the end of a worksharing-loop construct with a nowait clause and for which the same list item appears in both firstprivate and lastprivate clauses; and

• implicit barrier regions.

When a thread reaches one of the above cancellation points and if the cancel-var ICV is true, then:

• If the thread is at a cancel or cancellation\_point region and cancel-directive-name is not taskgroup, the thread continues execution at the end of the canceled region if cancellation has been activated for the innermost enclosing region of the type specified.

• If the thread is at a cancel or cancellation\_point region and cancel-directive-name is taskgroup, the encountering task checks for active cancellation of all of the taskgroup sets to which the encountering task belongs, and continues execution at the end of the current task region if cancellation has been activated for any of the taskgroup sets.

• If the encountering task is at a barrier region or at the end of a worksharing-loop construct with a nowait clause and for which the same list item appears in both firstprivate and lastprivate clauses, the encountering task checks for active cancellation of the innermost enclosing parallel region. If cancellation has been activated, then the encountering task continues execution at the end of the canceled region.

When cancellation of tasks is activated through a cancel construct with taskgroup for cancel-directive-name, the tasks that belong to the taskgroup set of the innermost enclosing taskgroup region will be canceled; that taskgroup set is then the canceled taskgroup set corresponding to that cancel region. The task that encountered that construct continues execution at the end of its task region, which implies completion of that task. Any task that belongs to the canceled taskgroup set and has already begun execution must run to completion or until a cancellation point is reached. Upon reaching a cancellation point and if cancellation is active, the task continues execution at the end of its task region, which implies the completion of the task. Any task that belongs to the canceled taskgroup set and that has not begun execution or that has not yet been fulfilled through an event variable may be discarded, which implies its completion.

When cancellation of tasks is activated through a cancel construct with cancel-directive-name other than taskgroup, each thread of the binding thread set resumes execution at the end of the canceled region if a cancellation point is encountered. If the canceled region is a parallel region, any tasks that have been created by a task or a taskloop construct and their descendent tasks are canceled according to the above taskgroup cancellation semantics. If the canceled region is not a parallel region, no task cancellation occurs.

C++

The usual C++ rules for object destruction are followed when cancellation is performed.

C++

Fortran

All private objects or subobjects with the ALLOCATABLE attribute that are allocated inside the canceled construct are deallocated.

Fortran

If the canceled construct specifies an original list-item updating clause, the final values of the list items that appear in those clauses are undefined.

When an if clause is present on a cancel construct and if-expression evaluates to false, the cancel construct does not activate cancellation. The cancellation point associated with the cancel construct is always encountered regardless of the value of if-expression.

Note – The programmer is responsible for releasing locks and other synchronization data structures that might cause a deadlock when a cancel construct is encountered and blocked threads cannot be canceled. The programmer is also responsible for ensuring proper synchronizations to avoid deadlocks that might arise from cancellation of regions that contain synchronization constructs.

## Execution Model Events

If a task encounters a cancel construct that will activate cancellation then a cancel event occurs. A discarded-task event occurs for any discarded tasks.

## Tool Callbacks

A thread dispatches a registered cancel callback for each occurrence of a cancel event in the context of the encountering task. (flags & ompt\_cancel\_activated) always evaluates to true in the dispatched callback; (flags & ompt\_cancel\_parallel) evaluates to true in the dispatched callback if cancel-directive-name is parallel;

(flags & ompt\_cancel\_sections) evaluates to true in the dispatched callback if cancel-directive-name is sections; (flags & ompt\_cancel\_loop) evaluates to true in the dispatched callback if cancel-directive-name is for or do; and

(flags & ompt\_cancel\_taskgroup) evaluates to true in the dispatched callback if cancel-directive-name is taskgroup.

A thread dispatches a registered cancel callback with its task\_data argument pointing to the data object associated with the discarded task and with ompt\_cancel\_discarded\_task as its flags argument for each occurrence of a discarded-task event. The callback occurs in the context of the task that discards the task.

## Restrictions

Restrictions to the cancel construct are as follows:

• The behavior for concurrent cancellation of a region and a region nested within it is unspecified.

• If cancel-directive-name is taskgroup, the cancel construct must be a closely nested construct of a task or a taskloop construct and the cancel region must be a closely nested region of a taskgroup region.

• If cancel-directive-name is not taskgroup, the cancel construct must be a closely nested construct of a construct that matches cancel-directive-name.

• A worksharing construct that is canceled must not have a nowait clause or a reduction clause with a user-defined reduction that uses omp\_orig in the initializer-expr of the corresponding declare\_reduction directive.

• A worksharing-loop construct that is canceled must not have an ordered clause or a reduction clause with the inscan reduction-modifier.

• When cancellation is active for a parallel region, a thread in the team that binds to that region must not be executing or encounter a worksharing construct with an ordered clause, a reduction clause with the inscan reduction-modifier or a reduction clause with a user-defined reduction that uses omp\_orig in the initializer-expr of the corresponding declare\_reduction directive.

• During execution of a construct that may be subject to cancellation, a thread must not encounter an orphaned cancellation point. That is, a cancellation point must only be encountered within that construct and must not be encountered elsewhere in its region.

## Cross References

• barrier Construct, see Section 17.3.1

• cancel Callback, see Section 34.6

• OMPT cancel\_flag Type, see Section 33.7

• cancellation\_point Construct, see Section 18.3

• OMPT data Type, see Section 33.8

• declare\_reduction Directive, see Section 7.6.14

• firstprivate Clause, see Section 7.5.4

• cancel-var ICV, see Table 3.1

• if Clause, see Section 5.5

• nowait Clause, see Section 17.6

• omp\_get\_cancellation Routine, see Section 30.1

• ordered Clause, see Section 6.4.6

• private Clause, see Section 7.5.3

• reduction Clause, see Section 7.6.10

• task Construct, see Section 14.1

## 18.3 cancellation\_point Construct

<table><tr><td>Name: cancellation_pointCategory: executable</td><td>Association: unassociatedProperties: default</td></tr></table>

## Clause groups

cancel-directive-name

## Additional information

The cancellation\_point directive may alternatively be specified with cancellation point as the directive-name.

## Binding

The binding thread set of the cancellation\_point construct is the current team. The binding region of the cancellation\_point region is the innermost enclosing region of the type that corresponds to cancel-directive-name.

## Semantics

The cancellation\_point construct introduces a user-defined cancellation point at which an implicit task or explicit task must check if cancellation of the innermost enclosing region of the type specified by cancel-directive-name, which must be the directive-name of a cancellable construct, has been activated. This construct does not implement any synchronization between threads or tasks. The semantics, including the execution model events and tool callbacks, for when an implicit task or explicit task reaches a user-defined cancellation point are identical to those of any other cancellation point and are defined in Section 18.2.

## Restrictions

Restrictions to the cancellation point construct are as follows:

• A cancellation\_point construct for which cancel-directive-name is taskgroup must be a closely nested construct of a task or taskloop construct, and the cancellation\_point region must be a closely nested region of a taskgroup region.

• A cancellation\_point construct for which cancel-directive-name is not taskgroup must be a closely nested construct inside a construct that matches cancel-directive-name.

## Cross References

• cancel-var ICV, see Table 3.1

• omp\_get\_cancellation Routine, see Section 30.1

# 19 Composition of Constructs
