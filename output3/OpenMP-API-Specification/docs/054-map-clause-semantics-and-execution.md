If corresponding storage that difers from the original storage is created in a device data environment, all new list items that are created in that corresponding storage are default initialized. Default initialization for new list items of class type, including their data members, is performed as if with an implicitly-declared default constructor and as if non-static data member initializers are ignored.

C++

Fortran

If a new list item is created then the new list item will have the same type, type parameter, and rank as the original list item. The new list item inherits all default values for the type parameters from the original list item.

Fortran

The close-modifier is a hint that the corresponding storage should be close to the target device.

If a map-entering clause specifies a self map for a list item then runtime error termination is performed if any of the following is true:

• The original list item is not accessible and cannot be made accessible from the target device;

• The corresponding list item is present prior to a task encountering the construct on which the clause appears, and the corresponding storage difers from the original storage; or

• The list item is a pointer that would be assigned a diferent value as a result of pointer attachment.

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
