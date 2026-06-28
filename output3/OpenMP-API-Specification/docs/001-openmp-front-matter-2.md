# OpenMP Application Programming Interface

Version 6.0 November 2024

Copyright ©1997-2024 OpenMP Architecture Review Board. Permission to copy without fee all or part of this material is granted, provided the OpenMP Architecture Review Board copyright notice and the title of this document appear. Notice is given that copying is by permission of the OpenMP Architecture Review Board.

This page intentionally left blank in published version.

## Contents

I Definitions
1 Overview of the OpenMP API
2
1.1 Scope .... 2
1.2 Execution Model .... 2
1.3 Memory Model .... 7
1.3.1 Structure of the OpenMP Memory Model .... 7
1.3.2 Device Data Environments .... 8
1.3.3 Memory Management .... 9
1.3.4 The Flush Operation .... 10
1.3.5 Flush Synchronization and Happens-Before Order .... 11
1.3.6 OpenMP Memory Consistency .... 13
1.4 Tool Interfaces .... 14
1.4.1 OMPT .... 14
1.4.2 OMPD .... 15
1.5 OpenMP Compliance .... 15
1.6 Normative References .... 16
1.7 Organization of this Document .... 17
2 Glossary
3 Internal Control Variables
115
3.1 ICV Descriptions .... 115
3.2 ICV Initialization .... 118
3.3 Modifying and Retrieving ICV Values .... 121
3.4 How the Per-Data Environment ICVs Work .... 124
3.5 ICV Override Relationships .... 125

Environment Variables 127
4.1 Parallel Region Environment Variables 128
4.1.1 Abstract Name Values 128
4.1.2 OMP\_DYNAMIC 128
4.1.3 OMP\_NUM\_THREADS 129
4.1.4 OMP\_THREAD\_LIMIT 130
4.1.5 OMP\_MAX\_ACTIVE\_LEVELS 130
4.1.6 OMP\_PLACES 130
4.1.7 OMP\_PROC\_BIND 132
4.2 Teams Environment Variables 133
4.2.1 OMP\_NUM\_TEAMS 133
4.2.2 OMP\_TEAMS\_THREAD\_LIMIT 134
4.3 Program Execution Environment Variables 134
4.3.1 OMP\_SCHEDULE 134
4.3.2 OMP\_STACKSIZE 135
4.3.3 OMP\_WAIT\_POLICY 135
4.3.4 OMP\_DISPLAY\_AFFINITY 136
4.3.5 OMP\_AFFINITY\_FORMAT 137
4.3.6 OMP\_CANCELLATION 139
4.3.7 OMPAVAILABLE\_DEVICES 139
4.3.8 OMP\_DEFAULT\_DEVICE 140
4.3.9 OMP\_TARGET\_OFFLOAD 141
4.3.10 OMP\_THREADS\_RESERVE 141
4.3.11 OMP\_MAX\_TASK\_PRIORITY 143
4.4 Memory Allocation Environment Variables 143
4.4.1 OMP\_ALLOCATOR 143
4.5 OMPT Environment Variables 144
4.5.1 OMP\_TOOL 144
4.5.2 OMP\_TOOL\_LIBRARIES 145
4.5.3 OMP\_TOOL\_VERBOSE\_INIT 145
4.6 OMPD Environment Variables 146
4.6.1 OMP\_DEBUG 146
4.7 OMP\_DISPLAY\_ENV 147

5 Directive and Construct Syntax 148  
5.1 Directive Format 150  
5.1.1 Free Source Form Directives 156  
5.1.2 Fixed Source Form Directives 157  
5.2 Clause Format 157  
5.2.1 OpenMP Argument Lists 162  
5.2.2 Reserved Locators 164  
5.2.3 OpenMP Operations 165  
5.2.4 Array Shaping 165  
5.2.5 Array Sections 166  
5.2.6 iterator Modifier 169  
5.3 Conditional Compilation 171  
5.3.1 Free Source Form Conditional Compilation Sentinel 172  
5.3.2 Fixed Source Form Conditional Compilation Sentinels 173  
5.4 directive-name-modifier Modifier 173  
5.5 if Clause 179  
5.6 init Clause 180  
5.7 destroy Clause 182  
6 Base Language Formats and Restrictions 183  
6.1 OpenMP Types and Identifiers 183  
6.2 OpenMP Stylized Expressions 185  
6.3 Structured Blocks 186  
6.3.1 OpenMP Allocator Structured Blocks 187  
6.3.2 OpenMP Function Dispatch Structured Blocks 187  
6.3.3 OpenMP Atomic Structured Blocks 188  
6.4 Loop Concepts 195  
6.4.1 Canonical Loop Nest Form 196  
6.4.2 Canonical Loop Sequence Form 202  
6.4.3 OpenMP Loop-Iteration Spaces and Vectors 203  
6.4.4 Consistent Loop Schedules 205  
6.4.5 collapse Clause 205  
6.4.6 ordered Clause 206  
6.4.7 looprange Clause 207

