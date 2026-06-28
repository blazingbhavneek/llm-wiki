
• loop Construct, see Section 13.8

• ordered Clause, see Section 6.4.6

• parallel Construct, see Section 12.1

• private Clause, see Section 7.5.3

• scan Directive, see Section 7.7

• schedule Clause, see Section 13.6.3

• scope Construct, see Section 13.2

• sections Construct, see Section 13.3

• simd Construct, see Section 12.4

• taskloop Construct, see Section 14.2

• teams Construct, see Section 12.2

## 7.6.11 task\_reduction Clause

<table><tr><td>Name: task_reduction</td><td>Properties: data-environment attribute, data-sharing attribute, original list-item updating, privatization, reduction scoping</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>reduction-identifier</td><td>all arguments</td><td>An OpenMP reduction iden-tifier</td><td>required, ultimate</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

taskgroup

## Semantics

The task\_reduction clause is a reduction-scoping clause, as described in Section 7.6.7, that specifies a task reduction. For each list item, the number of copies is unspecified. Any copies associated with the reduction are initialized before they are accessed by the tasks that participate in the reduction. After the end of the region, the original list item contains the result of the reduction.

## Restrictions

Restrictions to the task\_reduction clause are as follows:

• All restrictions common to all reduction clauses, as listed in Section 7.6.5 and Section 7.6.6, apply to this clause.

## Cross References

• taskgroup Construct, see Section 17.4

## 7.6.12 in\_reduction Clause

<table><tr><td>Name: in_reduction</td><td>Properties: data-environment attribute, data-sharing attribute, privatization, reduction participating</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>reduction-identifier</td><td>all arguments</td><td>An OpenMP reduction iden-tifier</td><td>required, ultimate</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

target, target\_data, task, taskloop

## Semantics

The in\_reduction clause is a reduction-participating clause, as described in Section 7.6.8, that specifies that a task participates in a reduction. For a given list item, the in\_reduction clause defines a task to be a participant in a task reduction that is defined by an enclosing region for a matching list item that appears in a task\_reduction clause or a reduction clause with the task reduction-modifier, where either:

1. The matching list item has the same storage location as the list item in the in\_reduction clause; or

2. A private copy, derived from the matching list item, that is used to perform the task reduction has the same storage location as the list item in the in\_reduction clause.

For the task construct, the generated task becomes the participating task. For each list item, a private copy may be created as if the private clause had been used.

For the target construct, the target task becomes the participating task. For each list item, a private copy may be created in the data environment of the target task as if the private clause had been used. This private copy will be implicitly mapped into the device data environment of the target device, if the target device is not the parent device.

At the end of the task region, if a private copy was created its value is combined with a copy created by a reduction-scoping clause or with the original list item.

When specified on the target\_data directive, the in\_reduction clause has the all-data-environments property.

## Restrictions

Restrictions to the in\_reduction clause are as follows:

• All restrictions common to all reduction clauses, as listed in Section 7.6.5 and Section 7.6.6, apply to this clause.

• For each list item, a matching list item must exist that appears in a task\_reduction clause or a reduction clause with the task reduction-modifier that is specified on a construct that corresponds to a region in which the region of the participating task is closely nested. The construct that corresponds to the innermost enclosing region that meets this condition must specify the same reduction-identifier for the matching list item as the in\_reduction clause.

## Cross References

• target Construct, see Section 15.8

• target\_data Construct, see Section 15.7

• task Construct, see Section 14.1

• taskloop Construct, see Section 14.2

## 7.6.13 induction Clause

<table><tr><td>Name: induction</td><td>Properties: data-environment attribute, data-sharing attribute, original list-item updating, privatization</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

## Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>induction-identifier</td><td>list</td><td>OpenMP induction identifier</td><td>required, ultimate</td></tr><tr><td>step-modifier</td><td>list</td><td>Complex, name: stepArguments:induction-step expression of induction-step type (region-invariant)</td><td>required</td></tr><tr><td>induction-modifier</td><td>list</td><td>Keyword: relaxed, strict</td><td>default</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

distribute, do, for, simd, taskloop

## Semantics

The induction clause provides a superset of the functionality provided by the private clause. A list item that appears in an induction clause is subject to the private clause semantics described in Section 7.5.3, except as otherwise specified. The new list items have the induction attribute.

When an induction clause is specified on a loop-nest-associated directive and the strict induction-modifier is present, the value of the new list item at the beginning of each collapsed iteration is determined by the closed form of the induction operation. The value of the original list item at the end of the last collapsed iteration is the result of applying the inductor expression to the value of the new list item at the beginning of that collapsed iteration. When the relaxed induction-modifier is present, the implementation may assume that the value of the new list item at the end of the previous collapsed iteration, if executed by the same task or SIMD lane, is the value determined by the closed form of the induction operation. When an induction-modifier is not specified, the behavior is as if the relaxed induction-modifier is present.

The value of the new list item at the end of the last collapsed iteration is assigned to the original list item.

C++

For class types, the copy assignment operator is invoked. The order in which copy assignment operators for diferent variables of the same class type are invoked is unspecified.

C++

C / C++

For an array of elements of non-array type, each element is assigned to the corresponding element of the original array.

C / C++

