# OpenMP-API-Specification Source Lines 13361-13864

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source OpenMP-API-Specification:L13361-L13864

Citation: [OpenMP-API-Specification:L13361-L13864]

````text
## 9.9.3 indirect Clause

<table><tr><td>Name: indirect</td><td>Properties: unique</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>invoked-by-fptr</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

begin declare\_target, declare\_target

## Semantics

If invoked-by-fptr evaluates to true, any procedures that appear in an enter clause on the directive on which the indirect clause is specified may be called with an indirect device invocation. If the invoked-by-fptr does not evaluate to true, any procedures that appear in an enter clause on the directive may not be called with an indirect device invocation. Unless otherwise specified by an indirect clause, procedures may not be called with an indirect device invocation. If the indirect clause is specified and invoked-by-fptr is not specified, the efect of the clause is as if invoked-by-fptr evaluates to true.

## C / C++

If a procedure appears in the implicit enter clause of a begin declare\_target directive and in the enter clause of a declare target directive that is contained in the delimited code region of the begin declare\_target directive, and if an indirect clause appears on both directives, then the indirect clause on the begin declare\_target directive has no efect or that procedure.

![](images/301363971646706b660c4cf1543545c48decb5b16ed657ee60f47097fbf4cc4d.jpg)

## Restrictions

Restrictions to the indirect clause are as follows:

• If invoked-by-fptr evaluates to true, a device\_type clause must not appear on the same directive unless it specifies any for its device-type-description.

## Cross References

• begin declare\_target Directive, see Section 9.9.2

• declare\_target Directive, see Section 9.9.1

# 10 Informational and Utility Directives

An informational directive conveys information about code properties to the compiler while a utility directive facilitates interactions with the compiler or supports code readability. A utility directive is informational unless the at clause implies it is an executable directive.

## 10.1 error Directive

<table><tr><td>Name: errorCategory: utility</td><td>Association: unassociatedProperties: pure</td></tr></table>

## Clauses

at, message, severity

## Semantics

The error directive instructs the compiler or runtime to perform an error action. The error action displays an implementation defined message. The severity clause determines whether the error action is abortive following the display of the message. If sev-level is fatal and the action-time of the at clause is compilation, the message is displayed and compilation of the current compilation unit is aborted. If sev-level is fatal and action-time is execution, the message is displayed and program execution is aborted.

## Execution Model Events

The runtime-error event occurs when a thread encounters an error directive for which the at clause specifies execution.

## Tool Callbacks

A thread dispatches a registered error callback for each occurrence of a runtime-error event in the context of the encountering task.

## Restrictions

Restrictions to the error directive are as follows:

• The directive is pure only if action-time is compilation.

## Cross References

• at Clause, see Section 10.2

• error Callback, see Section 34.2

• message Clause, see Section 10.3

• severity Clause, see Section 10.4

## 10.2 at Clause

<table><tr><td>Name: at</td><td>Properties: unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>action-time</td><td>Keyword:compilation,execution</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

## error

## Semantics

The at clause determines when the implementation performs an action that is associated with a utility directive. If action-time is compilation, the action is performed during compilation if the directive appears in a declarative context or in an executable context that is reachable at runtime. If action-time is compilation and the directive appears in an executable context that is not reachable at runtime, the action may or may not be performed. If action-time is execution, the action is performed during program execution when a thread encounters the directive and the directive is considered to be an executable directive. If the at clause is not specified, the efect is as if action-time is compilation.

## Cross References

• error Directive, see Section 10.1

## 10.3 message Clause

<table><tr><td>Name: message</td><td>Properties: unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>msg-string</td><td>expression of string type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

error, parallel

## Semantics

The message clause specifies that msg-string is included in the implementation defined message that is associated with the directive on which the clause appears.

## Restrictions

• If the action-time is compilation, msg-string must be a constant expression.

## Cross References

• error Directive, see Section 10.1

• parallel Construct, see Section 12.1

## 10.4 severity Clause

<table><tr><td>Name: severity</td><td>Properties: unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>sev-level</td><td>Keyword: fatal, warning</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

error, parallel

## Semantics

The severity clause determines the action that the implementation performs if an error is encountered with respect to the directive on which the clause appears. If sev-level is warning, the implementation takes no action besides displaying the message that is associated with the directive. If sev-level is fatal, the implementation performs the abortive action associated with the directive on which the clause appears. If no severity clause is specified then the efect is as if sev-level is fatal.

## Cross References

• error Directive, see Section 10.1

• parallel Construct, see Section 12.1

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

## 10.6 Assumption Directives

Diferent assumption directives facilitate definition of assumptions for a scope that is appropriate to each base language. The assumption scope of a particular format is defined in the section that defines that directive. If the invariants specified by the assumption directive do not hold at runtime, the behavior is unspecified.

## 10.6.1 assumption Clauses

## Clause groups

<table><tr><td>Properties: required, unique</td><td>Members:Clausesabsent, contains, holds,no_openmp, no_openmp_constructs,no_openmp_routines, no_parallelism</td></tr></table>

## Directives

assume, assumes, begin assumes

## Semantics

The assumption clause group defines a clause set that indicates the invariants that a program ensures the implementation can exploit.

The absent and contains clauses accept a directive-name list that may match a construct that is encountered within the assumption scope. An encountered construct matches the directive name if it or one of its constituent constructs has the same directive-name as one of the list items.

## Restrictions

The restrictions to assumption clauses are as follows:

• A directive-name list item must not specify a directive that is a declarative directive, an informational directive, or a metadirective.

## Cross References

• assume Directive, see Section 10.6.3

• assumes Directive, see Section 10.6.2

• begin assumes Directive, see Section 10.6.4

## 10.6.1.1 absent Clause

<table><tr><td>Name: absent</td><td>Properties: unique</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-list</td><td>list of directive-name list item type</td><td>default</td></tr></table>

## Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

assume, assumes, begin assumes

## Semantics

The absent clause specifies that the program guarantees that no construct that matches a directive-name list item is encountered in the assumption scope.

## Cross References

• assume Directive, see Section 10.6.3

• assumes Directive, see Section 10.6.2

• begin assumes Directive, see Section 10.6.4
````
