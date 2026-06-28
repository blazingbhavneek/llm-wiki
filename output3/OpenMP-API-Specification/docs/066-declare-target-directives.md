
<table><tr><td>Name:declare_targetCategory:declarative</td><td>Association:explicitProperties:declare-target, device, pure, variant-generating</td></tr></table>

## Arguments

declare\_target(extended-list)

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>extended-list</td><td>list of extended list item type</td><td>optional</td></tr></table>

## Clauses

device\_type, enter, indirect, link, local

## Additional information

The declare\_target directive may alternatively be specified with declare target as the directive-name.

## Semantics

The declare\_target directive is a declare target directive. If the extended-list argument is specified, the efect is as if any list items from extended-list that are not groupprivate variables appear in the list argument of an implicit enter clause and any list items that are groupprivate variables appear in the list argument of an implicit local clause.

If neither the extended-list argument nor a data-environment attribute clause is specified then the directive is a declaration-associated directive. The efect is as if the name of the associated procedure appears as a list item in an enter clause of a declare target directive that otherwise specifies the same set of clauses.

## C / C++

If the declare\_target directive is specified as an attribute specifier with the decl attribute and a decl attribute is not used on the declaration to specify groupprivate variables, the efect is as if an enter clause is specified if a link or local clause is not specified.

If the declare\_target directive is specified as an attribute specifier with the decl attribute and a decl attribute is used on the declaration to specify groupprivate variables, the efect is as if a local clause is specified.

## C / C++

## Restrictions

Restrictions to the declare\_target directive are as follows:

• If the extended-list argument is specified, no clauses may be specified.

• If the directive is not a declaration-associated directive and an extended-list argument is not specified, a data-environment attribute clause must be present.

• A variable for which nohost is specified must not appear in a link clause.

• A groupprivate variable must not appear in any enter clauses or link clauses.

$$
\mathrm{C} / \mathrm{C} + +
$$

• If the directive is not a declaration-associated directive, it must appear at the same scope as the declaration of every list item in its extended-list or in its data-environment attribute clauses.

$$
\mathrm{C} / \mathrm{C} + +
$$

• If a list item is a procedure name, it must not be a generic name, procedure pointer, entry name, or statement function name.

• If the directive is a declaration-associated directive, the directive must appear in the specification part of a subroutine subprogram, function subprogram or interface body.

• If a list item is a procedure name that is not declared via a procedure declaration statement, the directive must be in the specification part of the subprogram or interface body of that procedure.

• If a list item in extended-list is a variable, the directive must appear in the specification part in which the variable is declared.

• If a declare\_target directive is specified for a procedure that has an explicit interface then the definition of the procedure must contain a declare\_target directive with identical clauses with identical arguments and modifiers.

• If an external procedure is a type-bound procedure of a derived type and the directive is specified in the definition of the external procedure, it must appear in the interface block that is accessible to the derived-type definition.

• If any procedure is declared via a procedure declaration statement that is not in the type-bound procedure part of a derived-type definition, any declare\_target directive with the procedure name must appear in the same specification part.

• If a declare\_target directive that specifies a common block name appears in one program unit, then such a directive must also appear in every other program unit that contains a COMMON statement that specifies the same name, after the last such COMMON statement in the program unit.

• If a list item is declared with the BIND attribute, the corresponding C entities must also be specified in a declare\_target directive in the C program.

• A variable can only appear in a declare\_target directive in the scope in which it is declared. It must not be an element of a common block or appear in an EQUIVALENCE statement.

## Cross References

• device\_type Clause, see Section 15.1

• enter Clause, see Section 7.9.7

• Declare Target Directives, see Section 9.9

• indirect Clause, see Section 9.9.3

• link Clause, see Section 7.9.8

C / C++

## 9.9.2 begin declare\_target Directive

<table><tr><td>Name: begindeclare_targetCategory:declarative</td><td>Association:delimitedProperties:declare-target,device,variant-generating</td></tr></table>

## Clauses

device\_type, indirect

## Additional information

The begin declare\_target directive may alternatively be specified with begin declare target as the directive-name.

## Semantics

The begin declare\_target directive is a declare target directive. The directive and its paired end directive form a delimited code region that defines an implicit extended-list and implicit local-list that is converted to an implicit enter clause with the extended-list as its argument and an implicit local clause with the local-list as its argument, respectively. The delimited code region is a declaration sequence.

The implicit extended-list consists of the variable and procedure names of any variable or procedure declarations at file scope that appear in the delimited code region, excluding declarations of groupprivate variables. If any groupprivate variables are declared in the delimited code region, the efect is as if the variables appear in the implicit local-list.

![](images/c17b6c8479cccb0475d28f0fc0d9c3bedd934039a0adda8c9e343d870508ef8a.jpg)

Additionally, the implicit extended-list and local-list consist of the variable and procedure names of any variable or procedure declarations at namespace or class scope that appear in the delimited code region, including the operator() member function of the resulting closure type of any lambda expression that is defined in the delimited code region.

![](images/f32c82abded3c299b286cfa83526350904043c25be62bead906b0c6e87246f1f.jpg)

The delimited code region may contain declare target directives. If a device\_type clause is present on the contained declare target directive, then its argument determines which versions are made available. If a list item appears both in an implicit and explicit list, the explicit list determines which versions are made available.

![](images/44373eb8a082613619d2818813e27b66c0b4049c0c612cd1edf880ccede1c626.jpg)

## Restrictions

Restrictions to the begin declare\_target directive are as follows:

C++

• The function names of overloaded functions or template functions may only be specified within an implicit extended-list.

• If a lambda declaration and definition appears between a begin declare\_target directive and the paired end directive, all variables that are captured by the lambda expression must also appear in an enter clause.

• A module export or import statement may not appear between a begin declare\_target directive and the paired end directive.

## Cross References

• device\_type Clause, see Section 15.1

• enter Clause, see Section 7.9.7

• Declare Target Directives, see Section 9.9

• indirect Clause, see Section 9.9.3

C / C++
