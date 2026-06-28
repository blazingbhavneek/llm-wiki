
<table><tr><td>Name: nowait</td><td>Properties: outermost-leaf, unique, end-clause</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>do_not_synchronize</td><td>expression of OpenMP logical type</td><td>optional</td></tr></table>

## Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

dispatch, do, for, interop, scope, sections, single, target, target\_data, target\_enter\_data, target\_exit\_data, target\_update, taskwait, workshare

## Semantics

If do\_not\_synchronize evaluates to true, the nowait clause overrides any synchronization that would otherwise occur at the end of a construct. It can also specify that a semantic requirement set includes the nowait property. If do\_not\_synchronize is not specified, the efect is as if do\_not\_synchronize evaluates to true. If do\_not\_synchronize evaluates to false, the efect is as if the nowait clause is not specified on the directive.

If the construct includes an implicit barrier and do\_not\_synchronize evaluates to true, the nowait clause specifies that the barrier will not occur. If the construct includes an implicit barrier and the nowait is not specified, the barrier will occur.

For constructs that generate a task, if do\_not\_synchronize evaluates to true, the nowait clause specifies that the generated task may be deferred. If the nowait clause is not specified on the directive then the generated task is an included task (so it executes synchronously in the context of the encountering task).

For directives that generate a semantic requirement set, the nowait clause adds the nowait property to the set if do-not-synchronize evaluates to true.

## Restrictions

Restrictions to the nowait clause are as follows:

• The do\_not\_synchronize argument must evaluate to the same value for all threads in the binding thread set, if defined for the construct on which the nowait clause appears.

• The do\_not\_synchronize argument must evaluate to the same value for all tasks in the binding task set, if defined for the construct on which the nowait clause appears.

## Cross References

• dispatch Construct, see Section 9.7

• do Construct, see Section 13.6.2

• for Construct, see Section 13.6.1

• interop Construct, see Section 16.1

• scope Construct, see Section 13.2

• sections Construct, see Section 13.3

• single Construct, see Section 13.1

• target Construct, see Section 15.8

• target\_data Construct, see Section 15.7

• target\_enter\_data Construct, see Section 15.5

• target\_exit\_data Construct, see Section 15.6

• target\_update Construct, see Section 15.9

• taskwait Construct, see Section 17.5

• workshare Construct, see Section 13.4

## 17.7 nogroup Clause

<table><tr><td>Name: nogroup</td><td>Properties: outermost-leaf, unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>do_not_synchronize</td><td>expression of OpenMP logical type</td><td>optional</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

target\_data, taskgraph, taskloop

## Semantics

If do\_not\_synchronize evaluates to true, the nogroup clause overrides any implicit taskgroup that would otherwise enclose the construct. If do\_not\_synchronize evaluates to false, the efect is as if the nogroup clause is not specified on the directive. If do\_not\_synchronize is not specified, the efect is as if do\_not\_synchronize evaluates to true.

## Cross References

• target\_data Construct, see Section 15.7

• taskgraph Construct, see Section 14.3

• taskloop Construct, see Section 14.2

# 17.8 OpenMP Memory Ordering

This sections describes constructs and clauses that support ordering of memory operations.

## 17.8.1 memory-order Clauses

## Clause groups

<table><tr><td>Properties: exclusive, unique</td><td>Members:Clausesacq_rel, acquire, relaxed, release, seq_cst</td></tr></table>

## Directives

atomic, flush

## Semantics

The memory-order clause group defines a set of clauses that indicate the memory ordering requirements for the visibility of the efects of the constructs on which they may be specified.

## Cross References

• atomic Construct, see Section 17.8.5

• flush Construct, see Section 17.8.6

• OpenMP Memory Consistency, see Section 1.3.6

## 17.8.1.1 acq\_rel Clause

<table><tr><td>Name: acq_rel</td><td>Properties: unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>use-semantics</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

atomic, flush

## Semantics

If use\_semantics evaluates to true, the acq\_rel clause specifies for the construct to use acquire/release memory ordering semantics. If use\_semantics evaluates to false, the efect is as if the acq\_rel clause is not specified. If use\_semantics is not specified, the efect is as if use\_semantics evaluates to true.

## Cross References

• atomic Construct, see Section 17.8.5

• flush Construct, see Section 17.8.6

• OpenMP Memory Consistency, see Section 1.3.6

## 17.8.1.2 acquire Clause

<table><tr><td colspan="2">Name: acquire</td><td colspan="2">Properties: unique</td></tr><tr><td colspan="4">Arguments</td></tr><tr><td>Name</td><td colspan="2">Type</td><td>Properties</td></tr><tr><td>use_semantics</td><td colspan="2">expression of OpenMP logical type</td><td>constant, optional</td></tr><tr><td colspan="4">Modifiers</td></tr><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

