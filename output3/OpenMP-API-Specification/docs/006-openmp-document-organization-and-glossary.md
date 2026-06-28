
The remainder of this document is structured as normative chapters that define the directives, including their syntax and semantics, the routines and the tool interfaces that comprise the OpenMP API. The document also includes appendices that facilitate maintaining a compliant implementation of the API.

Some sections of this document only apply to programs written in a certain base language. Text that applies only to programs for which the base language is C or C++ is shown as follows:

C / C++

C/C++ specific text...

C / C++

Text that applies only to programs for which the base language is C only is shown as follows:

C

C specific text...

C

Text that applies only to programs for which the base language is C++ only is shown as follows:

C++

C++ specific text...

C++

Text that applies only to programs for which the base language is Fortran is shown as follows:

Fortran

Fortran specific text...

Fortran

Text that applies only to programs for which the base language is Fortran or C++ is shown as follows:

Fortran / C++

Fortran/C++ specific text...

Fortran / C++

Where an entire page consists of base language specific text, a marker is shown at the top of the page. For Fortran-specific text, the marker is:

Fortran (cont.)

For C/C++-specific text, the marker is:

C/C++ (cont.)

Some text is for information only, and is not part of the normative specification. Such text is designated as a note or comment, like this:

Note – Non-normative text...

COMMENT: Non-normative text...

## 2 Glossary

## A | B | C | D | E | F | G | H | I | L | M | N | O | P | R | S | T | U | V | W | Z

## A

## abstract name

A conceptual abstract name or a numeric abstract name. 128, 34, 77, 128, 131, 134, 886, 897 accessible device

The host device or any non-host device accessible for execution. 119, 139–141, 360

## accessible storage

A storage block that may be accessed by a given thread. 285, 606

## acquire flush

A flush that has the acquire flush property. 10, 11, 12, 92, 101, 496, 499, 501–504

## acquire flush property

A flush with the acquire flush property orders memory operations that follow the flush after memory operations performed by a diferent thread that synchronizes with it. 19, 52, 499

## active level

An active parallel region that encloses a given region at some point in the execution of an OpenMP program. The number of active levels is the number of active parallel regions that encloses the given region. 19, 75, 100, 129, 130, 133, 576, 886, 892, 911

## active parallel region

A parallel region comprised of implicit tasks that are being executed by a team to which multiple threads are assigned. 19, 105, 115, 116, 132, 216, 217, 571, 576, 577, 579, 580, 885, 888, 915, 916

## active target region

A target region that is executed on a device other than the device that encountered the target construct. 124

## address range

The addresses of a contiguous set of storage locations. 51, 70, 99, 606

## address space

A collection of logical, virtual, or physical memory address ranges that contain code, stack, and/or data. Address ranges within an address space need not be contiguous. An address space consists of one or more segments. 20, 52, 80, 95, 109, 145, 146, 359, 606, 699, 700, 820, 831, 836, 838, 839, 841–843, 846, 849, 850, 852, 853, 855, 870, 872, 874

## address space context

A tool context that refers to an address space within an OpenMP process. 820

## address space handle

A handle that refers to an address space within an OpenMP process. 828, 849–851, 857, 868

## affected iteration

A logical iteration of the afected loops of a loop-nest-associated directive. 60, 94, 97, 382

## affected loop

A loop from a canonical loop nest, or a DO CONCURRENT loop in Fortran, that is afected by a given loop-nest-associated directive. 203, 4, 20, 62, 67, 68, 108, 113, 154, 203–205, 211, 212, 226, 230, 231, 233, 234, 253, 259, 267, 268, 371, 372, 378–381, 424, 910

## affected loop nest

The subset of canonical loop nests of an associated loop sequence that are selected by the looprange clause. 207, 35, 92, 205, 371, 375

## aggregate variable

A variable, such as an array or structure, composed of other variables. For Fortran, a variable of character type is considered an aggregate variable. 8, 20, 40, 112, 164, 217, 223, 292, 445, 885

## aligned-memory-allocating routine

A memory-management routine that has the aligned-memory-allocating-routine property. 654, 655, 657, 659

## aligned-memory-allocating-routine property

The property that a memory-allocating routine ensures the allocated memory is aligned with respect to an alignment argument. 654, 20, 657, 659

## all-constituents property

The property that a clause applies to all leaf constructs that permit it when the clause appears on a compound directive. 159, 160, 528

## all-contention-group-tasks binding property

The binding property that the binding task set is all tasks in the contention group. 534, 664–671, 673–676

## all-data-environments clause

A clause that has the all-data-environments property. 73, 236, 238

## all-data-environments property

The property that a data-sharing attribute clause afects any data environment for which it is specified, including minimal data environments. 21, 236, 238, 257

## all-device-tasks binding property

The binding property that the binding task set is all tasks on a specified device. 690

## all-device-threads binding property

The binding property that the binding thread set is all threads on the current device. The efect of executing a construct or a routine with this property is not related to any specific region that corresponds to any other construct or routine. 534, 586, 594, 630–636, 638–644, 646–651, 679, 680, 791, 792

## allocator

A memory allocator. 21, 143, 144, 305–312, 315, 316, 358, 463, 545, 547, 555, 558, 638–640, 645, 647, 652–655, 662, 888, 899, 900, 904, 905

## allocator structured block

A context-specific structured block that may be associated with an allocators directive. 187, 315

## allocator trait

A trait of an allocator. 144, 305, 307, 308, 311, 313, 547, 549, 552, 638, 645, 888, 899, 900, 910

## all-privatizing property

The property that a clause, when it appears on a combined construct or a composite construct, applies to all constituent constructs to which it applies for which a data-sharing attribute clause may create a private copy of the same list item. 159, 312, 528

## all tasks

All tasks participating in the OpenMP program or in a specified limiting context. 21, 28, 251, 301, 306, 535, 690

## all-tasks binding property

The binding property that the binding task set is all tasks. 690, 689, 690

## all threads

All OpenMP threads participating in the OpenMP program. A specific usage of the term may be explicitly limited to a limiting context, such as all threads on a given device or an OpenMP thread pool. 8, 13, 21, 22, 28, 231, 494, 535, 630, 691, 791–793

## all-threads binding property

The binding property that the binding thread set is all threads. The efect of executing a construct or a routine with this property is not related to any specific region that corresponds to any other construct or routine. 534

## ancestor thread

For a given thread, its parent thread or one of the ancestor threads of its parent thread. 22, 578, 579, 589, 902, 916

## antecedent task

A task that must complete before its dependent tasks can be executed. 507, 42, 51, 59, 86, 103, 503, 507, 509, 762

## argument list

A list that is used as an argument of a directive, clause, or modifier. 158, 46, 47, 51, 63, 65, 80, 83, 86, 87, 108, 112, 159, 162, 163, 210, 218, 219, 269, 270

## array base

The base array of a given array section or array element, if it exists; otherwise, the base pointer of the array section or array element.

COMMENT: For the array section (\*p0).x0[k1].p1->p2[k2].x1[k3].x2[4][0:n], where identifiers pi have a pointer type declaration and identifiers xi have an array type declaration, the array base is: (\*p0).x0[k1].p1->p2[k2].x1[k3].x2.

More examples for C/C++:

• The array base for x[i] and for x[i:n] is x, if x is an array or pointer.

• The array base for x[5][i] and for x[5][i:n] is x, if x is a pointer to an array or x is 2-dimensional array.

• The array base for y[5][i] and for y[5][i:n] is y[5], if y is an array of pointers or y is a pointer to a pointer.

Examples for Fortran:

• The array base for x(i) and for x(i:j) is x.

