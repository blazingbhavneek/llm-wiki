
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
