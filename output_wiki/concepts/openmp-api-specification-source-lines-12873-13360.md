# OpenMP-API-Specification Source Lines 12873-13360

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source OpenMP-API-Specification:L12873-L13360

Citation: [OpenMP-API-Specification:L12873-L13360]

````text
## 9.7 dispatch Construct

<table><tr><td>Name: dispatchCategory: executable</td><td>Association: block : function-dispatchProperties: context-matching</td></tr></table>

## Clauses

depend, device, has\_device\_addr, interop, is\_device\_ptr, nocontext, novariants, nowait

## Binding

The binding task set for a dispatch region is the generating task. The dispatch region binds to the region of the generating task.

## Semantics

The dispatch construct controls whether variant substitution occurs for target-call in the associated function-dispatch structured block. The dispatch construct may also modify the semantic requirement set of elements that afect the arguments of the function variant if variant substitution occurs (see Section 9.6.2 and Section 9.6.3).

Elements added to the semantic requirement set by the dispatch construct can be removed by the efect of declare variant directives (see Section 9.5) before the dispatch region is executed. If one or more depend clauses are present on the dispatch construct, they are added as depend elements of the semantic requirement set. If a nowait clause is present on the dispatch construct the nowait element is added to the semantic requirement set. For each list item specified in an is\_device\_ptr clause, an is\_device\_ptr element for that list item is added to the semantic requirement set. For each list item specified in a has\_device\_addr clause, a has\_device\_addr element for that list item is added to the semantic requirement set. For each list item specified in an interop clause, an interop element for that list item is added to the semantic requirement set in the same order that they were specified on the directive.

If the dispatch directive adds one or more depend element to the semantic requirement set, and those element are not removed by the efect of a declare variant directive, the behavior is as if those elements were applied as depend clauses to a taskwait construct that is executed before the dispatch region is executed.

The addition of the nowait and interop elements to the semantic requirement set by the dispatch directive has no efect on the dispatch construct apart from the efect it may have on the arguments that are passed when calling a function variant.

If the device clause is present, the value of the default-device-var ICV is set to the value of the expression in the clause on entry to the dispatch region and is restored to its previous value at the end of the region.

If the interop clause is present and has only one interop-var, and the device clause is not specified, the behavior is as if the device clause is present with a device-description equivalent to the device\_num property of the interop-var.

## Restrictions

Restrictions to the dispatch construct are as follows:

• If the interop clause is present and has more than one interop-var then the device clause must also be present.

## Cross References

• depend Clause, see Section 17.9.5

• device Clause, see Section 15.2

• OpenMP Function Dispatch Structured Blocks, see Section 6.3.2

• Semantic Requirement Set, see Section 9.5

• has\_device\_addr Clause, see Section 7.5.9

• interop Clause, see Section 9.7.1

• is\_device\_ptr Clause, see Section 7.5.7

• nocontext Clause, see Section 9.7.3

• novariants Clause, see Section 9.7.2

• nowait Clause, see Section 17.6

• taskwait Construct, see Section 17.5

## 9.7.1 interop Clause

<table><tr><td>Name: interop</td><td>Properties: unique</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>interop-var-list</td><td>list of variable of interop OpenMP type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

## dispatch

## Semantics

The interop clause specifies interoperability objects to be added to the semantic requirement set of the encountering task. They are added to the semantic requirement set in the same order in which they are specified in the interop clause.

## Restrictions

Restrictions to the interop clause are as follows:

• If the interop clause is specified on a dispatch construct, the matching declare\_variant directive for the target-call must have an append\_args clause with a number of list items that equals or exceeds the number of list items in the interop clause.

## Cross References

• dispatch Construct, see Section 9.7

## 9.7.2 novariants Clause

<table><tr><td>Name: novariants</td><td>Properties: unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>do-not-use-variant</td><td>expression of OpenMP logical type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

## dispatch

## Semantics

If do-not-use-variant evaluates to true, no function variant is selected for the target-call of the dispatch region associated with the novariants clause even if one would be selected normally. The use of a variable in do-not-use-variant causes an implicit reference to the variable in all enclosing constructs. do-not-use-variant is evaluated in the enclosing context.

