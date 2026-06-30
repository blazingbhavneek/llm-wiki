# OpenMP-API-Specification Source Lines 9129-9830

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source OpenMP-API-Specification:L9129-L9830

Citation: [OpenMP-API-Specification:L9129-L9830]

````text
## Restrictions

Restrictions to the firstprivate clause are as follows:

• A list item that is private within a parallel region must not appear in a firstprivate clause on a worksharing construct if any of the worksharing regions that arise from the worksharing construct ever bind to any of the parallel regions that arise from the parallel construct.

• A list item that is private within a teams region must not appear in a firstprivate clause on a distribute construct if any of the distribute regions that arise from the distribute construct ever bind to any of the teams regions that arise from the teams construct.

• A list item that appears in a reduction clause on a parallel construct must not appear in a firstprivate clause on a task or taskloop construct if any of the task regions that arise from the task or taskloop construct ever bind to any of the parallel regions that arise from the parallel construct.

• A list item that appears in a reduction clause on a worksharing construct must not appear in a firstprivate clause on a task construct encountered during execution of any of the worksharing regions that arise from the worksharing construct.

C++

• A variable of class type (or array thereof) that appears in a firstprivate clause requires an accessible, unambiguous copy constructor for the class type.

• If the original list item in a firstprivate clause on a work-distribution construct has a reference type then it must bind to the same object for all threads in the binding thread set of the work-distribution region.

![](images/a34c5b571a5d7d370924aba110a3480405b7969a61b3a724deed30fddd570743.jpg)

## Cross References

• distribute Construct, see Section 13.7

• do Construct, see Section 13.6.2

• for Construct, see Section 13.6.1

• parallel Construct, see Section 12.1

• private Clause, see Section 7.5.3

• scope Construct, see Section 13.2

• sections Construct, see Section 13.3

• single Construct, see Section 13.1

• target Construct, see Section 15.8

• target\_data Construct, see Section 15.7

• task Construct, see Section 14.1

• taskloop Construct, see Section 14.2

• teams Construct, see Section 12.2

## 7.5.5 lastprivate Clause

<table><tr><td>Name: lastprivate</td><td>Properties: data-environment attribute, data-sharing attribute, original list-item updating, privatization</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>lastprivate-modifier</td><td>list</td><td>Keyword:conditional</td><td>default</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword:directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

distribute, do, for, loop, sections, simd, taskloop

## Semantics

The lastprivate clause provides a superset of the functionality provided by the private clause. A list item that appears in a lastprivate clause is subject to the private clause semantics described in Section 7.5.3. In addition, each new list item has the lastprivate attribute. Further, when a lastprivate clause without the conditional modifier appears on a directive and the list item is not a loop-iteration variable of any afected loop, the value of each new list item from the sequentially last iteration of the afected loops, or the lexically last structured block sequence associated with a sections construct, is assigned to the original list item. Alternatively, when the conditional modifier appears on the clause or the list item is a loop-iteration variable of one of the afected loops, if execution of the canonical loop nest, when it is not associated with a directive, would assign a value to the list item then the original list item is assigned that value.

For class types, the copy assignment operator is invoked. The order in which copy assignment operators for diferent variables of the same class type are invoked is unspecified.

C++ C / C++

For an array of elements of non-array type, each element is assigned to the corresponding element of the original array.

C / C++ Fortran

If the original list item does not have the POINTER attribute, its update occurs as if by intrinsic assignment unless it has a type bound procedure as a defined assignment.

If the original list item has the POINTER attribute, its update occurs as if by pointer assignment.

Fortran

When the conditional modifier does not appear on the lastprivate clause, any list item that is not a loop-iteration variable of the afected loops and that is not assigned a value by the sequentially last iteration of the loops, or by the lexically last structured block sequence associated with a sections construct, has an unspecified value after the construct. When the conditional modifier does not appear on the lastprivate clause, a list item that is the loop-iteration variable of an afected loop has an unspecified value after the construct if it would not be assigned a value during execution of the canonical loop nest when the loop nest is not associated with a directive. Unassigned subcomponents also have unspecified values after the construct.

