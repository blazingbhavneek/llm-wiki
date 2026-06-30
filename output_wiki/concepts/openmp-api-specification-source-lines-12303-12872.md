# OpenMP-API-Specification Source Lines 12303-12872

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source OpenMP-API-Specification:L12303-L12872

Citation: [OpenMP-API-Specification:L12303-L12872]

````text
## 9.3 Matching and Scoring Context Selectors

A compatible context selector for an OpenMP context satisfies the following conditions:

• All trait selectors in its user selector set are true;

• All traits and trait properties that are defined by trait selectors in the target\_device selector set are active in the target device trait set for the device that is identified by the device\_num trait selector;

• All traits and trait properties that are defined by trait selectors in its construct selector set, its device selector set and its implementation selector set are active in the corresponding trait sets of the OpenMP context;

• For each trait selector in the context selector, its properties are a subset of the properties of the corresponding trait of the OpenMP context; and

• Trait selectors in its construct selector set appear in the same relative order as their corresponding traits in the construct trait set of the OpenMP context;

Some properties of the simd trait selector have special rules to match the properties of the simd trait:

• The simdlen( N) property of the trait selector matches the simdlen(M) trait of the OpenMP context if M is a multiple of N; and

• The aligned( list:N) property of the trait selector matches the aligned(list:M) trait of the OpenMP context if N is a multiple of M.

Among compatible context selectors, a score is computed using the following algorithm:

1. Each trait selector for which the corresponding trait appears in the construct trait set in the OpenMP context is given the value $2 ^ { p - 1 }$ where $p$ is the position of the corresponding trait, $c _ { p } ,$ , in the construct trait set; if the traits that correspond to the construct selector set appear multiple times in the OpenMP context, the highest valued subset of context traits that contains all trait selectors in the same order are used;

2. The kind, arch, and isa trait selectors, if specified, are given the values $2 ^ { l } , 2 ^ { l + 1 }$ and $2 ^ { l + 2 }$ respectively, where l is the number of traits in the construct trait set;

3. Trait selectors for which a trait-score is specified are given the value specified by the trait-score score-expression;

4. The values given to any additional trait selectors allowed by the implementation are implementation defined;

5. Other trait selectors are given a value of zero; and

6. A context selector that is a strict subset of another compatible context selector has a score of zero. For other context selectors, the final score is the sum of the values of all specified trait selectors plus 1.

## 9.4 Metadirectives

A metadirective is a directive that can specify multiple directive variants of which one may be conditionally selected to replace the metadirective based on the enclosing context. A metadirective is replaced by a nothing directive or one of the directive variants specified by the when clauses or the otherwise clause. If no otherwise clause is specified the efect is as if one was specified without an associated directive variant.

The OpenMP context for a given metadirective is defined according to Section 9.1. The order of clauses that appear on a metadirective is significant and, if specified, otherwise must be the last clause specified on a metadirective.

Replacement candidates for a metadirective are ordered according to the following rules in decreasing precedence:

• A candidate is before another one if the score associated with the context selector of the corresponding when clause is higher.

• A candidate that was explicitly specified is before one that was implicitly specified.

• Candidates are ordered according to the order in which they lexically appear on the metadirective.

The list of dynamic replacement candidates is the prefix of the sorted list of replacement candidates up to and including the first candidate for which the corresponding when or otherwise clause has a static context selector. The first dynamic replacement candidate for which the corresponding when or otherwise clause has a compatible context selector, according to the matching rules defined in Section 9.3, replaces the metadirective.

## Restrictions

Restrictions to metadirectives are as follows:

• Replacement of the metadirective with the directive variant associated with any of the dynamic replacement candidates must result in a conforming program.

• Insertion of user code at the location of a metadirective must be allowed if the first dynamic replacement candidate does not have a static context selector.

• If the list of dynamic replacement candidates has multiple items then all items must be executable directives.

## Fortran

• A metadirective that appears in the specification part of a subprogram must follow all variant-generating directives that appear in the same specification part.

• A metadirective is pure if and only if all directive variants specified for it are pure.

Fortran

## 9.4.1 when Clause

<table><tr><td>Name: when</td><td>Properties: default</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>directive-variant</td><td>directive-specification</td><td>optional, unique</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>context-selector</td><td>directive-variant</td><td>An OpenMP context-selector-specification</td><td>required, unique</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

begin metadirective, metadirective

## Semantics

