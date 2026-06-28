
<table><tr><td>Name: unrollCategory:executable</td><td>Association: loop nestProperties: generally-composable,loop-transforming, order-concurrent-nestable, pure, simdizable, teams-nestable</td></tr></table>

Clauses

apply, full, partial

Clause set

Loop Modifiers for the apply Clause

<table><tr><td>loop-modifier</td><td>Number of Generated Loops</td><td>Description</td></tr><tr><td>unrolled (default)</td><td>1</td><td>the grid loop  $g_{1}$  of the tiling step</td></tr></table>

## Semantics

The unroll construct has one transformation-afected loop, which is unrolled according to its specified clauses. If no clauses are specified, if and how the loop is unrolled is implementation defined. The unroll construct results in a generated loop that has canonical loop nest form if and only if the partial clause is specified.

## Restrictions

Restrictions to the unroll directive are as follows:

• The apply clause can only be specified if the partial clause is specified.

## Cross References

• apply Clause, see Section 11.1

• full Clause, see Section 11.9.1

• partial Clause, see Section 11.9.2

## 11.9.1 full Clause

<table><tr><td>Name: full</td><td>Properties: unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>fully_unroll</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

unroll

## Semantics

If fully\_unroll evaluates to true, the full clause specifies that the transformation-afected loop is fully unrolled. The construct is replaced by a structured block that only contains n instances of its loop body, one for each of the n afected iterations and in their logical iteration order. If fully\_unroll evaluates to false, the full clause has no efect. If fully\_unroll is not specified, the efect is as if fully\_unroll evaluates to true.

## Restrictions

Restrictions to the full clause are as follows:

• The iteration count of the transformation-afected loop must be constant.

## Cross References

• unroll Construct, see Section 11.9

## 11.9.2 partial Clause

<table><tr><td>Name: partial</td><td>Properties: unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>unroll-factor</td><td>expression of integer type</td><td>optional, constant, positive</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

unroll

## Semantics

The partial clause specifies that the transformation-afected loop is first tiled with a tile size of unroll-factor. Then, the generated tile loop is fully unrolled. If the partial clause is used without an unroll-factor argument then unroll-factor is an implementation defined positive integer.

## Cross References

• unroll Construct, see Section 11.9
