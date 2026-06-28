
A synchronization construct imposes an order on the completion of code executed by diferent threads through synchronizing flushes that are executed as part of the region that corresponds to the construct. Section 1.3.4 and Section 1.3.6 describe synchronization through the use of synchronizing flushes and atomic operations. Section 17.8.7 defines the behavior of synchronizing flushes that are implied at various other locations in an OpenMP program.

## 17.1 hint Clause

Modifiers

<table><tr><td>Name: hint</td><td>Properties: unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>hint-expr</td><td>expression of sync_hint type</td><td>default</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

atomic, critical

## Semantics

The hint clause gives the implementation additional information about the expected runtime properties of the region that corresponds to the construct on which it appears and that can optionally be used to optimize the implementation. The presence of a hint clause does not afect the semantics of the construct. If no hint clause is specified for a construct that accepts it, the efect is as if omp\_sync\_hint\_none had been specified as hint-expr.

## Restrictions

• hint-expr must evaluate to a valid synchronization hint.

## Cross References

• atomic Construct, see Section 17.8.5

• critical Construct, see Section 17.2

• OpenMP sync\_hint Type, see Section 20.9.5

## 17.2 critical Construct

<table><tr><td>Name: criticalCategory:executable</td><td>Association: blockProperties: mutual-exclusion, thread-limiting, thread-exclusive</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>name</td><td>base language identifier</td><td>optional</td></tr></table>

## Clauses

hint

## Binding

The binding thread set for a critical region is all threads executing tasks in the contention group.

## Semantics

The name argument is used to identify the critical construct. For any critical construct for which name is not specified, the efect is as if an identical (unspecified) name was specified. The regions that correspond to any critical construct of a given name are executed as if only by a single thread at a time among all threads associated with the contention group that execute the regions, without regard to the teams to which the threads belong.

C / C++

Identifiers used to identify a critical construct have external linkage and are in a name space that is separate from the name spaces used by labels, tags, members, and ordinary identifiers.

C / C++

Fortran

The names of critical constructs are global entities of the OpenMP program. If a name conflicts with any other entity, the behavior of the program is unspecified.

Fortran

## Execution Model Events

The critical-acquiring event occurs in a thread that encounters the critical construct on entry to the critical region before initiating synchronization for the region. The critical-acquired event occurs in a thread that encounters the critical construct after it enters the region, but before it executes the structured block of the critical region. The critical-released event occurs in a thread that encounters the critical construct after it completes any synchronization on exit from the critical region.

## Tool Callbacks

A thread dispatches a registered mutex\_acquire callback for each occurrence of a critical-acquiring event in that thread. A thread dispatches a registered mutex\_acquired callback for each occurrence of a critical-acquired event in that thread. A thread dispatches a registered mutex\_released callback for each occurrence of a critical-released event in that thread. These callbacks occur in the task that encounters the critical construct. The callbacks should receive ompt\_mutex\_critical as their kind argument if practical, but a less specific kind is acceptable.

## Restrictions

Restrictions to the critical construct are as follows:

• Unless omp\_sync\_hint\_none is specified in a hint clause, the critical construct must specify a name.

• The hint-expr that is specified in the hint clause on each critical construct with the same name must evaluate to the same value.

• A critical region must not be nested (closely or otherwise) inside a critical region with the same name. This restriction is not suficient to prevent deadlock.

## Fortran

• If a name is specified on a critical directive and a paired end directive is specified, the same name must also be specified on the end directive.

• If no name appears on the critical directive and a paired end directive is specified, no name can appear on the end directive.

## Fortran

## Cross References

• hint Clause, see Section 17.1

• OMPT mutex Type, see Section 33.20

• mutex\_acquire Callback, see Section 34.7.8

• mutex\_acquired Callback, see Section 34.7.12

• mutex\_released Callback, see Section 34.7.13

• OpenMP sync\_hint Type, see Section 20.9.5

## 17.3 Barriers

## 17.3.1 barrier Construct

<table><tr><td>Name: barrierCategory:executable</td><td>Association: unassociatedProperties: team-executed</td></tr></table>

## Binding

The binding thread set for a barrier region is the current team. A barrier region binds to the innermost enclosing parallel region.

## Semantics

The barrier construct specifies an explicit barrier at the point at which the construct appears. Unless the binding region is canceled, all threads of the team that executes that binding region must enter the barrier region and complete execution of all explicit tasks bound to that binding region before any of the threads continue execution beyond the barrier.

The barrier region includes an implicit task scheduling point in the current task region.

## Execution Model Events

The explicit-barrier-begin event occurs in each thread that encounters the barrier construct on entry to the barrier region. The explicit-barrier-wait-begin event occurs when a task begins a waiting interval in a barrier region. The explicit-barrier-wait-end event occurs when a task ends a waiting interval and resumes execution in a barrier region. The explicit-barrier-end event occurs in each thread that encounters the barrier construct after the barrier synchronization on exit from the barrier region. A cancellation event occurs if cancellation is activated at an implicit cancellation point in a barrier region.

