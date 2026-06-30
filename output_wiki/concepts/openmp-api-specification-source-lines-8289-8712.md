# OpenMP-API-Specification Source Lines 8289-8712

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source OpenMP-API-Specification:L8289-L8712

Citation: [OpenMP-API-Specification:L8289-L8712]

````text
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

Fortran

• Loop-iteration variables inside parallel, teams, taskgraph, or task-generating constructs are private in the innermost such construct that encloses the loop.

Fortran

C / C++

• Variables with static storage duration that are declared in a scope inside the construct are shared.

• If a list item in a has\_device\_addr clause or in a map clause on the target construct has a base pointer, and the base pointer is a scalar variable that is not a list item in a map clause on the construct, the base pointer is firstprivate

• If a list item in a reduction or in\_reduction clause on the construct has a base pointer then the base pointer is private.

• Static data members are shared.

• If a list item in a shared clause on the construct is a referencing variable then the referring pointer of the list item is firstprivate.

• If a list item in a map clause on the target construct has a base referencing variable that does not have a containing structure, the referring pointer of the base referencing variable is firstprivate.

• The \_\_func\_\_ variable and similar function-local predefined variables are shared.

C / C++ Fortran

• Assumed-size arrays and named constants are shared in constructs that are not data-mapping constructs.

• A named constant is firstprivate in target constructs.

• An associate name that may appear in a variable definition context is shared if its association occurs outside of the construct and otherwise it has the same data-sharing attribute as the selector with which it is associated.

• If a list item in a map clause on the target construct has a base referencing variable that is not the list item itself, the referring pointer of the base referencing variable is firstprivate unless that referencing variable is a structure element, a list item in an enter clause on a declare target directive, or a list item in a map clause on the construct where the semantics of the clause apply to its referring pointer.

## Fortran

• If a list item in a has\_device\_addr clause on the target construct has a base referencing variable, the referring pointer of the base referencing variable is firstprivate.

Variables with predetermined data-sharing attributes may not be listed in data-sharing clauses, except for the cases listed below. For these exceptions only, listing a predetermined variable in a data-sharing clause is allowed and overrides its predetermined data-sharing attributes.

• The loop-iteration variable in any afected loop of a loop-nest-associated directive may be listed in a private or lastprivate clause.

• If a simd construct has just one afected loop then its loop-iteration variable may be listed in a linear clause with a linear-step that is the increment of the afected loop.

## C / C++

• Variables with const-qualified type with no mutable members may be listed in a firstprivate clause, even if they are static data members.

• The \_\_func\_\_ variable and similar function-local predefined variables may be listed in a shared or firstprivate clause.

C / C++

Fortran

• A loop-iteration variable of a loop that is not associated with any directive may be listed in a data-sharing attribute clause on the surrounding teams, parallel or task-generating construct, and on enclosed constructs, subject to other restrictions.

• An assumed-size array may be listed in a shared clause.

• A named constant may be listed in a shared or firstprivate clause.

Fortran

Additional restrictions on the variables that may appear in individual clauses are described with each clause in Section 7.5.

Variables with explicitly determined data-sharing attributes are those that are referenced in a given construct and are listed in a data-sharing clause on the construct. Variables with implicitly determined data-sharing attributes are those that are referenced in a given construct and do not have predetermined data-sharing attributes or explicitly determined data-sharing attributes in that construct. Rules for variables with implicitly determined data-sharing attributes are as follows:

• In a parallel, teams, or task-generating construct, the data-sharing attributes of these variables are determined by the default clause, if present (see Section 7.5.1).

• In a parallel construct, if no default clause is present, these variables are shared.

• If no default clause is present on constructs that are not task-generating constructs, these variables reference the variables with the same names that exist in the enclosing context. If no default clause is present on a task-generating construct and the generated task is a sharing task, these variables are shared.

• In a target construct, variables that are not mapped after applying data-mapping attribute rules (see Section 7.9) are firstprivate.

• In an orphaned task-generating construct, if no default clause is present, formal arguments passed by reference are firstprivate.

C++

Fortran

• In an orphaned task-generating construct, if no default clause is present, dummy arguments are firstprivate.

Fortran

• In a task-generating construct, if no default clause is present, a variable for which the data-sharing attribute is not determined by the rules above is shared if the variable is determined to be shared by all implicit tasks bound to the current team in the enclosing context.

• In a task-generating construct, if no default clause is present, a variable for which the data-sharing attribute is not determined by the rules above is firstprivate.

An OpenMP program is non-conforming if a variable in a task-generating construct is implicitly determined to be firstprivate according to the above rules but is not permitted to appear in a firstprivate clause according to the restrictions specified in Section 7.5.4.

## 7.1.2 Variables Referenced in a Region but not in a Construct

The data-sharing attribute of a variable or object that is referenced in a region, but not in the corresponding construct, is determined by the first matching rule from the following list.

• Variables with automatic storage duration that are declared in called procedures in the region are private.

• Variables and common blocks (in Fortran) that appear as arguments in threadprivate directives or variables with the \_Thread\_local (in C) or thread\_local (in C/C++) storage-class specifier are threadprivate.

• Variables and common blocks (in Fortran) that appear as arguments in groupprivate directives are groupprivate.

• Variables and common blocks (in Fortran) that appear as list items in local clauses on declare\_target directives are device-local.

