# 15 Device Directives and Clauses

This chapter defines constructs and concepts related to device execution.

## 15.1 device\_type Clause

<table><tr><td>Name: device_type</td><td>Properties: unique</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>device-type-description</td><td>Keyword: any, host, nohost</td><td>default</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

begin declare\_target, declare\_target, groupprivate, target

## Semantics

If the device\_type clause appears on a declarative directive, the device-type-description argument specifies the type of devices for which a version of the procedure or variable should be made available. If the device\_type clause appears on a target construct, the argument specifies the type of devices for which the implementation should support execution of the corresponding target region.

The host device-type-description specifies the host device. The nohost device-type-description specifies any supported non-host device. The any device-type-description specifies any supported device. If the device\_type clause is not specified, the behavior is as if the device\_type clause appears with any specified.

If the device\_type clause specifies the host device on a target construct for which the target device is a non-host device, the corresponding region executes on the host device. Otherwise, if the devices specified by the device\_type clause does not include the target device then runtime error termination is performed.

## Cross References

• begin declare\_target Directive, see Section 9.9.2

• declare\_target Directive, see Section 9.9.1

• groupprivate Directive, see Section 7.13

• target Construct, see Section 15.8

## 15.2 device Clause

<table><tr><td>Name: device</td><td>Properties: ICV-defaulted, unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>device-description</td><td>expression of integer type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>device-modifier</td><td>device-description</td><td>Keyword: ancestor, device_num</td><td>default</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

dispatch, interop, target, target\_data, target\_enter\_data, target\_exit\_data, target\_update

## Semantics

The device clause identifies the target device that is associated with a device construct.

If device\_num is specified as the device-modifier, the device-description specifies the device number of the target device. If device-modifier does not appear in the clause, the behavior of the clause is as if device-modifier is device\_num. If the device-description evaluates to omp\_invalid\_device, runtime error termination is performed.

If ancestor is specified as the device-modifier, the device-description specifies the number of target nesting levels of the target device. Specifically, if the device-description evaluates to 1, the target device is the parent device of the enclosing target region. If the construct on which the device clause appears is not encountered in a target region, the current device is treated as the parent device.

Unless otherwise specified, for directives that accept the device clause, if no device clause is present, the behavior is as if the device clause appears with device\_num as device-modifier and with a device-description that evaluates to the value of the default-device-var ICV.

## Restrictions

• The ancestor device-modifier must not appear on the device clause on any directive other than the target construct.

• If the ancestor device-modifier is specified, the device-description must evaluate to 1 and a requires directive with the reverse\_offload clause must be specified;

• If the device\_num device-modifier is specified and target-ofload-var is not mandatory, device-description must evaluate to a conforming device number.

## Cross References

• dispatch Construct, see Section 9.7

• target-ofload-var ICV, see Table 3.1

• interop Construct, see Section 16.1

• target Construct, see Section 15.8

• target\_data Construct, see Section 15.7

• target\_enter\_data Construct, see Section 15.5

• target\_exit\_data Construct, see Section 15.6

• target\_update Construct, see Section 15.9

## 15.3 thread\_limit Clause

<table><tr><td>Name: thread_limit</td><td>Properties: ICV-modifying, target-consistent, unique</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>threadlim</td><td>expression of integer type</td><td>positive</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

target, teams

## Semantics

As described in Section 3.4, some constructs limit the number of threads that may participate in the parallel execution of tasks in a contention group initiated by each team by setting the value of the thread-limit-var ICV for the initial task to an implementation defined value greater than zero. If the thread\_limit clause is specified, the number of threads will be less than or equal to threadlim. Otherwise, if the teams-thread-limit-var ICV is greater than zero, the efect on a teams construct is as if the thread\_limit clause was specified with a threadlim that evaluates to an implementation defined value less than or equal to the teams-thread-limit-var ICV.

## Cross References

• target Construct, see Section 15.8

