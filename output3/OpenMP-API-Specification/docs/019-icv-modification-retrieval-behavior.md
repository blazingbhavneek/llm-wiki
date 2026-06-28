
## Cross References

• OMP\_AFFINITY\_FORMAT, see Section 4.3.5

• OMP\_ALLOCATOR, see Section 4.4.1

• OMP\_AVAILABLE\_DEVICES, see Section 4.3.7

• OMP\_CANCELLATION, see Section 4.3.6

• OMP\_DEBUG, see Section 4.6.1

• OMP\_DEFAULT\_DEVICE, see Section 4.3.8

• OMP\_DISPLAY\_AFFINITY, see Section 4.3.4

• OMP\_DYNAMIC, see Section 4.1.2

• OMP\_MAX\_ACTIVE\_LEVELS, see Section 4.1.5

• OMP\_MAX\_TASK\_PRIORITY, see Section 4.3.11

• OMP\_NUM\_TEAMS, see Section 4.2.1

• OMP\_NUM\_THREADS, see Section 4.1.3

• OMP\_PLACES, see Section 4.1.6

• OMP\_PROC\_BIND, see Section 4.1.7

• OMP\_SCHEDULE, see Section 4.3.1

• OMP\_STACKSIZE, see Section 4.3.2

• OMP\_TARGET\_OFFLOAD, see Section 4.3.9

• OMP\_TEAMS\_THREAD\_LIMIT, see Section 4.2.2

• OMP\_THREAD\_LIMIT, see Section 4.1.4

• OMP\_TOOL, see Section 4.5.1

• OMP\_TOOL\_LIBRARIES, see Section 4.5.2

• OMP\_WAIT\_POLICY, see Section 4.3.3

## 3.3 Modifying and Retrieving ICV Values

Section 3.3 shows methods for modifying and retrieving the ICV values. If (none) is listed for an ICV, the OpenMP API does not support its modification or retrieval. Calls to routines retrieve or modify ICVs with data environment ICV scope in the data environment of their binding task set.

TABLE 3.3: Ways to Modify and to Retrieve ICV Values

