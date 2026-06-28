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

## modifier

A mechanism to customize clause behavior for its specified arguments. xxvii, 22, 33, 35, 41, 50, 53, 63, 70, 76, 80, 81, 86, 87, 91, 92, 97, 109, 110, 126, 158–163, 169, 171, 174, 181, 215, 224, 230, 231, 233, 249, 251, 268, 275, 276, 278, 280–282, 286, 287, 294–296, 300, 316, 317, 331–333, 342, 343, 348, 414, 419, 421, 435–437, 459, 468, 470, 471, 505, 513, 528, 529, 739, 888, 890, 891, 898–902, 904–907, 909, 911

## mutex-acquiring callback

A callback that has the mutex-acquiring property. 765

## mutex-acquiring property

The property of a callback that it is dispatched when attempting to acquire mutually-exclusive access for a mutual-exclusion construct or when initializing or attempting to acquire a lock. 765, 73, 766

## mutex-execution callback

A callback that has the mutex-execution property. 767

## mutex-execution property

The property of a callback that it is dispatched when mutually-exclusive access is acquired or released for a mutual-exclusion construct or when a lock is acquired, released, or destroyed. 767, 74, 767, 768

## mutual-exclusion construct

A construct that has the mutual-exclusion property. 74, 765–768

## mutual-exclusion property

The property that a construct provides mutual-exclusion semantics. 74, 473, 494, 514, 515

## mutually exclusive tasks

Tasks that may be executed in any order, but not at the same time. 448, 508

## N

## named-handle property

The property that a handle is an integer kind in Fortran that is distinguished by the name of the handle. 538, 553, 558–560

## named parameter list item

A parameter list item that is the name of a parameter of a procedure. 163, 162, 163, 299, 300

## named pointer

For C/C++, the base pointer of a given lvalue expression or array section, or the base pointer of one of its named pointers. For Fortran, the base pointer of a given variable or array section, or the base pointer of one of its named pointers.

COMMENT: For the array section (\*p0).x0[k1].p1->p2[k2].x1[k3].x2[4][0:n], where identifiers pi have a pointer type declaration and identifiers xi have an array type declaration, the named pointers are: p0, (\*p0).x0[k1].p1, and (\*p0).x0[k1].p1->p2.

74, 165

## name-list trait

A trait that is defined with properties that match the names that identify particular instances of the trait that are efective at a given point in an OpenMP program. 318, 319, 321, 322

## native thread

An execution entity upon which an OpenMP thread may be implemented. 3, 5, 6, 75, 80, 81, 88, 107, 117, 135, 136, 385, 395, 398, 719, 733, 734, 742, 745, 747, 777, 786, 817, 829, 836, 855–857, 867, 878

## native thread context

A tool context that refers to a native thread. 822, 836, 837, 839, 841

## native thread handle

A handle that refers to a native thread. 828, 854–857, 867, 869

## native thread identifier

An identifier for a native thread defined by a native thread implementation. 138, 822, 829, 830, 841, 851, 855, 856

## native trace format

A format for implementation defined trace records that may be device-specific. 75, 704–706, 812, 814

## native trace record

A trace record in a native trace format. 706, 726, 727, 812–814

## nestable lock

A lock that can be acquired (i.e., set) multiple times by the same task before being released (i.e., unset). 663, 75, 504, 560, 663, 664, 672, 734, 769, 795

## nestable lock property

The property that a routine operates on nestable locks. 663, 75, 665, 667, 669, 671, 674, 676

## nestable lock routine

A routine that has the nestable lock property. 663, 560
