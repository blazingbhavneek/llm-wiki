## pure property

The property that a directive has no observable side efects or state, yielding the same result every time it is encountered. 149, 215, 260, 263, 266, 293, 301, 310, 325, 327, 334, 341, 346, 352, 368, 369, 374, 375, 377, 379–381, 399, 897, 904

## R

## raw-memory-allocating routine

A memory-allocating routine that has the raw-memory-allocating-routine property. 654, 654–657

## raw-memory-allocating-routine property

The property that a memory-allocating routine returns a pointer to uninitialized memory. 654, 89, 656, 657

## read-modify-write

An atomic operation that reads and writes to a given storage location. COMMENT: Any atomic update is a read-modify-write operation.

11, 89

## read structured block

An atomic structured block that may be associated with an atomic directive that expresses an atomic read operation. 189, 190, 192, 497

## rectangular-memory-copying property

The property of a memory-copying routine that the memory that it copies forms a rectangular subvolume. 612, 89, 614, 617

## rectangular-memory-copying routine

A routine with the rectangular-memory-copying property. 612, 612, 615, 618, 735, 779, 893 reduction A use of a reduction operation. 33, 90, 104, 183, 239–242, 244, 245, 249–251, 253, 256, 430, 898, 904, 907, 909, 912, 914

## reduction attribute

For a given construct, a data-sharing attribute of a data entity that implies the private attribute and for which a partial result is computed in the context of a reduction computation. 249, 90

## reduction clause

A reduction-scoping clause or a reduction-participating clause. 239, 61, 219, 222, 239–241, 247–251, 253, 256, 257, 260, 261

## reduction expression

A combiner expression or an initializer expression. 240, 240

## reduction identifier

An OpenMP identifier that specifies a combiner OpenMP operation to use in a reduction. 239, 183, 239, 240, 244, 245, 247–249, 251, 260, 261, 430, 899

## reduction operation

An operation that applies a combiner and an associated initializer to a set of values. 32, 89, 94, 111, 239

## reduction-participating clause

A clause that defines the participants in a reduction. 239, 90, 239, 251, 252, 256

## reduction-participating property

The property that a clause is a reduction-participating clause. 252, 256

## reduction-scoping clause

A clause that defines the region in which a reduction is computed. 239, 90, 239, 250–253, 256, 257, 430

## reduction-scoping property

The property that a clause is a reduction-scoping clause. 252, 255

## reduction variable

A private variable that has the reduction attribute with respect to a given construct. 249, 249

## referenced pointee

For a given referencing variable, the referenced data object to which the referring pointer points. 26, 27, 91, 237, 238, 279, 282, 283, 296

## referencing variable

For C++, a data entity that is a reference. For Fortran, a data entity that is an allocatable variable or a data pointer. 25, 27, 90, 91, 112, 210, 212, 237, 238, 279, 282, 283, 289, 296

## referring pointer

If a given referencing variable is a Fortran data pointer, the pointer object that is pointer associated with the referenced pointee; otherwise, an associated implementation defined handle through which the referenced pointee is made accessible. 25, 37, 38, 90, 210, 212, 238, 279, 282–284, 289, 461

## region

All code encountered during a specific instance of the execution of a given construct, structured block sequence or routine. A region includes any code in called procedures as well as any implementation code. The generation of a task at the point where a task-generating construct is encountered is a part of the region of the encountering thread. However, an explicit task region that corresponds to a task-generating construct is not part of the region of the encountering thread unless it is an included task region. The point where a target or teams directive is encountered is a part of the region of the encountering thread, but the region that corresponds to the target or teams directive is not.

