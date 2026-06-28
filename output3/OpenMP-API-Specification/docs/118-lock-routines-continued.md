
This chapter describes general-purpose lock routines that can be used for synchronization via mutual exclusion. These routines with the lock property operate on OpenMP locks that are represented by OpenMP lock variables. OpenMP lock variables must be accessed only through the lock routines; OpenMP programs that otherwise access OpenMP lock variables are non-conforming.

A lock can be in one of the following lock states: uninitialized; unlocked; or locked. If a lock is in the unlocked state, a task can acquire the lock by executing a lock-acquiring routine, a routine that has the lock-acquiring property, through which it changes the lock state to the locked state. The task that acquires the lock is then said to own the lock. A task that owns a lock can release it by executing a lock-releasing routine, a routine that has the lock-releasing property, through which it returns the lock state to the unlocked state. An OpenMP program in which a task executes a lock-releasing routine on a lock that is owned by another task is non-conforming.

OpenMP supports two types of locks: simple locks and nestable locks. A nestable lock can be acquired (i.e., set) multiple times by the same task before being released (i.e., unset); a simple lock cannot be acquired if it is already owned by the task trying to set it. Simple lock variables are associated with simple locks and can only be passed to simple lock routines (routines that have the simple lock property). Nestable lock variables are associated with nestable locks and can only be passed to nestable lock routines (routines that have the nestable lock property).

Each type of lock can also have a synchronization hint that contains information about the intended usage of the lock by the OpenMP program. The efect of the hint is implementation defined. An OpenMP implementation can use this hint to select a usage-specific lock, but hints do not change the mutual exclusion semantics of locks. A compliant implementation can safely ignore the hint.

Constraints on the lock state and ownership of the lock accessed by each of the lock routines are described with the routine. If these constraints are not met, the behavior of the routine is unspecified.

The lock routines access an OpenMP lock variable such that they always read and update its most current value. An OpenMP program does not need to include explicit flush directives to ensure that the value of a lock is consistent among diferent tasks.

## Restrictions

Restrictions to OpenMP lock routines are as follows:

• The use of the same lock in diferent contention groups results in unspecified behavior.

## 28.1 Lock Initializing Routines

Lock-initializing routines are routines with the lock-initializing property. These routines initialize the lock to the unlocked state; that is, no task owns the lock. In addition, the nesting count for a nestable lock is set to zero.

## Restrictions

Restrictions to lock-initializing routines are as follows:

• A lock-initializing routine must not access a lock that is not in the uninitialized state.

28.1.1 omp\_init\_lock Routine

<table><tr><td colspan="2">Name: omp_init_lockCategory: subroutine</td><td colspan="2">Properties: all-contention-group-tasks-binding, lock-initializing, simple-lock</td></tr><tr><td colspan="4">Arguments</td></tr><tr><td>Name</td><td colspan="2">Type</td><td>Properties</td></tr><tr><td>svar</td><td colspan="2">lock</td><td>C/C++ pointer, omp</td></tr><tr><td colspan="4">PrototypesC / C++void omp_init_lock(omp_lock_t *svar);C / C++Fortransubroutine omp_init_lock(svar)integer (kind=omp_lock_kind) svarFortran</td></tr></table>

## Effect

The omp\_init\_lock routine is a lock-initializing routine.

## Execution Model Events

The lock-init event occurs in a thread that executes an omp\_init\_lock region after initialization of the lock, but before it finishes the region.

## Tool Callbacks

A thread dispatches a registered lock\_init callback with omp\_sync\_hint\_none as the hint argument and ompt\_mutex\_lock as the kind argument for each occurrence of a lock-init event in that thread. This callback occurs in the task that encounters the routine.

## Cross References

• OpenMP lock Type, see Section 20.9.3

• lock\_init Callback, see Section 34.7.9

• OMPT mutex Type, see Section 33.20

## 28.1.2 omp\_init\_nest\_lock Routine

