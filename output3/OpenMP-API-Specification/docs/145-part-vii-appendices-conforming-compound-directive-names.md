
• If the simd parallelization-level clause is specified on an ordered construct, the ordered region must bind to a simd region or one that corresponds to a compound construct for which the simd construct is a leaf construct (see Section 17.10.2).

• If the threads parallelization-level clause is specified on an ordered construct, the ordered region must bind to a worksharing-loop region or one that corresponds to a compound construct for which a worksharing-loop construct is a leaf construct (see Section 17.10.2).

• If the threads parallelization-level clause is specified on an ordered construct and the binding region corresponds to a compound construct then the simd construct must not be a leaf construct unless the simd parallelization-level clause is also specified (see Section 17.10.2).

• If cancel-directive-name is taskgroup, the cancel construct must be closely nested inside a task construct and the cancel region must be closely nested inside a taskgroup region. Otherwise, the cancel construct must be closely nested inside a construct for which directive-name is cancel-directive-name (see Section 18.2).

• A cancellation point construct for which cancel-directive-name is taskgroup must be closely nested inside a task construct, and the cancellation point region must be closely nested inside a taskgroup region. Otherwise, a cancellation point construct must be closely nested inside a construct for which directive-name is cancel-directive-name (see Section 18.3).

# D Conforming Compound Directive Names

This appendix provides the grammar from which one may derive the full list of conforming compound-directive names (see Section 19.1) after excluding any productions for compound-directive name that would violate the following constraints:

• Leaf-directive names must be unique.

• The nesting of constructs indicated by the compound construct must be conforming.

• For Fortran, where spaces are optional, the resulting compound-directive name must have unambiguous leaf-directive names (e.g., plus signs should be used to separate leaf-directive names to disambiguate taskloop and task loop as constituent-directive names).

compound-dir-name: composite-loop-dir-name parallelism-generating-combined-dir-name thread-selecting-combined-dir-name

composite-loop-dir-name: distribute-composite-dir-name taskloop-composite-dir-name worksharing-loop-composite-dir-name

parallelism-generating-combined-dir-name: parallel-combined-dir-name target-combined-dir-name target\_data-combined-dir-name task-combined-dir-name teams-combined-dir-name

thread-selecting-combined-dir-name: masked-combined-dir-name single-combined-dir-name

distribute-composite-dir-name: distribute parallel-worksharing-loop-dir-name distribute simd-dir-name

taskloop-composite-dir-name: taskloop simd-dir-name

worksharing-loop-composite-dir-name: for simd-dir-name do simd-dir-name

parallel-combined-dir-name: parallel partitioned-worksharing-dir-name parallel simd-dir-name parallel target-task-generating-dir-name parallel task-dir-name parallel taskloop-dir-name parallel thread-selecting-dir-name

target-combined-dir-name: target loop-dir-name target parallel-dir-name target simd-dir-name target task-dir-name target taskloop-dir-name target teams-dir-name

target\_data-combined-dir-name: target\_data loop-dir-name target\_data parallel-dir-name target\_data simd-dir-name

task-combined-dir-name: task loop-dir-name task parallel-dir-name task simd-dir-name

teams-combined-dir-name: teams parallel-dir-name teams partitioned-nonworksharing-workdist-dir-name teams simd-dir-name teams target-task-generating-dir-name teams task-dir-name teams taskloop-dir-name

masked-combined-dir-name: masked loop-dir-name

```txt
masked parallel-dir-name
masked simd-dir-name
masked target-task-generating-dir-name
masked task-dir-name
masked taskloop-dir-name

single-combined-dir-name:
    single loop-dir-name
    single parallel-dir-name
    single simd-dir-name
    single target-task-generating-dir-name
    single task-dir-name
    single taskloop-dir-name

parallel-worksharing-loop-dir-name:
    parallel worksharing-loop-dir-name

simd-dir-name:
    simd

partitioned-worksharing-dir-name:
    loop-dir-name
    single-dir-name
    worksharing-loop-dir-name
    sections
    workshare

target-task-generating-dir-name:
    target_data-dir-name
    target-dir-name
    target_enter_data
    target_exit_data
    target_update

task-dir-name:
    task-combined-dir-name
    task

taskloop-dir-name:
    taskloop-composite-dir-name
    taskloop

thread-selecting-dir-name:
```

```txt
masked-dir-name
    single-dir-name

loop-dir-name:
    loop

parallel-dir-name:
    parallel-combined-dir-name
    parallel

teams-dir-name:
    teams-combined-dir-name
    teams

partitioned-nonworksharing-workdist-dir-name:
    distribute-dir-name
    loop-dir-name
    workdistribute

worksharing-loop-dir-name:
    worksharing-loop-composite-dir-name
    for
    do

single-dir-name:
    single-combined-dir-name
    single

target_data-dir-name:
    target_data-combined-dir-name
    target_data

target-dir-name:
    target-combined-dir-name
    target

masked-dir-name:
    masked-combined-dir-name
    masked

distribute-dir-name:
    distribute-composite-dir-name
    distribute
```
