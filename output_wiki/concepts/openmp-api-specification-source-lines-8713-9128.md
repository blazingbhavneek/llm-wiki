# OpenMP-API-Specification Source Lines 8713-9128

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source OpenMP-API-Specification:L8713-L9128

Citation: [OpenMP-API-Specification:L8713-L9128]

````text
## Restrictions

Restrictions to the threadprivate directive are as follows:

• A thread must not reference a copy of a threadprivate variable that belongs to another thread.

• A threadprivate variable must not appear as the base variable of a list item in any clause except for the copyin and copyprivate clauses.

• An OpenMP program in which an untied task accesses threadprivate memory is non-conforming.

• Each list item must be a file-scope, namespace-scope, or static block-scope variable.

• No list item may have an incomplete type.

• The address of a threadprivate variable must not be an address constant.

• If the value of a variable referenced in an explicit initializer of a threadprivate variable is modified prior to the first reference to any instance of the threadprivate variable, the behavior is unspecified.

• A threadprivate directive for file-scope variables must appear outside any definition or declaration, and must lexically precede all references to any of the variables in its argument list.

• A threadprivate directive for namespace-scope variables must appear outside any definition or declaration other than the namespace definition itself and must lexically precede all references to any of the variables in its argument list.

• Each variable in the argument list of a threadprivate directive at file, namespace, or class scope must refer to a variable declaration at file, namespace, or class scope that lexically precedes the directive.

• A threadprivate directive for a static block-scope variable must appear in the scope of the variable and not in a nested scope. The directive must lexically precede all references to any of the variables in its argument list.

• Each variable in the argument list of a threadprivate directive in block scope must refer to a variable declaration in the same scope that lexically precedes the directive. The variable must have static storage duration.

• If a variable is specified in a threadprivate directive in one compilation unit, it must be specified in a threadprivate directive in every compilation unit in which it is declared.

C / C++

C++

• A threadprivate directive for static class member variables must appear in the class definition, in the same scope in which the member variables are declared, and must lexically precede all references to any of the variables in its argument list.

• A threadprivate variable must not have an incomplete type or a reference type.

• A threadprivate variable with class type must have:

– An accessible, unambiguous default constructor in the case of default initialization without a given initializer;

– An accessible, unambiguous constructor that accepts the given argument in the case of direct initialization; and

– An accessible, unambiguous copy constructor in the case of copy initialization with an explicit initializer.

• Each list item must be a named variable or a named common block; a named common block must appear between slashes.

• The list argument must not include any coarrays or associate names.

• The threadprivate directive must appear in the declaration section of a scoping unit in which the common block or variable is declared.

• If a threadprivate directive that specifies a common block name appears in one compilation unit, then such a directive must also appear in every other compilation unit that contains a COMMON statement that specifies the same name. It must appear after the last such COMMON statement in the compilation unit.

• If a threadprivate variable or a threadprivate common block is declared with the BIND attribute, the corresponding C entities must also be specified in a threadprivate directive in the C program.

• A variable may only appear as an argument in a threadprivate directive in the scope in which it is declared. It must not be an element of a common block or appear in an EQUIVALENCE statement.

• A variable that appears as an argument in a threadprivate directive must be declared in the scope of a module or have the SAVE attribute, either explicitly or implicitly.

• The efect of an access to a threadprivate variable in a DO CONCURRENT construct is unspecified.

## Cross References

• copyin Clause, see Section 7.8.1

• dyn-var ICV, see Table 3.1

• order Clause, see Section 12.3

• Determining the Number of Threads for a parallel Region, see Section 12.1.1

## 7.4 List Item Privatization

Some data-sharing attribute clauses, including reduction clauses, specify that list items that appear in their argument list may be privatized for the construct on which they appear. Each task that references a privatized list item in any statement in the construct receives at least one new list item if the construct is a loop-collapsing construct, and otherwise each such task receives one new list item. Each SIMD lane used in a simd construct that references a privatized list item in any statement in the construct receives at least one new list item. Language-specific attributes for new list items are derived from the corresponding original list items. Inside the construct, all references to the original list items are replaced by references to the new list items received by the task or SIMD lane, and the new list items have the private attribute.