• Variables with static storage duration are shared.

• Objects with dynamic storage duration are shared.

## Fortran

• Variables that are accessed by host or use association are shared.

• A dummy argument of a called procedure in the region that does not have the VALUE attribute is private if the associated actual argument is not shared.

• A dummy argument of a called procedure in the region that does not have the VALUE attribute is shared if the actual argument is shared and it is a scalar variable, structure, an array that is not a pointer or assumed-shape array, or a simply contiguous array section. Otherwise, the data-sharing attribute of the dummy argument is implementation defined if the associated actual argument is shared.

Fortran

## 7.2 saved Modifier

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>saved</td><td>list</td><td>Keyword: saved</td><td>default</td></tr></table>

## Clauses

firstprivate

## Semantics

If the saved modifier is present in a data-environment attribute clause that is specified on a replayable construct then its original list items of a replay execution are defined by the saved data environment of the replayable construct. The saved modifier has no efect if specified in a clause that does not appear on a replayable construct.

## Cross References

• firstprivate Clause, see Section 7.5.4

• taskgraph Construct, see Section 14.3

## 7.3 threadprivate Directive

<table><tr><td>Name: threadprivateCategory: declarative</td><td>Association: explicitProperties: pure</td></tr></table>

## Arguments

threadprivate(list)

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

## Semantics

The threadprivate directive specifies that variables have the threadprivate attribute and therefore they are replicated with each thread having its own copy. Unless otherwise specified, each copy of a threadprivate variable is initialized once, in the manner specified by the program, but at an unspecified point in the program prior to the first reference to that copy. The storage of all copies of a threadprivate variable is freed according to how variables with static storage duration are handled in the base language, but at an unspecified point in the program.

C++

Each copy of a block-scope threadprivate variable that has a dynamic initializer is initialized the first time its thread encounters its definition; if its thread does not encounter its definition, whether it is initialized is unspecified. If it is initialized, its initialization occurs at an unspecified point in the program.

The content of a threadprivate variable can change across a task scheduling point if the executing thread switches to another task that modifies the variable. For more details on task scheduling, see Section 1.2 and Chapter 14.

In parallel regions, references by the primary thread are to the copy of the variable of the thread that encountered the parallel region.

During a sequential part, references are to the copy of the variable of the initial thread. The values of data in the copy for the initial thread are guaranteed to persist between any two consecutive references to the threadprivate variable in the program, provided that no teams construct that is not nested inside of a target construct is encountered between the references and that the initial thread is not executing code inside of a teams region. For initial threads that are executing code inside of a teams region, the values of data in the copies of a threadprivate variable for those initial threads are guaranteed to persist between any two consecutive references to the variable inside that teams region.

The values of data in the threadprivate variables of threads that are not initial threads are guaranteed to persist between two consecutive active parallel regions only if all of the following conditions hold:

• Neither parallel region is nested inside another explicit parallel region;

• The sizes of the teams used to execute both parallel regions are the same;

• The thread afinity policies used to execute both parallel regions are the same;

• The value of the dyn-var ICV in the enclosing task region is false at entry to both parallel regions;

• No teams construct that is not nested inside of a target construct is encountered between the parallel regions;

• No construct with an order clause that specifies concurrent is encountered between the parallel regions; and

• Neither the omp\_pause\_resource nor omp\_pause\_resource\_all routine is called.

If these conditions all hold, and if a threadprivate variable is referenced in both regions, then threads with the same thread number in their respective regions reference the same copy of that variable.

![](images/1ce4686592f533de1a9666912686ec04dddf994e932d1fe0f8af9a4f9c0ef944.jpg)

If the above conditions hold, the storage duration, lifetime, and value of a copy of a threadprivate variable that does not appear in any copyin clause on the corresponding construct of the second region spans the two consecutive active parallel regions. Otherwise, the storage duration, lifetime, and value of the copy of the variable in the second region is unspecified.

C / C++

## Fortran

If the above conditions hold, the definition, association, or allocation status of a copy of a threadprivate variable or a variable in a threadprivate common block that is not afected by any copyin clause that appears on the corresponding construct of the second region (a variable is afected by a copyin clause if the variable appears in the copyin clause or it is in a common block that appears in the copyin clause) spans the two consecutive active parallel regions. Otherwise, the definition and association status of a copy of the variable in the second region are undefined, and the allocation status of an allocatable variable are implementation defined.

If a threadprivate variable or a variable in a threadprivate common block is not afected by any copyin clause that appears on the corresponding construct of the first parallel region in which it is referenced, the copy of the variable inherits the declared type parameter and the default parameter values from the original variable. The variable or any subobject of the variable is initially defined or undefined according to the following rules:

• If it has the ALLOCATABLE attribute, each copy created has an initial allocation status of unallocated;

• If it has the POINTER attribute, each copy has the same association status as the initial association status; and

• If it does not have either the POINTER or the ALLOCATABLE attribute:

– If it is initially defined, either through explicit initialization or default initialization, each copy created is so defined;

– Otherwise, each copy created is undefined.

Fortran

The order in which any constructors for diferent threadprivate variables of class type are called is unspecified. The order in which any destructors for diferent threadprivate variables of class type are called is unspecified. A variable that is part of an aggregate variable may appear in a threadprivate directive only if it is a static data member of a C++ class.

C++
````
