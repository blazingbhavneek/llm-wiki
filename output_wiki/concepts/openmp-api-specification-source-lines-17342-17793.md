# OpenMP-API-Specification Source Lines 17342-17793

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source OpenMP-API-Specification:L17342-L17793

Citation: [OpenMP-API-Specification:L17342-L17793]

````text
## Fortran

When an internal procedure is called in a target region, any references to variables that are host associated in the procedure have unspecified behavior.

Fortran

## Execution Model Events

Events associated with a target task are the same as for the task construct defined in Section 14.1. Events associated with the initial task that executes the target region are defined in Section 14.13. The target-submit-begin event occurs prior to initiating creation of an initial task on a target device for a target region. The target-submit-end event occurs after initiating creation of an initial task on a target device for a target region. The target-begin event occurs after creation of the target task and completion of all predecessor tasks that are not target tasks for the same device. The target-begin event is a target-task-begin event. The target-end event occurs after the target-submit-begin, target-submit-end and target-begin events associated with the target construct and any events associated with map clauses on the construct. If the nowait clause is not present, the target-end event also occurs after all events associated with the target task and initial task but before the thread resumes execution of the encountering task.

## Tool Callbacks

Callbacks associated with events for target tasks are the same as for the task construct defined in Section 14.1; (flags & ompt\_task\_target) always evaluates to true in the dispatched callback.

A thread dispatches a registered target\_emi callback with ompt\_scope\_begin as its endpoint argument and ompt\_target or ompt\_target\_nowait if the nowait clause is present as its kind argument for each occurrence of a target-begin event in that thread in the context of the target task on the host device. Similarly, a thread dispatches a registered target\_emi callback with ompt\_scope\_end as its endpoint argument and ompt\_target or ompt\_target\_nowait if the nowait clause is present as its kind argument for each occurrence of a target-end event in that thread in the context of the target task on the host device.

A thread dispatches a registered target\_submit\_emi callback with ompt\_scope\_begin as its endpoint argument for each occurrence of a target-submit-begin event in that thread. Similarly, a thread dispatches a registered target\_submit\_emi callback with ompt\_scope\_end as its endpoint argument for each occurrence of a target-submit-end event in that thread. These callback occur in the context of the target task.

## Restrictions

Restrictions to the target construct are as follows:

• Device-afecting constructs, other than target constructs for which the ancestor device-modifier is specified, must not be encountered during execution of a target region.

• The result of an omp\_set\_default\_device, omp\_get\_default\_device, or omp\_get\_num\_devices routine called within a target region is unspecified.

• The efect of an access to a threadprivate variable in a target region is unspecified.

• If a list item in a map clause is a structure element, any other element of that structure that is referenced in the target construct must also appear as a list item in a map clause.

• A list item in a map clause that is specified on a target construct must have a base variable or base pointer.

• A list item in a data-sharing attribute clause that is specified on a target construct must not have the same base variable as a list item in a map clause on the construct.

• A variable referenced in a target region but not the target construct that is not declared in the target region must appear in a declare target directive.

• If a device clause is specified with the ancestor device-modifier, only the device, firstprivate, private, defaultmap, nowait, and map clauses may appear on the construct and no constructs or calls to routines are allowed inside the corresponding target region.

• If a device clause is specified with the ancestor device-modifier, whether a storage block on the encountering device that has no corresponding storage on the specified device may be mapped is implementation defined.

• Memory allocators that do not appear in a uses\_allocators clause cannot appear as an allocator in an allocate clause or be used in the target region unless a requires directive with the dynamic\_allocators clause is present in the same compilation unit.

• Any IEEE floating-point exception status flag, halting mode, or rounding mode set prior to a target region is unspecified in the region.

• Any IEEE floating-point exception status flag, halting mode, or rounding mode set in a target region is unspecified upon exiting the region.

• An OpenMP program must not rely on the value of a function address in a target region except for assignments, pointer association queries, and indirect calls.

C / C++

• Upon exit from a target region, the value of an attached pointer must not be diferent from the value when entering the region.

C / C++

C++

• The run-time type information (RTTI) of an object can only be accessed from the device on which it was constructed.

• Invoking a virtual member function of an object on a device other than the device on which the object was constructed results in unspecified behavior, unless the object is accessible and was constructed on the host device.

• If an object of polymorphic class type is destructed, virtual member functions of any previously existing corresponding objects in other device data environments must not be invoked.

C++

Fortran

• An attached pointer that is associated with a given pointer target must not be associated with a diferent pointer target upon exit from a target region.

• A reference to a coarray that is encountered on a non-host device must not be coindexed or appear as an actual argument to a procedure where the corresponding dummy argument is a coarray.

