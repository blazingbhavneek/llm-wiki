
In implementations that support a preprocessor, the \_OPENMP macro name is defined to have the decimal value yyyymm where yyyy and mm are the year and month designations of the version of the OpenMP API that the implementation supports.

Fortran

The OpenMP API requires Fortran lines to be compiled conditionally, as described in the following sections.

Fortran

## Restrictions

Restrictions to conditional compilation are as follows:

• A #define or a #undef preprocessing directive in user code must not define or undefine the \_OPENMP macro name.

Fortran

## 5.3.1 Free Source Form Conditional Compilation Sentinel

The following conditional compilation sentinel is recognized in free form source files:

## !\$

To enable conditional compilation, a line with a conditional compilation sentinel must satisfy the following criteria:

• The sentinel can appear in any column but must be preceded only by white space;

• The sentinel must appear as a single word with no intervening white space;

• Initial lines must have a blank character after the sentinel; and

• Continued lines must have an ampersand as the last non-blank character on the line, prior to any comment appearing on the conditionally compiled line.

Continuation lines can have an ampersand after the sentinel, with optional white space before and after the ampersand. If these criteria are met, the sentinel is replaced by two spaces. If these criteria are not met, the line is left unchanged.

Note – In the following example, the two forms for specifying conditional compilation in free source form are equivalent (the first line represents the position of the first 9 columns):

```c
!23456789
!$ iam = omp_get_thread_num() +          &
!$&     index

#ifdef _OPENMP
    iam = omp_get_thread_num() +          &
    &     index
#endif
```

Fortran

## 5.3.2 Fixed Source Form Conditional Compilation Sentinels

The following conditional compilation sentinels are recognized in fixed form source files:

```txt
! \$ | * \$ | c \$
```

To enable conditional compilation, a line with a conditional compilation sentinel must satisfy the following criteria:

• The sentinel must start in column 1 and appear as a single word with no intervening white space;

• After the sentinel is replaced with two spaces, initial lines must have a space or zero in column 6 and only white space and numbers in columns 1 through 5; and

• After the sentinel is replaced with two spaces, continuation lines must have a character other than a space or zero in column 6 and only white space in columns 1 through 5.

If these criteria are met, the sentinel is replaced by two spaces. If these criteria are not met, the line is left unchanged.

Note – In the following example, the two forms for specifying conditional compilation in fixed source form are equivalent (the first line represents the position of the first 9 columns):

```c
c23456789
!\$ 10 iam = omp_get_thread_num() +
!\$    &        index

#ifdef _OPENMP
    10 iam = omp_get_thread_num() +
        &        index
#endif
```

Fortran

## 5.4 directive-name-modifier Modifier

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Clauses

absent, acq\_rel, acquire, adjust\_args, affinity, align, aligned, allocate, allocator, append\_args, apply, at, atomic\_default\_mem\_order, bind, capture, collapse, collector, combiner, compare, contains, copyin, copyprivate, default, defaultmap, depend, destroy, detach, device, device\_safesync, device\_type, dist\_schedule, doacross, dynamic\_allocators, enter, exclusive, fail, filter, final, firstprivate, from, full, grainsize, graph\_id, graph\_reset, has\_device\_addr, hint, holds, if, in\_reduction, inbranch, inclusive, indirect, induction, inductor, init, init\_complete, initializer, interop, is\_device\_ptr, lastprivate, linear, link, local, map, match, memscope, mergeable, message, no\_openmp, no\_openmp\_constructs, no\_openmp\_routines, no\_parallelism, nocontext, nogroup, nontemporal, notinbranch, novariants, nowait, num\_tasks, num\_teams, num\_threads, order, ordered, otherwise, partial, permutation, priority, private, proc\_bind, read, reduction, relaxed, release, replayable, reverse\_offload, safelen, safesync, schedule, self\_maps, seq\_cst, severity, shared, simd, simdlen, sizes, task\_reduction, thread\_limit, threads, threadset, to, transparent, unified\_address, unified\_shared\_memory, uniform, untied, update, update, use, use\_device\_addr, use\_device\_ptr, uses\_allocators, weak, when, write

