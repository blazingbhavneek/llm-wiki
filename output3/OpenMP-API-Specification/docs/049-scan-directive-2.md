## 7.7 scan Directive

<table><tr><td>Name: scanCategory: subsidiary</td><td>Association: separatingProperties: pure</td></tr></table>

## Separated directives

do, for, simd

## Clauses

exclusive, inclusive, init\_complete

Clause set

<table><tr><td>Properties: unique, required, exclusive</td><td>Members: exclusive, inclusive, init_complete</td></tr></table>

## Semantics

The scan directive is a subsidiary directive that separates the final-loop-body of an enclosing simd construct or worksharing-loop construct (or a composite construct that combines them) into structured block sequences that represent diferent phases of a scan computation. The use of scan directives results in a structured block sequence that serves as an input phase, a structured block sequence that serves as a scan phase, and, optionally, a structured block sequence that serves as an initialization phase. The optional initialization phase begins the collapsed iteration by initializing private variables that can be used in the input phase, the input phase contains all computations that update the list item in the collapsed iteration, and the scan phase ensures that any statement that reads the list item uses the result of the scan computation for that collapsed iteration. Thus, the scan directive specifies that a scan computation updates each list item on each collapsed iteration of the enclosing canonical loop nest that is associated with the separated construct.

The clause that is specified on the scan directive determines the phases of the scan computation that correspond to the structured block sequences that precede and follow the directive.

The result of a scan computation for a given collapsed iteration is calculated according to the last generalized prefix sum $\left( \mathrm { P R E S U M _ { \mathrm { 1 a s t } } } \right)$ applied over the sequence of values given by the value of the original list item prior to the afected loops and all preceding updates to the new list item in the collapsed iteration space. The operation $\mathtt { P R E S U M _ { \mathrm { 1 a s t } } } ( o p , a _ { 1 } , . . . , a _ { \mathrm { N } } )$ is defined for a given binary operator op and a sequence of N values $a _ { 1 } , . . . , a _ { \mathrm { N } }$ as follows:

• if $N = 1 , a _ { 1 }$

$$
\begin{array}{l} \bullet \text {if} N > 1, o p (\text {PRESUM} _ {\text {last}} (o p, a _ {1}, \dots , a _ {\mathrm{j}}), \text {PRESUM} _ {\text {last}} (o p, a _ {\mathrm{k}}, \dots , a _ {\mathrm{N}})), \\ 1 \leq j + 1 = k \leq N. \end{array}
$$

At the beginning of the input phase of each collapsed iteration, the new list item is either initialized with the value of the initializer expression of the reduction-identifier specified by the reduction clause on the separated construct or with the value of the list item in the scan phase of some collapsed iteration. The update value of a new list item is, for a given collapsed iteration, the value the new list item would have on completion of its input phase if it were initialized with the value of the initializer expression.

Let orig-val be the value of the original list item on entry to the separated construct. Let combiner be the combiner expression for the reduction-identifier specified by the reduction clause on the construct. Let $u _ { \mathrm { i } }$ be the update value of a list item for collapsed iteration i. For list items that appear in an inclusive clause on the scan directive, at the beginning of the scan phase for collapsed iteration i the new list item is assigned the result of the operation $\mathtt { P R E S U M _ { l a s t } } ($ ( combiner, orig-val, $u _ { 0 } , \ldots , u _ { \mathrm { i } } )$ . For list items that appear in an exclusive clause on the scan directive, at the beginning of the scan phase for collapsed iteration i = 0 the list item is assigned the value orig-val, and at the beginning of the scan phase for collapsed iteration $i > 0$ the list item is assigned the result of the operation $\mathtt { P R E S U M _ { \mathrm { 1 a s t } } } ( $ ( combiner, orig-val, $u _ { 0 } , \ldots , u _ { \mathrm { i - 1 } } )$

For list items that appear in an inclusive clause, at the end of the separated construct, the original list item is assigned the value of the private copy from the last collapsed iteration of the afected loops of the separated construct. For list items that appear in an exclusive clause, let k be the last collapsed iteration of the afected loops of the separated construct. At the end of the separated construct, the original list item is assigned the result of the operation PRESUM<sub>last</sub>( combiner, orig-val, u , . . . , u ).

## Restrictions

Restrictions to the scan directive are as follows:

• The separated construct must have at most one scan directive with an inclusive or exclusive clause as a separating directive.

• The separated construct must have at most one scan directive with an init\_complete clause as a separating directive.

• If specified, a scan directive with an init\_complete clause must precede a scan directive with an exclusive clause that is a subsidiary directive of the same construct.

• The afected loops of the separated construct must all be perfectly nested loops.

• Each list item that appears in the inclusive or exclusive clause must appear in a reduction clause with the inscan modifier on the separated construct.

• Each list item that appears in a reduction clause with the inscan modifier on the separated construct must appear in a clause on the scan separating directive.

• Cross-iteration dependences across diferent collapsed iterations of the separated construct must not exist, except for dependences for the list items specified in an inclusive or exclusive clause.

• Intra-iteration dependences from a statement in the structured block sequence that immediately precedes a scan directive with an inclusive or exclusive clause to a statement in the structured block sequence that follows that scan directive must not exist, except for dependences for the list items specified in that clause.

• The private copy of a list item that appears in the inclusive or exclusive clause must not be modified in the scan phase.

• Any list item that appears in an exclusive clause must not be modified or used in the initialization phase.

• Statements in the initialization phase must only modify private variables. Any private variables modified in the initialization phase must not be used in the scan phase.

## Cross References

• do Construct, see Section 13.6.2

• exclusive Clause, see Section 7.7.2

• for Construct, see Section 13.6.1

• inclusive Clause, see Section 7.7.1

• init\_complete Clause, see Section 7.7.3

• reduction Clause, see Section 7.6.10

• simd Construct, see Section 12.4