• If the allocation status of a mapped variable or a list item that appears in a has\_device\_addr clause that has the ALLOCATABLE attribute is unallocated on entry to a target region, the allocation status of the corresponding variable in the device data environment must be unallocated upon exiting the region.

• If the allocation status of a mapped variable or a list item that appears in a has\_device\_addr clause that has the ALLOCATABLE attribute is allocated on entry to a target region, the allocation status and shape of the corresponding variable in the device data environment may not be changed, either explicitly or implicitly, in the region after entry to it.

• If the association status of a list item with the POINTER attribute that appears in a map or has\_device\_addr clause on the construct is disassociated upon entry to the target region, the list item must be disassociated upon exit from the region.

• If the association status of a list item with the POINTER attribute that appears in a map or has\_device\_addr clause on the construct is associated upon entry to the target region, the list item must be associated with the same pointer target upon exit from the region.

• An OpenMP program must not rely on the association status of a procedure pointer in a target region except for calls to the ASSOCIATED inquiry function without the optional proc-target argument, pointer assignments and indirect calls.

Fortran

## Cross References

• allocate Clause, see Section 8.6

• default Clause, see Section 7.5.1

• defaultmap Clause, see Section 7.9.9

• depend Clause, see Section 17.9.5

• device Clause, see Section 15.2

• device\_type Clause, see Section 15.1

• firstprivate Clause, see Section 7.5.4

• has\_device\_addr Clause, see Section 7.5.9

• if Clause, see Section 5.5

• in\_reduction Clause, see Section 7.6.12

• is\_device\_ptr Clause, see Section 7.5.7

• map Clause, see Section 7.9.6

• nowait Clause, see Section 17.6

• priority Clause, see Section 14.9

• private Clause, see Section 7.5.3

• replayable Clause, see Section 14.6

• OMPT scope\_endpoint Type, see Section 33.27

• OMPT target Type, see Section 33.34

• target\_data Construct, see Section 15.7

• target\_emi Callback, see Section 35.8

• target\_submit\_emi Callback, see Section 35.10

• task Construct, see Section 14.1

• OMPT task\_flag Type, see Section 33.37

• thread\_limit Clause, see Section 15.3

• uses\_allocators Clause, see Section 8.8

## 15.9 target\_update Construct

<table><tr><td>Name: target_updateCategory: executable</td><td>Association: unassociatedProperties: parallelism-generating, task-generating, device, device-affecting</td></tr></table>

## Clauses

depend, device, from, if, nowait, priority, replayable, to

## Clause set

<table><tr><td>Properties: required</td><td>Members: from, to</td></tr></table>

## Additional information

The target\_update directive may alternatively be specified with target update as the directive-name.

## Binding

The binding task set for a target\_update region is the generating task, which is the target task generated by the target\_update construct. The target\_update region binds to the corresponding target task region.

## Semantics

The target\_update directive makes the corresponding list items in the device data environment consistent with their original list items, according to the specified data-motion clauses. The target\_update construct generates a target task. The generated task region encloses the target\_update region. If a depend clause is present, it is associated with the target task. If the nowait clause is present, execution of the target task may be deferred. If the nowait clause is not present, the target task is an included task.

All clauses are evaluated when the target\_update construct is encountered. The data environment of the target task is created according to data-motion clauses on the target\_update construct, ICVs with data environment ICV scope, and any default data-sharing attribute rules that apply to the target\_update construct. If a variable or part of a variable is a list item in a data-motion clause on the target\_update construct, the variable has a default data-sharing attribute of shared in the data environment of the target task.

Assignment operations associated with any data-motion clauses occur when the target task executes. When an if clause is present and if-expression evaluates to false, no assignments occur.

## Execution Model Events

Events associated with a target task are the same as for the task construct defined in Section 14.1.

The target-update-begin event occurs after creation of the target task and completion of al predecessor tasks that are not target tasks for the same device. The target-update-end event occurs after all other events associated with the target\_update construct.

The target-data-op-begin event occurs in the target\_update region before a thread initiates a data operation on the target device. The target-data-op-end event occurs in the target\_update region after a thread initiates a data operation on the target device.

## Tool Callbacks

Callbacks associated with events for target tasks are the same as for the task construct defined in Section 14.1; (flags & ompt\_task\_target) always evaluates to true in the dispatched callback.

A thread dispatches a registered target\_emi callback with ompt\_scope\_begin as its endpoint argument and ompt\_target\_update or ompt\_target\_update\_nowait if the nowait clause is present as its kind argument for each occurrence of a target-update-begin event in that thread in the context of the target task on the host device. Similarly, a thread dispatches a registered target\_emi callback with ompt\_scope\_end as its endpoint argument and ompt\_target\_update or ompt\_target\_update\_nowait if the nowait clause is present as its kind argument for each occurrence of a target-update-end event in that thread in the context of the target task on the host device.