II Directives and Clauses 209
7 Data Environment 210
7.1 Data-Sharing Attribute Rules . 210
7.1.1 Variables Referenced in a Construct . 210
7.1.2 Variables Referenced in a Region but not in a Construct . 214
7.2 saved Modifier . 215
7.3 threadprivate Directive . 215
7.4 List Item Privatization . 219
7.5 Data-Sharing Attribute Clauses . 222
7.5.1 default Clause . 223
7.5.2 shared Clause . 224
7.5.3 private Clause . 225
7.5.4 firstprivate Clause . 227
7.5.5 lastprivate Clause . 229
7.5.6 linear Clause . 232
7.5.7 is\_device\_ptr Clause . 235
7.5.8 use\_device\_ptr Clause . 236
7.5.9 has\_device\_addr Clause . 237
7.5.10 use\_device\_addr Clause . 238
7.6 Reduction and Induction Clauses and Directives . 239
7.6.1 OpenMP Reduction and Induction Identifiers . 239
7.6.2 OpenMP Reduction and Induction Expressions . 240
7.6.3 Implicitly Declared OpenMP Reduction Identifiers . 244
7.6.4 Implicitly Declared OpenMP Induction Identifiers . 246
7.6.5 Properties Common to Reduction and induction Clauses . 247
7.6.6 Properties Common to All Reduction Clauses . 249
7.6.7 Reduction Scoping Clauses . 250
7.6.8 Reduction Participating Clauses . 251
7.6.9 reduction-identifier Modifier . 251
7.6.10 reduction Clause . 252
7.6.11 task\_reduction Clause . 255
7.6.12 in\_reduction Clause . 256
7.6.13 induction Clause . 257

7.6.14 declare\_reduction Directive 260
7.6.15 combiner Clause 262
7.6.16 initializer Clause 262
7.6.17 declare\_induction Directive 263
7.6.18 inductor Clause 265
7.6.19 collector Clause 266
7.7 scan Directive 266
7.7.1 inclusive Clause 269
7.7.2 exclusive Clause 269
7.7.3 init\_complete Clause 270
7.8 Data Copying Clauses 270
7.8.1 copyin Clause 271
7.8.2 copyprivate Clause 272
7.9 Data-Mapping Control 274
7.9.1 map-type Modifier 274
7.9.2 Map Type Decay 275
7.9.3 Implicit Data-Mapping Attribute Rules 276
7.9.4 Mapper Identifiers and mapper Modifiers 278
7.9.5 ref-modifier Modifier 279
7.9.6 map Clause 279
7.9.7 enter Clause 289
7.9.8 link Clause 290
7.9.9 defaultmap Clause 291
7.9.10 declare\_mapper Directive 293
7.10 Data-Motion Clauses 295
7.10.1 to Clause 297
7.10.2 from Clause 298
7.11 uniform Clause 299
7.12 aligned Clause 300
7.13 groupprivate Directive 301
7.14 local Clause 303

Memory Management 304
8.1 Memory Spaces 304

8.2 Memory Allocators 305  
8.3 align Clause 309  
8.4 allocator Clause 310  
8.5 allocate Directive 310  
8.6 allocate Clause 312  
8.7 allocators Construct 315  
8.8 uses\_allocators Clause 315  

Variant Directives 318  
9.1 OpenMP Contexts 318  
9.2 Context Selectors 320  
9.3 Matching and Scoring Context Selectors 323  
9.4 Metadirectives 324  
9.4.1 when Clause 325  
9.4.2 otherwise Clause 326  
9.4.3 metadirective 327  
9.4.4 begin metadirective 327  
9.5 Semantic Requirement Set 328  
9.6 Declare Variant Directives 328  
9.6.1 match Clause 330  
9.6.2 adjust\_args Clause 331  
9.6.3 append\_args Clause 333  
9.6.4 declare\_variant Directive 334  
9.6.5 begin declare\_variant Directive 336  
9.7 dispatch Construct 337  
9.7.1 interop Clause 339  
9.7.2 novariants Clause 340  
9.7.3 nocontext Clause 340  
9.8 declare\_simd Directive 341  
9.8.1 branch Clauses 343  
9.9 Declare Target Directives 345  
9.9.1 declare\_target Directive 346  
9.9.2 begin declare\_target Directive 349  
9.9.3 indirect Clause 350