The specified directive-variant is a replacement candidate for the metadirective on which the clause is specified if the static part of the context selector specified by context-selector is compatible with the OpenMP context according to the matching rules defined in Section 9.3. If a when clause does not explicitly specify a directive variant, it implicitly specifies a nothing directive as the directive variant.

Expressions that appear in the context selector of a when clause are evaluated if no prior dynamic replacement candidate has a compatible context selector, and the number of times each expression is evaluated is implementation defined. All variables referenced by these expressions are considered to be referenced by the metadirective.

A directive variant that is associated with a when clause can only afect the OpenMP program if the directive variant is a dynamic replacement candidate.

## Restrictions

Restrictions to the when clause are as follows:

• directive-variant must not specify a metadirective.

• context-selector must not specify any properties for the simd trait selector.

C / C++

• directive-variant must not specify a begin declare\_variant directive.

C / C++

## Cross References

• begin metadirective, see Section 9.4.4

• Context Selectors, see Section 9.2

• metadirective, see Section 9.4.3

• nothing Directive, see Section 10.7

## 9.4.2 otherwise Clause

<table><tr><td>Name: otherwise</td><td>Properties: unique, ultimate</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>directive-variant</td><td>directive-specification</td><td>optional, unique</td></tr></table>

## Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

begin metadirective, metadirective

## Semantics

The otherwise clause is treated as a when clause with the specified directive variant, if any, and a static context selector that is always compatible and has a score lower than the scores associated with any other directive variant.

## Restrictions

Restrictions to the otherwise clause are as follows:

• directive-variant must not specify a metadirective.

C / C++

• directive-variant must not specify a begin declare\_variant directive.

C / C++

## Cross References

• begin metadirective, see Section 9.4.4

• metadirective, see Section 9.4.3

• when Clause, see Section 9.4.1

9.4.3 metadirective

<table><tr><td>Name: metadirectiveCategory: meta</td><td>Association: unassociatedProperties: pure</td></tr></table>

## Clauses

otherwise, when

## Semantics

The metadirective specifies metadirective semantics.

## Cross References

• Metadirectives, see Section 9.4

• otherwise Clause, see Section 9.4.2

• when Clause, see Section 9.4.1

## 9.4.4 begin metadirective

<table><tr><td>Name: begin metadirectiveCategory: meta</td><td>Association: delimitedProperties: pure</td></tr></table>

## Clauses

otherwise, when

## Semantics

The begin metadirective is a metadirective that is a delimited directive and for which the specified directive variants other than the nothing directive must accept a paired end directive. For any directive variant that is selected to replace the begin metadirective directive, the required paired end directive is implicitly replaced by the end directive of the directive variant to demarcate the statements that are associated with the directive variant. If the nothing directive is selected to replace the begin metadirective directive, the end directive is ignored.

## Restrictions

The restrictions to begin metadirective are as follows:

• Any directive-variant that is specified by a when or otherwise clause must be a directive that has a paired end directive or must be the nothing directive.

## Cross References

• Metadirectives, see Section 9.4

• nothing Directive, see Section 10.7

• otherwise Clause, see Section 9.4.2

• when Clause, see Section 9.4.1

## 9.5 Semantic Requirement Set

The semantic requirement set of each task is a logical set of elements that can be added to or removed from the set by diferent directives in the scope of the task region, as well as afect the semantics of those directives.

A directive can add the following elements to the set:

• depend, which specifies that a construct requires enforcement of the synchronization relationship expressed by the depend clause;

• nowait, which specifies that a construct is asynchronous;

• is\_device\_ptr(list-item), which specifies that the list-item is a device pointer in a construct;

• has\_device\_addr(list-item), which specifies that the list-item has a device address in a construct; and

• interop(list-item), which specifies that the list-item is a user-provided interoperability object to be used in a construct. The order in which the interop elements are added is relevant.

If an implementation supports the unified\_address requirement then:

• Adding an is\_device\_ptr element for a list item also adds a has\_device\_addr element for any data entity for which the list item is a base pointer; and

• Adding a has\_device\_addr element for a list item that has a base pointer also adds an is\_device\_ptr element for that base pointer if the base pointer is an identifier.

The following directives may add elements to the set:

• dispatch.

The following directives may remove elements from the set:

• declare\_variant

## Cross References

• dispatch Construct, see Section 9.7

• Declare Variant Directives, see Section 9.6

## 9.6 Declare Variant Directives

