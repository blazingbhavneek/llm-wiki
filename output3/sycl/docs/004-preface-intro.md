
## Preface

If you are new to parallel programming that is okay. If you have never heard of SYCL or the DPC++ compilerthat is also okay

Compared with programming in CUDA, C++ with SYCL offers portability beyond NVIDIA, and portability beyond GPUs, plus a tight alignment to enhance modern C++ as it evolves too. C++ with SYCL offers these advantages without sacrificing performance.

C++ with SYCL allows us to accelerate our applications by harnessing the combined capabilities of CPUs, GPUs, FPGAs, and processing devices of the future without being tied to any one vendor.

SYCL is an industry-driven Khronos Group standard adding advanced support for data parallelism with C++ to exploit accelerated (heterogeneous) systems. SYCL provides mechanisms for C++ compilers that are highly synergistic with C++ and C++ build systems. DPC++ is an open source compiler project based on LLVM that adds SYCL support. All examples in this book should work with any C++ compiler supporting SYCL 2020 including the DPC++ compiler.

If you are a C programmer who is not well versed in C++, you are in good company. Several of the authors of this book happily share that they picked up much of C++ by reading books that utilized C++ like this one. With a little patience, this book should also be approachable by C programmers with a desire to write modern C++ programs.

## Second Edition

With the benefit of feedback from a growing community of SYCL users, we have been able to add content to help learn SYCL better than ever.

## Preface

This edition teaches C++ with SYCL 2020. The first edition preceded the SYCL 2020 specification, which differed only slightly from what the first edition taught (the most obvious changes for SYCL 2020 in this edition are the header file location, the device selector syntax, and dropping an explicit host device).

