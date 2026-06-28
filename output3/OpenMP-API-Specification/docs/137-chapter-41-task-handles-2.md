## 41.6 Task Handle Routines

## 41.6.1 ompd\_get\_curr\_task\_handle Routine

<table><tr><td>Name: ompd_get_curr_task_handleCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>thread_handle</td><td>thread_handle</td><td>opaque, pointer</td></tr><tr><td>task_handle</td><td>task_handle</td><td>opaque, pointer-to-pointer</td></tr></table>

## Prototypes

C

ompd\_rc\_t ompd\_get\_curr\_task\_handle( ompd\_thread\_handle\_t <sub>\*</sub>thread\_handle, ompd\_task\_handle\_t <sub>\*\*</sub>task\_handle);

C

## Semantics

The ompd\_get\_curr\_task\_handle routine obtains a pointer to the task handle for the current task region that is associated with an OpenMP thread. This routine yields meaningful results only if the thread for which the handle is provided is stopped. The task handle must be released with ompd\_rel\_task\_handle. The thread\_handle argument is an opaque handle that selects the thread on which to operate. On return, the task\_handle argument points to a location that points to a handle for the task that the thread is currently executing. In addition to the return codes permitted for all OMPD routines, this routine returns ompd\_rc\_unavailable if the thread is currently not executing a task.

## Cross References

• ompd\_rel\_task\_handle Routine, see Section 41.8.3

• OMPD rc Type, see Section 39.9

• OMPD task\_handle Type, see Section 39.18.3

• OMPD thread\_handle Type, see Section 39.18.4

## 41.6.2 ompd\_get\_generating\_task\_handle Routine

<table><tr><td>Name: ompd_get_generating_task_handleCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>task_handle</td><td>task_handle</td><td>pointer</td></tr><tr><td>generating_task_handle</td><td>task_handle</td><td>pointer-to-pointer</td></tr></table>

## Prototypes

ompd\_rc\_t ompd\_get\_generating\_task\_handle(

ompd\_task\_handle\_t <sub>\*</sub>task\_handle,

ompd\_task\_handle\_t \*\*generating\_task\_handle);

C

## Semantics

The ompd\_get\_generating\_task\_handle routine obtains a pointer to the task handle of the generating task region. The generating task is the task that was active when the task specified by task\_handle was created. This routine yields meaningful results only if the thread that is executing the task that task\_handle specifies is stopped while executing the task. The generating task handle must be released with ompd\_rel\_task\_handle. On return, the generating\_task\_handle argument points to a location that points to a handle for the generating task. In addition to the return codes permitted for all OMPD routines, this routine returns ompd\_rc\_unavailable if no generating task region exists.

## Cross References

• ompd\_rel\_task\_handle Routine, see Section 41.8.3

• OMPD rc Type, see Section 39.9

• OMPD task\_handle Type, see Section 39.18.3

## 41.6.3 ompd\_get\_scheduling\_task\_handle Routine

<table><tr><td>Name: ompd_get_scheduling_task_handleCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>task_handle</td><td>task_handle</td><td>pointer</td></tr><tr><td>scheduling_task_handle</td><td>task_handle</td><td>pointer-to-pointer</td></tr></table>

## Prototypes

C

ompd\_rc\_t ompd\_get\_scheduling\_task\_handle(

ompd\_task\_handle\_t <sub>\*</sub>task\_handle,

ompd\_task\_handle\_t \*\*scheduling\_task\_handle);

C

## Semantics

The ompd\_get\_scheduling\_task\_handle routine obtains a task handle for the task that was active when the task that task\_handle represents was scheduled. An implicit task does not have a scheduling task. This routine yields meaningful results only if the thread that is executing the task that task\_handle specifies is stopped while executing the task. On return, the scheduling\_task\_handle argument points to a location that points to a handle for the task that is still on the stack of execution on the same thread and was deferred in favor of executing the selected task. This task handle must be released with ompd\_rel\_task\_handle. In addition to the return codes permitted for all OMPD routines, this routine returns ompd\_rc\_unavailable if no scheduling task exists.

## Cross References

• ompd\_rel\_task\_handle Routine, see Section 41.8.3

• OMPD rc Type, see Section 39.9

• OMPD task\_handle Type, see Section 39.18.3

## 41.6.4 ompd\_get\_task\_in\_parallel Routine