• teams Construct, see Section 12.2

## 15.4 Device Initialization

## Execution Model Events

The device-initialize event occurs in a thread that begins initialization of OpenMP on the device, after OpenMP initialization of the device, which may include device-side tool initialization, completes. The device-load event for a code block for a target device occurs in some thread before any thread executes code from that code block on that target device. The device-unload event for a target device occurs in some thread whenever a code block is unloaded from the device. The device-finalize event for a target device that has been initialized occurs in some thread before an OpenMP implementation shuts down.

## Tool Callbacks

A thread dispatches a registered device\_initialize callback for each occurrence of a device-initialize event in that thread. A thread dispatches a registered device\_load callback for each occurrence of a device-load event in that thread. A thread dispatches a registered device\_unload callback for each occurrence of a device-unload event in that thread. A thread dispatches a registered device\_finalize callback for each occurrence of a device-finalize event in that thread.

## Restrictions

Restrictions to OpenMP device initialization are as follows:

• No thread may ofload execution of a construct to a device until a dispatched device\_initialize callback completes.

• No thread may ofload execution of a construct to a device after a dispatched device\_finalize callback occurs.

## Cross References

• device\_finalize Callback, see Section 35.2

• device\_initialize Callback, see Section 35.1

• device\_load Callback, see Section 35.3

• device\_unload Callback, see Section 35.4

## 15.5 target\_enter\_data Construct

<table><tr><td>Name: target_enter_dataCategory: executable</td><td>Association: unassociatedProperties: parallelism-generating, task-generating, device, device-affecting, data-mapping, map-entering</td></tr></table>

## Clauses

depend, device, if, map, nowait, priority, replayable

## Additional information

The target\_enter\_data directive may alternatively be specified with target enter data as the directive-name.

## Binding

The binding task set for a target\_enter\_data region is the generating task, which is the target task generated by the target\_enter\_data construct. The target\_enter\_data region binds to the corresponding target task region.

## Semantics

When a target\_enter\_data construct is encountered, the list items in the map clause are mapped to the device data environment according to the map clause semantics. The target\_enter\_data construct generates a target task. The generated task region encloses the target\_enter\_data region. If a depend clause is present, it is associated with the target task. If the nowait clause is present, execution of the target task may be deferred. If the nowait clause is not present, the target task is an included task.

All clauses are evaluated when the target\_enter\_data construct is encountered. The data environment of the target task is created according to the data-mapping attribute clauses on the target\_enter\_data construct, ICVs with data environment ICV scope, and any default data-sharing attribute rules that apply to the target\_enter\_data construct. If a variable or part of a variable is mapped by the target\_enter\_data construct, the variable has a default data-sharing attribute of shared in the data environment of the target task.

Assignment operations associated with mapping a variable (see Section 7.9.6) occur when the target task executes.

When an if clause is present and if-expression evaluates to false, the target device is the host device.

## Execution Model Events

Events associated with a target task are the same as for the task construct defined in Section 14.1.

The target-enter-data-begin event occurs after creation of the target task and completion of all predecessor tasks that are not target tasks for the same device. The target-enter-data-begin event is a target-task-begin event. The target-enter-data-end event occurs after all other events associated with the target\_enter\_data construct.

## Tool Callbacks

Callbacks associated with events for target tasks are the same as for the task construct defined in Section 14.1; (flags & ompt\_task\_target) always evaluates to true in the dispatched callback.

A thread dispatches a registered target\_emi callback with ompt\_scope\_begin as its endpoint argument and ompt\_target\_enter\_data or

ompt\_target\_enter\_data\_nowait if the nowait clause is present as its kind argument for each occurrence of a target-enter-data-begin event in that thread in the context of the target task on the host device. Similarly, a thread dispatches a registered target\_emi callback with ompt\_scope\_end as its endpoint argument and ompt\_target\_enter\_data or ompt\_target\_enter\_data\_nowait if the nowait clause is present as its kind argument for each occurrence of a target-enter-data-end event in that thread in the context of the target task on the host device.

