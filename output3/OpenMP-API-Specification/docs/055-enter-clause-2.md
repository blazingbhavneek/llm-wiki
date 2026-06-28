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