A thread dispatches a registered target\_data\_op\_emi callback with ompt\_scope\_begin as its endpoint argument for each occurrence of a target-data-op-begin event in that thread. Similarly, a thread dispatches a registered target\_data\_op\_emi callback with ompt\_scope\_end as its endpoint argument for each occurrence of a target-data-op-end event in that thread. These callbacks occur in the context of the target task.

## Cross References

• depend Clause, see Section 17.9.5

• device Clause, see Section 15.2

• from Clause, see Section 7.10.2

• if Clause, see Section 5.5

• nowait Clause, see Section 17.6

• priority Clause, see Section 14.9

• replayable Clause, see Section 14.6

• OMPT scope\_endpoint Type, see Section 33.27

• OMPT target Type, see Section 33.34

• target\_data\_op\_emi Callback, see Section 35.7

• target\_emi Callback, see Section 35.8

• task Construct, see Section 14.1

• OMPT task\_flag Type, see Section 33.37

• to Clause, see Section 7.10.1

## 16 Interoperability

An OpenMP implementation may interoperate with one or more foreign runtime environments through the use of the interop construct that is described in this chapter, the interop operation for a declared function variant and the interoperability routines.

## Cross References

• Interoperability Routines, see Chapter 26

## 16.1 interop Construct

<table><tr><td>Name: interopCategory: executable</td><td>Association: unassociatedProperties: device</td></tr></table>

## Clauses

depend, destroy, device, init, nowait, use

## Clause set

action-clause

<table><tr><td>Properties: required</td><td>Members: destroy, init, use</td></tr></table>

## Binding

The binding task set for an interop region is the generating task. The interop region binds to the region of the generating task.

## Semantics

The interop construct retrieves interoperability properties from the OpenMP implementation to enable interoperability with foreign execution contexts. When an interop construct is encountered, the encountering task executes the region.

The interop-type set for an init clause is the set of specified interop-type modifiers. For any other action-clause and the interoperability object that its argument specifies, the interop-type set is the set of modifiers that were specified by the init clause that initialized that interoperability object.

If the interop-type set includes targetsync, an empty mergeable task is generated. If the nowait clause is not present on the construct then the task is also an included task. If the interop-type set does not include targetsync, the nowait clause has no efect. Any depend clauses that are present on the construct apply to the generated task.

The interop construct ensures an ordered execution of the generated task relative to foreign tasks executed in the foreign execution context through the foreign synchronization object that is accessible through the targetsync property. When the creation of the foreign task precedes the encountering of an interop construct in happens-before order, the foreign task must complete execution before the generated task begins execution. Similarly, when the creation of a foreign task follows the encountering of an interop construct in between the encountering thread and either foreign tasks or OpenMP tasks by the interop construct.

## Restrictions

Restrictions to the interop construct are as follows:

• A depend clause must only appear on the directive if the interop-type includes targetsync.

• An interoperability object must not be specified in more than one action-clause that appears on the interop construct.

## Cross References

• depend Clause, see Section 17.9.5

• destroy Clause, see Section 5.7

• device Clause, see Section 15.2

• init Clause, see Section 5.6

• nowait Clause, see Section 17.6

• use Clause, see Section 16.1.2

## 16.1.1 OpenMP Foreign Runtime Identifiers

Allowed values for foreign runtime identifiers include the names (as string literals) and integer values that the OpenMP Additional Definitions document specifies and the corresponding omp\_ifr\_name values of the interop\_fr OpenMP type. Implementation defined values for foreign runtime identifiers may also be supported.

## 16.1.2 use Clause

<table><tr><td>Name: use</td><td>Properties: default</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td> $\text{interop-var}$ </td><td>variable of interopOpenMP type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

interop

## Semantics

The use clause specifies the interop-var that is used for the efects of the directive on which the clause appears. However, interop-var is not initialized, destroyed or otherwise modified. The interop-type set is inferred based on the interop-type modifiers used to initialize interop-var.

## Restrictions

• The state of interop-var must be initialized.

## Cross References

• interop Construct, see Section 16.1

## 16.1.3 prefer-type Modifier

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>prefer-type</td><td>init-var</td><td>Complex, name: prefer_typeArguments: prefer-type-specification list of preference spec- ification list item type (default)</td><td>complex, unique</td></tr></table>

## Clauses

init

## Semantics

The prefer-type modifier specifies a set of preferences to be used to initialize an interoperability object. Each preference specification list item specified in the prefer-type-specification argument is a preference specification that has the following syntax:

preference-specification:

{preference-selector[, preference-selector[, ...]]}

foreign-runtime-identifier

preference-selector:

fr(foreign-runtime-identifier)

attr(preference-property-extension[, preference-property-extension[, ...]])

preference-property-extension: ext-string-literal