<table><tr><td>ICV</td><td>Ways to Modify Value</td><td>Ways to Retrieve Value</td></tr><tr><td>active-levels-var</td><td>(none)</td><td>omp_get_active_level</td></tr><tr><td rowspan="2">affinity-format-var</td><td colspan="2">omp_set_affinity_format</td></tr><tr><td></td><td>omp_get_affinity_format</td></tr><tr><td>available-devices-var</td><td>(none)</td><td>(none)</td></tr><tr><td>bind-var</td><td>(none)</td><td>omp_get_proc_bind</td></tr><tr><td>cancel-var</td><td>(none)</td><td>omp_get_cancellation</td></tr><tr><td>debug-var</td><td>(none)</td><td>(none)</td></tr><tr><td rowspan="2">def-allocator-var</td><td colspan="2">omp_set_default_allocator</td></tr><tr><td></td><td>omp_get_default_allocator</td></tr><tr><td rowspan="2">default-device-var</td><td colspan="2">omp_set_default_device</td></tr><tr><td></td><td>omp_get_default_device</td></tr><tr><td>device-num-var</td><td>(none)</td><td>omp_get_device_num</td></tr><tr><td>display-affinity-var</td><td>(none)</td><td>(none)</td></tr><tr><td>dyn-var</td><td>omp_set_dynamic</td><td>omp_get_dynamic</td></tr><tr><td>explicit-task-var</td><td>(none)</td><td>omp_in_explicit_task</td></tr><tr><td>final-task-var</td><td>(none)</td><td>omp_in_final</td></tr><tr><td>free-agent-thread-limit-var</td><td>(none)</td><td>(none)</td></tr><tr><td>free-agent-var</td><td>(none)</td><td>omp_is_free_agent</td></tr><tr><td>league-size-var</td><td>(none)</td><td>omp_get_num_teams</td></tr><tr><td>levels-var</td><td>(none)</td><td>omp_get_level</td></tr><tr><td rowspan="2">max-active-levels-var</td><td colspan="2">omp_set_max_active_levels</td></tr><tr><td></td><td>omp_get_max_active_levels</td></tr><tr><td>max-task-priority-var</td><td>(none)</td><td>omp_get_max_task_priority</td></tr><tr><td rowspan="3">nteams-var</td><td colspan="2">omp_set_device_num_teams</td></tr><tr><td></td><td>omp_get_device_num_teams</td></tr><tr><td>omp_set_num_teams</td><td>omp_get_max_teams</td></tr><tr><td>nthreads-var</td><td>omp_set_num_threads</td><td>omp_get_max_threads</td></tr><tr><td>num-devices-var</td><td>(none)</td><td>omp_get_num_devices</td></tr><tr><td>num-procs-var</td><td>(none)</td><td>omp_get_num_procs</td></tr><tr><td>place-assignment-var</td><td>(none)</td><td>(none)</td></tr><tr><td>place-partition-var</td><td>(none)</td><td>omp_get_partition_num_places, omp_get_partition_place_nums, omp_get_place_num_procs, omp_get_place_proc_ids</td></tr><tr><td>run-sched-var</td><td>omp_set_schedule</td><td>omp_get_schedule</td></tr><tr><td>stacksize-var</td><td>(none)</td><td>(none)</td></tr><tr><td>structured-thread-limit-var</td><td>(none)</td><td>(none)</td></tr><tr><td>target-offload-var</td><td>(none)</td><td>(none)</td></tr><tr><td>team-generator-var</td><td>(none)</td><td>(none)</td></tr><tr><td>team-num-var</td><td>(none)</td><td>omp_get_team_num</td></tr><tr><td>team-size-var</td><td>(none)</td><td>omp_get_num_threads</td></tr><tr><td>teams-thread-limit-var</td><td>omp_set_device_teams_thread_limit</td><td>omp_get_device_teams_thread_limit</td></tr><tr><td></td><td>omp_set_teams_thread_limit</td><td>omp_get_teams_thread_limit</td></tr><tr><td>thread-limit-var</td><td>thread_limit</td><td>omp_get_thread_limit</td></tr><tr><td>thread-num-var</td><td>(none)</td><td>omp_get_thread_num</td></tr><tr><td>tool-libraries-var</td><td>(none)</td><td>(none)</td></tr><tr><td>tool-var</td><td>(none)</td><td>(none)</td></tr><tr><td>tool-verbose-init-var</td><td>(none)</td><td>(none)</td></tr><tr><td>wait-policy-var</td><td>(none)</td><td>(none)</td></tr></table>

## Semantics

• The value of the bind-var ICV is a list. The omp\_get\_proc\_bind routine retrieves the value of the first element of this list.

• The value of the nthreads-var ICV is a list. The omp\_set\_num\_threads routine sets the value of the first element of this list, and the omp\_get\_max\_threads routine retrieves the value of the first element of this list.

• Detailed values in the place-partition-var ICV are retrieved using the listed routines.

• The thread\_limit clause sets the thread-limit-var ICV for the region of the construct on which it appears.

## Cross References

• omp\_get\_active\_level Routine, see Section 21.17

• omp\_get\_affinity\_format Routine, see Section 29.9

• omp\_get\_cancellation Routine, see Section 30.1

• omp\_get\_default\_allocator Routine, see Section 27.10

• omp\_get\_default\_device Routine, see Section 24.2

• omp\_get\_device\_num Routine, see Section 24.4

• omp\_get\_device\_num\_teams Routine, see Section 24.11

• omp\_get\_device\_teams\_thread\_limit Routine, see Section 24.13

• omp\_get\_dynamic Routine, see Section 21.8

• omp\_get\_level Routine, see Section 21.14

• omp\_get\_max\_active\_levels Routine, see Section 21.13

• omp\_get\_max\_task\_priority Routine, see Section 23.1.1

• omp\_get\_max\_teams Routine, see Section 22.4

• omp\_get\_max\_threads Routine, see Section 21.4

• omp\_get\_num\_devices Routine, see Section 24.3

• omp\_get\_num\_procs Routine, see Section 24.5

• omp\_get\_num\_teams Routine, see Section 22.1

• omp\_get\_num\_threads Routine, see Section 21.2

• omp\_get\_partition\_num\_places Routine, see Section 29.6

• omp\_get\_partition\_place\_nums Routine, see Section 29.7

• omp\_get\_place\_num\_procs Routine, see Section 29.3

• omp\_get\_place\_proc\_ids Routine, see Section 29.4

