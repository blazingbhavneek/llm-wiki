## 10.6 Assumption Directives

Diferent assumption directives facilitate definition of assumptions for a scope that is appropriate to each base language. The assumption scope of a particular format is defined in the section that defines that directive. If the invariants specified by the assumption directive do not hold at runtime, the behavior is unspecified.

## 10.6.1 assumption Clauses

## Clause groups

<table><tr><td>Properties: required, unique</td><td>Members:Clausesabsent, contains, holds,no_openmp, no_openmp_constructs,no_openmp_routines, no_parallelism</td></tr></table>

## Directives

assume, assumes, begin assumes

## Semantics

The assumption clause group defines a clause set that indicates the invariants that a program ensures the implementation can exploit.

The absent and contains clauses accept a directive-name list that may match a construct that is encountered within the assumption scope. An encountered construct matches the directive name if it or one of its constituent constructs has the same directive-name as one of the list items.

## Restrictions

The restrictions to assumption clauses are as follows:

• A directive-name list item must not specify a directive that is a declarative directive, an informational directive, or a metadirective.

## Cross References

• assume Directive, see Section 10.6.3

• assumes Directive, see Section 10.6.2

• begin assumes Directive, see Section 10.6.4

## 10.6.1.1 absent Clause

<table><tr><td>Name: absent</td><td>Properties: unique</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-list</td><td>list of directive-name list item type</td><td>default</td></tr></table>

## Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

assume, assumes, begin assumes

## Semantics

The absent clause specifies that the program guarantees that no construct that matches a directive-name list item is encountered in the assumption scope.

## Cross References

• assume Directive, see Section 10.6.3

• assumes Directive, see Section 10.6.2

• begin assumes Directive, see Section 10.6.4

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
