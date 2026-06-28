
This section describes constructs and clauses in OpenMP that support the specification and enforcement of dependences. OpenMP supports two kinds of dependences: task dependences, which enforce orderings between dependence-compatible tasks; and doacross dependences, which enforce orderings between doacross iterations of a loop.

## 17.9.1 task-dependence-type Modifier

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>task-dependence-type</td><td>all arguments</td><td>Keyword:depobj, in,inout, inoutset, mutexinoutset, out</td><td>unique</td></tr></table>

## Clauses

depend, update

## Semantics

Clauses that are related to task dependences use the task-dependence-type modifier to identify the type of dependence relevant to that clause. The efect of the type of dependence is associated with locator list items as described with the depend clause, see Section 17.9.5.

## Cross References

• depend Clause, see Section 17.9.5

• update Clause, see Section 17.9.4

## 17.9.2 Depend Objects

Depend objects are OpenMP objects that can be used to supply user-computed dependences to depend clauses. Depend objects must be accessed only through the depobj construct, the depend clause and the asynchronous device routines; OpenMP programs that otherwise access depend objects are non-conforming programs. A depend object can be in one of the following states: uninitialized or initialized. Initially, depend objects are in the uninitialized state.

## 17.9.3 depobj Construct

<table><tr><td>Name: depobjCategory: executable</td><td>Association: unassociatedProperties: default</td></tr></table>

## Clauses

destroy, init, update

<table><tr><td colspan="2">Clause set</td></tr><tr><td>Properties: required</td><td>Members: destroy, init, update</td></tr></table>

## Additional information

The depobj construct may alternatively be specified with a directive argument depend-object that is a depend object. If this syntax is used, the init clause must not be specified and instead the depend clause may be specified to initialize depend-object to represent a given dependence type and locator list item. With this syntax the update clause is only permitted to specify the task-dependence-type as if it is the sole argument of the clause, with the efect being that the specified dependence type applies to depend-object. With this syntax, any update-var or destroy-var that is specified in an update or destroy clause must be the same as depend-object. Finally, with this syntax only one clause may be specified and it must be depend, update, or destroy.

## Binding

The binding thread set for a depobj region is the encountering thread.

## Semantics

The depobj construct initializes, updates or destroys depend objects. If an init clause is specified, the state of the specified depend object is set to initialized and the depend object is set to represent the specified dependence type and locator list item. If an update clause is specified, the specified depend object is updated to represent the new dependence type. If a destroy clause is specified, the specified depend object is set to uninitialized.

## Cross References

• destroy Clause, see Section 5.7

• init Clause, see Section 5.6

• update Clause, see Section 17.9.4

## 17.9.4 update Clause

Modifiers

<table><tr><td>Name: update</td><td>Properties: innermost-leaf, unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>update-var</td><td>variable of OpenMP depend type</td><td>default</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>task-dependence-type</td><td>all arguments</td><td>Keyword:depobj, in,inout, inoutset, mutexinoutset, out</td><td>unique</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

depobj

## Semantics

The update clause sets the dependence type of update-var to task-dependence-type.

## Restrictions

Restrictions to the update clause are as follows:

• task-dependence-type must not be depobj.

• The state of update-var must be initialized.

• If the locator list item represented by update-var is the omp\_all\_memory reserved locator, task-dependence-type must be either out or inout.

## Cross References

• depobj Construct, see Section 17.9.3

• task-dependence-type Modifier, see Section 17.9.1

## 17.9.5 depend Clause

<table><tr><td>Name: depend</td><td>Properties: taskgraph-altering, task-inherited</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>locator-list</td><td>list of locator list item type</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>task-dependence-type</td><td>all arguments</td><td>Keyword:depobj, in,inout, inoutset, mutexinoutset, out</td><td>unique</td></tr><tr><td>iterator</td><td>locator-list</td><td>Complex, name:iteratorArguments:iterator-specifierlist of iterator specifier list item type (default)</td><td>unique</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

dispatch, interop, target, target\_data, target\_enter\_data, target\_exit\_data, target\_update, task, task\_iteration, taskwait

## Semantics

The depend clause enforces additional constraints on the scheduling of tasks. These constraints establish dependences only between two dependence-compatible tasks: the antecedent task and the dependent task. The scheduling constraints are transitive so that the antecedent task must complete execution before any of its successor tasks execute. Similarly, the dependent task cannot start execution before all of its predecessor tasks complete execution. Task dependences are derived from the task-dependence-type and the list items in the locator-list argument.

