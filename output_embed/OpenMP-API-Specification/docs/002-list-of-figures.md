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

28 Lock Routines
28.1 Lock Initializing Routines ..... ........... 664
28.1.1 omp\_init\_lock Routine ..... ........... 664
28.1.2 omp\_init\_nest\_lock Routine ..... ........... 665
28.1.3 omp\_init\_lock\_with\_hint Routine ..... ........... 666

28.1.4 omp\_init\_nest\_lock\_with\_hint Routine . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 667
28.2 Lock Destroying Routines . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 668
28.2.1 omp\_destroy\_lock Routine . . . . . . . . . . . . . . . . . . . . . . . 668
28.2.2 omp\_destroy\_nest\_lock Routine . . . . . . . . . . . . . . . . 669
28.3 Lock Acquiring Routines . . . . . . . . . . . . . . . . . 670
28.3.1 omp\_set\_lock Routine . . . . . . . . . . . . 670
28.3.2 omp\_set\_nest\_lock Routine 671
28.4 Lock Releasing Routines 672
28.4.1 omp\_unset\_lock Routine 673
28.4.2 omp\_unset\_nest\_lock Routine 674
28.5 Lock Testing Routines 675
28.5.1 omp\_test\_lock Routine 675
28.5.2 omp\_test\_nest\_lock Routine 676
29 Thread Affinity Routines 678
29.1 omp\_get\_proc\_bind Routine 678
29.2 omp\_get\_num\_places Routine 679
29.3 omp\_get\_place\_num\_procs Routine 679
29.4 omp\_get\_place\_proc\_ids Routine 680
29.5 omp\_get\_place\_num Routine 681
29.6 omp\_get\_partition\_num\_places Routine 681
29.7 omp\_get\_partition\_place\_nums Routine 682
29.8 omp\_set\_affinity\_format Routine 683
29.9 omp\_get\_affinity\_format Routine 684
29.10 omp\_display\_affinity Routine 685
29.11 omp\_capture\_affinity Routine 686
30 Execution Control Routines 688
30.1 omp\_get\_cancellation Routine 688
30.2 Resource Relinquishing Routines 689
30.2.1 omp\_pause\_resource Routine 689
30.2.2 omp\_pause\_resource\_all Routine 690
30.3 Timing Routines 691
30.3.1 omp\_get\_wtime Routine 691

30.3.2 omp\_get\_wtick Routine 691  
30.4 omp\_display\_env Routine 692  
31 Tool Support Routines 694  
31.1 omp\_control\_tool Routine 694  
IV OMPT 696  
32 OMPT Overview 697  
32.1 OMPT Interfaces Definitions 697  
32.2 Activating a First-Party Tool 697  
32.2.1 empt\_start\_tool Procedure 697  
32.2.2 Determining Whether to Initialize a First-Party Tool 699  
32.2.3 Initializing a First-Party Tool 700  
32.2.4 Monitoring Activity on the Host with OMPT 703  
32.2.5 Tracing Activity on Target Devices 704  
32.3 Finalizing a First-Party Tool 707  
33 OMPT Data Types 708  
33.1 OMPT Predefined Identifiers 708  
33.2 OMPT any\_record\_empt Type 708  
33.3 OMPT buffer Type 710  
33.4 OMPT buffer\_cursor Type 710  
33.5 OMPT callback Type 711  
33.6 OMPT callbacks Type 711  
33.7 OMPT cancel\_flag Type 714  
33.8 OMPT data Type 714  
33.9 OMPT dependence Type 715  
33.10 OMPT dependence\_type Type 716  
33.11 OMPT device Type 717  
33.12 OMPT device\_time Type 717  
33.13 OMPT dispatch Type 717  
33.14 OMPT dispatch\_chunk Type 718  
33.15 OMPT frame Type 719

33.16 OMPT frame\_flag Type 720
33.17 OMPT hwid Type 721
33.18 OMPT id Type 721
33.19 OMPT interface\_fn Type 722
33.20 OMPT mutex Type 722
33.21 OMPT native\_mon\_flag Type 723
33.22 OMPT parallel\_flag Type 724
33.23 OMPT record Type 725
33.24 OMPT record\_abstract Type 725
33.25 OMPT record\_native Type 727
33.26 OMPT record\_ompt Type 727
33.27 OMPT scope\_endpoint Type 728
33.28 OMPT set\_result Type 729
33.29 OMPT severity Type 730
33.30 OMPT start\_tool\_result Type 731
33.31 OMPT state Type 731
33.32 OMPT subvolume Type 734
33.33 OMPT sync\_region Type 735
33.34 OMPT target Type 736
33.35 OMPT target\_data\_op Type 736
33.36 OMPT target\_map\_flag Type 738
33.37 OMPT task\_flag Type 739
33.38 OMPT task\_status Type 740
33.39 OMPT thread Type 741
33.40 OMPT wait\_id Type 742
33.41 OMPT work Type 743