10 Informational and Utility Directives 352  
10.1 error Directive 352  
10.2 at Clause 353  
10.3 message Clause 353  
10.4 severity Clause 354  
10.5 requires Directive 355  
10.5.1 requirement Clauses 356  
10.6 Assumption Directives 362  
10.6.1 assumption Clauses 363  
10.6.2 assumes Directive 368  
10.6.3 assume Directive 369  
10.6.4 begin assumes Directive 369  
10.7 nothing Directive 369  
11 Loop-Transforming Constructs 371  
11.1 apply Clause 372  
11.2 sizes Clause 374  
11.3 fuse Construct 374  
11.4 interchange Construct 375  
11.4.1 permutation Clause 376  
11.5 reverse Construct 377  
11.6 split Construct 377  
11.6.1 counts Clause 378  
11.7 stripe Construct 379  
11.8 tile Construct 380  
11.9 unroll Construct 381  
11.9.1 full Clause 382  
11.9.2 partial Clause 383  
12 Parallelism Generation and Control 384  
12.1 parallel Construct 384  
12.1.1 Determining the Number of Threads for a parallel Region 388  
12.1.2 num\_threads Clause 388  
12.1.3 Controlling OpenMP Thread Affinity 389

12.1.4 proc\_bind Clause 392  
12.1.5 safesync Clause 393  
12.2 teams Construct 394  
12.2.1 num\_teams Clause 397  
12.3 order Clause 397  
12.4 simd Construct 399  
12.4.1 nontemporal Clause 400  
12.4.2 safelen Clause 401  
12.4.3 simdlen Clause 401  
12.5 masked Construct 402  
12.5.1 filter Clause 403  
13 Work-Distribution Constructs 404  
13.1 single Construct 405  
13.2 scope Construct 406  
13.3 sections Construct 407  
13.3.1 section Directive 408  
13.4 workshare Construct 409  
13.5 workdistribute Construct 412  
13.6 Worksharing-Loop Constructs 414  
13.6.1 for Construct 416  
13.6.2 do Construct 417  
13.6.3 schedule Clause 418  
13.7 distribute Construct 420  
13.7.1 dist\_schedule Clause 422  
13.8 loop Construct 423  
13.8.1 bind Clause 424  
14 Tasking Constructs 426  
14.1 task Construct 426  
14.2 taskloop Construct 429  
14.2.1 grainsize Clause 432  
14.2.2 num\_tasks Clause 433  
14.2.3 task\_iteration Directive 434

14.3 taskgraph Construct 435
14.3.1 graph\_id Clause 438
14.3.2 graph\_reset Clause 438
14.4 untied Clause 439
14.5 mergeable Clause 440
14.6 replayable Clause 440
14.7 final Clause 441
14.8 threadset Clause 442
14.9 priority Clause 443
14.10 affinity Clause 444
14.11 detach Clause 445
14.12 taskyield Construct 446
14.13 Initial Task 446
14.14 Task Scheduling 447

15 Device Directives and Clauses 450
15.1 device\_type Clause 450
15.2 device Clause 451
15.3 thread\_limit Clause 452
15.4 Device Initialization 453
15.5 target\_enter\_data Construct 454
15.6 target\_exit\_data Construct 456
15.7 target\_data Construct 458
15.8 target Construct 460
15.9 target\_update Construct 465

16 Interoperability 468
16.1 interop Construct 468
16.1.1 OpenMP Foreign Runtime Identifiers 469
16.1.2 use Clause 469
16.1.3 prefer-type Modifier 470

17 Synchronization Constructs and Clauses 472
17.1 hint Clause 472
17.2 critical Construct 473