<table><tr><td>Name: omp_init_nest_lockCategory: subroutine</td><td>Properties: all-contention-group-tasks-binding, lock-initializing, nestable-lock</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>nvar</td><td>nest_lock</td><td>C/C++ pointer, omp</td></tr></table>

## Prototypes

C / C++

void omp\_init\_nest\_lock(omp\_nest\_lock\_t <sub>\*</sub>nvar);

C / C++

Fortran

subroutine omp\_init\_nest\_lock(nvar)

integer (kind=omp\_nest\_lock\_kind) nvar

Fortran

## Effect

The omp\_init\_nest\_lock routine is a lock-initializing routine.

## Execution Model Events

The nest-lock-init event occurs in a thread that executes an omp\_init\_nest\_lock region after initialization of the lock, but before it finishes the region.

## Tool Callbacks

A thread dispatches a registered lock\_init callback with omp\_sync\_hint\_none as the hint argument and ompt\_mutex\_nest\_lock as the kind argument for each occurrence of a nest-lock-init event in that thread. This callback occurs in the task that encounters the routine.

## Cross References

• lock\_init Callback, see Section 34.7.9

• OMPT mutex Type, see Section 33.20

• OpenMP nest\_lock Type, see Section 20.9.4

28.1.3 omp\_init\_lock\_with\_hint Routine

<table><tr><td>Name: omp_init_lock_with_hintCategory: subroutine</td><td>Properties: all-contention-group-tasks-binding, lock-initializing, simple-lock</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>svar</td><td>lock</td><td>C/C++ pointer, omp</td></tr><tr><td>hint</td><td>sync_hint</td><td>omp</td></tr></table>

## Prototypes

C / C++

void omp\_init\_lock\_with\_hint(omp\_lock\_t <sub>\*</sub>svar,

omp\_sync\_hint\_t hint);

C / C++

Fortran

subroutine omp\_init\_lock\_with\_hint(svar, hint)

integer (kind=omp\_lock\_kind) svar

integer (kind=omp\_sync\_hint\_kind) hint

## Fortran

## Effect

The omp\_init\_lock\_with\_hint routine is a lock-initializing routine.

## Execution Model Events

The lock-init-with-hint event occurs in a thread that executes an omp\_init\_lock\_with\_hint region after initialization of the lock, but before it finishes the region.

## Tool Callbacks

A thread dispatches a registered lock\_init callback with the same value for its hint argument as the hint argument of the call to omp\_init\_lock\_with\_hint and ompt\_mutex\_lock as the kind argument for each occurrence of a lock-init-with-hint event in that thread. This callback occurs in the task that encounters the routine.

## Cross References

• OpenMP lock Type, see Section 20.9.3

• lock\_init Callback, see Section 34.7.9

• OMPT mutex Type, see Section 33.20

• OpenMP sync\_hint Type, see Section 20.9.5

## 28.1.4 omp\_init\_nest\_lock\_with\_hint Routine

<table><tr><td>Name: omp_init_nest_lock_with_hintCategory: subroutine</td><td>Properties: all-contention-group-tasks-binding, lock-initializing, nestable-lock</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>nvar</td><td>nest_lock</td><td>C/C++ pointer, omp</td></tr><tr><td>hint</td><td>sync_hint</td><td>omp</td></tr></table>

## Prototypes

C / C++

void omp\_init\_nest\_lock\_with\_hint(omp\_nest\_lock\_t <sub>\*</sub>nvar, omp\_sync\_hint\_t hint);

C / C++

Fortran

subroutine omp\_init\_nest\_lock\_with\_hint(nvar, hint)

integer (kind=omp\_nest\_lock\_kind) nvar

integer (kind=omp\_sync\_hint\_kind) hint

## Fortran

## Effect

The omp\_init\_nest\_lock\_with\_hint routine is a lock-initializing routine.

## Execution Model Events

