## 9.9 Declare Target Directives

Declare target directives apply to procedures and/or variables to ensure that they can be executed or accessed on a device. Variables are either replicated as device-local variables for each device through a local clause, are mapped for all device executions through an enter clause, or are mapped for specific device executions through a link clause. An implementation may generate diferent versions of a procedure to be used for target regions that execute on diferent devices. Whether it generates diferent versions, and whether it calls a diferent version in a target region from the version that it calls outside a target region, are implementation defined.

To facilitate device usage, OpenMP defines rules that implicitly specify declare target directives for procedures and variables. The remainder of this section defines those rules as well as restrictions that apply to all declare target directives.

C++

If a variable with static storage duration has the constexpr specifier and is not a groupprivate variable then the variable is treated as if it had appeared as a list item in an enter clause on a declare target directive.

If a variable with static storage duration that is not a device-local variable (including that it is not a groupprivate variable) is declared in a device procedure then the variable is treated as if it had appeared as a list item in an enter clause on a declare target directive.

If a procedure is referenced outside of any reverse-ofload region in a procedure that appears as a list item in an enter clause on a non-host declare target directive then the name of the referenced procedure is treated as if it had appeared in an enter clause on a declare target directive.

C / C++

If a variable with static storage duration or a function (except lambda for C++) is referenced in the initializer expression list of a variable with static storage duration that appears as a list item in an enter or local clause on a declare target directive then the name of the referenced variable or procedure is treated as if it had appeared in an enter clause on a declare target directive.

C / C++

Fortran

If a declare\_target directive has a device\_type clause then any enclosed internal procedure cannot contain any declare\_target directives. The enclosing device\_type clause implicitly applies to internal procedures.

Fortran

A reference to a device-local variable that has static storage duration inside a device procedure is replaced with a reference to the copy of the variable for the device. Otherwise, a reference to a variable that has static storage duration in a device procedure is replaced with a reference to a corresponding variable in the device data environment. If the corresponding variable does not exist or the variable does not appear in an enter or link clause on a declare target directive, the behavior is unspecified.

## Execution Model Events

The target-global-data-op event occurs when an original list item is associated with a corresponding list item on a device as a result of a declare target directive; the event occurs before the first access to the corresponding list item.

## Tool Callbacks

A thread dispatches a registered target\_data\_op\_emi callback with ompt\_scope\_beginend as its endpoint argument for each occurrence of a target-global-data-op event in that thread.

## Restrictions

Restrictions to any declare target directive are as follows:

• The same list item must not explicitly appear in both an enter clause on one declare target directive and a link or local clause on another declare target directive.

• The same list item must not explicitly appear in both a link clause on one declare target directive and a local clause on another declare target directive.

• If a variable appears in a enter clause on a declare target directive, its initializer must not refer to a variable that appears in a link clause on a declare target directive.

## Cross References

• begin declare\_target Directive, see Section 9.9.2

• declare\_target Directive, see Section 9.9.1

• enter Clause, see Section 7.9.7

• link Clause, see Section 7.9.8

• OMPT scope\_endpoint Type, see Section 33.27

• target Construct, see Section 15.8

• target\_data\_op\_emi Callback, see Section 35.7

## 9.9.1 declare\_target Directive
