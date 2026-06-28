
• OMPD team\_generator Type, see Section 39.13

## 3.5 ICV Override Relationships

Section 3.5 shows the override relationships among construct clauses and ICVs. The table only lists ICVs that can be overridden by a clause.

TABLE 3.4: ICV Override Relationships

<table><tr><td>ICV</td><td>Clause, if used</td></tr><tr><td>bind-var</td><td>proc_bind</td></tr><tr><td>def-allocator-var</td><td>allocate, allocator</td></tr><tr><td>nteams-var</td><td>num_teams</td></tr><tr><td>nthreads-var</td><td>num_threads</td></tr><tr><td>run-sched-var</td><td>schedule</td></tr><tr><td>teams-thread-limit-var</td><td>thread_limit</td></tr></table>

If a schedule clause specifies a modifier then that modifier overrides any modifier that is specified in the run-sched-var ICV.

If bind-var is not set to false then the proc\_bind clause overrides the value of the first element of the bind-var ICV; otherwise, the proc\_bind clause has no efect.

## Cross References

• allocate Clause, see Section 8.6

• allocator Clause, see Section 8.4

• num\_teams Clause, see Section 12.2.1

• num\_threads Clause, see Section 12.1.2

• proc\_bind Clause, see Section 12.1.4

• schedule Clause, see Section 13.6.3

• thread\_limit Clause, see Section 15.3

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