Declare variant directives declare base functions to have the specified function variant. The context selector specified by context-selector in the match clause is associated with the function variant. The OpenMP context for a direct call to a given base function is defined according to Section 9.1.

For a function variant to be a replacement candidate to be called instead of the base function, its declare variant directive for the base function must be visible at the call site and the static part of its associated context selector must be compatible with the OpenMP context of the call according to the matching rules defined in Section 9.3. In addition, if the base function is called from a non-host device, the declare variant directive must not specify an append\_args clause or an adjust\_args clause with a need\_device\_ptr or need\_device\_addr adjust-op.

Replacement candidates are ordered in decreasing order of the score associated with the context selector. If two replacement candidates have the same score then their order is implementation defined.

The list of dynamic replacement candidates is the prefix of the sorted list of replacement candidates up to and including the first candidate for which the corresponding match clause has a static context selector.

The first dynamic replacement candidate for which the corresponding match clause has a compatible context selector is called instead of the base function. If no compatible candidate exists then the base function is called.

Expressions that appear in the context selector of a match clause are evaluated if no prior dynamic replacement candidate has a compatible context selector, and the number of times each expression is evaluated is implementation defined. All variables referenced by these expressions are considered to be referenced at the call site.

![](images/5e686eab27640b191dc468499e552a7476d750e16fc92847e1a586b58375c94e.jpg)

For calls to constexpr base functions that are evaluated in constant expressions, whether variant substitution occurs is implementation defined.

![](images/22b2f633891d63e0bcfa1267ce519b5ec84ebddd21462d41c48e2c673b076c0f.jpg)

For indirect function calls that can be determined to call a particular base function, whether variant substitution occurs is unspecified.

Any diferences that the specific OpenMP context requires in the prototype of the function variant from the base function prototype are implementation defined.

Diferent declare variant directives may be specified for diferent declarations of the same base function.

## Restrictions

Restrictions to declare variant directives are as follows:

• Calling procedures that a declare variant directive determined to be a function variant directly in an OpenMP context that is diferent from the one that the construct selector set of the context selector specifies is non-conforming.

• If a procedure is determined to be a function variant through more than one declare variant directive then the construct selector set of their context selectors must be the same.

• A procedure determined to be a function variant may not be specified as a base function in another declare variant directive.

• An adjust\_args clause or append\_args clause may only be specified if the dispatch trait selector of the construct selector set appears in the match clause.

C / C++

• The type of the function variant must be compatible with the type of the base function after the implementation defined transformation for its OpenMP context.

C / C++

C++

• Declare variant directives may not be specified for virtual, defaulted or deleted functions.

• Declare variant directives may not be specified for constructors or destructors.

• Declare variant directives may not be specified for immediate functions.

• The procedure that a declare variant directive determined to be a function variant may not be an immediate function.

C++

Fortran

• The characteristic of the function variant must be compatible with the characteristic of the base function after the implementation defined transformation for its OpenMP context.

Fortran

## Cross References

• Context Selectors, see Section 9.2

• OpenMP Contexts, see Section 9.1

## 9.6.1 match Clause

<table><tr><td>Name: match</td><td>Properties: unique, required</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>context-selector</td><td>An OpenMP context-selector-specification</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

begin declare\_variant, declare\_variant

## Semantics

The context-selector argument of the match clause specifies the context selector to use to determine if a specified function variant is a replacement candidate for the specified base function in a given OpenMP context.

## Restrictions

Restrictions to the match clause are as follows:

• All variables that are referenced in an expression that appears in the context selector of a match clause must be accessible at each call site to the base function according to the base language rules.

## Cross References

• begin declare\_variant Directive, see Section 9.6.5

• declare\_variant Directive, see Section 9.6.4

• Context Selectors, see Section 9.2

## 9.6.2 adjust\_args Clause

<table><tr><td>Name: adjust_args</td><td>Properties: default</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>parameter-list</td><td>list of parameter list item type</td><td>default</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>adjust-op</td><td>parameter-list</td><td>Keyword: need_device_addr, need_device_ptr, nothing</td><td>required</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

declare\_variant

## Semantics

The adjust\_args clause specifies how to adjust the arguments of the base function when a specified function variant is selected for replacement in the context of a function-dispatch structured block. For each adjust\_args clause that is present on the selected function variant, the adjustment operation specified by the adjust-op modifier is applied to each argument specified in the clause before being passed to the selected function variant. Any argument specified in the clause that does not exist at a given function call site is ignored.

