
<table><tr><td>Name: tileCategory: executable</td><td>Association: loop nestProperties: loop-transforming, order-concurrent-nestable, pure, simdizable, teams-nestable</td></tr></table>

Clauses

apply, sizes

Loop Modifiers for the apply Clause

<table><tr><td>loop-modifier</td><td>Number of Generated Loops</td><td>Description</td></tr><tr><td>grid</td><td>m</td><td>the grid loops  $g_1, \dots, g_m$ </td></tr><tr><td>intratile</td><td>m</td><td>the tile loops  $t_1, \dots, t_m$ </td></tr></table>

## Semantics

The tile construct has m transformation-afected loops, where m is the number of list items in the size-list argument of the sizes clause, which consists of list items $s _ { 1 } , \ldots , s _ { m }$ . Let $\ell _ { 1 } , . . . , \ell _ { m }$ be the transformation-afected loops, from outermost to innermost, which the construct replaces with a canonical loop nest that consists of 2m perfectly nested loops. Let $g _ { 1 } , \ldots , g _ { m } , t _ { 1 } , \ldots , t _ { m }$ be the generated loops, from outermost to innermost. The loops $g _ { 1 } , \ldots , g _ { m }$ are the grid loops and the loops $t _ { 1 } , \ldots , t _ { m }$ are the tile loops.

<table><tr><td>Properties: exclusive</td><td>Members: full, partial</td></tr></table>

Let Ω be the logical iteration vector space of the transformation-afected loops. For any $( \alpha _ { 1 } , \ldots , \alpha _ { m } ) \in \mathbb { N } ^ { m }$ , define the set of iterations $\{ ( i _ { 1 } , \dotsc , i _ { m } ) \in \Omega | \forall k \in \{ 1 , \dotsc , m \} : s _ { k } \alpha _ { k } \leq i _ { k } < s _ { k } \alpha _ { k } + s _ { k } \}$ to be tile $T _ { \alpha _ { 1 } , \dots , \alpha _ { m } }$ and $G = \{ T _ { \alpha _ { 1 } , \dots , \alpha _ { m } } \ | \ T _ { \alpha _ { 1 } , \dots , \alpha _ { m } } \neq \emptyset \}$ to be the set of tiles with at least one iteration. Tiles that contain $\scriptstyle \prod _ { k = 1 } ^ { m } s _ { k }$ iterations are complete tile. Otherwise, they are partial tiles.

The grid loops iterate over all tiles $\{ T _ { \alpha _ { 1 } , \dots , \alpha _ { m } } \in G \}$ in lexicographic order with respect to their indices $\left( \alpha _ { 1 } , \ldots , \alpha _ { m } \right)$ and the tile loops iterate over the iterations in $T _ { \alpha _ { 1 } , \dots , \alpha _ { m } }$ in the lexicographic order of the corresponding iteration vectors. An implementation may reorder the sequential execution of two iterations if at least one is from a partial tile and if their respective logical iteration vectors in loop-nest do not have a product order relation.

If a grid loop and a tile loop that are generated from the same tile construct are afected loops of the same loop-nest-associated construct, the tile loops may execute additional empty logical iterations. The number of empty logical iterations is implementation defined.

## Restrictions

Restrictions to the tile construct are as follows:

• The transformation-afected loops must be perfectly nested loops.

• No transformation-afected loops may be a non-rectangular loop.

## Cross References

• apply Clause, see Section 11.1

• Consistent Loop Schedules, see Section 6.4.4

• sizes Clause, see Section 11.2

## 11.9 unroll Construct
