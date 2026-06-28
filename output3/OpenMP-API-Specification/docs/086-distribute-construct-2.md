## 13.7 distribute Construct

<table><tr><td>Name: distributeCategory: executable</td><td>Association: loop nestProperties: SIMD-partitionable,teams-nestable, work-distribution, partitioned</td></tr></table>

## Clauses

allocate, collapse, dist\_schedule, firstprivate, induction, lastprivate, order, private

## Binding

The binding thread set for a distribute region is the set of initial threads executing an enclosing teams region. A distribute region binds to this teams region.

## Semantics

The distribute construct specifies that the collapsed iterations will be executed by the initial teams in the context of their implicit tasks. The collapsed iterations are distributed across the initial threads of all initial teams that execute the teams region to which the distribute region binds. No implicit barrier occurs at the end of a distribute region. To avoid data races the original list items that are modified due to lastprivate clauses should not be accessed between the end of the distribute construct and the end of the teams region to which the distribute binds.

If the dist\_schedule clause is not specified, the loop schedule is implementation defined.

The schedule is reproducible if one of the following conditions is true:

• The order clause is specified with the reproducible order-modifier modifier; or

• The dist\_schedule clause is specified with static as the kind argument and the order clause is not specified with the unconstrained order-modifier.

## Execution Model Events

The distribute-begin event occurs after an initial task encounters a distribute construct but before the task starts to execute the structured block of the distribute region. The distribute-end event occurs after an initial task finishes execution of a distribute region but before it resumes execution of the enclosing context.

The distribute-chunk-begin event occurs for each scheduled chunk of a distribute region before execution of any collapsed iteration.

## Tool Callbacks

A thread dispatches a registered work callback with ompt\_scope\_begin as its endpoint argument and ompt\_work\_distribute as its work\_type argument for each occurrence of a distribute-begin event in that thread. Similarly, a thread dispatches a registered work callback with ompt\_scope\_end as its endpoint argument and ompt\_work\_distribute as its work\_type argument for each occurrence of a distribute-end event in that thread. The callbacks occur in the context of the implicit task.

A thread dispatches a registered dispatch callback for each occurrence of a distribute-chunk-begin event in that thread. The callback occurs in the context of the initial task.

## Restrictions

Restrictions to the distribute construct are as follows:

• The collapsed iteration space must the same for all teams in the league.

• The region that corresponds to the distribute construct must be a strictly nested region of a teams region.

• A list item may appear in a firstprivate or lastprivate clause, but not in both.

• The conditional lastprivate-modifier must not be specified.

• All list items that appear in an induction clause must be private variables in the enclosing context.

## Cross References

• allocate Clause, see Section 8.6

• collapse Clause, see Section 6.4.5

• dispatch Callback, see Section 34.4.2

• dist\_schedule Clause, see Section 13.7.1

• firstprivate Clause, see Section 7.5.4

• Consistent Loop Schedules, see Section 6.4.4

• induction Clause, see Section 7.6.13

• lastprivate Clause, see Section 7.5.5

• order Clause, see Section 12.3

• private Clause, see Section 7.5.3

• OMPT scope\_endpoint Type, see Section 33.27

• teams Construct, see Section 12.2

• work Callback, see Section 34.4.1

• OMPT work Type, see Section 33.41
