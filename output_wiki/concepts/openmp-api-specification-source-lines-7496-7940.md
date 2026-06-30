# OpenMP-API-Specification Source Lines 7496-7940

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source OpenMP-API-Specification:L7496-L7940

Citation: [OpenMP-API-Specification:L7496-L7940]

````text
## 6.3 Structured Blocks

This section specifies the concept of a structured block. A structured block:

• may contain infinite loops where the point of exit is never reached;

• may halt due to an IEEE exception;

C / C++

• may contain calls to exit(), \_Exit(), quick\_exit(), abort() or functions with a \_Noreturn specifier (in C) or a noreturn attribute (in C/C++);

• may be an expression statement, iteration statement, selection statement, or try block, provided that the corresponding compound statement obtained by enclosing it in { and } would be a structured block; and

C / C++

Fortran

• may contain STOP or ERROR STOP statements.

Fortran

C / C++

A structured block sequence that consists of no statements or more than one statement may appear only for executable directives that explicitly allow it. The corresponding compound statement obtained by enclosing the sequence in { and } must be a structured block and the structured block sequence then should be considered to be a structured block with all of its restrictions.

The remainder of this section covers OpenMP context-specific structured blocks that conform to specific syntactic forms and restrictions that are required for certain block-associated directives.

Restrictions

Restrictions to structured blocks are as follows:

• Entry to a structured block must not be the result of a branch.

• The point of exit cannot be a branch out of the structured block.

![](images/b3fe3cb78a86272f5ab6d947c0bfb9e57ca6f58ed19e236a04cea92d4e5494f0.jpg)

• The point of entry to a structured block must not be a call to setjmp.

• longjmp must not violate the entry/exit criteria of structured blocks.

C / C++

• throw, co\_await, co\_yield and co\_return must not violate the entry/exit criteria of structured blocks.

## Fortran

• If a BLOCK construct appears in a structured block, that BLOCK construct must not contain any ASYNCHRONOUS or VOLATILE statements, nor any specification statements that include the ASYNCHRONOUS or VOLATILE attributes.

Fortran

## 6.3.1 OpenMP Allocator Structured Blocks

Fortran

An OpenMP allocator structured block is a context-specific structured block that is associated with an allocators directive. It consists of allocate-stmt, where allocate-stmt is a Fortran ALLOCATE statement. For an allocators directive, the paired end directive is optional.

Fortran

## Cross References

• allocators Construct, see Section 8.7

## 6.3.2 OpenMP Function Dispatch Structured Blocks

An OpenMP function-dispatch structured block is a context-specific structured block that is associated with a dispatch directive. It identifies the location of a function dispatch.

C / C++

A function-dispatch structured block is an expression statement with one of the following forms:

lvalue-expression = target-call ( [expression-list] );

or

target-call ( [expression-list] );

C / C++

Fortran

A function-dispatch structured block is an expression statement with one of the following forms, where expression can be a variable or a function reference with data pointer result:

expression = target-call ( [arguments] )

or

CALL target-call [ ( [arguments] )]

For a dispatch directive, the paired end directive is optional.

Fortran

## Restrictions

Restrictions to the function-dispatch structured blocks are as follows:

C++

• The target-call expression can only be a direct call.

C++

Fortran

• target-call must be a procedure name.

• target-call must not be a procedure pointer.

Fortran

## Cross References

• dispatch Construct, see Section 9.7

## 6.3.3 OpenMP Atomic Structured Blocks

An OpenMP atomic structured block is a context-specific structured block that is associated with an atomic directive. The form of an atomic structured block depends on the atomic semantics that the directive enforces.

C / C++

Any instance of any atomic structured block in which any statement is enclosed in braces remains an instance of the same kind of atomic structured block.

C / C++

Fortran

Enclosing any instance of any atomic structured block in the pair of BLOCK and END BLOCK remains an instance of the same kind of atomic structured block, in which case the paired end directive is optional.

Fortran

In the following definitions:

C / C++

• x, r (result), and v (as applicable) are lvalue expressions with scalar type.

• e (expected) is an expression with scalar type.

• d (desired) is an expression with scalar type.

• e and v may refer to, or access, the same storage location.

• expr is an expression with scalar type.

• The order operation, ordop, is either < or >.

• binop is one of +, \*, -, /, &, ^, |, <<, or >>.

• == comparisons are performed by comparing the value representation of operand values for equality after the usual arithmetic conversions; if the object representation does not have any padding bits, the comparison is performed as if with memcmp.

• For forms that allow multiple occurrences of x, the number of times that x is evaluated is unspecified but will be at least one.

• For forms that allow multiple occurrences of expr, the number of times that expr is evaluated is unspecified but will be at least one.

• The number of times that r is evaluated is unspecified but will be at least one.

• Whether d is evaluated if x == e evaluates to false is unspecified.

C / C++

Fortran

• x and v (as applicable) are either scalar variables or function references with scalar data pointer result of non-character intrinsic type or variables that are non-polymorphic scalar pointers and any length type parameter must be constant.

• e (expected) and d (desired) are either scalar expressions or scalar variables.

• expr is a scalar expression or scalar variable.

• r (result) is a scalar logical variable.

• expr-list is a comma-separated, non-empty list of scalar expressions and scalar variables.

• intrinsic-procedure-name is one of MAX, MIN, IAND, IOR, IEOR, PREVIOUS, or NEXT.

