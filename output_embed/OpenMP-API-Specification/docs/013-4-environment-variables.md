## 4 Environment Variables

This chapter describes the OpenMP environment variables that specify the settings of the ICVs that afect the execution of OpenMP programs (see Chapter 3). The names of the environment variables must be upper case. Unless otherwise specified, the values assigned to the environment variables are case insensitive and may have leading and trailing white space. The assigned values for most environment variables are strings or integers. In particular, boolean values are specified as the string true or false. Modifications to the environment variables after the program has started, even if modified by the program itself, are ignored by the OpenMP implementation. However, the settings of some of the ICVs can be modified during the execution of the OpenMP program by the use of the appropriate directive clauses or OpenMP API routines. These examples demonstrate how to set the OpenMP environment variables in diferent environments:

• csh-like shells:

setenv OMP\_SCHEDULE "dynamic"

• bash-like shells:

```txt
export OMP_SCHEDULE="dynamic"
```

• Windows Command Line:

set OMP\_SCHEDULE=dynamic

As defined in Section 3.2, device-specific environment variables extend many of the environment variables defined in this chapter. If the corresponding environment variable for a specific device number is set, then the setting for that environment variable is used to set the value of the associated ICV of the device with the corresponding device number. If the corresponding environment variable that includes the \_DEV sufix but no device number is set, then its setting is used to set the value of the associated ICV of any non-host device for which the device number-specific corresponding environment variable is not set. The corresponding environment variable without a sufix sets the associated ICV of the host device. If the corresponding environment variable includes the \_ALL sufix, the setting of that environment variable is used to set the value of the associated ICV of any host or non-host device for which corresponding environment variables that are device number specific through the use of the \_DEV sufix or the absence of a sufix are not set.

## Restrictions

Restrictions to device-specific environment variables are as follows:

• Device-specific environment variables must not correspond to environment variables that initialize ICVs with global ICV scope.

• Device-specific environment variables must not specify the host device.

## 4.1 Parallel Region Environment Variables

This section defines environment variables that afect the operation of parallel regions.

## 4.1.1 Abstract Name Values

This section defines abstract names that must be understood by the execution and runtime environment for the environment variables that explicitly allow them. The entities defined by the abstract names are implementation defined. There are two kinds of abstract names: conceptual abstract names and numeric abstract names.

Conceptual abstract names include place-list abstract names that are the strings defined in Table 4.1. If an environment variable is set to a value that includes a place-list abstract name, the behavior is as if the place-list abstract name were replaced with the list of places associated with that abstract name on each device where the environment variable is applied.

TABLE 4.1: Predefined Place-list Abstract Names

<table><tr><td>Abstract Name</td><td>Meaning</td></tr><tr><td>threads</td><td>A set where each place corresponds to a single hardware thread of the device.</td></tr><tr><td>cores</td><td>A set where each place corresponds to a single core of the device.</td></tr><tr><td>11_caches</td><td>A set where each place corresponds to the set of cores for a single last-level cache of the device.</td></tr><tr><td>numa_domains</td><td>A set where each place corresponds to the set of cores for a single NUMA domain of the device.</td></tr><tr><td>sockets</td><td>A set where each place corresponds to the set of cores for a single socket of the device.</td></tr></table>

For each place-list abstract name specified in Table 4.1, a corresponding place-count abstract name prefixed with n\_ also exists for which the associated value is the number of places in the list of places specified by the place-list abstract name, as described above.

If an environment variable is set to a value that includes a numeric abstract name, the behavior is as if the numeric abstract name were replaced with the value associated with that numeric abstract name.

## 4.1.2 OMP\_DYNAMIC

The OMP\_DYNAMIC environment variable controls dynamic adjustment of the number of threads to use for executing parallel regions by setting the initial value of the dyn-var ICV.

The value of this environment variable must be one of the following:

## true | false

If the environment variable is set to true, the OpenMP implementation may adjust the number of threads to use for executing parallel regions in order to optimize the use of system resources. If the environment variable is set to false, the dynamic adjustment of the number of threads is disabled. The behavior of the program is implementation defined if the value of OMP\_DYNAMIC is neither true nor false.

