
The OMP\_CANCELLATION environment variable sets the initial value of the cancel-var ICV. The value of this environment variable must be one of the following:

true | false

If the environment variable is set to true, the efects of the cancel construct and of cancellation points are enabled (i.e., cancellation is enabled). If the environment variable is set to false, cancellation is disabled and cancel constructs and cancellation points are efectively ignored. The behavior of the program is implementation defined if OMP\_CANCELLATION is set to neither true nor false.

## Cross References

• cancel Construct, see Section 18.2

• cancel-var ICV, see Table 3.1

## 4.3.7 OMP\_AVAILABLE\_DEVICES

The OMP\_AVAILABLE\_DEVICES environment variable sets the available-devices-var ICV and determines the available non-host devices and their device numbers by permitting selection of devices from the set of supported accessible devices and by ordering them. This ICV is initialized before any other ICV that uses a device number, depends on the number of available devices, or permits device-specific environment variables. After the available-devices-var ICV is initialized, only those devices that the ICV identifies are available devices and the omp\_get\_num\_devices routine returns the number of devices stored in the ICV.

The value of this environment variable must be a comma-separated list. Each item is either a trait specification as specified in the following or \*. A \* expands to all non-host accessible devices that are supported devices while a trait specification expands to a possibly empty set of accessible and supported devices for which the specification is fulfilled. After expansion, further selection via an optional array subscript syntax and removal of devices that appear in previous items, each item contains an unordered set of devices. A consecutive unique device number is then assigned to each device in the sets, starting with device number zero, where the device number of the first device in an item is the total number of devices in all previous items.

Traits are specified by the case-insensitive trait name followed by the argument in parentheses. The permitted traits are kind(kind-name), isa(isa-name), arch(arch-name),

vendor(vendor-name), and uid(uid-string), where the names are as specified in Section 9.1 and the OpenMP Additional Definitions document; the kind-name host is not permitted. Multiple traits can be combined using the binary operators && and || to require both or either trait, respectively. Parentheses can be used for grouping, but are optional except that && and || may not appear in the same grouping level. The unary ! operator inverts the meaning of the immediately following trait or parenthesized group.

Each trait specification or \* yields a (possibly zero-sized) array of non-host devices with the lowest array element, if it exists, having index zero. The C/C++ syntax [index] can be used to select an element and the array section syntax for C/C++ as specified in Section 5.2.5 can be used to specify a subset of elements. Any array element specified by the subscript that is outside the bounds of the array resulting from the trait specification or \* is silently excluded.

## Example:

Four GPUs are accessible and supported, with unique identifiers represented as <uid-gpu0>,...,<uid-gpu3>.

```txt
export OMPAVAILABLE_DEVICES="kind(gpu)"
```

export OMP\_AVAILABLE\_DEVICES="uid(<uid-gpu0>),kind(gpu)"

export OMP\_AVAILABLE\_DEVICES="uid(<uid-gpu1>),kind(gpu)[:2]"

where the above OMP\_AVAILABLE\_DEVICES assignments select:

• All GPUs;

• All GPUs with device <uid-gpu0> assigned device number 0; and

• Device <uid-gpu1>, which is assigned device number 0, and two other GPUs.

## Cross References

• Device Directives and Clauses, see Chapter 15

• available-devices-var ICV, see Table 3.1

## 4.3.8 OMP\_DEFAULT\_DEVICE

The OMP\_DEFAULT\_DEVICE environment variable sets the initial value of the default-device-var ICV. The value of this environment variable must be a comma-separated list, each item being either a non-negative integer value that denotes the device number, a trait specification with an optional subscript selector, or one of the following case-insensitive string literals: initial to specify the host device, invalid to specify the device number omp\_invalid\_device, or default to set the ICV as if this environment variable was not specified (see Section 1.2).

The trait specification is as described for OMP\_AVAILABLE\_DEVICES (see Section 4.3.7), except that in addition the trait device\_num(device number) may be specified and host is permitted as kind-name. The device numbers yielded by the trait specification are sorted in ascending order by device number and form a set; the array-element syntax as described for

OMP\_AVAILABLE\_DEVICES can be used to select an element from this set. If an item is an empty set, non-existing element, or does not evaluate to an available device, the next item is evaluated; otherwise, the default-device-var ICV is set to the first value of the set. However, initial, invalid, and default always match. If none of the list items match, the default-device-var ICV is set to omp\_invalid\_device.

Example:

Four GPUs are accessible and supported, with unique identifiers represented as <uid-gpu0>,...,<uid-gpu3>. The default device is set to device <uid-gpu0>.

export OMP\_DEFAULT\_DEVICE="uid(<uid-gpu0>)"

## Cross References

• Device Directives and Clauses, see Chapter 15

• default-device-var ICV, see Table 3.1

## 4.3.9 OMP\_TARGET\_OFFLOAD

The OMP\_TARGET\_OFFLOAD environment variable sets the initial value of the target-ofload-var ICV. Its value must be one of the following:

## mandatory | disabled | default