• omp\_get\_proc\_bind Routine, see Section 29.1

• omp\_get\_schedule Routine, see Section 21.10

• omp\_get\_supported\_active\_levels Routine, see Section 21.11

• omp\_get\_team\_num Routine, see Section 22.3

• omp\_get\_teams\_thread\_limit Routine, see Section 22.5

• omp\_get\_thread\_limit Routine, see Section 21.5

• omp\_get\_thread\_num Routine, see Section 21.3

• omp\_in\_explicit\_task Routine, see Section 23.1.2

• omp\_in\_final Routine, see Section 23.1.3

• omp\_set\_affinity\_format Routine, see Section 29.8

• omp\_set\_default\_allocator Routine, see Section 27.9

• omp\_set\_default\_device Routine, see Section 24.1

• omp\_set\_device\_num\_teams Routine, see Section 24.12

• omp\_set\_device\_teams\_thread\_limit Routine, see Section 24.14

• omp\_set\_dynamic Routine, see Section 21.7

• omp\_set\_max\_active\_levels Routine, see Section 21.12

• omp\_set\_num\_teams Routine, see Section 22.2

• omp\_set\_num\_threads Routine, see Section 21.1

• omp\_set\_schedule Routine, see Section 21.9

• omp\_set\_teams\_thread\_limit Routine, see Section 22.6

• thread\_limit Clause, see Section 15.3

## 3.4 How the Per-Data Environment ICVs Work

When a task-generating construct, a parallel construct or a teams construct is encountered, each generated task inherits the values of the ICVs with data environment ICV scope from the ICV values of the generating task, unless otherwise specified.

When a parallel construct is encountered, the value of each ICV with implicit task ICV scope is inherited from the binding implicit task of the generating task unless otherwise specified.

When a task-generating construct is encountered, each generated task inherits the value of nthreads-var from the nthreads-var value of the generating task. If a parallel construct is encountered on which a num\_threads clause is specified with a nthreads list of more than one list item, the value of nthreads-var for the generated implicit tasks is the list obtained by deletion of the first item of the nthreads list. Otherwise, when a parallel construct is encountered, if the nthreads-var list of the generating task contains a single element, the generated implicit tasks inherit that list as the value of nthreads-var; if the nthreads-var list of the generating task contains multiple elements, the generated implicit tasks inherit the value of nthreads-var as the list obtained by deletion of the first element from the nthreads-var value of the generating task. The bind-var ICV is handled in the same way as the nthreads-var ICV, except that an override list cannot be specified through the proc\_bind clause of an encountered parallel construct.

When a target construct corresponds to an active target region, the resulting initial task uses the values of the data environment scoped ICVs from the device data environment ICV values of the device that will execute the region, unless otherwise specified.

When a target construct corresponds to an inactive target region, the resulting initial task uses the values of the ICVs with data environment ICV scope from the data environment of the task that encountered the target construct, unless otherwise specified.

If a target construct with a thread\_limit clause is encountered, the thread-limit-var ICV from the data environment of the resulting initial task is instead set to an implementation defined value between one and the value specified in the clause.

If a target construct with no thread\_limit clause is encountered, the thread-limit-var ICV from the data environment of the resulting initial task is set to an implementation defined value that is greater than zero.

If a teams construct with a thread\_limit clause is encountered, the thread-limit-var ICV from the data environment of the initial task for each team is instead set to an implementation defined value between one and the value specified in the clause.

If a teams construct with no thread\_limit clause is encountered and teams-thread-limit-var is greater than zero, the thread-limit-var ICV from the data environment of the initial task of each team is set to an implementation defined value that is greater than zero and does not exceed teams-thread-limit-var. If a teams construct with no thread\_limit clause is encountered and teams-thread-limit-var is zero, the thread-limit-var ICV from the data environment of the initial task of each team is set to an implementation defined value that is greater than zero.

If a target construct, teams construct, or parallel construct is encountered, the team-generator-var ICV for the data environments of the generated implicit tasks is instead set to the value of the appropriate team generator type as specified in Section 39.13.

When encountering a worksharing-loop region for which the runtime schedule type is specified, all implicit task regions that constitute the binding parallel region must have the same value for run-sched-var in their data environments. Otherwise, the behavior is unspecified.

## Cross References
