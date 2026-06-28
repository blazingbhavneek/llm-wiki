
This section describes callbacks that are related to tasks.

## 34.5.1 task\_create Callback

<table><tr><td>Name: task_createCategory: subroutine</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>encountering_task_data</td><td>data</td><td>OMPT, pointer</td></tr><tr><td>encountering_task_frame</td><td>frame</td><td>intent(in), OMPT, pointer, untraced-argument</td></tr><tr><td>new_task_data</td><td>data</td><td>OMPT, pointer</td></tr><tr><td>flags</td><td>integer</td><td>default</td></tr><tr><td>has_dependencies</td><td>integer</td><td>default</td></tr><tr><td>codeptr_ra</td><td>void</td><td>intent(in), pointer</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_callback\_task\_create\_t) ( ompt\_data\_t \*encountering\_task\_data, const ompt\_frame\_t \*encountering\_task\_frame, ompt\_data\_t \*new\_task\_data, int flags, int has\_dependences, const void \*codeptr\_ra);

C / C++

## Trace Record

C / C++

typedef struct ompt\_record\_task\_create\_t {

ompt\_id\_t encountering\_task\_id;

int has\_dependences;

const void <sub>\*</sub>codeptr\_ra;

} ompt\_record\_task\_create\_t;

C / C++

## Semantics

A tool provides a task\_create callback, which has the task\_create OMPT type, that the OpenMP implementation dispatches when task regions are generated. The binding of the new\_task\_data argument is the generated task. The flags argument indicates the kind of task (explicit task or target task) that is generated. Values for flags are a disjunction of elements in the task\_flag OMPT type. The has\_dependences argument is true if the generated task has dependences and false otherwise.

## Cross References

• OMPT data Type, see Section 33.8

• OMPT frame Type, see Section 33.15

• Initial Task, see Section 14.13

• OMPT id Type, see Section 33.18

• task Construct, see Section 14.1

• OMPT task\_flag Type, see Section 33.37

## 34.5.2 task\_schedule Callback

<table><tr><td>Name: task_scheduleCategory: subroutine</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>prior_task_data</td><td>data</td><td>OMPT, pointer</td></tr><tr><td>prior_task_status</td><td>task_status</td><td>OMPT</td></tr><tr><td>next_task_data</td><td>data</td><td>OMPT, pointer</td></tr></table>

## Type Signature

typedef void (<sub>\*</sub>ompt\_callback\_task\_schedule\_t) ( ompt\_data\_t \*prior\_task\_data, ompt\_task\_status\_t prior\_task\_status, ompt\_data\_t \*next\_task\_data);

## Trace Record

C / C++

typedef struct ompt\_record\_task\_schedule\_t { ompt\_id\_t prior\_task\_id; ompt\_task\_status\_t prior\_task\_status; ompt\_id\_t next\_task\_id; } ompt\_record\_task\_schedule\_t;

## C / C++

## Semantics

A tool provides a task\_schedule callback, which has the task\_schedule OMPT type, that the OpenMP implementation dispatches when task scheduling decisions are made. The binding of the prior\_task\_data argument is the task that arrived at the task scheduling point. This argument can be NULL if no task was active when the next task is scheduled. The prior\_task\_status argument indicates the status of that prior task. The binding of the next\_task\_data argument is the task that is resumed at the task scheduling point. This argument is NULL if the callback is dispatched for a task-fulfill event or if the callback signals completion of a taskwait construct. This argument can be NULL if no task was active when the prior task was scheduled.

## Cross References

• OMPT data Type, see Section 33.8

• Task Scheduling, see Section 14.14

• OMPT id Type, see Section 33.18

• OMPT task\_status Type, see Section 33.38

## 34.5.3 implicit\_task Callback

<table><tr><td>Name: implicit_taskCategory: subroutine</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>endpoint</td><td>scope_endpoint</td><td>OMPT</td></tr><tr><td>parallel_data</td><td>data</td><td>OMPT, pointer</td></tr><tr><td>task_data</td><td>data</td><td>OMPT, pointer</td></tr><tr><td>actual_parallelism</td><td>integer</td><td>unsigned</td></tr><tr><td>index</td><td>integer</td><td>unsigned</td></tr><tr><td>flags</td><td>integer</td><td>default</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_callback\_implicit\_task\_t) ( ompt\_scope\_endpoint\_t endpoint, ompt\_data\_t <sub>\*</sub>parallel\_data, ompt\_data\_t \*task\_data, unsigned int actual\_parallelism, unsigned int index, int flags);

