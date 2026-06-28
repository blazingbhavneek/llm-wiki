
This chapter describes routines that afect and monitor the league of teams that may execute a teams region.

## 22.1 omp\_get\_num\_teams Routine

<table><tr><td colspan="2">Name: omp_get_num_teamsCategory: function</td><td>Properties: ICV-retrieving, teams-nestable</td></tr><tr><td colspan="3">Return Type</td></tr><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td colspan="3">PrototypesC / C++int omp_get_num_teams(void);C / C++Fortraninteger function omp_get_num_teams()Fortran</td></tr></table>

## Effect

The omp\_get\_num\_teams routine returns the value of the league-size-var ICV, which is the number of initial teams in the current teams region. The routine returns 1 if it is called from outside of a teams region.

## Cross References

• league-size-var ICV, see Table 3.1

• teams Construct, see Section 12.2

## 22.2 omp\_set\_num\_teams Routine

<table><tr><td>Name: omp_set_num_teamsCategory: subroutine</td><td>Properties: ICV-modifying</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>num_teams</td><td>integer</td><td>non-negative</td></tr></table>

## Prototypes

C / C++

void omp\_set\_num\_teams(int num\_teams);

C / C++

Fortran

subroutine omp\_set\_num\_teams(num\_teams)

integer num\_teams

Fortran

## Effect

The efect of the omp\_set\_num\_teams routine is to set the value of the nteams-var ICV of the host device to the value specified in the num\_teams argument.

## Restrictions

Restrictions to the omp\_set\_num\_teams routine are as follows:

• An omp\_set\_num\_teams region must be a strictly nested region of the implicit parallel region that surrounds the whole OpenMP program.

## Cross References

• nteams-var ICV, see Table 3.1

• num\_teams Clause, see Section 12.2.1

• teams Construct, see Section 12.2

## 22.3 omp\_get\_team\_num Routine

<table><tr><td>Name: omp_get_team_numCategory: function</td><td>Properties: ICV-retrieving, teams-nestable</td></tr></table>

## Return Type

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr></table>

Prototypes

C / C++

int omp\_get\_team\_num(void);

C / C++

Fortran

integer function omp\_get\_team\_num()

Fortran

## Effect

The omp\_get\_team\_num routine returns the value of the team-num-var ICV, which is the team number of the current team and is an integer between 0 and one less than the value returned by omp\_get\_num\_teams, inclusive. The routine returns 0 if it is called outside of a teams region.

Cross References

• team-num-var ICV, see Table 3.1

• omp\_get\_num\_teams Routine, see Section 22.1

• teams Construct, see Section 12.2

## 22.4 omp\_get\_max\_teams Routine

<table><tr><td colspan="2">Name: omp_get_max_teamsCategory: function</td><td>Properties: ICV-retrieving</td></tr><tr><td colspan="3">Return Type</td></tr><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td colspan="3">PrototypesC / C++int omp_get_max_teams(void);C / C++Fortraninteger function omp_get_max_teams()Fortran</td></tr></table>

## Effect

The omp\_get\_max\_teams routine returns the value of the nteams-var ICV of the current device. If positive, this value is also an upper bound on the number of teams that can be created by a teams construct without a num\_teams clause that is encountered after execution returns from this routine.

## Cross References

• nteams-var ICV, see Table 3.1

• num\_teams Clause, see Section 12.2.1

• teams Construct, see Section 12.2

## 22.5 omp\_get\_teams\_thread\_limit Routine

<table><tr><td>Name: omp_get_teams_thread_limitCategory: function</td><td>Properties: ICV-retrieving</td></tr></table>

## Return Type

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr></table>

## Prototypes

C / C++

int omp\_get\_teams\_thread\_limit(void);

C / C++

Fortran

integer function omp\_get\_teams\_thread\_limit()

Fortran

## Effect

The omp\_get\_teams\_thread\_limit routine returns the value of the teams-thread-limit-var ICV, which is the maximum number of threads available to execute tasks in each contention group that a teams construct creates.

Cross References

• teams-thread-limit-var ICV, see Table 3.1

• teams Construct, see Section 12.2

## 22.6 omp\_set\_teams\_thread\_limit Routine

<table><tr><td>Name: omp_set_teams_thread_limitCategory: subroutine</td><td>Properties: ICV-modifying</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>thread_limit</td><td>integer</td><td>positive</td></tr></table>

## Prototypes

C / C++

void omp\_set\_teams\_thread\_limit(int thread\_limit);

C / C++

Fortran

subroutine omp\_set\_teams\_thread\_limit(thread\_limit)

integer thread\_limit

## Fortran

## Effect

The omp\_set\_teams\_thread\_limit routine sets the value of the teams-thread-limit-var ICV to the value of the thread\_limit argument and thus defines the maximum number of threads that can execute tasks in each contention group that a teams construct creates on the host device. If the value of thread\_limit exceeds the number of threads that an implementation supports for each contention group created by a teams construct, the value of the teams-thread-limit-var ICV will be set to the number that is supported by the implementation.

## Restrictions

Restrictions to the omp\_set\_teams\_thread\_limit routine are as follows:

• An omp\_set\_num\_teams region must be a strictly nested region of the implicit parallel region that surrounds the whole OpenMP program.

## Cross References

• teams-thread-limit-var ICV, see Table 3.1

• teams Construct, see Section 12.2

• thread\_limit Clause, see Section 15.3
