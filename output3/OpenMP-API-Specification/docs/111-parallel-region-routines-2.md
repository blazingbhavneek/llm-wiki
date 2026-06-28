
This chapter describes routines that support execution of parallel regions, including routines to determine the number of OpenMP threads for parallel regions and that query the nesting of paralle regions at runtime.

## 21.1 omp\_set\_num\_threads Routine

<table><tr><td>Name: omp_set_num_threadsCategory: subroutine</td><td>Properties: ICV-modifying</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>num_threads</td><td>integer</td><td>positive</td></tr></table>

## Prototypes

C / C++

void omp\_set\_num\_threads(int num\_threads);

C / C++

Fortran

subroutine omp\_set\_num\_threads(num\_threads)

integer num\_threads

Fortran

## Effect

The efect of this routine is to set the value of the first element of the nthreads-var ICV of the current task to the value specified in the argument. Thus, the routine has the ICV modifying property, through which it afects the number of threads to be used for subsequent parallel regions that do not specify a num\_threads clause.

Cross References

• nthreads-var ICV, see Table 3.1

• num\_threads Clause, see Section 12.1.2

• parallel Construct, see Section 12.1

• Determining the Number of Threads for a parallel Region, see Section 12.1.1

## 21.2 omp\_get\_num\_threads Routine

Return Type

<table><tr><td>Name: omp_get_num_threadsCategory: function</td><td>Properties: default</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr></table>

C / C++

int omp\_get\_num\_threads(void);

C / C++

Fortran

integer function omp\_get\_num\_threads()

Fortran

The omp\_get\_num\_threads routine returns the number of threads in the team that is executing the parallel region to which the routine region binds.

## 21.3 omp\_get\_thread\_num Routine

<table><tr><td>Name: omp_get_thread_numCategory: function</td><td>Properties: default</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr></table>

C / C++

int omp\_get\_thread\_num(void);

C / C++

Fortran

integer function omp\_get\_thread\_num()

Fortran

The omp\_get\_thread\_num routine returns the thread number of the calling thread, within the team that is executing the parallel region to which the routine region binds. For assigned threads, the thread number is an integer between 0 and one less than the value returned by omp\_get\_num\_threads, inclusive. The thread number of the primary thread of the team is 0. For unassigned threads, the thread number is the value omp\_unassigned\_thread.

## Cross References

• Predefined Identifiers, see Section 20.1

• omp\_get\_num\_threads Routine, see Section 21.2

## 21.4 omp\_get\_max\_threads Routine

<table><tr><td>Name: omp_get_max_threadsCategory: function</td><td>Properties: ICV-retrieving</td></tr></table>

## Return Type

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr></table>

## Prototypes

C / C++

int omp\_get\_max\_threads(void);

C / C++

Fortran

integer function omp\_get\_max\_threads()

Fortran

## Effect

The value returned by omp\_get\_max\_threads is the value of the first element of the nthreads-var ICV of the current task; thus, the routine has the ICV retrieving property. Its return value is an upper bound on the number of threads that could be used to form a new team if a parallel region without a num\_threads clause is encountered after execution returns from this routine.

Cross References

• nthreads-var ICV, see Table 3.1

• num\_threads Clause, see Section 12.1.2

• parallel Construct, see Section 12.1

• Determining the Number of Threads for a parallel Region, see Section 12.1.1

## 21.5 omp\_get\_thread\_limit Routine

<table><tr><td>Name: omp_get_thread_limitCategory: function</td><td>Properties: ICV-retrieving</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr></table>

## Prototypes

C / C++

int omp\_get\_thread\_limit(void);

C / C++

Fortran

integer function omp\_get\_thread\_limit()

Fortran

Effect

The omp\_get\_thread\_limit routine returns the value of the thread-limit-var ICV. Thus, it returns the maximum number of threads available to execute tasks in the current contention group.

Cross References

• thread-limit-var ICV, see Table 3.1

## 21.6 omp\_in\_parallel Routine

<table><tr><td colspan="2">Name: omp_in_parallelCategory: function</td><td>Properties: default</td></tr><tr><td colspan="3">Return Type</td></tr><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>logical</td><td>default</td></tr><tr><td colspan="3">PrototypesC / C++int omp_in_parallel(void);C / C++Fortranlogical function omp_in_parallel()Fortran</td></tr></table>

The efect of the omp\_in\_parallel routine is to return true if the current task is enclosed by an active parallel region, and the parallel region is enclosed by the outermost initial task region on the device. That is, it returns true if the active-levels-var ICV is greater than zero. Otherwise, it returns false.

## Cross References

• active-levels-var ICV, see Table 3.1

• parallel Construct, see Section 12.1

## 21.7 omp\_set\_dynamic Routine

Return Type

<table><tr><td>Name: omp_set_dynamicCategory: subroutine</td><td>Properties: ICV-modifying</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>dynamic_threads</td><td>logical</td><td>default</td></tr></table>

Prototypes

C / C++

void omp\_set\_dynamic(int dynamic\_threads);

C / C++

Fortran

