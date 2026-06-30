# OpenMP-API-Specification Source Lines 6353-6928

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source OpenMP-API-Specification:L6353-L6928

Citation: [OpenMP-API-Specification:L6353-L6928]

````text
## 5.1.1 Free Source Form Directives

The following sentinels are recognized in free form source files:

!\$omp | !\$ompx

The sentinel can appear in any column as long as it is preceded only by white space. It must appear as a single word with no intervening white space. Fortran free form line length and white space rules apply to the directive line. The syntax that allows white space to be optional has been deprecated. Initial directive lines must have a space after the sentinel. The initial line of a directive must not be a continuation line for a base language statement. Fortran free form continuation rules apply. Thus, continued directive lines must have an ampersand (&) as the last non-blank character on the line, prior to any comment placed inside the directive; continuation directive lines can have an ampersand after the directive sentinel with optional white space before and after the ampersand.

Comments may appear on the same line as a directive. The exclamation point (!) initiates a comment. The comment extends to the end of the source line and is ignored. If the first non-blank character after the directive sentinel is an exclamation point, the line is ignored.

Fortran

## 5.1.2 Fixed Source Form Directives

The following sentinels are recognized in fixed form source files:

<table><tr><td>! $omp | c$omp | *$omp | ! $omx | c$omx | *$omx</td></tr></table>

Sentinels must start in column 1 and appear as a single word with no intervening characters. Fortran fixed form line length, white space, continuation, and column rules apply to the directive line. The syntax that allows white space to be optional has been deprecated. Initial directive lines must have a space or a zero in column 6, and continuation directive lines must have a character other than a space or a zero in column 6.

Comments may appear on the same line as a directive. The exclamation point initiates a comment when it appears after column 6. The comment extends to the end of the source line and is ignored. If the first non-blank character after the directive sentinel of an initial or continuation directive line is an exclamation point, the line is ignored.

Fortran

## 5.2 Clause Format

This section defines the format and categories of OpenMP clauses. Clauses are specified as part of a directive-specification. Clauses have the optional property and, thus, may be omitted from a directive-specification unless otherwise specified, in which case they have the required property. The order in which clauses appear on directives is not significant unless otherwise specified. Some clauses form natural groupings that have similar semantic efect and so are frequently specified as a clause group. A clause-specification specifies each clause in a directive-specification where clause-specification is:

clause-name[(clause-argument-specification [; clause-argument-specification [;...]])]

C / C++

White space in a clause-name is prohibited. White space within a clause-argument-specification and between another clause-argument-specification is optional.

C / C++

An implementation may allow clauses with clause names that start with the ompx\_ prefix for use on any OpenMP directive, and the format and semantics of any such clause is implementation defined.

The first clause-argument-specification is required unless otherwise explicitly specified while additional ones are only permitted on clauses that explicitly allow them. When the first one is omitted, the syntax is simply:

clause-name

Clause arguments may be unmodified or modified. For an unmodified argument, clause-argument-specification is:

## clause-argument-list

Unless otherwise specified, modified arguments have the pre-modified property, in which case the format is:

## [modifier-specification-list :]clause-argument-list

Some modified arguments are explicitly specified to have the post-modified property, in which case the format is:

## clause-argument-list[: modifier-specification-list]

For many clauses, clause-argument-list is an OpenMP argument list, which is a comma-separated list of a specific kind of list items (see Section 5.2.1), in which case the format of clause-argument-list is:

## argument-name

For all other clauses, clause-argument-list is a comma-separated list of arguments so the format is: argument-name [, argument-name [,... ]]

In most of these cases, the list only has a single item so the format of clause-argument-list is again: argument-name

In all cases, white space in clause-argument-list is optional.

A modifier-specification-list is a comma-separated list of clause argument modifiers for which the format is:

## modifier-specification [, modifier-specification [,... ]]

Clause argument modifiers may be simple modifiers or complex modifier. Many clause argument modifiers are simple modifiers, for which the format of modifier-specification is:

## modifier-name

## modifier-name[(modifier-parameter-specification)]

where modifier-parameter-specification is a comma-separated list of arguments as defined above for clause-argument-list. The position of each modifier-argument-name in the list is significant. The modifier-parameter-specification and parentheses are required unless every modifier-argument-name is optional and omitted, in which case the format of the complex modifier is identical to that of a simple modifier: ■modifier-name

## modifier-name

Each argument-name and modifier-name is an OpenMP term that may be used in the definitions of the clause and any directives on which the clause may appear. Syntactically, each of these terms is one of the following:

• keyword: An OpenMP keyword;

• OpenMP identifier: An OpenMP identifier;

• OpenMP argument list: An OpenMP argument list;

• expression: An expression of some OpenMP type; or

