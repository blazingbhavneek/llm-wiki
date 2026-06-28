
3 CUDA Dynamic Parallelism 317
13.1 Introduction 317
13.1.1 Overview 317
13.1.2 Glossary 317
13.2 Execution Environment and Memory Model 318
13.2.1 Execution Environment 318
13.2.1.1 Parent and Child Grids 318
13.2.1.2 Scope of CUDA Primitives 319
13.2.1.3 Synchronization 319
13.2.1.4 Streams and Events 320
13.2.1.5 Ordering and Concurrency 320
13.2.1.6 Device Management 320
13.2.2 Memory Model 321
13.2.2.1 Coherence and Consistency 321
13.3 Programming Interface 323
13.3.1 CUDA C++ Reference 323
13.3.1.1 Device-Side Kernel Launch 323
13.3.1.2 Streams 324
13.3.1.3 Events 326
13.3.1.4 Synchronization 327
13.3.1.5 Device Management 327
13.3.1.6 Memory Declarations 327
13.3.1.7 API Errors and Launch Failures 328
13.3.1.8 API Reference 330
13.3.2 Device-side Launch from PTX 332
13.3.2.1 Kernel Launch APIs 332
13.3.2.2 Parameter Buffer Layout 333
13.3.3 Toolkit Support for Dynamic Parallelism 333

13.3.3.1 Including Device Runtime API in CUDA Code 333
13.3.3.2 Compiling and Linking 334
13.4 Programming Guidelines 334
13.4.1 Basics 334
13.4.2 Performance 335
13.4.2.1 Dynamic-parallelism-enabled Kernel Overhead 335
13.4.3 Implementation Restrictions and Limitations 335
13.4.3.1 Runtime 336
13.5 CDP2 vs CDP1 338
13.5.1 Differences Between CDP1 and CDP2 338
13.5.2 Compatibility and Interoperability 339
13.6 Legacy CUDA Dynamic Parallelism (CDP1) 339
13.6.1 Execution Environment and Memory Model (CDP1) 339
13.6.1.1 Execution Environment (CDP1) 340
13.6.1.2 Memory Model (CDP1) 343
13.6.2 Programming Interface (CDP1) 346
13.6.2.1 CUDA C++ Reference (CDP1) 346
13.6.2.2 Device-side Launch from PTX (CDP1) 354
13.6.2.3 Toolkit Support for Dynamic Parallelism (CDP1) 356
13.6.3 Programming Guidelines (CDP1) 357
13.6.3.1 Basics (CDP1) 357
13.6.3.2 Performance (CDP1) 358
13.6.3.3 Implementation Restrictions and Limitations (CDP1) 359
