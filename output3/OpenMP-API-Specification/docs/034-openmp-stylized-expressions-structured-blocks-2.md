
• OpenMP Foreign Runtime Identifiers, see Section 16.1.1

• OpenMP Reduction and Induction Identifiers, see Section 7.6.1

• Mapper Identifiers and mapper Modifiers, see Section 7.9.4

## 6.2 OpenMP Stylized Expressions

An OpenMP stylized expression is a base language expression that is subject to restrictions that enable its use within an OpenMP implementation. OpenMP stylized expressions often use OpenMP identifiers that the implementation binds to well-defined internal state.

## Cross References

• OpenMP Collector Expressions, see Section 7.6.2.4

• OpenMP Combiner Expressions, see Section 7.6.2.1

• OpenMP Inductor Expressions, see Section 7.6.2.3

• OpenMP Initializer Expressions, see Section 7.6.2.2

![](images/ea8a44ade411ce027677b194c54986d0e71bc00aa00aa5b3b1d558deef490b77.jpg)

![](images/22f346b74da0196c0dd016b75852c25451f805f458be03d85e1e9d0d19cbd8e6.jpg)

## 6.3 Structured Blocks

This section specifies the concept of a structured block. A structured block:

• may contain infinite loops where the point of exit is never reached;

• may halt due to an IEEE exception;

C / C++

• may contain calls to exit(), \_Exit(), quick\_exit(), abort() or functions with a \_Noreturn specifier (in C) or a noreturn attribute (in C/C++);

• may be an expression statement, iteration statement, selection statement, or try block, provided that the corresponding compound statement obtained by enclosing it in { and } would be a structured block; and

C / C++

Fortran

• may contain STOP or ERROR STOP statements.

Fortran

C / C++

A structured block sequence that consists of no statements or more than one statement may appear only for executable directives that explicitly allow it. The corresponding compound statement obtained by enclosing the sequence in { and } must be a structured block and the structured block sequence then should be considered to be a structured block with all of its restrictions.

The remainder of this section covers OpenMP context-specific structured blocks that conform to specific syntactic forms and restrictions that are required for certain block-associated directives.

Restrictions

Restrictions to structured blocks are as follows:

• Entry to a structured block must not be the result of a branch.

• The point of exit cannot be a branch out of the structured block.

![](images/b3fe3cb78a86272f5ab6d947c0bfb9e57ca6f58ed19e236a04cea92d4e5494f0.jpg)

• The point of entry to a structured block must not be a call to setjmp.

• longjmp must not violate the entry/exit criteria of structured blocks.

C / C++

• throw, co\_await, co\_yield and co\_return must not violate the entry/exit criteria of structured blocks.

## Fortran
