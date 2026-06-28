## Doing I/O in the Kernel

Print statement is the most fundamental capability needed for looking at the results of a program. In accelerators, printing is surprisingly hard and also fairly expensive in terms of overhead.

SYCL\* provides some capabilities to help make this task similar to standard I/O C/C++ programs, but there are some quirks you need to understand because of the way accelerators work. File I/O is not possible from SYCL\* kernels.

SYCL\* provides the stream class to let you print information to the console from within kernels, providing an easy way to debug simple issues without resorting to a debugger. The stream class provides functionality that is very similar to the C++ STL ostream class, and its usage is similar to the STL class. Below we describe how to use SYCL stream class to output information from within an enqueued kernel.

To use the class we must first instantiate it. The signature of the stream constructor is as follows:

```c
stream(size_t BufferSize, size_t MaxStatementSize, handler &CGH);
```

The constructor takes three parameters:

• BufferSize: the total number of characters that may be printed over the entire kernel range • MaxStatementSize: the maximum number of characters in any one call to the stream class • CGH: reference to the sycl::handler parameter in the sycl::queue::submit call

Usage is very similar to that of the C++ STL ostream std::cout class. The message or data that needs to be printed is sent to the SYCL stream instance via the appropriate operator<< method. SYCL provides implementations for all the built-in data types (such as int, char and float) as well as some common classes (such as sycl::nd\_range and sycl::group).

Here is an example usage of a SYCL stream instance:

```cpp
void out1() {
    constexpr int N = 16;
    sycl::queue q;
    q.submit([&](auto &cgh) {
        sycl::stream str(8192, 1024, cgh);
        cgh.parallel_for(N, [=](sycl::item<1> it) {
            int id = it[0];
            /* Send the identifier to a stream to be printed on the console */
            str << "ID=" << id << sycl::endl;
        });
    }).wait();
} // end out1
```

The use of sycl::endl is analogous to the use of the C++ STL std::endlostream reference–it serves to insert a new line as well as flush the stream.

Compiling and executing the above kernel gives the following output:

Care must be taken in choosing the appropriate BufferSize and MaxStatementSize parameters. Insufficient sizes may cause statements to either not be printed, or to be printed with less information than expected. Consider the following kernel:

```cpp
void out2() {
    sycl::queue q;
    q.submit([&](auto &cgh) {
        sycl::stream str(8192, 4, cgh);
```

```cpp
cgh.parallel_for(1, [=](sycl::item<1>) {
    str << "ABC" << sycl::endl;      // Print statement 1
    str << "ABCDEFG" << sycl::endl; // Print statement 2
});
}).wait();
} // end out2
```

Compiling and running this kernel gives the following output:

```txt
ABC
```

The first statement was successfully printed out since the number of characters to be printed is 4 (including the newline introduced by sycl::endl) and the maximum statement size (as specified by the MaxStatementSize parameter to the sycl::stream constructor) is also 4. However, only the newline from the second statement is printed.

The following kernel shows the impact of increasing the allowed maximum character size:

```cpp
void out3() {
    sycl::queue q;
    q.submit([&](auto &cgh) {
        sycl::stream str(8192, 10, cgh);
        cgh.parallel_for(1, [=](sycl::item<1>) {
            str << "ABC" << sycl::endl;      // Print statement 1
            str << "ABCDEFG" << sycl::endl; // Print statement 2
        });
    }).wait();
} // end out3
```

Compiling and running the above kernel gives the expected output:

```txt
ABC
ABCDEFGHIJKLMNOPQRSTUVWXYZ
```

The examples above used simple kernels with a single work item. More realistic kernels will typically include multiple work items. In these cases, no guarantee is made as to the specific order of the statements printed to the console and you should expect statements from different work items to be interleaved. Consider the following kernel:

```cpp
void out4() {
    sycl::queue q;
    q.submit([&](auto &cgh) {
        sycl::stream str(8192, 1024, cgh);
        cgh.parallel_for(sycl::nd_range<1>(32, 4), [=](sycl::nd_item<1> it) {
            int id = it.get_global_id();
            str << "ID=" << id << sycl::endl;
        });
    }).wait();
} // end out4
```

One run can produce the following output.

```txt
ID=29
ID=30
ID=31
```

When this program is run again, we might get the output in a totally different order, depending on the order the threads are executed.

The output from sycl::stream is printed after the kernel has completed execution. In most cases this is of no consequence. However, should the kernel fault or throw an exception, no statement will be printed. To illustrate this, consider the following kernel, which raises an exception:

```cpp
void out5() {
    int *m = NULL;
    sycl::queue q;
    q.submit([&](auto &cgh) {
        sycl::stream str(8192, 1024, cgh);
        cgh.parallel_for(sycl::nd_range<1>(32, 4), [=](sycl::nd_item<1> it) {
            int id = it.get_global_id();
            str << "ID=" << id << sycl::endl;
            if (id == 31)
                *m = id;
        });
    }).wait();
} // end out5
```

Compiling and executing the above code generates a segmentation fault due the write to a null pointer.

```txt
Segmentation fault (core dumped)
```

None of the print statements are actually printed to the console. Instead, you will see an error message about a segmentation fault. This is unlike traditional C/C++ streams.
