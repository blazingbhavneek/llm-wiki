## 7.5.5 lastprivate Clause

<table><tr><td>Name: lastprivate</td><td>Properties: data-environment attribute, data-sharing attribute, original list-item updating, privatization</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>lastprivate-modifier</td><td>list</td><td>Keyword:conditional</td><td>default</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword:directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

distribute, do, for, loop, sections, simd, taskloop

## Semantics

The lastprivate clause provides a superset of the functionality provided by the private clause. A list item that appears in a lastprivate clause is subject to the private clause semantics described in Section 7.5.3. In addition, each new list item has the lastprivate attribute. Further, when a lastprivate clause without the conditional modifier appears on a directive and the list item is not a loop-iteration variable of any afected loop, the value of each new list item from the sequentially last iteration of the afected loops, or the lexically last structured block sequence associated with a sections construct, is assigned to the original list item. Alternatively, when the conditional modifier appears on the clause or the list item is a loop-iteration variable of one of the afected loops, if execution of the canonical loop nest, when it is not associated with a directive, would assign a value to the list item then the original list item is assigned that value.

For class types, the copy assignment operator is invoked. The order in which copy assignment operators for diferent variables of the same class type are invoked is unspecified.

C++ C / C++

For an array of elements of non-array type, each element is assigned to the corresponding element of the original array.

C / C++ Fortran

If the original list item does not have the POINTER attribute, its update occurs as if by intrinsic assignment unless it has a type bound procedure as a defined assignment.

If the original list item has the POINTER attribute, its update occurs as if by pointer assignment.

Fortran

When the conditional modifier does not appear on the lastprivate clause, any list item that is not a loop-iteration variable of the afected loops and that is not assigned a value by the sequentially last iteration of the loops, or by the lexically last structured block sequence associated with a sections construct, has an unspecified value after the construct. When the conditional modifier does not appear on the lastprivate clause, a list item that is the loop-iteration variable of an afected loop has an unspecified value after the construct if it would not be assigned a value during execution of the canonical loop nest when the loop nest is not associated with a directive. Unassigned subcomponents also have unspecified values after the construct.

If the lastprivate clause is used on a construct to which neither the nowait nor the nogroup clauses are applied, the original list item becomes defined at the end of the construct. Otherwise, if the lastprivate clause is used on a construct to which the nowait or the nogroup clauses are applied, accesses to the original list item may create a data race so if an assignment to the original list item occurs then other synchronization must ensure that the assignment completes and the original list item is flushed to memory. In either case, to avoid data races, concurrent reads or updates of the original list item must be synchronized with any update of the original list item that occurs as a result of the lastprivate clause.

If a list item that appears in a lastprivate clause with the conditional modifier is modified in the region by an assignment outside the construct or by an assignment that does not lexically assign to the list item then the value assigned to the original list item is unspecified.

## Restrictions

Restrictions to the lastprivate clause are as follows:

• A list item must not appear in a lastprivate clause on a work-distribution construct if the corresponding region binds to the region of a parallelism-generating construct in which the list item is private.

• A list item that appears in a lastprivate clause with the conditional modifier must be a scalar variable.

## C++

• A variable of class type (or array thereof) that appears in a lastprivate clause requires an accessible, unambiguous default constructor for the class type, unless the list item is also specified in a firstprivate clause.

• A variable of class type (or array thereof) that appears in a lastprivate clause requires an accessible, unambiguous copy assignment operator for the class type.

• If an original list item in a lastprivate clause on a work-distribution construct has a reference type then it must bind to the same object for all threads in the binding thread set of the work-distribution region.

C++

Fortran

• A variable that appears in a lastprivate clause must be definable.

• If the original list item has the ALLOCATABLE attribute, the corresponding list item of which the value is assigned to the original list item must have an allocation status of allocated upon exit from the sequentially last iteration of the afected loops or lexically last structured block sequence associated with a sections construct.

• If the list item is a polymorphic variable with the ALLOCATABLE attribute, the behavior is unspecified.

Fortran

## Cross References

• distribute Construct, see Section 13.7

• do Construct, see Section 13.6.2

• for Construct, see Section 13.6.1

• loop Construct, see Section 13.8

• private Clause, see Section 7.5.3

• sections Construct, see Section 13.3

• simd Construct, see Section 12.4

• taskloop Construct, see Section 14.2

## 7.5.6 linear Clause

Modifiers

<table><tr><td>Name: linear</td><td>Properties: data-environment attribute, data-sharing attribute, privatization, innermost-leaf, post-modified</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>step-simple-modifier</td><td>list</td><td>OpenMP integer expression</td><td>exclusive, region-invariant, unique</td></tr><tr><td>step-complex-modifier</td><td>list</td><td>Complex, name: stepArguments:linear-stepexpression of integer type (region-invariant)</td><td>unique</td></tr><tr><td>linear-modifier</td><td>list</td><td>Keyword: ref, uval, val</td><td>unique</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