The nest-lock-init-with-hint event occurs in a thread that executes an omp\_init\_nest\_lock region after initialization of the lock, but before it finishes the region.

## Tool Callbacks

A thread dispatches a registered lock\_init callback with the same value for its hint argument as the hint argument of the call to omp\_init\_nest\_lock\_with\_hint and

ompt\_mutex\_nest\_lock as the kind argument for each occurrence of a nest-lock-init-with-hint event in that thread This callback occurs in the task that encounters the routine.

## Cross References

• lock\_init Callback, see Section 34.7.9

• OMPT mutex Type, see Section 33.20

• OpenMP nest\_lock Type, see Section 20.9.4

• OpenMP sync\_hint Type, see Section 20.9.5

## 28.2 Lock Destroying Routines

Lock-destroying routines are routines with the lock-destroying property. These routines deactivate the lock by setting it to the uninitialized state.

## Restrictions

Restrictions to lock-destroying routines are as follows:

• A lock-destroying routine must not access a lock that is not in the unlocked state.

## 28.2.1 omp\_destroy\_lock Routine

<table><tr><td>Name: omp_destroy_lockCategory: subroutine</td><td>Properties: all-contention-group-tasks-binding, lock-destroying, simple-lock</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>svar</td><td>lock</td><td>C/C++ pointer, omp</td></tr></table>

## Prototypes

subroutine omp\_destroy\_lock(svar)

## Effect

The omp\_destroy\_lock routine is a lock-destroying routine.

## Execution Model Events

The lock-destroy event occurs in a thread that executes an omp\_destroy\_lock region before it finishes the region.

## Tool Callbacks

A thread dispatches a registered lock\_destroy callback with ompt\_mutex\_lock as the kind argument for each occurrence of a lock-destroy event in that thread. This callback occurs in the task that encounters the routine.

## Cross References

• OpenMP lock Type, see Section 20.9.3

• lock\_destroy Callback, see Section 34.7.11

• OMPT mutex Type, see Section 33.20

## 28.2.2 omp\_destroy\_nest\_lock Routine

<table><tr><td>Name: omp_destroy_nest_lockCategory: subroutine</td><td>Properties: all-contention-group-tasks-binding, lock-destroying, nestable-lock</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>nvar</td><td>nest_lock</td><td>C/C++ pointer, omp</td></tr></table>

## Prototypes

C / C++

void omp\_destroy\_nest\_lock(omp\_nest\_lock\_t <sub>\*</sub>nvar);

C / C++

Fortran

subroutine omp\_destroy\_nest\_lock(nvar)

integer (kind=omp\_nest\_lock\_kind) nvar

Fortran

## Effect

The omp\_destroy\_nest\_lock routine is a lock-destroying routine.

## Execution Model Events

The nest-lock-destroy event occurs in a thread that executes an omp\_destroy\_nest\_lock region before it finishes the region.

## Tool Callbacks

A thread dispatches a registered lock\_destroy callback with ompt\_mutex\_nest\_lock as the kind argument for each occurrence of a nest-lock-destroy event in that thread. This occurs in the task that encounters the routine.

## Cross References

• lock\_destroy Callback, see Section 34.7.11

• OMPT mutex Type, see Section 33.20

• OpenMP nest\_lock Type, see Section 20.9.4

## 28.3 Lock Acquiring Routines

Lock-acquiring routines are routines with the lock-acquiring property. These routines provide a means of setting locks. The encountering task region behaves as if it was suspended until the lock can be acquired by this task.

##

Note – The semantics of lock-acquiring routine are specified as if they serialize execution of the region guarded by the lock. However, implementations may implement them in other ways provided that the isolation properties are respected so that the actual execution delivers a result that could arise from some serialization.

## Restrictions

Restrictions to lock-acquiring routines are as follows:

• A lock-acquiring routine must not access a lock that is in the uninitialized state.

## 28.3.1 omp\_set\_lock Routine

