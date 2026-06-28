
This chapter describes the OpenMP API routines that control the execution state of the OpenMP implementation and provide information about that state. These routines include:

• Routines that monitor and control cancellation;

• Resource-relinquishing routines that free resources used by the OpenMP program;

• Routines that support timing measurements of OpenMP programs; and

• The environment display routine that displays the initial values of ICVs.

## 30.1 omp\_get\_cancellation Routine

<table><tr><td colspan="2">Name: omp_get_cancellationCategory: function</td><td>Properties: ICV-retrieving</td></tr><tr><td colspan="3">Return Type</td></tr><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>logical</td><td>default</td></tr></table>

## Effect

The omp\_get\_cancellation routine returns the value of the cancel-var ICV. Thus, it returns true if cancellation is enabled and otherwise it returns false.

## Cross References

• cancel-var ICV, see Table 3.1

## 30.2 Resource Relinquishing Routines

This section describes routines that have the resource-relinquishing property. Each resource-relinquishing routine region implies a barrier. Each resource-relinquishing routine returns zero in case of success, and non-zero otherwise.

## Tool Callbacks

If the tool is not allowed to interact with the specified device after encountering the resource-relinquishing routine, then the runtime must call the tool finalizer for that device.

## Restrictions

Restrictions to resource-relinquishing routines are as follows:

• A resource-relinquishing routine region may not be nested in any explicit region.

• A resource-relinquishing routine may only be called when all explicit tasks that do not bind to the implicit parallel region to which the encountering thread binds have finalized execution.

## 30.2.1 omp\_pause\_resource Routine

<table><tr><td>Name: omp_pause_resourceCategory: function</td><td>Properties: all-tasks-binding,resource-relinquishing</td></tr></table>

Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>kind</td><td>pause_resource</td><td>default</td></tr><tr><td>device_num</td><td>integer</td><td>default</td></tr></table>

Prototypes

<table><tr><td>C / C++</td></tr><tr><td>int omp_pause_resource(omp_pause_resource_t kind, int device_num);</td></tr><tr><td>C / C++</td></tr><tr><td>Fortran</td></tr><tr><td>integer function omp_pause_resource(kind, device_num)</td></tr><tr><td>integer (kind=omp_pause_resource_kind) kind</td></tr><tr><td>integer device_num</td></tr></table>

The omp\_pause\_resource routine allows the runtime to relinquish resources used by OpenMP on the specified device. The device\_num argument indicates the device that will be paused. If the device number has the value omp\_invalid\_device, runtime error termination is performed.

The binding task set for a omp\_pause\_resource routine region is all tasks on the specified device. That is, this routines has the all-device-tasks binding property. If omp\_pause\_stop\_tool is specified for a non-host device, the efect is the same as for omp\_pause\_hard and (unlike for the host device) does not shutdown the OMPT interface.

## Restrictions

Restrictions to the omp\_pause\_resource routine are as follows:

• The device\_num argument must be a conforming device number.

## Cross References

• Predefined Identifiers, see Section 20.1

• OpenMP pause\_resource Type, see Section 20.11.1

## 30.2.2 omp\_pause\_resource\_all Routine

<table><tr><td colspan="2">Name: omp_pause_resource_allCategory: function</td><td colspan="2">Properties: all-tasks-binding,resource-relinquishing</td></tr><tr><td colspan="4">Return Type and Arguments</td></tr><tr><td>Name</td><td colspan="2">Type</td><td>Properties</td></tr><tr><td></td><td colspan="2">integer</td><td>default</td></tr><tr><td>kind</td><td colspan="2">pause_resource</td><td>default</td></tr></table>

## Prototypes

C / C++

int omp\_pause\_resource\_all(omp\_pause\_resource\_t kind);

C / C++

Fortran

integer function omp\_pause\_resource\_all(kind)

integer (kind=omp\_pause\_resource\_kind) kind

Fortran

## Effect

The omp\_pause\_resource\_all routine allows the runtime to relinquish resources used by OpenMP on all devices. It is equivalent to calling the omp\_pause\_resource routine once for each available device, including the host device. The binding task set for a omp\_pause\_resource\_all routine region is all tasks in the OpenMP program. That is, this routine has the all-tasks binding property.

## Cross References

• omp\_pause\_resource Routine, see Section 30.2.1

• OpenMP pause\_resource Type, see Section 20.11.1

## 30.3 Timing Routines

This section describes routines that support a portable wall clock timer.

## 30.3.1 omp\_get\_wtime Routine

