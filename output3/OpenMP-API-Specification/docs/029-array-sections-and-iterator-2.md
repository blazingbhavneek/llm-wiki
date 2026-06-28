
• If the type T is a reference to a type $T '$ , then the type will be considered to be $T '$ for all purposes of the designated array.

C++ C / C++

## 5.2.5 Array Sections

An array section designates a subset of the elements in an array.

C / C++

To specify an array section in an OpenMP directive, array subscript expressions are extended with one of the following syntaxes:

```ini
[ lower-bound : length : stride]
[ lower-bound : length : ]
[ lower-bound : length ]
[ lower-bound : : stride]
[ lower-bound : : ]
[ lower-bound : ]
[ : length : stride]
[ : length : ]
[ : length ]
[ : : stride]
[ : : ]
[ : ]
```

The array section must be a subset of the original array.

Array sections are allowed on multidimensional arrays. Base language array subscript expressions can be used to specify length-one dimensions of multidimensional array sections.

Each of the lower-bound, length, and stride expressions if specified must be an integral type expression of the base language. When evaluated they represent a set of integer values as follows:

{ lower-bound, lower-bound + stride, lower-bound + 2 \* stride,... , lower-bound + ((length - 1) \* stride) }

The length must evaluate to a non-negative integer.

The stride must evaluate to a positive integer.

When the stride is absent it defaults to 1.

When the length is absent and the size of the dimension is known, it defaults to ⌈(size − lower-bound)/stride⌉, where size is the size of the array dimension. When the length is absent and the size of the dimension is not known, the array section is an assumed-size array.

When the lower-bound is absent it defaults to 0.

$$
\mathrm{C} / \mathrm{C} + + (\text {cont.})
$$

The precedence of a subscript operator that uses the array section syntax is the same as the precedence of a subscript operator that does not use the array section syntax.

Note – The following are examples of array sections:

```txt
a[0:6]
a[0:6:1]
a[1:10]
a[1:]
a[:10:2]
b[10][:][:]
b[10][:][:0]
c[42][0:6][:]
c[42][0:6:2][:]
c[1:10][42][0:6]
S.c[:100]
p->y[:10]
this->a[:N]
(p+10)[:N]
```

Assume a is declared to be a 1-dimensional array with dimension size 11. The first two examples are equivalent, and the third and fourth examples are equivalent. The fifth example specifies a stride of 2 and therefore is not contiguous.

Assume b is declared to be a pointer to a 2-dimensional array with dimension sizes 10 and 10. The sixth example refers to all elements of the 2-dimensional array given by b[10]. The seventh example is a zero-length array section.

Assume c is declared to be a 3-dimensional array with dimension sizes 50, 50, and 50. The eighth example is contiguous, while the ninth and tenth examples are not contiguous.

The final four examples show array sections that are formed from more general array bases.

The following are examples that are non-conforming array sections:

```clojure
s[:10].x
p[:10]->y
*(xp[:10])
```

For all three examples, a base language operator is applied in an undefined manner to an array section. The only operator that may be applied to an array section is a subscript operator for which the array section appears as the postfix expression.

C / C++

Fortran

Fortran has built-in support for array sections although some restrictions apply to their use in OpenMP directives, as enumerated at the end of this section.

Fortran

## Restrictions

Restrictions to array sections are as follows:

• An array section can appear only in clauses for which it is explicitly allowed.

• A stride expression may not be specified unless otherwise stated.

C / C++

• An assumed-size array can appear only in clauses for which it is explicitly allowed.

• An element of an array section with a non-zero size must have a complete type.

• The array base of an array section must have an array or pointer type.

• If a consecutive sequence of array subscript expressions appears in an array section, and the first subscript expression in the sequence uses the extended array section syntax defined in this section, then only the last subscript expression in the sequence may select array elements that have a pointer type.

C / C++

C++

• If the type of the array base of an array section is a reference to a type T, then the type will be considered to be T for all purposes of the array section.

• An array section cannot be used in an overloaded [] operator.

Fortran

• If a stride expression is specified, it must be positive.

• The upper bound for the last dimension of a dummy assumed-size array must be specified.

