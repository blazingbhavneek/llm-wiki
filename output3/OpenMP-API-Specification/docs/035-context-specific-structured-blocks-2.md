
• If a BLOCK construct appears in a structured block, that BLOCK construct must not contain any ASYNCHRONOUS or VOLATILE statements, nor any specification statements that include the ASYNCHRONOUS or VOLATILE attributes.

Fortran

## 6.3.1 OpenMP Allocator Structured Blocks

Fortran

An OpenMP allocator structured block is a context-specific structured block that is associated with an allocators directive. It consists of allocate-stmt, where allocate-stmt is a Fortran ALLOCATE statement. For an allocators directive, the paired end directive is optional.

Fortran

## Cross References

• allocators Construct, see Section 8.7

## 6.3.2 OpenMP Function Dispatch Structured Blocks

An OpenMP function-dispatch structured block is a context-specific structured block that is associated with a dispatch directive. It identifies the location of a function dispatch.

C / C++

A function-dispatch structured block is an expression statement with one of the following forms:

lvalue-expression = target-call ( [expression-list] );

or

target-call ( [expression-list] );

C / C++

Fortran

A function-dispatch structured block is an expression statement with one of the following forms, where expression can be a variable or a function reference with data pointer result:

expression = target-call ( [arguments] )

or

CALL target-call [ ( [arguments] )]

For a dispatch directive, the paired end directive is optional.

Fortran

## Restrictions

Restrictions to the function-dispatch structured blocks are as follows:

C++

• The target-call expression can only be a direct call.

C++

Fortran

• target-call must be a procedure name.

• target-call must not be a procedure pointer.

Fortran

## Cross References

• dispatch Construct, see Section 9.7