If the lastprivate clause is used on a construct to which neither the nowait nor the nogroup clauses are applied, the original list item becomes defined at the end of the construct. Otherwise, if the lastprivate clause is used on a construct to which the nowait or the nogroup clauses are applied, accesses to the original list item may create a data race so if an assignment to the original list item occurs then other synchronization must ensure that the assignment completes and the original list item is flushed to memory. In either case, to avoid data races, concurrent reads or updates of the original list item must be synchronized with any update of the original list item that occurs as a result of the lastprivate clause.

If a list item that appears in a lastprivate clause with the conditional modifier is modified in the region by an assignment outside the construct or by an assignment that does not lexically assign to the list item then the value assigned to the original list item is unspecified.

## Restrictions

Restrictions to the lastprivate clause are as follows:

• A list item must not appear in a lastprivate clause on a work-distribution construct if the corresponding region binds to the region of a parallelism-generating construct in which the list item is private.

• A list item that appears in a lastprivate clause with the conditional modifier must be a scalar variable.

## C++

• A variable of class type (or array thereof) that appears in a lastprivate clause requires an accessible, unambiguous default constructor for the class type, unless the list item is also specified in a firstprivate clause.

• A variable of class type (or array thereof) that appears in a lastprivate clause requires an accessible, unambiguous copy assignment operator for the class type.

• If an original list item in a lastprivate clause on a work-distribution construct has a reference type then it must bind to the same object for all threads in the binding thread set of the work-distribution region.

C++

Fortran

• A variable that appears in a lastprivate clause must be definable.

• If the original list item has the ALLOCATABLE attribute, the corresponding list item of which the value is assigned to the original list item must have an allocation status of allocated upon exit from the sequentially last iteration of the afected loops or lexically last structured block sequence associated with a sections construct.

• If the list item is a polymorphic variable with the ALLOCATABLE attribute, the behavior is unspecified.

Fortran

## Cross References

• distribute Construct, see Section 13.7

• do Construct, see Section 13.6.2

• for Construct, see Section 13.6.1

• loop Construct, see Section 13.8

• private Clause, see Section 7.5.3

• sections Construct, see Section 13.3

• simd Construct, see Section 12.4

• taskloop Construct, see Section 14.2

## 7.5.6 linear Clause

Modifiers

<table><tr><td>Name: linear</td><td>Properties: data-environment attribute, data-sharing attribute, privatization, innermost-leaf, post-modified</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>step-simple-modifier</td><td>list</td><td>OpenMP integer expression</td><td>exclusive, region-invariant, unique</td></tr><tr><td>step-complex-modifier</td><td>list</td><td>Complex, name: stepArguments:linear-stepexpression of integer type (region-invariant)</td><td>unique</td></tr><tr><td>linear-modifier</td><td>list</td><td>Keyword: ref, uval, val</td><td>unique</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

declare\_simd, do, for, simd

## Semantics

The linear clause provides a superset of the functionality provided by the private clause. A list item that appears in a linear clause is subject to the private clause semantics described in Section 7.5.3, except as noted. Additionally, each new list item has the linear attribute and so is a linear variable. If the step-simple-modifier is specified, the behavior is as if the step-complex-modifier is instead specified with step-simple-modifier as its linear-step argument. If linear-step is not specified, it is assumed to be one.

When a linear clause is specified on a loop-collapsing construct and a list item is the loop-iteration variable of an afected loop, the efect is as if that list item had appeared in a lastprivate clause. Otherwise, when a linear clause is specified on a loop-collapsing construct, the value of the new list item on each collapsed iteration corresponds to the value of the original list item before entering the construct plus the logical number of the iteration times linear-step. The value that corresponds to the sequentially last collapsed iteration of the collapsed loops is assigned to the original list item.

