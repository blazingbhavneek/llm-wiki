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
