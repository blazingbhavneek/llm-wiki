# OpenMP-API-Specification Source Lines 3411-4020

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source OpenMP-API-Specification:L3411-L4020

Citation: [OpenMP-API-Specification:L3411-L4020]

````text
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

## nested construct

A construct (lexically) enclosed by another construct. 210

## nested parallelism

A condition in which more than one level of parallelism is active at a point in the execution of an OpenMP program. 4, 908

## nested region

A region (dynamically) enclosed by another region. That is, a region generated from the execution of another region or one of its nested regions. 3, 37, 76, 84, 369, 404

## new list item

An instance of a list item created for the data environment of the construct on which a privatization clause or a data-mapping attribute clause specified. 219, 37, 87, 111, 219–221, 226–228, 230, 233, 235, 236, 258, 267, 283–285, 916

## NUMA domain

A device partition in which the closest memory to all cores is the same memory and is at a similar distance from the cores. 128

## non-negative property

The property that an expression, including one that is used as the argument of a clause, a modifier or a routine, has a value that is greater than or equal to zero. 161, 119, 130, 131, 133, 140, 142–144, 160, 163, 204, 305, 322, 378, 384, 394, 443, 541, 575, 582, 600, 636, 680, 695, 771, 793, 794, 892, 893

## non-conforming program

An OpenMP program that is not a conforming program. 2, 34, 42, 110, 214, 217, 429, 448, 505, 663, 900

## non-host declare target directive

A declare target directive that does not specify a device\_type clause with host. 345

## non-host device

A device that is not the host device. 7, 19, 26, 100, 117, 119, 120, 127, 139, 140, 329, 359, 362, 385, 425, 450, 464, 594, 690, 692, 850, 851, 857, 889, 896

## non-null pointer

A pointer that is not NULL. 622, 698, 700, 704, 745, 746, 813

## non-null value

A value that is not NULL. 655, 731, 797, 798, 818, 836, 837, 839, 871

## non-property trait

A trait that is specified without additional properties. 318, 319, 323

## nonrectangular-compatible property

The property that the transformation defined by a loop-transforming construct is compatible with non-rectangular loops and therefore will not yield a non-conforming canonical loop nest due to their presence. 371, 372, 375

## non-rectangular loop

For a loop nest, a loop for which a loop bound references the iteration variable of a surrounding loop in the loop nest. 76, 200, 202, 205, 207, 234, 259, 372, 376, 380, 381, 420, 423, 433, 909

## non-sequentially consistent atomic construct

An atomic construct for which the seq\_cst clause is not specified 13

## NULL

A null pointer. For C/C++, the value NULL or the value nullptr. For Fortran, the disassociated pointer for variables that have the POINTER attribute or the value C\_NULL\_PTR for variables of type C\_PTR. 76, 145, 332, 590, 597, 605–609, 611, 612, 618, 627, 628, 654, 655, 661, 684, 686, 687, 695, 698, 700, 704, 744, 757, 758, 763, 764, 771, 773, 774, 779, 781, 787, 789, 790, 795–799, 818, 836, 837, 839, 844, 872, 894

## numeric abstract name

An abstract name that refers to a quantity associated with a conceptual abstract name. 128, 19, 85, 128–130, 134, 897

## O

## offsetting loop

The outer generated loops of a stripe construct that determine the ofsets within the grid cells used for each execution of the grid loops. 379, 379, 380, 889

## OMPD

An interface that helps a third-party tool inspect the OpenMP state of a program that has begun execution. 816, 2, 14, 15, 77, 108, 116, 146, 184, 185, 816–818, 820, 822, 824, 827–829, 833, 836, 841, 845–849, 855, 878

## OMPD callback

A callback that has the OMPD property. 184, 185, 823, 826, 827, 831, 833, 836, 837, 839, 841

## OMPD library

A dynamically loadable library that implements the OMPD interface. 816, 15, 46, 816–823, 826, 829–831, 833–839, 841–851, 853, 867, 870, 872, 874, 876

## OMPD property

The property that a callback, routine or type is included in OMPD and its namespace, which implies it has the ompd\_ prefix. 77, 78, 819, 820, 822–832, 834, 835, 837–849, 851–869, 871–873, 875–877

## OMPD routine

A routine that has the OMPD property. 826, 827, 831, 845–850, 855, 856, 858–862, 875–877

## OMPD type