When a linear clause is specified on a declare\_simd directive, the list items refer to parameters of the procedure to which the directive applies. For a given call to the procedure, the clause determines whether the SIMD version generated by the directive may be called. If the clause does not specify the ref linear-modifier, the SIMD version requires that the value of the corresponding argument at the callsite is equal to the value of the argument from the first lane plus the logical number of the SIMD lane times the linear-step. If the clause specifies the ref linear-modifier, the SIMD version requires that the storage locations of the corresponding arguments at the callsite from each SIMD lane correspond to storage locations within a hypothetical array of elements of the same type, indexed by the logical number of the SIMD lane times the linear-step.

## Restrictions

Restrictions to the linear clause are as follows:

• If a reduction clause with the inscan modifier also appears on the construct, only loop-iteration variables of afected loops may appear as list items in a linear clause.

• A linear-modifier may be specified as ref or uval only for linear clauses on declare\_simd directives.

• For a linear clause that appears on a loop-nest-associated directive, the diference between the value of a list item at the end of a collapsed iteration and its value at the beginning of the collapsed iteration must be equal to linear-step.

• If linear-modifier is uval for a list item in a linear clause that is specified on a declare\_simd directive and the list item is modified during a call to the SIMD version of the procedure, the OpenMP program must not depend on the value of the list item upon return from the procedure.

• If linear-modifier is uval for a list item in a linear clause that is specified on a declare\_simd directive, the OpenMP program must not depend on the storage of the argument in the procedure being the same as the storage of the corresponding argument at the callsite.

• None of the afected loops of a loop-nest-associated construct that has a linear clause may be a non-rectangular loop.

• All list items must be of integral or pointer type.

• If specified, linear-modifier must be val.

C

C++

• If linear-modifier is not ref, all list items must be of integral or pointer type, or must be a reference to an integral or pointer type.

• If linear-modifier is ref or uval, all list items must be of a reference type.

• If a list item in a linear clause on a worksharing construct has a reference type then it must bind to the same object for all threads of the team.

• If a list item in a linear clause that is specified on a declare\_simd directive is of a reference type and linear-modifier is not ref, the diference between the value of the argument on exit from the function and its value on entry to the function must be the same for all SIMD lanes.

C++

Fortran

• If linear-modifier is not ref, all list items must be of type integer.

• If linear-modifier is ref or uval, all list items must be dummy arguments without the VALUE attribute.

• List items must not be variables that have the POINTER attribute.

• If linear-modifier is not ref and a list item has the ALLOCATABLE attribute, the allocation status of the list item in the last collapsed iteration must be allocated upon exit from that collapsed iteration.

• If linear-modifier is ref, list items must be polymorphic variables, assumed-shape arrays, or variables with the ALLOCATABLE attribute.

• If a list item in a linear clause that is specified on a declare\_simd directive is a dummy argument without the VALUE attribute and linear-modifier is not ref, the diference between the value of the argument on exit from the procedure and its value on entry to the procedure must be the same for all SIMD lanes.

• A common block name must not be a list item in a linear clause.

Fortran

## Cross References

• declare\_simd Directive, see Section 9.8

• do Construct, see Section 13.6.2

• for Construct, see Section 13.6.1

• private Clause, see Section 7.5.3

• simd Construct, see Section 12.4

• taskloop Construct, see Section 14.2

## 7.5.7 is\_device\_ptr Clause

<table><tr><td>Name: is_device_ptr</td><td>Properties: data-environment attribute, data-sharing attribute, device-associated, innermost-leaf, privatization</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

dispatch, target

## Semantics

The is\_device\_ptr clause indicates that its list items are device pointers. Support for device pointers created outside of any OpenMP mechanism that returns a device pointer, is implementation defined.

If the is\_device\_ptr clause is specified on a target construct, each list item is privatized inside the construct. Each new list item has the is-device-ptr attribute and is initialized to the device address to which the original list item refers.

## Restrictions

Restrictions to the is\_device\_ptr clause are as follows:

• Each list item must be a valid device pointer for the device data environment.

## Cross References

• dispatch Construct, see Section 9.7

• has\_device\_addr Clause, see Section 7.5.9

• target Construct, see Section 15.8

## 7.5.8 use\_device\_ptr Clause

