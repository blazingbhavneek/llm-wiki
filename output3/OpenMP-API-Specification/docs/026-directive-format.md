
This section defines several categories of directives and constructs. Directives are specified with a directive specification. A directive specification consists of the directive specifier and any clauses that may optionally be associated with the directive, Thus, the directive-specifation is:

directive-specifier [[,] clause[ [,] clause] ... ]

where the directive-specifier is:

directive-name

or for argument-modified directives:

directive-name[(directive-arguments)]

where directive-name is the directive name of the directive.

Some directives specify a paired end directive. If the directive-name of such a directive starts with begin, the end directive has the same directive name except begin is replaced with end. If the directive-name does not start with begin, unless otherwise specified the directive name of the end directive is end directive-name.

Some directives have underscores in their directive-name. Some of those directives are explicitly specified alternatively to allow the underscores in their directive-name to be replaced with white space. In addition, if a directive-name starts with either begin or end then it is separated from the rest of the directive-name by white space.

The directive-specification of a paired end directive may include one or more optional end-clause:

directive-specifier [[,] end-clause[ [,] end-clause]...]

where end-clause has the end-clause property, which explicitly allows it on a paired end directive.

C / C++

A directive may be specified as a pragma directive:

#pragma omp directive-specification new-line

or a pragma operator:

\_Pragma("omp directive-specification")

Note – In this directive, directive-name is depobj, directive-arguments is o. directive-specifier is depobj(o) and directive-specification is depobj(o) depend(inout: d).

#pragma omp depobj(o) depend(inout: d)

White space can be used before and after the #. Preprocessing tokens in a directive-specification of #pragma and \_Pragma pragmas are subject to macro expansion.

In C23 and later versions or C++11 and later versions, a directive may be specified as a C/C++ attribute specifier:

```jsonl
[[ omp :: directive-attr ]]
```

C++

or

[[ using omp : directive-attr ]]

C++

where directive-attr is

```txt
directive( directive-specification )
```

sequence( [omp::]directive-attr [[, [omp::]directive-attr] ... ] )

Multiple attributes on the same statement are allowed. Attribute directives that apply to the same statement are unordered unless the sequence attribute is specified, in which case the right-to-left ordering applies. The omp:: namespace qualifier within a sequence attribute is optional. The application of multiple attributes in a sequence attribute is ordered as if each directive had been specified as a pragma directive on subsequent lines. The directive attribute must not be specified inside a sequence attribute unless it specifies a block-associated directive.

Note – This example shows the expected transformation:

```txt
[[ omp::sequence(directive(parallel), directive(for)) ]]
for(...) {}
// becomes
#pragma omp parallel
#pragma omp for
for(...) {}
```

The pragma and attribute forms are interchangeable for any directive. Some directives may be composed of consecutive attribute specifiers if specified in their syntax. Any two consecutive attribute specifiers may be reordered or expressed as a single attribute specifier, as permitted by the base language, without changing the behavior of the directive.

Directives are case-sensitive. Each expression used in the OpenMP syntax inside of a clause must be a valid assignment-expression of the base language unless otherwise specified.

C / C++

C++

Directives may not appear in constexpr functions or in constant expressions.

C++

## Fortran

A directive for Fortran is specified with a stylized comment as follows:

sentinel directive-specification

All directives must begin with a directive sentinel. The format of a sentinel difers between fixed form and free form source files, as described in Section 5.1.1 and Section 5.1.2. In order to simplify the presentation, free form is used for the syntax of directives for Fortran throughout this document, except as noted.

Directives are case insensitive. Directives cannot be embedded within continued statements, and statements cannot be embedded within directives. Each expression used in the OpenMP syntax inside of a clause must be a valid expression of the base language unless otherwise specified.

Fortran

A directive may be categorized as one of the following:

• declarative directive;

• executable directive;

• informational directive;

• metadirective;

• subsidiary directive; or

• utility directive.

Base language code can be associated with directives. A directive may be categorized by its base language code association as one of the following:

• block-associated directive;

• declaration-associated directive;

• delimited directive;

• explicitly associated directive;

• loop-nest-associated directive;

• loop-sequence-associated directive;

• separating directive; or

• unassociated directive.

A directive and its associated base language code (if any) constitute a syntactic formation that follows the syntax given below unless otherwise specified. The end-directive in a specified formation refers to the paired end directive for the directive. A construct is a formation for an executable directive. An end directive is considered a subsidiary directive of a construct if it is the end directive of that construct.

Unassociated directives are not directly associated with any base language code. The resulting formation therefore has the following syntax:

## directive

Unassociated directives that are declarative directives declare identifiers for use in other directives. Unassociated directives that are executable directives are stand-alone directives.

Explicitly associated directives are declarative directives that take a variable or extended list as a directive or clause argument that indicates the declarations with which the directive is associated. As a result, explicitly associated directives have the same syntax as the formation for unassociated directives.

