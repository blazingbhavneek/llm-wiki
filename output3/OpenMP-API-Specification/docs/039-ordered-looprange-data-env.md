
## 6.4.4 Consistent Loop Schedules

A loop schedule for a given loop-nest-associated construct assigns a thread in the binding thread set of that construct to a logical iteration vector of the afected loop nest. If the loop schedules of two loop-nest-associated constructs are consistent schedules, the behavior is as if they produce the same mapping of logical iteration vectors to threads. In particular, if two loop-nest-associated construct have consistent schedules and they have the same binding thread set, the implementation will guarantee that memory efects of a logical iteration in the first loop nest have completed before the execution of the corresponding logical iteration in the second loop nest.

Two loop-nest-associated constructs have consistent schedules if all of the following conditions hold:

• The constructs have the same directive-name;

• The regions that correspond to the two constructs have the same binding region;

• The constructs have the same schedule specification;

• The constructs have reproducible schedules;

• The afected loops have identical logical iteration vector spaces;

• The two sets of afected loops either consist of only rectangular loops or both contain a non-rectangular loop; and

• The loop schedules of transformation-afected loops among any afected loops that are generated loops of a loop-transforming construct are all themselves consistent.

## 6.4.5 collapse Clause

<table><tr><td colspan="2">Name: collapse</td><td colspan="2">Properties: once-for-all-constituents, unique</td></tr><tr><td colspan="4">Arguments</td></tr><tr><td>Name</td><td colspan="2">Type</td><td>Properties</td></tr><tr><td>n</td><td colspan="2">expression of integer type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

distribute, do, for, loop, simd, taskloop

## Semantics

The collapse clause afects one or more loops of a canonical loop nest on which it appears for the purpose of identifying the portion of the depth of the canonical loop nest to which to apply the work distribution semantics of the directive. The argument n specifies the number of loops of the associated loop nest to which to apply those semantics. On all directives on which the collapse clause may appear, the efect is as if a value of one was specified for n if the collapse clause is not specified.

## Restrictions

• n must not evaluate to a value greater than the loop nest depth.

## Cross References

• distribute Construct, see Section 13.7

• do Construct, see Section 13.6.2

• for Construct, see Section 13.6.1

• loop Construct, see Section 13.8

• simd Construct, see Section 12.4

• taskloop Construct, see Section 14.2

## 6.4.6 ordered Clause

<table><tr><td>Name: ordered</td><td>Properties: once-for-all-constituents, unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>n</td><td>expression of integer type</td><td>optional, constant, positive</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr><tr><td colspan="2">Name: looprange</td><td colspan="2">Properties: unique</td></tr><tr><td colspan="4">Arguments</td></tr><tr><td>Name</td><td colspan="2">Type</td><td>Properties</td></tr><tr><td>first</td><td colspan="2">expression of OpenMP integer type</td><td>constant, positive</td></tr><tr><td>count</td><td colspan="2">expression of OpenMP integer type</td><td>constant, positive, ultimate</td></tr></table>

Directives do, for

## Semantics

The ordered clause is used to specify the doacross-afected loops for the purpose of identifying cross-iteration dependences. The argument n specifies the number of doacross-afected loops to use for that purpose. If n is not specified then the behavior is as if n is specified with the same value as is specified for the collapse clause on the construct.

## Restrictions

• None of the doacross-afected loops may be non-rectangular loops.

• n must not evaluate to a value greater than the depth of the associated loop nest.

• If n is explicitly specified and the collapse clause is also specified for the ordered clause on the same construct, n must be greater than or equal to the n specified for the collapse clause.

## Cross References

• collapse Clause, see Section 6.4.5

• do Construct, see Section 13.6.2

• for Construct, see Section 13.6.1

## 6.4.7 looprange Clause

## Directives

fuse

## Semantics

For a loop-sequence-associated construct, the looprange clause determines the canonical loop nests of the associated loop sequence that are afected by the directive. The afected loop nests are the count consecutive canonical loop nests that begin with the canonical loop nest specified by the first argument.

For all directives on which the looprange clause may appear, if the clause is not specified then the efect is as if the clause was specified with a value equal to the loop sequence lengths of the associated canonical loop sequence.

## Restrictions

Restrictions to the looprange clause are as follows:

• f irst + count − 1 must not evaluate to a value greater than the loop sequence length of the associated canonical loop sequence.

## Cross References

• fuse Construct, see Section 11.3

• Canonical Loop Sequence Form, see Section 6.4.2

Part II

Directives and Clauses

## 7 Data Environment

This chapter presents directives and clauses for controlling data environments. These directives and clauses include the data-environment attribute clauses (or simply data-environment clauses), which explicitly determine the data-environment attributes of list items specified in an argument list. The data-environment clauses form a general clause set for which certain restrictions apply to their use on directives that accept any members of the set. In addition, these clauses are divided into two subsets that also form general clause sets: data-sharing attribute clauses (or simply data-sharing clauses) and data-mapping attribute clause (or simply data-mapping clauses). Additional restrictions apply to the use of these clause sets on directives that accept any members of them.

Data-sharing clauses control the data-sharing attributes of variables in a construct, indicating whether a variable is shared or private in the outermost scope of the construct. Any clause that indicates a variable is private in that scope is a privatization clause. Data-mapping clauses control the data-mapping attributes of variables in a data environment, indicating whether a variable is mapped from the data environment to another device data environment.

## 7.1 Data-Sharing Attribute Rules

This section describes how the data-sharing attributes of variables referenced in data environments are determined. The following two cases are described separately:

• Section 7.1.1 describes the data-sharing attribute rules for variables referenced in a construct.

• Section 7.1.2 describes the data-sharing attribute rules for variables referenced in a region, but outside any construct.

For any variable that is a referencing variable (including formal arguments passed by reference for C++), the data-sharing attribute rules apply only to its referring pointer unless otherwise specified.

## 7.1.1 Variables Referenced in a Construct

A variable that is referenced in a construct can have a predetermined data-sharing attribute, an explicitly determined data-sharing attribute, or an implicitly determined data-sharing attribute, according to the rules outlined in this section.

Specifying a variable in a copyprivate clause or a data-sharing attribute clause other than the private clause on a nested construct causes an implicit reference to the variable in the enclosing construct. Specifying a variable in a map clause of an enclosed construct may cause an implicit reference to the variable in the enclosing construct. Such implicit references are also subject to the data-sharing attribute rules outlined in this section.

## Fortran

A type parameter inquiry or complex part designator that is referenced in a construct is treated as if its designator is referenced.

Fortran

Certain variables and objects have predetermined data-sharing attributes for the construct in which they are referenced. The first matching rule from the following list of predetermined data-sharing attribute rules applies for variables and objects that are referenced in a construct.

• Variables with automatic storage duration that are declared in a scope inside the construct are private.

• Variables and common blocks (in Fortran) that appear as arguments in threadprivate directives or variables with the \_Thread\_local (in C) or thread\_local (in C/C++) storage-class specifier are threadprivate.

• Variables and common blocks (in Fortran) that appear as arguments in groupprivate directives are groupprivate.

• Variables and common blocks (in Fortran) that appear as list items in local clauses on declare\_target directives are device-local.

• Variables with static storage duration that are declared in a scope inside the construct are shared.

• Objects with dynamic storage duration are shared.

• The loop-iteration variable in any afected loop of a loop or simd construct is lastprivate.

• The loop-iteration variable in any afected loop of a loop-nest-associated directive is otherwise private.

C++

• The implicitly declared variables of a range-based for loop are private.

C++