C / C++

## Trace Record

C / C++

typedef struct ompt\_record\_implicit\_task\_t { ompt\_scope\_endpoint\_t endpoint; ompt\_id\_t parallel\_id; ompt\_id\_t task\_id; unsigned int actual\_parallelism; unsigned int index; int flags; } ompt\_record\_implicit\_task\_t;

C / C++

## Semantics

A tool provides an implicit\_task callback, which has the implicit\_task OMPT type, that the OpenMP implementation dispatches when initial tasks and implicit tasks are generated and completed. The flags argument, which has the task\_flag OMPT type, indicates the kind of task (initial task or implicit task). For the implicit-task-end and the initial-task-end events, the parallel\_data argument is NULL.

The actual\_parallelism argument indicates the number of threads in the parallel region or the number of teams in the teams region. For initial tasks that are not closely nested in a teams construct, this argument is 1. For the implicit-task-end and the initial-task-end events, this argument is 0.

The index argument indicates the thread number or team number of the calling thread, within the team or league that is executing the parallel region or teams region to which the implicit task region binds. For initial tasks that are not created by a teams construct, this argument is 1.

## Cross References

• OMPT data Type, see Section 33.8

• OMPT id Type, see Section 33.18

• parallel Construct, see Section 12.1

• OMPT scope\_endpoint Type, see Section 33.27

• OMPT task\_flag Type, see Section 33.37

• teams Construct, see Section 12.2

## 34.6 cancel Callback

<table><tr><td colspan="2">Name: cancelCategory: subroutine</td><td>Properties: C/C++-only, OMPT</td></tr><tr><td colspan="3">Arguments</td></tr><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>task_data</td><td>data</td><td>OMPT, pointer</td></tr><tr><td>flags</td><td>integer</td><td>default</td></tr><tr><td>codeptr_ra</td><td>void</td><td>intent(in), pointer</td></tr><tr><td colspan="3">Type SignatureC / C++typedef void (*empt_callback_cancel_t) (empt_data_t *task_data,int flags, const void *codeptr_ra);C / C++Trace RecordC / C++typedef struct empt_record_cancel_t {empt_id_t task_id;int flags;const void *codeptr_ra;} empt_record_cancel_t;C / C++</td></tr></table>

## Semantics

A tool provides a cancel callback, which has the cancel OMPT type, that the OpenMP implementation dispatches when cancellation, cancel and discarded-task events occur. The flags argument, which is defined by the cancel\_flag OMPT type, indicates whether cancellation is activated by the encountering task or detected as being activated by another task. The construct that is being canceled is also described in the flags argument. When several constructs are detected as being concurrently canceled, each corresponding bit in the argument will be set.

## Cross References

• OMPT cancel\_flag Type, see Section 33.7

• OMPT data Type, see Section 33.8

• OMPT id Type, see Section 33.18

## 34.7 Synchronization Callback Signatures

This section describes callbacks that are related to synchronization constructs and clauses.

## 34.7.1 dependences Callback

<table><tr><td>Name: dependencesCategory: subroutine</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>task_data</td><td>data</td><td>OMPT, pointer</td></tr><tr><td>deps</td><td>dependence</td><td>intent(in), pointer</td></tr><tr><td>ndeps</td><td>integer</td><td>default</td></tr></table>

## Type Signature

typedef void (<sub>\*</sub>ompt\_callback\_dependences\_t) (

ompt\_data\_t <sub>\*</sub>task\_data, const ompt\_dependence\_t <sub>\*</sub>deps, int ndeps);

C / C++

## Trace Record

C / C++

typedef struct ompt\_record\_dependences\_t {

ompt\_id\_t task\_id;

ompt\_dependence\_t dep;

int ndeps;

} ompt\_record\_dependences\_t;

C / C++

## Semantics