Formations that result from a block-associated directive have the following syntax:

directive

C / C++

structured-block

C / C++

Fortran

directive

structured-block

[end-directive]

If structured-block is a loosely structured block, end-directive is required, unless otherwise specified. If structured-block is a strictly structured block, end-directive is optional. An end-directive that immediately follows a directive and its associated strictly structured block is always paired with that directive.

Fortran

Loop-nest-associated directives are block-associated directives for which the associated structured-block is loop-nest, a canonical loop nest. Loop-sequence-associated directives are block-associated directives for which the associated structured-block is canonical-loop-sequence, a canonical loop sequence.

Fortran

The associated structured block of a block-associated directive can be a DO CONCURRENT loop where it is explicitly allowed.

For a loop-nest-associated directive, the paired end directive is optional.

Fortran

A declaration-associated directive is directly associated with a base language declaration.

C / C++

Formations that result from a declaration-associated directive have the following syntax:

declaration-associated-specification

where declaration-associated-specification is either:

directive function-definition-or-declaration

or:

directive declaration-associated-specification

In all cases the directive is associated with the function-definition-or-declaration.

C / C++

Fortran

The formation that results from a declaration-associated directive in Fortran has the same syntax as the formation for an unassociated directive as the associated declaration is determined directly from the specification part in which the directive appears.

Fortran

Fortran / C++

If a directive appears in the specification part of a module then the behavior is as if that directive, with the variables, types and procedures that have PRIVATE accessibility omitted, appears in the specification part of any compilation unit that references the module unless otherwise specified.

Fortran / C++

The formation that results from a delimited directive has the following syntax:

directive

base-language-code

end-directive

Separating directives are used to split statements contained in the associated structured block of a block-associated directive (the separated construct) into multiple structured block sequences. If the separated construct is a loop-nest-associated construct then any separating directives divide the loop body of the innermost afected loop into structured block sequences. Otherwise, the separating directives divide the associated structured block into structured block sequences.

Separating directives and the containing structured block have the following syntax:

structured-block-sequence

directive

structured-block-sequence

[directive

structured-block-sequence ...]

wrapped in a single compound statement for C/C++ or optionally wrapped in a single BLOCK construct for Fortran.

Formations that result from directives that are specified as attribute specifiers that use the directive attribute are specified as follows. If the directive is an unassociated directive, the resulting formation is an attribute-declaration if the directive is not executable and it consists of the attribute specifier and a null statement (i.e., “;”) if the directive is an executable directive. For a block-associated directive, the resulting formation consists of the attribute specifier and a structured block to which the specifier applies. If the directives are separating directives or delimited directives then the resulting formation is as specified above for those associations except that the attribute specifier for each directive, including the end directive, applies to a null statement.

A declarative directive that is a declaration-associated directive may alternatively be expressed as an attribute specifier:

[[ omp :: decl( directive-specification ) ]]

C++

or

[[ using omp : decl( directive-specification ) ]]

C++

An explicitly associated directive may alternatively be expressed with an attribute specifier that also uses the decl attribute, applies to a variable and/or function declaration, and omits the variable list or extended list argument. The efect is as if the omitted list argument is the list of declared variables and/or functions to which the attribute specifier applies.

Formations that result from directives that are specified as attribute specifiers and are declaration-associated directives or use the decl attribute are specified as follows. If the directives are declaration-associated directives then the resulting formation consists of the attribute specifiers and the function-definition-or-declaration to which the specifiers apply. If the directive uses the decl attribute then the resulting formation consists of the attribute specifier and the variable and/or function declarations to which the specifier applies.

C / C++

Restrictions

Restrictions to directive format are as follows:

C / C++

• A directive-name must not include white space except where explicitly allowed.

C / C++

• Orphaned separating directives are prohibited. That is, the separating directives must appear within the structured block associated with the same construct with which it is associated and must not be encountered elsewhere in the region of that separated construct.

• A stand-alone directive may be placed only at a point where a base language executable statement is allowed.

Fortran

• A declarative directive must be specified in the specification part after all USE, IMPORT and IMPLICIT statements.

Fortran

C / C++

• A directive that uses the attribute syntax cannot be applied to the same statement or associated declaration as a directive that uses the pragma syntax.

• For any directive that has a paired end directive, both directives must use either the attribute syntax or the pragma syntax.

• The directive and subsidiary directives of a construct must all use the attribute syntax or must all use the pragma syntax.

• Neither a stand-alone directive nor a declarative directive may be used in place of a substatement in a selection statement or iteration statement, or in place of the statement that follows a label.

• If a declarative directive applies to a function declaration or definition and it is specified with one or more C or C++ attribute specifiers, the specified attributes must be applied to the function as permitted by the base language.

C / C++

Fortran
