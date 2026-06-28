
Arguments

<table><tr><td>Name: counts</td><td>Properties: unique, required</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>count-list</td><td>list of OpenMP integer expression type</td><td>non-negative</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

split

## Semantics

For a given loop-transforming directive on which the clause appears, the counts clause specifies the manner in which the logical iteration space of the transformation-afected loop is subdivided into n partitions, where m is the number of list items in count-list and where each partition is associated with a generated loop of the directive. Specifically, each list item in count-list specifies the iteration count of one of the generated loops. List items in count-list are not required to be unique.

## Restrictions

Restrictions to the counts clause are as follows:

• A list item in count-list must be constant or omp\_fill.

## Cross References

• split Construct, see Section 11.6

## 11.7 stripe Construct

<table><tr><td>Name: stripeCategory:executable</td><td>Association: loop nestProperties: loop-transforming, order-concurrent-nestable, pure, simdizable, teams-nestable</td></tr></table>

Clauses

apply, sizes

Loop Modifiers for the apply Clause

<table><tr><td>loop-modifier</td><td>Number of Generated Loops</td><td>Description</td></tr><tr><td>offsets</td><td>m</td><td>the offsetting loops  $o_1, \dots, o_m$ </td></tr><tr><td>grid</td><td>m</td><td>the grid loops  $g_1, \dots, g_m$ </td></tr></table>

## Semantics

The stripe construct has m transformation-afected loops, where m is the number of list items in the size-list argument of the sizes clause, which consists of the list items $s _ { 1 } , \ldots , s _ { m }$ . The construct has the efect of striping the execution order of the logical iterations across the grid cells of the logical iteration space that result from the sizes clause. Let $\ell _ { 1 } , . . . , \ell _ { m }$ be the transformation-afected loops, from outermost to innermost, which the construct replaces with a canonical loop nest that consists of 2m perfectly nested loops. Let $o _ { 1 } , \ldots , o _ { m } , g _ { 1 } , \ldots , g _ { m }$ be the generated loops, from outermost to innermost. The loops $o _ { 1 } , \ldots , o _ { m }$ are the ofsetting loops and the loops $g _ { 1 } , \ldots , g _ { m }$ are the grid loops.

Let $n _ { 1 } , \ldots , n _ { m }$ be number of logical iterations of each afected loop and $O = \{ G _ { \alpha _ { 1 } , \dots , \alpha _ { m } } ~ | ~ \forall k \in \{ 1 , \dots , m \} : 0 \leq \alpha _ { 1 } < s _ { k } \}$ the logical iteration vector space of the ofsetting loops. The logical iteration $( i _ { 1 } , \ldots , i _ { m } )$ is executed in the logical iteration space of $G _ { i _ { 1 } }$ mod $s _ { 1 } , . . . , i _ { m }$ mod $s _ { m }$

The ofsetting loops iterate over all $G _ { \alpha _ { 1 } , \dots , \alpha _ { m } }$ in lexicographic order of their indices and the grid loops iterate over the logical iteration space in the lexicographic order of the corresponding logica iteration vectors.

If an ofsetting loop and a grid loop that are generated from the same stripe construct are afected loops of the same loop-nest-associated construct, the grid loops may execute additional empty logical iterations. The number of empty logical iterations is implementation defined.

## Restrictions

Restrictions to the stripe construct are as follows:

• The transformation-afected loops must be perfectly nested loops.

• No transformation-afected loops may be a non-rectangular loop.

## Cross References

• apply Clause, see Section 11.1

• Consistent Loop Schedules, see Section 6.4.4

• sizes Clause, see Section 11.2

## 11.8 tile Construct