A type that has the OMPD property. 184, 33, 56, 81, 83, 184, 185, 819–824, 826–837, 839, 841–844

## OMPT

An interface that helps a first-party tool monitor the execution of an OpenMP program. 697, 2, 14, 45, 78, 98, 144, 146, 185, 476, 565, 690, 697–701, 703–706, 722, 725, 727, 733, 744–746, 772, 786, 787, 802, 803, 812, 813, 877, 894, 903

## OMPT active

An OMPT interface state in which the OpenMP implementation is prepared to accept runtime calls from a first-party tool and will dispatch any registered callbacks and in which a first-party tool can invoke runtime entry points if not otherwise restricted. 695, 700, 707

## OMPT callback

A callback that has the OMPT property. 185, 703, 711, 713, 744, 787, 802

## OMPT inactive

An OMPT interface state in which the OpenMP implementation will not make any callbacks and in which a first-party tool cannot invoke runtime entry points. 695, 699, 700, 745

## OMPT interface state

A state that indicates the permitted interactions between a first-party tool and the OpenMP implementation. 78, 695, 699, 700, 707, 745

## OMPT pending

An OMPT interface state in which the OpenMP implementation can only call functions to initialize a first-party tool and in which a first-party tool cannot invoke runtime entry points. 699, 700

## OMPT property

The property that a callback, runtime entry point or type is included in OMPT and its namespace, which implies it has the ompt\_ prefix. 78, 79, 697, 698, 708, 710–712, 714–732, 734–743, 745–753, 755–757, 759–770, 772–777, 780, 782, 784, 786–797, 799–801, 803–814

## OMPT-tool finalizer

An implementation of the finalize callback. 707, 446, 698, 746

## OMPT-tool initializer

An implementation of the initialize callback. 697, 446, 698, 700, 703, 745

## OMPT type

A type that has the OMPT property. xxvii, 184, 33, 56, 81, 83, 185, 415, 697, 698, 700, 703, 705–708, 710, 711, 713–731, 733, 735–738, 740–743, 745–751, 753, 754, 756–776, 778, 779, 781, 783–785, 787–796, 798–814, 824, 830, 864, 870, 877, 894, 896, 903, 905, 908

## once-for-all-constituents property

The property that a clause applies once for all constituent constructs to which it applies when it appears on a compound construct. 159, 205, 206, 528

## opaque property

The property that an OpenMP type is opaque, which implies that objects of that type may only be accessed, modified and destroyed through OpenMP directives, routines, callbacks and entry points. Further, an object of an opaque type can be copied without afecting, or copying, its underlying state. Destruction of an OpenMP object, which by definition has an opaque type, destroys the state to which all copies of the object refer. All handles have opaque types. 79, 538, 539, 553, 558–560, 623–628, 710, 717, 772, 776, 811–813, 840, 849–853, 857, 858, 860, 863, 865–873, 875–877

## opaque type

A type that has the opaque property. 62, 79, 80, 538, 539, 553, 558–560

## OpenMP Additional Definitions document

A document that exists outside of the OpenMP specification and defines additional values that may be used in a conforming program. The OpenMP Additional Definitions document is available via https://www.openmp.org/specifications/. 79, 140, 319, 469, 539, 541

## OpenMP API routine

A runtime library routine that is defined by the OpenMP implementation and that can be called from user code via the OpenMP API. 45, 80, 93, 115, 127, 240, 359, 360, 367, 533, 586, 630, 688, 694, 892

## OpenMP architecture

The architecture on which a region executes. 80, 699

## OpenMP context

The execution context of an OpenMP program as represented by a set of traits, including active constructs, execution devices, OpenMP functionality supported by the implementation and any available dynamic values. 318, 33, 37, 98, 183, 318, 320, 321, 323–325, 328–331, 335, 337, 341, 355, 541, 889, 906

## OpenMP environment variable

A variable that is part of the runtime environment in which an OpenMP program executes and that a user may set to control the behavior of the program, typically through the initialization of an ICV. 127, 45, 50, 115, 120, 127, 872, 914

## OpenMP identifier

An identifier that has a specialized purpose for use in OpenMP programs, as defined by this specification. 183, 60, 70, 86, 90, 93, 159, 164, 183, 185, 241–244

## OpenMP lock variable

A lock. 663

## OpenMP object

Any object of an opaque type that allows programmers to save, to manipulate and to use state related to the OpenMP API. 42, 62, 71, 72, 79, 505, 773, 776, 803, 811, 813

