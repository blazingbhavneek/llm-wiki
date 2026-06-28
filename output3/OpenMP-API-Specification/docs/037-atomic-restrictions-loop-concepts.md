
Restrictions to OpenMP atomic structured blocks are as follows:

```txt
C / C++
```

• In forms where e is assigned it must be an lvalue.

• r must be of integral type.

• During the execution of an atomic region, multiple syntactic occurrences of x must designate the same storage location.

• During the execution of an atomic region, multiple syntactic occurrences of r must designate the same storage location.

• During the execution of an atomic region, multiple syntactic occurrences of expr must evaluate to the same value.

• None of v, x, r, d and expr (as applicable) may access the storage location designated by any other symbol in the list.

• In forms that capture the original value of x in v, v and e may not refer to, or access, the same storage location.

• binop, binop=, ordop, ==, ++, and -- are not overloaded operators.

• The expression x binop expr must be numerically equivalent to x binop (expr). This requirement is satisfied if the operators in expr have precedence greater than binop, or by using parentheses around expr or subexpressions of expr.

• The expression expr binop x must be numerically equivalent to (expr) binop x. This requirement is satisfied if the operators in expr have precedence equal to or greater than binop, or by using parentheses around expr or subexpressions of expr.

• The expression x ordop expr must be numerically equivalent to x ordop (expr). This requirement is satisfied if the operators in expr have precedence greater than ordop, or by using parentheses around expr or subexpressions of expr.

• The expression expr ordop x must be numerically equivalent to (expr) ordop x. This requirement is satisfied if the operators in expr have precedence equal to or greater than ordop, or by using parentheses around expr or subexpressions of expr.

• The expression x == e must be numerically equivalent to x == (e). This requirement is satisfied if the operators in e have precedence equal to or greater than ==, or by using parentheses around e or subexpressions of e.

Fortran

• x must not have the ALLOCATABLE attribute.

• During the execution of an atomic region, multiple syntactic occurrences of x must designate the same storage location.

• During the execution of an atomic region, multiple syntactic occurrences of r must designate the same storage location.

• During the execution of an atomic region, multiple syntactic occurrences of expr must evaluate to the same value.

• None of v, x, d, r, expr, and expr-list (as applicable) may access the same storage location as any other symbol in the list.

• In forms that capture the original value of x in v, v may not access the same storage location as e.

• If intrinsic-procedure-name refers to IAND, IOR, IEOR, PREVIOUS, or NEXT then exactly one expression must appear in expr-list.

• The expression x operator expr must be, depending on its type, either mathematically or logically equivalent to x operator (expr). This requirement is satisfied if the operators in expr have precedence greater than operator, or by using parentheses around expr or subexpressions of expr.

• The expression expr operator x must be, depending on its type, either mathematically or logically equivalent to (expr) operator x. This requirement is satisfied if the operators in expr have precedence equal to or greater than operator, or by using parentheses around expr or subexpressions of expr.

• The expression x equalop e must be, depending on its type, either mathematically or logically equivalent to x equalop (e). This requirement is satisfied if the operators in e have precedence equal to or greater than equalop, or by using parentheses around e or subexpressions of e.

• intrinsic-procedure-name must refer to the intrinsic procedure name and not to other program entities.

• operator must refer to the intrinsic operator and not to a user-defined operator.

• Assignments must be either all intrinsic assignments or all pointer assignments.

• If the ASSOCIATED intrinsic function is referenced in a condition, all assignments must be pointer assignments. If pointer assignments are used, only the ASSOCIATED intrinsic function may be referenced in a condition.

• Unless x is a scalar variable or a function references with scalar data pointer result of non-character intrinsic type, intrinsic assignments, equalop, and ordop must not be used.

• Arguments to an ASSOCIATED intrinsic function must not have zero-sized storage sequences.

## Cross References

• atomic Construct, see Section 17.8.5

## 6.4 Loop Concepts

OpenMP semantics frequently involve loops that occur in the base language code. As detailed in this section, OpenMP defines several concepts that facilitate the specification of those semantics and their associated syntax.

## 6.4.1 Canonical Loop Nest Form

A loop nest has canonical loop nest form if it conforms to loop-nest in the following grammar:

loop-nest

One of the following:

for (init-expr; test-expr; incr-expr) loop-body

loop-nest

C / C++

or

for (range-decl: range-expr) loop-body

![](images/db996f652c14096ad7ecb313b54c5b77e5663093c7814b8a9aa78bfd0a91f0eb.jpg)

A range-based for loop is equivalent to a regular for loop using iterators, as defined in the base language. A range-based for loop has no loop-iteration variable.

C++

or

Fortran

DO [ label ] var = lb , ub [ , incr ]

[intervening-code]

loop-body

[intervening-code]

[ label ] END DO

If the loop-nest is a nonblock-do-construct, it is treated as a block-do-construct for each DO construct.

The value of incr is the increment of the loop. If not specified, its value is assumed to be 1.

or

BLOCK

loop-nest

END BLOCK

Fortran

![](images/a81ef4472cdc70c2ad371679a0928f599fadaa514cfe0f0b313e471f78e5bdd4.jpg)

loop-nest-generating-construct A loop-transforming construct that generates a canonical loop nest, which may be a canonical loop sequence that contains exactly one canonical loop nest.

25 generated-canonical-loop 26 A generated loop from a loop-transforming construct that has canonical loop nest 27 form and for which the loop body matches loop-body.

intervening-code

C / C++

A non-empty sequence of structured blocks or declarations, referred to as intervening code. It must not contain iteration statements, continue statements or break statements that apply to the enclosing loop.