![](images/36e992e6788475c5c247acbe3efa00157e216c94d79a2b0390a48f3dc1506620.jpg)

## Fortran

If the original list item does not have the POINTER attribute, its update occurs as if by intrinsic assignment unless it has a type bound procedure as a defined assignment.

If the original list item has the POINTER attribute, its update occurs as if by pointer assignment.

## Fortran

If the construct is a worksharing-loop construct with the nowait clause present and the original list item is shared in the enclosing context, access to the original list item after the construct may create a data race. To avoid this data race, user code must insert synchronization.

The induction-identifier must match a previously declared induction identifier of the same name and type for each of the list items and for the induction-step-expr. This match is done by means of a name lookup in the base language.

## Restrictions

Restrictions to the induction clause are as follows:

• All restrictions listed in Section 7.6.5 apply to this clause.

• The induction-step must not be an array or array section.

• If an array section or array element appears as a list item in an induction clause on a worksharing construct, all threads of the team must specify the same storage location.

• None of the afected loops of a loop-nest-associated construct that has an induction clause may be a non-rectangular loop.

## C / C++

• If a list item in an induction clause on a worksharing construct has a reference type and the original list item is shared in the enclosing context then it must bind to the same object for all threads of the team.

• If a list item in an induction clause on a worksharing construct is an array section or an array element that has a base pointer and the original list item is shared in the enclosing context, the base pointer must point to the same variable for all threads of the team.

## Cross References

• distribute Construct, see Section 13.7

• do Construct, see Section 13.6.2

• for Construct, see Section 13.6.1

• List Item Privatization, see Section 7.4

• private Clause, see Section 7.5.3

• simd Construct, see Section 12.4

![](images/02e249e46ef0c8579181ffc228b3e6e4cd1ba6e88ae6f6323892a25123f5acdb.jpg)

## 7.6.14 declare\_reduction Directive

<table><tr><td>Name:declare_reductionCategory:declarative</td><td>Association:unassociatedProperties:pure</td></tr></table>

## Arguments

declare\_reduction(reduction-specifier)

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>reduction-specifier</td><td>OpenMP reduction specifier</td><td>default</td></tr></table>

## Clauses

combiner, initializer

## Additional information

The declare\_reduction directive may alternatively be specified with declare reduction as the directive-name.

The syntax reduction-identifier : typename-list : combiner-expr, where combiner is an OpenMP combiner expression, may alternatively be used for reduction-specifier. The combiner clause must not be specified if this syntax is used. This syntax has been deprecated.

## Semantics

The declare\_reduction directive declares a reduction identifier that can be used in a reduction clause as a user-defined reduction. The directive argument reduction-specifier uses the following syntax:

reduction-identifier : typename-list

where reduction-identifier is a reduction identifier and typename-list is a type-name list.

The specified reduction identifier and type-name list identify the declare\_reduction directive. The reduction identifier can later be used in a reduction clause that uses variables of the types specified in the type-name list. If the directive specifies several types then the behavior is as if a declare\_reduction directive was specified for each type. The visibility and accessibility of a user-defined reduction are the same as those of a variable declared at the same location in the program.

The declare\_reduction directive can also appear at the locations in a program where a static data member could be declared. In this case, the visibility and accessibility of the declaration are the same as those of a static data member declared at the same location in the program.

The enclosing context of the combiner expression specified by the combiner clause and of the initializer expression specified by the initializer clause is that of the

declare\_reduction directive. The combiner expression and the initializer expression must be correct in the base language, as if they were the body of a procedure defined at the same location in the program.

## Fortran

If a type with a deferred or assumed length type parameter is specified in a

declare\_reduction directive, the reduction identifier of that directive can be used in a reduction clause with any variable of the same type and the same kind parameter, regardless of the length type parameters with which the variable is declared.

If the specified reduction identifier is the same as the name of a user-defined operator or an extended operator, or the same as a generic name that is one of the allowed intrinsic procedures, and if the operator or procedure name appears in an accessibility statement in the same module, the accessibility of the corresponding declare\_reduction directive is determined by the accessibility attribute of the statement.

If the specified reduction identifier is the same as a generic name that is one of the allowed intrinsic procedures and is accessible, and if it has the same name as a derived type in the same module, the accessibility of the corresponding declare\_reduction directive is determined by the accessibility of the generic name according to the base language.

Fortran

## Restrictions

Restrictions to the declare\_reduction directive are as follows:

• A reduction identifier must not be re-declared in the current scope for the same type or for a type that is compatible according to the base language rules.

• The type-name list must not declare new types.

C / C++

• A type name in a declare\_reduction directive must not be a function type, an array type, a reference type, or a type qualified with const, volatile or restrict.

C / C++

Fortran

• If the length type parameter is specified for a type, it must be a constant, a colon (:) or an asterisk (\*).

• If a type with a deferred or assumed length parameter is specified in a declare\_reduction directive, no other declare\_reduction directive with the same type, the same kind parameters and the same reduction identifier is allowed in the same scope.

Fortran

## Cross References

• combiner Clause, see Section 7.6.15

• OpenMP Combiner Expressions, see Section 7.6.2.1

• OpenMP Initializer Expressions, see Section 7.6.2.2

• OpenMP Reduction and Induction Identifiers, see Section 7.6.1

• initializer Clause, see Section 7.6.16