declare\_simd, do, for, simd

## Semantics

The linear clause provides a superset of the functionality provided by the private clause. A list item that appears in a linear clause is subject to the private clause semantics described in Section 7.5.3, except as noted. Additionally, each new list item has the linear attribute and so is a linear variable. If the step-simple-modifier is specified, the behavior is as if the step-complex-modifier is instead specified with step-simple-modifier as its linear-step argument. If linear-step is not specified, it is assumed to be one.

When a linear clause is specified on a loop-collapsing construct and a list item is the loop-iteration variable of an afected loop, the efect is as if that list item had appeared in a lastprivate clause. Otherwise, when a linear clause is specified on a loop-collapsing construct, the value of the new list item on each collapsed iteration corresponds to the value of the original list item before entering the construct plus the logical number of the iteration times linear-step. The value that corresponds to the sequentially last collapsed iteration of the collapsed loops is assigned to the original list item.

When a linear clause is specified on a declare\_simd directive, the list items refer to parameters of the procedure to which the directive applies. For a given call to the procedure, the clause determines whether the SIMD version generated by the directive may be called. If the clause does not specify the ref linear-modifier, the SIMD version requires that the value of the corresponding argument at the callsite is equal to the value of the argument from the first lane plus the logical number of the SIMD lane times the linear-step. If the clause specifies the ref linear-modifier, the SIMD version requires that the storage locations of the corresponding arguments at the callsite from each SIMD lane correspond to storage locations within a hypothetical array of elements of the same type, indexed by the logical number of the SIMD lane times the linear-step.

## Restrictions

Restrictions to the linear clause are as follows:

• If a reduction clause with the inscan modifier also appears on the construct, only loop-iteration variables of afected loops may appear as list items in a linear clause.

• A linear-modifier may be specified as ref or uval only for linear clauses on declare\_simd directives.

• For a linear clause that appears on a loop-nest-associated directive, the diference between the value of a list item at the end of a collapsed iteration and its value at the beginning of the collapsed iteration must be equal to linear-step.

• If linear-modifier is uval for a list item in a linear clause that is specified on a declare\_simd directive and the list item is modified during a call to the SIMD version of the procedure, the OpenMP program must not depend on the value of the list item upon return from the procedure.

• If linear-modifier is uval for a list item in a linear clause that is specified on a declare\_simd directive, the OpenMP program must not depend on the storage of the argument in the procedure being the same as the storage of the corresponding argument at the callsite.

• None of the afected loops of a loop-nest-associated construct that has a linear clause may be a non-rectangular loop.

• All list items must be of integral or pointer type.

• If specified, linear-modifier must be val.

C

C++

• If linear-modifier is not ref, all list items must be of integral or pointer type, or must be a reference to an integral or pointer type.

• If linear-modifier is ref or uval, all list items must be of a reference type.

• If a list item in a linear clause on a worksharing construct has a reference type then it must bind to the same object for all threads of the team.

• If a list item in a linear clause that is specified on a declare\_simd directive is of a reference type and linear-modifier is not ref, the diference between the value of the argument on exit from the function and its value on entry to the function must be the same for all SIMD lanes.

C++

Fortran

• If linear-modifier is not ref, all list items must be of type integer.

• If linear-modifier is ref or uval, all list items must be dummy arguments without the VALUE attribute.

• List items must not be variables that have the POINTER attribute.

• If linear-modifier is not ref and a list item has the ALLOCATABLE attribute, the allocation status of the list item in the last collapsed iteration must be allocated upon exit from that collapsed iteration.

• If linear-modifier is ref, list items must be polymorphic variables, assumed-shape arrays, or variables with the ALLOCATABLE attribute.

• If a list item in a linear clause that is specified on a declare\_simd directive is a dummy argument without the VALUE attribute and linear-modifier is not ref, the diference between the value of the argument on exit from the procedure and its value on entry to the procedure must be the same for all SIMD lanes.

• A common block name must not be a list item in a linear clause.

Fortran

## Cross References

• declare\_simd Directive, see Section 9.8

• do Construct, see Section 13.6.2

• for Construct, see Section 13.6.1

• private Clause, see Section 7.5.3

• simd Construct, see Section 12.4

• taskloop Construct, see Section 14.2

## 7.5.7 is\_device\_ptr Clause

<table><tr><td>Name: is_device_ptr</td><td>Properties: data-environment attribute, data-sharing attribute, device-associated, innermost-leaf, privatization</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

dispatch, target

## Semantics

The is\_device\_ptr clause indicates that its list items are device pointers. Support for device pointers created outside of any OpenMP mechanism that returns a device pointer, is implementation defined.