## Example:

## export OMP\_DYNAMIC=true

## Cross References

• dyn-var ICV, see Table 3.1

• omp\_get\_dynamic Routine, see Section 21.8

• omp\_set\_dynamic Routine, see Section 21.7

• parallel Construct, see Section 12.1

## 4.1.3 OMP\_NUM\_THREADS

The OMP\_NUM\_THREADS environment variable sets the number of threads to use for parallel regions by setting the initial value of the nthreads-var ICV. See Chapter 3 for a comprehensive set of rules about the interaction between the OMP\_NUM\_THREADS environment variable, the num\_threads clause, the omp\_set\_num\_threads routine and dynamic adjustment of threads, and Section 12.1.1 for a complete algorithm that describes how the number of threads for a parallel region is determined.

The value of this environment variable must be a list of positive integer values and/or numeric abstract names. The values of the list set the number of threads to use for parallel regions at the corresponding nested levels.

The behavior of the program is implementation defined if any value of the list specified in the OMP\_NUM\_THREADS environment variable leads to a number of threads that is greater than an implementation can support or if any value is not a positive integer.

The OMP\_NUM\_THREADS environment variable sets the max-active-levels-var ICV to the number of active levels of parallelism that the implementation supports if the OMP\_NUM\_THREADS environment variable is set to a comma-separated list of more than one value. The value of the max-active-levels-var ICV may be overridden by setting OMP\_MAX\_ACTIVE\_LEVELS. See Section 4.1.5 for details.

Example:

export OMP\_NUM\_THREADS=4,3,2 export OMP\_NUM\_THREADS=n\_cores,2

## Cross References

• OMP\_MAX\_ACTIVE\_LEVELS, see Section 4.1.5

• nthreads-var ICV, see Table 3.1

• num\_threads Clause, see Section 12.1.2

• omp\_set\_num\_threads Routine, see Section 21.1

• parallel Construct, see Section 12.1

## 4.1.4 OMP\_THREAD\_LIMIT

The OMP\_THREAD\_LIMIT environment variable sets the number of threads to use for a contention group by setting the thread-limit-var ICV. The value of this environment variable must be a positive integer or a numeric abstract name. The behavior of the program is implementation defined if the requested value of OMP\_THREAD\_LIMIT is greater than the number of threads that an implementation can support, or if the value is not a positive integer.

## Cross References

• thread-limit-var ICV, see Table 3.1

## 4.1.5 OMP\_MAX\_ACTIVE\_LEVELS

The OMP\_MAX\_ACTIVE\_LEVELS environment variable controls the maximum number of nested active parallel regions by setting the initial value of the max-active-levels-var ICV. The value of this environment variable must be a non-negative integer. The behavior of the program is implementation defined if the requested value of OMP\_MAX\_ACTIVE\_LEVELS is greater than the maximum number of active levels an implementation can support, or if the value is not a non-negative integer.

## Cross References

• max-active-levels-var ICV, see Table 3.1

## 4.1.6 OMP\_PLACES

The OMP\_PLACES environment variable sets the initial value of the place-partition-var ICV. A list of places can be specified in the OMP\_PLACES environment variable. The value of OMP\_PLACES can be one of two types of values: either a place-list abstract name that describes a set of places or an explicit list of places described by non-negative numbers.

The OMP\_PLACES environment variable can be defined using an explicit ordered list of comma-separated places. A place is defined by an unordered set of comma-separated non-negative numbers enclosed by braces, or a non-negative number. The meaning of the numbers and how the numbering is done are implementation defined. Generally, the numbers represent the smallest unit of execution exposed by the execution environment, typically a hardware thread.

Intervals may also be used to define places. Intervals can be specified using the <lower-bound> : <length> : <stride> notation to represent the following list of numbers: “<lower-bound>, <lower-bound> + <stride>, ..., <lower-bound> + (<length> - 1)\*<stride>.” When <stride> is omitted, a unit stride is assumed. Intervals can specify numbers within a place as well as sequences of places.

