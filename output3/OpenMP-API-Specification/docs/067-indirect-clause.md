
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