The mandatory value specifies that the efect of any device construct or device routine that uses a device that is not an available device or a supported device, or uses a non-conforming device number, is as if the omp\_invalid\_device device number was used. Support for the disabled value is implementation defined. If an implementation supports it, the behavior is as if the only device is the host device. The default value specifies the default behavior as described in Section 1.2.

Example:

export OMP\_TARGET\_OFFLOAD=mandatory

## Cross References

• Device Directives and Clauses, see Chapter 15

• Device Memory Routines, see Chapter 25

• target-ofload-var ICV, see Table 3.1

## 4.3.10 OMP\_THREADS\_RESERVE

The OMP\_THREADS\_RESERVE environment variable controls the number of reserved threads in each contention group by setting the initial value of the structured-thread-limit-var and the free-agent-thread-limit-var ICVs.

The OMP\_THREADS\_RESERVE environment variable can be defined using a non-negative integer or an unordered list of reservations. Each reservation specifies a thread-reservation type, for which the possible values are listed in Table 4.3. The reservation type may be appended with one non-negative number in parentheses, that is, reservation\_type(<num-threads>), where <num-threads> denotes the number of threads to reserve for that reservation type. If only a non-negative integer is provided, this number denotes the number of threads to reserve for structured parallelism. If only one reservation type is provided, and its <num-threads> is not specified, the number of threads to reserve is thread-limit-var if the reservation type is structured, or thread-limit-var minus 1 if the reservation type is free\_agent.

TABLE 4.3: Reservation Types for OMP\_THREADS\_RESERVE

<table><tr><td>Reservation Type</td><td>Meaning</td><td>Default Value</td></tr><tr><td>structured</td><td>Threads reserved for structured threads</td><td>1</td></tr><tr><td>free_agent</td><td>Threads reserved for free-agent threads</td><td>0</td></tr></table>

The OMP\_THREADS\_RESERVE environment variable sets the initial value of the structured-thread-limit-var and the free-agent-thread-limit-var ICVs according to Algorithm 4.1.

```ocaml
Algorithm 4.1 Initial structured-thread-limit-var and free-agent-thread-limit-var ICVs Values
let structured-reserve be the number of threads to reserve for structured threads;
let free-agent-reserve be the number of threads to reserve for free-agent threads;
let threads-reserve be the sum of structured-reserve and free-agent-reserve;
if (structured-reserve < 1) then structured-reserve = 1;
if (free-agent-reserve = thread-limit-var) then free-agent-reserve = free-agent-reserve - 1;
if (threads-reserve ≤ thread-limit-var) then
    structured-thread-limit-var = thread-limit-var - free-agent-reserve;
    free-agent-thread-limit-var = thread-limit-var - structured-reserve;
else behavior is implementation defined
```

The following grammar describes the values accepted for the OMP\_THREADS\_RESERVE environment variable.

$$
\langle \text {reserve} \rangle \models \langle \text {res - list} \rangle \mid \langle \text {res - type} \rangle \mid \langle \text {res - num} \rangle
$$

$$
\langle \text {res - list} \rangle \models \langle \text {res} \rangle \mid \langle \text {res - list} \rangle , \langle \text {res} \rangle
$$

$$
\langle \text {res} \rangle \models \langle \text {res - type} \rangle (\langle \text {res - num} \rangle)
$$

$$
\langle \text {res - type} \rangle \models \text {structured} \mid \text {free\_agent}
$$

$$
\langle \text {res - num} \rangle \models \text {non - negative integer}
$$

Examples:

```txt
export OMP_THREADS_RESERVE=4
export OMP_THREADS_RESERVE="structured(4)"
export OMP_THREADS_RESERVE="structured"
export OMP_THREADS_RESERVE="structured(2),free_agent(2)"
```

where the first two definitions correspond to the same reservation for structured parallelism, the third definition reserves all available threads for structured parallelism, and the last one reserves threads for both structured parallelism and free-agent threads.

## Cross References

• free-agent-thread-limit-var ICV, see Table 3.1

• structured-thread-limit-var ICV, see Table 3.1

• parallel Construct, see Section 12.1

• threadset Clause, see Section 14.8

## 4.3.11 OMP\_MAX\_TASK\_PRIORITY

The OMP\_MAX\_TASK\_PRIORITY environment variable controls the use of task priorities by setting the initial value of the max-task-priority-var ICV. The value of this environment variable must be a non-negative integer.

Example:

```txt
export OMP_MAX_TASK_PRIORITY=20
```

## Cross References

• max-task-priority-var ICV, see Table 3.1

## 4.4 Memory Allocation Environment Variables

This section defines environment variables that afect memory allocations.

## 4.4.1 OMP\_ALLOCATOR

The OMP\_ALLOCATOR environment variable sets the initial value of the def-allocator-var ICV that specifies the default allocator for allocation calls, directives and clauses that do not specify an allocator. The following grammar describes the values accepted for the OMP\_ALLOCATOR environment variable.

⟨allocator⟩ |= ⟨predef-allocator⟩ | ⟨predef-mem-space⟩ | ⟨predef-mem-space⟩:⟨traits⟩

⟨traits⟩ |= ⟨trait⟩=⟨value⟩ | ⟨trait⟩=⟨value⟩,⟨traits⟩

