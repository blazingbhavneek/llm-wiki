
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