<table><tr><td>Name: omp_get_wtimeCategory: function</td><td>Properties: default</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>double</td><td>default</td></tr></table>

C / C++

double omp\_get\_wtime(void);

C / C++

Fortran

double precision function omp\_get\_wtime()

Fortran

## Effect

The omp\_get\_wtime routine returns a value equal to the elapsed wall clock time in seconds since some time-in-the-past. The actual time-in-the-past is arbitrary, but it is guaranteed not to change during the execution of an OpenMP program. The time returned is a per-thread time, so it is not required to be globally consistent across all threads that participate in an OpenMP program.

30.3.2 omp\_get\_wtick Routine

<table><tr><td colspan="2">Name: omp_get_wtickCategory: function</td><td colspan="2">Properties: default</td></tr><tr><td colspan="4">Return Type</td></tr><tr><td>Name</td><td colspan="2">Type</td><td>Properties</td></tr><tr><td></td><td colspan="2">double</td><td>default</td></tr><tr><td colspan="4">PrototypesC / C++double omp_get_wtick(void);C / C++Fortrandouble precision function omp_get_wtick()Fortran</td></tr></table>

## Effect

The omp\_get\_wtick routine returns the precision of the timer used by omp\_get\_wtime as a value equal to the number of seconds between successive clock ticks. The return value of the omp\_get\_wtick routine is not guaranteed to be consistent across any set of threads.

## Cross References

• omp\_get\_wtime Routine, see Section 30.3.1

## 30.4 omp\_display\_env Routine

<table><tr><td colspan="2">Name: omp_display_envCategory: subroutine</td><td colspan="2">Properties: default</td></tr><tr><td colspan="4">Arguments</td></tr><tr><td>Name</td><td colspan="2">Type</td><td>Properties</td></tr><tr><td>verbose</td><td colspan="2">logical</td><td>intent(in)</td></tr><tr><td colspan="4">PrototypesC / C++void omp_display_env(int verbose);C / C++Fortransubroutine omp_display_env(verbose)logical, intent(in) :: verboseFortran</td></tr></table>

## Effect

Each time that the omp\_display\_env routine is invoked, the runtime system prints the OpenMP version number and the initial values of the ICVs associated with the environment variables described in Chapter 4. The displayed values are the values of the ICVs after they have been modified according to the environment variable settings and before the execution of any construct or routine.

The display begins with "OPENMP DISPLAY ENVIRONMENT BEGIN", followed by the \_OPENMP version macro (or the openmp\_version predefined identifier for Fortran) and ICV values, in the format NAME ’=’ VALUE. NAME corresponds to the macro or environment variable name, prepended with a bracketed DEVICE. VALUE corresponds to the value of the macro or ICV associated with this environment variable. Values are enclosed in single quotes. DEVICE corresponds to a comma-separated list of the devices on which the value of the ICV is applied. It is host if the device is the host device; device if the ICV applies to all non-host devices; all if the ICV has global scope or the value applies to the host device and all non-host devices; dev, a space, and the device number if it applies to a specific non-host devices. Instead of a single number a range can also be specified using the first and last device number separated by a hyphen. Whether

ICVs with the same value are combined or displayed in multiple lines is implementation defined. The display is terminated with "OPENMP DISPLAY ENVIRONMENT END".

If the verbose argument evaluates to false, the runtime displays the OpenMP version number defined by the \_OPENMP version macro (or the openmp\_version predefined identifier for Fortran) value and the initial ICV values for the environment variables listed in Chapter 4. If the verbose argument evaluates to true, the runtime may also display the values of vendor-specific ICVs that may be modified by vendor-specific environment variables.

## Example output:

```txt
OPENMP DISPLAY ENVIRONMENT BEGIN
  _OPENMP='202411'
  [dev 1] OMP_SCHEDULE='GUIDED,4'
  [host] OMP_NUM_THREADS='4,3,2'
  [device] OMP_NUM_THREADS='2'
  [host, dev 2] OMP_DYNAMIC='TRUE'
  [dev 2-3, dev 5] OMP_DYNAMIC='FALSE'
  [all] OMP_WAIT_POLICY='ACTIVE'
  [host] OMP_PLACES='{0:4},{4:4},{8:4},{12:4}'
  ...
OPENMP DISPLAY ENVIRONMENT END
```

## Restrictions

Restrictions to the omp\_display\_env routine are as follows:

• When called from within a target region the efect is unspecified.

## Cross References

• Predefined Identifiers, see Section 20.1
