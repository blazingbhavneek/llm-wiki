
This section defines concepts and restrictions on base language code used in OpenMP. The concepts help support base language neutrality for OpenMP directives and their associated semantics.

## 6.1 OpenMP Types and Identifiers

An OpenMP identifier is a special identifier for use within OpenMP programs for some specific purpose. For example, reduction identifiers specify the combiner OpenMP operation to use in a reduction, OpenMP mapper identifiers specify the name of a user-defined mapper, and foreign runtime identifiers specify the name of a foreign runtime.

Predefined identifiers can be used in base language code. Many predefined identifiers have the constant property, as is indicated where they are defined in this specification. The implementation implicitly declares these OpenMP identifiers and evaluates them when they are referenced in a given context.

Generic OpenMP types specify the type of expression or variable that is used in OpenMP contexts regardless of the base language. These OpenMP types support the definition of many important OpenMP concepts independently of the base language in which they are used.

Assignable OpenMP type instances are defined to facilitate base language neutrality. An assignable OpenMP type instance can be used as an argument of a construct in order for the implementation to modify the value of that instance.

C / C++

An assignable OpenMP type instance is an lvalue expression of that OpenMP type.

C / C++

Fortran

An assignable OpenMP type instance is a variable or a function reference with data pointer result of that OpenMP type.

Fortran

The logical OpenMP type supports logical variables and expressions in any base language.

C / C++

Any expression of logical OpenMP type is a scalar expression. This document uses true as a generic term for a non-zero integer value and false as a generic term for an integer value of zero.

C / C++

Fortran

Any expression of logical OpenMP type is a scalar logical expression. This document uses true as a generic term for a logical value of .TRUE. and false as a generic term for a logical value of .FALSE..

Fortran

The integer OpenMP type supports integer variables and expressions in any base language.

C / C++

Any expression of integer OpenMP type is an integer expression.

C / C++

Fortran

Any expression of integer OpenMP type is a scalar integer expression.

Fortran

The string OpenMP type supports character string variables and expressions in any base language.

C / C++

Any expression of string OpenMP type is an expression of type qualified or unqualified const char \* or char \* pointing to a null-terminated character string.

C / C++

Fortran

Any expression of string OpenMP type is a character string of default kind.

Fortran

OpenMP function identifiers support procedure names in any base language. Regardless of the base language, any OpenMP function identifier is the name of a procedure as a base language identifier.

Each OpenMP type other than those specifically defined in this section has a generic name,

<generic\_name>, by which it is referred throughout this document and that is used to construct the base language construct that corresponds to that OpenMP type. Some OpenMP types are OMPD types or OMPT types; all of these OpenMP types have generic names.

C / C++

Unless otherwise specified, an OMPD trace record has a <generic\_name> OMPD type, which corresponds to the type ompd\_record\_<generic\_name>\_t and an OMPD callback has a <generic\_name> OMPD type signature, which corresponds to the type

ompd\_callback\_<generic\_name>\_fn\_t. Unless otherwise specified, all other<generic\_name> OMPD types correspond to the type ompd\_<generic\_name>\_t.

Unless otherwise specified, an OMPT trace record has a <generic\_name> OMPT type, which corresponds to the type ompt\_record\_<generic\_name>\_t and an OMPT callback has a <generic\_name> OMPT type signature, which corresponds to the type

ompt\_callback\_<generic\_name>\_t. Unless otherwise specified, all other <generic\_name>OMPT types correspond to the type ompt\_<generic\_name>\_t.

Otherwise, unless otherwise specified, a variable of <generic\_name> OpenMP type is a variable oftype omp\_<generic\_name>\_t.

C / C++

Fortran

Unless otherwise specified, the type of an OMPD trace record is not defined and the type signature of an OMPD callback is not defined. Unless otherwise specified, a variable of a <generic\_name> OMPD type is an integer scalar variable of kind ompd\_<generic\_name>\_kind.

Unless otherwise specified, the type of an OMPT trace record is not defined and the type signature of an OMPT callback is not defined. Unless otherwise specified, a variable of a <generic\_name> OMPT type is an integer scalar variable of kind ompt\_<generic\_name>\_kind.

Otherwise, unless otherwise specified, a variable of <generic\_name> OpenMP type is an integerscalar variable of kind omp\_<generic\_name>\_kind.

Fortran

## Cross References