A tool provides a dependences callback, which has the dependences OMPT type, that the OpenMP implementation dispatches when tasks are generated and when ordered constructs are encountered. The binding of the task\_data argument is the generated task for a depend clause on a task construct, the target task for a depend clause on a device construct, the depend object in an asynchronous routine, or the encountering task for a doacross clause of the ordered

construct. The deps argument points to an array of structures of dependence OMPT type that represent dependences of the generated task or the iteration-specifier of the doacross clause. Dependences denoted with depend objects are described in terms of their dependence semantics. The ndeps argument specifies the length of the list passed by the deps argument. The memory for deps is owned by the caller; the tool cannot rely on the data after the callback returns.

When the implementation logs dependences trace records for a given event, the ndeps field determines the number of trace records that are logged, one for each dependence. The dep field in a given trace record denotes a structure of dependence OMPT type that represents the dependence.

## Cross References

• OMPT data Type, see Section 33.8

• depend Clause, see Section 17.9.5

• OMPT dependence Type, see Section 33.9

• OMPT id Type, see Section 33.18

• Stand-alone ordered Construct, see Section 17.10.1

## 34.7.2 task\_dependence Callback

<table><tr><td colspan="2">Name: task_dependenceCategory: subroutine</td><td>Properties: C/C++-only, OMPT</td></tr><tr><td colspan="3">Arguments</td></tr><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>src_task_data</td><td>data</td><td>OMPT, pointer</td></tr><tr><td>sink_task_data</td><td>data</td><td>OMPT, pointer</td></tr><tr><td colspan="3">Type SignatureC / C++typedef void (*ompt_callback_task_dependence_t) (empt_data_t *src_task_data, empt_data_t *sink_task_data);C / C++Trace RecordC / C++typedef struct empt_record_task_dependence_t {empt_id_t src_task_id;empt_id_t sink_task_id;} empt_record_task_dependence_t;C / C++</td></tr></table>

## Semantics

A tool provides a task\_dependence callback, which has the task\_dependence OMPT type, that the OpenMP implementation dispatches when it encounters an unfulfilled task dependence. The binding of the src\_task\_data argument is an uncompleted antecedent task. The binding of the sink\_task\_data argument is a corresponding dependent task.

## Cross References

• OMPT data Type, see Section 33.8

• depend Clause, see Section 17.9.5

• OMPT id Type, see Section 33.18

## 34.7.3 OMPT sync\_region Type

<table><tr><td>Name: sync_regionCategory: subroutine pointer</td><td>Properties: C/C++-only, OMPT, overlapping-type-name</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>kind</td><td>sync_region</td><td>OMPT</td></tr><tr><td>endpoint</td><td>scope_endpoint</td><td>OMPT</td></tr><tr><td>parallel_data</td><td>data</td><td>OMPT, pointer</td></tr><tr><td>task_data</td><td>data</td><td>OMPT, pointer</td></tr><tr><td>codeptr_ra</td><td>void</td><td>intent(in), pointer</td></tr></table>

## Type Signature

typedef void (<sub>\*</sub>ompt\_callback\_sync\_region\_t) ( ompt\_sync\_region\_t kind, ompt\_scope\_endpoint\_t endpoint, ompt\_data\_t \*parallel\_data, ompt\_data\_t \*task\_data, const void \*codeptr\_ra);

C / C++

## Trace Record

C / C++

typedef struct ompt\_record\_sync\_region\_t { ompt\_sync\_region\_t kind; ompt\_scope\_endpoint\_t endpoint; ompt\_id\_t parallel\_id; ompt\_id\_t task\_id; const void <sub>\*</sub>codeptr\_ra; } ompt\_record\_sync\_region\_t;

C / C++

## Semantics

Callbacks that have the sync\_region OMPT type are synchronizing-region callbacks, which each have the synchronizing-region property. A tool provides these callbacks to mark the beginning and end of regions that have synchronizing semantics. The kind argument, which has the sync\_region OMPT type, indicates the kind of synchronization.

## Cross References

• OMPT data Type, see Section 33.8

• OMPT id Type, see Section 33.18

• OMPT scope\_endpoint Type, see Section 33.27

• OMPT sync\_region Type, see Section 33.33

## 34.7.4 sync\_region Callback

<table><tr><td>Name: sync_regionCategory: subroutine</td><td>Properties: C/C++-only, common-type-callback, synchronizing-region, OMPT</td></tr></table>