<table><tr><td>Name: use_device_ptr</td><td>Properties: all-data-environments, data-environment attribute, data-sharing attribute, device-associated, privatization</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

## target\_data

## Semantics

Each list item in the use\_device\_ptr clause results in a new list item that has the use-device-ptr attribute and is a device pointer that refers to a device address. Since the use\_device\_ptr clause is an all-data-environments clause, it has this efect even for minimal data environments. The device address is determined as follows. A list item is treated as if a zero-ofset assumed-size array at the storage location to which the list item points is mapped by a map clause on the construct with a map-type of storage. If a matched candidate is found for the assumed-size array (see Section 7.9.6), the new list item refers to the device address that is the base address of the array section that corresponds to the assumed-size array in the device data environment. Otherwise, the new list item refers to the address stored in the original list item. All references to the list item inside the structured block associated with the construct are replaced with the new list item that is a private copy in the associated data environment on the encountering device. Thus, the use\_device\_ptr clause is a privatization clause.

## Restrictions

Restrictions to the use\_device\_ptr clause are as follows:

• Each list item must be a C pointer for which the value is the address of an object that has corresponding storage or is accessible on the target device.

Cross References

• target\_data Construct, see Section 15.7

## 7.5.9 has\_device\_addr Clause

<table><tr><td>Name: has_device_addr</td><td>Properties: data-environment attribute, data-sharing attribute, device-associated, outermost-leaf</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

dispatch, target

## Semantics

The has\_device\_addr clause indicates that its list items already have device addresses and therefore they may be directly accessed from a target device. Inside the construct, the list items have the has-device-addr attribute. The list items may include array sections. If the list item is a referencing variable, the semantics of the has\_device\_addr clause apply to its referenced pointee. When the clause appears on the target construct, if the device address of a list item is not for the device on which the target region executes, accessing the list item inside the region results in unspecified behavior.

## Fortran

For a list item in a has\_device\_addr clause, the CONTIGUOUS attribute, storage location, storage size, array bounds, character length, association status and allocation status (as applicable) are the same inside the construct on which the clause appears as for the original list item. The result of inquiring about other list item properties inside the structured block is implementation defined. For a list item that is an array section, the array bounds and result when invoking C\_LOC inside the structured block is the same as if the array base had been specified in the clause instead.

Fortran

## Restrictions

Restrictions to the has\_device\_addr clause are as follows:

C / C++

• Each list item must have a valid device address for the device data environment.

C / C++

## Fortran

• A list item must either have a valid device address for the device data environment, be an unallocated allocatable variable, or be a disassociated data pointer.

• The association status of a list item that is a pointer must not be undefined unless it is a structure component and it results from a predefined default mapper.

Fortran

## Cross References

• dispatch Construct, see Section 9.7

• target Construct, see Section 15.8

## 7.5.10 use\_device\_addr Clause

<table><tr><td>Name: use_device_addr</td><td>Properties: all-data-environments, data-environment attribute, data-sharing attribute, device-associated</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

## target\_data

## Semantics

Each list item in a use\_device\_addr clause has the use-device-addr attribute inside the construct. If the list item is present in the device data environment on entry to the construct, the list item is treated as if it is implicitly mapped by a map clause on the construct with a map-type of storage and all references to the list item inside the structured block associated with the construct are to the corresponding list item in the device data environment. The list items in a use\_device\_addr clause may include array sections and assumed-size arrays. Since the use\_device\_addr clause is an all-data-environments clause, it has this efect even for minimal data environments.

If the list item is a referencing variable, the semantics of the use\_device\_addr clause apply to its referenced pointee. A private copy of the referring pointer that refers to the corresponding referenced pointee is used in place of the original referring pointer in the structured block.

C / C++

If a list item is an array section that has a base pointer, all references to the base pointer inside the structured block are replaced with a new pointer that contains the base address of the corresponding list item. This conversion may be elided if no corresponding list item is present.

C / C++

## Restrictions

Restrictions to the use\_device\_addr clause are as follows:

• Each list item must have a corresponding list item in the device data environment or be accessible on the target device.

• If a list item is an array section, the array base must be a base language identifier.