22, 167, 168, 237, 239, 247, 277, 281, 282

## array element

A single member of an array as defined by the base language. 23, 241, 247, 259, 269, 270, 276, 281, 286, 295, 296

## array item

An array, an array section, or an array element. 529

## array section

A designated subset of the elements of an array that is specified using a subscript notation that can select more than one array element. 22–24, 26, 27, 36, 37, 39, 74, 97, 112, 114, 140, 163, 166–168, 221, 236–239, 241, 243, 244, 247, 259, 269, 270, 280, 281, 283, 286, 288, 294, 295, 395, 444, 508, 509, 529, 898, 906, 909, 911, 912, 914

## array shaping

A mechanism that reinterprets the region of memory to which an expression that has a type of pointer to T as an n-dimensional array of type T. 95, 909

## assignable OpenMP type instance

An instance of an OpenMP type to which an assignment can be performed. 183, 183

## assigned list item

A list item to which assignment is performed as the result of a data-motion clause. 296, 298

## assigned thread

A thread that has been assigned an implicit task of a parallel region. 3, 4, 87, 104, 106, 390, 391, 414, 569

## assigning map type

A map-type for which the mapping operations may include an assignment operation. 275

## associated device

The associated device of a memory allocator is the device that is specified when the memory allocator is created. If the associated memory space is a predefined memory space, the associated device is the current device. 7, 23

## associated loop nest

The associated canonical loop nest, or DO CONCURRENT loop in Fortran, of a loop-nest-associated directive. 67, 68, 203, 206, 207, 371, 374

## associated loop sequence

The associated canonical loop sequence of a loop-sequence-associated directive. 20, 207, 371

## associated memory space

The associated memory space of a memory allocator is the memory space that is specified when the memory allocator is created. 23, 24, 71, 305, 308

## assumed-size array

For C/C++, an array section for which the length is absent and the size of the dimensions is not known. For Fortran, an assumed-size array in the base language. 24, 71, 114, 166, 168, 198, 212, 213, 222, 236, 238, 275, 280, 281, 286, 287, 535, 899, 915

## assumption directive

A directive that provides invariants that specify additional information about the expected properties of the program that can optionally be used for optimization. 24, 362, 365, 904, 906

## assumption scope

The scope for which the invariants specified by an assumption directive must hold. 362–369

## asynchronous device routine

A routine that has the asynchronous-device routine property. 505, 603, 604, 616, 618, 621

## asynchronous-device routine property

The property of a device routine that it performs its operation asynchronously. 24, 604, 615, 617, 620

## async signal safe

The guarantee that interruption by signal delivery will not interfere with a set of operations. An async signal safe runtime entry point is safe to call from a signal handler. 24, 744, 777, 786

## async-signal-safe entry point

An entry point that has the async-signal-safe property. 786

## async-signal-safe property

The property of a routine or entry point that it is async signal safe. 7, 24, 786, 791–795, 797, 799–801

## atomic captured update

An atomic update operation that is specified by an atomic construct on which the capture clause is present. 111, 193, 491, 495, 914

## atomic conditional update

An atomic update operation that is specified by an atomic construct on which the compare clause is present. 34, 35, 191, 491, 492, 495–497, 907

## atomic operation

An operation that is specified by an atomic construct or is implicitly performed by the OpenMP implementation and that atomically accesses and/or modifies a specific storage location. 8, 11–13, 25, 89, 92, 95, 283, 284, 308, 472, 496, 497, 502, 907

## atomic read

An atomic operation that is specified by an atomic construct on which the read clause is present. 89, 190, 488, 495

## atomic scope

The set of threads that may concurrently access or modify a given storage location with atomic operations, where at least one of the operations modifies the storage location. 8, 12, 308, 494

## atomic structured block

A context-specific structured block that may be associated with an atomic directive. 188, 30, 89, 111, 114, 188, 193, 494–496, 898

## atomic update

An atomic operation that is specified by an atomic construct on which the update clause is present. 24, 89, 111, 190, 489, 491, 495–497, 914

## atomic write

An atomic operation that is specified by an atomic construct on which the write clause is present. 114, 190, 490, 495

## attached pointer

A pointer variable or referring pointer in a device data environment that, as a result of a mapping operation, points to a given data entity that also exists in the device data environment. 85, 284, 287, 288, 296, 463

## attach-ineligible

An attribute of a pointer for which pointer attachment may not be performed. 282

## automatic storage duration

For C/C++, the lifetime of a variable or object with automatic storage duration, as defined by the base language. For Fortran, the lifetime of a variable, including implied-do, FORALL, and DO CONCURRENT indices, that is neither a variable that has static storage duration nor a dummy argument without the VALUE attribute. For referencing variables, this refers to the lifetime of the referring pointer unless explicitly specified otherwise. 211, 214, 220

## available device

An available non-host device or, where explicitly specified, the host device. 139, 141, 319, 634, 652, 690

## available non-host device

A non-host device that can be used for the current OpenMP program execution. 26, 139

## B

## barrier

A point in the execution of a program encountered by a team, beyond which no thread in the team may execute until all threads in the team have reached the barrier and all explicit tasks generated for execution by the team have executed to completion. If cancellation has been requested, threads may proceed to the end of the canceled region even if some threads in the team have not reached the barrier. 4, 6, 26, 50, 58, 273, 385, 402, 404–407, 409, 414, 448, 475–477, 482, 496, 500–502, 521, 590, 689, 704, 733, 763, 764, 902, 917

## base address

If a data entity has a base pointer, the address of the first storage location of the implicit array of its base pointer; otherwise, if the data entity has a referenced pointee, the address of the first storage location of its referenced pointee; otherwise, if the data entity has a base variable, the address of the first storage location of its base variable; otherwise, the address of the first storage location of the data entity. 51, 236, 239, 281, 610

## base array

For C/C++, a containing array of a given lvalue expression or array section that does not appear in the expression of any of its other containing arrays. For Fortran, a containing array of a given variable or array section that does not appear in the designator of any of its other containing arrays.

COMMENT: For the array section (\*p0).x0[k1].p1->p2[k2].x1[k3].x2[4][0:n], where identifiers pi have a pointer type declaration and identifiers xi have an array type declaration, the base array is: (\*p0).x0[k1].p1->p2[k2].x1[k3].x2.

22, 26, 529

## base function

A procedure that is declared and defined in the base language. 41, 54, 92, 113, 322, 328–333, 335, 336, 889

## base language

A programming language that serves as the foundation of the OpenMP specification. Section 1.6 lists the current base languages for the OpenMP API. 2, 3, 6, 8, 12, 13, 15, 17, 18, 23–27, 29, 38, 39, 41, 42, 46, 48, 51, 53, 54, 56, 81, 86–88, 93, 94, 98, 100, 101, 109,

148, 151–153, 155, 156, 162–164, 166, 167, 169, 183–185, 189, 195, 196, 201, 203, 215, 221, 239, 240, 242, 247, 249, 259, 261, 264, 278, 281, 293, 294, 308, 309, 311, 315, 316, 331, 335, 337, 362, 411, 495, 516, 533, 535, 564, 885, 904, 905, 909

## base language thread

A thread of execution that defines a single flow of control within the program and that may execute concurrently with other base language threads, as specified by the base language. 6, 27

## base pointer

For C/C++, an lvalue pointer expression that is used by a given lvalue expression or array section to refer indirectly to its storage, where the lvalue expression or array section is part of the implicit array for that lvalue pointer expression. For Fortran, a data pointer that appears last in the designator for a given variable or array section, where the variable or array section is part of the pointer target for that data pointer.

