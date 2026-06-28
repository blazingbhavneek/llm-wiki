
This chapter defines rules and mechanisms for nesting regions and for combining constructs.

## 19.1 Compound Directive Names

Unless explicitly specified otherwise, the directive-name of a compound directive concatenates two or more directive names, with an intervening separating character, the directive-name separator between each of them. Each directive name, as well as any concatenation of consecutive directive names and their directive-name separator, is a constituent-directive name. Any constituent-directive name that is not itself a compound-directive name is a leaf-directive name.

Let directive-name-A refer to the first leaf-directive name that appears in a compound-directive name, and let directive-name-B refer to the constituent-directive name that forms the remainder of the compound-directive name. If the construct named by directive-name-B can be immediately nested inside the construct named by directive-name-A, the compound-directive name is a combined-directive name, the name of combined directive. Otherwise, the compound-directive name is a composite-directive name. Unless explicitly specified otherwise, the syntax for a compound-directive name is <compound-directive-name>, as described in the following grammar:

<compound-directive-name>:

<combined-directive-name>

<composite-directive-name>

<combined-directive-name>:

<directive-name-A><separator><directive-name-B>

<directive-name-A>:

<parallelism-generating-directive-name>

<thread-selecting-directive-name>

<directive-name-B>:

<composite-directive-name>

<parallelism-generating-directive-name>

<combined-parallelism-generating-directive-name>

<partitioned-directive-name>

<combined-partitioned-directive-name>

<thread-selecting-directive-name>

<combined-thread-selecting-directive-name>

<composite-directive-name>: <loop-distributed-composite-construct-name> <simd-partitioned-composite-construct-name>

<loop-distributed-composite-construct-name>: <distribute-directive-name><separator><parallel-loop-directive-name>

<simd-partitioned-composite-construct-name>: <simd-partitionable-directive-name><separator><simd-directive-name>

## where:

• <composite-directive-name> is a composite-directive name;

• <parallelism-generating-directive-name> is the name of a parallelism-generating construct;

• <combined-parallelism-generating-directive-name> is a <combined-directive-name> for which <directive-name-A> is a <parallelism-generating-directive-name>.

• <thread-selecting-directive-name> is the name of a thread-selecting construct;

• <combined-thread-selecting-directive-name> is a <combined-directive-name> for which <directive-name-A> is a <thread-selecting-directive-name>.

• <partitioned-directive-name> is the name of a partitioned construct;

• <combined-partitioned-directive-name> is a <combined-directive-name> for which <directive-name-A> is a <partitioned-directive-name>;

• <distribute-directive-name> is distribute;

• <parallel-loop-directive-name> is the name of a combined construct for which <directive-name-A> is parallel and <directive-name-B> is the name of a worksharing-loop construct or a composite directive for which <directive-name-A> is the name of a worksharing-loop construct;

• <simd-partitionable-directive-name> is the name of a SIMD-partitionable construct;

• <simd-directive-name> is simd.

C / C++

• <separator>, the directive-name separator, is white space.

C / C++

Fortran

• <separator>, the directive-name separator, is white space or a plus sign (i.e., ’+’).

Fortran

The section that defines any composite directive for which its composite-directive name is not composed from its leaf-directive names in the fashion described above, such as those that combine a series of directives into one directive, also specifies the composite-directive name and its leaf directives. Unless otherwise specified, those leaf directives may be specified by their leaf-directive names in a directive-name-modifier.

## Restrictions

Restrictions to compound-directive names are as follows:

• Any given instance of a compound-directive name must use the same character for all instances of <separator>.

• Leaf-directive names that include spaces are not permitted in a compound-directive name; they must instead be specified with an underscore replacing each space in the directive name.

• The leaf-directive names of a given compound-directive name must be unique.

• The construct corresponding to <directive-name-B> must be permitted to be immediately nested inside the construct corresponding to <directive-name-A>.

• If the first leaf-directive name of <directive-name-B> is the name of a worksharing construct or a thread-selecting construct then <directive-name-A> must be parallel.

• If <directive-name-A> and the first leaf-directive name of <directive-name-B> are the names of task-generating constructs then their respective explicit task regions must not bind to the same parallel region.

