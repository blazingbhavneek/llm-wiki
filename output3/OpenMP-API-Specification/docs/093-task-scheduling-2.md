
<table><tr><td>Name: taskyieldCategory: executable</td><td>Association: unassociatedProperties: default</td></tr></table>

## Binding

A taskyield region binds to the current task region. The binding thread set of the taskyield region is the current team.

## Semantics

The taskyield region includes an explicit task scheduling point in the current task region.

## Cross References

• Task Scheduling, see Section 14.14

## 14.13 Initial Task

## Execution Model Events

While no events are associated with the implicit parallel region in each initial thread, several events are associated with initial tasks. The initial-thread-begin event occurs in an initial thread after the OpenMP runtime invokes the OMPT-tool initializer but before the initial thread begins to execute the first explicit region in the initial task. The initial-task-begin event occurs after an initial-thread-begin event but before the first explicit region in the initial task begins to execute. The initial-task-end event occurs before an initial-thread-end event but after the last region in the initial task finishes execution. The initial-thread-end event occurs as the final event in an initia thread at the end of an initial task immediately prior to invocation of the OMPT-tool finalizer.

## Tool Callbacks

A thread dispatches a registered thread\_begin callback for the initial-thread-begin event in an initial thread. The callback occurs in the context of the initial thread. The callback receives ompt\_thread\_initial as its thread\_type argument.

A thread dispatches a registered implicit\_task callback with ompt\_scope\_begin as its endpoint argument for each occurrence of an initial-task-begin event in that thread. Similarly, a thread dispatches a registered implicit\_task callback with ompt\_scope\_end as its endpoint argument for each occurrence of an initial-task-end event in that thread. The callbacks occur in the context of the initial task. In the dispatched callback,

(flags & ompt\_task\_initial) and (flags & ompt\_task\_implicit) evaluate to true.

A thread dispatches a registered thread\_end callback for the initial-thread-end event in that thread. The callback occurs in the context of the thread. The implicit parallel region does not dispatch a parallel\_end callback; however, the implicit parallel region can be finalized within this thread\_end callback.

## Cross References

• implicit\_task Callback, see Section 34.5.3

• parallel\_end Callback, see Section 34.3.2

• OMPT scope\_endpoint Type, see Section 33.27

• OMPT task\_flag Type, see Section 33.37

• OMPT thread Type, see Section 33.39

• thread\_begin Callback, see Section 34.1.3

• thread\_end Callback, see Section 34.1.4

## 14.14 Task Scheduling

Whenever a thread reaches a task scheduling point, it may begin or resume execution of a task from its schedulable task set. An idle thread is treated as if it is always at a task scheduling point. For other threads, task scheduling points are implied at the following locations:

• During the generation of an explicit task;

• The point immediately following the generation of an explicit task;

• After the point of completion of the structured block associated with a task;

• In a taskyield region;

• In a taskwait region;

• At the end of a taskgroup region;

• At the beginning and end of a taskgraph region;

• In an implicit barrier region;

• In an explicit barrier region;

• During the generation of a target region;

• The point immediately following the generation of a target region;

• In a target\_update region;

• In a target\_enter\_data region;

• In a target\_exit\_data region;

• In each instance of any memory-copying routine;and

• In each instance of any memory-setting routine.

When a thread encounters a task scheduling point it may do one of the following, subject to the task scheduling constraints specified below:

• Begin execution of a tied task in its schedulable task set;

• Resume the suspended task region of any task to which it is tied;

• Begin execution of an untied task in its schedulable task set; or

• Resume the suspended task region of any untied task in its schedulable task set.

If more than one of the above choices is available, which one is chosen is unspecified.

Task Scheduling Constraints are as follows:

1. If any suspended tasks are tied to the thread and are not suspended in a barrier region, a new explicit tied task may be scheduled only if it is a descendent task of all of those suspended tasks. Otherwise, any new explicit tied task may be scheduled.

2. A dependent task shall not start its execution until its task dependences are fulfilled.

3. A task shall not be scheduled while another task has been scheduled but has not yet completed, if they are mutually exclusive tasks.

4. A task shall not start or resume execution on an unassigned thread if it would result in the total number of free-agent threads in the OpenMP thread pool exceeding free-agent-thread-limit-var.

Task scheduling points dynamically divide task regions into subtasks. Each subtask is executed uninterrupted from start to end. Diferent subtasks of the same task region are executed in the order in which they are encountered. In the absence of task synchronization constructs, the order in which a thread executes subtasks of diferent tasks in its schedulable task set is unspecified.

A program must behave correctly and consistently with all conceivable scheduling sequences that are compatible with the rules above. A program that relies on any other assumption about task scheduling is a non-conforming program.

Note – For example, if threadprivate memory is accessed (explicitly in the source code or implicitly in calls to library procedures) in one subtask of a task region, its value cannot be assumed to be preserved into the next subtask of the same task region if another schedulable task exists that modifies it.

As another example, if diferent subtasks of a task region invoke a lock-acquiring routine and its corresponding lock-releasing routine, no invocation of a lock-acquiring routine for the same lock should be made in any subtask of another task that the executing thread may schedule. Otherwise, deadlock is possible. A similar situation can occur when a critical region spans multiple subtasks of a task and another schedulable task contains a critical region with the same name.

## Execution Model Events

The task-schedule event occurs in a thread when the thread switches tasks at a task scheduling point; no event occurs when switching to or from a merged task.

## Tool Callbacks

A thread dispatches a registered task\_schedule callback for each occurrence of a task-schedule event in the context of the task that begins or resumes. The prior\_task\_status argument is used to indicate the cause for suspending the prior task. This cause may be the completion of the prior task region, the encountering of a taskyield construct, or the encountering of an active cancellation point.

## Cross References

• task\_schedule Callback, see Section 34.5.2

# 15 Device Directives and Clauses
