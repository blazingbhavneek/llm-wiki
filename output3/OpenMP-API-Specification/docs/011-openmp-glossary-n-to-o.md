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