## Cross References

• target\_data Construct, see Section 15.7

## 7.6 Reduction and Induction Clauses and Directives

The reduction clauses and the induction clause are data-sharing attribute clauses that can be used to perform reductions and inductions in parallel. These recurrence calculations involve the repeated application of reduction operations or induction operations. Reduction clauses include reduction-scoping clauses and reduction-participating clauses. Reduction-scoping clauses define the region in which a reduction is computed. Reduction-participating clauses define the participants in the reduction. The induction clause can be used to express induction operations in a loop.

## 7.6.1 OpenMP Reduction and Induction Identifiers

The syntax of OpenMP reduction identifiers and induction identifiers is defined as follows:

A reduction identifier is either an identifier or one of the following operators: +, \*, &, |, ^, && or ||.

An induction identifier is either an identifier or one of the following operators: + or \*.

C++

A reduction identifier is either an id-expression or one of the following operators: +, \*, &, |, ^, && or ||.

An induction identifier is either an id-expression or one of the following operators: + or \*.

A reduction identifier is either a base language identifier, a user-defined operator, an allowed intrinsic procedure name or one of the following operators: +, \*, .and., .or., .eqv. or .neqv.. The intrinsic procedure names that are allowed as reduction identifiers are max, min, iand, ior and ieor.

An induction identifier is either a base language identifier, a user-defined operator, or one of the following operators: + or \*.

Fortran

## 7.6.2 OpenMP Reduction and Induction Expressions

A reduction expression is an OpenMP stylized expression that is relevant to reduction clauses. An induction expression is an OpenMP stylized expression that is relevant to the induction clause.

## Restrictions

Restrictions to reduction expressions and induction expressions are as follows:

• The execution of a reduction expression or induction expression must not result in the execution of a construct or an OpenMP API routine.

• A declare target directive must be specified for any procedure that can be accessed through any reduction expression or induction expression that respectively corresponds to a reduction identifier or an induction identifier that is used in a target region.

## Fortran

• Any generic identifier, defined operation, defined assignment, or specific procedure used in a reduction expression or an induction expression must be resolvable to a procedure with an explicit interface that has only scalar dummy arguments.

• Any procedure used in a reduction expression or an induction expression must not have any alternate returns appear in the argument list.

• Any procedure called in the region of a reduction expression or an induction expression must be pure and must not reference any host-associated or use-associated variables nor any variables in a common block.

Fortran

## 7.6.2.1 OpenMP Combiner Expressions

A combiner expression specifies how a reduction combines partial results into a single value.

Fortran

A combiner expression is an assignment statement or a subroutine name followed by an argument list.

Fortran

In the definition of a combiner expression, omp\_in and omp\_out are OpenMP identifiers for special variables that refer to storage of the type of the list item to which the reduction applies. If the list item is an array or array section, the OpenMP identifiers omp\_in and omp\_out each refer to an array element of that list item. Each of these OpenMP identifiers denotes one of the values to be combined before executing the combiner expression. The omp\_out OpenMP identifier refers to the storage that holds the resulting combined value after executing the combiner expression. The number of times that the combiner expression is executed and the order of these executions for any reduction clause are unspecified.

## Fortran

If the combiner expression is a subroutine name with an argument list, the combiner expression is evaluated by calling the subroutine with the specified argument list. If the combiner expression is an assignment statement, the combiner expression is evaluated by executing the assignment statement.

If a generic name is used in a combiner expression and the list item in the corresponding reduction clause is an array or array section, that generic name is resolved to the specific procedure that is elemental or only has scalar dummy arguments.

Fortran

## Restrictions

Restrictions to combiner expressions are as follows:

• The only variables allowed in a combiner expression are omp\_in and omp\_out.

Fortran

• Any selectors in the designator of omp\_in and omp\_out must be component selectors.

Fortran

## 7.6.2.2 OpenMP Initializer Expressions

If the initialization of the private copies of list items in a reduction clause is not determined a priori, the syntax of an initializer expression is as follows:

omp\_priv = initializer

C++

omp\_priv initializer

C++