COMMENT: For the array section (\*p0).x0[k1].p1->p2[k2].x1[k3].x2[4][0:n], where identifiers pi have a pointer type declaration and identifiers xi have an array type declaration, the base pointer is: (\*p0).x0[k1].p1->p2.

22, 26–28, 38, 74, 211, 212, 239, 259, 282–287, 328, 436, 437, 461, 462, 528, 529

## base program

A program written in a base language. 2, 80

## base referencing variable

For C++, a referencing variable that is used by a given lvalue expression or array section to refer indirectly to its storage, where the lvalue expression or array section is part of the referenced pointee of the referencing variable. For Fortran, a referencing variable that appears last in the designator for a given variable or array section, where the variable or array section is part of the referenced pointee of the referencing variable. 212, 461

## base variable

For a given data entity that is a variable or array section, a variable denoted by a base language identifier that is either the data entity or is a containing array or containing structure of the data entity.

COMMENT:

Examples for C/C++:

• The data entities x, x[i], x[:n], x[i].y[j] and x[i].y[:n], where x and y have array type declarations, all have the base variable x.

• The lvalue expressions and array sections p[i], p[:n], p[i].y[j] and p[i].y[:n], where p has a pointer type and p[i].y has an array type, has a base pointer p

but does not have a base variable.

## Examples for Fortran:

• The data objects x, x(i), x(:n), x(i)%y(j) and x(i)%y(:n), where x and y are arrays, all have the base variable x.

• The data objects p(i), p(:n), p(i)%y(j) and p(i)%y(:n), where p is a pointer and p(i)%y is an array, has a base pointer p but does not have a base variable.

• For the associated pointer p, p is both its base variable and base pointer.

26–28, 217, 276, 287, 436, 437, 462, 463, 528, 529

## binding implicit task

The implicit task of the current team assigned to the encountering thread. 28, 57, 124, 389, 652–654

## binding-implicit-task binding property

The binding property that the binding task set is the binding implicit task. 652, 653

## binding property

A property of a construct or a routine that determines the binding region, binding task set and/or binding thread set. 21, 22, 28, 49, 54, 535

## binding region

The enclosing region that determines the execution context and limits the scope of the efects of the bound region is called the binding region. The binding region is not defined for regions for which the binding thread set is all threads or the encountering thread, nor is it defined for regions for which the binding task set is all tasks. 4, 28, 82, 205, 412, 423, 425, 475, 513, 514, 516, 520, 524, 535, 683, 685, 880, 881, 883, 893, 918

## binding task set

The set of tasks that are afected by, or provide the context for, the execution of a region. The binding task set for a given region can be all tasks, the current team tasks, all tasks in the contention group, all tasks of the current team that are generated in the region, the binding implicit task, or the generating task. 21, 28, 54, 121, 338, 435, 454, 456, 458, 461, 465, 468, 478, 482, 535, 603, 652, 653, 690, 786, 880–88

## binding thread set

The set of threads that are afected by, or provide the context for, the execution of a region. The binding thread set for a given region can be all threads on a specified set of devices, all threads that are executing tasks in a contention group, all primary threads that are executing the initial tasks of an enclosing teams region, the current team, or the encountering thread. 5, 21, 22, 28, 49, 82, 84, 92, 107, 113, 205, 229, 231, 384, 394, 398, 399, 402, 404–407, 409,

412–414, 420, 423–426, 429, 430, 435, 439, 446, 473, 475, 479, 482, 494–496, 498, 505, 514, 515, 520, 521, 524, 535, 630, 683, 685, 786, 791–793, 893, 901, 902

## block-associated directive

A directive for which its associated base language code is a structured block. 153, 37, 82, 151–155, 186, 315, 337, 369, 384, 394, 402, 405–407, 409, 412, 426, 435, 458, 460, 473, 478, 494, 515

## bounds-independent loop

For a structured block sequence, an enclosed canonical loop nest where none of its loops have loop bounds that depend on the execution of a preceding executable statement in the sequence. 202

## C

## callback

A tool callback. xxvii, 14, 15, 29, 33, 45, 46, 72–74, 77–79, 81, 83, 85, 91, 101, 110, 250, 286, 346, 352, 386, 395, 403, 405–409, 411, 413, 415, 421, 427, 431, 446, 447, 449, 453, 455, 457, 459, 462, 466, 474–478, 480, 497, 500, 509, 513, 515, 516, 522, 590, 603, 604, 607, 609–611, 613–616, 618–621, 664–669, 671–675, 677, 695, 697, 698, 700, 701, 703–707, 720, 725, 730, 731, 737, 744–781, 783–787, 789, 790, 802, 803, 805–808, 810, 812, 816, 817, 821, 822, 826, 833–844, 846, 848, 851, 853, 870, 872, 874, 876, 894–896, 903, 908

## callback dispatch

The processing of a registered callback when an associated event occurs, in a manner consistent with the return code provided when a first-party tool registered the callback. 29, 729, 807

## callback registration

A process that makes a tool callback available to an OpenMP implementation to enable callback dispatch. 91, 700, 701, 703

## canceled taskgroup set

A taskgroup set that has been canceled. 521, 521

## cancellable construct

A construct that has the cancellable property. 519, 520, 524

## cancellable property

The property that a construct may be subject to cancellation. 519, 29, 384, 407, 416, 417, 478

## cancellation

An action that cancels (that is, aborts) a region and causes the execution of implicit tasks or explicit tasks to proceed to the end of the canceled region. 521, 5, 6, 26, 29, 30, 139, 404, 475, 476, 501, 504, 519–524, 688, 759, 913

## cancellation point

A point at which implicit tasks and explicit tasks check if cancellation has been activated. If cancellation has been activated, they perform the cancellation. 520, 5, 6, 111, 116, 139, 449, 475, 476, 501, 504, 521–524, 741

## candidate

A replacement candidate. 324, 329

## canonical frame address

An address associated with a procedure frame on a call stack that was the value of the stack pointer immediately prior to calling the procedure for which the frame represents the invocation. 721

## canonical loop nest

A loop nest that complies with the rules and restrictions defined in Section 6.4.1. 196, 20, 23, 29, 30, 54, 66–68, 76, 153, 197, 201–203, 206, 207, 230, 267, 370, 371, 374, 375, 379, 380, 382, 419, 531, 901, 909

## canonical loop sequence

A sequence of canonical loop nests that complies with the rules and restrictions defined in Section 6.4.2. 202, 23, 54, 67, 68, 153, 197, 203, 208, 371, 372, 378, 898, 900

## capture structured block

An atomic structured block that may be associated with an atomic directive that expresses capture semantics. 192, 192

## C/C++-only property

The property that an OpenMP feature is only supported in C/C++. 536, 708–711, 714–732, 734–743, 745–753, 755–757, 759–764, 766–770, 772–777, 780, 782, 784, 786–795, 797, 799–801, 803–814, 819, 820, 822–832

## C/C++ pointer property

The property that a routine argument has a pointer type in C/C++ but is an array in Fortran. 535, 554, 556, 574, 638–642, 644, 664–671, 673–676, 694

## child task

A task is a child task of its generating task region. The region of a child task is not part of its generating task region, unless the child task is an included task. 30, 42, 51, 59, 96, 103, 108,

## chunk

A contiguous non-empty subset of the collapsed iterations of a loop-collapsing construct. 94, 134, 414, 418, 419, 421, 422, 429, 531, 574, 719, 754, 894

## class type

For C++, the type of any variable declared with one of the class, struct, or union keywords. 217, 220, 222, 228–231, 244, 249, 254, 258, 271–274, 285, 287, 463

## clause

