
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