subroutine omp\_set\_dynamic(dynamic\_threads)

logical dynamic\_threads

Fortran

## Effect

For implementations that support dynamic adjustment of the number of threads, if the argument to omp\_set\_dynamic evaluates to true, dynamic adjustment is enabled for the current task by setting the value of the dyn-var ICV to true; otherwise, dynamic adjustment is disabled for the current task by setting the value of the dyn-var ICV to false. For implementations that do not support dynamic adjustment of the number of threads, this routine has no efect: the value of dyn-var remains false.

Cross References

• dyn-var ICV, see Table 3.1

## 21.8 omp\_get\_dynamic Routine

<table><tr><td>Name: omp_get_dynamicCategory: function</td><td>Properties: ICV-retrieving</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>logical</td><td>default</td></tr></table>

Prototypes

C / C++

int omp\_get\_dynamic(void);

C / C++

Fortran

logical function omp\_get\_dynamic()

Fortran

The omp\_get\_dynamic routine returns the value of the dyn-var ICV. Thus, this routine returns true if dynamic adjustment of the number of threads is enabled for the current task; otherwise, it returns false. If an implementation does not support dynamic adjustment of the number of threads, then this routine always returns false.

Cross References

• dyn-var ICV, see Table 3.1

## 21.9 omp\_set\_schedule Routine

<table><tr><td>Name: omp_set_scheduleCategory: subroutine</td><td>Properties: ICV-modifying</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>kind</td><td>sched</td><td>omp</td></tr><tr><td>chunk_size</td><td>integer</td><td>default</td></tr></table>

C / C++

void omp\_set\_schedule(omp\_sched\_t kind, int chunk\_size);

C / C++

subroutine omp\_set\_schedule(kind, chunk\_size)

integer (kind=omp\_sched\_kind) kind

Fortran

21 The efect of this routine is to set the value of the run-sched-var ICV of the current task to the 22 values specified in the two arguments. Thus, the routine afects the schedule that is applied when 23 runtime is used as the schedule type.

The schedule is set to the schedule type that is specified by the first argument kind. For the schedule types omp\_sched\_static, omp\_sched\_dynamic, and omp\_sched\_guided, the chunk\_size is set to the value of the second argument, or to the default chunk\_size if the value of the second argument is less than 1; for the schedule type omp\_sched\_auto, the second argument is ignored; for implementation defined schedule types, the values and associated meanings of the second argument are implementation defined.

## Cross References

• run-sched-var ICV, see Table 3.1

• OpenMP sched Type, see Section 20.5.1

## 21.10 omp\_get\_schedule Routine

<table><tr><td>Name: omp_get_scheduleCategory: subroutine</td><td>Properties: ICV-retrieving</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>kind</td><td>sched</td><td>C/C++ pointer, omp</td></tr><tr><td>chunk_size</td><td>integer</td><td>C/C++ pointer</td></tr></table>

## Prototypes

C / C++

void omp\_get\_schedule(omp\_sched\_t <sub>\*</sub>kind, int <sub>\*</sub>chunk\_size);

C / C++

Fortran

subroutine omp\_get\_schedule(kind, chunk\_size)

integer (kind=omp\_sched\_kind) kind

integer chunk\_size

Fortran

## Effect

The omp\_get\_schedule routine returns the run-sched-var ICV in the task to which the routine binds. Thus, the routine returns the schedule that is applied when the runtime schedule type is used. The first argument kind returns the schedule type to be used. If the returned schedule type is omp\_sched\_static, omp\_sched\_dynamic, or omp\_sched\_guided, the second argument, chunk\_size, returns the chunk size to be used, or a value less than 1 if the default chunk size is to be used. The value returned by the second argument is implementation defined for any other schedule types.

## Cross References

• run-sched-var ICV, see Table 3.1

• OpenMP sched Type, see Section 20.5.1

## 21.11 omp\_get\_supported\_active\_levels Routine

<table><tr><td>Name:omp_get_supported_active_levelsCategory: function</td><td>Properties: default</td></tr></table>

Return Type

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr></table>

## Prototypes

C / C++

int omp\_get\_supported\_active\_levels(void);

C / C++

Fortran

integer function omp\_get\_supported\_active\_levels()

Fortran

## Effect

The omp\_get\_supported\_active\_levels routine returns the number of supported active levels. The max-active-levels-var ICV cannot have a value that is greater than this number. The value that the omp\_get\_supported\_active\_levels routine returns is implementation defined, but it must be greater than 0.

Cross References

• max-active-levels-var ICV, see Table 3.1

## 21.12 omp\_set\_max\_active\_levels Routine

<table><tr><td>Name: omp_set_max_active_levelsCategory: subroutine</td><td>Properties: ICV-modifying</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>max_levels</td><td>integer</td><td>non-negative</td></tr></table>

Prototypes

C / C++

void omp\_set\_max\_active\_levels(int max\_levels);

C / C++

Fortran

subroutine omp\_set\_max\_active\_levels(max\_levels)

integer max\_levels

Fortran

## Effect

