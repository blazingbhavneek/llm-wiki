## 9 Variant Directives

This chapter defines directives and related concepts to support the seamless adaption of OpenMP programs to OpenMP contexts.

## 9.1 OpenMP Contexts

At any point in an OpenMP program, an OpenMP context exists that defines traits that describe the active constructs, the execution devices, functionality supported by the implementation and available dynamic values. The traits are grouped into trait sets. The defined trait sets are: the construct trait set; the device trait set; the target device trait set; the implementation trait set; and the dynamic trait set. Traits are categorized as name-list traits, clause-list traits, non-property traits and extension traits. This categorization determines the syntax that is used to match the trait, as defined in Section 9.2.

The construct trait set is composed of the directive names, each being a trait, of all enclosing constructs at that point in the OpenMP program up to a target construct. Compound constructs are added to the set as their leaf constructs in the same nesting order specified by the original constructs. The dispatch construct is added to the construct trait set only for the target-call of the associated function-dispatch structured block. The construct trait set is ordered by nesting level in ascending order. Specifically, the ordering of the set of constructs is $c _ { 1 } , \ldots , c _ { N }$ , where $c _ { 1 }$ is the construct at the outermost nesting level and $c _ { N }$ is the construct at the innermost nesting level. In addition, if the point in the OpenMP program is not enclosed by a target construct, the following rules are applied in order:

1. For procedures with a declare\_simd directive, the simd trait is added to the beginning of the construct trait set as $c _ { 1 }$ for any generated SIMD versions so the total size of the trait set is increased by one.

2. For procedures that are determined to be function variants by a declare variant directive, the trait selectors $c _ { 1 } , \ldots , c _ { M }$ of the construct selector set are added in the same order to the beginning of the construct trait set as $c _ { 1 } , . . . , c _ { M }$ so the total size of the trait set is increased by M.

3. For procedures that are determined to be target variants by a declare target directive, the target trait is added to the beginning of the construct trait set as $c _ { 1 }$ so the total size of the trait set is increased by one.

The simd trait is a clause-list trait that is defined with properties that match the clauses that can be specified on the declare\_simd directive with the same names and semantics. The simd trait

defines at least the simdlen property and one of the inbranch or notinbranch properties. Traits in the construct trait set other than simd are non-property traits.

The device trait set includes traits that define the characteristics of the device that the compiler determines will be the current device during program execution at a given point in the OpenMP program. A trait in the device trait set is considered to be active at program points that fall outside a defined procedure if it defines a characteristic of some available device, including the host device. For each target device that the implementation supports, a target device trait set exists that defines the characteristics of that device. At least the following traits must be defined for the device trait set and all target device trait sets:

• The kind(kind-list) name-list trait specifies the general kind of the device. Each member of kind-list is a kind-name, for which the following values are defined:

– host, which specifies that the device is the host device;

– nohost, which specifies that the device is not the host device; and

– the values defined in the OpenMP Additional Definitions document.

• The isa(isa-list) name-list trait specifies the Instruction Set Architectures supported by the device. Each member of isa-list is an isa-name, for which the accepted values are implementation defined.

• The arch(arch-list) name-list trait specifies the architectures supported by the device. Each member of arch-list is an arch-name, for which the accepted values are implementation defined.

The target device trait set also defines the following traits:

• The device\_num trait specifies the device number of the device.

• The uid trait specifies a unique identifier string of the device, for which the accepted values are implementation defined.

The implementation trait set includes traits that describe the functionality supported by the OpenMP implementation at that point in the OpenMP program. At least the following traits can be defined:

• The vendor(vendor-list) name-list trait, which specifies the vendor identifiers of the implementation. Each member of vendor-list is a vendor-name, for which the defined values are in the OpenMP Additional Definitions document.

• The extension(extension-list) name-list trait, which specifies vendor-specific extensions to the OpenMP specification. Each member of extension-list is an extension-name, for which the accepted values are implementation defined.

• A requires(requires-list) clause-list trait, for which the properties are the clauses that have been supplied to the requires directive prior to the program point as well as implementation defined implicit requirements.

Implementations can define additional traits in the device trait set, target device trait set and implementation trait set; these traits are extension traits.

The dynamic trait set includes traits that define the dynamic properties of an OpenMP program at a point in its execution. The data state trait in the dynamic trait set refers to the complete data state of the OpenMP program that may be accessed at runtime.

## 9.2 Context Selectors

Context selectors are used to define the properties that can match an OpenMP context. OpenMP defines diferent trait selector sets, each of which contains diferent trait selectors.

The syntax for a context selector is context-selector-specification as described in the following grammar:

```txt
context-selector-specification:
    trait-set-selector[, trait-set-selector[, ...]]

trait-set-selector:
    trait-set-selector-name={trait-selector[, trait-selector[, ...]]}

trait-selector:
    trait-selector-name[ ([trait-score: ] trait-property[, trait-property[, ...]])]

trait-property:
    trait-property-name
    trait-property-clause
    trait-property-expression
    trait-property-extension

trait-property-clause:
    clause

trait-property-name:
    identifier
    string-literal

trait-property-expression
    scalar-expression (for C/C++)
    scalar-logical-expression (for Fortran)
    scalar-integer-expression (for Fortran)

trait-score:
    score(score-expression)

trait-property-extension:
    trait-property-name
```

identifier(trait-property-extension[, trait-property-extension[, ...]]) constant integer expression

For trait selectors that correspond to name-list traits, each trait-property should be trait-property-name and, for any value that is a valid identifier, both the identifier and the corresponding string literal (for C/C++) and the corresponding char-literal-constant (for Fortran) representation are considered representations of the same value.

For trait selectors that correspond to clause-list traits, each trait-property should be trait-property-clause. The syntax is the same as for the matching clause.

The construct selector set defines the traits in the construct trait set that should be active in the OpenMP context. Each trait selector that can be defined in the construct selector set is the directive-name of a context-matching construct. Each trait-property of the simd trait selector is a trait-property-clause. The syntax is the same as for a valid clause of the declare\_simd directive and the restrictions on the clauses from that directive apply. The construct selector set is an ordered list c<sub>1</sub>, . . . , c<sub>N</sub> .

The device selector set and implementation selector set define the traits that should be active in the corresponding trait set of the OpenMP context. The target\_device selector set defines the traits that should be active in the target device trait set for the device that the specified device\_num trait selector identifies. The same traits that are defined in the corresponding trait sets can be used as trait selectors with the same properties. The kind trait selector of the device selector set and target\_device selector set can also specify the value any, which is as if no kind trait selector was specified. If a device\_num trait selector does not appear in the target\_device selector set then a device\_num trait selector that specifies the value of the default-device-var ICV is implied. For the device\_num trait selector of the target\_device selector set, a single trait-property-expression must be specified. The device\_num trait selector can be true only if that trait-property-expression evaluates to a conforming device number other than omp\_invalid\_device. For the atomic\_default\_mem\_order trait selector of the implementation selector set, a single trait-property must be specified as an identifier equal to one of the valid arguments to the atomic\_default\_mem\_order clause on the requires directive. For the requires trait selector of the implementation selector set, each trait-property is a trait-property-clause. The syntax is the same as for a valid clause of the requires directive and the restrictions on the clauses from that directive apply.

The user selector set defines the condition trait selector that provides additional user-defined conditions. The condition trait selector contains a single trait-property-expression that must evaluate to true for the trait selector to be true. Any non-constant trait-property-expression that is evaluated to determine the suitability of a variant is evaluated according to the data state trait in the dynamic trait set of the OpenMP context. The user selector set is dynamic if the condition trait selector is present and the expression in the condition trait selector is not a constant expression; otherwise, it is static.

All parts of a context selector define the static part of the context selector except the following parts, which define the dynamic part of the context selector:

• Its user selector set if it is dynamic; and

• Its target\_device selector set.

For the match clause of a declare\_variant directive, any argument of the base function that is referenced in an expression that appears in the context selector is treated as a reference to the expression that is passed into that argument at the call to the base function. Otherwise, a variable or procedure reference in an expression that appears in a context selector is a reference to the variable or procedure of that name that is visible at the location of the directive on which the context selector appears.

Each occurrence of the this pointer in an expression in a context selector that appears in the match clause of a declare\_variant directive is treated as an expression that is the address of the object on which the associated base function is invoked.

![](images/3e84a8c2c99433999a2aa486f1ee8db161e699bac0bb574d7e3f76830ac4da94.jpg)

Implementations can allow further trait selectors to be specified. Each specified trait-property for these implementation defined trait selectors should be a trait-property-extension. Implementations can ignore specified trait selectors that are not those described in this section.

## Restrictions

Restrictions to context selectors are as follows:

• Each trait-property may only be specified once in a trait selector other than those in the construct selector set.

• Each trait-set-selector-name may only be specified once in a context selector.

• Each trait-selector-name may only be specified once in a trait selector set.

• A trait-score cannot be specified in traits from the construct selector set, the device selector set or the target\_device selector sets.

• A score-expression must be a non-negative constant integer expression.

• The expression of a device\_num trait must evaluate to a conforming device number.

• A variable or procedure that is referenced in an expression that appears in a context selector must be visible at the location of the directive on which the context selector appears unless the directive is a declare\_variant directive and the variable is an argument of the associated base function.

• If trait-property any is specified in the kind trait-selector of the device selector set or the target\_device selector sets, no other trait-property may be specified in the same selector set.

• For a trait-selector that corresponds to a name-list trait, at least one trait-property must be specified.

• For a trait-selector that corresponds to a non-property trait, no trait-property may be specified.

• For the requires trait selector of the implementation selector set, at least one trait-property must be specified.

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
