Part VI Appendices

# A OpenMP Implementation-Defined Behaviors

This appendix summarizes the behaviors that are described as implementation defined in the OpenMP API. Each behavior is cross-referenced back to its description in the main specification. An implementation is required to define and to document its behavior in these cases.

## Chapter 1:

• Memory model: The minimum size at which a memory update may also read and write back adjacent variables that are part of an aggregate variable is implementation defined but is no larger than the base language requires. The manner in which a program can obtain the referenced device address from a device pointer, outside the mechanisms specified by OpenMP, is implementation defined (see Section 1.3.1).

• Device data environments: Whether a variable with static storage duration that is accessible on a device and is not a device-local variable is mapped with a persistent self map at the beginning of the program is implementation defined (see Section 1.3.2).

## Chapter 2:

• Processor: A hardware unit that is implementation defined (see Chapter 2).

• Device: An implementation defined logical execution engine (see Chapter 2).

• Device pointer: An implementation defined handle that refers to a device address (see Chapter 2).

• Supported active levels of parallelism: The maximum number of active parallel regions that may enclose any region of code in an OpenMP program is implementation defined (see Chapter 2).

• Deprecated features: For any deprecated feature, whether any modifications provided by its replacement feature (if any) apply to the deprecated feature is implementation defined (see Chapter 2).

## Chapter 3:

• Internal control variables: The initial values of dyn-var, nthreads-var, run-sched-var, bind-var, stacksize-var, wait-policy-var, thread-limit-var, max-active-levels-var, place-partition-var, afinity-format-var, default-device-var, num-procs-var and def-allocator-var are implementation defined (see Section 3.2).

## Chapter 4:

• OMP\_DYNAMIC environment variable: If the value is neither true nor false, the behavior of the program is implementation defined (see Section 4.1.2).

• OMP\_NUM\_THREADS environment variable: If any value of the specified list leads to a number of threads that is greater than the implementation can support, or if any value is not a positive integer, then the behavior of the program is implementation defined (see Section 4.1.3).

• OMP\_THREAD\_LIMIT environment variable: If the requested value is greater than the number of threads that an implementation can support, or if the value is not a positive integer, the behavior of the program is implementation defined (see Section 4.1.4).

• OMP\_MAX\_ACTIVE\_LEVELS environment variable: If the value is a negative integer or is greater than the maximum number of nested active levels that an implementation can support then the behavior of the program is implementation defined (see Section 4.1.5).

• OMP\_PLACES environment variable: The meaning of the numbers specified in the environment variable and how the numbering is done are implementation defined. The precise definitions of the abstract names are implementation defined. An implementation may add implementation defined abstract names as appropriate for the target platform. When creating a place list of n elements by appending the number n to an abstract name, the determination of which resources to include in the place list is implementation defined. When requesting more resources than available, the length of the place list is also implementation defined. The behavior of the program is implementation defined when the execution environment cannot map a numerical value (either explicitly defined or implicitly derived from an interval) within the OMP\_PLACES list to a processor on the target platform, or if it maps to an unavailable processor. The behavior is also implementation defined when the OMP\_PLACES environment variable is defined using an abstract name (see Section 4.1.6).

• OMP\_PROC\_BIND environment variable: If the value is not true, false, or a comma separated list of primary, close, or spread, the behavior is implementation defined. The behavior is also implementation defined if an initial thread cannot be bound to the first place in the OpenMP place list. The thread afinity policy is implementation defined if the value is true (see Section 4.1.7).

• OMP\_SCHEDULE environment variable: If the value does not conform to the specified format then the behavior of the program is implementation defined (see Section 4.3.1).

• OMP\_STACKSIZE environment variable: If the value does not conform to the specified format or the implementation cannot provide a stack of the specified size then the behavior is implementation defined (see Section 4.3.2).

• OMP\_WAIT\_POLICY environment variable: The details of the active and passive behaviors are implementation defined (see Section 4.3.3).

• OMP\_DISPLAY\_AFFINITY environment variable: For all values of the environment variable other than true or false, the display action is implementation defined (see Section 4.3.4).