A region may also be thought of as the dynamic or runtime extent of a construct or of a routine. During the execution of an OpenMP program, a construct may give rise to many regions. 3–8, 12, 13, 19, 21, 22, 26, 28, 30, 31, 38, 39, 42, 45, 47–51, 54, 55, 58, 59, 61, 69, 71, 76, 79, 81–84, 87, 90–93, 95–97, 99, 101–107, 109, 113–117, 122, 124, 128–130, 133, 136, 149, 155, 193, 194, 198, 205, 210, 214, 216, 217, 220, 221, 228, 231, 237, 239, 240, 248, 250–254, 256, 257, 271, 281, 283, 284, 286, 288, 296, 306–308, 311, 313, 316, 328, 338, 340, 345, 358, 359, 366, 369, 384, 385, 388, 389, 391, 394–396, 398–400, 402–410, 412, 413, 420, 421, 423–427, 429, 430, 433, 435–437, 439, 445–451, 454, 456, 458, 459, 461–466, 468, 472–480, 494–505, 513–516, 519–525, 535, 564, 568, 569, 571, 576, 577, 580–583, 585, 588, 590, 592–594, 596–603, 618, 630, 645, 646, 652, 653, 655, 664–676, 678, 683, 685–687, 689, 690, 693–695, 703, 704, 706, 715, 719, 725, 733, 734, 736, 742, 744, 749–751, 753, 758, 763–768, 778, 781, 785, 788, 795, 796, 800, 850, 859, 878–881, 883, 885, 887–889, 891, 893, 894, 898, 900–903, 906, 910, 912, 913, 915–918

## region endpoint

An event that indicates the beginning or end of a region that may be of interest to a tool. 703, 704, 729

## region-invariant property

The property that an expression, including one that is used as the argument of a clause, a modifier or a routine, has a value that is invariant for the associated region. 161, 160, 232, 258, 300, 384, 394, 418, 422

## registered callback

A callback for which callback registration has been performed. 14, 29, 78, 701, 703, 894

## release flush

A flush that has the release flush property. 10, 11, 12, 92, 101, 496, 499, 501–504

## release flush property

A flush with the release flush property orders memory operations that precede the flush before memory operations performed by a diferent thread with which it synchronizes. 52, 92, 499

## release sequence

A set of modifying atomic operations that are associated with a release flush that may establish a synchronizes-with relation between the release flush and an acquire flush. 11, 12, 502

## repeatable property

The property that a clause or modifier may appear more than once in a given context with which it is associated. 159, 180

## replacement candidate

A directive variant or function variant that may be selected to replace a metadirective or base function. 324, 30, 48, 324, 325, 328, 329, 331, 335, 889

## replayable construct

A task-generating construct that an implementation must record into a taskgraph record, if one is recorded. 435, 92, 94, 103, 215, 435–437, 441

## replay execution

An execution of a given taskgraph region that entails executing replayable constructs that are saved in a matching taskgraph record. 436, 52, 94, 103, 215, 435–437, 891, 898

## reproducible schedule

A loop schedule for the afected loop nest of a given loop-nest-associated construct that does not change between diferent executions of the construct that have the same binding thread set and have the same number of logical iterations. 404, 205, 398, 414, 420, 423, 905

## required property

The property that a clause, a modifier, an argument, or at least one member of a clause set is required and, thus, may not be omitted. 160, 157, 159–161, 181, 251, 252, 255, 256, 258, 262, 265, 266, 325, 330, 331, 356, 363, 374, 378, 458, 465, 468, 505, 511, 512, 519, 535

## reservation type

A thread-reservation type. 142

## reserved locator

An OpenMP identifier that represents system storage that is not necessarily bound to any base language storage item. 164, 163, 164, 506, 508, 509, 906

## reserved thread

A thread in an OpenMP thread pool that must have a particular thread-reservation type when executing a task. 141

## resource-relinquishing property

The property that a routine relinquishes some (or all) resources that the OpenMP program is currently using. 688, 93, 689, 690

## resource-relinquishing routine

A routine that has the resource-relinquishing property. 688, 56, 98, 563, 564, 688, 689

## reverse-offload region

A region that is associated with a target construct that specifies a device clause with the ancestor device-modifier. 345, 911

## routine

Unless specifically stated otherwise, an OpenMP API routine. xxvii, 2, 3, 6, 7, 14, 15, 17, 21, 22, 24, 28, 30, 35, 44, 49, 52, 53, 55, 57, 58, 61–63, 65, 66, 71–73, 75–79, 81, 83, 85, 86, 88, 89, 91, 93, 97, 105, 110, 112, 115, 120–122, 129, 139, 147, 216, 306, 398, 462, 463, 533–535, 537, 555, 556, 561, 563–565, 567–590, 592–612, 614–616, 618, 620–626, 628–676, 678–694, 698, 701, 744, 745, 754, 760, 769, 787, 798, 817, 826, 833, 845–867, 870–872, 874–877, 892–894, 901–903, 907–911, 913, 915–917

## runtime entry point