• OpenMP stylized expression: An OpenMP stylized expression.

A particular lexical instantiation of an argument specifies a parameter of the clause, while a lexical instantiation of a modifier and its parameters afects how or when the argument is applied.

The order of arguments must match the order in the clause-specification or modifier-specification. The order of modifiers in a clause-argument-specification is not significant unless otherwise specified.

General syntactic properties govern the use of clauses, clause and directive arguments, and modifiers in a directive. These properties are summarized in Table 5.1, along with the respective default properties for clauses, arguments and modifiers.

TABLE 5.1: Syntactic Properties for Clauses, Arguments and Modifiers

<table><tr><td>Property</td><td>Property Description</td><td>Inverse Property</td><td>Clause defaults</td><td>Argument defaults</td><td>Modifier defaults</td></tr><tr><td>required</td><td>must be present</td><td>optional</td><td>optional</td><td>required</td><td>optional</td></tr><tr><td>unique</td><td>may appear at most once</td><td>repeatable</td><td>repeatable</td><td>unique</td><td>unique</td></tr><tr><td>exclusive</td><td>must appear alone</td><td>compatible</td><td>compatible</td><td>compatible</td><td>compatible</td></tr><tr><td>ultimate</td><td>must lexically appear last (or first for a modifier on a clause with the post-modified property)</td><td>free</td><td>free</td><td>free</td><td>free</td></tr></table>

A clause, argument or modifier with a given property implies that it does not have the corresponding inverse property, and vice versa. The ultimate property implies the unique property. If all arguments and modifiers of an argument-modified clause or directive are optional property and omitted then the parentheses of the syntax for the clause or directive is also omitted.

Arguments of directives, clauses and modifiers are never repeatable. Instead, argument lists are used whenever the corresponding semantics may be specified for multiple list items that serve as the arguments of the directives, clauses or modifiers.

Some clause properties determine the constituent directives to which they apply when specified on compound directives. A clause with the all-constituents property applies to all constituent directives of any compound directive on which it is specified. Unless otherwise specified, a clause has the all-constituents property. That is, the all-constituents property is a default clause property. A clause with the once-for-all-constituents property applies to the directive once, before any of the constituent directives are applied. A clause with the innermost-leaf property applies to the innermost constituent directive to which it may be applied. A clause with the outermost-leaf property applies to the outermost constituent directive to which it may be applied. A clause with the all-privatizing property applies to all constituent directives that permit the clause and to which a data-sharing attribute clause that may create a private copy of the same list item is applied.

Arguments and modifiers that are expressions may additionally have any of the following value properties: the constant property; the positive property; the non-negative property; and the region-invariant property.

##

Note – In this example, clause-specification is depend(inout: d), clause-name is depend and clause-argument-specification is inout: d. The depend clause has an argument for which argument-name is locator-list, which syntactically is the OpenMP locator list d in the example. Similarly, the depend clause accepts a simple modifier with the name task-dependence-type. Syntactically, task-dependence-type is the keyword inout in the example.

#pragma omp depobj(o) depend(inout: d)

## ▲

The clauses that a directive accepts may form clause sets. These clause sets may imply restrictions on their use on that directive or may otherwise capture properties for the clauses on the directive. While specific properties may be defined for a clause set on a particular directive, the following clause set properties have general meanings and implications as indicated by the restrictions below: the required property, the unique property, and the exclusive property.

All clauses that are specified as a clause group form a clause set for which properties are specified with the specification of the clause group. Some directives accept a clause group for which each member is a directive-name of a directive that has a specific property. These clause groups have the required property, the unique property and the exclusive property unless otherwise specified.

The restrictions for a directive apply to the union of the clauses on the directive and its paired end directive.

## Restrictions

Restrictions to clauses and clause sets are as follows:

• A clause with the required property for a directive must appear on the directive.

• A clause with the unique property for a directive may appear at most once on the directive.

• A clause with the exclusive property for a directive must not appear if a clause with a diferent clause-name also appears on the directive.

• An ultimate clause, that is one that has the ultimate property for a directive, must be the lexically last clause to appear on the directive.

• If a clause set has the required property, at least one clause in the set must be present on the directive for which the clause set is specified.

• If a clause is a member of a clause set that has the unique property for a directive then the clause has the unique property for that directive regardless of whether it has the unique property when it is not part of such a clause set.

• If one clause of a clause set with the exclusive property appears on a directive, no other clauses with a diferent clause-name in that clause set may appear on the directive.

• An argument with the required property must appear in the clause-specification, unless otherwise specified.

• An argument with the unique property may appear at most once in a clause-argument-specification.

• An argument with the exclusive property must not appear if an argument with a diferent argument-name appears in the clause-argument-specification.

• A modifier with the required property must appear in the clause-argument-specification.

