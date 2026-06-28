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
