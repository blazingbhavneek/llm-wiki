
This chapter defines constructs and concepts related to device execution.

## 15.1 device\_type Clause

<table><tr><td>Name: device_type</td><td>Properties: unique</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>device-type-description</td><td>Keyword: any, host, nohost</td><td>default</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

begin declare\_target, declare\_target, groupprivate, target

## Semantics

If the device\_type clause appears on a declarative directive, the device-type-description argument specifies the type of devices for which a version of the procedure or variable should be made available. If the device\_type clause appears on a target construct, the argument specifies the type of devices for which the implementation should support execution of the corresponding target region.

The host device-type-description specifies the host device. The nohost device-type-description specifies any supported non-host device. The any device-type-description specifies any supported device. If the device\_type clause is not specified, the behavior is as if the device\_type clause appears with any specified.

If the device\_type clause specifies the host device on a target construct for which the target device is a non-host device, the corresponding region executes on the host device. Otherwise, if the devices specified by the device\_type clause does not include the target device then runtime error termination is performed.

## Cross References

• begin declare\_target Directive, see Section 9.9.2

• declare\_target Directive, see Section 9.9.1

• groupprivate Directive, see Section 7.13

• target Construct, see Section 15.8

## 15.2 device Clause

<table><tr><td>Name: device</td><td>Properties: ICV-defaulted, unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>device-description</td><td>expression of integer type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>device-modifier</td><td>device-description</td><td>Keyword: ancestor, device_num</td><td>default</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

dispatch, interop, target, target\_data, target\_enter\_data, target\_exit\_data, target\_update

## Semantics

The device clause identifies the target device that is associated with a device construct.

If device\_num is specified as the device-modifier, the device-description specifies the device number of the target device. If device-modifier does not appear in the clause, the behavior of the clause is as if device-modifier is device\_num. If the device-description evaluates to omp\_invalid\_device, runtime error termination is performed.

If ancestor is specified as the device-modifier, the device-description specifies the number of target nesting levels of the target device. Specifically, if the device-description evaluates to 1, the target device is the parent device of the enclosing target region. If the construct on which the device clause appears is not encountered in a target region, the current device is treated as the parent device.

Unless otherwise specified, for directives that accept the device clause, if no device clause is present, the behavior is as if the device clause appears with device\_num as device-modifier and with a device-description that evaluates to the value of the default-device-var ICV.

## Restrictions

• The ancestor device-modifier must not appear on the device clause on any directive other than the target construct.

• If the ancestor device-modifier is specified, the device-description must evaluate to 1 and a requires directive with the reverse\_offload clause must be specified;

• If the device\_num device-modifier is specified and target-ofload-var is not mandatory, device-description must evaluate to a conforming device number.

## Cross References

• dispatch Construct, see Section 9.7

• target-ofload-var ICV, see Table 3.1

• interop Construct, see Section 16.1

• target Construct, see Section 15.8

• target\_data Construct, see Section 15.7

• target\_enter\_data Construct, see Section 15.5

• target\_exit\_data Construct, see Section 15.6

• target\_update Construct, see Section 15.9