• A modifier with the unique property may appear at most once in a clause-argument-specification.

• A modifier with the exclusive property must not appear if a modifier with a diferent modifier-name also appears in the clause-argument-specification.

• If a clause has the pre-modified property, a modifier with the ultimate property must be the last modifier in any clause-argument-specification in which any modifier appears.

• If a clause has the post-modified property, a modifier with the ultimate property must be the first modifier in any clause-argument-specification in which any modifier appears.

• A modifier that is an expression must neither lexically match the name of a simple modifier defined for the clause that is an OpenMP keyword nor modifier-name parenthesized-tokens, where modifier-name is the modifier-name of a complex modifier defined for the clause and parenthesized-tokens is a token sequence that starts with ( and ends with ).

• An argument or parameter with the constant property must be a compile-time constant.

• An argument or parameter with the positive property must be greater than zero.

• An argument or parameter with the non-negative property must be greater than or equal to zero.

• An argument or parameter with the region-invariant property must have the same value throughout any given execution of the construct or, for declarative directives, execution of the procedure with which the declaration is associated.

## Cross References

• Directive Format, see Section 5.1

• OpenMP Argument Lists, see Section 5.2.1

• OpenMP Stylized Expressions, see Section 6.2

• OpenMP Types and Identifiers, see Section 6.1

## 5.2.1 OpenMP Argument Lists

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

• If the type T is a reference to a type $T '$ , then the type will be considered to be $T '$ for all purposes of the designated array.

C++ C / C++

## 5.2.5 Array Sections

An array section designates a subset of the elements in an array.

C / C++

To specify an array section in an OpenMP directive, array subscript expressions are extended with one of the following syntaxes:

```ini
[ lower-bound : length : stride]
[ lower-bound : length : ]
[ lower-bound : length ]
[ lower-bound : : stride]
[ lower-bound : : ]
[ lower-bound : ]
[ : length : stride]
[ : length : ]
[ : length ]
[ : : stride]
[ : : ]
[ : ]
```

The array section must be a subset of the original array.

Array sections are allowed on multidimensional arrays. Base language array subscript expressions can be used to specify length-one dimensions of multidimensional array sections.

Each of the lower-bound, length, and stride expressions if specified must be an integral type expression of the base language. When evaluated they represent a set of integer values as follows:

{ lower-bound, lower-bound + stride, lower-bound + 2 \* stride,... , lower-bound + ((length - 1) \* stride) }

The length must evaluate to a non-negative integer.

The stride must evaluate to a positive integer.

When the stride is absent it defaults to 1.

When the length is absent and the size of the dimension is known, it defaults to ⌈(size − lower-bound)/stride⌉, where size is the size of the array dimension. When the length is absent and the size of the dimension is not known, the array section is an assumed-size array.

When the lower-bound is absent it defaults to 0.

$$
\mathrm{C} / \mathrm{C} + + (\text {cont.})
$$

The precedence of a subscript operator that uses the array section syntax is the same as the precedence of a subscript operator that does not use the array section syntax.

Note – The following are examples of array sections:

```txt
a[0:6]
a[0:6:1]
a[1:10]
a[1:]
a[:10:2]
b[10][:][:]
b[10][:][:0]
c[42][0:6][:]
c[42][0:6:2][:]
c[1:10][42][0:6]
S.c[:100]
p->y[:10]
this->a[:N]
(p+10)[:N]
```

Assume a is declared to be a 1-dimensional array with dimension size 11. The first two examples are equivalent, and the third and fourth examples are equivalent. The fifth example specifies a stride of 2 and therefore is not contiguous.

Assume b is declared to be a pointer to a 2-dimensional array with dimension sizes 10 and 10. The sixth example refers to all elements of the 2-dimensional array given by b[10]. The seventh example is a zero-length array section.

Assume c is declared to be a 3-dimensional array with dimension sizes 50, 50, and 50. The eighth example is contiguous, while the ninth and tenth examples are not contiguous.

The final four examples show array sections that are formed from more general array bases.

The following are examples that are non-conforming array sections:

```clojure
s[:10].x
p[:10]->y
*(xp[:10])
```

For all three examples, a base language operator is applied in an undefined manner to an array section. The only operator that may be applied to an array section is a subscript operator for which the array section appears as the postfix expression.

C / C++

Fortran

Fortran has built-in support for array sections although some restrictions apply to their use in OpenMP directives, as enumerated at the end of this section.

Fortran

## Restrictions

Restrictions to array sections are as follows:

• An array section can appear only in clauses for which it is explicitly allowed.

• A stride expression may not be specified unless otherwise stated.

C / C++

• An assumed-size array can appear only in clauses for which it is explicitly allowed.

• An element of an array section with a non-zero size must have a complete type.

