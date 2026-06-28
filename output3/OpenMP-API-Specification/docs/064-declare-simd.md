<table><tr><td>Name:declare_simdCategory:declarative</td><td>Association:declarationProperties:pure, variant-generating</td></tr></table>

## Arguments

declare\_simd[(proc-name)]

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>proc-name</td><td>identifier of function type</td><td>optional</td></tr></table>

## Clause groups

branch

## Clauses

aligned, linear, simdlen, uniform

## Additional information

The declare\_simd directive may alternatively be specified with declare simd as the directive-name.

## Semantics

The association of one or more declare\_simd directives with a procedure declaration or definition enables the creation of corresponding SIMD versions of the associated procedure that can be used to process multiple arguments from a single invocation in a SIMD loop concurrently.

If a SIMD version is created and the simdlen clause is not specified, the number of concurrent arguments for the function is implementation defined.

For purposes of the linear clause, any integer-typed parameter that is specified in a uniform clause on the directive is considered to be constant and so may be used in a step-complex-modifier as linear-step.

![](images/6d259ff53363d8adcebdcafb33398e1906c6c88fee21c8edc2a5f819afa05783.jpg)

C / C++

The expressions that appear in the clauses of each directive are evaluated in the scope of the arguments of the procedure declaration or definition.

C / C++

C++

The special this pointer can be used as if it was one of the arguments to the procedure in any of the linear, aligned, or uniform clauses.

C++

## Restrictions

Restrictions to the declare\_simd directive are as follows:

• The procedure body must be a structured block.

• The execution of the procedure, when called from a SIMD loop, must not result in the execution of any constructs except for atomic constructs and ordered constructs on which the simd clause is specified.

• The execution of the procedure must not have any side efects that would alter its execution for concurrent iterations of a SIMD chunk.

C / C++

• If a declare\_simd directive is specified for a declaration of a procedure then the definition of the procedure must have a declare\_simd directive with identical clauses with identical arguments and modifiers.

• The procedure must not contain calls to the longjmp or setjmp functions.

C / C++

• The procedure must not contain throw statements.

Fortran

• proc-name must not be a generic name, procedure pointer, or entry name.

• If proc-name is omitted, the declare\_simd directive must appear in the specification part of a subroutine subprogram or a function subprogram for which creation of the SIMD versions is enabled.

• Any declare\_simd directive must appear in the specification part of a subroutine subprogram, function subprogram, or interface body to which it applies.

• If a procedure is declared via a procedure declaration statement, the procedure proc-name should appear in the same specification.

• If a declare\_simd directive is specified for a procedure then the definition of the procedure must contain a declare\_simd directive with identical clauses with identical arguments and modifiers.

• Procedures pointers may not be used to access versions created by the declare\_simd directive.

Fortran

## Cross References

• aligned Clause, see Section 7.12

• linear Clause, see Section 7.5.6

• simdlen Clause, see Section 12.4.3

• uniform Clause, see Section 7.11

## 9.8.1 branch Clauses

Clause groups

<table><tr><td>Properties: exclusive, unique</td><td>Members:Clausesinbranch, notinbranch</td></tr></table>

## Directives

declare\_simd

## Semantics

The branch clause group defines a set of clauses that indicate if a procedure can be assumed to be or not to be encountered in a branch. If neither clause is specified, then the procedure may or may not be called from inside a conditional statement of the calling context.

## Cross References

• declare\_simd Directive, see Section 9.8

## 9.8.1.1 inbranch Clause

<table><tr><td>Name: inbranch</td><td>Properties: unique</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>inbranch</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

declare\_simd

## Semantics

If inbranch evaluates to true, the inbranch clause specifies that the procedure will always be called from inside a conditional statement of the calling context. If inbranch evaluates to false, the procedure may be called other than from inside a conditional statement. If inbranch is not specified, the efect is as if inbranch evaluates to true.

## Cross References

• declare\_simd Directive, see Section 9.8

## 9.8.1.2 notinbranch Clause

<table><tr><td>Name: notinbranch</td><td>Properties: unique</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>notinbranch</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

declare\_simd

## Semantics

If notinbranch evaluates to true, the notinbranch clause specifies that the procedure will never be called from inside a conditional statement of the calling context. If notinbranch evaluates to false, the procedure may be called from inside a conditional statement. If notinbranch is not specified, the efect is as if notinbranch evaluates to true.

## Cross References

• declare\_simd Directive, see Section 9.8