One task, A, is a preceding dependence-compatible task of another task, B, if one of the following is true:

• A is a previously generated sibling task of B;

• A is a preceding dependence-compatible task of an importing task for which B is a child task;

• A is a child task of an exporting task that is a predecessor task of B;

• A is a child task of an undeferred exporting task that is a previously generated sibling task of B.

The storage location of a list item matches the storage location of another list item if they have the same storage location, or if any of the list items is omp\_all\_memory.

For the in task-dependence-type, if the storage location of at least one of the list items matches the storage location of a list item appearing in a depend clause with an out, inout, mutexinoutset, or inoutset task-dependence-type on a construct from which a preceding dependence-compatible task was generated then the generated task will be a dependent task of that preceding dependence-compatible task.

For the out task-dependence-type and inout task-dependence-type, if the storage location of at least one of the list items matches the storage location of a list item appearing in a depend clause with an in, out, inout, mutexinoutset, or inoutset task-dependence-type on a construct from which a preceding dependence-compatible task was generated then the generated task will be a dependent task of that preceding dependence-compatible task.

For the mutexinoutset task-dependence-type, if the storage location of at least one of the list items matches the storage location of a list item appearing in a depend clause with an in, out, inout, or inoutset task-dependence-type on a construct from which a preceding dependence-compatible task was generated then the generated task will be a dependent task of that preceding dependence-compatible task.

If a list item appearing in a depend clause with a mutexinoutset task-dependence-type on a task-generating construct matches a list item appearing in a depend clause with a mutexinoutset task-dependence-type on a diferent task-generating construct, and both constructs generate dependence-compatible tasks, the dependence-compatible tasks will be mutually exclusive tasks.

For the inoutset task-dependence-type, if the storage location of at least one of the list items matches the storage location of a list item appearing in a depend clause with an in, out, inout, or mutexinoutset task-dependence-type on a construct from which a preceding dependence-compatible task was generated then the generated task will be a dependent task of that preceding dependence-compatible task.

When the task-dependence-type is depobj, the behavior is as if the dependence type and locator list item that each specified depend object list item represents was specified by depend clauses on the current construct.

The list items that appear in the depend clause may reference any iterator-identifier defined in its iterator modifier.

The list items that appear in the depend clause may include array sections or the omp\_all\_memory reserved locator.

C / C++

The list items that appear in a depend clause may use shape-operators.

C / C++

Note – The enforced task dependence establishes a synchronization of memory accesses performed by a dependent task with respect to accesses performed by the antecedent tasks. However, the programmer must properly synchronize with respect to other concurrent accesses that occur outside of those tasks.

## Execution Model Events

The task-dependences event occurs in a thread that encounters a task-generating construct or a taskwait construct with a depend clause immediately after the task-create event for the generated task or the taskwait-init event. The task-dependence event indicates an unfulfilled dependence for the generated task. This event occurs in a thread that observes the unfulfilled dependence before it is satisfied.

## Tool Callbacks

A thread dispatches the dependences callback for each occurrence of the task-dependences event to announce its dependences with respect to the list items in the depend clause. A thread dispatches the task\_dependence callback for a task-dependence event to report a dependence between a antecedent task (src\_task\_data) and a dependent task (sink\_task\_data).

## Restrictions

Restrictions to the depend clause are as follows:

• List items, other than reserved locators, used in depend clauses of the same task or dependence-compatible tasks must indicate identical storage locations or disjoint storage locations.

• List items used in depend clauses cannot be zero-length array sections.

• The omp\_all\_memory reserved locator can only be used in a depend clause with an out or inout task-dependence-type.

• Array sections cannot be specified in depend clauses with the depobj task-dependence-type.

• List items used in depend clauses with the depobj task-dependence-type must be expressions of the depend OpenMP type that correspond to depend objects in the initialized state.

• List items that are expressions of the depend OpenMP type can only be used in depend clauses with the depobj task-dependence-type.

Fortran

• A common block name cannot appear in a depend clause.

• If a locator list item has the ALLOCATABLE attribute and its allocation status is unallocated, the behavior is unspecified.

• If a locator list item has the POINTER attribute and its association status is disassociated or undefined, the behavior is unspecified.

Fortran

C / C++

• A bit-field cannot appear in a depend clause.

C / C++

## Cross References

• dependences Callback, see Section 34.7.1

• dispatch Construct, see Section 9.7