If the construct is a loop-collapsing construct then, within the same collapsed logical iteration of the collapsed loops, the same new list item replaces all references to the original list item. For any two collapsed iterations, if the references to the original list item are replaced by the same new list item then the collapsed iterations must execute in some sequential order.

In the rest of the region, whether references are to a new list item or the original list item is unspecified. Therefore, if an attempt is made to reference the original list item, its value after the region is also unspecified. If a task or a SIMD lane does not reference a privatized list item, whether the task or SIMD lane receives a new list item is unspecified.

The value and/or allocation status of the original list item will change only:

• If accessed and modified via a pointer;

• If possibly accessed in the region but outside of the construct;

• As a side efect of directives or clauses; or

Fortran

• If accessed and modified via construct association.

Fortran

C++

If the construct is contained in a member function, whether accesses anywhere in the region through the implicit this pointer refer to the new list item or the original list item is unspecified.

C++

C / C++

A new list item of the same type, with automatic storage duration, is allocated for the construct. The storage and thus lifetime of these new list items last until the block in which they are created exits. The size and alignment of the new list item are determined by the type of the variable. This allocation occurs once for each task generated by the construct and once for each SIMD lane used by the construct.

Unless otherwise specified, the new list item is initialized, or has an undefined initial value, as if it had been locally declared without an initializer.

C / C++

C++

If the type of a list item is a reference to a type T then the type will be considered to be T for all purposes of the clause.

The order in which any default constructors for diferent private variables of class type are called is unspecified. The order in which any destructors for diferent private variables of class type are called is unspecified.

## Fortran

If any statement of the construct references a list item, a new list item of the same type and type parameters is allocated. This allocation occurs once for each task generated by the construct and once for each SIMD lane used by the construct. If the type of the list item has default initialization, the new list item has default initialization. Otherwise, the initial value of the new list item is undefined. The initial status of a private pointer is undefined.

For a list item or the subobject of a list item with the ALLOCATABLE attribute:

• If the allocation status is unallocated, the new list item or the subobject of the new list item will have an initial allocation status of unallocated;

• If the allocation status is allocated, the new list item or the subobject of the new list item will have an initial allocation status of allocated; and

• If the new list item or the subobject of the new list item is an array, its bounds will be the same as those of the original list item or the subobject of the original list item.

A privatized list item may be storage-associated with other variables when the data-sharing attribute clause is encountered. Storage association may exist because of base language constructs such as EQUIVALENCE or COMMON. If A is a variable that is privatized by a construct and B is a variable that is storage-associated with A then:

• The contents, allocation, and association status of B are undefined on entry to the region;

• Any definition of A, or of its allocation or association status, causes the contents, allocation, and association status of B to become undefined; and

• Any definition of B, or of its allocation or association status, causes the contents, allocation, and association status of A to become undefined.

A privatized list item may be a selector of an ASSOCIATE, SELECT RANK or SELECT TYPE construct. If the construct association is established prior to a parallel region, the association between the associate name and the original list item will be retained in the region.

The dynamic type of a privatized list item of a polymorphic type is the declared type.

Finalization of a list item of a finalizable type or subobjects of a list item of a finalizable type occurs at the end of the region. The order in which any final subroutines for diferent variables of a finalizable type are called is unspecified.

## Fortran

If a list item appears in both firstprivate and lastprivate clauses, the update required for the lastprivate clause occurs after all initializations for the firstprivate clause.

## Restrictions

The following restrictions apply to any list item that is privatized unless otherwise specified for a given data-sharing attribute clause:

• If a list item is an array or array section, it must specify contiguous storage.

• A variable of class type (or array thereof) that is privatized requires an accessible, unambiguous default constructor for the class type.

• A variable that is privatized must not have the constexpr specifier unless it is of class type with a mutable member. This restriction does not apply to the firstprivate clause.

C / C++

• A variable that is privatized must not have a const-qualified type unless it is of class type with a mutable member. This restriction does not apply to the firstprivate clause.

• A variable that is privatized must not have an incomplete type or be a reference to an incomplete type.

C / C++

Fortran

• Variables that appear in namelist statements, in variable format expressions, and in expressions for statement function definitions, must not be privatized.

