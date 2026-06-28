## Execution Model Events

The target-map event occurs in a thread that executes the outermost region that corresponds to an encountered device construct with a map clause, after the target-task-begin event for the device construct and before any mapping operations are performed. The target-data-op-begin event occurs before a thread initiates a data operation on the target device that is associated with a map clause, in the outermost region that corresponds to the encountered construct. The target-data-op-end event occurs after a thread initiates a data operation on the target device that is associated with a map clause, in the outermost region that corresponds to the encountered construct.

## Tool Callbacks

A thread dispatches one or more registered target\_map\_emi callbacks for each occurrence of a target-map event in that thread. The callback occurs in the context of the target task. A thread dispatches a registered target\_data\_op\_emi callback with ompt\_scope\_begin as its endpoint argument for each occurrence of a target-data-op-begin event in that thread. Similarly, a thread dispatches a registered target\_data\_op\_emi callback with ompt\_scope\_end as its endpoint argument for each occurrence of a target-data-op-end event in that thread.

## Restrictions

Restrictions to the map clause are as follows:

• Two list items of the map clauses on the same construct must not share original storage unless one of the following is true: they are the same list item, one is the containing structure of the other, at least one is an assumed-size array, or at least one is implicitly mapped due to the list item also appearing in a use\_device\_addr clause.

• If the same list item appears more than once in map clauses on the same construct, the map clauses must specify the same mapper modifier.

• A variable that is a groupprivate variable or a device-local variable must not appear as a list item in a map clause.

• If a list item is an array or an array section, it must specify contiguous storage.

• If an expression that is used to form a list item in a map clause contains an iterator identifier that is defined by an iterator modifier, the list item instances that would result from diferent values of the iterator must not have the same containing array and must not have base pointers that share original storage.

• If multiple list items are explicitly mapped on the same construct and have the same containing array or have base pointers that share original storage, and if any of the list items do not have corresponding list items that are present in the device data environment prior to a task encountering the construct, then the list items must refer to the same array elements of either the containing array or the implicit array of the base pointers.

• If any part of the original storage of a list item that is explicitly mapped by a map clause has corresponding storage in the device data environment prior to a task encountering the construct associated with the map clause, all of the original storage must have corresponding storage in the device data environment prior to the task encountering the construct.

• If a list item in a map clause has corresponding storage in the device data environment, all corresponding storage must correspond to a single mappable storage block that was previously mapped.

• If a list item is an element of a structure, and a diferent element of the structure has a corresponding list item in the device data environment prior to a task encountering the construct associated with the map clause, then the list item must also have a corresponding list item in the device data environment prior to the task encountering the construct.

• Each list item must have a mappable type.

• If a mapper modifier appears in a map clause, the type on which the specified mapper operates must match the type of the list items in the clause.

• Handles for memory spaces and memory allocators must not appear as list items in a map clause.

• If a list item is an assumed-size array, multiple matched candidates must not exist unless they are subobjects of the same containing structure.

• If a list item is an assumed-size array, the map-type must be storage.

• If a list item appears in a map clause with the self-modifier, any other list item in a map clause on the same construct that has the same base variable or base pointer must also be specified with the self-modifier.

## C++

• If a list item has a polymorphic class type and its static type does not match its dynamic type, the behavior is unspecified if the map clause is specified on a map-entering construct and a corresponding list item is not present in the device data environment prior to a task encountering the construct.

• No type mapped through a reference may contain a reference to its own type, or any references to types that could produce a cycle of references.

• If a given variable is captured by reference by the associated lambda expression of a list item that has a closure type and that variable is a reference that binds to a variable with static storage duration, the variable to which it binds must appear in an enter clause or a link clause on a declare target directive and must have corresponding storage in the device data environment prior to a task encountering the construct.

• A list item cannot be a variable that is a member of a structure of a union type.

• A bit-field cannot appear in a map clause.

• A pointer that has a corresponding pointer that is an attached pointer must not be modified for the duration of the lifetime of the list item to which the corresponding pointer is attached in the device data environment.

## Fortran

• The association status of a list item that is a pointer must not be undefined unless it is a structure component and it results from a predefined default mapper.

• If a list item of a map clause is an allocatable variable or is the subobject of an allocatable variable, the original list item must not be allocated, deallocated or reshaped while the corresponding list item has allocated storage.

• A pointer that has a corresponding pointer that is an attached pointer and is associated with a given pointer target must not become associated with a diferent pointer target for the duration of the lifetime of the list item to which the corresponding pointer is attached in the device data environment.

• If a list item has polymorphic type, the behavior is unspecified.

• If an array section is mapped and the size of the array section is smaller than that of the whole array, the behavior of referencing the whole array in a target region is unspecified.

