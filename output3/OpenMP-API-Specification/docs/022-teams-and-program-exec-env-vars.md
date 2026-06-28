
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
