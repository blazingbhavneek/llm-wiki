# OpenMP-API-Specification Source Lines 3047-3410

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source OpenMP-API-Specification:L3047-L3410

Citation: [OpenMP-API-Specification:L3047-L3410]

````text
## locator list

An argument list that consists of locator list items. 162, 160, 295, 437

## locator list item

A list item that refers to storage locations in memory and is one of the items specifically identified in Section 5.2.1. 163, 65, 162–164, 181, 435, 437, 505, 506, 508, 510

## lock

An OpenMP variable that is used in lock routines to enforce mutual exclusion. 65, 66, 74, 75, 80, 97, 109, 110, 449, 496, 501, 504, 558, 561, 663–668, 670–676, 734, 742, 769, 788, 795, 893, 913

## lock-acquiring property

The property that a routine may acquire a lock by putting it into the locked state. 670, 65, 663, 670, 671

## lock-acquiring routine

A routine that has the lock-acquiring property. 670, 449, 663, 670, 675, 765–768

## lock-destroying property

The property that a routine destroys a lock by putting it into the uninitialized state. 667, 65, 668, 669

## lock-destroying routine

A routine that has the lock-destroying property. 667, 668, 669, 767

## locked state

The lock state that indicates the lock has been set by some task. 663, 65, 66, 673

## lock-initializing property

The property that a routine initializes a lock by putting it into the unlocked state. 664, 65, 664–667

## lock-initializing routine

A routine that has the lock-initializing property. 664, 664–667, 765, 766

## lock property

The property that a routine operates on locks. 663, 66

## lock-releasing property

The property that a routine may unset a lock by returning it to the unlocked state. 672, 66, 663, 673, 674

## lock-releasing routine

A routine that has the lock-releasing property. 672, 449, 663, 672, 673, 767, 768

## lock routine

A routine that has the lock property. 663, 65, 535, 663, 893

## lock state

The state of a lock that determines if it can be set. 663, 65, 109, 110, 663, 672–674

## lock-testing property

The property that a routine that may set a lock by putting it into the locked state does not suspend execution of the task that executes the routine if it cannot set the lock. 675, 66, 675, 676

## lock-testing routine

A routine that has the lock-testing property. 675, 675, 766–768

## logical iteration

An instance of the executed loop body of a canonical loop nest, or a DO CONCURRENT loop in Fortran, denoted by a number in the logical iteration space of the loops that indicates an order in which the logical iteration would be executed relative to the other logical iterations in a sequential execution. 4, 20, 32, 33, 47, 50, 59, 61, 66, 67, 92, 94, 99, 107, 111, 204, 205, 253, 370, 371, 375, 377–382, 401, 429–433, 534, 719, 754, 889, 890, 905, 907, 910, 912, 916

## logical iteration space

For a canonical loop nest, or a DO CONCURRENT loop in Fortran, the sequence $0 , \ldots , N - 1$ where N is the number of distinct logical iterations. 204, 32, 47, 55, 59, 66, 107, 204, 374, 377–380, 534

## logical iteration vector

An n-tuple $( i _ { 1 } , \ldots , i _ { n } )$ that identifies a logical iteration of a canonical loop nest, where n is the loop nest depth and $i _ { k }$ is the logical iteration number of the $k ^ { \mathrm { t h } }$ loop, from outermost to innermost. 64, 66, 88, 205, 380, 381, 905

## logical iteration vector space

The set of logical iteration vectors that each correspond to a logical iteration of a canonical loop nest. 205, 379, 381

## loop body

A structured block that encompasses the executable statements that are iteratively executed by a loop statement. 197, 62, 63, 66, 378, 434

## loop-collapsing construct

A loop-nest-associated construct for which some number of outer loops of the associated loop nest may be collapsed loops. 31, 32, 205, 219, 220, 233, 398

## loop-iteration variable

For a loop of a canonical loop nest, var as defined in Section 6.4.1. A C++ range-based for-statement has no loop-iteration variable. 67, 171, 196, 200–205, 211–213, 230, 233, 371, 424, 434, 512, 513, 529, 531, 916

## loop-iteration vector

An n-tuple $( i _ { 1 } , \ldots , i _ { n } )$ that identifies a logical iteration of the afected loops of a loop-nest-associated directive, where n is the number of afected loops and $i _ { k }$ is the value of the loop-iteration variable of the $k ^ { \mathrm { t h } }$ afected loop, from outermost to innermost. 67, 203, 204, 512, 513

## loop-iteration vector space

The set of loop-iteration vectors that each corresponds to a logical iteration of the afected loops of a loop-nest-associated directive. 204, 203, 204

## loop-nest-associated construct

A loop-nest-associated directive and its associated loop nest. 60, 62, 64, 67, 92, 94, 97, 113, 154, 205, 234, 259, 372, 373, 380, 381, 404, 512, 531

