
• If it has the ALLOCATABLE attribute and an allocated allocation status, and it is present in the device data environment when the construct is encountered, the map clause may treat its allocation status as if it is unallocated if the corresponding component does not have allocated storage.

If a list item in a map clause is an associated pointer that is attach-ineligible or the pointer is the base pointer of another list item in a map clause on the same construct then the efect of the map clause does not apply to its pointer target.

If a list item is a procedure pointer, it is attach-ineligible.

Fortran

C++

If a list item has a closure type that is associated with a lambda expression, it is mapped as if it has a structure type. For each variable that is captured by reference by the lambda expression, the behavior is as if the closure type contains a non-static data member that is a reference to that variable unless otherwise specified. If a variable that is captured by reference is a reference that binds to an object with static storage duration, a corresponding non-static data member might not exist in the closure type. For the corresponding list item of closure type, references in the body of the lambda expression to a variable that is captured by reference refer to the corresponding storage of the variable in the device data environment. For each pointer, that is not a function pointer, that is captured by the lambda expression, the behavior is as if the pointer or, if a corresponding pointer member exists, the corresponding pointer member of the closure object is the base pointer of a zero-ofset assumed-size array that appears as a list item in a map clause with the storage map-type.

If the this pointer is captured by a lambda expression in class scope, and a variable of the associated closure type is later mapped explicitly or implicitly with its full static type, the behavior is as if the object to which this points is also mapped as an array section, of length one, for which the base pointer is the non-static data member that corresponds to the this pointer in the closure object.

If a map clause with a present-modifier appears on a construct and on entry to the region the corresponding list item is not present in the device data environment, runtime error termination is performed.

If a map-entering clause has the self-modifier, the resulting mapping operations are self maps.

The efective map clause set of a data-mapping construct is the set of all map clauses that apply to that construct, including implicit map clauses and map clauses applied by mappers. The efective map clause set of a construct determines the set of mappable storage blocks for that construct. All map clause list items that share storage or have the same containing structure or containing array result in a single mappable storage block that contains the storage of the list items, unless otherwise specified. The storage for each other map clause list item becomes a distinct mappable storage block. If a list item is a referencing variable that has a containing structure, the behavior is as if only the storage for its referring pointer is part of that structure. In general, if a list item is a referencing variable then the storage for its referring pointer and its referenced pointee occupy distinct mappable storage blocks.

For each mappable storage block that is determined by the efective map clause set of a map-entering construct, on entry to the region the following sequence of steps occurs as if performed as a single atomic operation:

1. If a corresponding storage block is not present in the device data environment then:

a) A corresponding storage block, which may share storage with the original storage block, is created in the device data environment of the target device;

b) The corresponding storage block receives a reference count that is initialized to zero. This reference count also applies to any part of the corresponding storage block.

2. The reference count of the corresponding storage block is incremented by one.

3. For each map clause list item in the efective map clause set that is contained by the mappable storage block:

a) If the reference count of the corresponding storage block is one, a new list item with language-specific attributes derived from the original list item is created in the corresponding storage block. The reference count of the new list item is always equal to the reference count of its storage.

b) If the reference count of the corresponding list item is one or if the always-modifier is specified, and if the map type is to, the corresponding list item is updated as if the list item appeared in a to clause on a target\_update directive.

If the efect of the map clauses on a construct would assign the value of an original list item to a corresponding list item more than once then an implementation is allowed to ignore additional assignments of the same value to the corresponding list item.

In all cases on entry to the region, concurrent reads or updates of any part of the corresponding list item must be synchronized with any update of the corresponding list item that occurs as a result of the map clause to avoid data races.

For map clauses on map-entering constructs, if any list item has a base pointer or referring pointer for which a corresponding pointer exists in the device data environment after all mappable storage blocks are mapped, and either a new list item or the corresponding pointer is created in the device data environment on entry to the region, then pointer attachment is performed and the corresponding pointer becomes an attached pointer to the corresponding list item via corresponding pointer initialization.

The original list item and corresponding list item may share storage such that writes to either item by one task followed by a read or write of the other list item by another task without intervening synchronization can result in data races. They are guaranteed to share storage if the mapping operation is a self map, if the map clause appears on a data-mapping construct for which the target device is the encountering device, or if the corresponding list item has an attached pointer that shares storage with its original pointer.

For each mappable storage block that is determined by the efective map clause set of a map-exiting construct, and for which corresponding storage is present in the device data environment, on exit from the region the following sequence of steps occurs as if performed as a single atomic operation:

1. For each map clause list item in the efective map clause set that is contained by the mappable storage block:

a) If the reference count of the corresponding list item is one or if the always-modifier or delete-modifier is specified, and if the map type is from, the original list item is updated as if the list item appeared in a from clause on a target\_update directive.

2. If the delete-modifier is not present and the reference count of the corresponding storage block is finite then the reference count is decremented by one.

3. If the delete-modifier is present and the reference count of the corresponding storage block is finite then the reference count is set to zero.

4. If the reference count of the corresponding storage block is zero, all storage to which that reference count applies is removed from the device data environment.

If the efect of the map clauses on a construct would assign the value of a corresponding list item to an original list item more than once, then an implementation is allowed to ignore additional assignments of the same value to the original list item.

In all cases on exit from the region, concurrent reads or updates of any part of the original list item must be synchronized with any update of the original list item that occurs as a result of the map clause to avoid data races.

If a single contiguous part of the original storage of a list item that results from an implicitly determined data-mapping attribute has corresponding storage in the device data environment prior to a task encountering the construct on which the map clause appears, only that part of the original storage will have corresponding storage in the device data environment as a result of the map clause.

If a list item with an implicitly determined data-mapping attribute does not have any corresponding storage in the device data environment prior to a task encountering the construct associated with the map clause, and one or more contiguous parts of the original storage are either list items or base pointers to list items that are explicitly mapped on the construct, only those parts of the original storage will have corresponding storage in the device data environment as a result of the map clauses on the construct.

C / C++

If a new list item is created then the new list item will have the same static type as the original list item, and language-specific attributes of the new list item, including size and alignment, are determined by that type.

C / C++

C++