## Tool Callbacks

A thread dispatches a registered sync\_region callback with

ompt\_sync\_region\_barrier\_explicit as its kind argument and ompt\_scope\_begin as its endpoint argument for each occurrence of an explicit-barrier-begin event. Similarly, a thread dispatches a registered sync\_region callback with

ompt\_sync\_region\_barrier\_explicit as its kind argument and ompt\_scope\_end as its endpoint argument for each occurrence of an explicit-barrier-end event. These callbacks occur in the context of the task that encountered the barrier construct.

A thread dispatches a registered sync\_region\_wait callback with

ompt\_sync\_region\_barrier\_explicit as its kind argument and ompt\_scope\_begin as its endpoint argument for each occurrence of an explicit-barrier-wait-begin event. Similarly, a thread dispatches a registered sync\_region\_wait callback with

ompt\_sync\_region\_barrier\_explicit as its kind argument and ompt\_scope\_end as its endpoint argument for each occurrence of an explicit-barrier-wait-end event. These callbacks occur in the context of the task that encountered the barrier construct.

A thread dispatches a registered cancel callback with ompt\_cancel\_detected as its flags argument for each occurrence of a cancellation event in that thread. The callback occurs in the context of the encountering task.

## Restrictions

Restrictions to the barrier construct are as follows:

• Each barrier region must be encountered by all threads in a team or by none at all, unless cancellation has been requested for the innermost enclosing parallel region.

• The sequence of worksharing regions and barrier regions encountered must be the same for every thread in a team.

## Cross References

• cancel Callback, see Section 34.6

• OMPT cancel\_flag Type, see Section 33.7

• OMPT scope\_endpoint Type, see Section 33.27

• sync\_region Callback, see Section 34.7.4

• OMPT sync\_region Type, see Section 33.33

• sync\_region\_wait Callback, see Section 34.7.5

## 17.3.2 Implicit Barriers

This section describes the OMPT events and tool callbacks associated with implicit barriers, which occur at the end of various regions as defined in the description of the constructs to which they correspond. Implicit barriers are task scheduling points. For a description of task scheduling points, associated events, and tool callbacks, see Section 14.14.

## Execution Model Events

The implicit-barrier-begin event occurs in each task that encounters an implicit barrier at the beginning of the implicit barrier region. The implicit-barrier-wait-begin event occurs when a task begins a waiting interval in an implicit barrier region. The implicit-barrier-wait-end event occurs when a task ends a waiting interval and resumes execution of an implicit barrier region. The implicit-barrier-end event occurs in a task that encounters an implicit barrier after the barrier synchronization on exit from an implicit barrier region. A cancellation event occurs if cancellation is activated at an implicit cancellation point in an implicit barrier region.

## Tool Callbacks

A thread dispatches a registered sync\_region callback for each implicit-barrier-begin and implicit-barrier-end event. Similarly, a thread dispatches a registered sync\_region\_wait callback for each implicit-barrier-wait-begin and implicit-barrier-wait-end event. All callbacks for implicit barrier events execute in the context of the encountering task.

For the implicit barrier at the end of a worksharing construct, the kind argument is

ompt\_sync\_region\_barrier\_implicit\_workshare. For the implicit barrier at the end of a parallel region, the kind argument is

ompt\_sync\_region\_barrier\_implicit\_parallel. For a barrier at the end of a teams region, the kind argument is ompt\_sync\_region\_barrier\_teams. For an extra barrier added by an OpenMP implementation, the kind argument is ompt\_sync\_region\_barrier\_implementation.

A thread dispatches a registered cancel callback with ompt\_cancel\_detected as its flags argument for each occurrence of a cancellation event in that thread. The callback occurs in the context of the encountering task.

## Restrictions

Restrictions to implicit barriers are as follows:

• If a thread is in the ompt\_state\_wait\_barrier\_implicit\_parallel state, a call to get\_parallel\_info may return a pointer to a copy of the data object associated with the parallel region rather than a pointer to the associated data object itself. Writing to the data object returned by get\_parallel\_info when a thread is in the ompt\_state\_wait\_barrier\_implicit\_parallel state results in unspecified behavior.

## Cross References

• cancel Callback, see Section 34.6

• OMPT cancel\_flag Type, see Section 33.7

• get\_parallel\_info Entry Point, see Section 36.14

• OMPT scope\_endpoint Type, see Section 33.27

• OMPT state Type, see Section 33.31

• sync\_region Callback, see Section 34.7.4

• OMPT sync\_region Type, see Section 33.33

• sync\_region\_wait Callback, see Section 34.7.5

## 17.3.3 Implementation-Specific Barriers

An OpenMP implementation can execute implementation-specific barriers that the OpenMP specification does not imply; therefore, no execution model events are bound to them. The implementation can handle these barriers like implicit barriers and dispatch all events as for implicit barriers. Any callbacks for these events use

ompt\_sync\_region\_barrier\_implementation as the kind argument when they are dispatched.