atomic, flush

## Semantics

If use\_semantics evaluates to true, the acquire clause specifies for the construct to use acquire memory ordering semantics. If use\_semantics evaluates to false, the efect is as if the acquire clause is not specified. If use\_semantics is not specified, the efect is as if use\_semantics evaluates to true.

## Cross References

• atomic Construct, see Section 17.8.5

• flush Construct, see Section 17.8.6

• OpenMP Memory Consistency, see Section 1.3.6

Arguments  
Modifiers  
17.8.1.3 relaxed Clause

<table><tr><td>Name: relaxed</td><td>Properties: unique</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>use_semantics</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

atomic, flush

## Semantics

If use\_semantics evaluates to true, the relaxed clause specifies for the construct to use relaxed memory ordering semantics. If use\_semantics evaluates to false, the efect is as if the relaxed clause is not specified. If use\_semantics is not specified, the efect is as if use\_semantics evaluates to true.

## Cross References

• atomic Construct, see Section 17.8.5

• flush Construct, see Section 17.8.6

• OpenMP Memory Consistency, see Section 1.3.6

## 17.8.1.4 release Clause

<table><tr><td>Name: release</td><td>Properties: unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>use_semantics</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

atomic, flush

## Semantics

If use\_semantics evaluates to true, the release clause specifies for the construct to use release memory ordering semantics. If use\_semantics evaluates to false, the efect is as if the release clause is not specified. If use\_semantics is not specified, the efect is as if use\_semantics evaluates to true.

## Cross References

• atomic Construct, see Section 17.8.5

• flush Construct, see Section 17.8.6

• OpenMP Memory Consistency, see Section 1.3.6

## 17.8.1.5 seq\_cst Clause

<table><tr><td colspan="2">Name: seq_cst</td><td colspan="2">Properties: unique</td></tr><tr><td colspan="4">Arguments</td></tr><tr><td>Name</td><td colspan="2">Type</td><td>Properties</td></tr><tr><td>use_semantics</td><td colspan="2">expression of OpenMP logical type</td><td>constant, optional</td></tr><tr><td colspan="4">Modifiers</td></tr><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

atomic, flush

## Semantics

If use\_semantics evaluates to true, the seq\_cst clause specifies for the construct to use sequentially consistent memory ordering semantics. If use\_semantics evaluates to false, the efect is as if the seq\_cst clause is not specified. If use\_semantics is not specified, the efect is as if use\_semantics evaluates to true.

## Cross References

• atomic Construct, see Section 17.8.5

• flush Construct, see Section 17.8.6

• OpenMP Memory Consistency, see Section 1.3.6

## 17.8.2 atomic Clauses

## Clause groups

<table><tr><td>Properties: exclusive, unique</td><td>Members:Clausesread, update, write</td></tr></table>

## Directives

atomic

## Semantics

The atomic clause group defines a set of clauses that defines the semantics for which a directive enforces atomicity. If a construct accepts the atomic clause group and no member of the clause group is specified, the efect is as if the update clause is specified.

## Cross References

• atomic Construct, see Section 17.8.5

## 17.8.2.1 read Clause

<table><tr><td>Name: read</td><td>Properties: innermost-leaf, unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>use_semantics</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

atomic

## Semantics

If use\_semantics evaluates to true, the read clause specifies that the atomic construct has atomic read semantics, which read the value of the shared variable atomically. If use\_semantics evaluates to false, the efect is as if the read clause is not specified. If use\_semantics is not specified, the efect is as if use\_semantics evaluates to true.

## Cross References

• atomic Construct, see Section 17.8.5

17.8.2.2 update Clause

<table><tr><td>Name: update</td><td>Properties: innermost-leaf, unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>use_semantics</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

atomic

## Semantics

If use\_semantics evaluates to true, the update clause specifies that the atomic construct has atomic update semantics, which read and write the value of the shared variable atomically. If use\_semantics evaluates to false, the efect is as if the update clause is not specified. If use\_semantics is not specified, the efect is as if use\_semantics evaluates to true.

## Cross References

• atomic Construct, see Section 17.8.5

## 17.8.2.3 write Clause

<table><tr><td>Name: write</td><td>Properties: innermost-leaf, unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>use_semantics</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

atomic

## Semantics

If use\_semantics evaluates to true, the write clause specifies that the atomic construct has atomic write semantics, which write the value of the shared variable atomically. If use\_semantics evaluates to false, the efect is as if the write clause is not specified. If use\_semantics is not specified, the efect is as if use\_semantics evaluates to true.

Cross References

• atomic Construct, see Section 17.8.5

## 17.8.3 extended-atomic Clauses

## Clause groups

