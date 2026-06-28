
<table><tr><td>Name: apply</td><td>Properties: default</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>applied-directives</td><td>list of directive specification list item type</td><td>default</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>loop-modifier</td><td>applied-directives</td><td>Complex, Keyword: fused, grid, identity, interchanged, intratile, offsets, reversed, split, unrolledArguments: indices list of expression of integer type (optional)</td><td>optional</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

fuse, interchange, nothing, reverse, split, stripe, tile, unroll

## Semantics

The apply clause applies loop-nest-associated constructs, specified by the applied-directives list, to generated loops of a loop-transforming construct. The loop-modifier specifies to which generated loops the directives are applied. If the loop-transforming construct generates a canonical loop sequence, the generated loops to which the directives are applied are the outermost loops of each generated loop nest. An applied loop-transforming construct may also specify apply clauses.

The valid loop-modifier keywords, the default loop-modifier if it exists, the number of applied-directives list items, and the target of each applied-directives list item is defined by the loop-transforming construct to which it applies. Each of the indices in the argument of the loop-modifier specifies the position of the generated loop to which the respective applied-directives item is applied.

If the loop-modifier is specified with no argument, the behavior is as if the list 1, 2, . . . , m is specified, where m is the number of generated loops according to the specification of the loop-modifier keyword. If the loop-modifier is omitted and a default loop-modifier exists for the apply clause on the construct, the behavior is as if the default loop-modifier with the argument 1, 2, . . . , m is specified.

The list items of the apply clause arguments are not required to be directive-wide unique.

## Restrictions

Restrictions to the apply clause are as follows:

• Each list item in the applied-directives list of any apply clause must be nothing or the directive-specification of a loop-nest-associated construct.

• The loop-transforming construct on which the apply clause is specified must either have the generally-composable property or every list item in the applied-directives list of any apply clause must be the directive-specification of a loop-transforming directive.

• Every list item in the applied-directives list of any apply clause that is specified on a loop-transforming construct that is itself specified as a list item in the applied-directives list of another apply clause must be the directive-specification of a loop-transforming directive.

• For a given loop-modifier keyword, every indices list item may appear at most once in any apply clause on the directive.

• Every indices list item must be a positive constant less than or equal to m, the number of generated loops according to the specification of the loop-modifier keyword.

• The list items in indices must be in ascending order.

• If a directive does not define a default loop-modifier keyword, a loop-modifier is required.

## Cross References

• fuse Construct, see Section 11.3

• interchange Construct, see Section 11.4

• metadirective, see Section 9.4.3

• nothing Directive, see Section 10.7

• reverse Construct, see Section 11.5

• split Construct, see Section 11.6

• stripe Construct, see Section 11.7

• tile Construct, see Section 11.8

• unroll Construct, see Section 11.9

## 11.2 sizes Clause

<table><tr><td>Name: sizes</td><td>Properties: unique, required</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>size-list</td><td>list of OpenMP integer expression type</td><td>positive</td></tr></table>

## Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

stripe, tile

## Semantics

For a given loop-transforming directive on which the clause appears, the sizes clause specifies the manner in which the logical iteration space of the afected canonical loop nest is subdivided into m-dimensional grid cells that are relevant to the loop transformation, where m is the number of list items in size-list. Specificially, each list item in size-list specifies the size of the grid cells along the corresponding dimension. List items in size-list are not required to be unique.

## Restrictions

Restrictions to the sizes clause are as follows:

• The loop nest depth of the associated loop nest of the loop-transforming construct on which the clause is specified must be greater than or equal to m.

## Cross References

• stripe Construct, see Section 11.7

• tile Construct, see Section 11.8

## 11.3 fuse Construct
