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
