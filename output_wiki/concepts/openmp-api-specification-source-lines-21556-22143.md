# OpenMP-API-Specification Source Lines 21556-22143

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source OpenMP-API-Specification:L21556-L22143

Citation: [OpenMP-API-Specification:L21556-L22143]

````text
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

## 24 Device Information Routines

This chapter describes device-information routines, which are routines that have the device-information property. These routines modify or retrieve information that supports the use of the set of devices that are available to an OpenMP program.

## Restrictions

Restrictions to device-information routines are as follows.

• Any device\_num argument must be a conforming device number unless otherwise specified.

## 24.1 omp\_set\_default\_device Routine

<table><tr><td>Name: omp_set_default_deviceCategory: subroutine</td><td>Properties: device-information, ICV-modifying</td></tr></table>

Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>device_num</td><td>integer</td><td>default</td></tr></table>

## Prototypes

C / C++

void omp\_set\_default\_device(int device\_num);

C / C++

Fortran

subroutine omp\_set\_default\_device(device\_num)

integer device\_num

Fortran

## Effect

The efect of the omp\_set\_default\_device routine is to set the value of the default-device-var ICV of the current task to the value specified in the device-num argument, thus determining the default target device. When called from within a target region, the efect of this routine is unspecified.

## Cross References

• default-device-var ICV, see Table 3.1

• target Construct, see Section 15.8

## 24.2 omp\_get\_default\_device Routine

<table><tr><td>Name: omp_get_default_deviceCategory: function</td><td>Properties: device-information, ICV-retrieving</td></tr></table>

## Return Type

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr></table>

## Prototypes

C / C++

int omp\_get\_default\_device(void);

C / C++

Fortran

integer function omp\_get\_default\_device()

Fortran

## Effect

The omp\_get\_default\_device routine returns the value of the default-device-var ICV of the current task, which is the device number of the default target device. When called from within a target region the efect of this routine is unspecified.

Cross References

• default-device-var ICV, see Table 3.1

• target Construct, see Section 15.8

## 24.3 omp\_get\_num\_devices Routine

<table><tr><td colspan="2">Name: omp_get_num_devicesCategory: function</td><td>Properties: device-information, ICV-retrieving</td></tr><tr><td colspan="3">Return Type</td></tr><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td colspan="3">PrototypesC / C++int omp_get_num_devices(void);C / C++Fortraninteger function omp_get_num_devices()Fortran</td></tr></table>

## Effect

The omp\_get\_num\_devices routine returns the value of the num-devices-var ICV, which is the number of available non-host devices onto which code or data may be ofloaded. When called from within a target region the efect of this routine is unspecified.

## Cross References

• num-devices-var ICV, see Table 3.1

• target Construct, see Section 15.8

## 24.4 omp\_get\_device\_num Routine

<table><tr><td>Name: omp_get_device_numCategory: function</td><td>Properties: device-information</td></tr></table>

Return Type

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr></table>

## Prototypes

C / C++

int omp\_get\_device\_num(void);

C / C++

Fortran

integer function omp\_get\_device\_num()

Fortran

## Effect

The omp\_get\_device\_num routine returns the value of the device-num-var ICV, which is the device number of the device on which the encountering thread is executing. When called on the host device, it will return the same value as the omp\_get\_initial\_device routine.

Cross References

• device-num-var ICV, see Table 3.1

• target Construct, see Section 15.8

## 24.5 omp\_get\_num\_procs Routine

<table><tr><td>Name: omp_get_num_procsCategory: function</td><td>Properties: all-device-threads-binding, device-information, ICV-retrieving</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr></table>

## Prototypes

C / C++

int omp\_get\_num\_procs(void);

C / C++

Fortran

integer function omp\_get\_num\_procs()

Fortran

## Effect

The omp\_get\_num\_procs routine returns the value of the num-procs-var ICV. Thus, this routine returns the number of processors that are available to the device at the time the routine is called. This value may change between the time that it is determined by the omp\_get\_num\_procs routine and the time that it is read in the calling context due to system actions outside the control of the OpenMP implementation.

Cross References

• num-procs-var ICV, see Table 3.1

## 24.6 omp\_get\_max\_progress\_width Routine

<table><tr><td>Name: omp_get_max_progress_widthCategory: function</td><td>Properties: device-information</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>device_num</td><td>integer</td><td>default</td></tr></table>

## Prototypes

C / C++

int omp\_get\_max\_progress\_width(int device\_num);

C / C++

Fortran

integer function omp\_get\_max\_progress\_width(device\_num) integer device\_num

Fortran

## Effect

The omp\_get\_max\_progress\_width routine returns the maximum size, in terms of hardware threads, of progress units on the device specified by device\_num. When called from within a target region the efect of this routine is unspecified.

## 24.7 omp\_get\_device\_from\_uid Routine

<table><tr><td>Name: omp_get_device_from_uidCategory: function</td><td>Properties: device-information</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>uid</td><td>char</td><td>pointer, intent(in)</td></tr></table>

Prototypes

C / C++

int omp\_get\_device\_from\_uid(const char <sub>\*</sub>uid);

C / C++

Fortran

integer function omp\_get\_device\_from\_uid(uid)

character(len=<sub>\*</sub>), intent(in) :: uid

Fortran

## Effect