## Cross References

• dispatch Construct, see Section 9.7

## 9.7.3 nocontext Clause

<table><tr><td>Name: nocontext</td><td>Properties: unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>do-not-update-context</td><td>expression of OpenMP logical type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

dispatch

## Semantics

If do-not-update-context evaluates to true, the construct on which the nocontext clause appears is not added to the construct trait set of the OpenMP context. The use of a variable in do-not-update-context causes an implicit reference to the variable in all enclosing constructs. do-not-update-context is evaluated in the enclosing context.

## Cross References

• dispatch Construct, see Section 9.7

## 9.8 declare\_simd Directive

<table><tr><td>Name:declare_simdCategory:declarative</td><td>Association:declarationProperties:pure, variant-generating</td></tr></table>

## Arguments

declare\_simd[(proc-name)]

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>proc-name</td><td>identifier of function type</td><td>optional</td></tr></table>

## Clause groups

branch

## Clauses

aligned, linear, simdlen, uniform

## Additional information

The declare\_simd directive may alternatively be specified with declare simd as the directive-name.

## Semantics

The association of one or more declare\_simd directives with a procedure declaration or definition enables the creation of corresponding SIMD versions of the associated procedure that can be used to process multiple arguments from a single invocation in a SIMD loop concurrently.

If a SIMD version is created and the simdlen clause is not specified, the number of concurrent arguments for the function is implementation defined.

For purposes of the linear clause, any integer-typed parameter that is specified in a uniform clause on the directive is considered to be constant and so may be used in a step-complex-modifier as linear-step.

![](images/6d259ff53363d8adcebdcafb33398e1906c6c88fee21c8edc2a5f819afa05783.jpg)

C / C++

The expressions that appear in the clauses of each directive are evaluated in the scope of the arguments of the procedure declaration or definition.

C / C++

C++

The special this pointer can be used as if it was one of the arguments to the procedure in any of the linear, aligned, or uniform clauses.

C++

## Restrictions

Restrictions to the declare\_simd directive are as follows:

• The procedure body must be a structured block.

• The execution of the procedure, when called from a SIMD loop, must not result in the execution of any constructs except for atomic constructs and ordered constructs on which the simd clause is specified.

• The execution of the procedure must not have any side efects that would alter its execution for concurrent iterations of a SIMD chunk.

C / C++

• If a declare\_simd directive is specified for a declaration of a procedure then the definition of the procedure must have a declare\_simd directive with identical clauses with identical arguments and modifiers.

• The procedure must not contain calls to the longjmp or setjmp functions.

C / C++

• The procedure must not contain throw statements.

Fortran

• proc-name must not be a generic name, procedure pointer, or entry name.

• If proc-name is omitted, the declare\_simd directive must appear in the specification part of a subroutine subprogram or a function subprogram for which creation of the SIMD versions is enabled.

• Any declare\_simd directive must appear in the specification part of a subroutine subprogram, function subprogram, or interface body to which it applies.

• If a procedure is declared via a procedure declaration statement, the procedure proc-name should appear in the same specification.

• If a declare\_simd directive is specified for a procedure then the definition of the procedure must contain a declare\_simd directive with identical clauses with identical arguments and modifiers.

• Procedures pointers may not be used to access versions created by the declare\_simd directive.

Fortran

## Cross References

• aligned Clause, see Section 7.12

• linear Clause, see Section 7.5.6

• simdlen Clause, see Section 12.4.3

• uniform Clause, see Section 7.11

## 9.8.1 branch Clauses

Clause groups

<table><tr><td>Properties: exclusive, unique</td><td>Members:Clausesinbranch, notinbranch</td></tr></table>

## Directives

declare\_simd

## Semantics

The branch clause group defines a set of clauses that indicate if a procedure can be assumed to be or not to be encountered in a branch. If neither clause is specified, then the procedure may or may not be called from inside a conditional statement of the calling context.

## Cross References

• declare\_simd Directive, see Section 9.8

## 9.8.1.1 inbranch Clause

<table><tr><td>Name: inbranch</td><td>Properties: unique</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>inbranch</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

