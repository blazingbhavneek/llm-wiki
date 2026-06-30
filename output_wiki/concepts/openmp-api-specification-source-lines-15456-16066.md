# OpenMP-API-Specification Source Lines 15456-16066

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source OpenMP-API-Specification:L15456-L16066

Citation: [OpenMP-API-Specification:L15456-L16066]

````text
## 13.4 workshare Construct

<table><tr><td>Name: workshareCategory:executable</td><td>Association: blockProperties: work-distribution, team-executed, partitioned, worksharing</td></tr></table>

## Clauses

nowait

## Binding

The binding thread set for a workshare region is the current team. A workshare region binds to the innermost enclosing parallel region. Only the threads of the team that executes the binding parallel region participate in the execution of the units of work and the implied barrier of the workshare region if the barrier is not eliminated by a nowait clause.

## Semantics

The workshare construct divides the execution of the associated structured block into separate units of work and causes the threads of the team to share the work such that each unit of work is executed only once by one thread, in the context of its implicit task. An implicit barrier occurs at the end of a workshare region if a nowait clause does not specify otherwise.

An implementation of the workshare construct must insert any synchronization that is required to maintain Fortran semantics. For example, the efects of each statement within the structured block must appear to occur before the execution of the following statements, and the evaluation of the right hand side of an assignment must appear to complete prior to the efects of assigning to the left hand side.

The statements in the workshare construct are divided into units of work as follows:

• For array expressions within each statement, including transformational array intrinsic functions that compute scalar values from arrays:

– Evaluation of each element of the array expression, including any references to elemental functions, is a unit of work.

– Evaluation of transformational array intrinsic functions may be subdivided into any number of units of work.

• For array assignment statements, assignment of each element is a unit of work.

• For scalar assignment statements, each assignment operation is a unit of work.

• For WHERE statements or constructs, evaluation of the mask expression and the masked assignments are each a unit of work.

• For FORALL statements or constructs, evaluation of the mask expression, expressions occurring in the specification of the iteration space, and the masked assignments are each a unit of work.

• For atomic constructs, critical constructs, and parallel constructs, the construct is a unit of work. A new team executes the statements contained in a parallel construct.

• If none of the rules above apply to a portion of a statement in the structured block, then that portion is a unit of work.

The transformational array intrinsic functions are MATMUL, DOT\_PRODUCT, SUM, PRODUCT, MAXVAL, MINVAL, COUNT, ANY, ALL, SPREAD, PACK, UNPACK, RESHAPE, TRANSPOSE, EOSHIFT, CSHIFT, MINLOC, and MAXLOC.

The units of work are assigned to the threads that execute a workshare region such that each unit of work is executed once.

If an array expression in the structured block references the value, association status, or allocation status of private variables, the value of the expression is undefined, unless the same value would be computed by every thread.

If an array assignment, a scalar assignment, a masked array assignment, or a FORALL assignment assigns to a private variable in the structured block, the result is unspecified.

The workshare directive causes the sharing of work to occur only in the workshare construct, and not in the remainder of the workshare region.

## Execution Model Events

The workshare-begin event occurs after an implicit task encounters a workshare construct but before the task starts to execute the structured block of the workshare region. The workshare-end event occurs after an implicit task finishes execution of a workshare region but before it resumes execution of the enclosing context.

## Tool Callbacks

A thread dispatches a registered work callback with ompt\_scope\_begin as its endpoint argument and ompt\_work\_workshare as its work\_type argument for each occurrence of a workshare-begin event in that thread. Similarly, a thread dispatches a registered work callback with ompt\_scope\_end as its endpoint argument and ompt\_work\_workshare as its work\_type argument for each occurrence of a workshare-end event in that thread. The callbacks occur in the context of the implicit task.

## Restrictions

Restrictions to the workshare construct are as follows:

• The only OpenMP constructs that may be closely nested constructs of a workshare construct are the atomic, critical, and parallel constructs.

• Base language statements that are encountered inside a workshare construct but that are not enclosed within a parallel or atomic construct that is nested inside the workshare construct must consist of only the following:

– array assignments;

– scalar assignments;

– FORALL statements;

– FORALL constructs;

– WHERE statements;

– WHERE constructs; and

