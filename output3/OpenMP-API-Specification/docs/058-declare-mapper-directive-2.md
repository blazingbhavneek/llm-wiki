
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

## 7.10 Data-Motion Clauses

A data-motion clause specifies data movement between devices in a device set that is specified by the construct on which the clause appears, where one of the devices in the set is the encountering device and the remaining devices are target devices of the construct. Each data-motion clause specifies a data-motion attribute relative to the target devices.

A data-motion clause specifies an OpenMP locator list as its argument. A corresponding list item and an original list item exist for each list item. If the corresponding list item is not present in the device data environment then no assignment occurs between the corresponding list item and the original list item. Otherwise, each corresponding list item in the device data environment has an original list item in the data environment of the encountering task. Assignment is performed to either the original list item or the corresponding list item as specified with the specific data-motion clauses. List items may reference any iterator-identifier defined in an iterator modifier on the clause. The list items may include array sections with stride expressions.

C / C++

The list items may use shape-operators.

C / C++

If a list item is an array or array section then it is treated as if it is replaced by each of its array elements in the clause.

If the mapper modifier is not specified, the behavior is as if the modifier was specified with the default mapper identifier. The efect of a data-motion clause on a list item is modified by a visible user-defined mapper if a mapper modifier is specified with a mapper identifier for a type that matches the type of the list item. Otherwise, the predefined default mapper for the type of the list item applies. Each list item is replaced with the list items that the given mapper specifies are to be mapped with a compatible map type with respect to the data-motion attribute of the clause.

If a present-modifier is specified and the corresponding list item is not present in the device data environment then runtime error termination is performed. For a list item that is replaced with a set of list items as a result of a user-defined mapper, the present-modifier only applies to those mapper list items that share storage with the original list item.

If a list item is a referencing variable then the efect of the data-motion clause is applied only to its referenced pointee and only if the referenced pointee exists.

Fortran

If a list item is an associated procedure pointer, the corresponding list item on the device is associated with the target procedure of the host device.

Fortran

C / C++

On exit from the associated region, if the corresponding list item is an attached pointer, the original list item will have the value it had on entry to the region and the corresponding list item will have the value it had on entry to the region.

C / C++

For each list item that is not an attached pointer, the value of the assigned list item is assigned the value of the other list item. To avoid data races, concurrent reads or updates of the assigned list item must be synchronized with the update of an assigned list item that occurs as a result of a data-motion clause.

## Restrictions

Restrictions to data-motion clauses are as follows:

• Each list item of locator-list must have a mappable type.

• If an array appears as a list item in a data-motion clause and it has corresponding storage in the device data environment, the corresponding storage must correspond to a single mappable storage block that was previously mapped.

• If a list item in a data-motion clause has corresponding storage in the device data environment, all corresponding storage must correspond to a single mappable storage block that was previously mapped.

• If a mapper modifier appears in a data-motion clause, the specified mapper must operate on a type that matches either the type or array element type of each list item in the clause.

## Fortran

• The association status of a list item that is a pointer must not be undefined unless it is a structure component and it results from a predefined default mapper.