If the adjust-op modifier is nothing, the argument is passed to the selected function variant without being modified.

If the adjust-op modifier is need\_device\_ptr, the arguments are converted to corresponding device pointers of the default device if they are not already device pointers. If the current task has the is\_device\_ptr element for a given argument in its semantic requirement set (as added by the dispatch construct that encloses the call to the base function), the argument is not adjusted. Otherwise, the argument is converted in the same manner that a use\_device\_ptr clause on a target\_data construct converts its pointer list items into device pointers, except that if the argument cannot be converted into a device pointer then NULL is passed as the argument.

If the adjust-op modifier is need\_device\_addr, the arguments are replaced with references to the corresponding objects in the device data environment of the default device if they do not already have device addresses. If the current task has a has\_device\_addr element for a given argument in its semantic requirement set, as added by the dispatch construct that encloses the call to the base function, the argument is not adjusted. Otherwise, the argument is converted in the same manner that a use\_device\_addr clause on a target\_data construct replaces references to the list items.

## Restrictions

• If the need\_device\_addr adjust-op modifier is present and the has-device-addr element does not exist for a specified argument in the semantic requirement set of the current task, all restrictions that apply to a list item in a use\_device\_addr clause also apply to the corresponding argument that is passed by the call.

• If the need\_device\_ptr adjust-op modifier is present, each list item that appears in the clause that refers to a specific named argument in the declaration of the function variant must be of pointer type.

• The need\_device\_addr adjust-op modifier must not be specified in the clause.

C C++

• If the need\_device\_ptr adjust-op modifier is present, each list item that appears in the clause that refers to a specific named argument in the declaration of the function variant must be of pointer type or reference to pointer type.

• If the need\_device\_addr adjust-op modifier is present, each list item that appears in the clause must refer to an argument in the declaration of the function variant that has a reference type.

## Fortran

• If the need\_device\_ptr adjust-op modifier is present, each list item that appears in the clause must refer to a dummy argument of C\_PTR type in the declaration of the function variant.

• If the need\_device\_addr adjust-op modifier is present, each list item that appears in the clause must refer to a dummy argument in the declaration of the function variant that does not have the VALUE attribute.

• If the need\_device\_addr adjust-op modifier is present, the corresponding actual argument for each specified argument must be contiguous.

Fortran

## Cross References

• declare\_variant Directive, see Section 9.6.4

• use\_device\_addr Clause, see Section 7.5.10

• use\_device\_ptr Clause, see Section 7.5.8

## 9.6.3 append\_args Clause

<table><tr><td>Name: append_args</td><td>Properties: unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>append-op-list</td><td>list of OpenMP operation list item type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

declare\_variant

## Semantics

The append\_args clause specifies additional arguments to pass in the call when a specified function variant is selected for replacement in the context of a function-dispatch structured block. The arguments are formed according to each specified list item in append-op-list, in the order those list items appear. The arguments are passed to the function variant after any named arguments of the base function in the same order in which they are formed. If the base function is variadic, the formed arguments are passed before any variadic arguments.

The supported OpenMP operations in append-op-list are:

## interop

The interop operation accepts as its operator-parameter-specification any modifier-specification-list that is accepted by the init clause on the interop construct.

For each interop operation specified, an argument is formed and appended as follows. If the semantic requirement set contains one or more interop elements, the first of those elements that was added to the set is removed and the associated interoperability object of that removed element is appended as an argument. Otherwise, the interop operation constructs an argument of interop OpenMP type using the semantic requirement set of the encountering task. The argument is constructed as if by an interop construct with an init clause that specifies the modifier-specification-list specified in the interop operation. If the semantic requirement set contains one or more elements (as added by the dispatch construct) that correspond to clauses for an interop construct of interop-type, the behavior is as if the corresponding clauses are specified on the interop construct and those elements are removed from the semantic requirement set.

Any appended arguments that were not obtained from the interop elements of the semantic requirement set are destroyed after the call to the selected function variant returns, as if an interop construct with a destroy clause was used with the same clauses that were used to initialize the argument.

## Cross References

• declare\_variant Directive, see Section 9.6.4

• destroy Clause, see Section 5.7

• OpenMP Operations, see Section 5.2.3

• Semantic Requirement Set, see Section 9.5

• init Clause, see Section 5.6

• interop Construct, see Section 16.1