## Semantics

The directive-name-modifier is a universal modifier that can be used on any clause. The directive-name-modifier specifies directive-name, which is the directive name of a directive, construct or constituent construct to which the clause applies. If the directive name is that of a compound construct, then the leaf constructs to which the clause applies are determined as specified in Section 19.2. If no directive-name-modifier is specified then the efect is as if a directive-name-modifier was specified with the directive name of the directive on which the clause appears.

## Restrictions

Restrictions to the directive-name-modifier are as follows:

• The directive-name-modifier must specify the directive name of either the directive on which the clause appears or a constituent directive of that directive.

## Cross References

• absent Clause, see Section 10.6.1.1

• acq\_rel Clause, see Section 17.8.1.1

• acquire Clause, see Section 17.8.1.2

• adjust\_args Clause, see Section 9.6.2

• affinity Clause, see Section 14.10

• align Clause, see Section 8.3
• aligned Clause, see Section 7.12
• allocate Clause, see Section 8.6
• allocator Clause, see Section 8.4
• append\_args Clause, see Section 9.6.3
• apply Clause, see Section 11.1
• at Clause, see Section 10.2
• atomic\_default\_mem\_order Clause, see Section 10.5.1.1
• bind Clause, see Section 13.8.1
• capture Clause, see Section 17.8.3.1
• full Clause, see Section 11.9.1
• partial Clause, see Section 11.9.2
• collapse Clause, see Section 6.4.5
• collector Clause, see Section 7.6.19
• combiner Clause, see Section 7.6.15
• compare Clause, see Section 17.8.3.2
• contains Clause, see Section 10.6.1.2
• copyin Clause, see Section 7.8.1
• copyprivate Clause, see Section 7.8.2
• default Clause, see Section 7.5.1
• defaultmap Clause, see Section 7.9.9
• depend Clause, see Section 17.9.5
• destroy Clause, see Section 5.7
• detach Clause, see Section 14.11
• device Clause, see Section 15.2
• device\_safesync Clause, see Section 10.5.1.7
• device\_type Clause, see Section 15.1
• dist\_schedule Clause, see Section 13.7.1
• doacross Clause, see Section 17.9.7

• dynamic\_allocators Clause, see Section 10.5.1.2

• enter Clause, see Section 7.9.7

• exclusive Clause, see Section 7.7.2

• fail Clause, see Section 17.8.3.3

• filter Clause, see Section 12.5.1

• final Clause, see Section 14.7

• firstprivate Clause, see Section 7.5.4

• from Clause, see Section 7.10.2

• grainsize Clause, see Section 14.2.1

• graph\_id Clause, see Section 14.3.1

• graph\_reset Clause, see Section 14.3.2

• has\_device\_addr Clause, see Section 7.5.9

• hint Clause, see Section 17.1

• holds Clause, see Section 10.6.1.3

• if Clause, see Section 5.5

• in\_reduction Clause, see Section 7.6.12

• inbranch Clause, see Section 9.8.1.1

• inclusive Clause, see Section 7.7.1

• indirect Clause, see Section 9.9.3

• induction Clause, see Section 7.6.13

• inductor Clause, see Section 7.6.18

• init Clause, see Section 5.6

• init\_complete Clause, see Section 7.7.3

• initializer Clause, see Section 7.6.16

• interop Clause, see Section 9.7.1

• is\_device\_ptr Clause, see Section 7.5.7

• lastprivate Clause, see Section 7.5.5

• linear Clause, see Section 7.5.6

• link Clause, see Section 7.9.8