A mechanism to specify customized directive behavior. xxvii, 4–6, 8, 9, 20–22, 24, 25, 31–33, 35, 39–50, 52, 54, 55, 57, 61, 68–71, 73, 76, 77, 79–82, 86, 87, 90–95, 101, 103, 109, 110, 116, 119, 122, 124–127, 129, 132, 143, 148–153, 157–165, 168–171, 174, 179, 181, 182, 203, 204, 206–208, 210–217, 220–231, 233–240, 244, 247–249, 251–254, 256–296, 298–301, 303, 304, 309–319, 321, 322, 324–367, 370–376, 378–380, 382, 383, 385, 387–389, 393–399, 401–407, 409, 414, 418–427, 429, 430, 432–445, 450–459, 461–464, 466, 468–472, 474, 479–502, 504–519, 521–523, 528–531, 534, 535, 561, 568, 570, 583, 586, 590, 599, 600, 604, 607, 608, 610, 645, 646, 652, 653, 655, 678, 715, 716, 741, 748, 760, 761, 783, 888–891, 897–902, 904–907, 909–914, 916–918

## clause set

A set of clauses for which restrictions on their use or other properties of their use on a given directive are specified. 160, 31, 33, 50, 92, 110, 160, 161, 210, 356, 363, 430

## clause group

A clause set for which restrictions or properties related to their use on all directives are specified. 157, 160, 343, 356, 363, 484, 488, 490, 517, 519, 900

## clause-list trait

A trait that is defined with properties that match the clauses that may be specified for a given directive. 318, 319, 321

## closely nested construct

A construct nested inside another construct with no other construct nested between them. 411, 413, 425, 522, 524

## closely nested region

A region nested inside another region with no parallel region nested between them. 84, 257, 404, 425, 522, 524, 915

## code block

A contiguous region of memory that contains code of an OpenMP program to be executed on a device. 453

## collapsed iteration space

The logical iteration space of the collapsed loops of a loop-collapsing construct. 204, 264, 267, 401, 415, 418, 421, 422

## collapsed iteration

A logical iteration of the collapsed loops of a loop-collapsing construct. 31, 32, 35, 60, 67, 94, 113, 205, 220, 233, 234, 244, 258, 267, 268, 398, 399, 402, 404, 414, 418–423, 429, 502, 516, 531, 753, 754

## collapsed logical iteration

A collapsed iteration. 204, 220

## collapsed loop

For a loop-collapsing construct, a loop that is afected by the collapse clause. 4, 32, 67, 104, 204, 205, 220, 233, 264, 400, 414, 419, 420, 423, 424, 433, 434, 516, 888, 901

## collective step expression

An expression in terms of a step expression and a collector that eliminates recursive calculation in an induction operation. 60, 32, 244

## collector

A binary operator used to eliminate recursion in an induction operation. 60, 32, 266

## collector expression

An OpenMP stylized expression that evaluates to the value of the collective step expression of a collapsed iteration. 244, 60, 244, 246, 264, 266

## combined construct

A construct that is a shortcut for specifying one construct immediately nested inside a leaf construct. 530, 21, 32, 34, 526, 911, 912

## combined directive

A compound directive that is used to form a combined construct. 32, 34, 525

## combined-directive name

The name of a combined directive. 525

## combiner

A binary operator used by a reduction operation. 249, 90, 183, 252, 253

## combiner expression

An OpenMP stylized expression that specifies how a reduction combines partial results into a single value. 240, 90, 240, 241, 248, 251, 260–262, 267, 896

## common-field property

The property that a field has a name that is used in more than one OpenMP type, or in more than one OMPD type, or in more than one OMPT type. 726, 727

## common-type-callback property

The property that a callback has a type that at least one other callback has. 763, 764, 766–768, 838, 843

## compatible context selector

A context selector that matches the OpenMP context in which a directive is encountered. 323, 323–325, 329

## compatible map type

A map-type that is consistent with the data-motion attribute of a given data-motion clause. 295, 298

## compatible property

The property that a clause, an argument, a modifier, or a clause set does not have the exclusive property. 159

## compilation unit

For C/C++, a translation unit. For Fortran, a program unit. 9, 44, 154, 218, 219, 289, 302, 311, 312, 314, 352, 355–357, 361, 368, 463, 608, 645, 646, 655

## compile-time error termination

Error termination that is performed during compilation. 6, 356, 389, 890

## complete tile

A tile that has $\prod _ { k } s _ { k }$ logical iterations, where $s _ { k }$ are the list items of the sizes clause on the construct. 381, 84

## complex modifier

A modifier that may take at least one argument when it is specified. 158, 33, 158, 161, 169

## complex property

The property that a modifier is a complex modifier. 180, 470

## compliant implementation

An implementation of the OpenMP specification that compiles and executes any conforming program as defined by the specification. A compliant implementation may exhibit unspecified behavior when compiling or executing a non-conforming program. 15, 2, 5, 15, 17, 34, 42, 57, 110, 135, 136, 148, 419, 496, 533, 663, 697, 787, 816, 817, 891

## composite construct

A construct that is a shortcut for composing a series or nesting of multiple constructs, but that does not have the semantics of a combined construct. 21, 267, 275, 531, 899, 902

## composite directive

A directive that is composed of two (or more) directives but does not have identical semantics to specifying one of the directives immediately nested inside the other. A composite directive either adds semantics not included in the directives from which it is composed or provides an efective nesting of one directive inside the other that would otherwise be non-conforming. If the composite directive adds semantics not included in its constituent directives, the efects of the constituent directives may occur either as a nesting of the directives or as a sequence of the directives. 34, 458, 526, 527

## composite-directive name

The directive name of a composite directive. 525, 526, 527

## compound construct

A construct that corresponds to a compound directive. 34, 61, 79, 82, 96, 174, 179, 254, 318, 516, 527–531, 898, 913, 918, 919

## compound directive

A combined directive or a composite directive. 20, 32, 34, 35, 64, 160, 525, 528

## compound-directive name

The directive name of a compound directive. 525, 46, 525, 527, 902, 919

## compound target construct

A compound construct for which target is a constituent construct. 276, 277, 529

## conceptual abstract name

An abstract name that refers to an implementation defined abstraction that is relevant to the execution model described by this specification. 128, 19, 77, 85, 128

## conditional-update-capture structured block

An update structured block that may be associated with an atomic directive that expresses an atomic conditional update operation with capture semantics. 192, 192, 193, 497

## conditional-update structured block

An update structured block that may be associated with an atomic directive that expresses an atomic conditional update operation. 191, 191, 192, 497

## conforming device number

A device number that may be used in a conforming program. 7, 141, 305, 321, 322, 452, 547, 592, 599–603, 631, 647, 690

## conforming program

An OpenMP program that follows all rules and restrictions of the OpenMP specification. 2, 15, 34, 35, 76, 79, 110, 324, 371, 419

## C-only property

The property that an OpenMP feature is only supported in C. 697, 712, 820, 825, 827, 828, 834, 835, 837–849, 851–869, 871–873, 875–877

## consistent schedules

The loop schedules of two afected loop nests are consistent if for each assignment of a thread to a collapsed iteration that results from the schedule of one loop nest, the behavior is as if the same thread is assigned to the corresponding collapsed iteration of the other loop nest. 205, 35, 205, 404

## constant property

The property that an expression, including one that is used as the argument of a clause, a modifier or a routine, is a compile-time constant. 161, 53, 93, 151, 160, 162, 163, 181–183, 204, 206, 207, 270, 304, 309, 311, 313, 317, 321, 322, 343, 344, 350, 354, 357–362, 365–367, 373, 376, 379, 382, 383, 401, 439, 440, 443, 484–492, 517–519, 534, 900

