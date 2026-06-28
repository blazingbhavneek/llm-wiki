## 7.6.6 Properties Common to All Reduction Clauses

The clause-specification of a reduction clause has a clause-argument-specification that specifies a variable list and has a required reduction-identifier modifier that specifies the reduction identifier to use for the list items. This match is done by means of a name lookup in the base language.

C++

If the type is of class type and the reduction identifier is implicitly declared, then it must provide the operator as described in Section 7.6.5 as well as one of:

• A default constructor and an assignment operator that accepts a type T that can be implicitly constructed from an integer expression, such that the following requirement is valid:

```cpp
template<typename T>
requires(T&& t) {
    T();
    t = 0;
};
```

• A single-argument constructor that accepts a type T that can be implicitly constructed from an integer expression, such that the following requirement is valid:

```txt
template<typename T>
requires() {
    T(0);
};
```

The first of these that matches will be used, with the initializer value being passed to the assignment operator or constructor.

Any copies of a list item associated with the reduction have the reduction attribute and so are reduction variables. These reduction variables are initialized with the initializer value of the reduction identifier. Any copies are combined using the combiner associated with the reduction identifier.

## Execution Model Events

The reduction-begin event occurs before a task begins to perform loads and stores that belong to the implementation of a reduction and the reduction-end event occurs after the task has completed loads and stores associated with the reduction. If a task participates in multiple reductions, each reduction may be bracketed by its own pair of reduction-begin/reduction-end events or multiple reductions may be bracketed by a single pair of events. The interval defined by a pair of reduction-begin/reduction-end events will not contain a task scheduling point.

## Tool Callbacks

A thread dispatches a registered reduction callback with ompt\_sync\_region\_reduction in its kind argument and ompt\_scope\_begin as its endpoint argument for each occurrence of a reduction-begin event in that thread. Similarly, a thread dispatches a registered reduction callback with ompt\_sync\_region\_reduction in its kind argument and ompt\_scope\_end as its endpoint argument for each occurrence of a reduction-end event in that thread. These callbacks occur in the context of the task that performs the reduction.

## Restrictions

Restrictions common to reduction clauses are as follows:

• For a max or min reduction, the type of the list item must be an allowed arithmetic data type: char, int, float, double, or \_Bool, possibly modified with long, short, signed, or unsigned.

• For a max or min reduction, the type of the list item must be an allowed arithmetic data type: char, wchar\_t, int, float, double, or bool, possibly modified with long, short, signed, or unsigned.

![](images/a5154b9801927dfa11c25372d2a5dcf1a1902807e94e7fee133bfe20a8b3fc36.jpg)

## Cross References

• reduction Callback, see Section 34.7.6

• OMPT scope\_endpoint Type, see Section 33.27

• OMPT sync\_region Type, see Section 33.33

## 7.6.7 Reduction Scoping Clauses

Reduction-scoping clauses define the region in which a reduction is computed by tasks or SIMD lanes. All properties common to all reduction clauses, which are defined in Section 7.6.5 and Section 7.6.6, apply to reduction-scoping clauses.

The number of copies created for each list item and the point at which those copies are initialized are determined by the particular reduction-scoping clause that appears on the construct. The point at which the original list item contains the result of the reduction is determined by the particular

reduction-scoping clause. To avoid data races, concurrent reads or updates of the original list item must be synchronized with the update of the original list item that occurs as a result of the reduction, which may occur after execution of the construct on which the reduction-scoping clause appears, for example, due to the use of a nowait clause.

The location in the OpenMP program at which values are combined and the order in which values are combined are unspecified. Thus, when comparing sequential and parallel executions, or when comparing one parallel execution to another (even if the number of threads used is the same), bitwise-identical results are not guaranteed. Similarly, side efects (such as floating-point exceptions) may not be identical and may not occur at the same location in the OpenMP program

## 7.6.8 Reduction Participating Clauses

A reduction-participating clause specifies a task or a SIMD lane as a participant in a reduction defined by a reduction-scoping clause. All properties common to all reduction clauses, which are defined in Section 7.6.5 and Section 7.6.6, apply to reduction-participating clauses.

Accesses to the original list item may be replaced by accesses to copies of the original list item created by a region that corresponds to a construct with a reduction-scoping clause.

In any case, the final value of the reduction must be determined as if all tasks or SIMD lanes that participate in the reduction are executed sequentially in some arbitrary order.

## 7.6.9 reduction-identifier Modifier

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>reduction-identifier</td><td>all arguments</td><td>An OpenMP reduction iden-tifier</td><td>required, ultimate</td></tr></table>

## Clauses

in\_reduction, reduction, task\_reduction

## Semantics

Reduction clauses use the reduction-identifier modifier to specify the reduction identifier for the clause. The reduction identifier determines the initializer expression and combiner expression to use for the reduction.

## Cross References

• OpenMP Reduction and Induction Identifiers, see Section 7.6.1

• in\_reduction Clause, see Section 7.6.12

• reduction Clause, see Section 7.6.10

• task\_reduction Clause, see Section 7.6.11

7.6.10 reduction Clause

<table><tr><td>Name: reduction</td><td>Properties: data-environment attribute, data-sharing attribute, original list-item updating, privatization, reduction scoping, reduction participating</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>reduction-identifier</td><td>all arguments</td><td>An OpenMP reduction iden-tifier</td><td>required, ultimate</td></tr><tr><td>reduction-modifier</td><td>list</td><td>Keyword: default,inscan, task</td><td>default</td></tr><tr><td>original-sharing-modifier</td><td>list</td><td>Complex, name: originalArguments:sharing Keyword:default, private,shared (default)</td><td>default</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