An exclusion operator “!” can also be used to exclude the number or place immediately following the operator.

Alternatively, the place-list abstract names listed in Table 4.1 should be understood by the execution and runtime environment. The entities defined by the abstract names are implementation defined. An implementation may also add abstract names as appropriate for the target platform.

The abstract name may be appended with one or two positive numbers in parentheses, that is, abstract\_name(<len >) or abstract\_name(<len > : <stride >) where abstract\_name is a place-list abstract name listed in Table 4.1, len denotes the length of the place list and stride denotes the increment between consecutive places in the place list. When requesting fewer places than available on the system, the determination of which resources of type abstract\_name are to be included in the place list is implementation defined. When requesting more resources than available, the length of the place list is implementation defined.

The behavior of the program is implementation defined when the execution environment cannot map a numerical value (either explicitly defined or implicitly derived from an interval) within the OMP\_PLACES list to a processor on the target platform, or if it maps to an unavailable processor. The behavior is also implementation defined when the OMP\_PLACES environment variable is defined using a place-list abstract name.

The following grammar describes the values accepted for the OMP\_PLACES environment variable.

$$
\begin{array}{r l} \langle \text {list} \rangle & \models \langle \text {p - list} \rangle \mid \langle \text {aname} \rangle \\ \langle \text {p - list} \rangle & \models \langle \text {p - interval} \rangle \mid \langle \text {p - list}, \langle \text {p - interval} \rangle \\ \langle \text {p - interval} \rangle & \models \langle \text {place}: \langle \text {len} \rangle : \langle \text {stride} \rangle \mid \langle \text {place}: \langle \text {len} \rangle \mid \langle \text {place} \rangle \mid ! \langle \text {place} \rangle \\ \langle \text {place} \rangle & \models \{\langle \text {res - list} \rangle \} \mid \langle \text {res} \rangle \\ \langle \text {res - list} \rangle & \models \langle \text {res - interval} \rangle \mid \langle \text {res - list}, \langle \text {res - interval} \rangle \\ \langle \text {res - interval} \rangle & \models \langle \text {res}: \langle \text {len} \rangle : \langle \text {stride} \rangle \mid \langle \text {res}: \langle \text {len} \rangle \mid \langle \text {res} \rangle \mid ! \langle \text {res} \rangle \\ \langle \text {aname} \rangle & = \langle \text {word} (\langle \text {len}: \langle \text {stride} \rangle) | \langle \text {word} (\langle \text {len} \rangle) | \langle \text {word} \rangle \end{array}
$$

```txt
⟨word⟩ |= sockets | cores | ll_caches | numa_domains
        | threads | <implementation-defined abstract name>
    ⟨res⟩ |= non-negative integer
    ⟨len⟩ |= positive integer
⟨stride⟩ |= integer
```

```javascript
export OMP_PLACES=threads
export OMP_PLACES="threads(4)"
export OMP_PLACES="threads(8:2)"
export OMP_PLACES
    ="{0,1,2,3},{4,5,6,7},{8,9,10,11},{12,13,14,15}"
export OMP_PLACES="{0:4},{4:4},{8:4},{12:4}"
export OMP_PLACES="{0:4}:4:4"
```

where each of the last three definitions corresponds to the same four places including the smallest units of execution exposed by the execution environment numbered, in turn, 0 to 3, 4 to 7, 8 to 11, and 12 to 15.

## Cross References

• place-partition-var ICV, see Table 3.1

## 4.1.7 OMP\_PROC\_BIND

The OMP\_PROC\_BIND environment variable sets the initial value of the bind-var ICV. The value of this environment variable is either true, false, or a comma separated list of primary, close, or spread. The values of the list set the thread afinity policy to be used for parallel regions at the corresponding nested level. The first value also sets the thread afinity policy to be used for implicit parallel regions.

If the environment variable is set to false, the execution environment may move OpenMP threads between OpenMP places, thread afinity is disabled, and proc\_bind clauses on parallel constructs are ignored.