General Callbacks and Trace Records 744
34.1 Initialization and Finalization Callbacks 745
    34.1.1 initialize Callback 745
    34.1.2 finalize Callback 746
    34.1.3 thread\_begin Callback 746
    34.1.4 thread\_end Callback 747
34.2 error Callback 748

34.3 Parallelism Generation Callback Signatures 748  
34.3.1 parallel\_begin Callback 749  
34.3.2 parallel\_end Callback 750  
34.3.3 masked Callback 751  
34.4 Work Distribution Callback Signatures 752  
34.4.1 work Callback 752  
34.4.2 dispatch Callback 753  
34.5 Tasking Callback Signatures 755  
34.5.1 task\_create Callback 755  
34.5.2 task\_schedule Callback 756  
34.5.3 implicit\_task Callback 757  
34.6 cancel Callback 759  
34.7 Synchronization Callback Signatures 760  
34.7.1 dependences Callback 760  
34.7.2 task\_dependence Callback 761  
34.7.3 OMPT sync\_region Type 762  
34.7.4 sync\_region Callback 763  
34.7.5 sync\_region\_wait Callback 763  
34.7.6 reduction Callback 764  
34.7.7 OMPT mutex\_acquire Type 764  
34.7.8 mutex\_acquire Callback 766  
34.7.9 lock\_init Callback 766  
34.7.10 OMPT mutex Type 766  
34.7.11 lock\_destroy Callback 767  
34.7.12 mutex\_acquired Callback 768  
34.7.13 mutex\_released Callback 768  
34.7.14 nest\_lock Callback 769  
34.7.15 flush Callback 769  
34.8 control\_tool Callback 770  
35 Device Callbacks and Tracing 772  
35.1 device\_initialize Callback 772  
35.2 device\_finalize Callback 773  
35.3 device\_load Callback 774

35.4 device\_unload Callback 775
35.5 buffer\_request Callback 775
35.6 buffer\_complete Callback 776
35.7 target\_data\_op\_emi Callback 777
35.8 target\_emi Callback 780
35.9 target\_map\_emi Callback 782
35.10 target\_submit\_emi Callback 784

36 General Entry Points 786
36.1 function\_lookup Entry Point 786
36.2 enumerate\_states Entry Point 787
36.3 enumerate\_mutex\_impls Entry Point 788
36.4 set\_callback Entry Point 789
36.5 get\_callback Entry Point 790
36.6 get\_thread\_data Entry Point 791
36.7 get\_num\_procs Entry Point 791
36.8 get\_num\_places Entry Point 792
36.9 get\_place\_proc\_ids Entry Point 792
36.10 get\_place\_num Entry Point 793
36.11 get\_partition\_place\_nums Entry Point 793
36.12 get\_proc\_id Entry Point 794
36.13 get\_state Entry Point 795
36.14 get\_parallel\_info Entry Point 795
36.15 get\_task\_info Entry Point 797
36.16 get\_task\_memory Entry Point 799
36.17 get\_target\_info Entry Point 800
36.18 get\_num\_devices Entry Point 800
36.19 get\_unique\_id Entry Point 801
36.20 finalize\_tool Entry Point 801

37 Device Tracing Entry Points 803
37.1 get\_device\_num\_procs Entry Point 803
37.2 get\_device\_time Entry Point 804
37.3 translate\_time Entry Point 804

set\_trace\_empt Entry Point . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 805
set\_trace\_native Entry Point . . . . . . . . . . . . . . . . . . . . . . . 806
get\_buffer\_limits Entry Point . . . . . . . . . . . . . . . . . 807
start\_trace Entry Point . . . . . . . . . . . . . . . . 808
pause\_trace Entry Point . . . . . . . . . . . . . . 809
flush\_trace Entry Point . . . . . . . . . . . . 809
stop\_trace Entry Point . . . . . . 810
advance\_buffer\_cursor Entry Point 810
get\_record\_type Entry Point 811
get\_record\_empt Entry Point 812
get\_record\_native Entry Point 813
get\_record\_abstract Entry Point 814

V OMPD 815

38 OMPD Overview 816
38.1 OMPD Interfaces Definitions 817
38.2 Thread and Signal Safety 817
38.3 Activating a Third-Party Tool 817
38.3.1 Enabling Runtime Support for OMPD 817
38.3.2 ompd\_dll\_locations 817
38.3.3 ompd\_dll\_locations\_valid Breakpoint 818