<table><tr><td>Name: ompd_get_task_in_parallelCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>parallel_handle</td><td>parallel_handle</td><td>opaque, pointer</td></tr><tr><td>thread_num</td><td>integer</td><td>default</td></tr><tr><td>task_handle</td><td>task_handle</td><td>opaque, pointer-to-pointer</td></tr></table>

## Prototypes

C

ompd\_rc\_t ompd\_get\_task\_in\_parallel( ompd\_parallel\_handle\_t <sub>\*</sub>parallel\_handle, int thread\_num, ompd\_task\_handle\_t <sub>\*\*</sub>task\_handle);

C

## Semantics

The ompd\_get\_task\_in\_parallel routine obtains handles for the implicit tasks that are associated with a parallel region. A successful invocation of ompd\_get\_task\_in\_parallel returns a pointer to a task handle in the location to which task\_handle points. This routine yields meaningful results only if all OpenMP threads in the parallel region are stopped. The parallel\_handle argument is an opaque handle that selects the parallel region on which to operate. The thread\_num argument selects the implicit task of the team to be returned. The thread\_num argument is equal to the thread-num-var ICV value of the selected implicit task. This routine returns ompd\_rc\_bad\_input if the thread\_num argument is greater than or equal to the team-size-var ICV or negative.

## Cross References

• ompd\_get\_icv\_from\_scope Routine, see Section 41.11.2

• OMPD parallel\_handle Type, see Section 39.18.2

• OMPD rc Type, see Section 39.9

• OMPD task\_handle Type, see Section 39.18.3

41.6.5 ompd\_get\_task\_function Routine

<table><tr><td>Name: ompd_get_task_functionCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>task_handle</td><td>task_handle</td><td>opaque, pointer</td></tr><tr><td>entry_point</td><td>address</td><td>pointer</td></tr></table>

## Prototypes

C

ompd\_rc\_t ompd\_get\_task\_function(ompd\_task\_handle\_t <sub>\*</sub>task\_handle, ompd\_address\_t <sub>\*</sub>entry\_point);

C

## Semantics

The ompd\_get\_task\_function routine returns the entry point of the code that corresponds to the body of code that the task executes. This routine returns meaningful results only if the thread that is executing the task that task\_handle specifies is stopped while executing the task. That argument is an opaque handle that selects the task on which to operate. On return, the entry\_point argument is set to an address that describes the beginning of application code that executes the task region.

## Cross References

• OMPD address Type, see Section 39.2

• OMPD rc Type, see Section 39.9

• OMPD task\_handle Type, see Section 39.18.3

## 41.6.6 ompd\_get\_task\_frame Routine

<table><tr><td>Name: ompd_get_task_frameCategory: function</td><td>Properties: C-only, OMPD</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>rc</td><td>default</td></tr><tr><td>task_handle</td><td>task_handle</td><td>pointer</td></tr><tr><td>exit_frame</td><td>frame_info</td><td>pointer</td></tr><tr><td>enter_frame</td><td>frame_info</td><td>pointer</td></tr></table>

## Prototypes

ompd\_rc\_t ompd\_get\_task\_frame(ompd\_task\_handle\_t <sub>\*</sub>task\_handle, ompd\_frame\_info\_t <sub>\*</sub>exit\_frame, ompd\_frame\_info\_t <sub>\*</sub>enter\_frame);

C

## Semantics

The ompd\_get\_task\_frame routine extracts the frame pointers of a task. An OpenMP implementation maintains an object of frame OMPT type for every implicit task and explicit task. The ompd\_get\_task\_frame routine extracts the enter\_frame and exit\_frame fields of the frame object of the task that task\_handle identifies. This routine yields meaningful results only if the thread that is executing the task that task\_handle specifies is stopped while executing the task.

On return, the exit\_frame argument points to a frame\_info object that has the frame information with the same semantics as the exit\_frame field in the frame object that is associated with the specified task. On return, the enter\_frame argument points to a frame\_info object that has the frame information with the same semantics as the enter\_frame field in the frame object that is associated with the specified task.

## Cross References

• OMPD address Type, see Section 39.2

• OMPT frame Type, see Section 33.15

• OMPD frame\_info Type, see Section 39.7

• OMPD rc Type, see Section 39.9

• OMPD task\_handle Type, see Section 39.18.3