OMP\_AFFINITY\_FORMAT environment variable: Additional implementation defined field types can be added (see Section 4.3.5).

• OMP\_CANCELLATION environment variable: If the value is set to neither true nor false, the behavior of the program is implementation defined (see Section 4.3.6).

OMP\_TARGET\_OFFLOAD environment variable: The support of disabled is implementation defined (see Section 4.3.9).

• OMP\_THREADS\_RESERVE environment variable: If the requested values are greater than OMP\_THREAD\_LIMIT, the behavior of the program is implementation defined (see Section 4.3.10).

• OMP\_TOOL\_LIBRARIES environment variable: Whether the value of the environment variable is case sensitive is implementation defined (see Section 4.5.2).

• OMP\_TOOL\_VERBOSE\_INIT environment variable: Support for logging to stdout or stderr is implementation defined. Whether the value of the environment variable is case sensitive when it is treated as a filename is implementation defined. The format and detail of the log is implementation defined (see Section 4.5.3).

• OMP\_DEBUG environment variable: If the value is neither disabled nor enabled, the behavior is implementation defined (see Section 4.6.1).

• OMP\_NUM\_TEAMS environment variable: If the value is not a positive integer or is greater than the number of teams that an implementation can support, the behavior of the program is implementation defined (see Section 4.2.1).

• OMP\_TEAMS\_THREAD\_LIMIT environment variable: If the value is not a positive integer or is greater than the number of threads that an implementation can support, the behavior of the program is implementation defined (see Section 4.2.2).

## Chapter 5:

C / C++

• A pragma directive that uses ompx as the first processing token is implementation defined (see Chapter 5).

• The attribute namespace of an attribute specifier or the optional namespace qualifier within a sequence attribute that uses ompx is implementation defined (see Chapter 5).

C / C++ C++

• Whether a throw executed inside a region that arises from an exception-aborting directive results in runtime error termination is implementation defined (see Chapter 5).

Fortran

• Any directive that uses omx or ompx in the sentinel is implementation defined (see Chapter 5).

Fortran

## Chapter 6:

• Collapsed loops: The particular integer type used to compute the iteration count for the collapsed loop is implementation defined (see Section 6.4.3).

## Chapter 7:

Fortran

• data-sharing attributes: The data-sharing attributes of dummy arguments that do not have the VALUE attribute are implementation defined if the associated actual argument is shared unless the actual argument is a scalar variable, structure, an array that is not a pointer or assumed-shape array, or a simply contiguous array section (see Section 7.1.2).

• threadprivate directive: If the conditions for values of data in the threadprivate memories of threads (other than an initial thread) to persist between two consecutive active parallel regions do not all hold, the allocation status of an allocatable variable in the second region is implementation defined (see Section 7.3).

Fortran

• is\_device\_ptr clause: Support for pointers created outside of the OpenMP device memory routines is implementation defined (see Section 7.5.7).

## Fortran

• has\_device\_addr and use\_device\_addr clauses: The result of inquiring about list item properties other than the CONTIGUOUS attribute, storage location, storage size, array bounds, character length, association status and allocation status is implementation defined (see Section 7.5.9 and Section 7.5.10).

## Fortran

• aligned clause: If the alignment modifier is not specified, the default alignments for SIMD instructions on the target platforms are implementation defined (see Section 7.12).

## Chapter 8:

• Memory spaces: The actual storage resources that each memory space defined in Table 8.1 represents are implementation defined. The mechanism that provides the constant value of the variables allocated in the omp\_const\_mem\_space memory space is implementation defined (see Section 8.1).

• Memory allocators: The minimum size for partitioning allocated memory over storage resources is implementation defined. The default value for the omp\_atk\_pool\_size allocator trait (see Table 8.2) is implementation defined. The memory spaces associated with the predefined omp\_cgroup\_mem\_alloc, omp\_pteam\_mem\_alloc and omp\_thread\_mem\_alloc allocators (see Table 8.3) are implementation defined (see Section 8.2).

