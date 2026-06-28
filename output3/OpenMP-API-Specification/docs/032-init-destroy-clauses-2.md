## 5.5 if Clause

Modifiers

<table><tr><td>Name: if</td><td>Properties: target-consistent</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>if-expression</td><td>expression of OpenMP logical type</td><td>default</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

cancel, parallel, simd, target, target\_data, target\_enter\_data, target\_exit\_data, target\_update, task, task\_iteration, taskgraph, taskloop, teams

## Semantics

The efect of the if clause depends on the construct to which it is applied. If the construct is not a compound construct then the efect is described in the section that describes that construct.

## Restrictions

Restrictions to the if clause are as follows:

• At most one if clause can be specified that applies to the semantics of any construct or constituent construct of a directive-specification.

## Cross References

• cancel Construct, see Section 18.2

• parallel Construct, see Section 12.1

• simd Construct, see Section 12.4

• target Construct, see Section 15.8

• target\_data Construct, see Section 15.7

• target\_enter\_data Construct, see Section 15.5

• target\_exit\_data Construct, see Section 15.6

• target\_update Construct, see Section 15.9

• task Construct, see Section 14.1

• task\_iteration Directive, see Section 14.2.3

• taskgraph Construct, see Section 14.3

• taskloop Construct, see Section 14.2

• teams Construct, see Section 12.2

## 5.6 init Clause

<table><tr><td>Name: init</td><td>Properties: innermost-leaf</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>init-var</td><td>variable of OpenMP type</td><td>default</td></tr></table>

## Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>prefer-type</td><td>init-var</td><td>Complex, name: prefer_typeArguments: prefer-type-specification list of preference spec- ification list item type (default)</td><td>complex, unique</td></tr><tr><td>depinfo-modifier</td><td>init-var</td><td>Complex, Keyword: in, inout, inoutset, mutexinoutset, outArguments: locator-list-item locator list item (default)</td><td>complex, unique</td></tr><tr><td>interop-type</td><td>init-var</td><td>Keyword: target, targetsync</td><td>repeatable</td></tr><tr><td>directive-name- modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

depobj, interop

## Semantics

When the init clause appears on a depobj construct, it specifies that init-var is a depend object for which the state is set to initialized. The efect is that init-var is set to represent a dependence type and locator list item as specified by the name and argument of the depinfo-modifier.

When the init clause appears on an interop construct, it specifies that init-var is an interoperability object that is initialized to refer to the list of properties associated with any interop-type. For any interop-type, the properties type, type\_name, vendor, vendor\_name and device\_num will be available. If the implementation cannot initialize interop-var, it is initialized to omp\_interop\_none.

The targetsync interop-type will additionally provide the targetsync property, which is the handle to a foreign synchronization object for enabling synchronization between OpenMP tasks and foreign tasks that execute in the foreign execution context.

The target interop-type will additionally provide the following properties:

• device, which will be a foreign device handle;

• device\_context, which will be a foreign device context handle; and

• platform, which will be a handle to a foreign platform of the device.

## Restrictions

• init-var must not be constant.

• If the init clause appears on a depobj construct, init-var must refer to a variable of depend OpenMP type that is uninitialized.

• If the init clause appears on a depobj construct then the depinfo-modifier has the required property and otherwise it must not be present.

• If the init clause appears on an interop construct, init-var must refer to a variable of interop OpenMP type.

• If the init clause appears on an interop construct, the interop-type modifier has the required property and each interop-type keyword has the unique property. Otherwise, the interop-type modifier must not be present.

• The prefer-type modifier must not be present unless the init clause appears on an interop construct.

## Cross References

• depobj Construct, see Section 17.9.3

• interop Construct, see Section 16.1

## 5.7 destroy Clause

<table><tr><td>Name: destroy</td><td>Properties: default</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>destroy-var</td><td>variable of OpenMP variable type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

## depobj, interop

## Additional information

When the destroy clause appears on a depobj directive that specifies depend-object as a directive argument, the destroy-var argument may be omitted. If omitted, the efect is as if destroy-var refers to the depend-object argument.

## Semantics

When the destroy clause appears on a depobj construct, the state of destroy-var is set to uninitialized.

When the destroy clause appears on an interop construct, the interop-type is inferred based on the interop-type used to initialize destroy-var, and destroy-var is set to the value of omp\_interop\_none after resources associated with destroy-var are released. The object referred to by destroy-var is unusable after destruction and the efect of using values associated with it is unspecified until it is initialized again by another interop construct.

## Restrictions

• destroy-var must not be constant.

• If the destroy clause appears on a depobj construct, destroy-var must refer to a variable of depend OpenMP type that is initialized.

• If the destroy clause appears on an interop construct, destroy-var must refer to a variable of interop OpenMP type that is initialized.

## Cross References

• depobj Construct, see Section 17.9.3

• interop Construct, see Section 16.1

# 6 Base Language Formats and Restrictions