• The array base of an array section must have an array or pointer type.

• If a consecutive sequence of array subscript expressions appears in an array section, and the first subscript expression in the sequence uses the extended array section syntax defined in this section, then only the last subscript expression in the sequence may select array elements that have a pointer type.

C / C++

C++

• If the type of the array base of an array section is a reference to a type T, then the type will be considered to be T for all purposes of the array section.

• An array section cannot be used in an overloaded [] operator.

Fortran

• If a stride expression is specified, it must be positive.

• The upper bound for the last dimension of a dummy assumed-size array must be specified.

• If a list item is an array section with vector subscripts, the first array element must be the lowest in the array element order of the array section.

• If a list item is an array section, the last part-ref of the list item must have a section subscript list.

Fortran

## 5.2.6 iterator Modifier

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>iterator</td><td>locator-list</td><td>Complex, name: iteratorArguments:iterator-specifier list of iterator specifier list item type (default)</td><td>unique</td></tr></table>

Clauses

affinity, depend, from, map, to

An iterator modifier is a unique, complex modifier that defines a set of iterators, each of which is an iterator-identifier and an associated iterator value set. An iterator-identifier expands to those values in the clause argument for which it is specified. Each list item of the iterator argument is an iterator specifier with this format:

C / C++

[ iterator-type ] iterator-identifier = range-specification

C / C++

Fortran

[ iterator-type :: ] iterator-identifier = range-specification

Fortran

where:

• iterator-identifier is a base language identifier.

• iterator-type is a type that is permitted in a type-name list.

• range-specification is of the form begin:end[:step], where begin and end are expressions for which their types can be converted to iterator-type and step is an integral expression.

C / C++

In an iterator specifier, if the iterator-type is not specified then that iterator is of int type.

C / C++

Fortran

In an iterator specifier, if the iterator-type is not specified then that iterator has default integer type. Fortran Fortran

In a range-specification, if the step is not specified its value is implicitly defined to be 1.

An iterator only exists in the context of the clause argument that its iterator modifier modifies. An iterator also hides all accessible symbols with the same name in the context of that clause argument.

The use of a variable in an expression that appears in the range-specification causes an implicit reference to the variable in all enclosing constructs.

The iterator value set of the iterator are the set of values $i _ { 0 } , . . . , i _ { N - 1 }$ where:

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
- $i_0 = (\text{iterator-type})$ begin;
- $i_j = (\text{iterator-type}) (i_{j-1} + step)$, where $j \geq 1$; and
- if step &gt; 0,
    - $i_0 &lt; (\text{iterator-type})$ end;
    - $i_{N-1} &lt; (\text{iterator-type})$ end; and
    - $(\text{iterator-type}) (i_{N-1} + step) \geq (\text{iterator-type})$ end;
- if step &lt; 0,
    - $i_0 &gt; (\text{iterator-type})$ end;
    - $i_{N-1} &gt; (\text{iterator-type})$ end; and
    - $(\text{iterator-type}) (i_{N-1} + step) \leq (\text{iterator-type})$ end.
</div>

The iterator value set of the iterator are the set of values $i _ { 1 } , . . . , i _ { N }$ where:

$i _ { 1 } = b e g i n ;$

$i _ { j } = i _ { j - 1 } + s t e p , \mathrm { w h e r e \ } j \ge 2 ;$ and

• if step > 0,

• if step < 0,

## Fortran

The iterator value set will be empty if no possible value complies with the conditions above.

If an iterator-identifier appears in a list item expression of the modified argument, the efect is as if the list item is instantiated within the clause for each member of the iterator value set, substituting each occurrence of iterator-identifier in the list item expression with the member of the iterator value set. If the iterator value set is empty then the efect is as if the list item was not specified.

## Restrictions

Restrictions to iterator modifiers are as follows:

• The iterator-type must not declare a new type.

• For each value i in an iterator value set, the mathematical result of i + step must be representable in iterator-type.

C / C++

• The iterator-type must be an integral or pointer type.

• The iterator-type must not be const qualified.

C / C++

Fortran

• The iterator-type must be an integer type.

Fortran

• If the step expression of a range-specification equals zero, the behavior is unspecified.

• Each iterator-identifier can only be defined once in the modifier-parameter-specification.

• An iterator-identifier must not appear in the range-specification.

• If an iterator modifier appears in a clause that is specified on a task\_iteration directive then the loop-iteration variables of taskloop-afected loops of the associated taskloop construct must not appear in the range-specification.

## Cross References

• affinity Clause, see Section 14.10

• depend Clause, see Section 17.9.5

• from Clause, see Section 7.10.2

• map Clause, see Section 7.9.6

• to Clause, see Section 7.10.1

## 5.3 Conditional Compilation
````
