## 7.9 Data-Mapping Control

This section describes the available mechanisms for controlling how data are mapped to device data environments. It covers implicitly determined data-mapping attribute rules for variables referenced in target constructs, clauses that support explicitly determined data-mapping attributes, and clauses for mapping variables with static storage duration and making procedures available on other devices. It also describes how mappers may be defined and referenced to control the mapping of data with user-defined types. When storage is mapped, the programmer must ensure, by adding proper synchronization or by explicit unmapping, that the storage does not reach the end of its lifetime before it is unmapped.

## 7.9.1 map-type Modifier

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>map-type</td><td>all arguments</td><td>Keyword: from, storage, to, tofrom</td><td>default</td></tr></table>

## Clauses

map

## Additional information

The value alloc may be used on map-entering constructs and the value release may be used on map-exiting constructs with identical meaning to the value storage.

## Semantics

The map-type modifier determines the type of mapping operations that are performed as a result of the clause on which it appears. All mapping operations update the reference count of corresponding storage in a device data environment, which may entail creation or removal of that storage. The storage map-type never includes an assignment operation. If the map-type is to, from, or tofrom, the map-type is an assigning map type and may include an assignment operation to or from the target device.

The map-type is a map-entering map type if it is to, tofrom, or storage. The map-type is a map-exiting map type if it is from, tofrom, or storage. If the map-type is a map-entering map type, the clause on which the map-type appears is a map-entering clause. If the map-type is a map-exiting map type, the clause on which the map-type appears is a map-exiting clause.

When a map-type is not specified for a clause on which it may be specified, the map-type defaults to storage if the delete-modifier is present on the clause or if the list item for which the map-type is not specified is an assumed-size array. Otherwise, the map-type defaults to tofrom if a map-type is not specified for a clause on which it may be specified, unless otherwise specified.

Fortran

When a map-type is not specified for a clause on which it may be specified, the map-type defaults to storage if the list item for which the map-type is not specified is an assumed-type variable.

Fortran

## Restrictions

Restrictions to the map-type modifier are as follows:

• If the clause on which the map-type appears is specified on a construct that is map-entering but not map-exiting, the map-type must be map-entering.

• If the clause on which the map-type appears is specified on a construct that is map-exiting but not map-entering, the map-type must be map-exiting.

## Cross References

• map Clause, see Section 7.9.6

## 7.9.2 Map Type Decay

Map-type decay is a process that derives an output map type from a given input map type according to an underlying map type. This process is defined by Table 7.5, where the output map type is shown at the row and column that corresponds to the underlying map type and input map type, respectively. When map-type decay determines the map-type modifier to apply for a map clause on a data-mapping constituent directive of a composite construct, the input map type is given by the map-type modifier specified by the map clause on the composite construct and the underlying map type is respectively to or from for a map-entering constituent directive or a map-exiting constituent directive. When map-type decay is applied by an invoked mapper, the underlying map type is given by the map-type modifier of the map clause specified by the mapper and the input map type is given by the map-type modifier of the map clause that invokes the mapper.

TABLE 7.5: Map-Type Decay of Map Type Combinations

<table><tr><td></td><td>storage</td><td>to</td><td>from</td><td>tofrom</td></tr><tr><td>storage to from tofrom</td><td>storage storage storage storage</td><td>storage to storage to</td><td>storage storage from from</td><td>storage to from tofrom</td></tr></table>

## 7.9.3 Implicit Data-Mapping Attribute Rules

When specified, data-mapping attribute clauses on target directives determine the data-mapping attributes for variables referenced in a target construct. Otherwise, the first matching rule from the following list determines the implicitly determined data-mapping attribute (or implicitly determined data-sharing attribute) for variables referenced in a target construct that do not have a predetermined data-sharing attribute according to Section 7.1.1. References to structure elements or array elements are treated as references to the structure or array, respectively, for the purposes of implicitly determined data-mapping attributes or implicitly determined data-sharing attributes of variables referenced in a target construct.

• If a variable appears in an enter or link clause on a declare target directive that does not have a device\_type clause with the nohost device-type-description then it is treated as if it had appeared in a map clause with a map-type of tofrom.

• If a variable is the base variable of a list item in a reduction, lastprivate or linear clause on a compound target construct then the list item is treated as if it had appeared in a map clause with a map-type of tofrom if Section 19.2 specifies this behavior.

• If a variable is the base variable of a list item in an in\_reduction clause on a target construct then it is treated as if the list item had appeared in a map clause with a map-type of tofrom and an always-modifier.

• If a defaultmap clause is present for the category of the variable and specifies an implicit behavior other than default, the data-mapping attribute or data-sharing attribute is determined by that clause.