## Restrictions

Restrictions to the target\_enter\_data construct are as follows:

• At least one map clause must appear on the directive.

• All map clauses must be map-entering clauses.

## Cross References

• depend Clause, see Section 17.9.5

• device Clause, see Section 15.2

• if Clause, see Section 5.5

• map Clause, see Section 7.9.6

• nowait Clause, see Section 17.6

• priority Clause, see Section 14.9

• replayable Clause, see Section 14.6

• OMPT scope\_endpoint Type, see Section 33.27

• OMPT target Type, see Section 33.34

• target\_emi Callback, see Section 35.8

• task Construct, see Section 14.1

• OMPT task\_flag Type, see Section 33.37

## 15.6 target\_exit\_data Construct

<table><tr><td>Name: target_exit_dataCategory: executable</td><td>Association: unassociatedProperties: parallelism-generating, task-generating, device, device-affecting, data-mapping, map-exiting</td></tr></table>

## Clauses

depend, device, if, map, nowait, priority, replayable

## Additional information

The target\_exit\_data directive may alternatively be specified with target exit data as the directive-name.

## Binding

The binding task set for a target\_exit\_data region is the generating task, which is the target task generated by the target\_exit\_data construct. The target\_exit\_data region binds to the corresponding target task region.

## Semantics

When a target\_exit\_data construct is encountered, the list items in the map clauses are unmapped from the device data environment according to the map clause semantics. The target\_exit\_data construct generates a target task. The generated task region encloses the target\_exit\_data region. If a depend clause is present, it is associated with the target task. If the nowait clause is present, execution of the target task may be deferred. If the nowait clause is not present, the target task is an included task.

All clauses are evaluated when the target\_exit\_data construct is encountered. The data environment of the target task is created according to the data-mapping attribute clauses on the target\_exit\_data construct, ICVs with data environment ICV scope, and any default data-sharing attribute rules that apply to the target\_exit\_data construct. If a variable or part of a variable is mapped by the target\_exit\_data construct, the variable has a default data-sharing attribute of shared in the data environment of the target task.

Assignment operations associated with mapping a variable (see Section 7.9.6) occur when the target task executes.

When an if clause is present and if-expression evaluates to false, the target device is the host device.

## Execution Model Events

Events associated with a target task are the same as for the task construct defined in Section 14.1.

The target-exit-data-begin event occurs after creation of the target task and completion of all predecessor tasks that are not target tasks for the same device. The target-exit-data-begin event is a target-task-begin event. The target-exit-data-end event occurs after all other events associated with the target\_exit\_data construct.

## Tool Callbacks

Callbacks associated with events for target tasks are the same as for the task construct defined in Section 14.1; (flags & ompt\_task\_target) always evaluates to true in the dispatched callback.

A thread dispatches a registered target\_emi callback with ompt\_scope\_begin as its endpoint argument and ompt\_target\_exit\_data or

ompt\_target\_exit\_data\_nowait if the nowait clause is present as its kind argument for each occurrence of a target-exit-data-begin event in that thread in the context of the target task on the host device. Similarly, a thread dispatches a registered target\_emi callback with ompt\_scope\_end as its endpoint argument and ompt\_target\_exit\_data or ompt\_target\_exit\_data\_nowait if the nowait clause is present as its kind argument for each occurrence of a target-exit-data-end event in that thread in the context of the target task on the host device.

## Restrictions

Restrictions to the target\_exit\_data construct are as follows:

• At least one map clause must appear on the directive.

• All map clauses must be map-exiting clauses.

## Cross References

• depend Clause, see Section 17.9.5

• device Clause, see Section 15.2

• if Clause, see Section 5.5

• map Clause, see Section 7.9.6

• nowait Clause, see Section 17.6

• priority Clause, see Section 14.9

