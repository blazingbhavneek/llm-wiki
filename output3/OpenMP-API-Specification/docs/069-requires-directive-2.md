## 10.5 requires Directive

<table><tr><td>Name: requiresCategory: informational</td><td>Association: unassociatedProperties: default</td></tr></table>

## Clause groups

requirement

## Semantics

The requires directive specifies features that an implementation must support for correct execution and requirements for the execution of all code in the current compilation unit. The behavior that a requirement clause specifies may override the normal behavior specified elsewhere in this document. Whether an implementation supports the feature that a given requirement clause specifies is implementation defined.

The clauses of a requires directive are added to the requires trait in the OpenMP context for all program points that follow the directive.

## Restrictions

Restrictions to the requires directive are as follows:

• A requires directive must appear lexically after the specification of a context selector in which any clause of that requires directive is used, nor may the directive appear lexically after any code that depends on such a context selector.

• The requires directive must only appear at file scope.

C++

• The requires directive must only appear at file or namespace scope.

C++

C / C++

• Any requires directive that specifies a device global requirement clause must appear lexically before any device constructs or device procedures.

C / C++

## Fortran

• The requires directive must appear in the specification part of a program unit, either after all USE statements, IMPORT statements, and IMPLICIT statements or by referencing a module. Additionally, it may appear in the specification part of an internal or module subprogram that appears by referencing a module if each clause already appeared with the same arguments in the specification part of the program unit.

Fortran

## 10.5.1 requirement Clauses

## Clause groups

<table><tr><td>Properties: required, unique</td><td>Members:Clausesatomic_default_mem_order,device_safesync,dynamic_allocators,reverse_offload,self_maps,unified_address,unified_shared_memory</td></tr></table>

## Directives

## requires

## Semantics

The requirement clause group defines a clause set that indicates the requirements that a program requires the implementation to support. If an implementation supports a given requirement clause then the use of that clause on a requires directive will cause the implementation to ensure the enforcement of a guarantee represented by the specific member of the clause group. If the implementation does not support the requirement then it must perform compile-time error termination.

## Restrictions

• All compilation units of a program that contain declare target directives, device constructs or device procedures must specify the same set of requirements that are defined by clauses with the device global requirement property in the requirement clause group.

Cross References

• requires Directive, see Section 10.5

## 10.5.1.1 atomic\_default\_mem\_order Clause

<table><tr><td>Name: atomic_default_mem_order</td><td>Properties: unique</td></tr></table>

## Arguments

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>memory-order</td><td>Keyword: acq_rel, acquire, relaxed, release, seq_cst</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

requires

## Semantics

The atomic\_default\_mem\_order clause specifies the default memory ordering behavior for atomic constructs that an implementation must provide. The efect is as if its argument appears as a clause on any atomic construct that does not specify a memory-order clause.

## Restrictions

Restrictions to the atomic\_default\_mem\_order clause are as follows:

• All requires directives in the same compilation unit that specify the atomic\_default\_mem\_order requirement must specify the same argument.

• Any directive that specifies the atomic\_default\_mem\_order clause must not appear lexically after any atomic construct on which a memory-order clause is not specified.

## Cross References

• atomic Construct, see Section 17.8.5

• memory-order Clauses, see Section 17.8.1

• requires Directive, see Section 10.5

10.5.1.2 dynamic\_allocators Clause

<table><tr><td>Name: dynamic_allocators</td><td>Properties: unique</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>required</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

requires

## Semantics

If required evaluates to true, the dynamic\_allocators clause removes certain restrictions on the use of memory allocators in target regions. Specifically, allocators (including the default allocator that is specified by the def-allocator-var ICV) may be used in a target region or in an allocate clause on a target construct without specifying the uses\_allocators clause on the target construct. Additionally, the implementation must support calls to the omp\_init\_allocator and omp\_destroy\_allocator API routines in target regions. If required is not specified, the efect is as if required evaluates to true.

## Cross References

• allocate Clause, see Section 8.6

• def-allocator-var ICV, see Table 3.1

• omp\_destroy\_allocator Routine, see Section 27.7

• omp\_init\_allocator Routine, see Section 27.6

• requires Directive, see Section 10.5

• target Construct, see Section 15.8

• uses\_allocators Clause, see Section 8.8

## 10.5.1.3 reverse\_offload Clause

