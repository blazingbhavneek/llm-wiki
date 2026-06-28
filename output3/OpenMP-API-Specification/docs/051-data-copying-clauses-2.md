## 7.8 Data Copying Clauses

This section describes the copyin clause and the copyprivate clause. These two clauses support copying data values from private variables or threadprivate variables of an implicit task or thread to the corresponding variables of other implicit tasks or threads in the team.

7.8.1 copyin Clause

<table><tr><td>Name: copyin</td><td>Properties: outermost-leaf, data copying</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

## Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

parallel

## Semantics

The copyin clause provides a mechanism to copy the value of a threadprivate variable of the primary thread to the threadprivate variable of each other member of the team that is executing the parallel region.

C / C++

The copy is performed after the team is formed and prior to the execution of the associated structured block. For variables of non-array type, the copy is by copy assignment. For an array of elements of non-array type, each element is copied as if by assignment from an element of the array of the primary thread to the corresponding element of the array of all other threads.

C / C++

C++

For class types, the copy assignment operator is invoked. The order in which copy assignment operators for diferent variables of the same class type are invoked is unspecified.

C++

Fortran

The copy is performed, as if by assignment, after the team is formed and prior to the execution of the associated structured block.

Named variables that appear in a threadprivate common block may be specified. The whole common block does not need to be specified.

On entry to any parallel region, the copy of each thread of a variable that is afected by a copyin clause for the parallel region will acquire the type parameters, allocation, association, and definition status of the copy of the primary thread, according to the following rules:

• If the original list item has the POINTER attribute, each copy receives the same association status as that of the copy of the primary thread as if by pointer assignment.

• If the original list item does not have the POINTER attribute, each copy becomes defined with the value of the copy of the primary thread as if by intrinsic assignment unless the list item has a type bound procedure as a defined assignment. If the original list item does not have the POINTER attribute but has the allocation status of unallocated, each copy will have the same status.

• If the original list item is unallocated or unassociated, each copy inherits the declared type parameters and the default type parameter values from the original list item.

Fortran

## Restrictions

Restrictions to the copyin clause are as follows:

• A list item that appears in a copyin clause must be threadprivate.

C++

• A variable of class type (or array thereof) that appears in a copyin clause requires an accessible, unambiguous copy assignment operator for the class type.

C++

Fortran

• A common block name that appears in a copyin clause must be declared to be a common block in the same scoping unit in which the copyin clause appears.

Fortran

## Cross References

• parallel Construct, see Section 12.1

## 7.8.2 copyprivate Clause

<table><tr><td>Name: copyprivate</td><td>Properties: innermost-leaf, end-clause, data copying</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

## Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

single

## Semantics

The copyprivate clause provides a mechanism to use a private variable to broadcast a value from the data environment of one implicit task to the data environments of the other implicit tasks that belong to the innermost enclosing parallel region. The efect of the copyprivate clause on the specified list items occurs after the execution of the structured block associated with the construct on which the clause is specified, and before any of the threads in the team have left the barrier at the end of the construct. To avoid data races, concurrent reads or updates of the list item must be synchronized with the update of the list item that occurs as a result of the copyprivate clause if, for example, the nowait clause is used to remove the barrier.

C / C++

In all other implicit tasks that belong to the parallel region, each specified list item becomes defined with the value of the corresponding list item in the implicit task associated with the thread that executed the structured block. For variables of non-array type, the definition occurs by copy assignment. For an array of elements of non-array type, each element is copied by copy assignment from an element of the array in the data environment of the implicit task that is associated with the thread that executed the structured block to the corresponding element of the array in the data environment of the other implicit tasks.

C / C++

C++

For class types, a copy assignment operator is invoked. The order in which copy assignment operators for diferent variables of class type are called is unspecified.

C++

Fortran

If a list item does not have the POINTER attribute then, in all other implicit tasks that belong to the parallel region, the list item becomes defined as if by intrinsic assignment with the value of the corresponding list item in the implicit task that is associated with the thread that executed the structured block. If the list item has a type bound procedure as a defined assignment, the assignment is performed by the defined assignment.

If the list item has the POINTER attribute then, in all other implicit tasks that belong to the parallel region, the list item receives, as if by pointer assignment, the same association status as the corresponding list item in the implicit task that is associated with the thread that executed the structured block.

The order in which any final subroutines for diferent variables of a finalizable type are called is unspecified.

## Fortran

## Restrictions

Restrictions to the copyprivate clause are as follows:

• All list items that appear in a copyprivate clause must be either threadprivate or private in the enclosing context.

C++

• A variable of class type (or array thereof) that appears in a copyprivate clause requires an accessible unambiguous copy assignment operator for the class type.

C++

Fortran

• A common block that appears in a copyprivate clause must be threadprivate.

• Pointers with the INTENT(IN) attribute must not appear in a copyprivate clause.

• Any list item with the ALLOCATABLE attribute must have the allocation status of allocated when the intrinsic assignment is performed.

Fortran

## Cross References

• List Item Privatization, see Section 7.4

• single Construct, see Section 13.1

• threadprivate Directive, see Section 7.3
