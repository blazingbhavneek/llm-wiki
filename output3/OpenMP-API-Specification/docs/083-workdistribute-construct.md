
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