## Chapter 9:

• OpenMP context: The accepted isa-name values for the isa trait, the accepted arch-name values for the arch trait and the accepted extension-name values for the extension trait are implementation defined (see Section 9.1).

• Metadirectives: The number of times that each expression of the context selector of a when clause is evaluated is implementation defined (see Section 9.4.1).

Declare variant directives: If two replacement candidates have the same score then their order is implementation defined. The number of times each expression of the context selector of a match clause is evaluated is implementation defined. For calls to constexpr base functions that are evaluated in constant expressions, whether any variant replacement occurs is implementation defined. Any diferences that the specific OpenMP context requires in the prototype of the variant from the base function prototype are implementation defined (see Section 9.6).

• declare\_simd directive: If a SIMD version is created and the simdlen clause is not specified, the number of concurrent arguments for the procedure is implementation defined (see Section 9.8).

• Declare target directives: Whether the same version is generated for diferent devices, or whether a version that is called in a target region difers from the version that is called outside a target region, is implementation defined (see Section 9.9).

## Chapter 10:

• requires directive: Support for any feature specified by a requirement clause on a requires directive is implementation defined (see Section 10.5).

## Chapter 11:

• stripe construct: If a generated ofsetting loop and a generated grid loop are associated with the same construct, the grid loops may execute additional empty logical iterations. The number of empty logical iterations is implementation defined (see Section 11.7).

• tile construct: If a generated grid loop and a generated tile loop are associated with the same construct, the tile loops may execute additional empty logical iterations. The number of empty logical iterations is implementation defined (see Section 11.8).

unroll construct: If no clauses are specified, if and how the loop is unrolled is implementation defined. If the partial clause is specified without an unroll-factor argument then the unroll factor is a positive integer that is implementation defined (see Section 11.9).

## Chapter 12:

• Default safesync for non-host devices: Unless indicated otherwise by a device\_safesync requirement clause, if the parallel construct is encountered on a non-host device then the default behavior is as if the safesync clause appears on the directive with a width value that is implementation defined (see Section 12.1).

• Dynamic adjustment of threads: Providing the ability to adjust the number of threads dynamically is implementation defined (see Section 12.1.1).

• Compile-time message: If the implementation determines that the requested number of threads can never be provided and therefore performs compile-time error termination, the efect of any message clause associated with the directive is implementation defined (see Section 12.1.2).

• Thread afinity: If another OpenMP thread is bound to the place associated with its position, the place to which a free-agent thread is bound is implementation defined. For the spread thread afinity, if $T \leq P$ and T does not divide P evenly, which subpartitions contain ⌈P/T ⌉ places is implementation defined. For the close and spread thread afinity policies, if ET is not zero, which sets have AT positions and which sets have BT positions is implementation defined. Further, the positions assigned to the groups that are assigned sets with BT positions to make the number of positions assigned to each group AT is implementation defined. The determination of whether the thread afinity request can be fulfilled is implementation defined. If the thread afinity request cannot be fulfilled, then the thread afinity of threads in the team is implementation defined (see Section 12.1.3).

• teams construct: The number of teams that are created is implementation defined, but it is greater than or equal to the lower bound and less than or equal to the upper bound values of the num\_teams clause if specified. If the num\_teams clause is not specified, the number of teams is less than or equal to the value of the nteams-var ICV if its value is positive. Otherwise it is an implementation defined positive value (see Section 12.2).

• simd construct: The number of iterations that are executed concurrently at any given time is implementation defined (see Section 12.4).

## Chapter 13:

• single construct: The method of choosing a thread to execute the structured block each time the team encounters the construct is implementation defined (see Section 13.1).

• sections construct: The method of scheduling the structured block sequences among threads in the team is implementation defined (see Section 13.3).

• Worksharing-loop construct: The schedule that is used is implementation defined if the schedule clause is not specified or if the specified schedule has the kind auto. The value of simd\_width for the simd schedule modifier is implementation defined (see Section 13.6).

