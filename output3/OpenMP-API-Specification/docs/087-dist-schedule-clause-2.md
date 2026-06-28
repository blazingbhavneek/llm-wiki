## 13.7.1 dist\_schedule Clause

<table><tr><td>Name: dist_schedule</td><td>Properties: schedule-specification, unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>kind</td><td>Keyword: static</td><td>default</td></tr><tr><td>chunk_size</td><td>expression of integer type</td><td>ultimate, optional, positive, region-invariant</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

distribute

## Semantics

The dist\_schedule clause specifies how collapsed iterations of a distribute construct are divided into chunks, and how these chunks are distributed among the teams of the league. If chunk\_size is not specified, the collapsed iteration space is divided into chunks that are approximately equal in size, and at most one chunk is distributed to each initial team of the league. If the chunk\_size argument is specified, collapsed iterations are divided into chunks of chunk\_size iterations. The chunk\_size expression is evaluated using the original list items of any variables that become private variables in the distribute construct. Whether, in what order, or how many times, any side efects of the evaluation of this expression occur is unspecified. The use of a variable in a dist\_schedule clause expression of a distribute construct causes an implicit reference to the variable in all enclosing constructs. These chunks are assigned to the initial teams of the league in a round-robin fashion in the order of their team number.

## Restrictions

Restrictions to the dist\_schedule clause are as follows:

• The value of the chunk\_size expression must be the same for all teams in the league.

• The dist\_schedule clause cannot be specified if any of the collapsed loops is a non-rectangular loop.

## Cross References

• distribute Construct, see Section 13.7