• If the target construct is within a class non-static member function, and a variable is an accessible data member of the object for which the non-static member function is invoked, the variable is treated as if the this[:1] expression had appeared in a map clause with a map-type of tofrom. Additionally, if the variable is of type pointer or reference to pointer, it is also treated as if it is the array base of a zero-ofset assumed-size array that appears in a map clause with the storage map-type.

• If the this keyword is referenced inside a target construct within a class non-static member function, it is treated as if the this[:1] expression had appeared in a map clause with a map-type of tofrom.

C++

C / C++

• A variable that is of type pointer, but is neither a pointer to function nor (for C++) a pointer to a member function, is treated as if it is the array base of a zero-ofset assumed-size array that appears in a map clause with the storage map-type.

C / C++

C++

• A variable that is of type reference to pointer, but is neither a reference to pointer to function nor a reference to a pointer to a member function, is treated as if it is the array base of a zero-ofset assumed-size array that appears in a map clause with the storage map-type.

C++

Fortran

• If a compound target construct is associated with a DO CONCURRENT loop, a variable that has REDUCE or SHARED locality in the loop is treated as if it had appeared in a map clause with a map-type of tofrom.

Fortran

• If a variable is not a scalar variable then it is treated as if it had appeared in a map clause with a map-type of tofrom.

## Fortran

• If a scalar variable has the TARGET, ALLOCATABLE or POINTER attribute then it is treated as if it had appeared in a map clause with a map-type of tofrom.

• If a variable is an assumed-type variable then it is treated as if it had appeared in a map clause with a map-type of storage.

• A procedure pointer is treated as if it had appeared in a firstprivate clause.

Fortran

• If the above rules do not apply then a scalar variable is not mapped but instead has an implicitly determined data-sharing attribute of firstprivate (see Section 7.1.1).

## 7.9.4 Mapper Identifiers and mapper Modifiers

## Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>mapper</td><td>locator-list</td><td>Complex, name: mapperArguments:mapper-identifier OpenMPidentifier (default)</td><td>unique</td></tr></table>

## Clauses

from, map, to

## Semantics

Mapper identifiers can be used to identify uniquely the mapper used in a map or data-motion clause through a mapper modifier, which is a unique, complex modifier. A declare\_mapper directive defines a mapper identifier that can later be specified in a mapper modifier as its modifier-parameter-specification. Each mapper identifier is a base language identifier or default where default is the default mapper for all types.

A non-structure type T has a predefined default mapper that is defined as if by the following declare\_mapper directive:

C / C++

#pragma omp declare\_mapper(T v) map(tofrom: v)

C / C++

Fortran

!\$omp declare\_mapper(T :: v) map(tofrom: v)

## Fortran

A structure type T has a predefined default mapper that is defined as if by a declare\_mapper directive that specifies v in a map clause with the storage map-type and each structure element of v in a map clause with the tofrom map-type.

A declare\_mapper directive that uses the default mapper identifier overrides the predefined default mapper for the given type, making it the default mapper for variables of that type.

## Cross References

• declare\_mapper Directive, see Section 7.9.10

• from Clause, see Section 7.10.2

• Data-Motion Clauses, see Section 7.10

• map Clause, see Section 7.9.6

• to Clause, see Section 7.10.1

## 7.9.5 ref-modifier Modifier

## Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>ref-modifier</td><td>all arguments</td><td>Keyword: ref_ptee, ref_ptr, ref_ptr_ptee</td><td>unique</td></tr></table>

## Clauses

map

## Semantics

The ref-modifier for a given clause indicates how to interpret the identity of a list item argument of that clause. If the ref\_ptr or ref\_ptr\_ptee ref-modifier is specified, the semantics of the clause apply to the referring pointer of the referencing variable. If the ref\_ptee or ref\_ptr\_ptee ref-modifier is specified and a referenced pointee of the referencing variable exists, the semantics of the clause apply to the referenced pointee.

## Restrictions

Restrictions to the ref-modifier are as follows:

• A list item that appears in a clause with the ref-modifier must be a referencing variable.

C / C++

• A list item that appears in a clause for which the ref-modifier is specified must have a containing structure.

C / C++

## Cross References

• map Clause, see Section 7.9.6

## 7.9.6 map Clause