<table><tr><td>Name: omp_set_lockCategory: subroutine</td><td>Properties: all-contention-group-tasks-binding, lock-acquiring, simple-lock</td></tr></table>

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>svar</td><td>lock</td><td>C/C++ pointer, omp</td></tr></table>

C / C++

void omp\_set\_lock(omp\_lock\_t <sub>\*</sub>svar);

C / C++

Fortran

subroutine omp\_set\_lock(svar)

integer (kind=omp\_lock\_kind) svar

Fortran

## Effect

A simple lock is available when it is in the unlocked state. Ownership of the lock is granted to the task that executes the routine.

## Execution Model Events

The lock-acquire event occurs in a thread that executes an omp\_set\_lock region before the associated lock is requested. The lock-acquired event occurs in a thread that executes an omp\_set\_lock region after it acquires the associated lock but before it finishes the region.

## Tool Callbacks

A thread dispatches a registered mutex\_acquire callback for each occurrence of a lock-acquire event in that thread. A thread dispatches a registered mutex\_acquired callback for each occurrence of a lock-acquired event in that thread. These callbacks occur in the task that encounters the omp\_set\_lock routine and their kind argument is ompt\_mutex\_lock.

## Restrictions

Restrictions to the omp\_set\_lock routine are as follows:

• A task must not already own the lock that it accesses with a call to omp\_set\_lock (or deadlock will result).

## Cross References

• OpenMP lock Type, see Section 20.9.3

• OMPT mutex Type, see Section 33.20

• mutex\_acquire Callback, see Section 34.7.8

• mutex\_acquired Callback, see Section 34.7.12

## 28.3.2 omp\_set\_nest\_lock Routine

<table><tr><td>Name: omp_set_nest_lockCategory: subroutine</td><td>Properties: all-contention-group-tasks-binding, lock-acquiring, nestable-lock</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>nvar</td><td>nest_lock</td><td>C/C++ pointer, omp</td></tr></table>

## Prototypes

C / C++

void omp\_set\_nest\_lock(omp\_nest\_lock\_t <sub>\*</sub>nvar);

C / C++

Fortran

subroutine omp\_set\_nest\_lock(nvar)

integer (kind=omp\_nest\_lock\_kind) nvar

Fortran

## Effect

A nestable lock is available if it is in the unlocked state or if it is already owned by the task that executes the routine. The task that executes the routine is granted, or retains, ownership of the lock, and the nesting count for the lock is incremented.

## Execution Model Events

The nest-lock-acquire event occurs in a thread that executes an omp\_set\_nest\_lock region before the associated lock is requested. The nest-lock-acquired event occurs in a thread that executes an omp\_set\_nest\_lock region if the task did not already own the lock, after it acquires the associated lock but before it finishes the region. The nest-lock-owned event occurs in a task when it already owns the lock and executes an omp\_set\_nest\_lock region. The nest-lock-owned event occurs after the nesting count is incremented but before the task finishes the region.

## Tool Callbacks

A thread dispatches a registered mutex\_acquire callback for each occurrence of a nest-lock-acquire event in that thread. A thread dispatches a registered mutex\_acquired callback for each occurrence of a nest-lock-acquired event in that thread. A thread dispatches a registered nest\_lock callback with ompt\_scope\_begin as its endpoint argument for each occurrence of a nest-lock-owned event in that thread. These callbacks occur in the task that encounters the omp\_set\_nest\_lock routine and their kind argument is ompt\_mutex\_nest\_lock.

## Cross References

• OMPT mutex Type, see Section 33.20

• mutex\_acquire Callback, see Section 34.7.8

• mutex\_acquired Callback, see Section 34.7.12

• nest\_lock Callback, see Section 34.7.14

• OpenMP nest\_lock Type, see Section 20.9.4

• OMPT scope\_endpoint Type, see Section 33.27

## 28.4 Lock Releasing Routines