– BLOCK constructs that are strictly structured blocks associated with directives.

• All array assignments, scalar assignments, and masked array assignments that are encountered inside a workshare construct but are not nested inside a parallel construct that is nested inside the workshare construct must be intrinsic assignments.

• The construct must not contain any user-defined function calls unless either the function is pure and elemental or the function call is contained inside a parallel construct that is nested inside the workshare construct.

## Cross References

• atomic Construct, see Section 17.8.5

• critical Construct, see Section 17.2

• nowait Clause, see Section 17.6

• parallel Construct, see Section 12.1

• OMPT scope\_endpoint Type, see Section 33.27

• work Callback, see Section 34.4.1

• OMPT work Type, see Section 33.41

Fortran

Fortran

## 13.5 workdistribute Construct

<table><tr><td>Name: workdistributeCategory:executable</td><td>Association: blockProperties: work-distribution, partitioned</td></tr></table>

## Binding

The binding region is the innermost enclosing teams region. The binding thread set is the set of initial threads executing the enclosing teams region.

## Semantics

The workdistribute construct divides the execution of the associated structured block into separate units of work and causes the threads of the binding thread set to share the work such that each unit of work is executed only once by one thread, in the context of its implicit task. No implicit barrier occurs at the end of a workdistribute region.

An implementation must enforce ordering of statements that is required to maintain Fortran semantics. For example, the efects of each statement within the structured block must appear to occur before the execution of the subsequent statements, and the evaluation of the right hand side of an assignment must appear to complete prior to the efects of assigning to the left hand side.

The statements in the workdistribute construct are divided into units of work as follows:

• For array expressions within each statement, including transformational array intrinsic functions that compute scalar values from arrays:

– Evaluation of each element of the array expression, including any references to pure elemental procedures, is a unit of work.

– Evaluation of transformational array intrinsic functions may be subdivided into any number of units of work.

• For array assignment statements, assignment of each element is a unit of work.

• For scalar assignment statements, each assignment operation is a unit of work.

The transformational array intrinsic functions are MATMUL, DOT\_PRODUCT, SUM, PRODUCT, MAXVAL, MINVAL, COUNT, ANY, ALL, SPREAD, PACK, UNPACK, RESHAPE, TRANSPOSE, EOSHIFT, CSHIFT, MINLOC, and MAXLOC.

The units of work are assigned to the binding thread set that execute a workdistribute region such that each unit of work is executed once.

If an array expression in the structured block references the value, association status, or allocation status of private variables, the value of the expression is undefined, unless the same value would be computed by every thread.

## Execution Model Events

The workdistribute-begin event occurs after an initial task encounters a workdistribute construct but before the task starts to execute the structured block of the workdistribute region. The workdistribute-end event occurs after an initial task finishes execution of a workdistribute region but before it resumes execution of the enclosing context.

## Tool Callbacks

A thread dispatches a registered work callback with ompt\_scope\_begin as its endpoint argument and ompt\_work\_workdistribute as its work\_type argument for each occurrence of a workdistribute-begin event in that thread. Similarly, a thread dispatches a registered work callback with ompt\_scope\_end as its endpoint argument and

ompt\_work\_workdistribute as its work\_type argument for each occurrence of a workdistribute-end event in that thread. The callbacks occur in the context of the implicit task.

## Restrictions

Restrictions to the workdistribute construct are as follows:

• The workdistribute construct must be a closely nested construct inside a teams construct.

• No explicit region may be nested inside a workdistribute region.

• Base language statements that are encountered inside a workdistribute must consist of only the following:

– array assignments;

– scalar assignments; and

– calls to pure and elemental procedures.

• All array assignments and scalar assignments that are encountered inside a workdistribute construct must be intrinsic assignments.

• The construct must not contain any calls to procedures that are not pure and elemental.

• If a threadprivate variable or groupprivate variable is referenced inside a workdistribute region, the behavior is unspecified.

## Cross References

• OMPT scope\_endpoint Type, see Section 33.27

• target Construct, see Section 15.8

• teams Construct, see Section 12.2

• work Callback, see Section 34.4.1

• OMPT work Type, see Section 33.41

Fortran

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

13.6.3 schedule Clause