39 OMPD Data Types 819
39.1 OMPD addr Type 819
39.2 OMPD address Type 819
39.3 OMPD address\_space\_context Type 820
39.4 OMPD callbacks Type 820
39.5 OMPD device Type 822
39.6 OMPD device\_type\_sizes Type 823
39.7 OMPD frame\_info Type 823
39.8 OMPD icv\_id Type 824
39.9 OMPD rc Type 825
39.10 OMPD seg Type 826

39.11 OMPD scope Type . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 827
39.12 OMPD size Type . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 827
39.13 OMPD team\_generator Type . . . . . . . . . . . . . . . . . . 828
39.14 OMPD thread\_context Type . . . . . . . . . . . . . . . . 829
39.15 OMPD thread\_id Type . . . . . . . . . . . . . 829
39.16 OMPD wait\_id Type . . . . . . . . . . . . 830
39.17 OMPD word Type . . . . . . . . . . 830
39.18 OMPD Handle Types . . . . . 831
39.18.1 OMPD address\_space\_handle Type 831
39.18.2 OMPD parallel\_handle Type 831
39.18.3 OMPD task\_handle Type 832
39.18.4 OMPD thread\_handle Type 832
40 OMPD Callback Interface 833
40.1 Memory Management of OMPD Library 833
40.1.1 alloc\_memory Callback 834
40.1.2 free\_memory Callback 834
40.2 Accessing Program or Runtime Memory 835
40.2.1 symbol\_addr\_lookup Callback 835
40.2.2 OMPD memory\_read Type 837
40.2.3 write\_memory Callback 839
40.3 Context Management and Navigation 840
40.3.1 get\_thread\_context\_for\_thread\_id Callback 840
40.3.2 sizeof\_type Callback 841
40.4 Device Translating Callbacks 842
40.4.1 OMPD device\_host Type 842
40.4.2 device\_to\_host Callback 843
40.4.3 host\_to\_device Callback 843
40.5 print\_string Callback 844
41 OMPD Routines 845
41.1 OMPD Library Initialization and Finalization 845
41.1.1 ompd\_initialize Routine 845
41.1.2 ompd\_get\_api\_version Routine 846

41.1.3 ompd\_get\_version\_string Routine . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 847
41.1.4 ompd\_finalize Routine . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 848
41.2 Process Initialization and Finalization . . . . . . . . . . . . . . . . . . . 848
41.2.1 ompd\_process\_initialize Routine . . . . . . . . . . . . . . . . . 848
41.2.2 ompd\_device\_initialize Routine . . . . . . . . . . . . 849
41.2.3 ompd\_get\_device\_thread\_id\_kinds Routine . . . . . . . 851
41.3 Address Space Information . . . . . . 852
41.3.1 ompd\_get\_omp\_version Routine 852
41.3.2 ompd\_get\_omp\_version\_string Routine 852
41.4 Thread Handle Routines 853
41.4.1 ompd\_get\_thread\_in\_parallel Routine 853
41.4.2 ompd\_get\_thread\_handle Routine 854
41.4.3 ompd\_get\_thread\_id Routine 855
41.4.4 ompd\_get\_device\_from\_thread Routine 856
41.5 Parallel Region Handle Routines 857
41.5.1 ompd\_get\_curr\_parallel\_handle Routine 857
41.5.2 ompd\_get\_enclosing\_parallel\_handle Routine 858
41.5.3 ompd\_get\_task\_parallel\_handle Routine 859
41.6 Task Handle Routines 860
41.6.1 ompd\_get\_curr\_task\_handle Routine 860
41.6.2 ompd\_get\_generating\_task\_handle Routine 861
41.6.3 ompd\_get\_scheduling\_task\_handle Routine 862
41.6.4 ompd\_get\_task\_in\_parallel Routine 862
41.6.5 ompd\_get\_task\_function Routine 863
41.6.6 ompd\_get\_task\_frame Routine 864
41.7 Handle Comparing Routines 865
41.7.1 ompd\_parallel\_handle\_compare Routine 865
41.7.2 ompd\_task\_handle\_compare Routine 866
41.7.3 ompd\_thread\_handle\_compare Routine 867
41.8 Handle Releasing Routines 867
41.8.1 ompd\_rel\_address\_space\_handle Routine 867
41.8.2 ompd\_rel\_parallel\_handle Routine 868
41.8.3 ompd\_rel\_task\_handle Routine 868

