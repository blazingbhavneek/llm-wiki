# OpenMP-API-Specification Source Lines 1923-2290

Fallback page created to preserve source coverage.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source OpenMP-API-Specification:L1923-L2290

Citation: [OpenMP-API-Specification:L1923-L2290]

````text
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
````