<table><tr><td>Name: schedule</td><td>Properties: schedule-specification, unique</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>kind</td><td>Keyword: auto, dynamic, guided, runtime, static</td><td>default</td></tr><tr><td>chunk_size</td><td>expression of integer type</td><td>ultimate, optional, positive, region-invariant</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>ordering-modifier</td><td>kind</td><td>Keyword: monotonic, nonmonotonic</td><td>unique</td></tr><tr><td>chunk-modifier</td><td>kind</td><td>Keyword: simd</td><td>unique</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

do, for

## Semantics

The schedule clause specifies how collapsed iterations of a worksharing-loop construct are divided into chunks, and how these chunks are distributed among threads of the team.

The chunk\_size expression is evaluated using the original list items of any variables that are made private variables in the worksharing-loop construct. Whether, in what order, or how many times, any side efects of the evaluation of this expression occur is unspecified. The use of a variable in a schedule clause expression of a worksharing-loop construct causes an implicit reference to the variable in all enclosing constructs.

If the kind argument is static, chunks of increasing collapsed iteration numbers are assigned to the threads of the team in a round-robin fashion in the order of the thread number. Each chunk includes chunk\_size collapsed iterations, except possibly for the chunk that contains the sequentially last iteration, which may have fewer iterations. If chunk\_size is not specified, the collapsed iteration space is divided into chunks that are approximately equal in size, and at most one chunk is distributed to each thread.

If the kind argument is dynamic, each thread executes a chunk, then requests another chunk, until no chunks remain to be assigned. Each chunk contains chunk\_size collapsed iterations, except for the chunk that contains the sequentially last iteration, which may have fewer iterations. If chunk\_size is not specified, it defaults to 1.

If the kind argument is guided, each thread executes a chunk, then requests another chunk, until no chunks remain to be assigned. For a chunk\_size of 1, the size of each chunk is proportional to the number of unassigned collapsed iterations divided by the number of threads in the team, decreasing to 1. For a chunk\_size with value $k > 1$ , the size of each chunk is determined in the same way, with the restriction that the chunks do not contain fewer than k collapsed iterations (except for the chunk that contains the sequentially last iteration, which may have fewer than k iterations). If chunk\_size is not specified, it defaults to 1.

If the kind argument is auto, the decision regarding scheduling is implementation defined. If the schedule clause is not specified on a worksharing-loop construct then the efect is as if the schedule clause was specified with auto as its kind argument.

If the kind argument is runtime, the decision regarding scheduling is deferred until runtime, and the behavior is as if the clause specifies kind, chunk-size and ordering-modifier as set in the run-sched-var ICV. If the schedule clause explicitly specifies any modifiers then they override any corresponding modifiers that are specified in the run-sched-var ICV.

If the simd chunk-modifier is specified and the canonical loop nest is associated with a SIMD construct, new\_chunk\_size = ⌈chunk\_size/simd\_width⌉ ∗ simd\_width is the chunk\_size for all chunks except the first and last chunks, where simd\_width is an implementation defined value. The first chunk will have at least new\_chunk\_size collapsed iterations except if it is also the last chunk. The last chunk may have fewer collapsed iterations than new\_chunk\_size. If the simd chunk-modifier is specified and the canonical loop nest is not associated with a SIMD construct, the modifier is ignored.

##

Note – For a team of $\dot { \mathbf { \rho } } _ { p }$ threads and collapsed loops of n collapsed iterations, let $\lceil n / p \rceil$ be the integer q that satisfies $n = p * q - r .$ with $0 < = r < p .$ One compliant implementation of the static schedule type (with no specified chunk\_size) would behave as though chunk\_size had been specified with value q. Another compliant implementation would assign q collapsed iterations to the first $p - r$ threads, and $q - 1$ collapsed iterations to the remaining r threads. This illustrates why a conforming program must not rely on the details of a particular implementation.

A compliant implementation of the guided schedule type with a chunk\_size value of k would assign $q = \lceil n / p \rceil$ collapsed iterations to the first available thread and set n to the larger of $n - q$ and $p * k .$ . It would then repeat this process until q is greater than or equal to the number of remaining collapsed iterations, at which time the remaining iterations form the final chunk. Another compliant implementation could use the same method, except with $q = \lceil n / ( 2 p ) \rceil$ , and set n to the larger of $n - q$ and $2 * p * k$