<table><tr><td>Name: map</td><td>Properties: data-environment attribute, data-mapping attribute</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>locator-list</td><td>list of locator list item type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>always-modifier</td><td>locator-list</td><td>Keyword: always</td><td>map-type-modifying</td></tr><tr><td>close-modifier</td><td>locator-list</td><td>Keyword: close</td><td>map-type-modifying</td></tr><tr><td>present-modifier</td><td>locator-list</td><td>Keyword: present</td><td>map-type-modifying</td></tr><tr><td>self-modifier</td><td>locator-list</td><td>Keyword: self</td><td>map-type-modifying</td></tr><tr><td>ref-modifier</td><td>all arguments</td><td>Keyword: ref_ptee, ref_ptr, ref_ptr_ptee</td><td>unique</td></tr><tr><td>delete-modifier</td><td>locator-list</td><td>Keyword: delete</td><td>map-type-modifying</td></tr><tr><td>mapper</td><td>locator-list</td><td>Complex, name: mapperArguments:mapper-identifier OpenMPidentifier (default)</td><td>unique</td></tr><tr><td>iterator</td><td>locator-list</td><td>Complex, name: iteratorArguments:iterator-specifier list of iterator specifier list item type (default)</td><td>unique</td></tr><tr><td>map-type</td><td>all arguments</td><td>Keyword: from, storage, to, tofrom</td><td>default</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

declare\_mapper, target, target\_data, target\_enter\_data, target\_exit\_data

## Semantics

The map clause specifies how an original list item is mapped from the data environment of the current task to a corresponding list item in the device data environment of the device identified by the construct. The list items that appear on a map clause may include array sections, assumed-size arrays, and structure elements. A list item in a map clause may reference any iterator-identifier defined in its iterator modifier. A list item may appear more than once in the map clauses that are specified on the same directive.

## C / C++

If a list item is a zero-length array section that has a single array subscript, the behavior is as if the list item is an assumed-size array that is instead mapped with the storage map-type.

When a list item in a map clause that is not an assumed-size array is mapped on a map-entering construct and corresponding storage is created in the device data environment on entry to the region, the list item becomes a matchable candidate with an associated starting address, ending address, and base address that define its mapped address range and extended address range. The current set of matchable candidates consists of any map clause list item on the construct that is a matchable candidate and all matchable candidates that were previously mapped and are still mapped.

A list item in a map clause that is an assumed-size array is treated as if an array section, with an array base, lower bound and length determined as follows, is substituted in its place if a matched candidate is found. If the assumed-size array is an array section, the array base of the substitute array section is the same as for the assumed-size array; otherwise, the array base is the assumed-size array. If the mapped address range of a matchable candidate includes the first storage location of the assumed-size array, it is a matched candidate. If a matchable candidate does not exist for which the mapped address range includes the first storage location of the assumed-size array then a matchable candidate is a matched candidate if its extended address range includes the first storage location of the assumed-size array. If multiple matched candidates exist, an arbitrary one of them is the found matched candidate. The lower bound and length of the substitute array section are set such that its storage is identical to the storage of the found matched candidate. If a matched candidate is not found then a substitute array section is not formed and no further actions that are described in this section are performed for the list item.

## Fortran

The list items may include assumed-type variables and procedure pointers.

If a list item in a map clause is an assumed-type variable for which the storage location is included in the mapped address range of a matchable candidate, the list item is treated as if it refers to the storage of that matchable candidate. Otherwise, no further actions that are described in this section are performed for the list item.

## Fortran

If a list item is an array or array section, the array elements become implicit list items with the same modifiers (including the map-type) specified in the clause. If the array or array section is implicitly mapped and corresponding storage exists in the device data environment prior to a task encountering the construct on which the map clause appears, only those array elements that have corresponding storage are implicitly mapped.

If a mapper modifier is not present, the behavior is as if a mapper modifier was specified with the default parameter. The map behavior of a list item in a map clause is modified by a visible user-defined mapper (see Section 7.9.10) if the mapper-identifier of the mapper modifier is defined for a base language type that matches the type of the list item. Otherwise, the predefined default mapper for the type of the list item applies. The efect of the mapper modifier is to remove the list item from the map clause and to apply the clauses specified in the declared mapper to the construct on which the map clause appears. In the clauses applied by the mapper, references to var are replaced with references to the list item and the map-type is replaced with the output map type that is determined according to the rules of map-type decay. If any modifier with the

map-type-modifying property appears in the map clause then the efect is as if that modifier appears in each map clause specified in the declared mapper.

Unless otherwise specified, if a list item is a referencing variable then the efect of the map clause is applied to its referring pointer and, if a referenced pointee exists, its referenced pointee. For the purposes of the map clause, the referenced pointee is treated as if its referring pointer is the referring pointer of the referencing variable.

C++

If a list item is a reference and it does not have a containing structure then the map clause is applied only to its referenced pointee.

C++

Fortran

If a component of a derived type list item is a map clause list item that results from the predefined default mapper for that derived type, and if the derived type component is not an explicit list item or the array base of an explicit list item in a map clause on the construct then:

• If it has the POINTER attribute, it is attach-ineligible; and