17.3 Barriers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 475
17.3.1 barrier Construct . . . . . . . . . . . . . . . . . . . . . . . . . . 475
17.3.2 Implicit Barriers . . . . . . . . . . . . . . . . . . . 476
17.3.3 Implementation-Specific Barriers . . . . . . . . . . . . 477
17.4 taskgroup Construct . . . . . . . . . . . . . . . 478
17.5 taskwait Construct . . . . . . . . . . . . 479
17.6 nowait Clause . . . . . . . . . 481
17.7 nogroup Clause . . . . . . 483
17.8 OpenMP Memory Ordering 484
17.8.1 memory-order Clauses 484
17.8.2 atomic Clauses 488
17.8.3 extended-atomic Clauses 490
17.8.4 memscope Clause 493
17.8.5 atomic Construct 494
17.8.6 flush Construct 498
17.8.7 Implicit Flushes 500
17.9 OpenMP Dependences 504
17.9.1 task-dependence-type Modifier 504
17.9.2 Depend Objects 505
17.9.3 depobj Construct 505
17.9.4 update Clause 506
17.9.5 depend Clause 507
17.9.6 transparent Clause 510
17.9.7 doacross Clause 511
17.10 ordered Construct 513
17.10.1 Stand-alone ordered Construct 514
17.10.2 Block-associated ordered Construct 515
17.10.3 parallelization-level Clauses 517
Cancellation Constructs 519
18.1 cancel-directive-name Clauses 519
18.2 cancel Construct 520
18.3 cancellation\_point Construct 524

19 Composition of Constructs 525
19.1 Compound Directive Names 525
19.2 Clauses on Compound Constructs 528
19.3 Compound Construct Semantics 531

III Runtime Library Routines 532

20 Runtime Library Definitions 533
20.1 Predefined Identifiers 534
20.2 Routine Bindings 535
20.3 Routine Argument Properties 535
20.4 General OpenMP Types 536
20.4.1 OpenMP intptr Type 536
20.4.2 OpenMP uintptr Type 536
20.5 OpenMP Parallel Region Support Types 536
20.5.1 OpenMP sched Type 536
20.6 OpenMP Tasking Support Types 538
20.6.1 OpenMP event\_handle Type 538
20.7 OpenMP Interoperability Support Types 538
20.7.1 OpenMP interop Type 538
20.7.2 OpenMP interop\_fr Type 539
20.7.3 OpenMP interop\_property Type 540
20.7.4 OpenMP interop\_rc Type 541
20.8 OpenMP Memory Management Types 544
20.8.1 OpenMP allocator\_handle Type 544
20.8.2 OpenMP alloctrait Type 545
20.8.3 OpenMP alloctrait\_key Type 547
20.8.4 OpenMP alloctrait\_value Type 550
20.8.5 OpenMP alloctrait\_val Type 552
20.8.6 OpenMP mempartition Type 553
20.8.7 OpenMP mempartitioner Type 553
20.8.8 OpenMP mempartitioner\_lifetime Type 554
20.8.9 OpenMP mempartitioner\_compute\_proc Type 554

20.8.10 OpenMP mempartitioner\_release\_proc Type . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 556
20.8.11 OpenMP memspace\_handle Type . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 557
20.9 OpenMP Synchronization Types . . . . . . . . . . . . . . . . . . . . . . . . . . . 558
20.9.1 OpenMP depend Type . . . . . . . . . . . . . . . . . . . . . 558
20.9.2 OpenMP impex Type . . . . . . . . . . . . . . . . 558
20.9.3 OpenMP lock Type . . . . . . . . . . . . 559
20.9.4 OpenMP nest\_lock Type. 560
20.9.5 OpenMP sync\_hint Type. 560
20.10 OpenMP Affinity Support Types. 562
20.10.1 OpenMP proc\_bind Type. 562
20.11 OpenMP Resource Relinquishing Types. 563
20.11.1 OpenMP pause\_resource Type. 563
20.12 OpenMP Tool Types. 565
20.12.1 OpenMP control\_tool Type. 565
20.12.2 OpenMP control\_tool\_result Type. 566
21 Parallel Region Support Routines 568
21.1 omp\_set\_num\_threads Routine 568
21.2 omp\_get\_num\_threads Routine 569
21.3 omp\_get\_thread\_num Routine 569
21.4 omp\_get\_max\_threads Routine 570
21.5 omp\_get\_thread\_limit Routine 570
21.6 omp\_in\_parallel Routine 571
21.7 omp\_set\_dynamic Routine 572
21.8 omp\_get\_dynamic Routine 572
21.9 omp\_set\_schedule Routine 573
21.10 omp\_get\_schedule Routine 574
21.11 omp\_get\_supported\_active\_levels Routine 575
21.12 omp\_set\_max\_active\_levels Routine 575
21.13 omp\_get\_max\_active\_levels Routine 576
21.14 omp\_get\_level Routine 577
21.15 omp\_get\_ancestor\_thread\_num Routine 577
21.16 omp\_get\_team\_size Routine 578
21.17 omp\_get\_active\_level Routine 579