C / C++

function-name(argument-list)

C / C++

or

Fortran

omp\_priv = expression

or

subroutine-name(argument-list)

Fortran

In the definition of an initializer expression, the omp\_priv OpenMP identifier represents a special variable that refers to the storage to be initialized. The OpenMP identifier omp\_orig represents a special variable that can be used in an initializer expression to refer to the storage of the original list item to be reduced. The number of times that an initializer expression is evaluated and the order of these evaluations are unspecified.

C / C++

If an initializer expression is a function name with an argument list, it is evaluated by calling the function with the specified argument list. Otherwise, an initializer expression specifies how omp\_priv is declared and initialized.

C / C++

Fortran

If an initializer expression is a subroutine name with an argument list, it is evaluated by calling the subroutine with the specified argument list. If an initializer expression is an assignment statement, the initializer expression is evaluated by executing the assignment statement.

Fortran

C

The a priori initialization of private copies that are created for reductions follows the rules for initialization of objects with static storage duration.

C++

The a priori initialization of private copies that are created for reductions follows the base language rules for default initialization.

C++

Fortran

The rules for a priori initialization of private copies that are created for reductions are as follows:

• For complex, real, or integer types, the value 0 will be used.

• For logical types, the value .false. will be used.

• For derived types for which default initialization is specified, default initialization will be used.

• Otherwise, the behavior is unspecified.

Fortran

## Restrictions

Restrictions to initializer expressions are as follows:

• The only variables allowed in an initializer expression are omp\_priv and omp\_orig.

• An initializer expression must not modify the variable omp\_orig.

• If an initializer expression is a function name with an argument list, one of the arguments must be the address of omp\_priv.

C++

• If an initializer expression is a function name with an argument list, one of the arguments must be omp\_priv or the address of omp\_priv.

Fortran

• If an initializer expression is a subroutine name with an argument list, one of the arguments must be omp\_priv.

Fortran

## 7.6.2.3 OpenMP Inductor Expressions

An inductor expression specifies an inductor, which is how an induction operation determines a new value of the induction variable from its previous value and a step expression.

Fortran

An inductor expression is either an assignment statement or a subroutine name followed by an argument list.

Fortran

In the definition of an inductor expression, the OpenMP identifier omp\_var is a special variable that refers to storage of the type of the induction variable to which the induction operation applies, and the OpenMP identifier omp\_step is a special variable that refers to the step expression of the induction operation. If the list item is an array or array section, the OpenMP identifier omp\_var refers to an array element of that list item.

## Fortran

If the inductor expression is a subroutine name with an argument list, the inductor expression is evaluated by calling the subroutine with the specified argument list. If the inductor expression is an assignment statement, the inductor expression is evaluated by executing the assignment statement.

If a generic name is used in an inductor expression and the list item in the corresponding induction clause is an array or array section, that generic name is resolved to the specific procedure that is elemental or only has scalar dummy arguments.

Fortran

## Restrictions

Restrictions to inductor expressions are as follows:

• The only variables allowed in an inductor expression are omp\_var and omp\_step.

Fortran

• Any selectors in the designator of omp\_var and omp\_step must be component selectors.

Fortran

## 7.6.2.4 OpenMP Collector Expressions

A collector expression evaluates to the value of the collective step expression of a collapsed iteration. In the definition of a collector expression, the OpenMP identifier omp\_step is a special variable that refers to the step expression and the OpenMP identifier omp\_idx is a special variable that refers to the collapsed iteration number.

## Restrictions

Restrictions to collector expressions are as follows:

• The only variables allowed in a collector expression are omp\_step and omp\_idx.

## 7.6.3 Implicitly Declared OpenMP Reduction Identifiers

C / C++

Table 7.1 lists each reduction identifier that is implicitly declared at every scope and its semantic initializer expression. The actual initializer value is that value as expressed in the data type of the reduction list item if that list item is an arithmetic type. In C++, list items of class type are assigned or constructed with an integral value that matches the initializer value as specified in Section 7.6.6.

TABLE 7.1: Implicitly Declared C/C++ Reduction Identifiers

