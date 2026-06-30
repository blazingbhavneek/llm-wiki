# OpenMP-API-Specification Source Lines 1405-1922

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source OpenMP-API-Specification:L1405-L1922

Citation: [OpenMP-API-Specification:L1405-L1922]

````text
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
````