• The compound construct named by a given compound-directive name must have at most one constituent construct that is a map-entering construct.

• The compound construct named by a given compound-directive name must have at most one constituent construct that is a map-exiting construct.

## Fortran

• If a directive name is ambiguous due to the use of optional intervening spaces between leaf-directive names, the directive-name separator must be a plus sign.

## Cross References

• distribute Construct, see Section 13.7

• parallel Construct, see Section 12.1

• simd Construct, see Section 12.4

## 19.2 Clauses on Compound Constructs

This section specifies the handling of clauses on compound constructs and the handling of implicit clauses that arise from any variable with predetermined data-sharing attributes on more than one leaf construct. For any clause for which a directive-name-modifier is specified, the efect of the modifier is applied prior to any of the rules that are specified in this section. Some clauses are permitted only on a single leaf construct of the compound construct, in which case the efect is as if the clause is applied to that specific construct. Other clauses that are permitted on more than one leaf construct have the efect as if they are applied to a subset of those constructs, as detailed in this section. Unless otherwise specified, the efect of a clause on a compound directive is as if it is applied to all leaf constructs that permit it (i.e., it has the default all-constituents property).

Unless otherwise specified, certain clause properties determine how each clause with those properties applies to any constituent directives of a compound directive on which it appears. Regardless of any specified directive-name-modifier, the efect of any clause with the once-for-all-constituents property on a compound construct is as if it is applied once to the compound construct regardless of how many constituent constructs to which they may apply.

The efect of any clause with the all-privatizing property on a compound directive is as if it is applied to all leaf constructs that permit the clause and to which a data-sharing attribute clause that may create a private copy of the same list item is applied. Unless otherwise specified, the efect of any clause with the innermost-leaf property on a compound construct is as if it is applied only to the innermost leaf construct that permits it. Unless otherwise specified, the efect of any clause with the outermost-leaf property on a compound construct is as if it is applied only to the outermost leaf construct that permits it.

The efect of the firstprivate clause is as if it is applied to one or more leaf constructs as follows:

• To the distribute construct if it is among the constituent constructs;

• To the teams construct if it is among the constituent constructs and the distribute construct is not;

• To a worksharing construct that accepts the clause if one is among the constituent constructs;

• To the taskloop construct if it is among the constituent constructs;

• To the parallel construct if it is among the constituent construct and neither a taskloop construct nor a worksharing construct that accepts the clause is among them;

• To the target construct if it is among the constituent constructs and the same list item neither appears in a lastprivate clause nor is the base variable or base pointer of a list item that appears in a map clause.

If the parallel construct is among the constituent constructs and the efect is not as if the firstprivate clause is applied to it by the above rules, then the efect is as if the shared clause with the same list item is applied to the parallel construct. If the teams construct is among the constituent constructs and the efect is not as if the firstprivate clause is applied to it by the above rules, then the efect is as if the shared clause with the same list item is applied to the teams construct.

The efect of the lastprivate clause is as if it is applied to all leaf constructs that permit the clause. If the parallel construct is among the constituent constructs and the list item is not also specified in the firstprivate clause, then the efect of the lastprivate clause is as if the shared clause with the same list item is applied to the parallel construct. If the teams construct is among the constituent constructs and the list item is not also specified in the firstprivate clause, then the efect of the lastprivate clause is as if the shared clause with the same list item is applied to the teams construct. If the target construct is among the constituent constructs and the list item is not the base variable or base pointer of a list item that appears in a map clause, the efect of the lastprivate clause is as if the same list item appears in a map clause with a map-type of tofrom.

The efect of the reduction clause is as if it is applied to all leaf constructs that permit the clause, except for the following constructs:

• The parallel construct, when combined with the sections, worksharing-loop, loop, or taskloop construct; and

• The teams construct, when combined with the loop construct.