declare\_simd

## Semantics

If inbranch evaluates to true, the inbranch clause specifies that the procedure will always be called from inside a conditional statement of the calling context. If inbranch evaluates to false, the procedure may be called other than from inside a conditional statement. If inbranch is not specified, the efect is as if inbranch evaluates to true.

## Cross References

• declare\_simd Directive, see Section 9.8

## 9.8.1.2 notinbranch Clause

<table><tr><td>Name: notinbranch</td><td>Properties: unique</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>notinbranch</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

declare\_simd

## Semantics

If notinbranch evaluates to true, the notinbranch clause specifies that the procedure will never be called from inside a conditional statement of the calling context. If notinbranch evaluates to false, the procedure may be called from inside a conditional statement. If notinbranch is not specified, the efect is as if notinbranch evaluates to true.

## Cross References

• declare\_simd Directive, see Section 9.8

## 9.9 Declare Target Directives

Declare target directives apply to procedures and/or variables to ensure that they can be executed or accessed on a device. Variables are either replicated as device-local variables for each device through a local clause, are mapped for all device executions through an enter clause, or are mapped for specific device executions through a link clause. An implementation may generate diferent versions of a procedure to be used for target regions that execute on diferent devices. Whether it generates diferent versions, and whether it calls a diferent version in a target region from the version that it calls outside a target region, are implementation defined.

To facilitate device usage, OpenMP defines rules that implicitly specify declare target directives for procedures and variables. The remainder of this section defines those rules as well as restrictions that apply to all declare target directives.

C++

If a variable with static storage duration has the constexpr specifier and is not a groupprivate variable then the variable is treated as if it had appeared as a list item in an enter clause on a declare target directive.

If a variable with static storage duration that is not a device-local variable (including that it is not a groupprivate variable) is declared in a device procedure then the variable is treated as if it had appeared as a list item in an enter clause on a declare target directive.

If a procedure is referenced outside of any reverse-ofload region in a procedure that appears as a list item in an enter clause on a non-host declare target directive then the name of the referenced procedure is treated as if it had appeared in an enter clause on a declare target directive.

C / C++

If a variable with static storage duration or a function (except lambda for C++) is referenced in the initializer expression list of a variable with static storage duration that appears as a list item in an enter or local clause on a declare target directive then the name of the referenced variable or procedure is treated as if it had appeared in an enter clause on a declare target directive.

C / C++

Fortran

If a declare\_target directive has a device\_type clause then any enclosed internal procedure cannot contain any declare\_target directives. The enclosing device\_type clause implicitly applies to internal procedures.

Fortran

A reference to a device-local variable that has static storage duration inside a device procedure is replaced with a reference to the copy of the variable for the device. Otherwise, a reference to a variable that has static storage duration in a device procedure is replaced with a reference to a corresponding variable in the device data environment. If the corresponding variable does not exist or the variable does not appear in an enter or link clause on a declare target directive, the behavior is unspecified.

## Execution Model Events

The target-global-data-op event occurs when an original list item is associated with a corresponding list item on a device as a result of a declare target directive; the event occurs before the first access to the corresponding list item.

## Tool Callbacks

A thread dispatches a registered target\_data\_op\_emi callback with ompt\_scope\_beginend as its endpoint argument for each occurrence of a target-global-data-op event in that thread.

## Restrictions

Restrictions to any declare target directive are as follows:

• The same list item must not explicitly appear in both an enter clause on one declare target directive and a link or local clause on another declare target directive.

• The same list item must not explicitly appear in both a link clause on one declare target directive and a local clause on another declare target directive.

• If a variable appears in a enter clause on a declare target directive, its initializer must not refer to a variable that appears in a link clause on a declare target directive.

## Cross References

• begin declare\_target Directive, see Section 9.9.2

• declare\_target Directive, see Section 9.9.1

• enter Clause, see Section 7.9.7

• link Clause, see Section 7.9.8

• OMPT scope\_endpoint Type, see Section 33.27

• target Construct, see Section 15.8

• target\_data\_op\_emi Callback, see Section 35.7

## 9.9.1 declare\_target Directive

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
````
