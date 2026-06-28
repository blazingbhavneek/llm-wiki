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

## 24.13 omp\_get\_device\_teams\_thread\_limit Routine

<table><tr><td>Name:omp_get_device_teams_thread_limitCategory: function</td><td>Properties: device-information, ICV-retrieving</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>device_num</td><td>integer</td><td>default</td></tr></table>

## Prototypes

C / C++

int omp\_get\_device\_teams\_thread\_limit(int device\_num);

C / C++

Fortran

integer function omp\_get\_device\_teams\_thread\_limit(device\_num) integer device\_num

Fortran

## Effect

The omp\_get\_device\_teams\_thread\_limit routine returns the value of the teams-thread-limit-var ICV in the device data environment of device device\_num, which is the maximum number of threads available to execute tasks in each contention group that a teams construct creates on that device. If device\_num is the device number of the host device, omp\_get\_device\_teams\_thread\_limit is equivalent to omp\_get\_teams\_thread\_limit. If the device\_num argument has the value of omp\_invalid\_device or is not a conforming device number, the routine returns zero. When called from within a target region, the efect of this routine is unspecified.

Cross References

• teams-thread-limit-var ICV, see Table 3.1

• teams Construct, see Section 12.2

## 24.14 omp\_set\_device\_teams\_thread\_limit Routine

<table><tr><td>Name:omp_set_device_teams_thread_limitCategory: subroutine</td><td>Properties: device-information, ICV-modifying</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>thread_limit</td><td>integer</td><td>positive</td></tr><tr><td>device_num</td><td>integer</td><td>default</td></tr></table>

## Prototypes

C / C++

void omp\_set\_device\_teams\_thread\_limit(int thread\_limit, int device\_num);

C / C++

Fortran

subroutine omp\_set\_device\_teams\_thread\_limit(thread\_limit, &

device\_num)

integer thread\_limit, device\_num

## Fortran

## Effect

The omp\_set\_device\_teams\_thread\_limit routine sets the value of the teams-thread-limit-var ICV in the device data environment of device device\_num to the value of the thread\_limit argument and thus defines the maximum number of threads that can execute tasks in each contention group that a teams construct creates on that device. If the value of thread\_limit exceeds the number of threads that an implementation supports for each contention group created by a teams construct on device device\_num, the value of the teams-thread-limit-var ICV will be set to the number that is supported by the implementation. If device\_num is the device number of the host device, omp\_set\_device\_teams\_thread\_limit is equivalent to omp\_set\_teams\_thread\_limit. If the device\_num argument has the value of omp\_invalid\_device or is not a conforming device number, runtime error termination occurs. When called from within a target region, the efect of this routine is unspecified.

## Restrictions

Restrictions to the omp\_set\_device\_teams\_thread\_limit routine are as follows:

• The routine must not execute concurrently with any device-afecting construct on device device\_num.

• If device device\_num is the host device, an omp\_set\_device\_teams\_thread\_limit region must be a strictly nested region of the implicit parallel region that surrounds the whole OpenMP program.

Cross References

• teams-thread-limit-var ICV, see Table 3.1

• teams Construct, see Section 12.2

• thread\_limit Clause, see Section 15.3