Lock-releasing routines are routines with the lock-releasing property. These routines provide a means of unsetting locks. If the efect of a lock-releasing routine changes the lock state to the unlocked state and one or more task regions were efectively suspended because the lock was unavailable, the efect is that one task is chosen and given ownership of the lock.

## Restrictions

Restrictions to lock-releasing routines are as follows:

• A lock-releasing routine must not access a lock that is not in the locked state.

• A lock-releasing routine must not access a lock that is owned by a task other than the encountering task

## 28.4.1 omp\_unset\_lock Routine

<table><tr><td colspan="2">Name: omp_unset_lockCategory: subroutine</td><td colspan="2">Properties: all-contention-group-tasks-binding, lock-releasing, simple-lock</td></tr><tr><td colspan="4">Arguments</td></tr><tr><td>Name</td><td colspan="2">Type</td><td>Properties</td></tr><tr><td>svar</td><td colspan="2">lock</td><td>C/C++ pointer, omp</td></tr><tr><td colspan="4">PrototypesC / C++void omp_unset_lock(omp_lock_t *svar);C / C++Fortransubroutine omp_unset_lock(svar)integer (kind=omp_lock_kind) svarFortran</td></tr></table>

## Effect

The omp\_unset\_lock routine changes the lock state to the unlocked state.

## Execution Model Events

The lock-release event occurs in a thread that executes an omp\_unset\_lock region after it releases the associated lock but before it finishes the region.

## Tool Callbacks

A thread dispatches a registered mutex\_released callback with ompt\_mutex\_lock as the kind argument for each occurrence of a lock-release event in that thread. This callback occurs in the encountering task.

## Cross References

• OpenMP lock Type, see Section 20.9.3

• OMPT mutex Type, see Section 33.20

• mutex\_released Callback, see Section 34.7.13

## 28.4.2 omp\_unset\_nest\_lock Routine

<table><tr><td>Name: omp_unset_nest_lockCategory: subroutine</td><td>Properties: all-contention-group-tasks-binding, lock-releasing, nestable-lock</td></tr></table>

## Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td>nvar</td><td>nest_lock</td><td>C/C++ pointer, omp</td></tr></table>

## Prototypes

C / C++

void omp\_unset\_nest\_lock(omp\_nest\_lock\_t <sub>\*</sub>nvar);

C / C++

Fortran

subroutine omp\_unset\_nest\_lock(nvar)

integer (kind=omp\_nest\_lock\_kind) nvar

Fortran

## Effect

The omp\_unset\_nest\_lock routine decrements the nesting count and, if the resulting nesting count is zero, changes the lock state to the unlocked state.

## Execution Model Events

The nest-lock-release event occurs in a thread that executes an omp\_unset\_nest\_lock region after it releases the associated lock but before it finishes the region. The nest-lock-held event occurs in a thread that executes an omp\_unset\_nest\_lock region before it finishes the region when the thread still owns the lock after the nesting count is decremented.

## Tool Callbacks

A thread dispatches a registered mutex\_released callback with ompt\_mutex\_nest\_lock as the kind argument for each occurrence of a nest-lock-release event in that thread. A thread dispatches a registered nest\_lock callback with ompt\_scope\_end as its endpoint argument for each occurrence of a nest-lock-held event in that thread. These callbacks occur in the encountering task.

## Cross References

• OMPT mutex Type, see Section 33.20

• mutex\_released Callback, see Section 34.7.13

• nest\_lock Callback, see Section 34.7.14

• OpenMP nest\_lock Type, see Section 20.9.4

• OMPT scope\_endpoint Type, see Section 33.27

## 28.5 Lock Testing Routines

Lock-testing routines are routines with the lock-testing property. These routines attempt to acquire a lock in the same manner as lock-acquiring routines, except that they do not suspend execution of the encountering task

## Restrictions

Restrictions on lock-testing routines are as follows.

• A lock-testing routine must not access a lock that is in the uninitialized state.

28.5.1 omp\_test\_lock Routine