For the parallel and teams constructs above, the efect of the reduction clause instead is as if each list item or, for any list item that is an array item, its corresponding base array or corresponding base pointer appears in a shared clause for the construct. If the task reduction-modifier is specified, the efect is as if it only modifies the behavior of the reduction clause on the innermost leaf construct that accepts the modifier (see Section 7.6.10). If the inscan reduction-modifier is specified, the efect is as if it modifies the behavior of the reduction clause on all constructs of the compound construct to which the clause is applied and that accept the modifier. If a list item in a reduction clause on a compound target construct does not have the same base variable or base pointer as a list item in a map clause on the construct, then the efect is as if the list item in the reduction clause appears as a list item in a map clause with a map-type of tofrom.

The efect of the linear clause is as if it is applied to the innermost leaf construct. Additionally, if the list item is not the loop-iteration variable of a construct for which simd is a constituent construct, the efect on the outer leaf constructs is as if the list item was specified in firstprivate and lastprivate clauses on the compound construct, with the rules specified above applied. If a list item of the linear clause is the loop-iteration variable of a construct for which the simd construct is a leaf construct and the variable is not declared in the construct, the efect on the outer leaf constructs is as if the list item was specified in a lastprivate clause on the compound construct with the rules specified above applied.

If the clauses have expressions on them, such as for various clauses where the argument of the clause is an expression, or lower-bound, length, or stride expressions inside array sections (or subscript and stride expressions in subscript-triplet for Fortran), or linear-step or alignment

expressions, the expressions are evaluated immediately before the construct to which the clause has been split or duplicated per the above rules (therefore inside of the outer leaf constructs). However, the expressions inside the num\_teams and thread\_limit clauses are always evaluated before the outermost leaf construct.

The restriction that a list item may not appear in more than one data-sharing attribute clause with the exception of specifying a variable in both firstprivate and lastprivate clauses applies after the clauses are split or duplicated per the above rules.

## Restrictions

Restrictions to clauses on compound constructs are as follows:

• A clause that appears on a compound construct must apply to at least one of the leaf constructs per the rules defined in this section.

## Cross References

• distribute Construct, see Section 13.7

• firstprivate Clause, see Section 7.5.4

• lastprivate Clause, see Section 7.5.5

• linear Clause, see Section 7.5.6

• loop Construct, see Section 13.8

• map Clause, see Section 7.9.6

• num\_teams Clause, see Section 12.2.1

• parallel Construct, see Section 12.1

• reduction Clause, see Section 7.6.10

• sections Construct, see Section 13.3

• shared Clause, see Section 7.5.2

• simd Construct, see Section 12.4

• target Construct, see Section 15.8

• taskloop Construct, see Section 14.2

• teams Construct, see Section 12.2

• thread\_limit Clause, see Section 15.3

## 19.3 Compound Construct Semantics

The semantics of combined constructs are identical to that of explicitly specifying the first construct containing one instance of the second construct and no other statements.

Most composite constructs compose constructs that otherwise cannot be immediately nested to apply multiple loop-nest-associated constructs to the same canonical loop nest. The semantics of each of these composite constructs first apply the semantics of the enclosing construct as specified by directive-name-A and any clauses that apply to it. For each task as appropriate for the semantics of directive-name-A, the application of its semantics yields a nested loop of depth two in which the outer loop iterates over the chunks assigned to that task and the inner loop iterates over the collapsed iteration of each chunk. The semantics of directive-name-B and any clauses that apply to it are then applied to that inner loop. If directive-name-A is taskloop and directive-name-B is simd then for the application of the simd construct, the efect of any in\_reduction clause is as if a reduction clause with the same reduction operator and list items is present.

For all compound constructs, tool callbacks are invoked as if the leaf constructs were explicitly nested. All compound constructs for which a loop-nest-associated construct is a leaf construct are themselves loop-nest-associated constructs.

## Restrictions

Restrictions to compound construct are as follows:

• The restrictions of all constituent directives apply.

• If distribute is a constituent-directive name, the linear clause may only be specified for loop-iteration variables of loops that are associated with the construct and the ordered clause must not be specified.

## Cross References

• distribute Construct, see Section 13.7

• in\_reduction Clause, see Section 7.6.12

• linear Clause, see Section 7.5.6

• ordered Clause, see Section 6.4.6

• parallel Construct, see Section 12.1

• reduction Clause, see Section 7.6.10

• simd Construct, see Section 12.4

• taskloop Construct, see Section 14.2

Part III