## OpenMP operation

When used as a list item, a special expression that returns an object of a specified OpenMP types. Otherwise, an operation that is applied to a list item according to the semantics of a directive, clause, or modifier. 165, 60, 61, 80, 90, 162, 165, 183, 333, 406, 499

## OpenMP operation list

An argument list that consists of OpenMP operation list items. 162, 165

## OpenMP operation list item

A list item that is an OpenMP operation. 162, 80

## OpenMP process

A collection of one or more native threads and address spaces. An OpenMP process may contain native threads and address spaces for multiple OpenMP architectures. At least one native thread in an OpenMP process is mapped to an OpenMP thread. An OpenMP process may be live or a core file. 20, 80, 819, 820, 829, 836, 845, 846, 849, 850

## OpenMP program

A program that consists of a base program that is annotated with OpenMP directives or that calls OpenMP API routines. 3, 5–9, 13, 14, 19, 21, 22, 26, 32, 35, 36, 44–46, 48, 55–58, 62, 72, 75, 76, 78–80, 91, 93, 108, 110, 115, 117, 127, 138, 148, 149, 164, 183, 214, 217, 222, 233, 251, 289, 293, 294, 304, 305, 318–320, 325, 360, 370, 395, 404, 443, 463, 464, 472, 473, 497, 499, 505, 582, 585, 592, 600, 602, 612, 663, 678, 688, 690, 691, 694, 695, 697, 699, 700, 703, 720, 721, 744, 771, 789, 796, 801, 802, 808, 816–818, 821, 826, 829, 835, 837, 839, 842–844, 878, 885, 915, 917

## OpenMP property

The property that a routine, callback or type is in the OpenMP namespace, which implies it has the omp\_ prefix. 81, 536–542, 544, 545, 547, 548, 550, 552–554, 556–558, 560, 562, 563, 565, 566, 573, 574, 623–628, 631–636, 638–642, 644, 646, 648–652, 656–661, 664–671, 673–676, 694

## OpenMP stylized expression

A base language expression that is subject to restrictions that enable its use within an OpenMP implementation. 32, 33, 60, 61, 159, 185, 240

## OpenMP thread

A logical execution entity with a stack and associated thread-specific memory subject to the semantics and constraints of this specification and may be implemented upon a native thread. 5–7, 22, 56, 75, 80, 84, 105–107, 132, 134, 136, 568, 777, 851, 854–858, 860, 863, 871, 878, 890

## OpenMP thread pool

The set of all threads that may execute a task of a contention group and, thus, are ever available to be assigned to a team that executes implicit tasks of the contention group, 3, 5, 22, 93, 94, 106, 442, 448

## OpenMP type

A type that has the OpenMP property or a type that is an OMPD type or an OMPT type. 183, 23, 33, 53, 56, 62, 79, 80, 82, 83, 159, 162, 163, 165, 181–185, 204, 334, 376, 469, 509, 519, 533, 534, 536, 538, 539, 541, 543–545, 547, 549, 552–556, 558–567, 622, 771, 892, 905, 907

## optional property

The property that a clause, a modifier or an argument is optional and thus may be omitted. If any argument of a routine has the optional property then the routine has the overloaded property. 81, 157–159, 163, 206, 270, 325, 326, 334, 341, 343, 344, 346, 350, 357–362, 365–367, 372, 382, 383, 393, 418, 422, 439, 440, 473, 481, 483–492, 498, 511, 517, 518, 535, 616, 617, 620, 623–625

## order-concurrent-nestable construct

A construct that has the order-concurrent-nestable property. 398, 917

## order-concurrent-nestable property

The property that a construct or routine generates a region that may be a strictly nested region of a region that was generated by a construct on which an order clause with an ordering argument of concurrent is specified. 81, 374, 375, 377, 379–381, 384, 399, 423, 494

## order-concurrent-nestable routine

A routine that has the order-concurrent-nestable property. 398, 917

## original list item

The instance of a list item in the data environment of the enclosing context. 37, 49, 51, 69, 70, 82, 98, 215, 219–221, 225, 227–231, 233, 235–237, 242, 247, 248, 250–254, 256–259, 267, 268, 271, 272, 280, 283–285, 288, 289, 295, 296, 298, 346, 361, 418, 420, 422, 444, 466, 899, 916

## original list-item updating clause

A clause that has the original list-item updating property 522