Otherwise, the execution environment should not move team-worker threads between places, thread afinity is enabled, and the initial thread is bound to the first place in the place-partition-var ICV prior to the first active parallel region, or immediately after encountering the first task-generating construct. An initial thread that is created by a teams construct is bound to the first place in its place-partition-var ICV before it begins execution of the associated structured block. A free-agent thread that executes a task bound to a team is assigned a place according to the rules described in Section 12.1.3.

If the environment variable is set to true, the thread afinity policy is implementation defined but must conform to the previous paragraph. The behavior of the program is implementation defined if the value in the OMP\_PROC\_BIND environment variable is not true, false, or a comma separated list of primary, close, or spread. The behavior is also implementation defined if an initial thread cannot be bound to the first place in the place-partition-var ICV.

The OMP\_PROC\_BIND environment variable sets the max-active-levels-var ICV to the number of active levels of parallelism that the implementation supports if the OMP\_PROC\_BIND environment variable is set to a comma-separated list of more than one element. The value of the max-active-levels-var ICV may be overridden by setting OMP\_MAX\_ACTIVE\_LEVELS. See Section 4.1.5 for details.

## Examples:

export OMP\_PROC\_BIND=false

export OMP\_PROC\_BIND="spread, spread, close"

## Cross References

• OMP\_MAX\_ACTIVE\_LEVELS, see Section 4.1.5

• Controlling OpenMP Thread Afinity, see Section 12.1.3

• bind-var ICV, see Table 3.1

• max-active-levels-var ICV, see Table 3.1

• place-partition-var ICV, see Table 3.1

• omp\_get\_proc\_bind Routine, see Section 29.1

• parallel Construct, see Section 12.1

• proc\_bind Clause, see Section 12.1.4

• teams Construct, see Section 12.2

## 4.2 Teams Environment Variables

This section defines environment variables that afect the operation of teams regions.

## 4.2.1 OMP\_NUM\_TEAMS

The OMP\_NUM\_TEAMS environment variable sets the maximum number of teams created by a teams construct by setting the nteams-var ICV. The value of this environment variable must be a non-negative integer. The behavior of the program is implementation defined if the requested value of OMP\_NUM\_TEAMS is greater than the number of teams that an implementation can support, or if the value is not a positive integer.

## Cross References

• nteams-var ICV, see Table 3.1

• teams Construct, see Section 12.2

## 4.2.2 OMP\_TEAMS\_THREAD\_LIMIT

The OMP\_TEAMS\_THREAD\_LIMIT environment variable sets the maximum number of OpenMP threads that can execute tasks in each contention group created by a teams construct by setting the teams-thread-limit-var ICV. The value of this environment variable must be a positive integer or a numeric abstract name. The behavior of the program is implementation defined if the requested value of OMP\_TEAMS\_THREAD\_LIMIT is greater than the number of threads that an implementation can support, or if the value is neither a positive integer nor one of the allowed abstract names.

## Cross References

• teams-thread-limit-var ICV, see Table 3.1

• teams Construct, see Section 12.2

## 4.3 Program Execution Environment Variables

This section defines environment variables that afect program execution.

## 4.3.1 OMP\_SCHEDULE

The OMP\_SCHEDULE environment variable controls the schedule type and chunk size of all worksharing-loop constructs that have the schedule type runtime, by setting the value of the run-sched-var ICV. The value of this environment variable takes the form [modifier:]kind[, chunk], where:

• modifier is one of monotonic or nonmonotonic;

• kind specifies the schedule type and is one of static, dynamic, guided, or auto;

• chunk is an optional positive integer that specifies the chunk size.

If the modifier is not present, the modifier is set to monotonic if kind is static; for any other kind it is set to nonmonotonic.

If chunk is present, white space may be on either side of the “,”.

The behavior of the program is implementation defined if the value of OMP\_SCHEDULE does not conform to the above format.

## Examples:

```shell
export OMP_SCHEDULE="guided,4"
export OMP_SCHEDULE="dynamic"
export OMP_SCHEDULE="nonmonotonic:dynamic,4"
```

## Cross References

• run-sched-var ICV, see Table 3.1