41.8.4 ompd\_rel\_thread\_handle Routine . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 869
41.9 Querying Thread States . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 869
41.9.1 ompd\_enumerate\_states Routine . . . . . . . . . . . . . . . . . . . . . . . . 869
41.9.2 ompd\_get\_state Routine . . . . . . . . . . . . . . . . . . 871
41.10 Display Control Variables .. 872
41.10.1 ompd\_get\_display\_control\_vars Routine .. 872
41.10.2 ompd\_rel\_display\_control\_vars Routine .. 873
41.11 Accessing Scope-Specific Information .. 873
41.11.1 ompd\_enumerate\_icvs Routine .. 873
41.11.2 ompd\_get\_icv\_from\_scope Routine .. 875
41.11.3 ompd\_get\_icv\_string\_from\_scope Routine .. 876
41.11.4 ompd\_get\_tool\_data Routine .. 877
42 OMPD Breakpoint Symbol Names 878
42.1 ompd\_bp\_thread\_begin Breakpoint .. 878
42.2 ompd\_bp\_thread\_end Breakpoint .. 878
42.3 ompd\_bp\_device\_begin Breakpoint .. 879
42.4 ompd\_bp\_device\_end Breakpoint .. 879
42.5 ompd\_bp\_parallel\_begin Breakpoint .. 879
42.6 ompd\_bp\_parallel\_end Breakpoint .. 880
42.7 ompd\_bp\_teams\_begin Breakpoint .. 881
42.8 ompd\_bp\_teams\_end Breakpoint .. 881
42.9 ompd\_bp\_task\_begin Breakpoint .. 882
42.10 ompd\_bp\_task\_end Breakpoint .. 882
42.11 ompd\_bp\_target\_begin Breakpoint .. 882
42.12 ompd\_bp\_target\_end Breakpoint .. 883
VI Appendices 884
A OpenMP Implementation-Defined Behaviors 885
B Features History 896
B.1 Deprecated Features .. 896
B.2 Version 5.2 to 6.0 Differences .. 896

B.3 Version 5.1 to 5.2 Differences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 903
B.4 Version 5.0 to 5.1 Differences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 905
B.5 Version 4.5 to 5.0 Differences . . . . . . . . . . . . . . . . . . . . . . . . 908
B.6 Version 4.0 to 4.5 Differences . . . . . . . . . . . . . . . . . . . 912
B.7 Version 3.1 to 4.0 Differences . . . . . . . . . . . 913
B.8 Version 3.0 to 3.1 Differences . . . . 914
B.9 Version 2.5 to 3.0 Differences .. 915
C Nesting of Regions 917
D Conforming Compound Directive Names 919
Index 923

## List of Figures

32.1 First-Party Tool Activation Flow Chart 699

## List of Tables

3.1 ICV Scopes and Descriptions . . . . . . . . . . . . . . . . . . . . . . . . . . 115
3.2 ICV Initial Values . . . . . . . . . . . . . . . . . . . . . . . 118
3.3 Ways to Modify and to Retrieve ICV Values . . . . . . . . . . . . . . . . 121
3.4 ICV Override Relationships . . . . . . . . . . . . . . . 125

4.1 Predefined Place-list Abstract Names . . . . . . . . . . . . . . . 128
4.2 Available Field Types for Formatting OpenMP Thread Affinity Information . . . 137
4.3 Reservation Types for OMP\_THREADS\_RESERVE . . . . . . . . 142

5.1 Syntactic Properties for Clauses, Arguments and Modifiers . . . 159

7.1 Implicitly Declared C/C++ Reduction Identifiers . . . 244
7.2 Implicitly Declared Fortran Reduction Identifiers . . 245
7.3 Implicitly Declared C/C++ Induction Identifiers . . 246
7.4 Implicitly Declared Fortran Induction Identifiers . 246
7.5 Map-Type Decay of Map Type Combinations . 276

8.1 Predefined Memory Spaces . . . 304
8.2 Allocator Traits . 305
8.3 Predefined Allocators . 308

12.1 Affinity-related Symbols used in this Section . 390

13.1 work OMPT types for Worksharing-Loop . 415

14.1 task\_create Callback Flags Evaluation . 427

20.1 Routine Argument Properties . 535
20.2 Required Values of the interop\_property OpenMP Type . 542
20.3 Required Values for the interop\_rc OpenMP Type . 543
20.4 Allowed Key-Values for alloctrait OpenMP Type . 546
20.5 Standard Tool Control Commands . 566

32.1 OMPT Callback Interface Runtime Entry Point Names and Their Type Signatures . 702
32.2 Callbacks for which set\_callback Must Return empt\_set\_always . 703
32.3 OMPT Tracing Interface Runtime Entry Point Names and Their Type Signatures . 705

35.1 Association of dev1 and dev2 arguments for target data operations ..... 779
39.1 Mapping of Scope Type and OMPD Handles ..... 828

Part I Definitions