• distribute construct: If no dist\_schedule clause is specified then the schedule for the distribute construct is implementation defined (see Section 13.7).

## Chapter 14:

• taskloop construct: The number of logical iterations assigned to a task created from a taskloop construct is implementation defined, unless the grainsize or num\_tasks clause is specified (see Section 14.2).

• taskloop construct: For firstprivate variables of class type, the number of invocations of copy constructors to perform the initialization is implementation defined (see Section 14.2).

• taskgraph construct: Whether foreign tasks are recorded or not in a taskgraph record and the manner in which they are executed during a replay execution if they are recorded is implementation defined (see Section 14.3).

![](images/a3d65a7702cd914de77274f1d07fa9726d260fd5d96bda7a1517f4d0f22216b4.jpg)

## Chapter 15:

• thread\_limit clause: The maximum number of threads that participate in executing tasks in the contention group that each team initiates is implementation defined if no thread\_limit clause is specified on the construct. Otherwise, it has the implementation defined upper bound of the teams-thread-limit-var ICV, if the value of this ICV is positive (see Section 15.3).

• target construct: If a device clause is specified with the ancestor device-modifier, whether a storage block on the encountering device that has no corresponding storage on the specified device may be mapped is implementation defined (see Section 15.8).

## Chapter 16:

• prefer-type modifier: The supported preference specifications are implementation defined, including the supported foreign runtime identifiers, which may be non-standard names compatible with the modifier. The default preference specification when the implementation supports multiple values is implementation defined (see Section 16.1.3).

## Chapter 17:

• atomic construct: A compliant implementation may enforce exclusive access between atomic regions that update diferent storage locations. The circumstances under which this occurs are implementation defined. If the storage location designated by x is not size-aligned (that is, if the byte alignment of x is not a multiple of the size of x), then the behavior of the atomic region is implementation defined (see Section 17.8.5).

## Chapter 18:

• None.

## Chapter 19:

• None.

## Chapter 20:

• Runtime routines: Routine names that begin with the ompx\_ prefix are implementation defined extensions to the OpenMP Runtime API (see Chapter 20).

## C / C++

• Runtime library definitions: The types for the allocator\_handle, event\_handle, interop\_fr, memspace\_handle and interop OpenMP types are implementation defined. The value of the omp\_invalid\_device predefined identifier is implementation defined. The value of the omp\_unassigned\_thread predefined identifier is implementation defined (see Chapter 20).

C / C++

Fortran

• Runtime library definitions: Whether the deprecated include file omp\_lib.h or the module omp\_lib (or both) is provided is implementation defined. Whether the omp\_lib.h file provides derived-type definitions or those routines that require an explicit interface is implementation defined. Whether any of the OpenMP API routines that take an argument are extended with a generic interface so arguments of diferent KIND type can be accommodated is implementation defined. The value of the omp\_invalid\_device predefined identifier is implementation defined (see Chapter 20).

## Fortran

• Routine arguments: The behavior is implementation defined if a routine argument is specified with a value that does not conform to the constraints that are implied by the properties of the argument (see Section 20.3).

• Interoperability objects: Implementation defined properties may use non-negative values for properties associated with an interoperability object (see Section 20.7).

## Chapter 21:

• omp\_set\_schedule routine: For any implementation defined schedule types, the values and associated meanings of the second argument are implementation defined (see Section 21.9).

• omp\_get\_schedule routine: The value returned by the second argument is implementation defined for any schedule types other than omp\_sched\_static, omp\_sched\_dynamic and omp\_sched\_guided (see Section 21.10).

• omp\_get\_supported\_active\_levels routine: The number of active levels supported by the implementation is implementation defined, but must be positive (see Section 21.11).

• omp\_set\_max\_active\_levels routine: If the argument is a negative integer then the behavior is implementation defined. If the argument is less than the active-levels-var ICV, the max-active-levels-var ICV is set to an implementation defined value between the value of the argument and the value of active-levels-var, inclusive (see Section 21.12).

## Chapter 22:

• omp\_set\_num\_teams routine: If the argument does not evaluate to a positive integer, the behavior of this routine is implementation defined (see Section 22.2).

• omp\_set\_teams\_thread\_limit routine: If the argument is not a positive integer, the behavior is implementation defined (see Section 22.6).

## Chapter 23:

• None.

## Chapter 24:

• None.

## Chapter 25:

• Rectangular-memory-copying routine: The maximum number of dimensions supported is implementation defined, but must be at least three (see Section 25.7).

## Chapter 26:

• None.

## Chapter 27:

• None.

## Chapter 28:

• Lock routines: If a lock contains a synchronization hint, the efect of the hint is implementation defined (see Chapter 28).

## Chapter 29:

omp\_get\_place\_proc\_ids routine: The meaning of the non-negative numerical identifiers returned by the omp\_get\_place\_proc\_ids routine is implementation defined. The order of the numerical identifiers returned in the array ids is implementation defined (see Section 29.4).

omp\_set\_affinity\_format routine: When called from within any parallel or teams region, the binding thread set (and binding region, if required) for the omp\_set\_affinity\_format region and the efect of this routine are implementation defined (see Section 29.8).

• omp\_get\_affinity\_format routine: When called from within any parallel or teams region, the binding thread set (and binding region, if required) for the omp\_get\_affinity\_format region is implementation defined (see Section 29.9).

• omp\_display\_affinity routine: If the format argument does not conform to the specified format then the result is implementation defined (see Section 29.10).

• omp\_capture\_affinity routine: If the format argument does not conform to the specified format then the result is implementation defined (see Section 29.11).

## Chapter 30:

• omp\_display\_env routine: Whether ICVs with the same value are combined or displayed in multiple lines is implementation defined (see Section 30.4).

## Chapter 31:

• None.

## Chapter 32:

• Tool callbacks: If a tool attempts to register a callback not listed in Table 32.2, whether the registered callback may never, sometimes or always invoke this callback for the associated events is implementation defined (see Section 32.2.4).

• Device tracing: Whether a target device supports tracing or not is implementation defined. If a target device does not support tracing, a NULL may be supplied for the lookup function to the device initializer of a tool (see Section 32.2.5).

• set\_trace\_ompt and get\_record\_ompt entry points: Whether a device-specific tracing interface defines this entry point, indicating that it can collect traces in standard trace format, is implementation defined. The kinds of trace records available for a device is implementation defined (see Section 32.2.5).

## Chapter 33:

• dispatch\_chunk OMPT type: Whether the chunk of a taskloop region is contiguous is implementation defined (see Section 33.14).

• record\_abstract OMPT type: The meaning of a hwid value for a device is implementation defined (see Section 33.24).

• state OMPT type: The set of OMPT thread states supported is implementation defined (see Section 33.31).

## Chapter 34:

• sync\_region\_wait callback: For the implicit-barrier-wait-begin and implicit-barrier-wait-end events at the end of a parallel region, whether the parallel\_data argument is NULL or points to the parallel data of the current parallel region is implementation defined (see Section 34.7.5).

## Chapter 35:

• target\_data\_op\_emi callbacks: Whether dev1\_addr or dev2\_addr points to an intermediate bufer in some operations is implementation defined (see Section 35.7).

## Chapter 36:

• get\_place\_proc\_ids entry point: The meaning of the numerical identifiers returned is implementation defined. The order of ids returned in the array is implementation defined (see Section 36.9).

• get\_partition\_place\_nums entry point: The order of the identifiers returned in the place\_nums array is implementation defined (see Section 36.11).

• get\_proc\_id entry point: The meaning of the numerical identifier returned is implementation defined (see Section 36.12).

## Chapter 37:

• None.

## Chapter 38:

• None.

## Chapter 39:

• None.

## Chapter 40:

• print\_string callback: The value of the category argument is implementation defined (see Section 40.5).

## Chapter 41:

• handle-comparing routines: For all types of handles, the means by which two handles are ordered is implementation defined (see Section 41.7).

## Chapter 42:

• None.