## Type Signature sync\_region

## Semantics

A tool provides a sync\_region callback, which has the sync\_region OMPT type, that the OpenMP implementation dispatches when barrier regions, taskwait regions, and taskgroup regions begin and end. For the implicit-barrier-end event at the end of a parallel region, parallel\_data argument is NULL.

## Cross References

• barrier Construct, see Section 17.3.1

• Implicit Barriers, see Section 17.3.2

• OMPT sync\_region Type, see Section 34.7.3

• taskgroup Construct, see Section 17.4

• taskwait Construct, see Section 17.5

## 34.7.5 sync\_region\_wait Callback

<table><tr><td>Name: sync_region_waitCategory: subroutine</td><td>Properties: C/C++-only, common-type-callback, synchronizing-region, OMPT</td></tr></table>

## Type Signature

sync\_region

## Semantics

A tool provides a sync\_region\_wait callback, which has the sync\_region OMPT type, that the OpenMP implementation dispatches when waiting begins and ends for barrier regions, taskwait regions, and taskgroup regions. For the implicit-barrier-wait-begin and implicit-barrier-wait-end events at the end of a parallel region, whether parallel\_data is NULL or is the current parallel region is implementation defined.

## Cross References

• barrier Construct, see Section 17.3.1

• Implicit Barriers, see Section 17.3.2

• OMPT sync\_region Type, see Section 34.7.3

• taskgroup Construct, see Section 17.4

• taskwait Construct, see Section 17.5

## 34.7.6 reduction Callback

<table><tr><td>Name: reductionCategory: subroutine</td><td>Properties: C/C++-only, common-type-callback, synchronizing-region, OMPT</td></tr></table>

## Type Signature

sync\_region

## Semantics

A tool provides a reduction callback, which is a synchronizing-region callback, that the OpenMP implementation dispatches when it performs reductions.

## Cross References

• Properties Common to All Reduction Clauses, see Section 7.6.6

• OMPT sync\_region Type, see Section 34.7.3

## 34.7.7 OMPT mutex\_acquire Type

<table><tr><td>Name: mutex_acquireCategory: subroutine pointer</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>kind</td><td>mutex</td><td>OMPT, overlapping-type-name</td></tr><tr><td>hint</td><td>integer</td><td>unsigned</td></tr><tr><td>impl</td><td>integer</td><td>unsigned</td></tr><tr><td>wait_id</td><td>wait_id</td><td>OMPT</td></tr><tr><td>codeptr_ra</td><td>void</td><td>intent(in), pointer</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_callback\_mutex\_acquire\_t) (ompt\_mutex\_t kind, unsigned int hint, unsigned int impl, ompt\_wait\_id\_t wait\_id, const void \*codeptr\_ra);

C / C++

## Trace Record

C / C++

typedef struct ompt\_record\_mutex\_acquire\_t { ompt\_mutex\_t kind; unsigned int hint; unsigned int impl; ompt\_wait\_id\_t wait\_id; const void <sub>\*</sub>codeptr\_ra; } ompt\_record\_mutex\_acquire\_t;

C / C++

## Semantics

Callbacks that have the mutex\_acquire OMPT type are mutex-acquiring callbacks, which each have the mutex-acquiring property. A tool provides these callbacks to monitor the beginning of regions associated with mutual-exclusion constructs, lock-initializing routines and lock-acquiring routines. The kind argument, which has the mutex OMPT type, indicates the kind of mutual exclusion event. The hint argument indicates the hint that was provided when initializing an implementation of mutual exclusion. If no hint is available when a thread initiates acquisition of mutual exclusion, the runtime may supply omp\_sync\_hint\_none as the value for hint. The impl argument indicates the mechanism chosen by the runtime to implement the mutual exclusion.

## Cross References

• OMPT mutex Type, see Section 33.20

• OMPT wait\_id Type, see Section 33.40

## 34.7.8 mutex\_acquire Callback

<table><tr><td>Name: mutex_acquireCategory: subroutine</td><td>Properties: C/C++-only, common-type-callback, mutex-acquiring, OMPT</td></tr></table>

## Type Signature

## Semantics