• operator is one of +, \*, -, /, .AND., .OR., .EQV., or .NEQV..

• equalop is ==, .EQ., or .EQV..

• The order operation, ordop, is one of <, .LT., >, or .GT..

• == or .EQ. comparisons are performed by comparing the physical representation of operand values for equality after the usual conversions as described in the base language, while ignoring padding bits, if any.

• .EQV. comparisons are performed as described in the base language.

• For forms that allow multiple occurrences of x, the number of times that x is evaluated is unspecified but will be at least one.

• For forms that allow multiple occurrences of expr, the number of times that expr is evaluated is unspecified but will be at least one.

• The number of times that r is evaluated is unspecified but will be at least one.

• Whether d is evaluated if x equalop e evaluates to false is unspecified.

Fortran

A read structured block can be specified for atomic directives that enforce atomic read semantics but not capture semantics.

C / C++

A read structured block is read-expr-stmt, a read expression statement that has the following form:

v = x;

C / C++

Fortran

A read structured block is read-statement, a read statement that has one of the following forms:

v = x

v => x

Fortran

A write structured block can be specified for atomic directives that enforce atomic write semantics but not capture semantics.

C / C++

A write structured block is write-expr-stmt, a write expression statement that has the following form:

x = expr;

C / C++

Fortran

A write structured block is write-statement, a write statement that has one of the following forms:

x = expr

x => expr

Fortran

An update structured block can be specified for atomic directives that enforce atomic update semantics but not capture semantics.

C / C++

An update structured block is update-expr-stmt, an update expression statement that has one of the following forms:

x binop= expr;

x = x binop expr;

x = expr binop x;

C / C++

```txt
if(expr ordop x) x = expr;
if(x ordop expr) x = expr;
if(x == e) x = d;
```

## Fortran

An update structured block is update-statement, an update statement that has one of the following forms:

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
$x = x operator expr$ $x = expr operator x$ $x = intrinsic-procedure-name (x)$ $x = intrinsic-procedure-name (x, expr-list)$ $x = intrinsic-procedure-name (expr-list, x)$
</div>

A conditional-update structured block can be specified for atomic directives that enforce atomic conditional update semantics but not capture semantics.

A conditional-update structured block is either cond-expr-stmt, a conditional expression statement that has one of the following forms:

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
$x = expr ordop x ? expr : x;$ $x = x ordop expr ? expr : x;$ $x = x == e ? d : x;$
</div>

or cond-update-stmt, a conditional update statement that has one of the following forms:

A conditional-update structured block is conditional-update-statement, a conditional update statement that has one of the following forms:

```matlab
if (x equalop e) x = d
if (x equalop e) then; x = d; end if
x = ( x equalop e ? d : x )
if (x ordop expr) x = expr
if (x ordop expr) then; x = expr; end if
x = ( x ordop expr ? expr : x )
if (expr ordop x) x = expr
if (expr ordop x) then; x = expr; end if
x = ( expr ordop x ? expr : x )
if (associated(x)) x => expr
if (associated(x)) then; x => expr; end if
if (associated(x, e)) x => expr
if (associated(x, e)) then; x => expr; end if
```

For an atomic construct with a read structured block, write structured block, update structured block, or conditional-update structured block, the paired end directive is optional.

Fortran

A capture structured block can be specified for atomic directives that enforce capture semantics. It is further categorized as write-capture structured block, update-capture structured block, or conditional-update-capture structured block, which can be specified for atomic directives that enforce write, update or conditional update atomic semantics in addition to capture semantics.

C / C++

A capture structured block is capture-stmt, a capture statement that has one of the following forms:

```lisp
v = expr-stmt
{ v = x; expr-stmt }
{ expr-stmt v = x; }
```

If expr-stmt is write-expr-stmt or expr-stmt is update-expr-stmt as specified above then it is an update-capture structured block. If expr-stmt is cond-expr-stmt as specified above then it is a conditional-update-capture structured block. In addition, a conditional-update-capture structured block can have one of the following forms:

```lisp
{ v = x; cond-update-stmt }
{ cond-update-stmt v = x;    }
if(x == e) x = d; else v = x;
{ r = x == e; if(r) x = d; }
{ r = x == e; if(r) x = d; else v = x; }
```

C / C++

A capture structured block has one of the following forms:

statement capture-statement

or

capture-statement statement

where capture-statement has either of the following forms:

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
$\begin{array}{l}\text{\rm v} = \text{\rm x}\\ \text{\rm v} \Rightarrow \text{\rm x} \end{array}$
</div>

If statement is write-statement as specified above then it is a write-capture structured block. If statement is update-statement as specified above then it is an update-capture structured block and may be used in atomic constructs that enforce atomic captured update semantics. If statement is conditional-update-statement as specified above then it is a conditional-update-capture structured block. In addition, for a conditional-update-capture structured block, statement can have either of the following forms:

```txt
x = expr
x => expr
```

In addition, a conditional-update-capture structured block can have one of the following forms:

```txt
if (cond) then
    x assign d
else
    v assign x
end if
```

```txt
r = cond
if (r) x assign d
```

```txt
r = cond
if (r) then
    x assign d
else
    v assign x
endif
```

where assign is either = or => and cond denotes one of the following conditions:

```txt
x equalop e
ASSOCIATED (x)
ASSOCIATED (x, e)
```

## Restrictions

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
````
