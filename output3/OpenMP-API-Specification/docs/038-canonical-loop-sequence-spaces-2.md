C / C++

Fortran

A non-empty structured block sequence, referred to as intervening code. It must not contain:

• loops;

• CYCLE statements;

• EXIT statements;

• array expressions;

• array references with a vector subscript;

• assignment statements where the target is an array object;

• references to elemental procedures with an array actual argument;

• references to procedures where the actual argument is an array that is not simply contiguous and the corresponding dummy argument has the CONTIGUOUS attribute or is an explicit-shape array or assumed-size array.

Fortran

Additionally, intervening code must not contain executable directives or calls to the OpenMP runtime API in its corresponding region. If intervening code is present, then a loop at the same depth within the loop nest is not a perfectly nested loop.

## final-loop-body

A structured block that terminates the scope of loops in the loop nest. If the loop nest is associated with a loop-nest-associated directive, loops in this structured block cannot be associated with that directive.

![](images/bd32187051eb396b61ab57b42b1e94c6511d5148c3de93338600ea7f5b2cd362.jpg)

## init-expr

One of the following:

var = lb

integer-type var = lb

pointer-type var = lb

C++

random-access-iterator-type var = lb

C++

test-expr

One of the following:

var relational-op ub

ub relational-op var

relational-op

One of the following:

<=

>

>=

!=

incr-expr

One of the following:

++var

var++

\- - var

var - -

var += incr

var - = incr

var = var + incr

var = incr + var

var = var - incr

The value of incr, respectively 1 and -1 for the increment and decrement operators, is the increment of the loop.

C / C++

var

One of the following:

C / C++

A variable of a signed or unsigned integer type.

C / C++

C

A variable of a pointer type.

C++

A variable of a random access iterator type.

C++

Fortran

A scalar variable of integer type.

Fortran

The loop-iteration variable var must not be modified during the execution of intervening-code or loop-body in the loop.

lb, ub One of the following:

Expressions of a type compatible with the type of var that are loop invariant with respect to the outermost loop.

One of the following:

$$
\text{var - outer}
$$

$$
v a r - o u t e r + a 2
$$

$$
a 2 + v a r - o u t e r
$$

$$
v a r - o u t e r - a 2
$$

where var-outer is of a type compatible with the type of var.

If var is of an integer type, one of the following:

$$
a 2 - v a r - o u t e r
$$

$$
a 1 * \text {var - outer}
$$

$$
a 1 * v a r - o u t e r + a 2
$$

$$
a 2 + a 1 * v a r - o u t e r
$$

$$
a 1 * v a r - o u t e r - a 2
$$

$$
a 2 - a 1 * \text {var - outer}
$$

$$
v a r - o u t e r * a 1
$$

$$
v a r - o u t e r * a 1 + a 2
$$

$$
a 2 + v a r - o u t e r * a 1
$$

$$
v a r - o u t e r * a 1 - a 2
$$

$$
a 2 - v a r - o u t e r * a 1
$$

where var-outer is of an integer type.

lb and ub are loop bounds. A loop for which lb or ub refers to var-outer is a non-rectangular loop. If var is of an integer type, var-outer must be of an integer type with the same signedness and bit precision as the type of var.

The coeficient in a loop bound is 0 if the bound does not refer to var-outer. If a loop bound matches a form in which a1 appears, the coeficient is $_ { - a I }$ if the product of var-outer and a1 is subtracted from $^ { a 2 , }$ and otherwise the coeficient is $_ { a l . }$ . For other matched forms where a1 does not appear, the coeficient is −1 if var-outer is subtracted from $^ { a 2 , }$ and otherwise the coeficient is 1.

a1, a2, incr Integer expressions that are loop invariant with respect to the outermost loop of the loop nest.

If the loop is associated with a directive, the expressions are evaluated before the construct formed from that directive.

var-outer

The loop-iteration variable of a surrounding loop in the loop nest.

C++

range-decl A declaration of a variable as defined by the base language for range-based for loops.

range-expr An expression that is valid as defined by the base language for range-based for loops. It must be invariant with respect to the outermost loop of the loop nest and the iterator derived from it must be a random access iterator.

C++

## Restrictions

Restrictions to canonical loop nests are as follows:

C / C++

• If test-expr is of the form var relational-op b and relational-op is < or <= then incr-expr must cause var to increase on each iteration of the loop. If test-expr is of the form var relational-op b and relational-op is > or >= then incr-expr must cause var to decrease on each iteration of the loop. Increase and decrease are using the order induced by relational-op.

• If test-expr is of the form ub relational-op var and relational-op is < or <= then incr-expr must cause var to decrease on each iteration of the loop. If test-expr is of the form ub relational-op var and relational-op is > or >= then incr-expr must cause var to increase on each iteration of the loop. Increase and decrease are using the order induced by relational-op.

• If relational-op is != then incr-expr must cause var to always increase by 1 or always decrease by 1 and the increment must be a constant expression.

• final-loop-body must not contain any break statement that would cause the termination of the innermost loop.

C / C++ Fortran

• final-loop-body must not contain any EXIT statement that would cause the termination of the innermost loop.

Fortran

• A loop-nest must also be a structured block.

• For a non-rectangular loop, if var-outer is referenced in lb and ub then they must both refer to the same loop-iteration variable.

• For a non-rectangular loop, let $a _ { \mathrm { l b } }$ and $a _ { \mathrm { u b } }$ be the respective coeficients in lb and $u b ,$ $i n c r _ { \mathrm { i n n e r } }$ the increment of the non-rectangular loop and $i n c r _ { \mathrm { o u t e r } }$ the increment of the loop referenced by var-outer. $i n c r _ { \mathrm { i n n e r } } ( a _ { \mathrm { u b } } - a _ { \mathrm { l b } } )$ must be a multiple of incr<sub>outer</sub>.