## original list-item updating property

The property that a clause includes an efect of updating the value of the original list item when the region for which it is specified is completed. 82, 229, 252, 255, 257

## original pointer

An original list item that corresponds to a corresponding pointer. 284

## original storage

The storage of a given mapped variable. 8, 70, 95, 285, 286, 739

## original storage block

A storage block that contains the storage of one or more mapped variables in a data environment. 8, 9, 38, 283

## original variable

For a variable that is referenced in the structured block that is associated with a block-associated directive that accepts data-sharing attribute clauses, the variable by the same name that exists immediately outside the construct. 7, 7

## orphaned construct

A construct that gives rise to a region for which the binding thread set is the current team, but is not nested within another construct that gives rise to the binding region. 515

## outermost-leaf property

The property that a clause applies to the outermost leaf construct that permits it when it appears on a compound construct. 159, 237, 271, 481, 483, 528

## output map type

The map type that results when map-type decay is applied to an input map type. 275, 61, 70, 109, 275, 281

## overlapping type name

An OpenMP type for which its name has the overlapping type-name property. 754

## overlapping type-name property

The property that an OpenMP type name is used for both an ordinary OpenMP type (possibly an OMPD type or an OMPT type) and for a callback in the same name space; which type is intended should be apparent from the context in this document. 82, 717, 722, 735, 743, 752, 753, 762, 765, 766

## overloaded property

The property that a routine has an overloaded C++ interface. 81, 83, 655–661

## overloaded routine

A routine that has the overloaded property. 655, 661

## P

## parallel handle

A handle that refers to a parallel region. 831, 828, 858–860, 866, 868

## parallelism-generating construct

A construct that has the parallelism-generating property. 231, 367, 371, 526

## parallelism-generating property

The property that a construct enables parallel execution by generating one or more teams, explicit tasks, or SIMD instructions. 83, 384, 394, 399, 426, 429, 454, 456, 458, 460, 465

## parallel region

A region that has a set of associated implicit tasks and an associated team of threads that execute those tasks. 4, 5, 19, 23, 31, 38, 53, 59, 83, 85, 100, 103–105, 114, 116, 125, 132, 136, 273, 389, 402, 404–407, 409, 414, 423–426, 429, 475–478, 502, 527, 536, 568–570, 715, 722, 744, 758, 763, 764, 796–798, 827, 831, 854, 858–860, 863, 866, 894, 914, 916

## parameter list

An argument list that consists of parameter list items. 162

## parameter list item

A list item that identifies one or more parameters of a procedure. 162, 74, 83, 162, 163, 534

## parent device

For a given target region, the device on which the corresponding target construct was encountered. 257, 359, 451, 461

## parent thread

The thread that encountered the parallel construct and generated a parallel region is the parent thread of each thread that executes a task region that binds to that parallel

region. The primary thread of a parallel region is the same thread as its parent thread with respect to any resources associated with an OpenMP thread. The thread that encounters a target or teams construct is not the parent thread of the initial thread of the corresponding target or teams region. 4, 22, 83, 84

## partial tile

A tile that is not a complete tile. 381, 381

## partitioned construct

A construct that has the partitioned property. 404, 84, 526

## partitioned property

The property of a construct that it is a work-distribution construct for which any encountered user code in the corresponding region, excluding code from nested regions that are not closely nested regions, is executed by only one thread from its binding thread set. 84, 405, 407, 409, 412, 416, 417, 420, 423

## partitioned worksharing construct

A construct that is both a partitioned construct and a worksharing construct. 4, 84

## partitioned worksharing region

A region that corresponds to a partitioned worksharing construct. 917

## perfectly nested loop

A loop that has no intervening code between it and the body of its surrounding loop. The outermost loop of a loop nest is always perfectly nested. 198, 57, 268, 376, 379–381, 514, 916

## persistent self map

A self map for which the corresponding storage remains present in the device data environment, as if it has an infinite reference count. 360, 8, 885

## place

An unordered set of processors on a device. 130, 4, 61, 84, 85, 106, 116, 117, 128, 131–133, 389–393, 679–682, 792–794, 886, 890, 897

## place-assignment group

A logical group of places and positions from the place-assignment-var ICV that is used to define a set of assignments of threads to places according to a given thread afinity policy. 390, 390, 391

## place-count abstract name

A numeric abstract name that refers to a quantity associated with a place-list abstract name. 128

## place list

