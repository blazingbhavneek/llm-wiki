# Assertion

Assertion is supported on compute capability 2.x and higher. The assert() function stops kernel execution if the expression is zero, triggering a debugger breakpoint or printing a formatted failure message to stderr. Subsequent synchronization calls return cudaErrorAssert until cudaDeviceReset() is called. Assertions can be disabled at compile time via NDEBUG but should not contain side effects.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L11101-L11154

Citation: [CUDA_C_Programming_Guide:L11101-L11154]

````text
## 10.32. Assertion

Assertion is only supported by devices of compute capability 2.x and higher.

```txt
void assert(int expression);
```

stops the kernel execution if expression is equal to zero. If the program is run within a debugger, this triggers a breakpoint and the debugger can be used to inspect the current state of the device. Otherwise, each thread for which expression is equal to zero prints a message to stderr after synchronization with the host via cudaDeviceSynchronize(), cudaStreamSynchronize(), or cudaEventSynchronize(). The format of this message is as follows:

```txt
<filename>:<line number>:<function>:
block: [blockId.x,blockId.x,blockIdx.z],
thread: [threadIdx.x,threadIdx.y,threadIdx.z]
Assertion `<expression>` failed.
```

Any subsequent host-side synchronization calls made for the same device will return cudaErrorAssert. No more commands can be sent to this device until cudaDeviceReset() is called to reinitialize the device.

If expression is diferent from zero, the kernel execution is unafected.

For example, the following program from source file test.cu

```c
#include <assert.h>

__global__ void testAssert(void)
{
    int is_one = 1;
    int should_be_one = 0;

    // This will have no effect
    assert(is_one);

    // This will halt kernel execution
    assert(should_be_one);
}

int main(int argc, char* argv[])
{
    testAssert<<<1,1>>>();
    cudaDeviceSynchronize();

    return 0;
}
```

will output:

```txt
test.cu:19: void testAssert(): block: [0,0,0], thread: [0,0,0] Assertion `should_be_ one` failed.
```

Assertions are for debugging purposes. They can afect performance and it is therefore recommended to disable them in production code. They can be disabled at compile time by defining the NDEBUG preprocessor macro before including assert.h. Note that expression should not be an expression with side efects (something like(++i > 0), for example), otherwise disabling the assertion will afect the functionality of the code.
````
