
13.6.3 schedule Clause

<table><tr><td>Name: schedule</td><td>Properties: schedule-specification, unique</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>kind</td><td>Keyword: auto, dynamic, guided, runtime, static</td><td>default</td></tr><tr><td>chunk_size</td><td>expression of integer type</td><td>ultimate, optional, positive, region-invariant</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>ordering-modifier</td><td>kind</td><td>Keyword: monotonic, nonmonotonic</td><td>unique</td></tr><tr><td>chunk-modifier</td><td>kind</td><td>Keyword: simd</td><td>unique</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

do, for

## Semantics

The schedule clause specifies how collapsed iterations of a worksharing-loop construct are divided into chunks, and how these chunks are distributed among threads of the team.

The chunk\_size expression is evaluated using the original list items of any variables that are made private variables in the worksharing-loop construct. Whether, in what order, or how many times, any side efects of the evaluation of this expression occur is unspecified. The use of a variable in a schedule clause expression of a worksharing-loop construct causes an implicit reference to the variable in all enclosing constructs.

If the kind argument is static, chunks of increasing collapsed iteration numbers are assigned to the threads of the team in a round-robin fashion in the order of the thread number. Each chunk includes chunk\_size collapsed iterations, except possibly for the chunk that contains the sequentially last iteration, which may have fewer iterations. If chunk\_size is not specified, the collapsed iteration space is divided into chunks that are approximately equal in size, and at most one chunk is distributed to each thread.

If the kind argument is dynamic, each thread executes a chunk, then requests another chunk, until no chunks remain to be assigned. Each chunk contains chunk\_size collapsed iterations, except for the chunk that contains the sequentially last iteration, which may have fewer iterations. If chunk\_size is not specified, it defaults to 1.

If the kind argument is guided, each thread executes a chunk, then requests another chunk, until no chunks remain to be assigned. For a chunk\_size of 1, the size of each chunk is proportional to the number of unassigned collapsed iterations divided by the number of threads in the team, decreasing to 1. For a chunk\_size with value $k > 1$ , the size of each chunk is determined in the same way, with the restriction that the chunks do not contain fewer than k collapsed iterations (except for the chunk that contains the sequentially last iteration, which may have fewer than k iterations). If chunk\_size is not specified, it defaults to 1.

If the kind argument is auto, the decision regarding scheduling is implementation defined. If the schedule clause is not specified on a worksharing-loop construct then the efect is as if the schedule clause was specified with auto as its kind argument.

If the kind argument is runtime, the decision regarding scheduling is deferred until runtime, and the behavior is as if the clause specifies kind, chunk-size and ordering-modifier as set in the run-sched-var ICV. If the schedule clause explicitly specifies any modifiers then they override any corresponding modifiers that are specified in the run-sched-var ICV.

If the simd chunk-modifier is specified and the canonical loop nest is associated with a SIMD construct, new\_chunk\_size = ⌈chunk\_size/simd\_width⌉ ∗ simd\_width is the chunk\_size for all chunks except the first and last chunks, where simd\_width is an implementation defined value. The first chunk will have at least new\_chunk\_size collapsed iterations except if it is also the last chunk. The last chunk may have fewer collapsed iterations than new\_chunk\_size. If the simd chunk-modifier is specified and the canonical loop nest is not associated with a SIMD construct, the modifier is ignored.

##

Note – For a team of $\dot { \mathbf { \rho } } _ { p }$ threads and collapsed loops of n collapsed iterations, let $\lceil n / p \rceil$ be the integer q that satisfies $n = p * q - r .$ with $0 < = r < p .$ One compliant implementation of the static schedule type (with no specified chunk\_size) would behave as though chunk\_size had been specified with value q. Another compliant implementation would assign q collapsed iterations to the first $p - r$ threads, and $q - 1$ collapsed iterations to the remaining r threads. This illustrates why a conforming program must not rely on the details of a particular implementation.

A compliant implementation of the guided schedule type with a chunk\_size value of k would assign $q = \lceil n / p \rceil$ collapsed iterations to the first available thread and set n to the larger of $n - q$ and $p * k .$ . It would then repeat this process until q is greater than or equal to the number of remaining collapsed iterations, at which time the remaining iterations form the final chunk. Another compliant implementation could use the same method, except with $q = \lceil n / ( 2 p ) \rceil$ , and set n to the larger of $n - q$ and $2 * p * k$

If the monotonic ordering-modifier is specified then each thread executes the chunks that it is assigned in increasing collapsed iteration order. When the nonmonotonic ordering-modifier is specified then chunks may be assigned to threads in any order and the behavior of an application that depends on any execution order of the chunks is unspecified. If an ordering-modifier is not specified, the efect is as if the monotonic ordering-modifier is specified if the kind argument is static or an ordered clause is specified on the construct; otherwise, the efect is as if the nonmonotonic ordering-modifier is specified.

## Restrictions

Restrictions to the schedule clause are as follows:

• The schedule clause cannot be specified if any of the collapsed loops is a non-rectangular loop.

• The value of the chunk\_size expression must be the same for all threads in the team.

• If runtime or auto is specified for kind, chunk\_size must not be specified.

• The nonmonotonic ordering-modifier cannot be specified if an ordered clause is specified on the same construct.

## Cross References

• do Construct, see Section 13.6.2

• for Construct, see Section 13.6.1

• run-sched-var ICV, see Table 3.1

• ordered Clause, see Section 6.4.6
