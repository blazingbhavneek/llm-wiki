
The OpenMP API defines several kinds of lists, each of which can be used as syntactic instances of directive, clause and modifier arguments. These comma-separated argument lists allow the corresponding semantics to apply to multiple list items. In any argument list the separation of list items has precedence for commas over any base language semantics for commas. Thus, application of base language semantics for commas to any expression in an argument list may require the use of parentheses.

A list of any OpenMP type consists of a comma-separated collection of one or more expressions of that OpenMP type. A parameter list consists of a comma-separated collection of one or more parameter list items. A variable list consists of a comma-separated collection of one or more variable list items. An extended list consists of a comma-separated collection of one or more extended list items, each of which is a variable list item or the name of a procedure. A locator list consists of a comma-separated collection of one or more locator list items. A type-name list consists of a comma-separated collection of one or more type-name list items. A directive-name list consists of a comma-separated collection of one or more directive-name list items, each of which is a directive name. A directive-specification list consists of a comma-separated collection of one or more directive-specification list items, each of which is a directive specification. A preference specification list consists of a comma-separated collection of one or more preference specification list items, each of which is a preference specification as defined in Section 16.1.3. An OpenMP operation list consists of a comma-separated collection of one or more OpenMP operation list items, each of which is a OpenMP operation defined in Section 5.2.3. An iterator-specifier list consists of a comma-separated collection of one or more iterator-specifier list items, each of which is an iterator specifier defined in Section 5.2.6.

A parameter list item can be one of the following:

• A named parameter list item;

• The position of a parameter in a parameter specification specified by a positive integer, where 1 represents the first parameter; or

• A parameter range specified by lb : ub where both lb and ub must be an expression of integer OpenMP type with the constant property and the positive property.

In both lb and ub, an expression using omp\_num\_args, that enables identification of parameters relative to the last argument of the call, can be used with the form:

$$
\text {omp\_num\_args} [ \pm \text {logical\_offset} ]
$$

where logical\_ofset is an expression of integer OpenMP type with the constant property and the non-negative property. The lb and ub expressions are both optional. If lb is not specified the first element of the range will be 1. If ub is not specified the last element of the range will be omp\_num\_args. The efect of a specified range of lb..ub is as if the parameters $l b ^ { t \bar { h } } , ( l b + 1 ) ^ { t h } , . . . , u b ^ { t h }$ had been specified individually.

C / C++

A named parameter list item is the name of a function parameter. A variable list item is a variable or an array section. A locator list item is a reserved locator, an array section, or any lvalue expression including variables. A type-name list item is a type name.

C / C++

Fortran

A named parameter list item is a dummy argument of a subroutine or function. A variable list item is one of the following:

• a variable that is not coindexed and that is not a substring;

• an array section that is not coindexed and that does not contain an element that is a substring;

• a named constant;

• a procedure pointer;

• an associate name that may appear in a variable definition context; or

• a common block name (enclosed in slashes).

A locator list item is a variable list item, a function reference with data pointer result, or a reserved locator. A type-name list item is a type specifier.

When a named common block appears in an argument list, it has the same meaning and restrictions as if every explicit member of the common block appeared in the list. An explicit member of a common block is a variable that is named in a COMMON statement that specifies the common block name and is declared in the same scoping unit in which the clause appears. Named common blocks do not include the blank common block.

Fortran

## Restrictions

The restrictions to argument lists are as follows:

• All list items must be visible, according to the scoping rules of the base language.

• Unless otherwise specified, OpenMP list items other than parameter list items must be directive-wide unique, i.e., a list item can only appear once in one OpenMP list of all arguments, clauses, and modifiers of the directive.

• Unless otherwise specified, any given parameter list item can only be specified once across all clauses of the same type in a given directive.

• The directive-specifier and the clauses in a directive-specification list item must not be comma-separated.

C

• Unless otherwise specified, a variable that is part of an aggregate variable must not be a variable list item or an extended list item.

C

C++

• Unless otherwise specified, a variable that is part of an aggregate variable must not be a variable list item or an extended list item except if the list appears on a clause that is associated with a construct within a class non-static member function and the variable is an accessible data member of the object for which the non-static member function is invoked.

C++

Fortran

• A named constant or a procedure pointer can appear as a list item only in clauses where it is explicitly allowed.

• Unless otherwise specified, a variable that is part of an aggregate variable must not be a variable list item or an extended list item.

• Unless otherwise specified, an assumed-type variable must not be a variable list item, an extended list item, or a locator list item.

• A type-name list item must not specify an abstract type or be either CLASS(\*) or TYPE(<sub>\*</sub>).

• Since common block names cannot be accessed by use association or host association, a common block name specified in a clause must be declared to be a common block in the same scoping unit in which the clause appears.

Fortran

## 5.2.2 Reserved Locators

On some directives, some clauses accept the use of reserved locators as special OpenMP identifiers that represent system storage not necessarily bound to any base language storage item. The reserved locators are:

omp\_all\_memory

The reserved locator omp\_all\_memory is an OpenMP identifier that denotes a list item treated as having storage that corresponds to the storage of all other objects in memory.

## Restrictions

Restrictions to the reserved locators are as follows:

• Reserved locators may only appear in clauses and directives where they are explicitly allowed and may not otherwise be referenced in an OpenMP program.

## 5.2.3 OpenMP Operations

On some directives, some clauses accept the use of OpenMP operations. An OpenMP operation named <generic\_name> is a special expression that may be specified in an OpenMP operation list and that is used to return an object of the <generic\_name> OpenMP type (see Section 6.1). In general, the format of an OpenMP operation is the following:

<generic\_name>(operation-parameter-specification)

$$
\mathrm{C/C++}
$$

## 5.2.4 Array Shaping

If an expression has a type of pointer to T, then a shape-operator can be used to specify the extent of that pointer. In other words, the shape-operator is used to reinterpret, as an n-dimensional array, the region of memory to which that expression points.

Formally, the syntax of the shape-operator is as follows:

$$
\text {shaped - expression} := \left(\left[ s _ {1} \right] \left[ s _ {2} \right] \dots \left[ s _ {n} \right]\right) \text {cast - expression}
$$

The result of applying the shape-operator to an expression is an lvalue expression with an n-dimensional array type with dimensions $s _ { I } \times s _ { 2 } \ldots \times s _ { n }$ and element type T.

The precedence of the shape-operator is the same as a type cast.

Each $s _ { i }$ is an integral type expression that must evaluate to a positive integer.

## Restrictions

Restrictions to the shape-operator are as follows:

• The type T must be a complete type.

• The shape-operator can appear only in clauses for which it is explicitly allowed.

• The result of a shape-operator must be a containing array of the list item or a containing array of one of its named pointers.

• The type of the expression upon which a shape-operator is applied must be a pointer type.

$$
\mathrm{C} + +
$$
