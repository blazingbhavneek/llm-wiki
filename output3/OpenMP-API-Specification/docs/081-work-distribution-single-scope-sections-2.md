
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
