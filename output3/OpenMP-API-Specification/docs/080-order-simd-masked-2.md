
• lower-bound must be less than or equal to upper-bound.

## Cross References

• nteams-var ICV, see Table 3.1

• teams Construct, see Section 12.2

## 12.3 order Clause

<table><tr><td>Name: order</td><td>Properties: schedule-specification, unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>ordering</td><td>Keyword: concurrent</td><td>default</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>order-modifier</td><td>ordering</td><td>Keyword: reproducible, unconstrained</td><td>default</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

distribute, do, for, loop, simd

## Semantics

The order clause specifies an ordering of execution for the collapsed iterations of a loop-collapsing construct. If ordering is concurrent, diferent collapsed iterations may execute in any order, including in parallel, as if by the binding thread set of the region. The binding thread set may recruit or create additional native threads to participate in the parallel execution of any collapsed iterations.

The order-modifier on the order clause afects the schedule specification for the purpose of determining its consistency with other schedules (see Section 6.4.4). If order-modifier is reproducible, the loop schedule for the construct on which the clause appears is reproducible, whereas if order-modifier is unconstrained, the loop schedule is not reproducible.

## Restrictions

Restrictions to the order clause are as follows:

• The only routines for which a call may be nested inside a region that corresponds to a construct on which the order clause is specified with concurrent as the ordering argument are order-concurrent-nestable routines.

• Only regions that correspond to order-concurrent-nestable constructs or order-concurrent-nestable routines may be strictly nested regions of regions that correspond to constructs on which the order clause is specified with concurrent as the ordering argument.

• If a threadprivate variable is referenced inside a region that corresponds to a construct with an order clause that specifies concurrent, the behavior is unspecified.

## Cross References

• distribute Construct, see Section 13.7

• do Construct, see Section 13.6.2

• for Construct, see Section 13.6.1

• loop Construct, see Section 13.8

• simd Construct, see Section 12.4

## 12.4 simd Construct

<table><tr><td>Name: simdCategory: executable</td><td>Association: loop nestProperties: context-matching, order-concurrent-nestable, parallelism-generating, pure, simdizable</td></tr></table>

## Separating directives

scan

## Clauses

aligned, collapse, if, induction, lastprivate, linear, nontemporal, order, private, reduction, safelen, simdlen

## Binding

A simd region binds to the current task region. The binding thread set of the simd region is the current team.

## Semantics

The simd construct enables the execution of multiple collapsed iterations concurrently by using SIMD instructions. The number of collapsed iterations that are executed concurrently at any given time is implementation defined. Each concurrent iteration will be executed by a diferent SIMD lane. Each set of concurrent iterations is a SIMD chunk. Lexical forward dependences in the iterations of the original loop must be preserved within each SIMD chunk, unless an order clause that specifies concurrent is present.

When an if clause is present with an if-expression that evaluates to false, the preferred number of iterations to be executed concurrently is one, regardless of whether a simdlen clause is specified.

## Restrictions

Restrictions to the simd construct are as follows:

• If both simdlen and safelen clauses are specified, the value of the simdlen length must be less than or equal to the value of the safelen length.

• Only SIMDizable constructs may be encountered during execution of a simd region.

• If an order clause that specifies concurrent appears on a simd directive, the safelen clause must not also appear.

C / C++

• The simd region cannot contain calls to the longjmp or setjmp functions.

C / C++

C++

• No exceptions can be raised in the simd region.

• The only random access iterator types that are allowed for the collapsed loops are pointer types.

C++

## Cross References

• aligned Clause, see Section 7.12

• collapse Clause, see Section 6.4.5

• if Clause, see Section 5.5

• induction Clause, see Section 7.6.13

• lastprivate Clause, see Section 7.5.5

• linear Clause, see Section 7.5.6

• nontemporal Clause, see Section 12.4.1

• order Clause, see Section 12.3

• private Clause, see Section 7.5.3

• reduction Clause, see Section 7.6.10

• safelen Clause, see Section 12.4.2

• scan Directive, see Section 7.7

• simdlen Clause, see Section 12.4.3

## 12.4.1 nontemporal Clause

<table><tr><td>Name: nontemporal</td><td>Properties: default</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

simd

## Semantics

The nontemporal clause specifies that accesses to the storage locations to which the list items refer have low temporal locality across the logical iterations in which those storage locations are accessed. The list items of the nontemporal clause may also appear as list items of data-environment attribute clauses.

## Cross References

• simd Construct, see Section 12.4

## 12.4.2 safelen Clause

<table><tr><td>Name: safelen</td><td>Properties: unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>length</td><td>expression of integer type</td><td>positive, constant</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

simd

## Semantics

The safelen clause specifies that no two concurrent logical iterations within a SIMD chunk can have a distance in the collapsed iteration space that is greater than or equal to the length argument.

## Cross References

• simd Construct, see Section 12.4

## 12.4.3 simdlen Clause

<table><tr><td>Name: simdlen</td><td>Properties: unique</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>length</td><td>expression of integer type</td><td>positive, constant</td></tr></table>

## Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

declare\_simd, simd

## Semantics

When the simdlen clause appears on a simd construct, length is treated as a hint that specifies the preferred number of collapsed iterations to be executed concurrently. When the simdlen clause appears on a declare\_simd directive, if a SIMD version of the associated procedure is created, length corresponds to the number of concurrent arguments of the procedure.

Cross References

• declare\_simd Directive, see Section 9.8

• simd Construct, see Section 12.4

## 12.5 masked Construct

<table><tr><td>Name: maskedCategory: executable</td><td>Association: blockProperties: thread-limiting, thread-selecting</td></tr></table>

## Clauses

filter

## Binding

The binding thread set for a masked region is the current team. A masked region binds to the innermost enclosing parallel region.

## Semantics

The masked construct specifies a structured block that is executed by a subset of the threads of the current team. The filter clause selects a subset of the threads of the team that executes the binding parallel region to execute the structured block of the masked region. Other threads in the team do not execute the associated structured block. No implied barrier occurs either on entry to or exit from the masked construct. The result of evaluating the thread\_num argument of the filter clause may vary across threads.

If more than one thread in the team executes the structured block of a masked region, the structured block must include any synchronization required to ensure that data races do not occur.

## Execution Model Events

The masked-begin event occurs in any thread of a team that executes the masked region on entry to the region. The masked-end event occurs in any thread of a team that executes the masked region on exit from the region.

## Tool Callbacks

A thread dispatches a registered masked callback with ompt\_scope\_begin as its endpoint argument for each occurrence of a masked-begin event in that thread. Similarly, a thread dispatches a registered masked callback with ompt\_scope\_end as its endpoint argument for each occurrence of a masked-end event in that thread. These callbacks occur in the context of the task executed by the encountering thread.

## Cross References

• filter Clause, see Section 12.5.1

• masked Callback, see Section 34.3.3

• OMPT scope\_endpoint Type, see Section 33.27

## 12.5.1 filter Clause

<table><tr><td>Name: filter</td><td>Properties: unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>thread_num</td><td>expression of integer type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

## masked

## Semantics

If thread\_num specifies the thread number of the encountering thread in the current team then the filter clause selects the encountering thread. If the filter clause is not specified, the efect is as if the clause is specified with thread\_num equal to zero, so that the filter clause selects the primary thread. The use of a variable in a thread\_num argument expression causes an implicit reference to the variable in all enclosing constructs.

## Cross References

• masked Construct, see Section 12.5

# 13 Work-Distribution Constructs