A tool provides a mutex\_acquire callback, which has the mutex\_acquire OMPT type, that the OpenMP implementation dispatches when regions associated with mutual-exclusion constructs, lock-acquiring routines and lock-testing routines are begun.

## Cross References

• OMPT mutex\_acquire Type, see Section 34.7.7

## 34.7.9 lock\_init Callback

<table><tr><td>Name: lock_initCategory: subroutine</td><td>Properties: C/C++-only, common-type-callback, mutex-acquiring, OMPT</td></tr></table>

## Type Signature

## Semantics

A tool provides a lock\_init callback, which has the mutex\_acquire OMPT type, that the OpenMP implementation dispatches when lock-initializing routines are executed.

## Cross References

• OMPT mutex\_acquire Type, see Section 34.7.7

## 34.7.10 OMPT mutex Type

<table><tr><td>Name: mutexCategory: subroutine pointer</td><td>Properties: C/C++-only, OMPT, overlapping-type-name</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>kind</td><td>mutex</td><td>OMPT, overlapping-type-name</td></tr><tr><td>wait_id</td><td>wait_id</td><td>OMPT</td></tr><tr><td>codeptr_ra</td><td>void</td><td>intent(in), pointer</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_callback\_mutex\_t) (ompt\_mutex\_t kind, ompt\_wait\_id\_t wait\_id, const void <sub>\*</sub>codeptr\_ra);

C / C++

## Trace Record

C / C++

typedef struct ompt\_record\_mutex\_t { ompt\_mutex\_t kind; ompt\_wait\_id\_t wait\_id; const void <sub>\*</sub>codeptr\_ra; } ompt\_record\_mutex\_t;

C / C++

## Semantics

Callbacks that have the mutex OMPT type are mutex-execution callbacks, which each have the mutex-execution property. A tool provides these callbacks to monitor the execution of a lock-destroying routine or the beginning or completion of execution of either the structured block associated with a mutual-exclusion construct, or the region guarded by a lock-acquiring routine or lock-testing routine paired with a lock-releasing routine. The kind argument, which has the mutex OMPT type, indicates the kind of mutual exclusion event.

## Cross References

• Lock Acquiring Routines, see Section 28.3

• Lock Destroying Routines, see Section 28.2

• Lock Releasing Routines, see Section 28.4

• Lock Testing Routines, see Section 28.5

• OMPT mutex Type, see Section 33.20

• OMPT wait\_id Type, see Section 33.40

## 34.7.11 lock\_destroy Callback

<table><tr><td>Name: lock_destroyCategory: subroutine</td><td>Properties: C/C++-only, common-type-callback, mutex-execution, OMPT</td></tr></table>

## Type Signature

mutex

## Semantics

A tool provides a lock\_destroy callback, which has the mutex OMPT type, that the OpenMP implementation dispatches when it executes a lock-destroying routine.

## Cross References

• Lock Destroying Routines, see Section 28.2

• OMPT mutex Type, see Section 34.7.10

## 34.7.12 mutex\_acquired Callback

<table><tr><td>Name: mutex_acquiredCategory: subroutine</td><td>Properties: C/C++-only, common-type-callback, mutex-execution, OMPT</td></tr></table>

## Type Signature

mutex

## Semantics

A tool provides a mutex\_acquired callback, which has the mutex OMPT type, that the OpenMP implementation dispatches when the structured block associated with a mutual-exclusion construct begins execution or when a region guarded by a lock-acquiring routine or lock-testing routine begins execution.

## Cross References

• Lock Acquiring Routines, see Section 28.3

• Lock Testing Routines, see Section 28.5

• OMPT mutex Type, see Section 34.7.10

## 34.7.13 mutex\_released Callback

<table><tr><td>Name: mutex_releasedCategory: subroutine</td><td>Properties: C/C++-only, common-type-callback, mutex-execution, OMPT</td></tr></table>

## Type Signature

mutex

## Semantics

A tool provides a mutex\_released callback, which has the mutex OMPT type, that the OpenMP implementation dispatches when the structured block associated with a mutual-exclusion construct completes execution or, similarly, when a region that a lock-releasing routine guards completes execution.

## Cross References

• Lock Releasing Routines, see Section 28.4

• OMPT mutex Type, see Section 34.7.10

## 34.7.14 nest\_lock Callback