• A list item must not be a complex part designator.

• If a list item is an assumed-type variable, the map-type must be storage.

## Cross References

• declare\_mapper Directive, see Section 7.9.10

• Array Sections, see Section 5.2.5

• iterator Modifier, see Section 5.2.6

• Mapper Identifiers and mapper Modifiers, see Section 7.9.4

• map-type Modifier, see Section 7.9.1

• OMPT scope\_endpoint Type, see Section 33.27

• target Construct, see Section 15.8

• target\_data Construct, see Section 15.7

• target\_data\_op\_emi Callback, see Section 35.7

• target\_enter\_data Construct, see Section 15.5

• target\_exit\_data Construct, see Section 15.6

• target\_map\_emi Callback, see Section 35.9

• target\_update Construct, see Section 15.9

7.9.7 enter Clause

<table><tr><td>Name: enter</td><td>Properties: data-environment attribute, data-mapping attribute</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of extended list item type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>automap-modifier</td><td>list</td><td>Keyword: automap</td><td>default</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

declare\_target

## Semantics

The enter clause is a data-mapping attribute clause.

If a procedure name appears in an enter clause in the same compilation unit in which the definition of the procedure occurs then a device-specific version of the procedure is created for all devices to which the directive of the clause applies.

C / C++

If a variable appears in an enter clause in the same compilation unit in which the definition of the variable occurs then a corresponding list item to the original list item is created in the device data environment of all devices to which the directive of the clause applies.

C / C++

Fortran

If a variable that is host associated appears in an enter clause then a corresponding list item to the original list item is created in the device data environment of all devices to which the directive of the clause applies.

Fortran

If a variable appears in an enter clause then the corresponding list item in the device data environment of each device to which the directive of the clause applies is initialized once, in the manner specified by the OpenMP program, but at an unspecified point in the OpenMP program prior to the first reference to that list item. The list item is never removed from those device data environments, as if its reference count was initialized to positive infinity, unless otherwise specified.

If a list item is a referencing variable, the efect of the enter clause applies to its referring pointer.

## Fortran

If a list item is an allocatable variable, the automap-modifier is present, and the variable is allocated by an ALLOCATE statement or deallocated by a DEALLOCATE statement where the enter clause is visible, the behavior is as follows:

• Upon allocation due to the ALLOCATE statement, the list item is mapped to the device data environment of the default device as if it appeared as a list item in a map clause on a target\_enter\_data directive; and

• Immediately prior to the deallocation due to the DEALLOCATE statement, the list item is removed from the device data environment of the default device as if it appeared as a list item in a map clause with the delete-modifier on a target\_exit\_data directive.

Fortran

## Restrictions

Restrictions to the enter clause are as follows:

• Each list item must have a mappable type.

• Each list item must have static storage duration.

C / C++

• The automap-modifier must not be present.

C / C++

Fortran

• If the automap-modifier is present, each list item must be an allocatable variable.

Fortran

## Cross References

• declare\_target Directive, see Section 9.9.1

## 7.9.8 link Clause

<table><tr><td>Name: link</td><td>Properties: data-environment attribute</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

## Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

## declare\_target

## Semantics

The link clause supports compilation of device procedures that refer to variables with static storage duration that appear as list items in the clause. The declare\_target directive on which the clause appears does not map the list items. Instead, they are mapped according to the data-mapping rules described in Section 7.9.3.

## Restrictions

Restrictions to the link clause are as follows:

• Each list item must have a mappable type.

• Each list item must have static storage duration.

## Cross References

• declare\_target Directive, see Section 9.9.1

• Data-Mapping Control, see Section 7.9

## 7.9.9 defaultmap Clause

<table><tr><td>Name: defaultmap</td><td>Properties: unique, post-modified</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>implicit-behavior</td><td>Keyword:default,firstprivate,from, none,present, private,self, storage, to,tofrom</td><td>default</td></tr></table>

## Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>variable-category</td><td>implicit-behavior</td><td>Keyword: aggregate, all, allocatable, pointer, scalar</td><td>default</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

target

## Additional information

The value alloc may also be specified as implicit-behavior with identical meaning to the value storage.

## Semantics

The defaultmap clause controls the implicitly determined data-mapping attributes or implicitly determined data-sharing attributes of certain variables that are referenced in a target construct, in accordance with the rules given in Section 7.9.3. The variable-category specifies the variables for which the attribute may be set, and the attribute is specified by implicit-behavior. If no variable-category is specified in the clause then the efect is as if all was specified for the variable-category.

C / C++

The scalar variable-category specifies non-pointer scalar variables.

C / C++

Fortran

The scalar variable-category specifies non-pointer and non-allocatable scalar variables. The allocatable variable-category specifies variables with the ALLOCATABLE attribute.