• replayable Clause, see Section 14.6

• OMPT scope\_endpoint Type, see Section 33.27

• OMPT target Type, see Section 33.34

• target\_emi Callback, see Section 35.8

• task Construct, see Section 14.1

• OMPT task\_flag Type, see Section 33.37

15.7 target\_data Construct

<table><tr><td>Name: target_dataCategory: executable</td><td>Association: blockProperties: device, device-affecting, data-mapping, map-entering, map-exiting, parallelism-generating, sharing-task, task-generating</td></tr></table>

## Clauses

affinity, allocate, default, depend, detach, device, firstprivate, if, in\_reduction, map, mergeable, nogroup, nowait, priority, private, shared, transparent, use\_device\_addr, use\_device\_ptr

## Clause set

data-environment-clause

<table><tr><td>Properties: required</td><td>Members: map, use_device_addr, use_device_ptr</td></tr></table>

## Additional information

The target\_data directive may alternatively be specified with target data as the directive-name.

## Binding

The binding task set for a target\_data region is the generating task. The target\_data region binds to the region of the generating task.

## Semantics

The target\_data construct is a composite directive that provides a superset of the functionality provided by the target\_enter\_data and target\_exit\_data directives. The functionality added by the target\_data directive is the inclusion of a task region for which data-sharing attributes may be specified. The efect of a target\_data directive is equivalent to that of specifying three constituent directives, as described in the following, except expressions in all clauses are evaluated when the target\_data construct is encountered.

The first constituent directive is a target\_enter\_data directive that is specified in the same code location as the target\_data directive. The second constituent directive is a task directive that is specified immediately after the target\_enter\_data directive and that is associated with the structured block associated with the target\_data directive. This task directive generates a sharing task. The third constituent directive is a target\_exit\_data directive that is specified immediately following the structured block that is associated with the target\_data directive.

Since each constituent directive is a task-generating construct, the target\_data directive generates three tasks. The task that is generated by the constituent target\_exit\_data directive is a dependent task of the task that is generated by the constituent task directive, which is a dependent task of the task that is generated by the constituent target\_enter\_data directive.

When an if clause is present on a target\_data construct, the efect is as if the clause is present only on the constituent data-mapping constructs.

When a nowait clause is present on a target\_data construct, the efect is as if the clause is present on the constituent data-mapping constructs. In addition, the task associated with the structured block may be deferred unless otherwise specified. If the nowait clause is not present, all tasks associated with the constituent directives are included tasks and, in addition, the task associated with the structured block is a merged task.

If the transparent clause is not specified then the efect is as if a transparent clause is specified such that impex-type evaluates to omp\_impex. If the mergeable clause is not specified then the efect is as if a mergeable clause is specified such that can\_merge evaluates to true.

When a map clause is present on a target\_data construct, the efect is as if the clause is present on the constituent data-mapping constructs with substituted map-type modifiers that are determined according to the rules of map-type decay.

A list item that appears in a map clause may also appear in a use\_device\_ptr clause or a use\_device\_addr clause. If one or more map clauses are present, the list item conversions that are performed for any use\_device\_ptr and use\_device\_addr clauses occur after all variables are mapped on entry to the region according to those map clauses.

If the nogroup clause is not present, the target\_data construct executes as if the structured block of the constituent task were enclosed in a taskgroup region. If the nogroup clause is present, no implicit taskgroup region is created.

## Execution Model Events

The events associated with entering a target\_data region are the same events as are associated with a target\_enter\_data construct, as described in Section 15.5, followed by the same events that are associated with a task construct, as described in Section 14.1.

The events associated with exiting a target\_data region are the same events as are associated with a target\_exit\_data construct, as described in Section 15.6.

## Tool Callbacks

The tool callbacks dispatched when entering a target\_data region are the same as the tool callbacks dispatched when encountering a target\_enter\_data construct, as described in Section 15.5, followed by the same tool callbacks that are dispatched when encountering a task construct, as described in Section 14.1.