## loop-nest-associated directive

An executable directive for which the associated user code must be a canonical loop nest. 153, 20, 23, 67, 152, 153, 198, 203, 211, 212, 233, 258, 371, 372, 375, 377, 379–381, 399, 416, 417, 420, 423, 429, 516

## loop nest depth

For a canonical loop nest, the maximal number of loops, including the outermost loop, that can be afected by a loop-nest-associated directive. 66, 203, 206, 374

## loop schedule

The manner in which the collapsed iterations of afected loops are to be distributed among a set of threads that cooperatively execute the afected loops. 205, 35, 92, 94, 205, 398, 404, 414, 420, 423, 905

## loop-sequence-associated construct

A loop-sequence-associated directive and its associated canonical loop sequence. 68, 207

## loop-sequence-associated directive

An executable directive for which the associated user code must be a canonical loop sequence. 153, 23, 67, 152, 371, 374

## loop sequence length

For a canonical loop sequence, the number of consecutive canonical loop nests regardless of their nesting into blocks. 203, 208

## loop-sequence-transforming construct

A loop-sequence-associated construct with the loop-transforming property. 371

## loop-transforming construct

A loop-transforming directive and its associated loop nest or associated canonical loop sequence. 371, 54, 76, 108, 197, 203, 205, 370–374, 378, 431, 900, 901, 904, 907

## loop-transforming directive

A directive with the loop-transforming property. 54, 68, 108, 371, 373, 374, 379

## loop-transforming property

The property that a construct is replaced by the loops that result from applying the transformation as defined by its directive to its afected loops. 68, 369, 374, 375, 377, 379–381

## loosely structured block

For Fortran, a block of zero or more executable constructs (including OpenMP constructs), where the first executable construct (if any) is not a Fortran BLOCK construct, with a single entry at the top and a single exit at the bottom. 99, 153

## M

## map-entering clause

A map clause that, if it appears on a map-entering construct, specifies that the reference counts of corresponding list items are increased and, as a result, those list items may enter the device data environment. 275, 68, 283, 285, 361, 455

## map-entering construct

A construct that has the map-entering property. 68, 274, 281, 283, 284, 287, 527, 564

## map-entering map type

A map-type that specifies the clause on which it is specified is a map-entering clause. 275, 275

## map-entering property

A property of a construct that it may include mapping operations that allocate storage on the target device and that result in assignment to the corresponding list item from the original list item. 68, 275, 454, 458, 460

## map-exiting clause

A map clause that, if it appears on a map-exiting construct, specifies that the reference counts of corresponding list items are decreased and, as a result, those list items may exit the device data environment. 275, 69, 457

## map-exiting construct

A construct that has the map-exiting property. 69, 274, 284, 527

## map-exiting map type

A map-type that specifies the clause on which it is specified is a map-exiting clause. 275, 275

## map-exiting property

A property of a construct that it may include mapping operations that release storage on the target device and that result in assignment from the corresponding list item to the original list item. 69, 275, 456, 458, 460

## mappable storage block

A storage block, derived from the list items of map clauses specified on a data-mapping construct, for which a corresponding storage block in a device data environment is created, removed, or otherwise referenced by the construct. 283, 284, 287, 296

## mappable type

A type that is valid for a mapped variable. If a type is composed from other types (such as the type of an array element or a structure element) and any of the other types are not mappable types then the type is not a mappable type.

For C, the type must be a complete type.

For C++, the type must be a complete type; in addition, for class types:

• All member functions accessed in any target region must appear in a declare target directive.

For Fortran, no restrictions on the type except that for derived types:

• All type-bound procedures accessed in any target region must appear in a declare\_target directive.

COMMENT: Pointer types are mappable types but the memory block to which the pointer refers is not mapped.

69, 287, 290, 291, 296

## mapped address range

For a given original list item, the address range that starts from its starting address and ends with its ending address. 280, 71, 281

## mapped variable

An original variable in a data environment with a corresponding variable in a device data environment. The original and corresponding variables may share storage. 38, 49, 69, 70, 82, 98, 464, 564

## mapper

An operation that defines how variables of given type are to be mapped or updated with respect to a device data environment. 41, 48, 111, 183, 274–276, 278, 281–283, 287, 293–296, 298, 299

## mapper identifier

An OpenMP identifier that specifies the name of a user-defined mapper. 278, 278, 295

## mapping operation

An operation that establishes or removes a correspondence between a variable in one data environment and another variable in a device data environment. 9, 23, 25, 69, 70, 95, 275, 283, 284, 286, 361, 564, 734, 739, 899, 900

## map type

A categorization of a data-mapping clause that determines whether the mapping operations that result from that clause include assignments between the original storage and corresponding storage of its list items. 61, 82, 109, 283, 284

## map-type decay

