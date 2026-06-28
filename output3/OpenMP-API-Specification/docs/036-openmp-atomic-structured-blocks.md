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