<table><tr><td>Properties: unique</td><td>Members:Clausescapture, compare, fail, weak</td></tr></table>

## Directives

atomic

## Semantics

The extended-atomic clause group defines a set of clauses that extend the atomicity semantics specified by members of the atomic clause group.

## Restrictions

Restrictions to the extended-atomic clause group are as follows:

• The compare clause may not be specified such that use\_semantics evaluates to false if the weak clause is specified such that use\_semantics evaluates to true.

## Cross References

• atomic Construct, see Section 17.8.5

• atomic Clauses, see Section 17.8.2

## 17.8.3.1 capture Clause

<table><tr><td>Name: capture</td><td>Properties: innermost-leaf, unique</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>use_semantics</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

Arguments  
Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

atomic

## Semantics

If use\_semantics evaluates to true, the capture clause extends the semantics of the atomic construct to have atomic captured update semantics, which capture the value of the shared variable being updated atomically. If use\_semantics evaluates to false, the value is not captured. If use\_semantics is not specified, the efect is as if use\_semantics evaluates to true.

## Cross References

• atomic Construct, see Section 17.8.5

## 17.8.3.2 compare Clause

<table><tr><td>Name: compare</td><td>Properties: innermost-leaf, unique</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>use_semantics</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

atomic

## Semantics

If use\_semantics evaluates to true, the compare clause extends the semantics of the atomic construct with atomic conditional update semantics so the atomic update is performed conditionally. If use\_semantics evaluates to false, the atomic update is performed unconditionally. If use\_semantics is not specified, the efect is as if use\_semantics evaluates to true.

## Cross References

• atomic Construct, see Section 17.8.5

Arguments  
17.8.3.3 fail Clause

<table><tr><td>Name: fail</td><td>Properties: innermost-leaf, unique</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>memorder</td><td>Keyword: acquire, relaxed, seq_cst</td><td>default</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

atomic

## Semantics

The fail clause extends the semantics of the atomic construct to specify the memory ordering requirements for any comparison performed by any atomic conditional update that fails. Its argument overrides any other specified memory ordering. If an atomic construct has atomic conditional update semantics and the fail clause is not specified, the efect is as if the fail clause is specified with a default argument that depends on the efective memory ordering. If the efective memory ordering is acq\_rel, the default argument is acquire. If the efective memory ordering is release, the default argument is relaxed. For any other efective memory ordering, the default argument is equal to that efective memory ordering. If the atomic construct does not have atomic conditional update semantics, the fail clause has no efect.

## Restrictions

Restrictions to the fail clause are as follows:

• memorder may not be acq\_rel or release.

## Cross References

• atomic Construct, see Section 17.8.5

• memory-order Clauses, see Section 17.8.1

## 17.8.3.4 weak Clause

<table><tr><td>Name: weak</td><td>Properties: innermost-leaf, unique</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>use_semantics</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

atomic

## Semantics

If use\_semantics evaluates to true, the weak clause has the same efect as the compare clause and, in addition, the atomic construct has weak comparison semantics, which mean that the comparison may spuriously fail, evaluating to not equal even when the values are equal. If use\_semantics evaluates to false, the semantics of the atomic construct are not extended. If use\_semantics is not specified, the efect is as if use\_semantics evaluates to true.

Note – Allowing for spurious failure by specifying a weak clause can result in performance gains on some systems when using compare-and-swap in a loop. For cases where a single compare-and-swap would otherwise be suficient, using a loop over a weak compare-and-swap is unlikely to improve performance.

## Cross References

• atomic Construct, see Section 17.8.5

## 17.8.4 memscope Clause

<table><tr><td>Name: memscope</td><td>Properties: unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>scope-specifier</td><td>Keyword: all, cgroup, device</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

atomic, flush

## Semantics

The memscope clause determines the binding thread set of the region that corresponds to the construct on which it is specified.

If the scope-specifier is device, the binding thread set consists of all threads on the device. If the scope-specifier is cgroup, the binding thread set consists of all threads that are executing tasks in the contention group. If the scope-specifier is all, the binding thread set consists of all threads on all devices.

Unless otherwise stated, the thread-set of any flushes that are performed in an atomic or flush region is the same as the binding thread set of the region, as determined by the memscope clause.

## Restrictions

The restrictions for the memscope clause are as follows:

• The binding thread set defined by the scope-specifier of the memscope clause on an atomic construct must be a subset of the atomic scope of the atomically accessed memory.

• The binding thread set defined by the scope-specifier of the memscope clause on an atomic construct must be a subset of all threads that are executing tasks in the contention group if the size of the atomically accessed storage location is not 8, 16, 32, or 64 bits.

## Cross References

• atomic Construct, see Section 17.8.5

• flush Construct, see Section 17.8.6

## 17.8.5 atomic Construct