local Clause, see Section 7.14
map Clause, see Section 7.9.6
match Clause, see Section 9.6.1
memscope Clause, see Section 17.8.4
mergeable Clause, see Section 14.5
message Clause, see Section 10.3
no\_openmp Clause, see Section 10.6.1.4
no\_openmp\_constructs Clause, see Section 10.6.1.5
no\_openmp\_routines Clause, see Section 10.6.1.6
no\_parallelism Clause, see Section 10.6.1.7
nocontext Clause, see Section 9.7.3
nogroup Clause, see Section 17.7
nontemporal Clause, see Section 12.4.1
notinbranch Clause, see Section 9.8.1.2
novariants Clause, see Section 9.7.2
nowait Clause, see Section 17.6
num\_tasks Clause, see Section 14.2.2
num\_teams Clause, see Section 12.2.1
num\_threads Clause, see Section 12.1.2
order Clause, see Section 12.3
ordered Clause, see Section 6.4.6
otherwise Clause, see Section 9.4.2
permutation Clause, see Section 11.4.1
priority Clause, see Section 14.9
private Clause, see Section 7.5.3
proc\_bind Clause, see Section 12.1.4
read Clause, see Section 17.8.2.1
reduction Clause, see Section 7.6.10
relaxed Clause, see Section 17.8.1.3

• release Clause, see Section 17.8.1.4

• replayable Clause, see Section 14.6

• reverse\_offload Clause, see Section 10.5.1.3

• safelen Clause, see Section 12.4.2

• safesync Clause, see Section 12.1.5

• schedule Clause, see Section 13.6.3

• self\_maps Clause, see Section 10.5.1.6

• seq\_cst Clause, see Section 17.8.1.5

• severity Clause, see Section 10.4

• shared Clause, see Section 7.5.2

• simd Clause, see Section 17.10.3.2

• simdlen Clause, see Section 12.4.3

• sizes Clause, see Section 11.2

• task\_reduction Clause, see Section 7.6.11

• thread\_limit Clause, see Section 15.3

• threads Clause, see Section 17.10.3.1

• threadset Clause, see Section 14.8

• to Clause, see Section 7.10.1

• transparent Clause, see Section 17.9.6

• unified\_address Clause, see Section 10.5.1.4

• unified\_shared\_memory Clause, see Section 10.5.1.5

• uniform Clause, see Section 7.11

• untied Clause, see Section 14.4

• update Clause, see Section 17.8.2.2

• update Clause, see Section 17.9.4

• use Clause, see Section 16.1.2

• use\_device\_addr Clause, see Section 7.5.10

• use\_device\_ptr Clause, see Section 7.5.8

• uses\_allocators Clause, see Section 8.8

• weak Clause, see Section 17.8.3.4

• when Clause, see Section 9.4.1

• write Clause, see Section 17.8.2.3

## 5.5 if Clause

Modifiers

<table><tr><td>Name: if</td><td>Properties: target-consistent</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>if-expression</td><td>expression of OpenMP logical type</td><td>default</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

cancel, parallel, simd, target, target\_data, target\_enter\_data, target\_exit\_data, target\_update, task, task\_iteration, taskgraph, taskloop, teams

## Semantics

The efect of the if clause depends on the construct to which it is applied. If the construct is not a compound construct then the efect is described in the section that describes that construct.

## Restrictions

Restrictions to the if clause are as follows:

• At most one if clause can be specified that applies to the semantics of any construct or constituent construct of a directive-specification.

## Cross References

• cancel Construct, see Section 18.2

• parallel Construct, see Section 12.1

• simd Construct, see Section 12.4

• target Construct, see Section 15.8

• target\_data Construct, see Section 15.7

• target\_enter\_data Construct, see Section 15.5

• target\_exit\_data Construct, see Section 15.6

• target\_update Construct, see Section 15.9

• task Construct, see Section 14.1

• task\_iteration Directive, see Section 14.2.3

• taskgraph Construct, see Section 14.3

• taskloop Construct, see Section 14.2

• teams Construct, see Section 12.2

## 5.6 init Clause

<table><tr><td>Name: init</td><td>Properties: innermost-leaf</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>init-var</td><td>variable of OpenMP type</td><td>default</td></tr></table>

## Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>prefer-type</td><td>init-var</td><td>Complex, name: prefer_typeArguments: prefer-type-specification list of preference spec- ification list item type (default)</td><td>complex, unique</td></tr><tr><td>depinfo-modifier</td><td>init-var</td><td>Complex, Keyword: in, inout, inoutset, mutexinoutset, outArguments: locator-list-item locator list item (default)</td><td>complex, unique</td></tr><tr><td>interop-type</td><td>init-var</td><td>Keyword: target, targetsync</td><td>repeatable</td></tr><tr><td>directive-name- modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