⟨predef-allocator⟩ |= one of the predefined allocators from Table 8.3

⟨predef-mem-space⟩ |= one of the predefined memory spaces from Table 8.1

⟨trait⟩ |= one of the allocator trait names from Table 8.2

⟨value⟩ |= one of the allowed values from Table 8.2 | non-negative integer

| ⟨predef-allocator⟩

The value can be an integer only if the trait accepts a numerical value, for the fb\_data trait the value can only be predef-allocator. If the value of this environment variable is not a predefined allocator then a new allocator with the given predefined memory space and optional traits is created and set as the def-allocator-var ICV. If the new allocator cannot be created, the def-allocator-var ICV will be set to omp\_default\_mem\_alloc.

## Example:

```txt
export OMP_ALLOCATOR=omp_high_bw_mem_alloc
export OMP_ALLOCATOR="omp_large_cap_mem_space:alignment=16,\pinned=true"
export OMP_ALLOCATOR="omp_high_bw_mem_space:pool_size=1048576,\fallback=allocator_fb,fb_data=omp_low_lat_mem_alloc"
```

## Cross References

• Memory Allocators, see Section 8.2

• def-allocator-var ICV, see Table 3.1

## 4.5 OMPT Environment Variables

This section defines environment variables that afect operation of the OMPT tool interface.

## 4.5.1 OMP\_TOOL

The OMP\_TOOL environment variable sets the tool-var ICV, which controls whether an OpenMP runtime will try to register a first-party tool. The value of this environment variable must be one of the following:

## enabled | disabled

If OMP\_TOOL is set to any value other than enabled or disabled, the behavior is unspecified. If OMP\_TOOL is not defined, the default value for tool-var is enabled.

Example: export OMP\_TOOL=enabled

## Cross References

• OMPT Overview, see Chapter 32

• tool-var ICV, see Table 3.1

## 4.5.2 OMP\_TOOL\_LIBRARIES

The OMP\_TOOL\_LIBRARIES environment variable sets the tool-libraries-var ICV to a list of tool libraries that are considered for use on a device on which an OpenMP implementation is being initialized. The value of this environment variable must be a list of names of dynamically-loadable libraries, separated by an implementation specific, platform typical separator. Whether the value of this environment variable is case sensitive is implementation defined.

If the tool-var ICV is not enabled, the value of tool-libraries-var is ignored. Otherwise, if ompt\_start\_tool is not visible in the address space on a device where OpenMP is being initialized or if ompt\_start\_tool returns NULL, an OpenMP implementation will consider libraries in the tool-libraries-var list in a left-to-right order. The OpenMP implementation will search the list for a library that meets two criteria: it can be dynamically loaded on the current device and it defines the symbol ompt\_start\_tool. If an OpenMP implementation finds a suitable library, no further libraries in the list will be considered.

Example:

export OMP\_TOOL\_LIBRARIES=libtoolXY64.so:/usr/local/lib/ libtoolXY32.so

## Cross References

• OMPT Overview, see Chapter 32

• tool-libraries-var ICV, see Table 3.1

• ompt\_start\_tool Procedure, see Section 32.2.1

## 4.5.3 OMP\_TOOL\_VERBOSE\_INIT

The OMP\_TOOL\_VERBOSE\_INIT environment variable sets the tool-verbose-init-var ICV, which controls whether an OpenMP implementation will verbosely log the registration of a tool. The value of this environment variable must be one of the following:

```txt
disabled|stdout|stderr|<filename>
```

If OMP\_TOOL\_VERBOSE\_INIT is set to any value other than case insensitive disabled, stdout, or stderr, the value is interpreted as a filename and the OpenMP runtime will try to log to a file with prefix filename. If the value is interpreted as a filename, whether it is case sensitive is implementation defined. If opening the logfile fails, the output will be redirected to stderr. If OMP\_TOOL\_VERBOSE\_INIT is not defined, the default value for tool-verbose-init-var is disabled. Support for logging to stdout or stderr is implementation defined. Unless tool-verbose-init-var is disabled, the OpenMP runtime will log the steps of the tool activation process defined in Section 32.2.2 to a file with a name that is constructed using the provided filename prefix. The format and detail of the log is implementation defined. At a minimum, the log will contain one of the following:

• That the tool-var ICV is disabled;

• An indication that a tool was available in the address space at program launch; or

• The path name of each tool in OMP\_TOOL\_LIBRARIES that is considered for dynamic loading, whether dynamic loading was successful, and whether the ompt\_start\_tool procedure is found in the loaded library.

In addition, if an ompt\_start\_tool procedure is called the log will indicate whether or not the tool will use the OMPT interface.

## Example:

export OMP\_TOOL\_VERBOSE\_INIT=disabled export OMP\_TOOL\_VERBOSE\_INIT=STDERR export OMP\_TOOL\_VERBOSE\_INIT=ompt\_load.log

## Cross References

• OMPT Overview, see Chapter 32

• tool-verbose-init-var ICV, see Table 3.1

## 4.6 OMPD Environment Variables
