22 Teams Region Routines 581
22.1 omp\_get\_num\_teams Routine 581
22.2 omp\_set\_num\_teams Routine 582
22.3 omp\_get\_team\_num Routine 582
22.4 omp\_get\_max\_teams Routine 583
22.5 omp\_get\_teams\_thread\_limit Routine 584
22.6 omp\_set\_teams\_thread\_limit Routine 584

23 Tasking Support Routines 586
23.1 Tasking Routines 586
23.1.1 omp\_get\_max\_task\_priority Routine 586
23.1.2 omp\_in\_explicit\_task Routine 587
23.1.3 omp\_in\_final Routine 587
23.1.4 omp\_is\_free\_agent Routine 588
23.1.5 omp\_ancestor\_is\_free\_agent Routine 588
23.2 Event Routine 589
23.2.1 omp\_fulfill\_event Routine 589

24 Device Information Routines 592
24.1 omp\_set\_default\_device Routine 592
24.2 omp\_get\_default\_device Routine 593
24.3 omp\_get\_num\_devices Routine 593
24.4 omp\_get\_device\_num Routine 594
24.5 omp\_get\_num\_procs Routine 594
24.6 omp\_get\_max\_progress\_width Routine 595
24.7 omp\_get\_device\_from\_uid Routine 596
24.8 omp\_get\_uid\_from\_device Routine 596
24.9 omp\_is\_initial\_device Routine 597
24.10 omp\_get\_initial\_device Routine 598
24.11 omp\_get\_device\_num\_teams Routine 599
24.12 omp\_set\_device\_num\_teams Routine 599
24.13 omp\_get\_device\_teams\_thread\_limit Routine 601
24.14 omp\_set\_device\_teams\_thread\_limit Routine 601

25 Device Memory Routines
25.1 Asynchronous Device Memory Routines 604
25.2 Device Memory Information Routines 604
25.2.1 omp\_target\_is\_present Routine 604
25.2.2 omp\_target\_is\_accessible Routine 605
25.2.3 omp\_get\_mapped\_ptr Routine 606
25.3 omp\_target\_alloc Routine 606
25.4 omp\_target\_free Routine 608
25.5 omp\_target\_associate\_ptr Routine 609
25.6 omp\_target\_disassociate\_ptr Routine 611
25.7 Memory Copying Routines 612
25.7.1 omp\_target\_memcpy Routine 613
25.7.2 omp\_target\_memcpy\_rect Routine 614
25.7.3 omp\_target\_memcpy\_async Routine 615
25.7.4 omp\_target\_memcpy\_rect\_async Routine 617
25.8 Memory Setting Routines 618
25.8.1 omp\_target\_memset Routine 619
25.8.2 omp\_target\_memset\_async Routine 620

26 Interoperability Routines
26.1 omp\_get\_num\_interop\_properties Routine 623
26.2 omp\_get\_interop\_int Routine 623
26.3 omp\_get\_interop\_ptr Routine 624
26.4 omp\_get\_interop\_str Routine 625
26.5 omp\_get\_interop\_name Routine 626
26.6 omp\_get\_interop\_type\_desc Routine 627
26.7 omp\_get\_interop\_rc\_desc Routine 628

27 Memory Management Routines
27.1 Memory Space Retrieving Routines 630
27.1.1 omp\_get\_devices\_memspace Routine 631
27.1.2 omp\_get\_device\_memspace Routine 632
27.1.3 omp\_get\_devices\_and\_host\_memspace Routine 632
27.1.4 omp\_get\_device\_and\_host\_memspace Routine 633

27.1.5 omp\_get\_devices\_all\_memspace Routine . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 634
27.2 omp\_get\_memspace\_num\_resources Routine . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 634
27.3 omp\_get\_memspace\_pagesize Routine . . . . . . . . . . . . . . . . . . . . . . . . 635
27.4 omp\_get\_submemspace Routine . . . . . . . . . . . . . . . . . . . 636
27.5 OpenMP Memory Partitioning Routines .. ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ...
27.5.1 omp\_init\_mepartitioner Routine .. ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ...
27.5.2 omp\_destroy\_mepartitioner Routine .. ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ...
27.5.3 omp\_init\_mepartition Routine .. ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ... ...
27.5.4 omp\_destroy\_mepartition Routine ..... ....... ....... ....... ....... ....... ....... ....... ....... ....... ....... ....... ....... ....... ....... .......
27.5.5 omp\_mepartition\_set\_part Routine ..... ............................................................................ ....... 641
27.5.6 omp\_mepartition\_get\_user\_data Routine ..... ..................................................................... ....... 643
27.6 omp\_init\_allocator Routine ..... ................................ 644
27.7 omp\_destroy\_allocator Routine ..... ................................ 646
27.8 Memory Allocator Retrieving Routines ..... ................................ 647
27.8.1 omp\_get\_devices\_allocator Routine ..... ................................ 647
27.8.2 omp\_get\_device\_allocator Routine ..... ................................ 648
27.8.3 omp\_get\_devices\_and\_host\_allocator Routine ..... ................................ 649
27.8.4 omp\_get\_device\_and\_host\_allocator Routine ..... ................................ 650
27.8.5 omp\_get\_devices\_all\_allocator Routine ..... ................................ 651
27.9 omp\_set\_default\_allocator Routine ..... ................................ 652
27.10 omp\_get\_default\_allocator Routine ..... ................................ 653
27.11 Memory Allocating Routines ..... ........... 654
27.11.1 omp\_alloc Routine ..... ........... 656
27.11.2 omp\_aligned\_alloc Routine ..... ........... 657
27.11.3 omp\_calloc Routine ..... ........... 658
27.11.4 omp\_aligned\_calloc Routine ..... ........... 659
27.11.5 omp\_realloc Routine ..... ........... 660
27.12 omp\_free Routine ..... ........... 661
