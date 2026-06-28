## 7.6.15 combiner Clause

<table><tr><td>Name: combiner</td><td>Properties: unique, required</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>combiner-expr</td><td>expression of combiner type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

declare\_reduction

## Semantics

This clause specifies combiner-expr as the combiner expression for a user-defined reduction.

## Cross References

• declare\_reduction Directive, see Section 7.6.14

• OpenMP Combiner Expressions, see Section 7.6.2.1

## 7.6.16 initializer Clause

<table><tr><td>Name: initializer</td><td>Properties: unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>initializer-expr</td><td>expression of initializer type</td><td>default</td></tr></table>

## Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

declare\_reduction

## Semantics

This clause specifies initializer-expr as the initializer expression for a user-defined reduction.

## Cross References

• declare\_reduction Directive, see Section 7.6.14

• OpenMP Initializer Expressions, see Section 7.6.2.2

## 7.6.17 declare\_induction Directive

<table><tr><td>Name:declare_inductionCategory:declarative</td><td>Association:unassociatedProperties:pure</td></tr></table>

## Arguments

declare\_induction(induction-specifier)

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>induction-specifier</td><td>OpenMP induction specifier</td><td>default</td></tr></table>

## Clauses

collector, inductor

## Semantics

The declare\_induction directive declares an induction identifier that can be used in an induction clause as a user-defined induction. The directive argument induction-specifier uses the following syntax:

```txt
induction-identifier : type-specifier-list
```

where type-specifier-list is defined as follows:

```txt
type-specifier-list := type-specifier | type-specifier , type-specifier-list
type-specifier := typename-list-item | typename-pair
typename-pair := ( typename-list-item , typename-list-item )
```

and where induction-identifier is the specified induction identifier and typename-list-item is a type-name list item

The induction identifier identifies the declare\_induction directive. The induction identifier can be used in an induction clause that lists induction variables of the types specified in the type-specifier-list, with corresponding step expressions of the same type if the type-specifier-list does not specify a typename-pair. If the type-specifier-list specifies a typename-pair then the induction identifier can be used in an induction clause that lists that pair, in which case the induction variable and omp\_var must be of the first type specified in the typename-pair while the corresponding step expression and omp\_step must be of the second type in the typename-pair. The type of omp\_idx is the type used for the iteration count of the collapsed iteration space of the collapsed loops of the construct on which the induction clause appears.

The visibility and accessibility of a user-defined induction are the same as those of a variable declared at the same location in the program.

The declare\_induction directive can also appear at the locations in a program where a static data member could be declared. In this case, the visibility and accessibility of the declaration are the same as those of a static data member declared at the same location in the program.

C++

The enclosing context of the inductor expression specified by the inductor clause and of the collector expression specified by the collector clause is that of the declare\_induction directive. The inductor expression and the collector expression must be correct in the base language, as if they were the body of a procedure defined at the same location in the program.

## Fortran

If the induction identifier is the same as the name of a user-defined operator or an extended operator, or the same as a generic name that is one of the allowed intrinsic procedures, and if the operator or procedure name appears in an accessibility statement in the same module, the accessibility of the corresponding declare\_induction directive is determined by the accessibility attribute of the statement.

If the induction identifier is the same as a generic name that is one of the allowed intrinsic procedures and is accessible, and if it has the same name as a derived type in the same module, the accessibility of the corresponding declare\_induction directive is determined by the accessibility of the generic name according to the base language.

Fortran

## Restrictions

Restrictions to the declare\_induction directive are as follows:

• An induction identifier must not be re-declared in the current scope for the same type or for a type that is compatible according to the base language rules.

• A type-name list item in the type-specifier-list must not declare a new type.

C / C++

• A type name in a declare\_induction directive must not be a function type, an array type, a reference type, or a type qualified with const, volatile or restrict.

C / C++

Fortran

• A type name in a declare\_induction directive must not be an enum type or an enumeration type.

Fortran

## Cross References

• collector Clause, see Section 7.6.19

• OpenMP Collector Expressions, see Section 7.6.2.4

• OpenMP Inductor Expressions, see Section 7.6.2.3

• OpenMP Loop-Iteration Spaces and Vectors, see Section 6.4.3

• OpenMP Reduction and Induction Identifiers, see Section 7.6.1

• inductor Clause, see Section 7.6.18

## 7.6.18 inductor Clause

<table><tr><td>Name: inductor</td><td>Properties: unique, required</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>inductor-expr</td><td>expression of inductor type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

declare\_induction

## Semantics

This clause specifies inductor-expr as the inductor expression for a user-defined induction.

## Cross References

• declare\_induction Directive, see Section 7.6.17

• OpenMP Inductor Expressions, see Section 7.6.2.3

## 7.6.19 collector Clause

<table><tr><td>Name: collector</td><td>Properties: unique, required</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>collector-expr</td><td>expression of collector type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

declare\_induction

## Semantics

This clause specifies collector-expr as the collector expression for a user-defined induction, which ensures that a collector is available for use in the closed form of the induction operation.

## Cross References

• declare\_induction Directive, see Section 7.6.17

• OpenMP Collector Expressions, see Section 7.6.2.4