<table><tr><td>Name: reverse_offload</td><td>Properties: unique, device global requirement</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>required</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

## Semantics

If required evaluates to true, the reverse\_offload clause requires an implementation to guarantee that if a target construct specifies a device clause in which the ancestor device-modifier appears, the target region can execute on the parent device of an enclosing target region. If required is not specified, the efect is as if required evaluates to true.

## Cross References

• device Clause, see Section 15.2

• requires Directive, see Section 10.5

• target Construct, see Section 15.8

## 10.5.1.4 unified\_address Clause

<table><tr><td>Name: unified_address</td><td>Properties: unique, device global requirement</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>required</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

requires

## Semantics

If required evaluates to true, the unified\_address clause requires an implementation to guarantee that all devices accessible through OpenMP API routines and directives use a unified address space. In this address space, a pointer will always refer to the same location in memory from all devices accessible through OpenMP. Any OpenMP mechanism that returns a device pointer is guaranteed to return a device address that supports pointer arithmetic, and the is\_device\_ptr clause is not necessary to obtain device addresses from device pointers for use inside target regions. Host pointers may be passed as device pointer arguments to device memory routines and device pointers may be passed as host pointer arguments to device memory routines. Non-host devices may still have discrete memories and dereferencing a device pointer on the host device or a host pointer on a non-host device remains unspecified behavior. Memory local to a specific execution context may be exempt from the unified\_address requirement, following the restrictions of locality to a given execution context, thread or contention group. If required is not specified, the efect is as if required evaluates to true.

## Cross References

• is\_device\_ptr Clause, see Section 7.5.7

• requires Directive, see Section 10.5

• target Construct, see Section 15.8

## 10.5.1.5 unified\_shared\_memory Clause

<table><tr><td>Name: unified_shared_memory</td><td>Properties: unique, device global requirement</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>required</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

## requires

## Semantics

If required evaluates to true, the unified\_shared\_memory clause requires the implementation to guarantee that all devices share memory that is generally accessible to all threads.

The unified\_shared\_memory clause implies the unified\_address requirement, inheriting all of its behaviors.

The implementation must guarantee that storage locations in memory are accessible to threads on all accessible devices, except for memory that is local to a specific execution context and exempt from the unified\_address requirement (see Section 10.5.1.4). Every device address that refers to storage allocated through OpenMP API routines is a valid host pointer that may be dereferenced and may be used as a host address. Values stored into memory by one device may not be visible to another device until synchronization establishes a happens-before order between the memory accesses.

The use of declare target directives in an OpenMP program is optional for referencing variables with static storage duration in device procedures.

Any data object that results from the declaration of a variable that has static storage duration is treated as if it is mapped with a persistent self map at the beginning of the program to the device data environments of all target devices if:

• The variable is not a device-local variable;

• The variable is not listed in an enter clause on a declare target directive; and

• The variable is referenced in a device procedure.

If required is not specified, the efect is as if required evaluates to true.

## Cross References

• enter Clause, see Section 7.9.7

• requires Directive, see Section 10.5

• unified\_address Clause, see Section 10.5.1.4

## 10.5.1.6 self\_maps Clause

<table><tr><td>Name: self_maps</td><td>Properties: unique, device global requirement</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>required</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

## requires

## Semantics

If required evaluates to true, the self\_maps clause implies the unified\_shared\_memory clause, inheriting all of its behaviors. Additionally, map-entering clauses in the compilation unit behave as if all resulting mapping operations are self maps, and all corresponding list items created by the enter clauses specified by declare target directives in the compilation unit share storage with the original list items. If required is not specified, the efect is as if required evaluates to true.

## Cross References

• enter Clause, see Section 7.9.7

• requires Directive, see Section 10.5

• unified\_shared\_memory Clause, see Section 10.5.1.5

## 10.5.1.7 device\_safesync Clause

<table><tr><td>Name: device_safesync</td><td>Properties: unique, device global requirement</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>required</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

## requires

## Semantics

If required evaluates to true, the device\_safesync clause indicates that any two synchronizing divergent threads in a team that execute on a non-host device must be able to make progress, unless indicated otherwise by the use of a safesync clause. If required is not specified, the efect is as if required evaluates to true.

## Cross References

• requires Directive, see Section 10.5

• safesync Clause, see Section 12.1.5