• Array Sections, see Section 5.2.5

• Array Shaping, see Section 5.2.4

• interop Construct, see Section 16.1

• iterator Modifier, see Section 5.2.6

• task-dependence-type Modifier, see Section 17.9.1

• target Construct, see Section 15.8

• target\_data Construct, see Section 15.7

• target\_enter\_data Construct, see Section 15.5

• target\_exit\_data Construct, see Section 15.6

• target\_update Construct, see Section 15.9

• task Construct, see Section 14.1

• task\_dependence Callback, see Section 34.7.2

• task\_iteration Directive, see Section 14.2.3

• taskwait Construct, see Section 17.5

## 17.9.6 transparent Clause

<table><tr><td>Name: transparent</td><td>Properties: unique</td></tr></table>

Modifiers  
Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>impex-type</td><td>expression of impexOpenMP type</td><td>optional</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

target\_data, task, taskloop

## Semantics

The transparent clause controls the task dependence importing and exporting characteristics of any generated tasks of the construct on which it appears. If impex-type evaluates to omp\_not\_impex then the generated tasks are neither importing tasks nor exporting tasks and so are not transparent tasks. Otherwise the clause extends the set of dependence-compatible tasks of any child task of any of the generated tasks as follows. If impex-type evaluates to omp\_import then the generated tasks are importing tasks. If impex-type evaluates to omp\_export then the generated tasks are exporting tasks. If impex-type evaluates to omp\_impex then the generated tasks are both importing tasks and exporting tasks.

The use of a variable in an impex-type expression causes an implicit reference to the variable in all enclosing constructs. The impex-type expression is evaluated in the context outside of the construct on which the clause appears. If impex-type is not specified, the efect is as if impex-type evaluates to omp\_impex.

## Cross References

• depend Clause, see Section 17.9.5

• target\_data Construct, see Section 15.7

• task Construct, see Section 14.1

• taskloop Construct, see Section 14.2

## 17.9.7 doacross Clause

<table><tr><td>Name: doacross</td><td>Properties: required</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>iteration-specifier</td><td>OpenMP iteration specifier</td><td>default</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>dependence-type</td><td>iteration-specifier</td><td>Keyword: sink, source</td><td>required</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

ordered

## Semantics

The doacross clause identifies doacross dependences that imply additional constraints on the scheduling of doacross logical iterations of a doacross loop nest. These constraints establish dependences only between doacross iterations. The iteration-specifier specifies a doacross iteration and is either a loop-iteration vector or uses the omp\_cur\_iteration keyword (see Section 6.4.3).

The source dependence-type specifies that the current doacross iteration is a source iteration and, thus, satisfies doacross dependences that arise from the current doacross iteration. If the source dependence-type is specified then the iteration-specifier argument is optional; if iteration-specifier is omitted, it is assumed to be omp\_cur\_iteration.

The sink dependence-type specifies the current doacross iteration is a sink iteration and, thus, has a doacross dependence, where iteration-specifier indicates the doacross iteration that satisfies the dependence. If iteration-specifier indicates a doacross iteration that does not occur in the doacross iteration space, the doacross clause is ignored. If all doacross clauses on an ordered construct are ignored then the construct is ignored.

Note – If the sink dependence-type is specified for an iteration-specifier that does not indicate an earlier iteration of the doacross iteration space, deadlock may occur.

## Restrictions

Restrictions to the doacross clause are as follows:

• If iteration-specifier is a loop-iteration vector that has n elements, the innermost loop-nest-associated construct that encloses the construct on which the clause appears must specify an ordered clause for which the parameter value equals n.

• If iteration-specifier is specified with the omp\_cur\_iteration keyword and with sink as the dependence-type then it must be omp\_cur\_iteration - 1.

• If iteration-specifier is specified with source as the dependence-type then it must be omp\_cur\_iteration.

• If iteration-specifier is a loop-iteration vector and the sink dependence-type is specified then for each element, if the loop-iteration variable var<sub>i</sub> has an integral or pointer type, the i<sup>th</sup> expression of vector must be computable without overflow in that type for any value of var<sub>i</sub> that can encounter the construct on which the doacross clause appears.

C++

• If iteration-specifier is a loop-iteration vector and the sink dependence-type is specified then for each element, if the loop-iteration variable var<sub>i</sub> is of a random access iterator type other than pointer type, the i<sup>th</sup> expression of vector must be computable without overflow in the type that would be used by std::distance applied to variables of the type of var<sub>i</sub> for any value of var<sub>i</sub> that can encounter the construct on which the doacross clause appears.

