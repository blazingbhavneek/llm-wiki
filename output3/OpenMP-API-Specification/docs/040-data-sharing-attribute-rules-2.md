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