The efect of this routine is to set the value of the max-active-levels-var ICV to the value specified in the argument. Thus, the routine limits the number of nested active parallel regions when a new nested parallel region is generated by the current task.

If the number of active levels requested exceeds the number of supported active levels, the value of the max-active-levels-var ICV will be set to the number of supported active levels. If the number of active levels requested is less than the value of the active-levels-var ICV, the value of the max-active-levels-var ICV will be set to an implementation defined value between the requested number and active-levels-var, inclusive.

## Cross References

• active-levels-var ICV, see Table 3.1

• max-active-levels-var ICV, see Table 3.1

• parallel Construct, see Section 12.1

## 21.13 omp\_get\_max\_active\_levels Routine

<table><tr><td>Name: omp_get_max_active_levelsCategory: function</td><td>Properties: ICV-retrieving</td></tr></table>

Return Type

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr></table>

## Prototypes

C / C++

int omp\_get\_max\_active\_levels(void);

C / C++ C/C++

Fortran

integer function omp\_get\_max\_active\_levels()

Fortran

The omp\_get\_max\_active\_levels routine returns the value of the max-active-levels-var ICV. The current task may only generate an active parallel region if the returned value is greater than the value of the active-levels-var ICV.

## Cross References

• max-active-levels-var ICV, see Table 3.1

## 21.14 omp\_get\_level Routine

<table><tr><td colspan="2">Name: omp_get_levelCategory: function</td><td colspan="2">Properties: ICV-retrieving</td></tr><tr><td colspan="4">Return Type</td></tr><tr><td>Name</td><td colspan="2">Type</td><td>Properties</td></tr><tr><td></td><td colspan="2">integer</td><td>default</td></tr><tr><td colspan="4">PrototypesC / C++int omp_get_level(void);C / C++Fortraninteger function omp_get_level()Fortran</td></tr></table>

The omp\_get\_level routine returns the value of the levels-var ICV. Thus, its efect is to return the number of nested parallel regions (whether active or inactive) that enclose the current task such that all of the parallel regions are enclosed by the outermost initial task region on the current device.

Cross References

• levels-var ICV, see Table 3.1

• parallel Construct, see Section 12.1

## 21.15 omp\_get\_ancestor\_thread\_num Routine

<table><tr><td>Name: omp_get_ancestor_thread_numCategory: function</td><td>Properties: default</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>level</td><td>integer</td><td>default</td></tr></table>

## Prototypes

C / C++

int omp\_get\_ancestor\_thread\_num(int level);

C / C++

Fortran

integer function omp\_get\_ancestor\_thread\_num(level) integer level

Fortran

## Effect

The omp\_get\_ancestor\_thread\_num routine returns the thread number of the ancestor thread at a given nest level of the encountering thread or the thread number of the encountering thread. If the requested nest level is outside the range of 0 and the nest level of the encountering thread, as returned by the omp\_get\_level routine, the routine returns -1.

Note – When the omp\_get\_ancestor\_thread\_num routine is called with value of level =0, the routine always returns 0. If level =omp\_get\_level(), the routine has the same efect as the omp\_get\_thread\_num routine.

Cross References

• omp\_get\_level Routine, see Section 21.14

• omp\_get\_thread\_num Routine, see Section 21.3

## 21.16 omp\_get\_team\_size Routine

<table><tr><td>Name: omp_get_team_sizeCategory: function</td><td>Properties: default</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>level</td><td>integer</td><td>default</td></tr></table>

![](images/17bbf07c6c2b80d04ff211bfcae91dd5eba948af4839e87cacc4e4097b892e01.jpg)

## Prototypes

C / C++

int omp\_get\_team\_size(int level);

C / C++

Fortran

integer function omp\_get\_team\_size(level)

integer level

Fortran

## Effect

The omp\_get\_team\_size routine returns the size of the current team to which the ancestor thread or the encountering task belongs. If the requested nested level is outside the range of 0 and the nested level of the encountering thread, as returned by the omp\_get\_level routine, the routine returns -1. Inactive parallel regions are regarded as active parallel regions executed with one thread.

Note – When the omp\_get\_team\_size routine is called with a value of level =0, the routine always returns 1. If level =omp\_get\_level(), the routine has the same efect as the omp\_get\_num\_threads routine.

Cross References

• omp\_get\_level Routine, see Section 21.14

• omp\_get\_num\_threads Routine, see Section 21.2

## 21.17 omp\_get\_active\_level Routine

<table><tr><td>Name: omp_get_active_levelCategory: function</td><td>Properties: ICV-retrieving</td></tr></table>

Return Type

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr></table>

## Prototypes

C / C++

int omp\_get\_active\_level(void);

C / C++

Fortran

integer function omp\_get\_active\_level()

Fortran

## Effect

The efect of the omp\_get\_active\_level routine is to return the number of nested active parallel regions that enclose the current task such that all parallel regions are enclosed by the outermost initial task region on the current device. Thus, the routine returns the value of the active-levels-var ICV.

## Cross References

• active-levels-var ICV, see Table 3.1

• parallel Construct, see Section 12.1

## 22 Teams Region Routines