## Cross References

• OpenMP Loop-Iteration Spaces and Vectors, see Section 6.4.3

• ordered Clause, see Section 6.4.6

• Stand-alone ordered Construct, see Section 17.10.1

## 17.10 ordered Construct

This section describes two forms for the ordered construct, the stand-alone ordered construct and the block-associated ordered construct. Both forms include the execution model events, too callbacks, and restrictions listed in this section.

## Execution Model Events

The ordered-acquiring event occurs in the task that encounters the ordered construct on entry to the ordered region before it initiates synchronization for the region. The ordered-released event occurs in the task that encounters the ordered construct after it completes any synchronization on exit from the region.

## Tool Callbacks

A thread dispatches a registered mutex\_acquire callback for each occurrence of an ordered-acquiring event in that thread. A thread dispatches a registered mutex\_released callback with ompt\_mutex\_ordered as the kind argument if practical, although a less specific kind may be used, for each occurrence of an ordered-released event in that thread. These callback occur in the task that encounters the construct.

## Restrictions

• The construct that corresponds to the binding region of an ordered region must specify an ordered clause.

• The construct that corresponds to the binding region of an ordered region must not specify a reduction clause with the inscan modifier.

• The region of a block-associated ordered construct must not have a binding region that corresponds to a construct in which a stand-alone ordered construct is closely nested.

• An ordered region that corresponds to an ordered construct with the threads or doacross clause may not be closely nested inside a critical, ordered, loop, task, or taskloop region (see Section 17.10).

• The doacross-afected loops of a doacross loop nest must be perfectly nested loops.

• The construct that corresponds to the binding region of an ordered region must not specify a linear clause.

![](images/c29111664804fd659b9e1774d41d7fc80a8895ed26f06795443dd89e7691a2b5.jpg)

• The doacross-afected loops of a doacross loop nest must not be range-based for loops.

![](images/7845d0fa9ef29560ecab0e2ebdd36b683e0a0df010743d23b627a03907e6275d.jpg)

## Cross References

• OMPT mutex Type, see Section 33.20

• mutex\_acquire Callback, see Section 34.7.8

• mutex\_released Callback, see Section 34.7.13

## 17.10.1 Stand-alone ordered Construct

<table><tr><td>Name: orderedCategory: executable</td><td>Association: unassociatedProperties: mutual-exclusion</td></tr></table>

## Clauses

doacross

## Binding

The binding thread set for a stand-alone ordered region is the current team. A stand-alone ordered region binds to the innermost enclosing worksharing-loop region.

## Semantics

The innermost enclosing worksharing-loop construct of a stand-alone ordered construct is associated with a doacross loop nest of the n doacross-afected loops. The stand-alone ordered construct specifies that execution must not violate doacross dependences as specified in the doacross clauses that appear on the construct. When a thread that is executing a doacross iteration encounters an ordered construct with one or more doacross clauses for which the sink dependence-type is specified, the thread waits until its dependences on all valid doacross iterations specified by the doacross clauses are satisfied before it continues execution. A specific dependence is satisfied when a thread that is executing the corresponding doacross iteration encounters an ordered construct with a doacross clause for which the source dependence-type is specified.

## Execution Model Events

The doacross-sink event occurs in the task that encounters an ordered construct for each doacross clause for which the sink dependence-type is specified after the dependence is fulfilled. The doacross-source event occurs in the task that encounters an ordered construct with a doacross clause for which the source dependence-type is specified before signaling that the dependence has been fulfilled.

## Tool Callbacks

A thread dispatches a registered dependences callback with all vector entries listed as ompt\_dependence\_type\_sink in the deps argument for each occurrence of a doacross-sink event in that thread. A thread dispatches a registered dependences callback with all vector entries listed as ompt\_dependence\_type\_source in the deps argument for each occurrence of a doacross-source event in that thread.

## Restrictions

Additional restrictions to the stand-alone ordered construct are as follows:

• At most one doacross clause may appear on the construct with source as the dependence-type.

• All doacross clauses that appear on the construct must specify the same dependence-type.

• The construct must not be an orphaned construct.

• The construct must be closely nested inside a worksharing-loop construct.

## Cross References

• OMPT dependence\_type Type, see Section 33.10

• dependences Callback, see Section 34.7.1

• doacross Clause, see Section 17.9.7