The ordered list that describes all OpenMP places available to the execution environment. 85, 131, 394, 679, 792, 886, 897

## place-list abstract name

A conceptual abstract name that refers to a set of hardware abstractions of a given category that may be used to specify each place in a place list. 128, 85, 128, 131

## place number

A number that uniquely identifies a place in the place list, with zero identifying the first place in the place list, and each consecutive whole number identifying the next place in the place list. 390, 390, 681, 682, 793, 794

## place partition

An ordered list that corresponds to a contiguous interval in the place list. It describes the places currently available to the execution environment for a given parallel region. 61, 106, 117, 391, 392

## pointer association query

A query to the association status of a pointer via comparison to zero in C/C++ or by calling the ASSOCIATED intrinsic with one argument in Fortran. 463

## pointer attachment

The process of making a pointer variable an attached pointer. 284, 25, 285

## pointer property

The property that a routine or callback either returns a pointer type in C/C++ and is an assumed-size array in Fortran or has an argument that has such a type. 535, 596, 597, 614, 616, 617, 620, 625–628, 631, 632, 636, 644, 648, 649, 680, 682–686, 698, 714, 726, 734, 745–753, 755–757, 759–762, 765, 766, 769, 770, 772, 774–777, 780, 782, 784, 786–788, 790–793, 795–797, 799, 800, 803–814, 834, 835, 837, 839–842, 844–846, 849–854, 856–873, 875–877

## pointer-to-pointer property

The property that a routine or callback either returns a pointer-to-pointer type in C/C++ or has an argument that has such a type. 535, 775, 782, 787, 788, 796, 797, 799, 800, 834, 840, 847, 849–851, 853, 854, 856–863, 870, 873, 876

## positive property

The property that an expression, including one that is used as the argument of a clause, a modifier or a routine, has a value that is greater than zero. 161, 129–131, 133–135, 160, 162, 206, 207, 300, 305, 306, 309, 313, 373, 374, 376, 383, 388, 393, 397, 401, 418, 422, 432, 433, 452, 546, 547, 568, 583, 584, 602, 605, 614, 617, 631, 632, 645, 648, 649, 734, 805, 886, 887, 889–893

## post-modified property

The property of a clause that its modifiers must appear after its arguments. 158, 159, 161, 223, 232, 291, 300

## preceding dependence-compatible task

For a given task, a dependence-compatible task that may be its antecedent task. 507, 51, 59, 507, 508

## predecessor task

For a given task, an antecedent task of that task, or any predecessor task of any of its antecedent tasks. 507, 86, 455, 457, 462, 466, 479, 508

## predefined default mapper

The default mapper that is used if no default mapper that is a user-defined mapper is visible for the type of a given list item. 278, 238, 278, 281, 282, 288, 295, 296

## predefined identifier

Unless otherwise specified, an OpenMP identifier that is defined for use in arbitrary base language expressions. 183, 7, 183, 378, 533, 534, 692, 693, 708, 847, 892

## predetermined data-sharing attribute

A data-sharing attribute that applies regardless of the clauses that are specified on a given construct, unless explicitly specified otherwise. 211, 210–213, 222, 224, 276, 292, 461, 528, 915

## preference specification

The specification of a set of preferences for interoperating with a foreign runtime environment. 470, 86, 162, 471, 891

## preference specification list

An argument list that consists of preference specification list items. 162

## preference specification list item

A list item that is a preference specification. 162, 86, 470

## pre-modified property

The property of a clause that its modifiers must appear before its arguments. 158, 161

## preprocessed code

For C/C++, a sequence of preprocessing tokens that result from the first six phases of translation, as defined by the base language. 337, 906

## present storage

A storage block that exists in a given device data environment. 282–287

## primary thread

An assigned thread that has thread number 0. A primary thread may be an initial thread or the thread that encounters a parallel construct, forms a team, generates a set of implicit tasks, and then executes one of those tasks as thread number 0. 4, 4, 5, 28, 53, 59, 84, 87, 105, 106, 216, 271, 272, 384, 385, 390, 392, 403, 405, 503, 569, 796, 916

## private attribute

For a given construct, a data-sharing attribute of a data entity that its lifetime is limited to that of the corresponding region and it is visible only to a single task generated by the construct or to a single SIMD lane used by the construct. 219, 7, 8, 21, 52, 60–63, 87, 90, 111, 160, 210–212, 214, 221, 228, 231, 236, 238, 241, 242, 247, 252–254, 256, 257, 267, 268, 273, 313, 371, 404, 521, 528, 915