<table><tr><td>Identifier</td><td>Initializer</td><td>Combiner</td></tr><tr><td>+</td><td>omp_priv = 0</td><td>omp_out += omp_in</td></tr><tr><td>*</td><td>omp_priv = 1</td><td>omp_out *= omp_in</td></tr><tr><td>&amp;</td><td>omp_priv = ~ 0</td><td>omp_out &amp;= omp_in</td></tr><tr><td>|</td><td>omp_priv = 0</td><td>omp_out |= omp_in</td></tr></table>

table continued on next page

table continued from previous page

<table><tr><td>Identifier</td><td>Initializer</td><td>Combiner</td></tr><tr><td>^</td><td>omp_priv = 0</td><td>omp_out ^= omp_in</td></tr><tr><td>&amp;&amp;</td><td>omp_priv = 1</td><td>omp_out = omp_in &amp;&amp; omp_out</td></tr><tr><td>||</td><td>omp_priv = 0</td><td>omp_out = omp_in || omp_out</td></tr><tr><td>max</td><td>omp_priv = Minimal representable number in the reduction list item type</td><td>omp_out = omp_in &gt; omp_out ? omp_in : omp_out</td></tr><tr><td>min</td><td>omp_priv = Maximal representable number in the reduction list item type</td><td>omp_out = omp_in &lt; omp_out ? omp_in : omp_out</td></tr></table>

Table 7.2 lists each reduction identifier that is implicitly declared for numeric and logical types and its semantic initializer value. The actual initializer value is that value as expressed in the data type of the reduction list item.

TABLE 7.2: Implicitly Declared Fortran Reduction Identifiers

<table><tr><td>Identifier</td><td>Initializer</td><td>Combiner</td></tr><tr><td>+</td><td>omp_priv = 0</td><td>omp_out = omp_in + omp_out</td></tr><tr><td>*</td><td>omp_priv = 1</td><td>omp_out = omp_in * omp_out</td></tr><tr><td>.and.</td><td>omp_priv = .true.</td><td>omp_out = omp_in .and. omp_out</td></tr><tr><td>.or.</td><td>omp_priv = .false.</td><td>omp_out = omp_in .or. omp_out</td></tr><tr><td>.eqv.</td><td>omp_priv = .true.</td><td>omp_out = omp_in .eqv. omp_out</td></tr><tr><td>.neqv.</td><td>omp_priv = .false.</td><td>omp_out = omp_in .neqv. omp_out</td></tr><tr><td>max</td><td>omp_priv = Minimal representable number in the reduction list item type</td><td>omp_out = max(omp_in, omp_out)</td></tr><tr><td>min</td><td>omp_priv = Maximal representable number in the reduction list item type</td><td>omp_out = min(omp_in, omp_out)</td></tr></table>

table continued on next page

table continued from previous page

<table><tr><td>Identifier</td><td>Initializer</td><td>Combiner</td></tr><tr><td>iand</td><td>omp_priv = All bits on</td><td>omp_out = iand(omp_in, omp_out)</td></tr><tr><td>ior</td><td>omp_priv = 0</td><td>omp_out = ior(omp_in, omp_out)</td></tr><tr><td>ieor</td><td>omp_priv = 0</td><td>omp_out = ieor(omp_in, omp_out)</td></tr></table>

## 7.6.4 Implicitly Declared OpenMP Induction Identifiers

C / C++

Table 7.3 lists each induction identifier that is implicitly declared at every scope for arithmetic types and its corresponding inductor expression and collector expression.

TABLE 7.3: Implicitly Declared C/C++ Induction Identifiers

<table><tr><td>Identifier</td><td>Inductor Expression</td><td>Collector Expression</td></tr><tr><td>+</td><td>omp_var = omp_var + omp_step</td><td>omp_step * omp_idx</td></tr><tr><td>*</td><td>omp_var = omp_var * omp_step</td><td>pow(omp_step, omp_idx)</td></tr></table>

Table 7.4 lists each induction identifier that is implicitly declared for numeric types and its corresponding inductor expression and collector expression.

