# OpenMP-API-Specification Source Lines 13865-14220

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source OpenMP-API-Specification:L13865-L14220

Citation: [OpenMP-API-Specification:L13865-L14220]

````text
## 10.6.1.2 contains Clause

<table><tr><td>Name: contains</td><td>Properties: unique</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-list</td><td>list of directive-name list item type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

assume, assumes, begin assumes

## Semantics

The contains clause specifies that constructs that match the directive-name list items are likely to be encountered in the assumption scope.

## Cross References

• assume Directive, see Section 10.6.3

• assumes Directive, see Section 10.6.2

• begin assumes Directive, see Section 10.6.4

## 10.6.1.3 holds Clause

<table><tr><td>Name: holds</td><td>Properties: unique</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>hold-expr</td><td>expression of OpenMP logical type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

assume, assumes, begin assumes

## Semantics

When the holds clause appears on an assumption directive, the program guarantees that the listed expression evaluates to true in the assumption scope. The efect of the clause does not include any evaluation of the expression that afects the behavior of the program.

## Cross References

• assume Directive, see Section 10.6.3

• assumes Directive, see Section 10.6.2

• begin assumes Directive, see Section 10.6.4

## 10.6.1.4 no\_openmp Clause

<table><tr><td>Name: no_openmp</td><td>Properties: unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>can_assume</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

assume, assumes, begin assumes

## Semantics

If can\_assume evaluates to true, the no\_openmp clause implies the no\_openmp\_constructs clause and the no\_openmp\_routines clause. If can\_assume is not specified, the efect is as if can\_assume evaluates to true.

C++

The no\_openmp clause also guarantees that no thread will throw an exception in the assumption scope if it is contained in a region that arises from an exception-aborting directive.

C++

## Cross References

• assume Directive, see Section 10.6.3

• assumes Directive, see Section 10.6.2

• begin assumes Directive, see Section 10.6.4

## 10.6.1.5 no\_openmp\_constructs Clause

<table><tr><td>Name: no_openmp_constructs</td><td>Properties: unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>can_assume</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

assume, assumes, begin assumes

## Semantics

If can\_assume evaluates to true, the no\_openmp\_constructs clause guarantees that no constructs are encountered in the assumption scope. If can\_assume is not specified, the efect is as if can\_assume evaluates to true.

## Cross References

• assume Directive, see Section 10.6.3

• assumes Directive, see Section 10.6.2

• begin assumes Directive, see Section 10.6.4

## 10.6.1.6 no\_openmp\_routines Clause

<table><tr><td>Name: no_openmp_routines</td><td>Properties: unique</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>can_assume</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

assume, assumes, begin assumes

## Semantics

If can\_assume evaluates to true, the no\_openmp\_routines clause guarantees that no OpenMP API routines are executed in the assumption scope. If can\_assume is not specified, the efect is as if can\_assume evaluates to true.

## Cross References

• assume Directive, see Section 10.6.3

• assumes Directive, see Section 10.6.2

• begin assumes Directive, see Section 10.6.4

## 10.6.1.7 no\_parallelism Clause

<table><tr><td>Name: no_parallelism</td><td>Properties: unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>can_assume</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

assume, assumes, begin assumes

## Semantics

If can\_assume evaluates to true, the no\_parallelism clause guarantees that no parallelism-generating constructs will be encountered in the assumption scope. If can\_assume is not specified, the efect is as if can\_assume evaluates to true.

## Cross References

• assume Directive, see Section 10.6.3

• assumes Directive, see Section 10.6.2

• begin assumes Directive, see Section 10.6.4

## 10.6.2 assumes Directive

<table><tr><td>Name: assumesCategory: informational</td><td>Association: unassociatedProperties: pure</td></tr></table>

## Clause groups

assumption

## Semantics

The assumption scope of the assumes directive is the code executed and reached from the current compilation unit.

Fortran

Referencing a module that has an assumes directive in its specification part does not have the efect as if the assumes directive appeared in the specification part of the referencing scope.

## Restrictions

Fortran

The restrictions to the assumes directive are as follows:

• The assumes directive must only appear at file scope.

C++

• The assumes directive must only appear at file or namespace scope.

C++

Fortran

• The assumes directive must only appear in the specification part of a module or subprogram, after all USE statements, IMPORT statements, and IMPLICIT statements.

Fortran

## 10.6.3 assume Directive

<table><tr><td>Name: assumeCategory: informational</td><td>Association: blockProperties: pure</td></tr></table>

## Clause groups

assumption

## Semantics

The assumption scope of the assume directive is the corresponding region and any nested region of that region.

C / C++

## 10.6.4 begin assumes Directive

<table><tr><td>Name: begin assumesCategory: informational</td><td>Association: delimitedProperties: default</td></tr></table>

## Clause groups

assumption

## Semantics

The assumption scope of the begin assumes directive is the code that is executed and reached from any of the declared functions in the delimited code region. The delimited code region is a declaration sequence.

C / C++

## 10.7 nothing Directive

<table><tr><td>Name: nothingCategory: utility</td><td>Association: unassociatedProperties: pure, loop-transforming</td></tr></table>

## Clauses

apply

Loop Modifiers for the apply Clause

<table><tr><td>loop-modifier</td><td>Number of Generated Loops</td><td>Description</td></tr><tr><td>identity (default)</td><td>1</td><td>the copy of the transformation-affected loop</td></tr></table>

## Semantics