A function interface provided by an OpenMP runtime for use by a tool. A runtime entry point is typically not associated with a global function symbol. 701, 24, 49, 78, 93, 697, 704, 705, 745, 786

## runtime error termination

An error termination that is performed during execution. 6, 50, 149, 283, 285, 296, 389, 450, 451, 600, 602, 603, 689, 887

## S

## safesync-compatible expression

An expression that is omp\_curr\_progress\_width, a constant expression, or an expression for which all operands are safesync-compatible expressions. 93, 393

## saved data environment

For a given replayable construct that is recorded in a taskgraph record, an associated enclosing data environment that is also saved in the record for possible use in a replay execution of the construct. 436, 103, 215, 435, 437

## scalar variable

For C/C++, a scalar-variable, as defined by the base language. For Fortran, a scalar variable with enum, enumeration, assumed, or intrinsic type, excluding character type, as defined by the base language. 185, 189, 195, 200, 211, 214, 223, 231, 277, 292, 778, 888, 912

## scan computation

A computation performed in the logical iterations of a loop nest that yields a set of values that are a running total, as defined by a reduction operation, over an input set of values. 267, 50, 59–61, 94, 111, 253, 254, 267

## scan phase

The portion of an afected iteration that includes all statements that read the result of a scan computation. 267, 60, 267–270

## schedulable task

A member of the schedulable task set of a thread. 448, 449

## schedulable task set

If the thread is a structured thread, the set of tasks bound to the current team. If the thread is an unassigned thread, any explicit task in the contention group associated with the current OpenMP thread pool. 94, 447, 448

## schedule specification

The specification of a loop schedule for a given loop-nest-associated construct, which includes but is not limited to the schedule type and chunk size. 404, 94, 205, 404

## schedule-specification clause

A clause that has the schedule-specification property. 404

## schedule-specification property

The property of a clause that it defines, in part or in full, the schedule specification of a given loop-nest-associated construct. 94, 397, 418, 422

## schedule type

The part of a schedule specification that identifies the method by which the collapsed iterations are distributed to threads. 94, 117, 125, 134, 415, 419, 537, 573, 574, 892

## scope handle

A handle that refers to an OpenMP scope. 827, 875–877

## segment

A portion of an address space associated with a set of address ranges. 20, 826

## selector set

Unless specifically stated otherwise, a trait selector set. 36, 45, 58, 102, 111, 322

## self map

A mapping operation for which the corresponding storage is the same as its original storage. 284, 84, 283, 285, 361, 900

## semantic requirement set

A logical set of semantic properties maintained by a task that is updated by directives in the scope of the task region. 328, 332, 334, 338, 339, 482

## separated construct

A construct for which its associated structured block is split into multiple structured block sequences by a separating directive. 154, 95, 154, 155, 267, 268

## separating directive

A directive that splits a structured block that is associated with a construct, the separated construct, into multiple structured block sequences. 154, 95, 152, 154, 155, 266, 268, 408

## sequentially consistent atomic operation

An atomic operation that is specified by an atomic construct for which the seq\_cst clause is specified. 13, 914

## sequential part

All code encountered during the execution of an initial task region that is not part of a parallel region that corresponds to a parallel construct or a task region corresponding to a task construct. Instead, it is enclosed by an implicit parallel region.

COMMENT: Executable statements in called procedures may be in both a sequential part and any number of explicit parallel regions at diferent points in the program execution.

95, 216, 683, 685

## shape-operator

For C/C++, an array shaping operator that reinterprets a pointer expression as an array with one or more specified dimensions. 165, 165, 295, 444, 509, 909

## shared attribute

For a given construct, a data-sharing attribute of a data entity that its lifetime is not limited to that of the corresponding region and, if the data entity is a variable, it is visible to all tasks generated by the construct in addition to being visible in the enclosing context of the construct if declared outside the construct. 225, 8, 96, 210–214, 225, 252–254, 259, 427, 430, 454, 456, 461, 466, 888

## shared variable

A variable that has the shared attribute with respect to a given construct. 7, 7, 10–12, 14, 488–491

## sharing task

A task for which the implicitly determined data-sharing attribute is shared unless explicitly specified otherwise. 213, 96, 458

## sharing-task property

The property that a task-generating construct generates sharing tasks. 458

## sibling task

Two tasks are each a sibling task of the other if they are child tasks of the same task region. 96, 507, 508

## signal