• schedule Clause, see Section 13.6.3

## 4.3.2 OMP\_STACKSIZE

The OMP\_STACKSIZE environment variable controls the size of the stack for threads, by setting the value of the stacksize-var ICV. The environment variable does not control the size of the stack for an initial thread. Whether this environment variable also controls the size of the stack of native threads is implementation defined. The value of this environment variable takes the form size[unit], where:

• size is a positive integer that specifies the size of the stack for threads.

• unit is B, K, M, or G and specifies whether the given size is in Bytes, Kilobytes (1024 Bytes), Megabytes (1024 Kilobytes), or Gigabytes (1024 Megabytes), respectively. If unit is present, white space may occur between size and it, whereas if unit is not present then K is assumed.

The behavior of the program is implementation defined if OMP\_STACKSIZE does not conform to the above format, or if the implementation cannot provide a stack with the requested size.

## Examples:

```shell
export OMP_STACKSIZE=2000500B
export OMP_STACKSIZE="3000 k "
export OMP_STACKSIZE=10M
export OMP_STACKSIZE=" 10 M "
export OMP_STACKSIZE="20 m "
export OMP_STACKSIZE=" 1G"
export OMP_STACKSIZE=20000
```

## Cross References

• stacksize-var ICV, see Table 3.1

## 4.3.3 OMP\_WAIT\_POLICY

The OMP\_WAIT\_POLICY environment variable provides a hint to an OpenMP implementation about the desired behavior of waiting native threads by setting the wait-policy-var ICV. A compliant implementation may or may not abide by the setting of the environment variable. The value of this environment variable must be one of the following:

## active | passive

The active value specifies that waiting native threads should mostly be active, consuming processor cycles, while waiting. A compliant implementation may, for example, make waiting native threads spin. The passive value specifies that waiting native threads should mostly be passive, not consuming processor cycles, while waiting. For example, a compliant implementation may make waiting native threads yield the processor to other native threads or go to sleep. The details of the active and passive behaviors are implementation defined. The behavior of the program is implementation defined if the value of OMP\_WAIT\_POLICY is neither active nor passive.

## Examples:

export OMP\_WAIT\_POLICY=ACTIVEexport OMP\_WAIT\_POLICY=activeexport OMP\_WAIT\_POLICY=PASSIVEexport OMP\_WAIT\_POLICY=passive

## Cross References

• wait-policy-var ICV, see Table 3.1

## 4.3.4 OMP\_DISPLAY\_AFFINITY

The OMP\_DISPLAY\_AFFINITY environment variable sets the display-afinity-var ICV so that the runtime displays formatted afinity information for the host device. Afinity information is printed for all OpenMP threads in each parallel region upon first entering it. Also, if the information accessible by the format specifiers listed in Table 4.2 changes for any thread in the parallel region then thread afinity information for all threads in that region is again displayed. If the thread afinity for each respective parallel region at each nesting level has already been displayed and the thread afinity has not changed, then the information is not displayed again. Thread afinit information for threads in the same parallel region may be displayed in any order. The value of the OMP\_DISPLAY\_AFFINITY environment variable may be set to one of these values:

## true | false

The true value instructs the runtime to display the thread afinity information, and uses the format setting defined in the afinity-format-var ICV. The runtime does not display the thread afinity information when the value of the OMP\_DISPLAY\_AFFINITY environment variable is false or undefined. For all values of the environment variable other than true or false, the display action is implementation defined.

## Example:

## export OMP\_DISPLAY\_AFFINITY=TRUE

For this example, an OpenMP implementation displays thread afinity information during program execution, in a format given by the afinity-format-var ICV. The following is a sample output:

<table><tr><td>nesting_level=</td><td>1,</td><td>thread_num=</td><td>0,</td><td>thread_affinity=</td><td>0,1</td></tr><tr><td>nesting_level=</td><td>1,</td><td>thread_num=</td><td>1,</td><td>thread_affinity=</td><td>2,3</td></tr></table>

## Cross References

• OMP\_AFFINITY\_FORMAT, see Section 4.3.5