• Pointers with the INTENT(IN) attribute must not be privatized. This restriction does not apply to the firstprivate clause.

• A private variable must not be coindexed or appear as an actual argument to a procedure where the corresponding dummy argument is a coarray.

• Assumed-size arrays must not be privatized.

• An optional dummy argument that is not present must not appear as a list item in a privatization clause or be privatized as a result of an implicitly determined data-sharing attribute or predetermined data-sharing attribute.

Fortran

## 7.5 Data-Sharing Attribute Clauses

Several constructs accept clauses that allow a user to control the data-sharing attributes of variables referenced in the construct. Not all of the clauses listed in this section are valid on all directives. The set of clauses that is valid on a particular directive is described with the directive. The reduction clauses are explained in Section 7.6.

A list item may be specified in both firstprivate and lastprivate clauses.

C++

If a variable referenced in a data-sharing attribute clause has a type derived from a template and the OpenMP program does not otherwise reference that variable, any behavior related to that variable is unspecified.

C++

## Fortran

If individual members of a common block appear in a data-sharing attribute clause other than the shared clause, the variables no longer have a Fortran storage association with the common block. Fortran

## 7.5.1 default Clause

<table><tr><td>Name: default</td><td>Properties: unique, post-modified</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>data-sharing-attribute</td><td>Keyword:firstprivate,none, private, shared</td><td>default</td></tr></table>

## Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>variable-category</td><td>implicit-behavior</td><td>Keyword: aggregate, all, allocatable, pointer, scalar</td><td>default</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

parallel, target, target\_data, task, taskloop, teams

## Semantics

The default clause determines the implicitly determined data-sharing attributes of certain variables that are referenced in the construct, in accordance with the rules given in Section 7.1.1.

The variable-category specifies the variables for which the attribute may be set, and the attribute is specified by implicit-behavior. If no variable-category is specified in the clause then the efect is as if all was specified for the variable-category.

C / C++

The scalar variable-category specifies non-pointer scalar variables.

C / C++

Fortran

The scalar variable-category specifies non-pointer and non-allocatable scalar variables. The allocatable variable-category specifies variables with the ALLOCATABLE attribute.

Fortran

The pointer variable-category specifies variables of pointer type. The aggregate variable-category specifies aggregate variables. Finally, the all variable-category specifies all variables.

If data-sharing-attribute is not none, the data-sharing attributes of the selected variables will be data-sharing-attribute. If data-sharing-attribute is none, the data-sharing attribute is not implicitly determined. If data-sharing-attribute is shared then the clause has no efect on a target construct; otherwise, its efect on a target construct is equivalent to specifying the defaultmap clause with the same data-sharing-attribute and variable-category. If both the default and defaultmap clauses are specified on a target construct, and their variable-category modifiers specify intersecting categories, the defaultmap clause has precedence over the default clause for variables of those categories.

## Restrictions

Restrictions to the default clause are as follows:

• If data-sharing-attribute is none, each variable that is referenced in the construct and does not have a predetermined data-sharing attribute must have an explicitly determined data-sharing attribute.

## C / C++

• If data-sharing-attribute is firstprivate or private, each variable with static storage duration that is declared in a namespace or global scope, is referenced in the construct, and does not have a predetermined data-sharing attribute must have an explicitly determined data-sharing attribute.

## Cross References

• defaultmap Clause, see Section 7.9.9

• parallel Construct, see Section 12.1

• target Construct, see Section 15.8

• target\_data Construct, see Section 15.7

• task Construct, see Section 14.1

• taskloop Construct, see Section 14.2

• teams Construct, see Section 12.2

## 7.5.2 shared Clause

<table><tr><td>Name: shared</td><td>Properties: data-environment attribute, data-sharing attribute</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

## Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

parallel, target\_data, task, taskloop, teams

## Semantics

The shared clause declares one or more list items to have a shared attribute in tasks generated by the construct on which it appears. All references to a list item within a task refer to the storage area of the original list item at the point the directive was encountered.

The programmer must ensure, by adding proper synchronization, that storage shared by an explicit task region does not reach the end of its lifetime before the explicit task region completes its execution.

## Fortran

The list items may include assumed-type variables and procedure pointers.

