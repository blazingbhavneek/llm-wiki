## 13.8 loop Construct

<table><tr><td>Name: loopCategory: executable</td><td>Association: loop nestProperties: order-concurrent-nestable, partitioned, simdizable, team-executed, teams-nestable, work-distribution, worksharing</td></tr></table>

## Clauses

bind, collapse, lastprivate, order, private, reduction

## Binding

The bind clause determines the binding region, which determines the binding thread set.

## Semantics

A loop construct specifies that the collapsed iterations execute in the context of the binding thread set, in an order specified by the order clause. If the order clause is not specified, the behavior is as if the order clause is present and specifies the concurrent ordering. The collapsed iterations are executed as if by the binding thread set, once per instance of the loop region that is encountered by the binding thread set.

The loop schedule for a loop construct is reproducible unless the order clause is present with the unconstrained order-modifier.

If the loop region binds to a teams region, the threads in the binding thread set may continue execution after the loop region without waiting for all collapsed iterations to complete. The collapsed iterations are guaranteed to complete before the end of the teams region. If the loop region does not bind to a teams region, all collapsed iterations must complete before the encountering threads continue execution after the loop region.

While a loop construct is always a work-distribution construct, it is a worksharing construct if and only if its binding region is the innermost enclosing parallel region. Further, the loop construct has the SIMDizable property if and only if its binding region is not defined.

Fortran

The collapsed loop may be a DO CONCURRENT loop.

Fortran

## Restrictions

Restrictions to the loop construct are as follows:

• A list item must not appear in a lastprivate clause unless it is the loop-iteration variable of an afected loop.

• If a reduction-modifier is specified in a reduction clause that appears on the directive then the reduction-modifier must be default.

• If a loop construct is not nested inside another construct then the bind clause must be present.

• If a loop region binds to a teams region or parallel region, it must be encountered by all threads in the binding thread set or by none of them.

Fortran

• If the collapsed loop is a DO CONCURRENT loop, neither the data-sharing attribute clauses nor the collapse clause may be specified.

• If a variable is accessed in more than one iteration of a DO CONCURRENT loop that is associated with a loop construct and at least one of the accesses modifies the variable, the variable must have locality specified in the DO CONCURRENT loop.

Fortran

## Cross References

• bind Clause, see Section 13.8.1

• collapse Clause, see Section 6.4.5

• Consistent Loop Schedules, see Section 6.4.4

• lastprivate Clause, see Section 7.5.5

• order Clause, see Section 12.3

• private Clause, see Section 7.5.3

• reduction Clause, see Section 7.6.10

• teams Construct, see Section 12.2

## 13.8.1 bind Clause
