12.2 teams Construct

<table><tr><td>Name: teamsCategory: executable</td><td>Association: blockProperties: parallelism-generating, team-generating, thread-limiting, context-matching</td></tr></table>

## Clauses

allocate, default, firstprivate, if, num\_teams, private, reduction, shared, thread\_limit

## Binding

The binding thread set for a teams region is the encountering thread.

## Semantics

When a thread encounters a teams construct, a league of teams is created. Each team is an initial team, and the initial thread in each team executes the teams region. The number of teams created is determined by evaluating the if and num\_teams clauses. Once the teams are created, the number of initial teams are region-invariant , thus do not change for the duration of the teams region. Within a teams region, initial team numbers uniquely identify each initial team. Initial teams numbers are consecutive non-negative integers ranging from zero to one less than the number of initial teams.

When an if clause is present on a teams construct and the if clause expression evaluates to false, the number of formed teams is one. The use of a variable in an if clause expression of a teams construct causes an implicit reference to the variable in all enclosing constructs. The if clause expression is evaluated in the context outside of the teams construct.

If a thread\_limit clause is not present on the teams construct, but the construct is closely nested inside a target construct on which the thread\_limit clause is specified, the behavior is as if that thread\_limit clause is also specified for the teams construct.

The place list, given by the place-partition-var ICV of the encountering thread, is split into subpartitions in an implementation defined manner, and each team is assigned to a subpartition by setting the place-partition-var of its initial thread to the subpartition.

The teams construct sets the default-device-var ICV for each initial thread to an implementation defined value.

After the teams have completed execution of the teams region, the encountering task resumes execution of the enclosing task region.

## Execution Model Events

The teams-begin event occurs in a thread that encounters a teams construct before any initial task is generated for the corresponding teams region.

Upon generation of each initial task, an initial-task-begin event occurs in the thread that executes the initial task after the initial task is fully initialized but before the thread begins to execute the structured block of the teams construct.

If a new native thread is created for the league of teams that executes the teams region upon encountering the construct, a native-thread-begin event occurs as the first event in the context of the new thread prior to the initial-task-begin event.

When a thread completes an initial task, an initial-task-end event occurs in the thread.

The teams-end event occurs in the thread that encounters the teams construct after the thread executes its initial-task-end event but before it resumes execution of the encountering task.

If a native thread is destroyed at the end of a teams region, a native-thread-end event occurs in the initial thread that uses the native thread as the last event prior to destruction of the native thread.

## Tool Callbacks

A thread dispatches a registered parallel\_begin callback for each occurrence of a teams-begin event in that thread. The callback occurs in the task that encounters the teams construct. In the dispatched callback, (flags & ompt\_parallel\_league) evaluates to true.

A thread dispatches a registered implicit\_task callback with ompt\_scope\_begin as its endpoint argument for each occurrence of an initial-task-begin event in that thread. Similarly, a thread dispatches a registered implicit\_task callback with ompt\_scope\_end as its endpoint argument for each occurrence of an initial-task-end event in that thread. The callbacks occur in the context of the initial task. In the dispatched callback,

(flags & ompt\_task\_initial) and (flags & ompt\_task\_implicit) evaluate to true.

A thread dispatches a registered parallel\_end callback for each occurrence of a teams-end event in that thread. The callback occurs in the task that encounters the teams construct.

A thread dispatches a registered thread\_begin callback for each native-thread-begin event in that thread. The callback occurs in the context of the thread.

A thread dispatches a registered thread\_end callback for each native-thread-end event in that thread. The callback occurs in the context of the thread.

## Restrictions

Restrictions to the teams construct are as follows:

• If a reduction-modifier is specified in a reduction clause that appears on the directive then the reduction-modifier must be default.

• A teams region must be a strictly nested region of the implicit parallel region that surrounds the whole OpenMP program or a target region. If a teams region is nested inside a target region, the corresponding target construct must not contain any statements, declarations or directives outside of the corresponding teams construct.

• For a teams construct that is an immediately nested construct of a target construct, the bounds expressions of any array sections and the index expressions of any array elements used in any clause on the construct, as well as all expressions of any target-consistent clauses on the construct, must be target-consistent expressions.

• Only regions that are generated by teams-nestable constructs or teams-nestable routines may be strictly nested regions of teams regions.

## Cross References

• allocate Clause, see Section 8.6

• default Clause, see Section 7.5.1

• distribute Construct, see Section 13.7

• firstprivate Clause, see Section 7.5.4

• default-device-var ICV, see Table 3.1

• place-partition-var ICV, see Table 3.1

• if Clause, see Section 5.5

• implicit\_task Callback, see Section 34.5.3

• num\_teams Clause, see Section 12.2.1

• omp\_get\_num\_teams Routine, see Section 22.1

• omp\_get\_team\_num Routine, see Section 22.3

• parallel Construct, see Section 12.1

• parallel\_begin Callback, see Section 34.3.1

• parallel\_end Callback, see Section 34.3.2

• OMPT parallel\_flag Type, see Section 33.22

• private Clause, see Section 7.5.3

• reduction Clause, see Section 7.6.10

• OMPT scope\_endpoint Type, see Section 33.27

• shared Clause, see Section 7.5.2

• target Construct, see Section 15.8

• OMPT task\_flag Type, see Section 33.37

• thread\_begin Callback, see Section 34.1.3

• thread\_end Callback, see Section 34.1.4

• thread\_limit Clause, see Section 15.3

<table><tr><td colspan="2">Name: num_teams</td><td colspan="2">Properties: target-consistent, unique</td></tr><tr><td colspan="4">Arguments</td></tr><tr><td>Name</td><td>Type</td><td colspan="2">Properties</td></tr><tr><td>upper-bound</td><td>expression of integer type</td><td colspan="2">positive</td></tr><tr><td colspan="4">Modifiers</td></tr><tr><td>Name</td><td>Modifies</td><td>Type</td><td>Properties</td></tr><tr><td>lower-bound</td><td>upper-bound</td><td>OpenMP integer expression</td><td>positive, ultimate, unique</td></tr><tr><td>directive-name-modifier</td><td>all arguments</td><td>Keyword: directive-name (a directive name)</td><td>unique</td></tr></table>

12.2.1 num\_teams Clause

## Directives

## teams

## Semantics

The num\_teams clause specifies the bounds on the number of teams formed by the construct on which it appears. lower-bound specifies the lower bound and upper-bound specifies the upper bound on the number of teams requested. If lower-bound is not specified, the efect is as if lower-bound is specified as equal to upper-bound. The number of teams formed is implementation defined, but it will be greater than or equal to the lower bound and less than or equal to the upper bound.

If the num\_teams clause is not specified on a construct then the efect is as if upper-bound was specified as follows. If the value of the nteams-var ICV is greater than zero, the efect is as if upper-bound was specified as an implementation defined value greater than zero but less than or equal to the value of the nteams-var ICV. Otherwise, the efect is as if upper-bound was specified as an implementation defined value greater than or equal to one.

## Restrictions