Important resources for updated SYCL information, including any known book errata, include the book GitHub (https://github. com/Apress/data-parallel-CPP), the Khronos Group SYCL standards website (www.khronos.org/sycl), and a key SYCL education website (https://sycl.tech).

Chapters 20 and 21 are additions encouraged by readers of the first edition of this book.

We added Chapter 20 to discuss backend interoperability. One of the key goals of the SYCL 2020 standard is to enable broad support for hardware from many vendors with many architectures. This required expanding beyond the OpenCL-only backend support of SYCL 1.2.1. While generally “it just works,” Chapter 20 explains this in more detail for those who find it valuable to understand and interface at this level.

For experienced CUDA programmers, we have added Chapter 21 to explicitly connect C++ with SYCL concepts to CUDA concepts both in terms of approach and vocabulary. While the core issues of expressing heterogeneous parallelism are fundamentally similar, C++ with SYCL offers many benefits because of its multivendor and multiarchitecture approach. Chapter 21 is the only place we mention CUDA terminology; the rest of this book teaches using C++ and SYCL terminology with its open multivendor, multiarchitecture approaches. In Chapter 21, we strongly encourage looking at the open source tool “SYCLomatic” (github.com/oneapi-src/ SYCLomatic), which helps automate migration of CUDA code. Because it

is helpful, we recommend it as the preferred first step in migrating code. Developers using C++ with SYCL have been reporting strong results on NVIDIA, AMD, and Intel GPUs on both codes that have been ported from CUDA and original C++ with SYCL code. The resulting C++ with SYCL offers portability that is not possible with NVIDIA CUDA.

The evolution of C++, SYCL, and compilers including DPC++ continues. Prospects for the future are discussed in the Epilogue, after we have taken a journey together to learn how to create programs for heterogeneous systems using C++ with SYCL.

It is our hope that this book supports and helps grow the SYCL community and helps promote data-parallel programming in C++ with SYCL.

## Structure of This Book

This book takes us on a journey through what we need to know to be an effective programmer of accelerated/heterogeneous systems using C++ with SYCL.

## Chapters 1–4: Lay Foundations

Chapters 1–4 are important to read in order when first approaching C++ with SYCL.

Chapter 1 lays the first foundation by covering core concepts that are either new or worth refreshing in our minds.

Chapters 2–4 lay a foundation of understanding for data-parallel programming in C++ with SYCL. When we finish reading Chapters 1–4, we will have a solid foundation for data-parallel programming in C++. Chapters 1–4 build on each other and are best read in order.

## Preface

## Chapters 5–12: Build on Foundations

With the foundations established, Chapters 5–12 fill in vital details by building on each other to some degree while being easy to jump between as desired. All these chapters should be valuable to all users of C++ with SYCL.

## Chapters 13–21: Tips/Advice for SYCL in Practice

These final chapters offer advice and details for specific needs. We encourage at least skimming them all to find content that is important to your needs.

## Epilogue: Speculating on the Future

The book concludes with an Epilogue that discusses likely and potential future directions for C++ with SYCL, and the Data Parallel C++ compiler for SYCL.

We wish you the best as you learn to use C++ with SYCL.

## Foreword

SYCL 2020 is a milestone in parallel computing. For the first time we have a modern, stable, feature-complete, and portable open standard that can target all types of hardware, and the book you hold in your hand is the premier resource to learn SYCL 2020.

Computer hardware development is driven by our needs to solve larger and more complex problems, but those hardware advances are largely useless unless programmers like you and me have languages that allow us to implement our ideas and exploit the power available with reasonable effort. There are numerous examples of amazing hardware, and the first solutions to use them have often been proprietary since it saves time not having to bother with committees agreeing on standards. However, in the history of computing, they have eventually always ended up as vendor lock-in—unable to compete with open standards that allow developers to target any hardware and share code—because ultimately the resources of the worldwide community and ecosystem are far greater than any individual vendor, not to mention how open software standards drive hardware competition.

Over the last few years, my team has had the tremendous privilege of contributing to shaping the emerging SYCL ecosystem through our development of GROMACS, one of the world’s most widely used scientific HPC codes. We need our code to run on every supercomputer in the world as well as our laptops. While we cannot afford to lose performance, we also depend on being part of a larger community where other teams invest effort in libraries we depend on, where there are open compilers available, and where we can recruit talent. Since the first edition of this book, SYCL has matured into such a community; in addition to several

vendor-provided compilers, we now have a major community-driven implementation<sup>1</sup> that targets all hardware, and there are thousands of developers worldwide sharing experiences, contributing to training events, and participating in forums. The outstanding power of open source—whether it is an application, a compiler, or an open standard—is that we can peek under the hood to learn, borrow, and extend. Just as we repeatedly learn from the code in the Intel-led LLVM implementation,<sup>2</sup> the community-driven implementation from Heidelberg University, and several other codes, you can use our public repository<sup>3</sup> to compare CUDA and SYCL implementations in a large production codebase or borrow solutions for your needs—because when you do so, you are helping to further extend our community.

Perhaps surprisingly, data-parallel programming as a paradigm is arguably far easier than classical solutions such as message-passing communication or explicit multithreading—but it poses special challenges to those of us who have spent decades in the old paradigms that focus on hardware and explicit data placement. On a small scale, it was trivial for us to explicitly decide how data is moved between a handful of processes, but as the problem scales to thousands of units, it becomes a nightmare to manage the complexity without introducing bugs or having the hardware sit idle waiting for data. Data-parallel programming with SYCL solves this by striking the balance of primarily asking us to explicitly express the inherent parallelism of our algorithm, but once we have done that, the compiler and drivers will mostly handle the data locality and scheduling over tens of thousands of functional units. To be successful in data-parallel programming, it is important not to think of a computer as a single unit executing one program, but as a collection of units working independently to solve parts of a large problem. As long as we can express our problem as an algorithm where each part does not have dependencies on other parts, it is in theory straightforward to implement it, for example, as a parallel for-loop that is executed on a GPU through a device queue. However, for more practical examples, our problems are frequently not large enough to use an entire device efficiently, or we depend on performing tens of thousands of iterations per second where latency in device drivers starts to be a major bottleneck. While this book is an outstanding introduction to performance-portable GPU programming, it goes far beyond this to show how both throughput and latency matter for real-world applications, how SYCL can be used to exploit unique features both of CPUs, GPUs, SIMD units, and FPGAs, but it also covers the caveats that for good performance we need to understand and possibly adapt code to the characteristics of each type of hardware. Doing so, it is not merely a great tutorial on dataparallel programing, but an authoritative text that anybody interested in programming modern computer hardware in general should read.

One of SYCL’s key strengths is the close alignment to modern C++. This can seem daunting at first; C++ is not an easy language to fully master (I certainly have not), but Reinders and coauthors take our hand and lead us on a path where we only need to learn a handful of C++ concepts to get started and be productive in actual data-parallel programming. However, as we become more experienced, SYCL 2020 allows us to combine this with the extreme generality of C++17 to write code that can be dynamically targeted to different devices, or relying on heterogeneous parallelism that uses CPU, GPU, and network units in parallel for different tasks. SYCL is not a separate bolted-on solution to enable accelerators but instead holds great promise to be the general way we express data parallelism in C++. The SYCL 2020 standard now includes several features previously only available as vendor extensions, for example, Unified Shared Memory, sub-groups, atomic operations, reductions, simpler accessors, and many other concepts that make code cleaner, and facilitates both development as well as porting from standard C++17 or CUDA to have your code target more diverse hardware. This book provides a wonderful and accessible introduction to all of them, and you will also learn how SYCL is expected to evolve together with the rapid development C++ is undergoing.

This all sounds great in theory, but how portable is SYCL in practice? Our application is an example of a codebase that is quite challenging to optimize since data access patterns are random, the amount of data to process in each step is limited, we need to achieve thousands of iterations per second, and we are limited both by memory bandwidth, floating-point, and integer operations—it is an extreme opposite of a simple data-parallel problem. We spent over two decades writing assembly SIMD instructions and native implementations for several GPU architectures, and our very first encounters with SYCL involved both pains with adapting to differences and reporting performance regressions to driver and compiler developers. However, as of spring 2023, our SYCL kernels can achieve 80–100% of native performance on all GPU architectures not only from a single codebase but even a single precompiled binary.

SYCL is still young and has a rapidly evolving ecosystem. There are a few things not yet part of the language, but SYCL is unique as the only performance-portable standard available that successfully targets all modern hardware. Whether you are a beginner wanting to learn parallel programming, an experienced developer interested in data-parallel programming, or a maintainer needing to port 100,000 lines of proprietary API code to an open standard, this second edition is the only book you will need to become part of this community.

Erik Lindahl Professor of Biophysics Dept. Biophysics & Biochemistry Science for Life Laboratory Stockholm University

xxviii

## Acknowledgments

We have been blessed with an outpouring of community input for this second edition of our book. Much inspiration came from interactions with developers as they use SYCL in production, classes, tutorials, workshops, conferences, and hackathons. SYCL deployments that include NVIDIA hardware, in particular, have helped us enhance the inclusiveness and practical tips in our teaching of SYCL in this second edition.

The SYCL community has grown a great deal—and consists of engineers implementing compilers and tools, and a much larger group of users that adopt SYCL to target hardware of many types and vendors. We are grateful for their hard work, and shared insights.

We thank the Khronos SYCL Working Group that has worked diligently to produce a highly functional specification. In particular, Ronan Keryell has been the SYCL specification editor and a longtime vocal advocate for SYCL.

We are in debt to the numerous people who gave us feedback from the SYCL community in all these ways. We are also deeply grateful for those who helped with the first edition a few years ago, many of whom we named in the acknowledgement of that edition.

The first edition received feedback via GitHub,<sup>1</sup> which we did review but we were not always prompt in acknowledging (imagine six coauthors all thinking “you did that, right?”). We did benefit a great deal from that feedback, and we believe we have addressed all the feedback in the samples and text for this edition. Jay Norwood was the most prolific at commenting and helping us—a big thank you to Jay from all the authors!

Other feedback contributors include Oscar Barenys, Marcel Breyer, Jeff Donner, Laurence Field, Michael Firth, Piotr Fusik, Vincent Mierlak, and Jason Mooneyham. Regardless of whether we recalled your name here or not, we thank everyone who has provided feedback and helped refine our teaching of C++ with SYCL.

For this edition, a handful of volunteers tirelessly read draft manuscripts and provided insightful feedback for which we are incredibly grateful. These reviewers include Aharon Abramson, Thomas Applencourt, Rod Burns, Joe Curley, Jessica Davies, Henry Gabb, Zheming Jin, Rakshith Krishnappa, Praveen Kundurthy, Tim Lewis, Eric Lindahl, Gregory Lueck, Tony Mongkolsmai, Ruyman Reyes Castro, Andrew Richards, Sanjiv Shah, Neil Trevett, and Georg Viehöver.

We all enjoy the support of our family and friends, and we cannot thank them enough. As coauthors, we have enjoyed working as a team challenging each other and learning together along the way. We appreciate our collaboration with the entire Apress team in getting this book published.

We are sure that there are more than a few people whom we have failed to mention explicitly who have positively impacted this book project. We thank all who helped us.

As you read this second edition, please do provide feedback if you find any way to improve it. Feedback via GitHub can open up a conversation, and we will update the online errata and book samples as needed.

Thank you all, and we hope you find this book invaluable in your endeavors.

# Introduction
