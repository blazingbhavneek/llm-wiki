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
