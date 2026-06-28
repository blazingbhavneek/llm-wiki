1 Cooperative Groups ..... 281
11.1 Introduction ..... 281
11.2 What's New in Cooperative Groups ..... 281
11.2.1 CUDA 13.0 ..... 281
11.2.2 CUDA 12.2 ..... 282
11.2.3 CUDA 12.1 ..... 282
11.2.4 CUDA 12.0 ..... 282
11.3 Programming Model Concept ..... 282
11.3.1 Composition Example ..... 283
11.4 Group Types ..... 284
11.4.1 Implicit Groups ..... 284
11.4.1.1 Thread Block Group ..... 284
11.4.1.2 Cluster Group ..... 285
11.4.1.3 Grid Group ..... 286
11.4.2 Explicit Groups ..... 287
11.4.2.1 Thread Block Tile ..... 287
11.4.2.2 Coalesced Groups ..... 290
11.5 Group Partitioning ..... 292

11.5.1 tiled\_partition 292
11.5.2 labeled\_partition 292
11.5.3 binary\_partition 293
11.6 Group Collectives 293
11.6.1 Synchronization 294
11.6.1.1 barrier\_arrive and barrier\_wait 294
11.6.1.2 sync 295
11.6.2 Data Transfer 295
11.6.2.1 memcpy\_async 295
11.6.2.2 wait and wait\_prior 297
11.6.3 Data Manipulation 298
11.6.3.1 reduce 298
11.6.3.2 Reduce Operators 300
11.6.3.3 inclusive\_scan and exclusive\_scan 301
11.6.4 Execution control 305
11.6.4.1 invoke\_one and invoke\_one\_broadcast 305
11.7 Grid Synchronization 306
