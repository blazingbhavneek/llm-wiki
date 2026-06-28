## worksharing-loop construct

A construct that has the worksharing-loop property. 414, 47, 48, 114, 134, 254, 259, 414–419, 514–516, 521, 523, 526, 753, 890, 899, 905, 910, 912, 916, 918

## worksharing-loop property

The property of a worksharing construct that it is a loop-nest-associated construct that distributes the collapsed iterations of the afected loops among the threads in the team. 113,

## 416, 417, 529

## worksharing-loop region

A region that corresponds to a worksharing-loop construct. 414, 117, 125, 414, 514, 516, 918

## worksharing property

The property of a construct that it is a work-distribution construct that is executed by the team of the innermost enclosing parallel region and includes, by default, an implicit barrier. 113, 405–407, 409, 416, 417, 423

## worksharing region

A region that corresponds to a worksharing construct. 404, 4, 228, 229, 252, 404, 476, 501, 753, 907, 917

## write-capture structured block

An atomic structured block that may be associated with an atomic directive that expresses an atomic write operation with capture semantics. 192, 193

## write structured block

An atomic structured block that may be associated with an atomic directive that expresses an atomic write operation. 190, 190, 192, 497

## Z

## zeroed-memory-allocating routine

A memory-allocating routine that has the zeroed-memory-allocating-routine property. 654, 654, 658, 659

## zeroed-memory-allocating-routine property

The property that a memory-allocating routine returns a pointer to memory that has been set to zero. 654, 114, 658, 659

## zero-length array section

An array section that does not include any elements of the array. 167, 247, 280, 509

## zero-offset assumed-size array

An assumed-size array for which the lower bound is zero. 236, 277, 282

## 3 Internal Control Variables

An OpenMP implementation must act as if internal control variables (ICVs) control the behavior of an OpenMP program. These ICVs store information such as the number of threads to use for future parallel regions. One copy exists of each ICV per instance of its ICV scope. Possible ICV scopes are: global; device; implicit task; and data environment. If an ICV scope is global then one copy of the ICV exists for the whole OpenMP program. If an ICV scope is device then a distinct copy of the ICV exists for each device. If an ICV scope is implicit task then a distinct copy of the ICV exists for each implicit task. If an ICV scope is data environment then a distinct copy of the ICV exists for the data environment of each task, unless otherwise specified. The ICVs are given values at various times (described below) during the execution of the program. They are initialized by the implementation itself and may be given values through OpenMP environment variables and through calls to OpenMP API routines. The program can retrieve the values of these ICVs only through routines.

For purposes of exposition, this document refers to the ICVs by certain names, but an implementation is not required to use these names or to ofer any way to access the variables other than through the ways shown in Section 3.2.