• The loop-iteration variable may not appear in a threadprivate directive.

## Cross References

• Canonical Loop Sequence Form, see Section 6.4.2

• Loop-Transforming Constructs, see Chapter 11

• threadprivate Directive, see Section 7.3

## 6.4.2 Canonical Loop Sequence Form

A structured block has canonical loop sequence form if it conforms to canonical-loop-sequence in the following grammar:

canonical-loop-sequence

loop-sequence

![](images/668317e6925a0caf0bc90d70ca9e97ac0302fbe55695f102750eda984ede8621.jpg)

BLOCK loop-sequence END BLOCK

loop-sequence A structured block sequence with executable statements that match canonical-loop-sequence, loop-sequence-generating-construct, or loop-nest (a canonical loop nest as defined in Section 6.4.1). The loops must be bounds-independent loops with respect to canonical-loop-sequence.

![](images/657e8134a060a41a623f7d74d4eff89b5425b4ef8f195295405eeb95305c06b4.jpg)

loop-sequence-generating-construct

A loop-transforming construct that generates a canonical loop sequence or canonical loop nest.

The loop sequence length and consecutive order of canonical loop nests matched by loop-nest ignore how they are nested in canonical-loop-sequence or loop-sequence.

## Cross References

• looprange Clause, see Section 6.4.7

• Canonical Loop Nest Form, see Section 6.4.1

• Loop-Transforming Constructs, see Chapter 11

## 6.4.3 OpenMP Loop-Iteration Spaces and Vectors

A loop-nest-associated directive afects some number of the outermost loops of an associated loop nest, called the afected loops, in accordance with its specified clauses. These afected loops and their loop-iteration variables form an OpenMP loop-iteration vector space. OpenMP loop-iteration vectors allow other directives to refer to points in that loop-iteration vector space.

A loop-transforming construct that appears inside a loop nest is replaced according to its semantics before any loop can be associated with a loop-nest-associated directive that is applied to the loop nest. The loop nest depth is determined according to the loops in the loop nest, after any such replacements have taken place. A loop counts towards the loop nest depth if it is a base language loop statement or generated loop and it matches loop-nest while applying the production rules for canonical loop nest form to the loop nest.

The canonical loop nest form allows the iteration count of all afected loops to be computed before executing the outermost loop. For any afected loop, the iteration count is computed as follows:

• If var has a signed integer type and the var operand of test-expr after usual arithmetic conversions has an unsigned integer type then the loop iteration count is computed from lb, test-expr and incr using an unsigned integer type corresponding to the type of var.

• Otherwise, if var has an integer type then the loop iteration count is computed from lb, test-expr and incr using the type of var.

• If var has a pointer type then the loop iteration count is computed from lb, test-expr and incr using the type ptrdiff\_t.

C++

• If var has a random access iterator type then the loop iteration count is computed from lb, test-expr and incr using the type

std::iterator\_traits<random-access-iterator-type>::difference\_type.

• For range-based for loops, the loop iteration count is computed from range-expr using the type std::iterator\_traits<random-access-iterator-type>::difference\_type where random-access-iterator-type is the iterator type derived from range-expr.

C++

Fortran

• The loop iteration count is computed from lb, ub and incr using the type of var.

Fortran

The behavior is unspecified if any intermediate result required to compute the iteration count cannot be represented in the type determined above.

No synchronization is implied during the evaluation of the lb, ub, incr or range-expr expressions. Whether, in what order, or how many times any side efects within the lb, ub, incr, or range-expr expressions occur is unspecified.

Let the number of loops afected with a construct be n, where all of the afected loops have a loop-iteration variable. The OpenMP loop-iteration vector space is the n-dimensional space defined by the values of var<sub>i</sub>, $. 1 \leq i \leq n ,$ , the loop-iteration variables of the afected loops, with i = 1 referring to the outermost loop of the loop nest. An OpenMP loop-iteration vector, which may be used as an argument of OpenMP directives and clauses, then has the form:

$$
\text {var} _ {1} \left[ \pm \text {offset} _ {1} \right], \text {var} _ {2} \left[ \pm \text {offset} _ {2} \right], \dots , \text {var} _ {n} \left[ \pm \text {offset} _ {n} \right]
$$

where $o f f s e t _ { i }$ is a constant, non-negative expression of integer OpenMP type that facilitates identification of relative points in the loop-iteration vector space.

Alternatively, OpenMP defines a special keyword omp\_cur\_iteration that represents the current logical iteration. It enables identification of relative points in the logical iteration space with:

## omp\_cur\_iteration [± logical\_ofset]

where logical\_ofset is a constant, non-negative expression of integer OpenMP type.

The iterations of some number of afected loops can be collapsed into one larger logical iteration space that is the collapsed iteration space. The particular integer type used to compute the iteration count for the collapsed loop is implementation defined, but its bit precision must be at least that of the widest type that the implementation would use for the iteration count of each loop if it was the only afected loop. The number of times that any intervening code between any two collapsed loops will be executed is unspecified but will be the same for all intervening code at the same depth, at least once per iteration of the loop that encloses the intervening code and at most once per collapsed logical iteration. If the iteration count of any loop is zero and that loop does not enclose the intervening code, the behavior is unspecified.

At the beginning of each collapsed iteration in a loop-collapsing construct, the loop-iteration variable or the variable declared by range-decl of each collapsed loop has the value that it would have if the collapsed loops were not associated with any directive.