• If a list item is an array section with vector subscripts, the first array element must be the lowest in the array element order of the array section.

• If a list item is an array section, the last part-ref of the list item must have a section subscript list.

Fortran

## 5.2.6 iterator Modifier

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>iterator</td><td>locator-list</td><td>Complex, name: iteratorArguments:iterator-specifier list of iterator specifier list item type (default)</td><td>unique</td></tr></table>

Clauses

affinity, depend, from, map, to

An iterator modifier is a unique, complex modifier that defines a set of iterators, each of which is an iterator-identifier and an associated iterator value set. An iterator-identifier expands to those values in the clause argument for which it is specified. Each list item of the iterator argument is an iterator specifier with this format:

C / C++

[ iterator-type ] iterator-identifier = range-specification

C / C++

Fortran

[ iterator-type :: ] iterator-identifier = range-specification

Fortran

where:

• iterator-identifier is a base language identifier.

• iterator-type is a type that is permitted in a type-name list.

• range-specification is of the form begin:end[:step], where begin and end are expressions for which their types can be converted to iterator-type and step is an integral expression.

C / C++

In an iterator specifier, if the iterator-type is not specified then that iterator is of int type.

C / C++

Fortran

In an iterator specifier, if the iterator-type is not specified then that iterator has default integer type. Fortran Fortran

In a range-specification, if the step is not specified its value is implicitly defined to be 1.

An iterator only exists in the context of the clause argument that its iterator modifier modifies. An iterator also hides all accessible symbols with the same name in the context of that clause argument.

The use of a variable in an expression that appears in the range-specification causes an implicit reference to the variable in all enclosing constructs.

The iterator value set of the iterator are the set of values $i _ { 0 } , . . . , i _ { N - 1 }$ where:

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
- $i_0 = (\text{iterator-type})$ begin;
- $i_j = (\text{iterator-type}) (i_{j-1} + step)$, where $j \geq 1$; and
- if step &gt; 0,
    - $i_0 &lt; (\text{iterator-type})$ end;
    - $i_{N-1} &lt; (\text{iterator-type})$ end; and
    - $(\text{iterator-type}) (i_{N-1} + step) \geq (\text{iterator-type})$ end;
- if step &lt; 0,
    - $i_0 &gt; (\text{iterator-type})$ end;
    - $i_{N-1} &gt; (\text{iterator-type})$ end; and
    - $(\text{iterator-type}) (i_{N-1} + step) \leq (\text{iterator-type})$ end.
</div>

The iterator value set of the iterator are the set of values $i _ { 1 } , . . . , i _ { N }$ where:

$i _ { 1 } = b e g i n ;$

$i _ { j } = i _ { j - 1 } + s t e p , \mathrm { w h e r e \ } j \ge 2 ;$ and

• if step > 0,

• if step < 0,

## Fortran

The iterator value set will be empty if no possible value complies with the conditions above.

If an iterator-identifier appears in a list item expression of the modified argument, the efect is as if the list item is instantiated within the clause for each member of the iterator value set, substituting each occurrence of iterator-identifier in the list item expression with the member of the iterator value set. If the iterator value set is empty then the efect is as if the list item was not specified.

## Restrictions

Restrictions to iterator modifiers are as follows:

• The iterator-type must not declare a new type.

• For each value i in an iterator value set, the mathematical result of i + step must be representable in iterator-type.

C / C++

• The iterator-type must be an integral or pointer type.

• The iterator-type must not be const qualified.

C / C++

Fortran

• The iterator-type must be an integer type.

Fortran

• If the step expression of a range-specification equals zero, the behavior is unspecified.

• Each iterator-identifier can only be defined once in the modifier-parameter-specification.

• An iterator-identifier must not appear in the range-specification.

• If an iterator modifier appears in a clause that is specified on a task\_iteration directive then the loop-iteration variables of taskloop-afected loops of the associated taskloop construct must not appear in the range-specification.

## Cross References

• affinity Clause, see Section 14.10

• depend Clause, see Section 17.9.5

• from Clause, see Section 7.10.2

• map Clause, see Section 7.9.6

• to Clause, see Section 7.10.1