The nothing directive has no efect on the execution of the OpenMP program unless otherwise specified by the apply clause.

If the nothing directive immediately precedes a canonical loop nest then it forms a loop-transforming construct. It is associated with the outermost loop and generates one loop that has the same logical iterations in the same order as the transformation-afected loop.

## Restrictions

• The apply clause can be specified if and only if the nothing directive forms a loop-transforming construct.

## Cross References

• apply Clause, see Section 11.1

• Loop-Transforming Constructs, see Chapter 11

# 11 Loop-Transforming Constructs

A loop-transforming construct replaces itself, including its associated loop nest (see Section 6.4.1) or associated loop sequence (see Section 6.4.2), with a structured block that may be another loop nest or loop sequence. If the replacement of a loop-transforming construct is another loop nest or sequence, that loop nest or sequence, possibly as part of an enclosing loop nest or sequence, may be associated with another loop-nest-associated directive or loop-sequence-associated directive. A nested loop-transforming construct and any loop-transforming constructs that result from its apply clauses are replaced before any enclosing loop-transforming construct.

A loop-sequence-transforming construct generates a canonical loop sequence from its associated canonical loop sequence. The canonical loop nests that precede or follow the afected loop nests in the associated canonical loop sequence will respectively precede or follow, in the generated canonical loop sequence, the generated loop nest or generated loop sequence that replaces the afected loop nests.

All generated loops have canonical loop nest form, unless otherwise specified. Loop-iteration variables of generated loops are always private in the innermost enclosing parallelism-generating construct.

At the beginning of each logical iteration, the loop-iteration variable or the variable declared by range-decl has the value that it would have if the transformation-afected loop was not associated with any directive. After the execution of the loop-transforming construct, the loop-iteration variables of any of its transformation-afected loops have the values that they would have without the loop-transforming directive.

## Restrictions

The following restrictions apply to loop-transforming constructs:

• The replacement of a loop-transforming construct with its generated loop nests or generated loop sequences must result in a conforming program.

• A generated loop of a loop-transforming construct must not be a doacross-afected loop.

• The arguments of any clauses on a loop-transforming construct must not refer to loop-iteration variables of surrounding loops in the same canonical loop nest.

• The lb and ub expressions of an afected loop (see Section 6.4.1) may only reference the loop-iteration variable of an enclosing loop afected by a loop-transforming construct if that loop-transforming construct has the nonrectangular-compatible property.

• A generated loop of a loop-transforming construct may only be a non-rectangular afected loop of an enclosing loop-nest-associated directive if that loop-transforming construct has the nonrectangular-compatible property.

## Cross References

• Canonical Loop Nest Form, see Section 6.4.1

## 11.1 apply Clause

<table><tr><td>Name: apply</td><td>Properties: default</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>applied-directives</td><td>list of directive specification list item type</td><td>default</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>loop-modifier</td><td>applied-directives</td><td>Complex, Keyword: fused, grid, identity, interchanged, intratile, offsets, reversed, split, unrolledArguments: indices list of expression of integer type (optional)</td><td>optional</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

fuse, interchange, nothing, reverse, split, stripe, tile, unroll

## Semantics

The apply clause applies loop-nest-associated constructs, specified by the applied-directives list, to generated loops of a loop-transforming construct. The loop-modifier specifies to which generated loops the directives are applied. If the loop-transforming construct generates a canonical loop sequence, the generated loops to which the directives are applied are the outermost loops of each generated loop nest. An applied loop-transforming construct may also specify apply clauses.

The valid loop-modifier keywords, the default loop-modifier if it exists, the number of applied-directives list items, and the target of each applied-directives list item is defined by the loop-transforming construct to which it applies. Each of the indices in the argument of the loop-modifier specifies the position of the generated loop to which the respective applied-directives item is applied.

If the loop-modifier is specified with no argument, the behavior is as if the list 1, 2, . . . , m is specified, where m is the number of generated loops according to the specification of the loop-modifier keyword. If the loop-modifier is omitted and a default loop-modifier exists for the apply clause on the construct, the behavior is as if the default loop-modifier with the argument 1, 2, . . . , m is specified.

The list items of the apply clause arguments are not required to be directive-wide unique.

## Restrictions

Restrictions to the apply clause are as follows:

• Each list item in the applied-directives list of any apply clause must be nothing or the directive-specification of a loop-nest-associated construct.

• The loop-transforming construct on which the apply clause is specified must either have the generally-composable property or every list item in the applied-directives list of any apply clause must be the directive-specification of a loop-transforming directive.

• Every list item in the applied-directives list of any apply clause that is specified on a loop-transforming construct that is itself specified as a list item in the applied-directives list of another apply clause must be the directive-specification of a loop-transforming directive.

• For a given loop-modifier keyword, every indices list item may appear at most once in any apply clause on the directive.

• Every indices list item must be a positive constant less than or equal to m, the number of generated loops according to the specification of the loop-modifier keyword.

• The list items in indices must be in ascending order.

• If a directive does not define a default loop-modifier keyword, a loop-modifier is required.

## Cross References

• fuse Construct, see Section 11.3

• interchange Construct, see Section 11.4

• metadirective, see Section 9.4.3

• nothing Directive, see Section 10.7

• reverse Construct, see Section 11.5

• split Construct, see Section 11.6

• stripe Construct, see Section 11.7

• tile Construct, see Section 11.8

• unroll Construct, see Section 11.9
````