A software interrupt delivered to a thread. 24, 96, 817

## signal handler

A function called asynchronously when a signal is delivered to a thread. 7, 24, 720, 786, 817 SIMD

Single Instruction, Multiple Data, a lock-step parallelization paradigm. 233, 318, 341, 342, 402, 888, 889, 914

## SIMD chunk

A set of iterations executed concurrently, each by a SIMD lane, by a single thread by means of SIMD instructions. 399, 97, 342, 399, 401, 912

## SIMD construct

A simd construct or a compound construct for which the simd construct is a constituent construct. 419

## SIMD instruction

A single machine instruction that can operate on multiple data elements. 3, 83, 96, 97, 300, 399

## SIMDizable construct

A construct that has the SIMDizable property. 399, 917

## SIMDizable property

The property that a construct may be encountered during execution of a simd region. 97, 374, 375, 377, 379–381, 399, 423, 494, 515, 516

## SIMD lane

A software or hardware mechanism capable of processing one data element from a SIMD instruction. 5, 7, 87, 96, 219–221, 226, 233, 234, 250–253, 258, 399

## SIMD loop

A loop that includes at least one SIMD chunk. 299, 341, 342

## SIMD-partitionable construct

A construct that has the SIMD-partitionable property. 526

## SIMD-partitionable property

The property of a loop-nest-associated construct that it partitions the set of afected iterations such that each partition can be divided into SIMD chunks. 97, 416, 417, 420, 429

## simple lock

A lock that cannot be set if it is already owned by the task trying to set it. 663, 97, 559, 663, 670

## simple lock property

The property that a routine operates on simple locks. 663, 97, 664, 666, 668, 670, 673, 675 simple lock routine

A routine that has the simple lock property. 663, 559

## simple modifier

A modifier that can never take an argument when it is specified. 158, 158, 160, 161

## simply contiguous array section

An array section that can be determined to have contiguous storage at compile time. In Fortran, this determination may result from the specification of the CONTIGUOUS attribute on the declaration of the array. 214, 888

## simply happens before

For an event A to simply happen before an event B, A must precede B in simply happens-before order. 12, 12, 13

## simply happens-before order

An ordering relation that is consistent with program order and the synchronizes-with relation. 12, 56, 97

## sink iteration

A doacross iteration for which executable code, because of a doacross dependence, cannot execute until executable code from the source iteration has completed. 512, 47

## socket

The physical location to which a single chip of one or more cores of a device is attached. 128 soft pause

An instance of a resource-relinquishing routine that specifies that the OpenMP state is required to persist. 564, 564

## source iteration

A doacross iteration for which executable code must complete execution before executable code from another doacross iteration can execute due to a doacross dependence. 512, 47, 98

## stand-alone directive

A unassociated directive that is also an executable directive. 153, 155, 156

## standard trace format

A format for OMPT trace records. 704, 710, 728, 812, 894

## starting address

The address of the first storage location of a list item or, for a mapped variable of its original list item. 51, 70, 281

## static context selector

The context selector for which traits in the OpenMP context can be fully determined at compile time. 48, 324, 326, 329

## static storage duration

For C/C++, the lifetime of an object with static storage duration, as defined by the base language. For Fortran, the lifetime of a variable with a SAVE attribute, implicit or explicit, a common block object or a variable declared in a module. 8, 25, 44, 55, 65, 106, 211, 214, 215, 218, 224, 242, 274, 282, 287, 290, 291, 298, 302, 305, 309, 311, 345, 360, 361, 436, 437, 461, 885

## step expression

A loop-invariant expression used by an induction operation. 32, 60, 64, 171, 243, 244, 248, 264

## storage block

The physical storage that corresponds to an address range in memory. 9, 19, 38, 52, 69, 72, 82, 87, 99, 112, 463, 891

## storage location

A storage block in memory. 7–9, 19, 25, 26, 49, 65, 89, 98, 188, 193–195, 233, 236, 237, 256, 259, 281, 308, 360, 401, 435, 494–497, 499, 500, 508, 509, 607, 715, 888, 891

## strictly nested region

A region nested inside another region with no other explicit region nested between them. 81, 105, 395, 396, 398, 421, 425, 582, 585, 600, 602, 901, 917

## strictly structured block

A single Fortran BLOCK construct, with a single entry at the top and a single exit at the bottom. 99, 153, 411

## string literal