<table><tr><td>Name: omp_test_lockCategory: function</td><td>Properties: all-contention-group-tasks-binding, lock-testing, simple-lock</td></tr></table>

Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>logical</td><td>default</td></tr><tr><td>svar</td><td>lock</td><td>C/C++ pointer, omp</td></tr></table>

## Prototypes

C / C++

int omp\_test\_lock(omp\_lock\_t <sub>\*</sub>svar);

C / C++

Fortran

logical function omp\_test\_lock(svar) integer (kind=omp\_lock\_kind) svar

Fortran

## Effect

The omp\_test\_lock routine returns true if it successfully acquires the lock; otherwise, it returns false.

## Execution Model Events

The lock-test event occurs in a thread that executes an omp\_test\_lock region before the associated lock is tested. The lock-test-acquired event occurs in a thread that executes an omp\_test\_lock region before it finishes the region if the associated lock was acquired.

## Tool Callbacks

A thread dispatches a registered mutex\_acquire callback for each occurrence of a lock-test event in that thread. A thread dispatches a registered mutex\_acquired callback for each occurrence of a lock-test-acquired event in that thread. These callbacks occur in the encountering task and their kind argument is ompt\_mutex\_test\_lock.

## Restrictions

Restrictions to omp\_test\_lock routines are as follows:

• An omp\_test\_lock routine must not access a lock that is already owned by the encountering task.

## Cross References

• OpenMP lock Type, see Section 20.9.3

• OMPT mutex Type, see Section 33.20

• mutex\_acquire Callback, see Section 34.7.8

• mutex\_acquired Callback, see Section 34.7.12

## 28.5.2 omp\_test\_nest\_lock Routine

<table><tr><td>Name: omp_test_nest_lockCategory: function</td><td>Properties: all-contention-group-tasks-binding, lock-testing, nestable-lock</td></tr></table>

## Return Type and Arguments

<table><tr><td>Name</td><td>Type</td><td>Properties</td></tr><tr><td></td><td>integer</td><td>default</td></tr><tr><td>nvar</td><td>nest_lock</td><td>C/C++ pointer, omp</td></tr></table>

## Prototypes

C / C++

int omp\_test\_nest\_lock(omp\_nest\_lock\_t <sub>\*</sub>nvar);

C / C++

Fortran

integer function omp\_test\_nest\_lock(nvar)

integer (kind=omp\_nest\_lock\_kind) nvar

Fortran

## Effect

The omp\_test\_nest\_lock routine returns the new nesting count if it successfully sets the lock; otherwise, it returns zero.

## Execution Model Events

The nest-lock-test event occurs in a thread that executes an omp\_test\_nest\_lock region before the associated lock is tested. The nest-lock-test-acquired event occurs in a thread that executes an omp\_test\_nest\_lock region before it finishes the region if the associated lock was acquired and the thread did not already own the lock. The nest-lock-owned event occurs in a thread that executes an omp\_test\_nest\_lock region before it finishes the region after the nesting count is incremented if the thread already owned the lock.

## Tool Callbacks

A thread dispatches a registered mutex\_acquire callback for each occurrence of a nest-lock-test event in that thread. A thread dispatches a registered mutex\_acquired callback for each occurrence of a nest-lock-test-acquired event in that thread. A thread dispatches a registered nest\_lock callback with ompt\_scope\_begin as its endpoint argument for each occurrence of a nest-lock-owned event in that thread. These callbacks occur in the encountering task and their kind argument is ompt\_mutex\_test\_nest\_lock.

## Cross References

• OMPT mutex Type, see Section 33.20

• mutex\_acquire Callback, see Section 34.7.8

• mutex\_acquired Callback, see Section 34.7.12

• nest\_lock Callback, see Section 34.7.14

• OpenMP nest\_lock Type, see Section 20.9.4

• OMPT scope\_endpoint Type, see Section 33.27

# 29 Thread Affinity Routines