The omp\_get\_device\_from\_uid routine returns the device number associated with the device specified by the uid; if no device with that uid is available, the value of omp\_invalid\_device is returned. When called from within a target region, the efect is unspecified.

Cross References

• available-devices-var ICV, see Table 3.1

• default-device-var ICV, see Table 3.1

• omp\_get\_uid\_from\_device Routine, see Section 24.8

## 24.8 omp\_get\_uid\_from\_device Routine

<table><tr><td>Name: omp_get_uid_from_deviceCategory: function</td><td>Properties: device-information</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>const char</td><td>pointer</td></tr><tr><td>device_num</td><td>integer</td><td>intent(in)</td></tr></table>

## Prototypes

C / C++

const char <sub>\*</sub>omp\_get\_uid\_from\_device(int device\_num);

C / C++

Fortran

character(:) function omp\_get\_uid\_from\_device(device\_num)

pointer :: omp\_get\_uid\_from\_device

integer, intent(in) :: device\_num

Fortran

## Effect

The omp\_get\_uid\_from\_device routine returns the implementation defined unique identifier string that identifies the device specified by device\_num. If the device\_num argument has a value of omp\_invalid\_device, the routine returns NULL. When called from within a target region, the efect is unspecified.

Cross References

• available-devices-var ICV, see Table 3.1

• default-device-var ICV, see Table 3.1

• omp\_get\_device\_from\_uid Routine, see Section 24.7

## 24.9 omp\_is\_initial\_device Routine

<table><tr><td>Name: omp_is_initial_deviceCategory: function</td><td>Properties: device-information</td></tr></table>

## Return Type

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>logical</td><td>default</td></tr></table>

Prototypes

C / C++

int omp\_is\_initial\_device(void);

C / C++

Fortran

logical function omp\_is\_initial\_device()

Fortran

## Effect

The omp\_is\_initial\_device routine returns true if the current task is executing on the host device; otherwise, it returns false.

## 24.10 omp\_get\_initial\_device Routine

<table><tr><td>Name: omp_get_initial_deviceCategory: function</td><td>Properties: device-information</td></tr></table>

## Return Type

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr></table>

## Prototypes

C / C++

int omp\_get\_initial\_device(void);

C / C++

Fortran

integer function omp\_get\_initial\_device()

Fortran

## Effect

The efect of the omp\_get\_initial\_device routine is to return the device number of the host device. The value of the device number is the value of omp\_initial\_device or the value returned by the omp\_get\_num\_devices routine. When called from within a target region the efect of this routine is unspecified.

## Cross References

• target Construct, see Section 15.8

## 24.11 omp\_get\_device\_num\_teams Routine

<table><tr><td>Name: omp_get_device_num_teamsCategory: function</td><td>Properties: device-information, ICV-retrieving</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>device_num</td><td>integer</td><td>default</td></tr></table>

## Prototypes

C / C++

int omp\_get\_device\_num\_teams(int device\_num);

C / C++

Fortran

integer function omp\_get\_device\_num\_teams(device\_num)

integer device\_num

Fortran

## Effect

The omp\_get\_device\_num\_teams routine returns the value of the nteams-var ICV in the device data environment of device device\_num. Thus, the routine returns the number of teams that will be requested for a teams region on device device\_num if the num\_teams clause is not specified. If device\_num is the device number of the host device,

omp\_get\_device\_num\_teams is equivalent to omp\_get\_num\_teams. If the device\_num argument has the value of omp\_invalid\_device or is not a conforming device number, the routine returns zero. When called from within a target region, the efect of this routine is unspecified.

Cross References

• nteams-var ICV, see Table 3.1

• num\_teams Clause, see Section 12.2.1

• teams Construct, see Section 12.2

## 24.12 omp\_set\_device\_num\_teams Routine

<table><tr><td>Name: omp_set_device_num_teamsCategory: subroutine</td><td>Properties: device-information, ICV-modifying</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>num_teams</td><td>integer</td><td>non-negative</td></tr><tr><td>device_num</td><td>integer</td><td>default</td></tr></table>

## Prototypes

C / C++

void omp\_set\_device\_num\_teams(int num\_teams, int device\_num);

C / C++

Fortran

subroutine omp\_set\_device\_num\_teams(num\_teams, device\_num)

integer num\_teams, device\_num

Fortran

## Effect

The efect of the omp\_set\_device\_num\_teams routine is to set the value of the nteams-var ICV of device device\_num to the value specified in the num\_teams argument. Thus, the routine determines the number of teams that will be requested for a teams region on device device\_num if the num\_teams clause is not specified. If device\_num is the device number of the host device, omp\_set\_device\_num\_teams is equivalent to omp\_set\_num\_teams. If the device\_num argument has the value of omp\_invalid\_device or is not a conforming device number, runtime error termination occurs. When called from within a target region, the efect of this routine is unspecified.

## Restrictions

Restrictions to the omp\_set\_device\_num\_teams routine are as follows:

• The routine must not execute concurrently with any device-afecting construct on device device\_num.

• If device device\_num is the host device, an omp\_set\_device\_num\_teams region must be a strictly nested region of the implicit parallel region that surrounds the whole OpenMP program.

## Cross References

• nteams-var ICV, see Table 3.1

• num\_teams Clause, see Section 12.2.1

• teams Construct, see Section 12.2
````