## constituent construct

For a given construct, a construct that corresponds to one of the constituent directives of the executable directive. 21, 34, 79, 96, 174, 179, 254, 363, 515, 527–529, 902

## constituent directive

For a given directive and its set of leaf directives, a leaf directive in the set or a compound directive that is a shortcut for composing two or more members of that set for which the directive names are consecutively listed. 34, 35, 160, 174, 275, 458, 459, 528, 531, 898

## constituent-directive name

The directive name of a constituent directive. 525, 525, 531, 919

## construct

An executable directive, its paired end directive (if any), and the associated structured block (if any), not including the code in any called procedures. That is, the lexical extent of an

executable directive. 2–7, 15, 19, 21, 22, 24, 25, 28, 29, 31–37, 40, 42, 43, 45, 46, 48–59, 61, 63, 64, 68, 69, 74–77, 79, 81–84, 86, 87, 90–97, 99–101, 103–107, 110, 111, 113, 114, 116, 117, 120, 122, 124, 125, 132–134, 139, 149, 150, 152, 155, 156, 161, 164, 169, 171, 174, 179, 181–183, 192, 193, 201, 204, 205, 207, 210–214, 216, 217, 219–231, 233, 235–238, 240, 248, 250–254, 257, 259, 264, 267, 268, 273–277, 280–287, 292, 295, 309, 310, 313, 315–318, 328, 332, 334, 338–342, 357–359, 363, 364, 366, 373, 375, 377–382, 384–386, 388, 394–399, 402–413, 416–427, 429–431, 433–437, 439–445, 449–459, 461–466, 468, 469, 472–476, 478–480, 482–506, 508, 509, 511–517, 519–525, 527–531, 561, 583–585, 601–603, 692, 698, 705, 706, 719, 725, 733, 734, 741, 745, 748, 753, 757–761, 770, 772, 783, 828, 829, 880, 881, 889–891, 898–902, 904–907, 909–919

## construct selector set

A selector set that may match the construct trait set. 321, 318, 321–323, 329, 330

## construct trait set

The trait set that, at a given point in an OpenMP program, consists of all enclosing constructs up to an enclosing target construct. 318, 36, 37, 318, 319, 321, 323, 341

## containing array

For C/C++, a non-subscripted array (a containing array) to which a series of zero or more array subscript operators and, when specified, dot (i.e., ’.’) operators are applied to yield a given lvalue expression or array section for which storage is contained by the array. For Fortran, an array (a containing array) without the POINTER attribute and without a subscript list to which a series of zero or more array subscript selectors and, when specified, component selectors are applied to yield a given variable or array section for which storage is contained by the array.

COMMENT: An array is a containing array of itself. For the array section (\*p0).x0[k1].p1->p2[k2].x1[k3].x2[4][0:n], where identifiers pi have a pointer type declaration and identifiers xi have an array type declaration, the containing arrays are: (\*p0).x0[k1].p1->p2[k2].x1 and (\*p0).x0[k1].p1->p2[k2].x1[k3].x2.

26, 27, 36, 165, 283, 286

## containing structure

For C/C++, a structure to which a series of zero or more . (dot) operators and/or array subscript operators are applied to yield a given lvalue expression or array section for which storage is contained by the structure. For Fortran, a structure to which a series of zero or more component selectors and/or array subscript selectors are applied to yield a given variable or array section for which storage is contained by the structure.

COMMENT: A structure is a containing structure of itself. For C/C++, a structure pointer p to which the -> operator applies is equivalent to the application of a . (dot) operator to $( ^ { * } p )$ for the purposes of determining containing structures.

For the array section (\*p0).x0[k1].p1->p2[k2].x1[k3].x2[4][0:n], where identifiers pi have a pointer type declaration and identifiers xi have an array type declaration, the containing structures are: \*(\*p0).x0[k1].p1, (\*(\*p0).x0[k1].p1).p2[k2] and (\*(\*p0).x0[k1].p1).p2[k2].x1[k3] 27, 36, 37, 212, 279, 282, 283, 286, 287

## contention group

All implicit tasks and their descendent tasks that are generated in an implicit parallel region, R, and in all nested regions for which R is the innermost enclosing implicit parallel region. 3–6, 21, 28, 64, 81, 94, 100, 116, 117, 130, 134, 141, 301, 306, 360, 387, 393, 453, 473, 494, 534, 535, 571, 584, 585, 601, 602, 663, 891, 899, 90

## context-matching construct

A construct that has the context-matching property. 321

## context-matching property

The property that a directive adds a trait of the same name to the construct trait set of the current OpenMP context. 37, 337, 384, 394, 399, 416, 417, 460

## context selector

The specification of traits that a directive variant or function variant requires in the current OpenMP context in order for that variant to be selected. 320, 33, 48, 98, 320–325, 328, 329, 331, 335–337, 355, 889, 906

## context-specific structured block

Structured blocks that conform to specific syntactic forms and restrictions that are required for certain block-associated directives. 186, 21, 25, 54, 187, 188

## core

A physically indivisible hardware execution unit on a device onto which one or more hardware threads may be mapped via distinct execution contexts. 63, 76, 98, 128, 726

## corresponding list item

For a privatization clause, a new list item that derives from an original list item. For a data-mapping attribute clause, a list item in a device data environment that corresponds to an original list item. 68, 69, 231, 238, 239, 273, 280, 282–289, 295, 296, 298, 316, 346, 361, 461, 466, 610, 899

## corresponding pointer

For a given pointer variable or a given referring pointer, the corresponding variable or handle that exists in a device data environment. 82, 284, 287, 288

## corresponding pointer initialization

For a given data entity that has a base pointer or referring pointer, an assignment to the base pointer or referring pointer such that any lexical reference to the data entity or a subobject of the data entity in a target region refers to its corresponding data entity or subobject in the device data environment. 284, 461

## corresponding storage

For a given storage block, its corresponding storage block. For a given mapped variable, the corresponding storage of its original storage block. 38, 70, 84, 95, 236, 275, 281, 282, 284–287, 296, 463, 605, 739, 891

## corresponding storage block

A storage block that contains the storage of one or more variables in a device data environment that corresponds to mapped variables in an original storage block. 8, 9, 38, 69, 283, 284

## C pointer

For C/C++, a base language pointer variable. For Fortran, a variable of type C\_PTR. 45, 111, 236

## current device

The device on which the current task is executing. 8, 10, 21, 23, 45, 57, 72, 102, 145, 319, 435, 451, 535, 577, 580, 583, 630, 647, 654, 655, 683–685, 789, 800

## current task

For a given thread, the task corresponding to the task region that it is executing. 38, 49, 57, 280, 305, 332, 478, 479, 568, 570–573, 576, 577, 580, 589, 592, 593, 598, 678

## current task region

The region that corresponds to the current task. 5, 104, 399, 427, 446, 475, 479, 520, 521, 860

## current team

All threads in the team executing the innermost enclosing parallel region. 28, 82, 94, 104, 106, 117, 214, 399, 402, 403, 405–407, 409, 414, 435, 442, 446, 475, 478, 479, 514, 515, 520, 524, 579, 590, 733

## current team tasks

All tasks encountered by the corresponding team. The implicit tasks constituting the parallel region and any descendent tasks encountered during the execution of these implicit tasks are included in this set of tasks. 28, 306

## D

## data-copying property

The property that a clause copies a list item from one data environment to other data environments. 271, 272

## data entity

For C/C++, a data object that is referenced by a given lvalue expression or array section. For Fortran, a data entity as defined by the base language. 25–27, 38–40, 44, 55, 56, 58, 60, 87, 90, 96, 106, 111, 328