If the monotonic ordering-modifier is specified then each thread executes the chunks that it is assigned in increasing collapsed iteration order. When the nonmonotonic ordering-modifier is specified then chunks may be assigned to threads in any order and the behavior of an application that depends on any execution order of the chunks is unspecified. If an ordering-modifier is not specified, the efect is as if the monotonic ordering-modifier is specified if the kind argument is static or an ordered clause is specified on the construct; otherwise, the efect is as if the nonmonotonic ordering-modifier is specified.

## Restrictions

Restrictions to the schedule clause are as follows:

• The schedule clause cannot be specified if any of the collapsed loops is a non-rectangular loop.

• The value of the chunk\_size expression must be the same for all threads in the team.

• If runtime or auto is specified for kind, chunk\_size must not be specified.

• The nonmonotonic ordering-modifier cannot be specified if an ordered clause is specified on the same construct.

## Cross References

• do Construct, see Section 13.6.2

• for Construct, see Section 13.6.1

• run-sched-var ICV, see Table 3.1

• ordered Clause, see Section 6.4.6

## 13.7 distribute Construct

<table><tr><td>Name: distributeCategory: executable</td><td>Association: loop nestProperties: SIMD-partitionable,teams-nestable, work-distribution, partitioned</td></tr></table>

## Clauses

allocate, collapse, dist\_schedule, firstprivate, induction, lastprivate, order, private

## Binding

The binding thread set for a distribute region is the set of initial threads executing an enclosing teams region. A distribute region binds to this teams region.

## Semantics

The distribute construct specifies that the collapsed iterations will be executed by the initial teams in the context of their implicit tasks. The collapsed iterations are distributed across the initial threads of all initial teams that execute the teams region to which the distribute region binds. No implicit barrier occurs at the end of a distribute region. To avoid data races the original list items that are modified due to lastprivate clauses should not be accessed between the end of the distribute construct and the end of the teams region to which the distribute binds.

If the dist\_schedule clause is not specified, the loop schedule is implementation defined.

The schedule is reproducible if one of the following conditions is true:

• The order clause is specified with the reproducible order-modifier modifier; or

• The dist\_schedule clause is specified with static as the kind argument and the order clause is not specified with the unconstrained order-modifier.

## Execution Model Events

The distribute-begin event occurs after an initial task encounters a distribute construct but before the task starts to execute the structured block of the distribute region. The distribute-end event occurs after an initial task finishes execution of a distribute region but before it resumes execution of the enclosing context.

The distribute-chunk-begin event occurs for each scheduled chunk of a distribute region before execution of any collapsed iteration.

## Tool Callbacks

A thread dispatches a registered work callback with ompt\_scope\_begin as its endpoint argument and ompt\_work\_distribute as its work\_type argument for each occurrence of a distribute-begin event in that thread. Similarly, a thread dispatches a registered work callback with ompt\_scope\_end as its endpoint argument and ompt\_work\_distribute as its work\_type argument for each occurrence of a distribute-end event in that thread. The callbacks occur in the context of the implicit task.

A thread dispatches a registered dispatch callback for each occurrence of a distribute-chunk-begin event in that thread. The callback occurs in the context of the initial task.

## Restrictions

Restrictions to the distribute construct are as follows:

• The collapsed iteration space must the same for all teams in the league.

• The region that corresponds to the distribute construct must be a strictly nested region of a teams region.

• A list item may appear in a firstprivate or lastprivate clause, but not in both.

• The conditional lastprivate-modifier must not be specified.

• All list items that appear in an induction clause must be private variables in the enclosing context.

## Cross References

• allocate Clause, see Section 8.6

• collapse Clause, see Section 6.4.5

• dispatch Callback, see Section 34.4.2

• dist\_schedule Clause, see Section 13.7.1

• firstprivate Clause, see Section 7.5.4

• Consistent Loop Schedules, see Section 6.4.4

• induction Clause, see Section 7.6.13

• lastprivate Clause, see Section 7.5.5

• order Clause, see Section 12.3

• private Clause, see Section 7.5.3