Where foreign-runtime-identifier is a foreign runtime identifier and an implementation defined ext-string-literal is a string literal that must start with the ompx\_ prefix and must not include any commas (i.e., instances of the character ’,’).

The fr preference-selector specifies a foreign runtime environment identified by its foreign runtime identifier. The attr preference-selector specifies a preference for the attributes specified as its arguments.

If a preference-specification is a foreign-runtime-identifier, it is equivalent to specifying a preference-specification that uses the fr preference-selector and the foreign runtime identifier as its argument.

The interoperability object specified by the init-var argument of the init clause is initialized based on the first supported preference specification, if any, in left-to-right order. If the implementation does not support any of the specified preference specifications, init-var is initialized based on an implementation defined preference specification.

## Restrictions

Restrictions to the prefer-type modifier are as follows:

• At most one fr preference-selector may be specified for each preference-specification.

## Cross References

• init Clause, see Section 5.6

# 17 Synchronization Constructs and Clauses

A synchronization construct imposes an order on the completion of code executed by diferent threads through synchronizing flushes that are executed as part of the region that corresponds to the construct. Section 1.3.4 and Section 1.3.6 describe synchronization through the use of synchronizing flushes and atomic operations. Section 17.8.7 defines the behavior of synchronizing flushes that are implied at various other locations in an OpenMP program.

## 17.1 hint Clause

Modifiers

<table><tr><td>Name: hint</td><td>Properties: unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>hint-expr</td><td>expression of sync_hint type</td><td>default</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

atomic, critical

## Semantics

The hint clause gives the implementation additional information about the expected runtime properties of the region that corresponds to the construct on which it appears and that can optionally be used to optimize the implementation. The presence of a hint clause does not afect the semantics of the construct. If no hint clause is specified for a construct that accepts it, the efect is as if omp\_sync\_hint\_none had been specified as hint-expr.

## Restrictions

• hint-expr must evaluate to a valid synchronization hint.

## Cross References

• atomic Construct, see Section 17.8.5

• critical Construct, see Section 17.2

• OpenMP sync\_hint Type, see Section 20.9.5

## 17.2 critical Construct

<table><tr><td>Name: criticalCategory:executable</td><td>Association: blockProperties: mutual-exclusion, thread-limiting, thread-exclusive</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>name</td><td>base language identifier</td><td>optional</td></tr></table>

## Clauses

hint

## Binding

The binding thread set for a critical region is all threads executing tasks in the contention group.

## Semantics

The name argument is used to identify the critical construct. For any critical construct for which name is not specified, the efect is as if an identical (unspecified) name was specified. The regions that correspond to any critical construct of a given name are executed as if only by a single thread at a time among all threads associated with the contention group that execute the regions, without regard to the teams to which the threads belong.

C / C++

Identifiers used to identify a critical construct have external linkage and are in a name space that is separate from the name spaces used by labels, tags, members, and ordinary identifiers.

C / C++

Fortran

The names of critical constructs are global entities of the OpenMP program. If a name conflicts with any other entity, the behavior of the program is unspecified.

Fortran

## Execution Model Events

The critical-acquiring event occurs in a thread that encounters the critical construct on entry to the critical region before initiating synchronization for the region. The critical-acquired event occurs in a thread that encounters the critical construct after it enters the region, but before it executes the structured block of the critical region. The critical-released event occurs in a thread that encounters the critical construct after it completes any synchronization on exit from the critical region.

## Tool Callbacks

A thread dispatches a registered mutex\_acquire callback for each occurrence of a critical-acquiring event in that thread. A thread dispatches a registered mutex\_acquired callback for each occurrence of a critical-acquired event in that thread. A thread dispatches a registered mutex\_released callback for each occurrence of a critical-released event in that thread. These callbacks occur in the task that encounters the critical construct. The callbacks should receive ompt\_mutex\_critical as their kind argument if practical, but a less specific kind is acceptable.

## Restrictions

Restrictions to the critical construct are as follows:

• Unless omp\_sync\_hint\_none is specified in a hint clause, the critical construct must specify a name.

• The hint-expr that is specified in the hint clause on each critical construct with the same name must evaluate to the same value.

• A critical region must not be nested (closely or otherwise) inside a critical region with the same name. This restriction is not suficient to prevent deadlock.

## Fortran

• If a name is specified on a critical directive and a paired end directive is specified, the same name must also be specified on the end directive.

• If no name appears on the critical directive and a paired end directive is specified, no name can appear on the end directive.

## Fortran

## Cross References

• hint Clause, see Section 17.1

• OMPT mutex Type, see Section 33.20

• mutex\_acquire Callback, see Section 34.7.8

• mutex\_acquired Callback, see Section 34.7.12

• mutex\_released Callback, see Section 34.7.13

• OpenMP sync\_hint Type, see Section 20.9.5
````