## data environment

The variables associated with the execution of a given region. 4, 6, 8, 9, 21, 39, 40, 43, 48, 57, 70, 73, 76, 82, 102, 115–117, 121, 124, 125, 210, 236, 257, 273, 280, 295, 426, 429, 436, 445, 454, 456, 461, 466, 603, 799, 904, 914

## data-environment attribute

A data-sharing attribute or a data-mapping attribute. 39, 210

## data-environment attribute clause

A clause that explicitly determines the data-environment attributes of the list items in its list argument. 210, 39, 215, 292, 347, 401, 436, 437, 445

## data-environment attribute property

The property that a clause is a data-environment clause. 224, 225, 227, 229, 232, 235–238, 252, 255–257, 279, 289, 290, 299, 300, 303, 315

## data-environment clause

A clause that is a data-environment attribute clause or otherwise afects the data environment. 210, 39, 210, 444

## data-mapping attribute

The relationship of a data entity in a given device data environment to the version of that entity in the enclosing data environment. 210, 39, 51, 58, 213, 276, 292, 910

## data-mapping attribute clause

A clause that explicitly determines the data-mapping attributes of the list items in its list argument. 210, 8, 37, 40, 51, 76, 276, 289, 316, 454, 456, 461, 898

## data-mapping attribute property

The property that a clause is a data-mapping clause. 279, 289

## data-mapping clause

A clause that is a data-mapping attribute clause or otherwise afects the data environment of the target device. 210, 39, 70, 210

## data-mapping construct

A construct that has the data-mapping property. 48, 69, 212, 275, 283, 284, 459

## data-mapping property

The property of a construct on which a data-mapping attribute clause may be specified. 40, 454, 456, 458, 460

## data-motion attribute

The data-movement relationship between a given device data environment and the version of that data entity in the enclosing data environment. 33, 295

## data-motion attribute property

The property that a clause is a data-motion clause. 297, 298

## data-motion clause

A clause that specifies data movement between a device set that is specified by the construct on which it appears. 23, 33, 40, 278, 293–296, 298, 466, 906

## data race

A condition in which diferent threads access the same memory location such that the accesses are unordered and at least one of the accesses is a write. Data races produce unspecified behavior. 8, 2, 8, 9, 13, 14, 40, 225, 227, 231, 251, 259, 273, 284, 296, 308, 402, 420, 496

## data-sharing attribute

For a given data entity in a data environment, an attribute that determines the scope in which the entity is visible (i.e., its name provides access to its storage) and/or the lifetime of the entity. A variable that is part of an aggregate variable cannot have a particular data-sharing attribute independent of the other components, except for static data members of C++ classes. 210, 39, 40, 44, 51, 52, 55, 56, 58, 60, 62–64, 86, 87, 90, 96, 106, 111, 210, 212–214, 222, 224, 276, 292, 454, 456, 458, 461, 466, 528, 888, 910

## data-sharing attribute clause

A clause that explicitly determines the data-sharing attributes of the list items in its list argument. 210, 7, 21, 41, 51, 82, 160, 210, 213, 219, 221–223, 225, 239, 313, 316, 424, 426, 429, 461, 463, 530, 898, 912

## data-sharing attribute property

The property that a clause is a data-sharing clause. 224, 225, 227, 229, 232, 235–238, 252, 255–257, 315, 445

## data-sharing clause

A clause that is a data-sharing attribute clause. 210, 41, 210, 212, 213

## declaration-associated directive

A declarative directive for which its associated base language code is a procedure declaration. 153, 152–155, 334, 341, 347, 348, 900

## declaration sequence

For C/C++, a sequence of base language declarations, including definitions, that appear in the same scope. The sequence may include other directives that are associated with the declarations. 336, 349, 369

## declarative directive

A directive that may only be placed in a declarative context and results in one or more declarations only; it is not associated with the immediate execution of any user code or implementation code. 41, 51, 60, 112, 152, 153, 155, 156, 161, 215, 260, 263, 293, 301, 310, 334, 336, 341, 346, 349, 363, 450, 897

## declare target directive

A declarative directive that has the declare-target property. 8, 69, 76, 212, 240, 276, 287, 301, 318, 345–347, 349, 351, 356, 360, 361, 461, 463, 564, 889, 904, 910

## declare-target property

The property that a directive applies to procedures and/or variables to ensure that they can be executed or accessed on a device. 41, 346, 349

## declare variant directive

A declarative directive that declares a function variant for a given base function. 48, 318, 328–330, 336, 338, 889, 906, 910

## default mapper

The mapper that is used for a map clause for which the mapper modifier is not explicitly specified. 86, 278

## defined

For variables, the property of having a valid value. For C, for the contents of variables, the property of having a valid value. For C++, for the contents of variables of POD (plain old data) type, the property of having a valid value. For variables of non-POD class type, the property of having been constructed but not subsequently destructed. For Fortran, for the contents of variables, the property of having a valid value. For the allocation or association status of variables, the property of having a valid status.

COMMENT: Programs that rely upon variables that are not defined are non-conforming programs.

42, 109, 131, 146, 916

## delimited directive

A directive for which the associated base language code is explicitly delimited by the use of a required paired end directive. 154, 152, 155, 327, 336, 349, 369

## dependence

An ordering relation between two instances of executable code that must be enforced by a compliant implementation. 504, 42, 47, 103, 181, 435, 504–509, 512, 514, 515, 604, 715, 756, 761, 762

## dependence-compatible task

Two tasks between which a task dependence may be established. 507, 86, 103, 108, 504, 508, 509, 511, 559

## dependent task

A task that because of a task dependence cannot be executed until its antecedent tasks have completed. 507, 22, 100, 103, 448, 458, 480, 502–504, 507–509, 604, 741, 762

## depend object

An OpenMP object that supplies user-computed dependences to depend clauses. 558, 181, 435, 481, 505, 506, 508, 509, 604, 760, 761, 911

## deprecated

For a construct, clause, or other feature, the property that it is normative in the current specification but is considered obsolescent and will be removed in the future. Deprecated features may not be fully specified. In general, a deprecated feature was fully specified in the version of the specification immediately prior to the one in which it is first deprecated. In most cases, a new feature replaces the deprecated feature. Unless otherwise specified, whether any modifications provided by the replacement feature apply to the deprecated feature is implementation defined. 42, 156, 157, 260, 533, 603, 710, 713, 737, 778, 781, 783, 784, 885, 896, 903–905, 907, 909, 911

## descendent task

A task that is the child task of a task region or of a region that corresponds to one of its descendent tasks. 37, 38, 42, 430, 448, 502, 521

## detachable task

An explicit task that only completes after an associated event variable that represents an allow-completion event is fulfilled and execution of the associated structured block has completed. 445, 426, 437, 502, 503, 538, 590, 910

## device

An implementation-defined logical execution engine.

COMMENT: A device could have one or more processors.

3, 4, 7–9, 19, 21–23, 28, 32, 37, 38, 40, 41, 43–46, 48, 53, 56, 59, 71, 75, 76, 79, 83, 84, 98, 100, 102, 103, 109, 115–117, 124, 127, 128, 139–141, 145, 181, 237, 274, 280, 289, 290, 295, 296, 303, 306–308, 318, 319, 321, 323, 332, 345, 346, 359, 360, 436, 450, 453, 455, 457, 461–463, 466, 494, 536, 564, 571, 590, 592, 594–597, 599–603, 605–607, 610–613, 618, 619, 630–634, 645, 647–652, 654, 655, 683, 689, 690, 692, 704–706, 708, 710, 711, 717, 722, 726, 744, 772–776, 778, 779, 785–787, 793, 800, 801, 803–810, 812–814, 819, 822, 826, 833, 836, 842, 846, 850–853, 857, 879, 883, 885, 889, 891, 894, 897, 899, 900, 902, 903, 906, 907, 909, 911–913