## 9.6.4 declare\_variant Directive

<table><tr><td>Name:declare_variantCategory:declarative</td><td>Association:declarationProperties:pure</td></tr></table>

## Arguments

declare\_variant([base–name:]variant-name)

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>base-name</td><td>identifier of function type</td><td>optional</td></tr><tr><td>variant-name</td><td>identifier of function type</td><td>default</td></tr></table>

## Clauses

adjust\_args, append\_args, match

## Additional information

The declare\_variant directive may alternatively be specified with declare variant as the directive-name.

## Semantics

The declare\_variant directive specifies declare variant semantics for a single replacement candidate; variant-name identifies the function variant while base-name identifies the base function.

C

Any expressions in the match clause are interpreted as if they appeared in the scope of arguments of the base function.

C

C++

variant-name and any expressions in the match clause are interpreted as if they appeared at the scope of the trailing return type of the base function.

The function variant is determined by base language standard name lookup rules ([basic.lookup]) of variant-name using the argument types at the call site after implementation defined changes have been made according to the OpenMP context.

C++

Fortran

The procedure to which base-name refers is resolved at the location of the directive according to the establishment rules for procedure names in the base language.

If a declare\_variant directive appears in the specification part of a subprogram or an interface body, its bound procedure is this subprogram or the procedure defined by the interface body, respectively. Otherwise there is no bound procedure.

Fortran

## Restrictions

The restrictions to the declare\_variant directive are as follows:

C / C++

• If base-name is specified, it must match the name used in the associated declaration, if any declaration is associated.

C / C++

C++

• If an expression in the context selector that appears in a match clause references the this pointer, the base function must be a non-static member function.

C++

## Fortran

• If the declare\_variant directive does not have a bound procedure or the base function is not the bound procedure, base-name must be specified.

• base-name must not be a generic name, an entry name, the name of a procedure pointer, a dummy procedure or a statement function.

• The procedure base-name must have an accessible explicit interface at the location of the directive.

Fortran

## Cross References

• adjust\_args Clause, see Section 9.6.2

• append\_args Clause, see Section 9.6.3

• Declare Variant Directives, see Section 9.6

• match Clause, see Section 9.6.1

C / C++

## 9.6.5 begin declare\_variant Directive

<table><tr><td>Name: begin declare_variantCategory: declarative</td><td>Association: delimitedProperties: default</td></tr></table>

## Clauses

match

## Additional information

The begin declare\_variant directive may alternatively be specified with begin declare variant as the directive-name.

## Semantics

The begin declare\_variant directive associates the context selector in the match clause with each function definition in the delimited code region formed by the directive and its paired end directive. The delimited code region is a declaration sequence. For the purpose of call resolution, each function definition that appears in the delimited code region is a function variant for an assumed base function, with the same name and a compatible prototype, that is declared elsewhere without an associated declare variant directive.

If a declare variant directive appears between a begin declare\_variant directive and its paired end directive, the efective context selectors of the outer directive are appended to the context selector of the inner directive to form the efective context selector of the inner directive. If a trait-set-selector is present on both directives, the trait-selector list of the outer directive is appended to the trait-selector list of the inner directive after equivalent trait-selectors have been

![](images/2bc834daba69330d88bd6604c62cda63c0788fbc1a79a17064c8ad969e604b56.jpg)

removed from the outer list. Restrictions that apply to explicitly specified context selectors also apply to efective context selectors constructed through this process.

The symbol name of a function definition that appears between a begin declare\_variant directive and its paired end directive is determined through the base language rules after the name of the function has been augmented with a string that is determined according to the efective context selector of the begin declare\_variant directive. The symbol names of two definitions of a function are considered to be equal if and only if their efective context selectors are equivalent.

If the context selector of a begin declare\_variant directive contains traits in the device or implementation set that are known never to be compatible with an OpenMP context during the current compilation, the preprocessed code that follows the begin declare\_variant directive up to its paired end directive is elided.

Any expressions in the match clause are interpreted at the location of the directive.

## Restrictions

The restrictions to begin declare\_variant directive are as follows:

• match clause must not contain a simd trait selector.

• Two begin declare\_variant directives and their paired end directives must either encompass disjoint source ranges or be perfectly nested.

• A match clause must not contain a dynamic context selector that references the this pointer.

## Cross References

• Declare Variant Directives, see Section 9.6

• match Clause, see Section 9.6.1

C / C++
````