• Worksharing-Loop Constructs, see Section 13.6

## 17.10.2 Block-associated ordered Construct

<table><tr><td>Name: orderedCategory:executable</td><td>Association: blockProperties: mutual-exclusion, simdizable, thread-limiting, thread-exclusive</td></tr></table>

## Clause groups

parallelization-level

## Binding

The binding thread set for a block-associated ordered region is the current team. A block-associated ordered region binds to the innermost enclosing region that corresponds to a construct for which a worksharing-loop construct or simd construct is a constituent construct.

## Semantics

If no clauses are specified, the efect is as if the threads parallelization-level clause was specified. If the threads clause is specified, the threads in the team that is executing the worksharing-loop region execute ordered regions sequentially in the order of the collapsed iterations. If the simd parallelization-level clause is specified, the ordered regions encountered by any thread will execute one at a time in the order of the collapsed iterations. With either parallelization-level, execution of code outside the region for diferent collapsed iterations can run in parallel; execution of that code within the same collapsed iteration must observe any constraints imposed by the base language semantics.

When the thread that is executing the first collapsed iteration of the loop encounters a block-associated ordered construct, it can enter the ordered region without waiting. When a thread that is executing any subsequent collapsed iteration encounters a block-associated ordered construct, it waits at the beginning of the ordered region until execution of all ordered regions that belong to all previous collapsed iterations has completed. ordered regions that bind to diferent regions execute independently of each other.

## Execution Model Events

The ordered-acquired event occurs in the task that encounters the ordered construct after it enters the region, but before it executes the associated structured block.

## Tool Callbacks

A thread dispatches a registered mutex\_acquired callback for each occurrence of an ordered-acquired event in that thread. This callback occurs in the task that encounters the construct.

## Restrictions

Additional restrictions to the block-associated ordered construct are as follows:

• The construct is SIMDizable only if the simd parallelization-level clause is specified.

• If the simd parallelization-level clause is specified, the binding region must correspond to a construct for which the simd construct is a leaf construct.

• If the threads parallelization-level clause is specified, the binding region must correspond to a construct for which a worksharing-loop construct is a leaf construct.

• If the threads parallelization-level clause is specified and the binding region corresponds to a compound construct then the simd construct must not be a leaf construct unless the simd parallelization-level clause is also specified.

• During execution of the collapsed iteration associated with a loop-nest-associated directive, a thread must not execute more than one block-associated ordered region that binds to the corresponding region of the loop-nest-associated directive.

• An ordered clause with an argument value equal to the number of collapsed loops must appear on the construct that corresponds to the binding region, if the binding region is not a simd region.

## Cross References

• parallelization-level Clauses, see Section 17.10.3

• Worksharing-Loop Constructs, see Section 13.6

• mutex\_acquired Callback, see Section 34.7.12

• ordered Clause, see Section 6.4.6

• simd Construct, see Section 12.4

## 17.10.3 parallelization-level Clauses

Clause groups

<table><tr><td>Properties: unique</td><td>Members:Clausessimd, threads</td></tr></table>

## Directives

ordered

## Semantics

The parallelization-level clause group defines a set of clauses that indicate the level of parallelization with which to associate a construct.

## Cross References

• Block-associated ordered Construct, see Section 17.10.2

## 17.10.3.1 threads Clause

<table><tr><td>Name: threads</td><td>Properties: innermost-leaf, unique</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>apply-to-threads</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

Modifiers

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

ordered

## Semantics

If apply\_to\_threads evaluates to true, the efect is as if the threads parallelization-level clause is specified. If apply\_to\_threads evaluates to false, the efect is as if the threads clause is not specified. If apply\_to\_threads is not specified, the efect is as if apply\_to\_threads evaluates to true.

## Cross References

• Block-associated ordered Construct, see Section 17.10.2

## 17.10.3.2 simd Clause

Arguments

<table><tr><td>Name: simd</td><td>Properties: innermost-leaf, unique</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>apply-to-simd</td><td>expression of OpenMP logical type</td><td>constant, optional</td></tr></table>

<table><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

## Directives

ordered

## Semantics

If apply\_to\_simd evaluates to true, the efect is as if the simd parallelization-level clause is specified. If apply\_to\_simd evaluates to false, the efect is as if the simd clause is not specified. If apply\_to\_simd is not specified, the efect is as if apply\_to\_simd evaluates to true.

## Cross References

• Block-associated ordered Construct, see Section 17.10.2