Fortran

The pointer variable-category specifies variables of pointer type. The aggregate variable-category specifies aggregate variables. Finally, the all variable-category specifies all variables.

If implicit-behavior corresponds to a map-type, the attribute is a data-mapping attribute determined by an implicit map clause with the specified map-type. If implicit-behavior is firstprivate, the attribute is a data-sharing attribute of firstprivate. If implicit-behavior is present, the attribute is a data-mapping attribute determined by an implicit map clause with a map-type of storage and the present-modifier. If implicit-behavior is self, the attribute is a data-mapping attribute determined by an implicit map clause with a map-type of storage and the self-modifier. If implicit-behavior is none then no implicitly determined data-mapping attributes or implicitly determined data-sharing attributes are defined for variables in variable-category, except for variables that appear in the enter or link clause of a declare\_target directive. If implicit-behavior is default then the clause has no efect.

Restrictions

Restrictions to the defaultmap clause are as follows:

• A given variable-category may be specified in at most one defaultmap clause on a construct.

• If a defaultmap clause specifies the all variable-category, no other defaultmap clause may appear on the construct.

• If implicit-behavior is none, each variable that is specified by variable-category and is referenced in the construct but does not have a predetermined data-sharing attribute and does not appear in an enter or link clause on a declare\_target directive must be explicitly listed in a data-environment attribute clause on the construct.

C / C++

• The specified variable-category must not be allocatable.

C / C++

## Cross References

• Implicit Data-Mapping Attribute Rules, see Section 7.9.3

• target Construct, see Section 15.8

## 7.9.10 declare\_mapper Directive

<table><tr><td>Name:declare_mapperCategory:declarative</td><td>Association:unassociatedProperties:pure</td></tr></table>

## Arguments

declare\_mapper(mapper-specifier)

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>mapper-specifier</td><td>OpenMP mapper specifier</td><td>default</td></tr></table>

## Clauses

map

## Additional information

The declare\_mapper directive may alternatively be specified with declare mapper as the directive-name.

## Semantics

User-defined mappers can be defined using the declare\_mapper directive. The mapper-specifier argument declares the mapper using the following syntax:

C / C++

[ mapper-identifier : ] type var

C / C++

Fortran

[ mapper-identifier : ] type :: var

Fortran

where mapper-identifier is a mapper identifier, type is a type that is permitted in a type-name list, and var is a base language identifier.

The type and an optional mapper-identifier uniquely identify the mapper for use in a map clause or data-motion clause later in the OpenMP program.

If mapper-identifier is not specified, the behavior is as if mapper-identifier is default.

The variable declared by var is available for use in all map clauses on the directive, and no part of the variable to be mapped is mapped by default.

The efect that a user-defined mapper has on either a map clause that maps a list item of the given base language type or a data-motion clause that invokes the mapper and updates a list item of the given base language type is to replace the map or update with a set of map clauses or updates derived from the map clauses specified by the mapper, as described in Section 7.9.6 and Section 7.10.

A list item in a map clause that appears on a declare\_mapper directive may include array sections.

All map clauses that are introduced by a mapper are further subject to mappers that are in scope, except a map clause with list item var maps var without invoking a mapper.

![](images/48e52199ce77c3b15b28ac6c949c2e959341bec1739ac977fdba8ca28fc743b4.jpg)

The declare\_mapper directive can also appear at locations in the OpenMP program at which a static data member could be declared. In this case, the visibility and accessibility of the declaration are the same as those of a static data member declared at the same location in the OpenMP program.

![](images/8b1b4b1928c77b14be8c5942dd8e398671e532fe05c80aff70a10d2c51fe5e88.jpg)

## Restrictions

Restrictions to the declare\_mapper directive are as follows:

• No instance of type can be mapped as part of the mapper, either directly or indirectly through another base language type, except the instance var that is passed as the list item. If a set of declare\_mapper directives results in a cyclic definition then the behavior is unspecified.

• The type must not declare a new base language type.

• At least one map clause that maps var or at least one element of var is required.

• List items in map clauses on the declare\_mapper directive may only refer to the declared variable var and entities that could be referenced by a procedure defined at the same location.

• If a mapper modifier is specified for a map clause, its parameter must be default.

• Multiple declare\_mapper directives that specify the same mapper-identifier for the same base language type or for compatible base language types, according to the base language rules, must not appear in the same scope.

• type must be a struct or union type.

C++

• type must be a struct, union, or class type.

• If type is a struct or class type, it must not be derived from any virtual base class.

C++

Fortran

• type must not be an intrinsic type, a parameterized derived type, an enum type, or an enumeration type.

Fortran

## Cross References

• map Clause, see Section 7.9.6