A process applied to input map type, according to an underlying map type, that results in an output map type. 275, 61, 82, 275, 281, 459

## map-type-modifying property

The property that a modifier that combines with a map-type to determine details of a mapping operation. 280, 282

## matchable candidate

A mapped variable for which corresponding storage was created in a device data environment. 280, 71, 281

## matched candidate

A matchable candidate that, due to a matching mapped address range or extended address range, may determine the lower bound and length to use for a given assumed-size array that is a list item in a map clause. 281, 236, 281, 287, 904

## matching taskgraph record

A finalized taskgraph record that has a matching value for the scalar expression that identifies a taskgraph region. 436, 92, 435–439

## memory

A storage resource for storing and retrieving variables that are accessible by threads. 7, 6–11, 13, 19, 20, 32, 44, 52, 63, 65, 71–73, 76, 89, 92, 99, 101, 105, 107, 114, 116, 143, 164, 165, 231, 303–308, 359, 360, 484–487, 494, 499, 509, 544, 555, 561, 603, 607, 608, 612, 618, 619, 630, 639, 643, 646, 647, 654, 655, 661, 662, 720, 774, 778, 779, 799, 821, 826, 833–837, 839, 840, 846, 853, 872, 874, 876, 885, 899, 900, 902, 903, 907–910, 913, 915

## memory-allocating routine

A memory-management routine that has the memory-allocating-routine property. 654, 20, 72, 89, 114, 654, 655, 662

## memory-allocating-routine property

The property that a memory-management routine allocates memory. 654, 71, 656–660

## memory allocator

An OpenMP object that fulfills requests to allocate and to deallocate memory for program variables from the storage resources of its associated memory space. 9, 9, 21, 23, 24, 71, 72, 116, 287, 305–313, 358, 463, 549, 646, 647, 652–655, 662, 888, 899, 903, 910

## memory-allocator-retrieving property

The property that a memory-management routine retrieves a memory allocator handle. 647, 71, 647–651

## memory-allocator-retrieving routine

A memory-management routine that has the memory-allocator-retrieving property. 647, 647–652

## memory-copying property

The property that a routine copies memory from the device data environment of one device to the device data environment of another device. 612, 71, 613–615, 617

## memory-copying routine

A routine that has the memory-copying property. 612, 52, 89, 448, 612, 613

## memory-management routine

A routine that has the memory-management-routine property. 630, 20, 71–73, 630, 635–637

## memory-management-routine property

The property that a routine manages memory on the current device. 630, 72, 631–636, 638–644, 646–653, 656–661

## memory part

A storage block that resides on a single storage resource within a memory space. 72

## memory partition

A definition of how a memory allocator divides the allocated memory into memory parts and the storage resources on which it allocates those memory parts. 72, 307, 553, 555, 556, 639, 641–644

## memory partitioner

An OpenMP object that represents mechanisms to create and to destroy memory partitions. 72, 306, 307, 547, 553–555, 637–644

## memory-partitioning property

The property that a memory-management routine creates or destroys or otherwise afects memory partitions or memory partitioners. 637, 72, 638–643

## memory-partitioning routine

A memory-management routine that has the memory-partitioning property. 637

## memory-reading callback

A callback that has the memory-reading property. 837, 837, 838

## memory-reading property

The property that a callback reads memory from an OpenMP program. 837, 72, 838

## memory-reallocating routine

A memory-management routine that has the memory-reallocating-routine property. 654, 655, 660

## memory-reallocating-routine property

The property that a memory-allocating routine deallocates memory in addition to allocating it. 72, 660

## memory-setting property

The property that a routine fills memory in a device data environment with a specified value. 618, 73, 619, 620

## memory-setting routine

A routine that has the memory-setting property. 618, 448, 618–621

## memory space

A representation of storage resources from which memory can be allocated or deallocated. More than one memory space may exist. 630, 9, 23, 24, 72, 73, 102, 144, 287, 304, 307, 317, 555, 630, 635–637, 643, 645, 647, 888, 903, 910

## memory-space-retrieving property

The property that a memory-management routine retrieves a memory space handle. 630, 73, 631–634

## memory-space-retrieving routine

A memory-management routine that has the memory-space-retrieving property. 630, 630–634

## mergeable task

A task that may be a merged task if it is an undeferred task. 440, 102, 427, 440, 468, 479

## merged task

A task with a minimal data environment. 73, 428, 440, 449, 459, 719, 781, 882

## metadirective

A directive that conditionally resolves to another directive. 324, 47, 48, 92, 152, 324–327, 363, 889, 904, 905, 907, 910

## minimal data environment

A data environment of a task that, inclusive of ICVs, is the same as that of its enclosing context, with the exception of list items in all-data-environments clauses that are specified on the task-generating construct that generated the task. 21, 73, 236, 238
````