## device address

An address of an object that may be referenced on a target device. 8, 8, 45, 62, 111, 235–238, 328, 332, 359, 360, 607, 885, 906, 909

## device-affecting construct

A construct that has the device-afecting property. 462, 600, 602, 917

## device-affecting property

The property that a device construct can modify the state of the device data environment of a specified target device. 43, 454, 456, 458, 460, 465

## device-associated property

The property of a clause that a device must be associated with the construct on which it appears. 235–238

## device construct

A construct that has the device property. 2, 43–45, 56, 62, 102, 111, 141, 286, 355, 356, 451, 736, 760, 781, 785, 908, 913

## device data environment

The initial data environment associated with a device. 8, 8, 9, 25, 37–40, 43, 56, 68–72, 84, 87, 111, 124, 210, 235–239, 257, 274, 275, 280–290, 295, 296, 332, 345, 361, 454, 456, 461, 463, 464, 466, 599, 601, 602, 605, 607, 608, 610, 612, 618, 779, 885, 898, 902

## device global requirement clause

A requirement clause that has the device global requirement property. 355

## device global requirement property

The property that a requirement clause indicates requirements for the behavior of device constructs that a program requires the implementation to support across all compilation units. 44, 356, 358–362

## device-information property

The property of a routine that it provides or modifies information about a specified device that supports use of the device in an OpenMP program. 592, 44, 592–599, 601

## device-information routine

A routine that has the device-information property. 592, 592

## device-local attribute

For a given device, a data-sharing attribute of a data entity that it has static storage duration and is visible only to tasks that execute on that device. 303, 44, 211, 214

## device-local variable

A variable that has the device-local attribute with respect to a given device. 303, 8, 286, 345, 361, 885

## device-memory-information routine

A routine that has the device-memory-information routine property. 604, 603

## device-memory-information routine property

The property of a device memory routine that it enables operations on memory that is associated with the specified devices but does not itself directly operate on that memory. 604, 44, 604–606

## device memory routine

A device routine that has the device memory routine property. 603, 44, 102, 564, 603, 604, 779, 888, 913

## device memory routine property

The property that a device routine operates on or otherwise enables operations on memory that is associated with the specified devices. 603, 44, 604–606, 608, 609, 611, 613–615, 617, 619, 620

## device number

A number that the OpenMP implementation assigns to a device or otherwise may be used in an OpenMP program to refer to a device. 7, 7, 35, 115, 116, 119, 120, 127, 139–141, 308,

451, 461, 542, 593, 594, 596, 598–602, 610, 612, 689, 692, 773–775, 779, 781, 800, 902

## device pointer

An implementation defined handle that refers to a device address and is represented by a C pointer. 8, 63, 111, 235, 236, 328, 332, 359, 604, 606–608, 610–613, 654, 885, 907

## device procedure

A procedure that can be executed on a target device, as part of a target region. 102, 291, 345, 355, 356, 360, 361

## device property

The property of a construct that it accepts the device clause. 43, 346, 349, 454, 456, 458, 460, 465, 468

## device region

A region that corresponds to a device construct. 715, 722, 744, 778, 781, 783, 785

## device routine

An OpenMP API routine that may require access to one or more specified devices. 24, 44, 141

## device selector set

A selector set that may match the device trait set. 321, 321–323

## device-specific environment variable

An alternative OpenMP environment variable that controls the behavior of the program only with respect to a particular device or set of devices. 119, 120, 127, 139, 906

## device-tracing callback

A callback that has the device-tracing property. 772

## device-tracing entry point

An entry point that has the device-tracing property. 772, 773

## device-tracing property

The property that an entry point or callback is part of the OMPT tracing interface and, so, is used to control the collection of trace records on a device. 772, 45, 772–777, 780, 782, 784

## device trait set

The trait set that consists of traits that define the characteristics of the device that the compiler determines will be the current device during program execution at a given point in the OpenMP program. 319, 45, 318, 319

## device-translating callback

A callback that has the device-translating property. 842, 843, 844

## device-translating property

The property that a callback translates data between the formats used for the device on which the third-party tool and OMPD library run and the device on which the OpenMP program runs. 842, 46, 843

## directive

A base language mechanism to specify OpenMP program behavior. 2, 3, 6–9, 13, 15, 17, 21, 22, 24, 25, 29–31, 33–35, 37, 41, 42, 46–50, 54, 57, 60, 64, 68, 69, 73, 79, 80, 89, 91, 95, 100, 103, 107, 109, 111, 112, 114, 116, 127, 143, 148–157, 159–166, 168, 171, 174, 182, 183, 187, 188, 190–192, 198, 201–208, 210, 211, 213–215, 217–220, 222, 225, 230, 233, 234, 247–249, 254, 257, 260, 261, 263–265, 267–270, 276, 278, 280, 283, 284, 289–294, 300–304, 306, 307, 311–316, 318, 319, 321, 322, 324–328, 335–339, 341–343, 345, 347–357, 359, 362, 363, 368–373, 379, 382, 385, 388, 389, 395, 399, 402, 409–411, 424, 426, 429, 431, 434, 445, 451, 452, 454–458, 461, 463, 465, 466, 469, 470, 474, 481–483, 488, 496, 500–503, 505, 519, 523, 524, 527, 535, 561, 564, 608, 645, 646, 652, 653, 655, 663, 744, 748, 887–890, 896–902, 904–907, 909, 910, 912, 914, 915, 917

## directive name

The name of a directive or a corresponding construct. 34, 35, 46, 47, 64, 150, 162, 173, 174, 179, 180, 182, 206, 223, 225–227, 230, 232, 235–238, 252, 255, 256, 258, 262, 263, 265, 266, 269–272, 280, 289–291, 297–300, 303, 309, 310, 313, 316, 325, 326, 330, 331, 333, 339, 340, 344, 350, 353, 354, 357–367, 372, 374, 376, 378, 382, 383, 388, 392, 393, 397, 398, 400–403, 418, 422, 425, 432, 433, 439–445, 450–452, 470, 472, 481, 483–489, 491–493, 506, 507, 511, 512, 517–519, 525, 52

## directive-name list

An argument list that consists of directive-name list items. 162

## directive-name list item

A list item that is a directive name. 162, 46

## directive-name separator

Characters used to separate the directive names of leaf constructs in a compound-directive name. A directive-name separator is either white space or, in Fortran, a plus sign (i.e., ’+’); a given instance of a compound-directive name must use the same character for all directive-name separators. 525, 46, 525–527

## directive specification

The directive specifier and list of clauses that specify a given directive. 150, 47, 150, 162

## directive-specification list

An argument list that consists of directive-specification list items. 162

## directive-specification list item

A list item that is a directive specification. 162, 47, 164

## directive specifier

The directive name and, where permitted, the directive arguments that are specified for a given directive. 150, 46

## directive variant

A directive specification that can be used in a metadirective. 324, 37, 92, 324–327, 910

## divergent threads

Two threads are divergent if one executes a diverging code path and the other does not due to a conditional statement. 7, 47, 362

## diverging code path

For a given pair of threads, the region of a structured block sequence that is executed by only one of the threads. 6, 47

## doacross-affected loop

For a worksharing-loop construct in which a stand-alone ordered directive is closely nested, a loop that is afected by its ordered clause. 48, 207, 371, 514, 900

## doacross dependence