do, for, loop, parallel, scope, sections, simd, taskloop, teams

## Semantics

The reduction clause is a reduction-scoping clause and a reduction-participating clause, as described in Section 7.6.7 and Section 7.6.8. For each list item, a private copy is created for each implicit task or SIMD lane and is initialized with the initializer value of the reduction-identifier. After the end of the region, the original list item is updated with the values of the private copies using the combiner associated with the reduction-identifier. If the clause appears on a worksharing construct and the original list item is private in the enclosing context of that construct, the behavior is as if a shared copy (initialized with the initializer value) specific to the worksharing region is updated by combining its value with the values of the private copies created by the clause; once an encountering thread observes that all of those updates are completed, the original list item for that thread is then updated by combining its value with the value of the shared copy.

If the original-sharing-modifier is not present, the behavior is as if it were present with the sharing argument specified as default. If the sharing argument is specified as default, original list items are assumed to be shared in the enclosing context unless determined not to be shared according to the rules specified in Section 7.1. If shared or private is specified as the

original-sharing-modifier sharing argument, the original list items are assumed to be shared or private, respectively, in the enclosing context.

If reduction-modifier is not present or the default reduction-modifier is present, the behavior is as follows. For parallel and worksharing constructs, one or more private copies of each list item are created for each implicit task, as if the private clause had been used. For the simd construct, one or more private copies of each list item are created for each SIMD lane, as if the private clause had been used. For the taskloop construct, private copies are created according to the rules of the reduction-scoping clause. For the teams construct, one or more private copies of each list item are created for the initial task of each team in the league, as if the private clause had been used. For the loop construct, private copies are created and used in the construct according to the description and restrictions in Section 7.4. At the end of a region that corresponds to a construct for which the reduction clause was specified, the original list item is updated by combining its original value with the final value of each of the private copies, using the combiner of the specified reduction-identifier.

If the inscan reduction-modifier is present, a scan computation is performed over updates to the list item performed in each logical iteration of the afected loops (see Section 7.7). The list items are privatized in the construct according to the description and restrictions in Section 7.4. At the end of the region, each original list item is assigned the value described in Section 7.7.

If the task reduction-modifier is present for a parallel or worksharing construct, then each list item is privatized according to the description and restrictions in Section 7.4, and an unspecified number of additional private copies may be created to support task reductions. Any copies associated with the reduction are initialized before they are accessed by the tasks that participate in the reduction, which include all implicit tasks in the corresponding region and all participating explicit tasks that specify an in\_reduction clause (see Section 7.6.12). After the end of the region, the original list item contains the result of the reduction.

## Restrictions

Restrictions to the reduction clause are as follows:

• All restrictions common to all reduction clauses, as listed in Section 7.6.5 and Section 7.6.6, apply to this clause.

• For a given construct on which the clause appears, the lifetime of all original list items must extend at least until after the synchronization point at which the completion of the corresponding region by all participants in the reduction can be observed by all participants.

• If the inscan reduction-modifier is specified on a reduction clause that appears on a worksharing construct and an original list item is private in the enclosing context of the construct, the private copies must all have identical values when the construct is encountered.

• If the reduction clause appears on a worksharing construct and the original-sharing-modifier specifies default as its sharing argument, each original list item must be shared in the enclosing context unless it is determined not to be shared according to the rules specified in Section 7.1.

• If the reduction clause appears on a worksharing construct and the original-sharing-modifier specifies shared or private as its sharing argument, the original list items must be shared or private, respectively, in the enclosing context.

• Each list item specified with the inscan reduction-modifier must appear as a list item in an inclusive or exclusive clause on a scan directive enclosed by the construct.

• If the inscan reduction-modifier is specified, a reduction clause without the inscan reduction-modifier must not appear on the same construct.

• A list item that appears in a reduction clause on a work-distribution construct for which the corresponding region binds to a teams region must be shared in the teams region.

• A reduction clause with the task reduction-modifier may only appear on a parallel construct or a worksharing construct, or a compound construct for which any of the aforementioned constructs is a constituent construct and neither simd nor loop are constituent constructs.

• A reduction clause with the inscan reduction-modifier may only appear on a worksharing-loop construct or a simd construct, or a compound construct for which any of the aforementioned constructs is a constituent construct and neither distribute nor taskloop is a constituent construct.

• The inscan reduction-modifier must not be specified on a construct for which the ordered or schedule clause is specified.

• A list item that appears in a reduction clause of the innermost enclosing worksharing construct or parallel construct must not be accessed in an explicit task generated by a construct unless an in\_reduction clause with the same list item appears on that construct.

• The task reduction-modifier must not appear in a reduction clause if the nowait clause is specified on the same construct.

## Fortran

• If the original-sharing-modifier for a reduction clause on a worksharing construct specifies default sharing and a list item in the clause either has a base pointer or is a dummy argument without the VALUE attribute, the original list item must refer to the same object for all threads of the team that execute the corresponding region.

Fortran

C / C++

• If the original-sharing-modifier specifies default as it sharing argument and a list item in a reduction clause on a worksharing construct has a reference type then that list item must bind to the same object for all threads of the team.

• A variable of class type (or array thereof) that appears in a reduction clause with the inscan reduction-modifier requires an accessible, unambiguous default constructor and copy assignment operator for the class type; the number of calls to them while performing the scan computation is unspecified.

## Cross References

• do Construct, see Section 13.6.2

• for Construct, see Section 13.6.1

• List Item Privatization, see Section 7.4
