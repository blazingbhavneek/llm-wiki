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
