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
