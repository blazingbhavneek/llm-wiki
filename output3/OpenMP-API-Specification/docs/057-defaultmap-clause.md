
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
