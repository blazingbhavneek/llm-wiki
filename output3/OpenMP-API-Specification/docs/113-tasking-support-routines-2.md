## 23 Tasking Support Routines

This chapter specifies OpenMP API routines that support task execution:

• Tasking routines that query general task execution properties; and

• The event routine to fulfill task dependences.

## 23.1 Tasking Routines

This section describes routines that pertain to OpenMP explicit tasks.

## 23.1.1 omp\_get\_max\_task\_priority Routine

<table><tr><td colspan="2">Name: omp_get_max_task_priorityCategory: function</td><td>Properties: all-device-threads-binding,ICV-retrieving</td></tr><tr><td colspan="3">Return Type</td></tr><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td colspan="3">PrototypesC / C++int omp_get_max_task_priority(void);C / C++Fortraninteger function omp_get_max_task_priority()Fortran</td></tr></table>

## Effect

The omp\_get\_max\_task\_priority routine returns the value of the max-task-priority-var ICV, which determines the maximum value that can be specified in the priority clause.

## Cross References

• max-task-priority-var ICV, see Table 3.1

• priority Clause, see Section 14.9

## 23.1.2 omp\_in\_explicit\_task Routine

<table><tr><td>Name: omp_in_explicit_taskCategory: function</td><td>Properties: ICV-retrieving</td></tr></table>

## Return Type

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>logical</td><td>default</td></tr></table>

## Prototypes

C / C++

int omp\_in\_explicit\_task(void);

C / C++

Fortran

logical function omp\_in\_explicit\_task()

Fortran

## Effect

The omp\_in\_explicit\_task routine returns the value of the explicit-task-var ICV, which indicates whether the encountering task is an explicit task region.

## Cross References

• explicit-task-var ICV, see Table 3.1

• task Construct, see Section 14.1

## 23.1.3 omp\_in\_final Routine

<table><tr><td>Name: omp_in_finalCategory: function</td><td>Properties: ICV-retrieving</td></tr></table>

## Return Type

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>logical</td><td>default</td></tr></table>

## Prototypes

C / C++

int omp\_in\_final(void);

C / C++

Fortran

logical function omp\_in\_final()

Fortran

## Effect

The omp\_in\_final routine returns the value of the final-task-var ICV, which indicates whether the encountering task is a final task region.

## Cross References

• final Clause, see Section 14.7

• final-task-var ICV, see Table 3.1

• task Construct, see Section 14.1

## 23.1.4 omp\_is\_free\_agent Routine

<table><tr><td>Name: omp_is_free_agentCategory: function</td><td>Properties: ICV-retrieving</td></tr></table>

## Return Type

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>logical</td><td>default</td></tr></table>

## Prototypes

C / C++

int omp\_is\_free\_agent(void);

C / C++

Fortran

logical function omp\_is\_free\_agent()

Fortran

## Effect

The omp\_is\_free\_agent routine returns the value of the free-agent-var ICV, which indicates whether a free-agent thread is executing the enclosing task region at the time the routine is called.

## Cross References

• free-agent-var ICV, see Table 3.1

• task Construct, see Section 14.1

• threadset Clause, see Section 14.8

## 23.1.5 omp\_ancestor\_is\_free\_agent Routine

<table><tr><td>Name: omp_ancestor_is_free_agentCategory: function</td><td>Properties: default</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>logical</td><td>default</td></tr><tr><td>level</td><td>integer</td><td>default</td></tr></table>

## Prototypes

C / C++

int omp\_ancestor\_is\_free\_agent(int level);

C / C++

Fortran

logical function omp\_ancestor\_is\_free\_agent(level) integer level

Fortran

## Effect

The omp\_ancestor\_is\_free\_agent routine returns true if the ancestor thread of the encountering thread is a free-agent thread, for a given nested level of the encountering thread; otherwise, it returns false. If the requested nesting level is outside the range of 0 and the nesting level of the current task, as returned by the omp\_get\_level routine, the routine returns false.

Note – When the omp\_ancestor\_is\_free\_agent routine is called with a value of level =omp\_get\_level, the routine has the same efect as the omp\_is\_free\_agent routine.

## Cross References

• omp\_get\_level Routine, see Section 21.14

• omp\_is\_free\_agent Routine, see Section 23.1.4

• task Construct, see Section 14.1

• threadset Clause, see Section 14.8

## 23.2 Event Routine

This section describes routines that support OpenMP event objects.

## 23.2.1 omp\_fulfill\_event Routine

<table><tr><td>Name: omp_fulfill_eventCategory: subroutine</td><td>Properties: default</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>event</td><td>event_handle</td><td>default</td></tr></table>

## Prototypes

C / C++

void omp\_fulfill\_event(omp\_event\_handle\_t event);

C / C++

Fortran

subroutine omp\_fulfill\_event(event)

integer (kind=omp\_event\_handle\_kind) event

Fortran

## Effect

The efect of this routine is to fulfill the event associated with the event argument. The efect of fulfilling the event will depend on how the event object was created. The event object is destroyed and cannot be accessed after calling this routine, and the event handle becomes unassociated with any event object. This routine has no efect if the event argument corresponds to a completed task.

## Execution Model Events

The task-fulfill event occurs in a thread that executes an omp\_fulfill\_event region before the event is fulfilled if the OpenMP event object was created by a detach clause on a task.

## Tool Callbacks

A thread dispatches a registered task\_schedule callback with NULL as its next\_task\_data argument while the argument prior\_task\_data binds to the detachable task for each occurrence of a task-fulfill event. If the task-fulfill event occurs before the detachable task finished execution of the associated structured block, the callback has ompt\_task\_early\_fulfill as its prior\_task\_status argument; otherwise the callback has ompt\_task\_late\_fulfill as its prior\_task\_status argument.

## Restrictions

Restrictions to the omp\_fulfill\_event routine are as follows:

• The event that corresponds to the event argument must not have already been fulfilled.

• The event handle that the event argument identifies must have been created by the efect of a detach clause.

• The event handle passed to the routine must refer to an event object that was created by a thread in the same device as the thread that invoked the routine.

• An event handle must be fulfilled before execution continues beyond the next barrier of the current team after a detach clause creates the event that the event argument represents.

## Cross References

• detach Clause, see Section 14.11

• OpenMP event\_handle Type, see Section 20.6.1

• task\_schedule Callback, see Section 34.5.2

• OMPT task\_status Type, see Section 33.38