• Controlling OpenMP Thread Afinity, see Section 12.1.3

• afinity-format-var ICV, see Table 3.1

• display-afinity-var ICV, see Table 3.1

## 4.3.5 OMP\_AFFINITY\_FORMAT

The OMP\_AFFINITY\_FORMAT environment variable sets the initial value of the afinity-format-var ICV which defines the format when displaying thread afinity information. The value of this environment variable is case sensitive and leading and trailing white space is significant. Its value is a character string that may contain as substrings one or more field specifiers (as well as other characters). The format of each field specifier is

## %[[[0].] size ] type

where each specifier must contain the percent symbol (%) and a type, that must be either a single character short name or its corresponding long name delimited with curly braces, such as %n or %{thread\_num}. A literal percent is specified as %%. Field specifiers can be provided in any order. The behavior is implementation defined for field specifiers that do not conform to this format.

The 0 modifier indicates whether or not to add leading zeros to the output, following any indication of sign or base. The . modifier indicates the output should be right justified when size is specified. By default, output is left justified. The minimum field length is size, which is a decimal digit string with a non-zero first digit. If no size is specified, the actual length needed to print the field will be used. If the 0 modifier is used with type of A, {thread\_affinity}, H, {host}, or a type that is not printed as a number, the result is unspecified. Any other characters in the format string that are not part of a field specifier will be included literally in the output.

TABLE 4.2: Available Field Types for Formatting OpenMP Thread Afinity Information

<table><tr><td>Short Name</td><td>Long Name</td><td>Meaning</td></tr><tr><td>t</td><td>team_num</td><td>The value returned by omp_get_team_num</td></tr><tr><td>T</td><td>num_teams</td><td>The value returned by omp_get_num_teams</td></tr></table>

table continued on next page

table continued from previous page

<table><tr><td>Short Name</td><td>Long Name</td><td>Meaning</td></tr><tr><td>L</td><td>nesting_level</td><td>The value returned by omp_get_level</td></tr><tr><td>n</td><td>thread_num</td><td>The value returned by omp_get_thread_num</td></tr><tr><td>N</td><td>num_threads</td><td>The value returned by omp_get_num_threads</td></tr><tr><td>a</td><td>ancestor_tnum</td><td>The value returned by omp_get_ancestor_thread_num with an argument of one less than the value returned by omp_get_level</td></tr><tr><td>H</td><td>host</td><td>The name for the host device on which the OpenMP program is running</td></tr><tr><td>P</td><td>process_id</td><td>The process identifier used by the implementation</td></tr><tr><td>i</td><td>native_thread_id</td><td>The native thread identifier used by the implementation</td></tr><tr><td>A</td><td>thread_affinity</td><td>The list of numerical identifiers, in the format of a comma-separated list of integers or integer ranges, that represent processors on which a thread may execute, subject to OpenMP thread affinity control and/or other external affinity mechanisms</td></tr></table>

Implementations may define additional field types. If an implementation does not have information for a field type or an unknown field type is part of a field specifier, "undefined" is printed for this field when displaying thread afinity information.

## Example:

```txt
export OMP_AFFINITY_FORMAT=\
"Thread Affinity: %0.3L %.8n %.15{thread_affinity} %.12H"
```

The above example causes an OpenMP implementation to display thread afinity information in the following form:

<table><tr><td>Thread Affinity: 001</td><td>0</td><td>0-1,16-17</td><td>nid003</td></tr><tr><td>Thread Affinity: 001</td><td>1</td><td>2-3,18-19</td><td>nid003</td></tr></table>

## Cross References

• Controlling OpenMP Thread Afinity, see Section 12.1.3

• afinity-format-var ICV, see Table 3.1

• omp\_get\_ancestor\_thread\_num Routine, see Section 21.15

• omp\_get\_level Routine, see Section 21.14

• omp\_get\_num\_teams Routine, see Section 22.1

• omp\_get\_num\_threads Routine, see Section 21.2

• omp\_get\_thread\_num Routine, see Section 21.3

## 4.3.6 OMP\_CANCELLATION

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