• OMPT scope\_endpoint Type, see Section 33.27

• teams Construct, see Section 12.2

• work Callback, see Section 34.4.1

• OMPT work Type, see Section 33.41

## 13.7.1 dist\_schedule Clause

<table><tr><td>Name: dist_schedule</td><td>Properties: schedule-specification, unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>kind</td><td>Keyword: static</td><td>default</td></tr><tr><td>chunk_size</td><td>expression of integer type</td><td>ultimate, optional, positive, region-invariant</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

distribute

## Semantics

The dist\_schedule clause specifies how collapsed iterations of a distribute construct are divided into chunks, and how these chunks are distributed among the teams of the league. If chunk\_size is not specified, the collapsed iteration space is divided into chunks that are approximately equal in size, and at most one chunk is distributed to each initial team of the league. If the chunk\_size argument is specified, collapsed iterations are divided into chunks of chunk\_size iterations. The chunk\_size expression is evaluated using the original list items of any variables that become private variables in the distribute construct. Whether, in what order, or how many times, any side efects of the evaluation of this expression occur is unspecified. The use of a variable in a dist\_schedule clause expression of a distribute construct causes an implicit reference to the variable in all enclosing constructs. These chunks are assigned to the initial teams of the league in a round-robin fashion in the order of their team number.

## Restrictions

Restrictions to the dist\_schedule clause are as follows:

• The value of the chunk\_size expression must be the same for all teams in the league.

• The dist\_schedule clause cannot be specified if any of the collapsed loops is a non-rectangular loop.

## Cross References

• distribute Construct, see Section 13.7

## 13.8 loop Construct

<table><tr><td>Name: loopCategory: executable</td><td>Association: loop nestProperties: order-concurrent-nestable, partitioned, simdizable, team-executed, teams-nestable, work-distribution, worksharing</td></tr></table>

## Clauses

bind, collapse, lastprivate, order, private, reduction

## Binding

The bind clause determines the binding region, which determines the binding thread set.

## Semantics

A loop construct specifies that the collapsed iterations execute in the context of the binding thread set, in an order specified by the order clause. If the order clause is not specified, the behavior is as if the order clause is present and specifies the concurrent ordering. The collapsed iterations are executed as if by the binding thread set, once per instance of the loop region that is encountered by the binding thread set.

The loop schedule for a loop construct is reproducible unless the order clause is present with the unconstrained order-modifier.

If the loop region binds to a teams region, the threads in the binding thread set may continue execution after the loop region without waiting for all collapsed iterations to complete. The collapsed iterations are guaranteed to complete before the end of the teams region. If the loop region does not bind to a teams region, all collapsed iterations must complete before the encountering threads continue execution after the loop region.

While a loop construct is always a work-distribution construct, it is a worksharing construct if and only if its binding region is the innermost enclosing parallel region. Further, the loop construct has the SIMDizable property if and only if its binding region is not defined.

Fortran

The collapsed loop may be a DO CONCURRENT loop.

Fortran

## Restrictions

Restrictions to the loop construct are as follows:

• A list item must not appear in a lastprivate clause unless it is the loop-iteration variable of an afected loop.

• If a reduction-modifier is specified in a reduction clause that appears on the directive then the reduction-modifier must be default.

• If a loop construct is not nested inside another construct then the bind clause must be present.

• If a loop region binds to a teams region or parallel region, it must be encountered by all threads in the binding thread set or by none of them.

Fortran

• If the collapsed loop is a DO CONCURRENT loop, neither the data-sharing attribute clauses nor the collapse clause may be specified.

• If a variable is accessed in more than one iteration of a DO CONCURRENT loop that is associated with a loop construct and at least one of the accesses modifies the variable, the variable must have locality specified in the DO CONCURRENT loop.

Fortran

## Cross References

• bind Clause, see Section 13.8.1

• collapse Clause, see Section 6.4.5

• Consistent Loop Schedules, see Section 6.4.4

• lastprivate Clause, see Section 7.5.5

• order Clause, see Section 12.3

• private Clause, see Section 7.5.3

• reduction Clause, see Section 7.6.10

• teams Construct, see Section 12.2

## 13.8.1 bind Clause

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
````