<table><tr><td>Name: nest_lockCategory: subroutine</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>endpoint</td><td>scope_endpoint</td><td>OMPT</td></tr><tr><td>wait_id</td><td>wait_id</td><td>OMPT</td></tr><tr><td>codeptr_ra</td><td>void</td><td>intent(in), pointer</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_callback\_nest\_lock\_t) ( ompt\_scope\_endpoint\_t endpoint, ompt\_wait\_id\_t wait\_id, const void \*codeptr\_ra);

C / C++

## Trace Record

C / C++

typedef struct ompt\_record\_nest\_lock\_t { ompt\_scope\_endpoint\_t endpoint; ompt\_wait\_id\_t wait\_id; const void <sub>\*</sub>codeptr\_ra; } ompt\_record\_nest\_lock\_t;

C / C++

## Semantics

A tool provides a nest\_lock callback, which has the nest\_lock OMPT type, that the OpenMP implementation dispatches when a thread that owns a nestable lock invokes a routine that alters the nesting count of the lock but does not relinquish its ownership.

Cross References

• OMPT scope\_endpoint Type, see Section 33.27

• OMPT wait\_id Type, see Section 33.40

## 34.7.15 flush Callback

<table><tr><td>Name: flushCategory: subroutine</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>thread_data</td><td>data</td><td>OMPT, pointer, untraced-argument</td></tr><tr><td>codeptr_ra</td><td>void</td><td>intent(in), pointer</td></tr></table>

## Type Signature

C / C++

typedef void (<sub>\*</sub>ompt\_callback\_flush\_t) (ompt\_data\_t <sub>\*</sub>thread\_data, const void \*codeptr\_ra);

C / C++

## Trace Record

C / C++

typedef struct ompt\_record\_flush\_t {const void <sub>\*</sub>codeptr\_ra;

} ompt\_record\_flush\_t;

C / C++

## Semantics

A tool provides a flush callback, which has the flush OMPT type, that the OpenMP implementation dispatches when it encounters a flush construct. The binding of the thread\_data argument is the encountering thread.

Cross References

• OMPT data Type, see Section 33.8

• flush Construct, see Section 17.8.6

## 34.8 control\_tool Callback

<table><tr><td>Name: control_toolCategory: function</td><td>Properties: C/C++-only, OMPT</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>command</td><td>c_uint64_t</td><td>default</td></tr><tr><td>modifier</td><td>c_uint64_t</td><td>default</td></tr><tr><td>arg</td><td>c_ptr</td><td>iso_c, value, untraced-argument</td></tr><tr><td>codeptr_ra</td><td>void</td><td>intent(in), pointer</td></tr></table>

## Type Signature

C / C++

typedef int (<sub>\*</sub>ompt\_callback\_control\_tool\_t) (uint64\_t command, uint64\_t modifier, void <sub>\*</sub>arg, const void <sub>\*</sub>codeptr\_ra);

## Trace Record

typedef struct ompt\_record\_control\_tool\_t { uint64\_t command; uint64\_t modifier; const void <sub>\*</sub>codeptr\_ra; } ompt\_record\_control\_tool\_t;

C / C++

## C / C++

## Semantics

A tool provides a control\_tool callback, which has the control\_tool OMPT type, that the OpenMP implementation uses to dispatch tool-control events. This callback may return any non-negative value, which will be returned to the OpenMP program as the return value of the omp\_control\_tool call that triggered the callback.

The command argument passes a command from an OpenMP program to a tool. Standard values for command are defined by the control\_tool OpenMP type. The modifier argument passes a command modifier from an OpenMP program to a tool. The command and modifier arguments may have tool-defined values. Tools must ignore command values that they are not designed to handle. The arg argument is a void pointer that enables a tool and an OpenMP program to exchange arbitrary state. The arg argument may be NULL.

## Restrictions

Restrictions on control\_tool callbacks are as follows:

• Tool-defined values for command must be greater than or equal to 64 and less than or equal to 2147483647 (INT32\_MAX).

• Tool-defined values for modifier must be non-negative and less than or equal to 2147483647 (INT32\_MAX).

## Cross References

• OpenMP control\_tool Type, see Section 20.12.1

• omp\_control\_tool Routine, see Section 31.1

# 35 Device Callbacks and Tracing