TABLE 7.4: Implicitly Declared Fortran Induction Identifiers

<table><tr><td>Identifier</td><td>Inductor Expression</td><td>Collector Expression</td></tr><tr><td>+</td><td>omp_var = omp_var + omp_step</td><td>omp_step * omp_idx</td></tr><tr><td>*</td><td>omp_var = omp_var * omp_step</td><td>omp_step ** omp_idx</td></tr></table>

# 7.6.5 Properties Common to Reduction and induction Clauses

The list items that appear in a reduction clause or an induction clause may include array sections and array elements.

C++

If the type is a derived class then any reduction identifier or induction identifier that matches its base classes is also a match if no specific match for the type has been specified.

If the reduction identifier or induction identifier is an implicitly declared reduction identifier or induction identifier or otherwise not an id-expression then it is implicitly converted to one by prepending the keyword operator (for example, + becomes operator+). This conversion is valid for the +, \*, /, && and || operators.

If the reduction identifier or induction identifier is qualified then a qualified name lookup is used to find the declaration.

If the reduction identifier or induction identifier is unqualified then an argument-dependent name lookup must be performed using the type of each list item.

C++

If a list item is an array or array section, it will be treated as if a reduction clause or an induction clause would be applied to each separate element of the array or array section.

If a list item is an array section, the elements of any copy of the array section will be stored contiguously.

Fortran

If the original list item has the POINTER attribute, any copies of the list item are associated with private targets.

Fortran

## Restrictions

Restrictions common to reduction clauses and induction clauses are as follows:

• Any array element must be specified at most once in all list items on a directive.

• For a reduction identifier or an induction identifier declared in a declare\_reduction or a declare\_induction directive, the directive must appear before its use in a reduction clause or induction clause.

• If a list item is an array section, it must not be a zero-length array section and its array base must be a base language identifier.

• If a list item is an array section or an array element, accesses to the elements of the array outside the specified array section or array element result in unspecified behavior.

## C / C++

• The type of a list item that appears in a reduction clause must be valid for the reduction identifier. The type of a list item and of the step expression that appear in an induction clause must be valid for the induction identifier.

• A list item that appears in a reduction clause or an induction clause must not be const-qualified.

• The reduction identifier or induction identifier for any list item must be unambiguous and accessible.

C / C++

Fortran

• The type, type parameters and rank of a list item that appears in a reduction clause must be valid for the combiner expression and the initializer expression. The type, type parameters and rank of a list item and of the step expression that appear in an induction clause must be valid for the inductor expression.

• A list item that appears in a reduction clause or an induction clause must be definable.

• A procedure pointer must not appear in a reduction clause or an induction clause.

• A pointer with the INTENT(IN) attribute must not appear in a reduction clause or an induction clause.

• An original list item with the POINTER attribute or any pointer component of an original list item that is referenced in a combiner expression or an inductor expression must be associated at entry with the construct that contains the reduction clause or induction clause. Additionally, the list item or the pointer component of the list item must not be deallocated, allocated, or pointer assigned within the region.

• An original list item with the ALLOCATABLE attribute or any allocatable component of an original list item that corresponds to a special variable identifier in a combiner expression, initializer expression, or inductor expression must be in the allocated state at entry to the construct that contains the reduction clause or induction clause. Additionally, the list item or the allocatable component of the list item must be neither deallocated nor allocated, explicitly or implicitly, within the region.

• If the reduction identifier or induction identifier is defined in a declare\_reduction or declare\_induction directive, that directive must be in the same subprogram, or accessible by host or use association.

• If the reduction identifier or induction identifier is a user-defined operator, the same explicit interface for that operator must be accessible at the location of the declare\_reduction or declare\_induction directive that defines the reduction or induction identifier.

• If the reduction identifier or induction identifier is defined in a declare\_reduction or declare\_induction directive, any procedure referenced in the initializer, combiner, inductor, or collector clause must be an intrinsic function, or must have an explicit interface where the same explicit interface is accessible as at the declare\_reduction or declare\_induction directive.

Fortran
````