The association status of a shared pointer becomes undefined upon entry to and exit from the construct if it is associated with a target or a subobject of a target that appears as a privatized list item in a data-sharing attribute clause on the construct. A reference to the shared storage that is associated with the dummy argument by any other task must be synchronized with the reference to the procedure to avoid possible data races.

## Fortran

## Cross References

• parallel Construct, see Section 12.1

• target\_data Construct, see Section 15.7

• task Construct, see Section 14.1

• taskloop Construct, see Section 14.2

• teams Construct, see Section 12.2

## 7.5.3 private Clause

<table><tr><td>Name: private</td><td>Properties: data-environment attribute, data-sharing attribute, innermost-leaf, privatization</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

## Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

distribute, do, for, loop, parallel, scope, sections, simd, single, target, target\_data, task, taskloop, teams

## Semantics

The private clause specifies that its list items are to be privatized list item according to Section 7.4. Each task or SIMD lane that references a list item in the construct receives only one new list item, unless the construct has one or more afected loops and an order clause that specifies concurrent is also present. Each new list item is a private-only variable, unless otherwise specified.

Fortran

The list items may include procedure pointers.

Fortran

## Restrictions

Restrictions to the private clause are as specified in Section 7.4.

## Cross References

• distribute Construct, see Section 13.7

• do Construct, see Section 13.6.2

• for Construct, see Section 13.6.1

• List Item Privatization, see Section 7.4

• loop Construct, see Section 13.8

• parallel Construct, see Section 12.1

• scope Construct, see Section 13.2

• sections Construct, see Section 13.3

• simd Construct, see Section 12.4

• single Construct, see Section 13.1

• target Construct, see Section 15.8

• target\_data Construct, see Section 15.7

• task Construct, see Section 14.1

• taskloop Construct, see Section 14.2

• teams Construct, see Section 12.2

## 7.5.4 firstprivate Clause

<table><tr><td>Name: firstprivate</td><td>Properties: data-environment attribute, data-sharing attribute, privatization</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>saved</td><td>list</td><td>Keyword: saved</td><td>default</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

distribute, do, for, parallel, scope, sections, single, target, target\_data, task, taskloop, teams

## Semantics

The firstprivate clause provides a superset of the functionality provided by the private clause. A list item that appears in a firstprivate clause is subject to the private clause semantics descrilbed in Section 7.5.3, except as noted. In addition, the new list item has the firstprivate attribute and is initialized from the original list item. The initialization of the new list item is done once for each task that references the list item in any statement in the construct. The initialization is done prior to the execution of the construct.

For a firstprivate clause on a construct that is not a work-distribution construct, the initial value of the new list item is the value of the original list item that exists immediately prior to the construct in the task region where the construct is encountered unless otherwise specified. For a firstprivate clause on a work-distribution construct, the initial value of the new list item for each implicit task of the threads that execute the construct is the value of the original list item that exists in the implicit task immediately prior to the point in time that the construct is encountered unless otherwise specified.

To avoid data races, concurrent updates of the original list item must be synchronized with the read of the original list item that occurs as a result of the firstprivate clause.

$$
\mathrm{C} / \mathrm{C} + +
$$

For variables of non-array type, the initialization occurs by copy assignment. For an array of elements of non-array type, each element is initialized as if by assignment from an element of the original array to the corresponding element of the new array.

$$
\mathrm{C/C++}
$$

For each variable of class type:

• If the firstprivate clause is not on a target construct then a copy constructor is invoked to perform the initialization; and

• If the firstprivate clause is on a target construct then how many copy constructors, if any, are invoked is unspecified.

If copy constructors are called, the order in which copy constructors for diferent variables of class type are called is unspecified.

C++

Fortran

If the firstprivate clause is on a target construct and a variable is of polymorphic type, the behavior is unspecified.

If an original list item does not have the POINTER attribute, initialization of the new list items occurs as if by intrinsic assignment unless the original list item has a compatible type-bound defined assignment, in which case initialization of the new list items occurs as if by the defined assignment. If an original list item that does not have the POINTER attribute has an allocation status of unallocated, the new list items will have the same status.

If an original list item has the POINTER attribute, the new list items receive the same association status as the original list item, as if by pointer assignment.

The list items may include named constants and procedure pointers.

Fortran
````
