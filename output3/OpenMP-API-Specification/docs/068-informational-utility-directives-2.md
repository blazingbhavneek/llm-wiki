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