The tool callbacks dispatched when exiting a target\_data region are the same as the tool callbacks dispatched when encountering a target\_exit\_data construct, as described in Section 15.6.

## Cross References

• affinity Clause, see Section 14.10

• allocate Clause, see Section 8.6

• default Clause, see Section 7.5.1

• depend Clause, see Section 17.9.5

• detach Clause, see Section 14.11

• device Clause, see Section 15.2

• firstprivate Clause, see Section 7.5.4

• if Clause, see Section 5.5

• in\_reduction Clause, see Section 7.6.12

• map Clause, see Section 7.9.6

• mergeable Clause, see Section 14.5

• nogroup Clause, see Section 17.7

• nowait Clause, see Section 17.6

• priority Clause, see Section 14.9

• private Clause, see Section 7.5.3

• shared Clause, see Section 7.5.2

• target\_enter\_data Construct, see Section 15.5

• target\_exit\_data Construct, see Section 15.6

• task Construct, see Section 14.1

• transparent Clause, see Section 17.9.6

• use\_device\_addr Clause, see Section 7.5.10

• use\_device\_ptr Clause, see Section 7.5.8

## 15.8 target Construct

<table><tr><td>Name: targetCategory:executable</td><td>Association: blockProperties: parallelism-generating, team-generating, thread-limiting, exception-aborting, task-generating, device, device-affecting, data-mapping, map-entering, map-exiting, context-matching</td></tr></table>

## Clauses

allocate, default, defaultmap, depend, device, device\_type, firstprivate, has\_device\_addr, if, in\_reduction, is\_device\_ptr, map, nowait, priority, private, replayable, thread\_limit, uses\_allocators

## Binding

The binding task set for a target region is the generating task, which is the target task generated by the target construct. The target region binds to the corresponding target task region.

## Semantics

The target construct generates a target task that encloses a target region to be executed on a device. If a depend clause is present, it is associated with the target task. The device and device\_type clauses determine the device on which to execute the target task region. If the nowait clause is present, execution of the target tasks may be deferred. If the nowait clause is not present, the target task is an included tasks. The efect of any map clauses occur on entry to and exit from the generated target region, as specified in Section 7.9.6.

All clauses are evaluated when the target construct is encountered. The data environment of the target task is created according to the data-sharing attribute clauses and data-mapping attribute clauses on the target construct, ICVs with data environment ICV scope, and any default data-sharing attribute rules that apply to the target construct. If a variable or part of a variable is mapped by the target construct and does not appear as a list item in an in\_reduction clause on the construct, the variable has a default data-sharing attribute of shared in the data environment of the target task. Assignment operations associated with mapping a variable (see Section 7.9.6) occur when the target task executes.

If the device clause is specified with the ancestor device-modifier, the encountering thread waits for completion of the target region on the parent device before resuming. For any list item that appears in a map clause on the same construct, if the corresponding list item exists in the device data environment of the parent device, it is treated as if it has a reference count of positive infinity.

When an if clause is present and if-expression evaluates to false, the efect is as if a device clause that specifies omp\_initial\_device as the device number is present, regardless of any other device clause on the directive.

If a procedure is explicitly or implicitly referenced in a target construct that does not specify a device clause in which the ancestor device-modifier appears then that procedure is treated as if its name had appeared in an enter clause on a declare target directive.

If a variable with static storage duration is declared in a target construct that does not specify a device clause in which the ancestor device-modifier appears then the named variable is treated as if it had appeared in an enter clause on a declare target directive if it is not a groupprivate variable and otherwise as if it had appeared in a local clause on a declare target directive.

If a list item in a map clause has a base pointer that is predetermined firstprivate or a base referencing variable for which the referring pointer is predetermined firstprivate (see Section 7.1.1), and on entry to the target region the list item is mapped, the firstprivate pointer is updated via corresponding pointer initialization.