depobj, interop

## Semantics

When the init clause appears on a depobj construct, it specifies that init-var is a depend object for which the state is set to initialized. The efect is that init-var is set to represent a dependence type and locator list item as specified by the name and argument of the depinfo-modifier.

When the init clause appears on an interop construct, it specifies that init-var is an interoperability object that is initialized to refer to the list of properties associated with any interop-type. For any interop-type, the properties type, type\_name, vendor, vendor\_name and device\_num will be available. If the implementation cannot initialize interop-var, it is initialized to omp\_interop\_none.

The targetsync interop-type will additionally provide the targetsync property, which is the handle to a foreign synchronization object for enabling synchronization between OpenMP tasks and foreign tasks that execute in the foreign execution context.

The target interop-type will additionally provide the following properties:

• device, which will be a foreign device handle;

• device\_context, which will be a foreign device context handle; and

• platform, which will be a handle to a foreign platform of the device.

## Restrictions

• init-var must not be constant.

• If the init clause appears on a depobj construct, init-var must refer to a variable of depend OpenMP type that is uninitialized.

• If the init clause appears on a depobj construct then the depinfo-modifier has the required property and otherwise it must not be present.

• If the init clause appears on an interop construct, init-var must refer to a variable of interop OpenMP type.

• If the init clause appears on an interop construct, the interop-type modifier has the required property and each interop-type keyword has the unique property. Otherwise, the interop-type modifier must not be present.

• The prefer-type modifier must not be present unless the init clause appears on an interop construct.

## Cross References

• depobj Construct, see Section 17.9.3

• interop Construct, see Section 16.1

## 5.7 destroy Clause

<table><tr><td>Name: destroy</td><td>Properties: default</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>destroy-var</td><td>variable of OpenMP variable type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

## depobj, interop

## Additional information

When the destroy clause appears on a depobj directive that specifies depend-object as a directive argument, the destroy-var argument may be omitted. If omitted, the efect is as if destroy-var refers to the depend-object argument.

## Semantics

When the destroy clause appears on a depobj construct, the state of destroy-var is set to uninitialized.

When the destroy clause appears on an interop construct, the interop-type is inferred based on the interop-type used to initialize destroy-var, and destroy-var is set to the value of omp\_interop\_none after resources associated with destroy-var are released. The object referred to by destroy-var is unusable after destruction and the efect of using values associated with it is unspecified until it is initialized again by another interop construct.

## Restrictions

• destroy-var must not be constant.

• If the destroy clause appears on a depobj construct, destroy-var must refer to a variable of depend OpenMP type that is initialized.

• If the destroy clause appears on an interop construct, destroy-var must refer to a variable of interop OpenMP type that is initialized.

## Cross References

• depobj Construct, see Section 17.9.3

• interop Construct, see Section 16.1

# 6 Base Language Formats and Restrictions

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

• OpenMP Foreign Runtime Identifiers, see Section 16.1.1

• OpenMP Reduction and Induction Identifiers, see Section 7.6.1

• Mapper Identifiers and mapper Modifiers, see Section 7.9.4

## 6.2 OpenMP Stylized Expressions

An OpenMP stylized expression is a base language expression that is subject to restrictions that enable its use within an OpenMP implementation. OpenMP stylized expressions often use OpenMP identifiers that the implementation binds to well-defined internal state.

## Cross References

• OpenMP Collector Expressions, see Section 7.6.2.4

• OpenMP Combiner Expressions, see Section 7.6.2.1

• OpenMP Inductor Expressions, see Section 7.6.2.3

• OpenMP Initializer Expressions, see Section 7.6.2.2

![](images/ea8a44ade411ce027677b194c54986d0e71bc00aa00aa5b3b1d558deef490b77.jpg)

![](images/22f346b74da0196c0dd016b75852c25451f805f458be03d85e1e9d0d19cbd8e6.jpg)