For C/C++, a string literal. For Fortran, a character literal constant. 53, 140, 469, 471

## striping

The reordering of logical iterations of a loop that follows a grid while skipping logica iterations in-between. 379, 901

## strong flush

A flush that has the strong flush property. 10, 10, 11, 13, 53, 496, 499

## strong flush property

A flush with the strong flush property flushes a set of variables from the temporary view of the memory of the current thread to the memory. 52, 99, 499

## structure

A structure is a variable that contains one or more variables that may have diferent types. This includes variables that have a struct type in C/C++, variables that have a class type in C++, and variables that have a derived type and are not arrays in Fortran. 36, 99, 212, 214, 238, 276, 278, 280, 282, 283, 287, 288, 296, 298, 299, 315, 462, 545, 698, 700, 707, 715, 718, 719, 725, 727, 728, 731, 734, 744–746, 754, 761, 798, 812, 819, 820, 823, 824, 831, 888, 909, 912

## structured block

For C/C++, an executable statement, possibly compound, with a single entry at the top and a single exit at the bottom, or an OpenMP construct. For Fortran, a strictly structured block or a loosely structured block. 186, 3, 7, 29, 35, 37, 43, 67, 82, 95, 109, 110, 132, 153–155, 186, 187, 198, 202, 236–239, 271, 273, 342, 371, 382, 384, 385, 395, 402, 405–407, 409, 410,

412–414, 421, 426, 427, 435, 439, 447, 458, 459, 474, 479, 502, 503, 516, 590, 705, 725, 741, 744, 754, 767, 768, 882, 890

## structured block sequence

For C/C++, a sequence of zero or more executable statements (including constructs) that together have a single entry at the top and a single exit at the bottom. For Fortran, a block of zero or more executable constructs (including OpenMP constructs) with a single entry at the top and a single exit at the bottom. 29, 47, 49, 91, 95, 101, 154, 186, 198, 202, 230, 231, 267–270, 407–409, 890

## structured parallelism

Parallel execution through the implicit tasks of (possibly nested) parallel regions by the set of structured threads in a contention group. 142, 143

## structured thread

A thread that is assigned to a team and is not a free-agent thread. 94, 100, 107, 117, 142, 387, 897

## subroutine

A procedure for which a call cannot be used as the right-hand side of a base language assignment operation. 554, 556, 568, 572–575, 582, 584, 589, 592, 599, 601, 608, 638–641, 646, 652, 661, 664–671, 673, 674, 680, 682, 683, 685, 692, 711, 722, 746–753, 755–757, 759–764, 766–769, 772–777, 780, 782, 784, 801, 807

## subsidiary directive

A directive that is not an executable directive and that appears only as part of a construct. 152, 156, 266–268, 408, 429, 434, 435, 901

## subtask

A portion of a task region between two consecutive task scheduling points in which a thread cannot switch from executing one task to executing another task. 5, 5, 448, 449

## successor task

For a given task, a dependent task of that task, or any successor task of a dependent task of that task. 507, 100

## supported active levels

An implementation defined maximum number of active levels of parallelism. 575, 576, 885

## supported device

The host device or any non-host device supported by the implementation, including any device-related requirements specified by the requires directive. 119, 139–141, 450

## synchronization construct

A construct that orders the completion of code executed by diferent threads. 472, 2, 6, 522, 760

## synchronization hint

An indicator of the expected dynamic behavior or suggested implementation of a synchronization mechanism. 561, 472, 561, 562, 663, 893, 911

## synchronizes with

For an event A to synchronize with an event B, a synchronizes-with relation must exist from A to B. 12, 11, 12, 19, 502–504

## synchronizes-with relation

An asymmetric relation that relates a release flush to an acquire flush, or, for C/C++, any pair of events A and B such that A “synchronizes with” B according to the base language, and establishes memory consistency between their respective executing threads. 10, 92, 98, 101

## synchronizing-region callback

A callback that has the synchronizing-region property. 763, 764

## synchronizing-region property

The property that a callback indicates the beginning or end of a synchronization-related region. 763, 101, 763, 764

## synchronizing threads

Two threads are synchronizing if the completion of a structured block sequence by one of the threads requires that it first observes a modification by the other thread, including the modification to an internal synchronization variable that an implementation performs for implicit flush synchronization as described in Section 1.3.5. 6, 7, 101, 362, 393
