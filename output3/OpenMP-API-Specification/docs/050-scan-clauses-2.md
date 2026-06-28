## 7.7.1 inclusive Clause

<table><tr><td>Name: inclusive</td><td>Properties: innermost-leaf, unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

## scan

## Semantics

The inclusive clause is used on a scan directive to specify that an inclusive scan computation is performed for each list item of the argument list. The structured block sequence that precedes the directive serves as the input phase of the inclusive scan computation while the structured block sequence that follows the directive serves as the scan phase of the inclusive scan computation. The list items that appear in an inclusive clause may include array sections and array elements.

## Cross References

• scan Directive, see Section 7.7

## 7.7.2 exclusive Clause

<table><tr><td>Name: exclusive</td><td>Properties: innermost-leaf, unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>list</td><td>list of variable list item type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

## scan

## Semantics

The exclusive clause is used on a scan directive to specify an exclusive scan computation is performed for each list item of the argument list. The structured block sequence that follows the directive serves as the input phase of the exclusive scan computation while the structured block sequence that precedes the directive serves as the scan phase of the exclusive scan computation. The list items that appear in an exclusive clause may include array sections and array elements.

## Cross References

• scan Directive, see Section 7.7

## 7.7.3 init\_complete Clause

<table><tr><td>Name: init_complete</td><td>Properties: innermost-leaf, unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>create_init_phase</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

## scan

## Semantics

The init\_complete clause is used on a scan directive to demarcate the end of the initialization phase of an exclusive scan computation. The structured block sequence that precedes the directive serves as the initialization phase of the exclusive scan computation while the structured block sequence that follows the directive serves as the scan phase of the exclusive scan computation. If create\_init\_phase is not specified, the efect is as if create\_init\_phase evaluates to true.

## Cross References

• scan Directive, see Section 7.7
