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
