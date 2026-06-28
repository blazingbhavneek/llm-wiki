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

## extended address range

For a given original list item, the address range that starts from the minimum of its starting address and its base address and ends with maximum of its ending address and its base address. 280, 71, 281

## extended list

An argument list that consists of extended list items. 162, 51

## extended list item

A variable list item or the name of a procedure. 162, 51, 164

## extension trait

A trait that is implementation defined. 319, 318

## F

## finalized taskgraph record

A taskgraph record in which all information required for a replay execution has been saved. 436, 71, 436

## final task

A task that generates included final tasks when it encounters task-generating constructs on which the final clause may be specified. 441, 52, 116, 427, 436, 437, 439, 441, 442, 445, 588, 915

## first-party tool

A tool that executes in the address space of the program that it is monitoring. 697, 14, 29, 78, 144, 695, 697, 699, 903, 911

## firstprivate attribute

For a given construct, a data-sharing attribute of a variable that implies the private attribute, and additionally the variable is initialized with the value of the variable that has the same name in the enclosing data environment of the construct. 227, 52, 211–214, 277, 292, 436, 461, 904, 912

## firstprivate variable

A private variable that has the firstprivate attribute with respect to a given construct. 430, 437, 891

## flat-memory-copying property

The property that a memory-copying routine copies a unidimensional, contiguous storage block. 612, 52, 613, 615

## flat-memory-copying routine

A routine that has the flat-memory-copying property. 612, 612, 614, 616

## flush

An operation that a thread performs to enforce consistency between its view of memory and the view of memory of any other threads. 6, 10–14, 19, 52, 58, 92, 99, 107, 404, 472, 494, 499–501, 908, 915

## flush property

A property that determines the manner in which a flush enforces memory consistency. Any flush has one or more of the following: the strong flush property, the release flush property, and the acquire flush property. 11, 908

## flush-set

The set of variables upon which a strong flush operates. 10, 10

## foreign execution context

A context that is instantiated from a foreign runtime environment in order to facilitate execution on a given device. 53, 181, 468, 469, 542, 907

## foreign runtime environment

A runtime environment that exists outside the OpenMP runtime with which the OpenMP implementation may interoperate. 53, 62, 86, 468, 471, 539, 542

## foreign runtime identifier

A base language string literal or a constant expression of integer OpenMP type that represents a foreign runtime environment. 183, 469, 471, 891, 902

## foreign task

An instance of executable code that is executed in a foreign execution context. 181, 437, 469, 891

## Fortran-only property

The property that an OpenMP feature is only supported in Fortran. 534

## frame

A storage area on the stack of a thread that is associated with a procedure invocation. A frame includes space for one or more saved registers and often also includes space for saved arguments, local variables, and padding for alignment. 30, 53, 719–721, 744, 798, 824, 864, 865

## free-agent thread

An unassigned thread on which an explicit task is scheduled for execution or a primary thread for an explicit parallel region that was a free-agent thread when it encountered the parallel construct. 53, 100, 107, 116, 132, 142, 143, 389, 390, 448, 588, 589, 734, 890, 897, 902

## free property

The property that a modifier can appear in any position in a modifier-specification-list. 159 function

A routine or procedure that returns a type that can be the right-hand side of a base language assignment operation. 155, 156, 163, 311, 332, 337, 569–572, 575–579, 581–584, 586–588, 593–599, 601, 604–606, 609, 611, 613–615, 617, 619, 620, 623–628, 631–636, 642–644, 647–651, 653, 656–660, 675, 676, 678, 679, 681, 684, 686, 688–691, 694, 697, 745, 770,

786–795, 797, 799–801, 803–806, 808–814, 834, 835, 837–849, 851–869, 871–873, 875–877