If the is\_device\_ptr clause is specified on a target construct, each list item is privatized inside the construct. Each new list item has the is-device-ptr attribute and is initialized to the device address to which the original list item refers.

## Restrictions

Restrictions to the is\_device\_ptr clause are as follows:

• Each list item must be a valid device pointer for the device data environment.

## Cross References

• dispatch Construct, see Section 9.7

• has\_device\_addr Clause, see Section 7.5.9

• target Construct, see Section 15.8

## 7.5.8 use\_device\_ptr Clause

<table><tr><td>Name: use_device_ptr</td><td>Properties: all-data-environments, data-environment attribute, data-sharing attribute, device-associated, privatization</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

## target\_data

## Semantics

Each list item in the use\_device\_ptr clause results in a new list item that has the use-device-ptr attribute and is a device pointer that refers to a device address. Since the use\_device\_ptr clause is an all-data-environments clause, it has this efect even for minimal data environments. The device address is determined as follows. A list item is treated as if a zero-ofset assumed-size array at the storage location to which the list item points is mapped by a map clause on the construct with a map-type of storage. If a matched candidate is found for the assumed-size array (see Section 7.9.6), the new list item refers to the device address that is the base address of the array section that corresponds to the assumed-size array in the device data environment. Otherwise, the new list item refers to the address stored in the original list item. All references to the list item inside the structured block associated with the construct are replaced with the new list item that is a private copy in the associated data environment on the encountering device. Thus, the use\_device\_ptr clause is a privatization clause.

## Restrictions

Restrictions to the use\_device\_ptr clause are as follows:

• Each list item must be a C pointer for which the value is the address of an object that has corresponding storage or is accessible on the target device.

Cross References

• target\_data Construct, see Section 15.7

## 7.5.9 has\_device\_addr Clause

<table><tr><td>Name: has_device_addr</td><td>Properties: data-environment attribute, data-sharing attribute, device-associated, outermost-leaf</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

dispatch, target

## Semantics

The has\_device\_addr clause indicates that its list items already have device addresses and therefore they may be directly accessed from a target device. Inside the construct, the list items have the has-device-addr attribute. The list items may include array sections. If the list item is a referencing variable, the semantics of the has\_device\_addr clause apply to its referenced pointee. When the clause appears on the target construct, if the device address of a list item is not for the device on which the target region executes, accessing the list item inside the region results in unspecified behavior.

## Fortran

For a list item in a has\_device\_addr clause, the CONTIGUOUS attribute, storage location, storage size, array bounds, character length, association status and allocation status (as applicable) are the same inside the construct on which the clause appears as for the original list item. The result of inquiring about other list item properties inside the structured block is implementation defined. For a list item that is an array section, the array bounds and result when invoking C\_LOC inside the structured block is the same as if the array base had been specified in the clause instead.

Fortran

## Restrictions

Restrictions to the has\_device\_addr clause are as follows:

C / C++

• Each list item must have a valid device address for the device data environment.

C / C++

## Fortran

• A list item must either have a valid device address for the device data environment, be an unallocated allocatable variable, or be a disassociated data pointer.

• The association status of a list item that is a pointer must not be undefined unless it is a structure component and it results from a predefined default mapper.

Fortran

## Cross References

• dispatch Construct, see Section 9.7

• target Construct, see Section 15.8

## 7.5.10 use\_device\_addr Clause

<table><tr><td>Name: use_device_addr</td><td>Properties: all-data-environments, data-environment attribute, data-sharing attribute, device-associated</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

## target\_data

## Semantics

Each list item in a use\_device\_addr clause has the use-device-addr attribute inside the construct. If the list item is present in the device data environment on entry to the construct, the list item is treated as if it is implicitly mapped by a map clause on the construct with a map-type of storage and all references to the list item inside the structured block associated with the construct are to the corresponding list item in the device data environment. The list items in a use\_device\_addr clause may include array sections and assumed-size arrays. Since the use\_device\_addr clause is an all-data-environments clause, it has this efect even for minimal data environments.

If the list item is a referencing variable, the semantics of the use\_device\_addr clause apply to its referenced pointee. A private copy of the referring pointer that refers to the corresponding referenced pointee is used in place of the original referring pointer in the structured block.

C / C++

If a list item is an array section that has a base pointer, all references to the base pointer inside the structured block are replaced with a new pointer that contains the base address of the corresponding list item. This conversion may be elided if no corresponding list item is present.

C / C++

## Restrictions

Restrictions to the use\_device\_addr clause are as follows:

• Each list item must have a corresponding list item in the device data environment or be accessible on the target device.

• If a list item is an array section, the array base must be a base language identifier.

## Cross References

• target\_data Construct, see Section 15.7