A dependence between executable code corresponding to stand-alone ordered regions from two doacross iterations: the sink iteration and the source iteration, where the source iteration precedes the sink iteration in the doacross iteration space. The doacross dependence is fulfilled when the executable code from the source iteration has completed. 504, 47, 98, 512, 514, 715

## doacross iteration

A logical iteration of a doacross loop nest. 47, 98, 503, 504, 512, 514

## doacross iteration space

The logical iteration space of a doacross loop nest. 47, 512

## doacross logical iteration

A doacross iteration. 512

## doacross loop nest

The doacross-afected loops of a worksharing-loop construct in which a stand-alone ordered construct is closely nested. 47, 512, 514, 912, 913

## dynamic context selector

Any context selector that is not a static context selector. 337

## dynamic replacement candidate

A replacement candidate that may be selected at runtime to replace a given metadirective. 324, 324, 325, 329

## dynamic storage duration

For C/C++, the lifetime of an object with dynamic storage duration, as defined by the base language. For Fortran, the lifetime of a data object that is dynamically allocated with the ALLOCATE statement or some other language mechanism. 211, 214

## dynamic trait set

The trait set that consists of traits that define the dynamic properties of an OpenMP program at a given point in its execution. 319, 111, 318, 320, 321

## E

## effective context selector

The resulting context selector that must be satisfied for a given function variant to be selected, as determined by the match clauses of all begin declare\_variant directives that delimit a base language code region that encloses the declare variant directive. 336, 336, 337

## effective map clause set

The set of all map clauses that apply to a data-mapping construct, including any implicit map clauses and map clauses applied by mappers. 283, 283, 284

## enclosing context

For C/C++, the innermost scope enclosing a directive. For Fortran, the innermost scoping unit enclosing a directive. 48, 73, 82, 96, 213, 214, 252–254, 259, 261, 264, 273, 324, 340, 341, 408, 410, 413, 421, 910

## enclosing data environment

For a given directive, the data environment of its enclosing context. 39, 40, 52, 56, 63, 94, 111, 436, 437

## encountering device

For a given construct, the device on which the encountering task of the construct executes. 236, 284, 295, 298, 463, 891

## encountering task

For a given region, the current task of the encountering thread. 6, 48, 49, 103, 295, 334, 339, 352, 385, 394, 395, 414, 427, 431, 436, 442, 445, 462, 468, 476, 477, 480, 482, 520–522, 535, 579, 587, 588, 670, 673–677, 706, 744, 759, 760, 781, 798, 799, 880, 881

## encountering-task binding property

The binding property that the binding thread set is the encountering task. 534

## encountering thread

For a given region, the thread that encounters the corresponding construct, structured block sequence, or routine. 4, 5, 28, 49, 59, 91, 252, 384, 389–391, 394, 403, 423, 425–427, 461, 469, 499, 505, 535, 578, 579, 589, 594, 681, 683, 685–687, 689, 695, 725, 770, 786, 791, 793–795, 798, 800, 902

## encountering-thread binding property

The binding property that the binding thread set is the encountering thread. 534

## end-clause property

The property that a clause may appear on an end directive. 150, 272, 481

## end directive

For a given directive, a paired directive that lexically delimits the code associated with that directive. 150, 35, 42, 49, 150, 152, 153, 155, 156, 160, 187, 188, 192, 327, 336, 337, 349, 350, 474, 904, 905

## ending address

The address of the last storage location of a list item or, for a mapped variable, of its original list item. 51, 70, 281

## entry point

A runtime entry point. 24, 45, 79, 700, 701, 703–706, 711, 720, 722, 729, 745, 772, 773, 776, 786–814, 894, 895, 903

## enumeration

A type or any variable of a type that consists of a specified set of named integer values. For C/C++, an enumeration type is specified with the enum specifier. For Fortran, an enumeration type is specified by either (1) a named integer constant that is used as the integer kind of a set of named integer constants that have unique values or (2) a C-interoperable enumeration definition. 49, 536, 539–541, 544, 547, 550, 554, 557–560, 562, 563, 565, 566, 711, 714, 716, 717, 720, 722–725, 727–731, 735, 736, 738–741, 743, 789, 825, 827, 828, 874

## environment variable

Unless specifically stated otherwise, an OpenMP environment variable. 2, 6, 118, 119, 127–137, 139–147, 692, 693, 872, 886, 887, 896, 897, 906, 908, 909, 912–915

## error termination

A fatal action preformed in response to an error. 6, 33, 93, 389, 900

## event

A point of interest in the execution of a thread or a task. 10, 11, 14, 15, 29, 43, 91, 102, 108, 250, 286, 346, 352, 385, 386, 394, 395, 403, 405–411, 413–415, 421, 426, 427, 430, 431, 437, 445–447, 449, 453, 455–457, 459, 462, 466, 474–478, 480, 496, 497, 500, 502, 503, 509, 513, 515, 516, 521, 522, 538, 586, 589, 590, 603, 604, 607–616, 618–621, 664–669, 671–677, 695, 697, 700, 703–705, 710, 726, 728–730, 741, 744, 746, 757–759, 761, 763–765, 767, 771, 772, 776, 778, 781, 783, 784, 786, 789, 790, 796, 805, 806, 808, 812, 813, 816, 878, 880, 881, 883, 894, 902

## exception-aborting directive

A directive that has the exception-aborting property. 366, 887

## exception-aborting property

For C++, the property of a directive that whether an exception that occurs in its associated region is caught or results in a runtime error termination is implementation defined. 50, 149, 460

## exclusive property

The property that a clause, an argument, or a modifier may not be specified when, (respectively), a diferent clause, argument or modifier is specified. When applied to a clause set, the property applies only to clauses within that set. 160, 33, 159–161, 232, 266, 313, 343, 381, 405, 426, 429, 484, 488, 519

## exclusive scan computation

A scan computation for which the value read does not include the updates performed in the same logical iteration. 270, 270, 909

## executable directive

A directive in an executable context that results in implementation code or prescribes the manner in which any associated user code must execute. 3, 35, 36, 60, 64, 67, 68, 98, 100, 112, 149, 152, 153, 155, 186, 198, 315, 324, 337, 352, 353, 374, 375, 377, 379–381, 384, 394, 399, 402, 405–407, 409, 412, 416, 417, 420, 423, 426, 429, 435, 446, 454, 456, 458, 460, 465, 468, 473, 475, 478, 479, 494, 498, 505, 514, 515, 520, 524

## explicit barrier

A barrier that is specified by a barrier construct. 475

## explicitly associated directive

A declarative directive for which its associated base language declarations are explicitly specified in a variable list or extended list argument. 153, 152, 153, 155, 215, 301, 310, 346

## explicitly determined data-mapping attribute

A data-mapping attribute that is determined due to the presence of a list item on a data-mapping attribute clause. 274

## explicitly determined data-sharing attribute

A data-sharing attribute that is determined due to the presence of a list item on a data-sharing attribute clause. 213, 210, 213, 224

## explicit region

A region that corresponds to either a construct of the same name or a library routine call tha explicitly appears in the program. 3, 3, 99, 149, 413, 446, 689, 802

## explicit task

A task that is not an implicit task. 5, 5, 7, 26, 30, 43, 51, 53, 83, 94, 103, 104, 116, 253, 254, 385, 389, 426, 427, 429–431, 447, 475, 503, 524, 586, 689, 719, 756, 798, 864, 910, 913, 916

## explicit task region

A region that corresponds to an explicit task. 8, 91, 225, 427, 527, 587, 903

## exporting task

A task that permits one of its child tasks to be an antecedent task of a task for which it is a preceding dependence-compatible task. 511, 108, 427, 437, 508, 511, 559
