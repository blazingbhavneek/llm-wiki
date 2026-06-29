# Assertion in CUDA

CUDA provides assertion support for devices with compute capability 2.x and higher. The `assert()` macro is used to verify conditions during kernel execution. If the expression provided to the macro evaluates to zero, kernel execution is halted. If the expression is non-zero, the kernel execution is unaffected [CUDA_C_Programming_Guide:L11102-L11156].

## Behavior and Output

When an assertion fails (expression is zero), the behavior depends on the execution environment:

*   **Debugger:** If the program is run within a debugger, the failure triggers a breakpoint, allowing the debugger to inspect the current state of the device [CUDA_C_Programming_Guide:L11102-L11156].
*   **Standard Execution:** If not running in a debugger, each thread for which the expression is zero prints a message to `stderr`. This message is printed after synchronization with the host via `cudaDeviceSynchronize()`, `cudaStreamSynchronize()`, or `cudaEventSynchronize()` [CUDA_C_Programming_Guide:L11102-L11156].

The format of the error message printed to `stderr` is:

```
<filename>:<line number>:<function>:
block: [blockIdx.x,blockIdx.y,blockIdx.z],
thread: [threadIdx.x,threadIdx.y,threadIdx.z]
Assertion `<expression>` failed.
```

## Error Handling and Recovery

Once an assertion fails, any subsequent host-side synchronization calls made for the same device will return `cudaErrorAssert`. No more commands can be sent to this device until `cudaDeviceReset()` is called to reinitialize the device [CUDA_C_Programming_Guide:L11102-L11156].

## Usage Example

The following example demonstrates the use of assertions in a CUDA kernel:

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

This program outputs:

```
test.cu:19: void testAssert(): block: [0,0,0], thread: [0,0,0] Assertion `should_be_one` failed.
```

## Performance and Debugging

Assertions are intended for debugging purposes. They can affect performance, so it is recommended to disable them in production code. They can be disabled at compile time by defining the `NDEBUG` preprocessor macro before including `assert.h` [CUDA_C_Programming_Guide:L11102-L11156].

Note that the expression in an assertion should not have side effects (e.g., `++i > 0`). If the assertion is disabled via `NDEBUG`, code relying on those side effects will behave differently [CUDA_C_Programming_Guide:L11102-L11156].