## private-only variable

A variable that has a private attribute and no other data-sharing attribute with respect to a given construct. 226, 437

## private variable

A variable that has a private attribute with respect to a given construct. 7, 7, 8, 52, 60, 64, 87, 90, 220, 222, 267, 268, 270, 273, 410, 413, 418, 421, 422, 898

## privatization clause

The clause that may result in private variables that are new list items. 210, 37, 76, 87, 222, 236

## privatization property

The property that a clause privatizes list items. 225, 227, 229, 232, 235, 236, 252, 255–257, 445

## privatized list item

A list item that appears in the argument list of a privatization clause, resulting in one or more private new list items. 219, 219–222, 225, 226, 235, 253

## procedure

A function (for C/C++ and Fortran) or subroutine (for Fortran). 15, 26, 30, 35, 41, 45, 51, 53, 54, 59, 65, 74, 83, 91, 95, 100, 107, 108, 112, 146, 149, 154, 161–164, 184, 188, 214, 225, 226, 228, 233, 234, 240, 261, 264, 277, 281, 282, 294, 296, 300, 318, 319, 322, 329, 330, 335, 336, 341–345, 347–351, 402, 412, 413, 448, 450, 461, 464, 533, 534, 555, 556, 638, 639, 641–644, 697, 698, 700, 707, 719, 721, 731, 798, 806, 821, 826, 827, 831, 836, 841, 889, 906, 910

## procedure property

The property that a routine argument has a function pointer type in C/C++ and a procedure type in Fortran. 535, 638, 808

## processor

An implementation defined hardware unit on which one or more threads can execute. 43, 84, 117, 131, 136, 595, 680, 791–794, 803, 885, 886, 914

## product order

The partial order of two logical iteration vectors $\omega _ { a } = ( i _ { 1 } , \ldots , i _ { n } )$ and $\omega _ { b } = ( j _ { 1 } , \ldots , j _ { n } )$ 2 denoted by $\omega _ { a } \leq _ { \mathrm { p r o d u c t } } \omega _ { b } .$ , where $i _ { k } \le j _ { k }$ for all $k \in \{ 1 , \ldots , n \}$ . 381

## program order

An ordering of operations performed by the same thread as determined by the execution sequence of operations specified by the base language.

COMMENT: For versions of C and C++ that include base language support for threading, program order corresponds to the sequenced-before relation between operations performed by the same thread.

12, 13, 88, 98

## progress group

A group of consecutive threads in a team that may execute on the same progress unit. 393, 393

## progress unit

An implementation defined set of consecutive hardware threads on which native threads may execute a common stream of instructions. 6, 6, 7, 88, 393, 534, 596

## property

A characteristic of an OpenMP feature. xxvii, 20–22, 24, 28–31, 33, 35, 37, 39–41, 43–46, 49, 50, 52–55, 57, 61–63, 65, 66, 68–79, 81–97, 101, 103–107, 109, 110, 112–114, 159, 160, 169, 173, 179–182, 205–207, 215, 223–227, 229, 230, 232, 235–238, 251, 252, 255–258, 260, 262, 263, 265, 266, 269–272, 274, 278–280, 289–291, 293, 297–301, 303, 309, 310, 312, 313, 315, 316, 318–321, 323, 325–327, 330, 331, 333, 334, 336–341, 343, 344, 346,

349, 350, 352–355, 357–369, 372, 374–384, 388, 392–394, 397–403, 405–409, 412, 416–418, 420, 422, 423, 425, 426, 429, 432–435, 438–446, 450–452, 454, 456, 458, 460, 465, 468–470, 472, 473, 475, 478, 479, 481–494, 498, 504–507, 511, 512, 514, 515 517–520, 524, 528, 535–545, 547, 548, 550, 552–554, 556–560, 562, 563, 565, 566, 568–579, 581–584, 586–590, 592–602, 604–609, 611, 613–617, 619, 620, 622–628, 631–636, 638–644, 646–653, 656–661, 664–671, 673–676, 678–686, 688–692, 694, 697, 698, 708–712, 714–732, 734–743, 745–753, 755–757, 759–770, 772–777, 780, 782, 784, 786–797, 799–801, 803–814, 819, 820, 822–832, 834, 835, 837–873, 875–877, 892, 899
````
