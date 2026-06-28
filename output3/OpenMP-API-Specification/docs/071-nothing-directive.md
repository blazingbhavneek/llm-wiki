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
