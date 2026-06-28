
Min value of the sum of two 32-bit signed integers, another 32-bit signed integer and a zero (ReLU)

```c
const int a = -5;
const int b = 6;
const int c = -2;
int max_value_0 = __viaddmax_s32_relu(a, b, c); // max(-5 + 6, -2, 0) = max(1, -2, 0)
    ← = 1
const int d = 4;
int max_value_1 = __viaddmax_s32_relu(a, d, c); // max(-5 + 4, -2, 0) = max(-1, -2, 0)
    ← = 0
```

Min value of two unsigned 32-bit integers and determining which value is smaller

```txt
const unsigned int a = 9;
const unsigned int b = 6;
bool smaller_value;
unsigned int min_value = __vibmin_u32(a, b, &smaller_value); // min_value is 6,
    ←smaller_value is true
```

Max values of three pairs of unsigned 16-bit integers

```txt
const unsigned a = 0x00050002;
const unsigned b = 0x00070004;
const unsigned c = 0x00020006;
unsigned int max_value = __vimax3_u16x2(a, b, c); // max(5, 7, 2) and max(2, 4, 6), so
    max_value is 0x00070006
```

## 10.26. Asynchronous Barrier

The NVIDIA C++ standard library introduces a GPU implementation of std::barrier. Along with the implementation of std::barrier the library provides extensions that allow users to specify the scope of barrier objects. The barrier API scopes are documented under Thread Scopes. Devices of compute capability 8.0 or higher provide hardware acceleration for barrier operations and integration of these barriers with the memcpy\_async feature. On devices with compute capability below 8.0 but starting 7.0, these barriers are available without hardware acceleration.

nvcuda::experimental::awbarrier is deprecated in favor of cuda::barrier.

## 10.26.1. Simple Synchronization Pattern

Without the arrive/wait barrier, synchronization is achieved using \_\_syncthreads() (to synchronize all threads in a block) or group.sync() when using Cooperative Groups.

```cpp
#include <cooperative_groups.h>

__global__ void simple_sync(int iteration_count) {
    auto block = cooperative_groups::this_thread_block();

    for (int i = 0; i < iteration_count; ++i) {
        /* code before arrive */
        block.sync(); /* wait for all threads to arrive here */
        /* code after wait */
    }
}
```

Threads are blocked at the synchronization point (block.sync()) until all threads have reached the synchronization point. In addition, memory updates that happened before the synchronization point are guaranteed to be visible to all threads in the block after the synchronization point, i.e., equivalent to atomic\_thread\_fence(memory\_order\_seq\_cst, thread\_scope\_block) as well as the sync.

This pattern has three stages:

Code before sync performs memory updates that will be read after the sync.

▶ Synchronization point

▶ Code after sync point with visibility of memory updates that happened before sync point.

## 10.26.2. Temporal Splitting and Five Stages of Synchronization

The temporally-split synchronization pattern with the std::barrier is as follows.

```c
#include <cuda/barrier>
#include <cooperative_groups.h>

__device__ void compute(float* data, int curr_iteration);
```

(continues on next page)

```cpp
(continued from previous page)
__global__ void split_arrive_wait(int iteration_count, float *data) {
    using barrier = cuda::barrier<cuda::thread_scope_block>;
    __shared__ barrier bar;
    auto block = cooperative_groups::this_thread_block();

    if (block.thread_rank() == 0) {
        init(&bar, block.size()); // Initialize the barrier with expected arrival count
    }
    block.sync();

    for (int curr_iter = 0; curr_iter < iteration_count; ++curr_iter) {
        /* code before arrive */
        barrier::arrival_token token = bar.arrive(); /* this thread arrives. Arrival
does not block a thread */
        compute(data, curr_iter);
        bar.wait(std::move(token)); /* wait for all threads participating in the barrier
to complete bar.arrive()*/
        /* code after wait */
    }
}
```

In this pattern, the synchronization point (block.sync()) is split into an arrive point (bar. arrive()) and a wait point (bar.wait(std::move(token))). A thread begins participating in a cuda::barrier with its first call to bar.arrive(). When a thread calls bar. wait(std::move(token)) it will be blocked until participating threads have completed bar. arrive() the expected number of times as specified by the expected arrival count argument passed to init(). Memory updates that happen before participating threads’ call to bar.arrive() are guaranteed to be visible to participating threads after their call to bar.wait(std::move(token)). Note that the call to bar.arrive() does not block a thread, it can proceed with other work that does not depend upon memory updates that happen before other participating threads’ call to bar.arrive().

The arrive and then wait pattern has five stages which may be iteratively repeated:

▶ Code before arrive performs memory updates that will be read after the wait.

▶ Arrive point with implicit memory fence (i.e., equivalent to atomic\_thread\_fence(memory\_order\_seq\_cst, thread\_scope\_block)).

Code between arrive and wait.

▶ Wait point.

▶ Code after the wait, with visibility of updates that were performed before the arrive.

## 10.26.3. Bootstrap Initialization, Expected Arrival Count, and Participation

Initialization must happen before any thread begins participating in a cuda::barrier.

```cpp
#include <cuda/barrier>
#include <cooperative_groups.h>

__global__ void init_barrier() {
    __shared__ cuda::barrier<cuda::thread_scope_block> bar;
```

(continues on next page)

(continued from previous page)

```rust
auto block = cooperative_groups::this_thread_block();

    if (block.thread_rank() == 0) {
        init(&bar, block.size()); // Single thread initializes the total expected arrival count.
    }
    block.sync();
}
```

Before any thread can participate in cuda::barrier, the barrier must be initialized using init() with an expected arrival count, block.size() in this example. Initialization must happen before any thread calls bar.arrive(). This poses a bootstrapping challenge in that threads must synchronize before participating in the cuda::barrier, but threads are creating a cuda::barrier in order to synchronize. In this example, threads that will participate are part of a cooperative group and use block.sync() to bootstrap initialization. In this example a whole thread block is participating in initialization, hence \_\_syncthreads() could also be used.

The second parameter of init() is the expected arrival count, i.e., the number of times bar. arrive() will be called by participating threads before a participating thread is unblocked from its call to bar.wait(std::move(token)). In the prior example the cuda::barrier is initialized with the number of threads in the thread block i.e., cooperative\_groups::this\_thread\_block().size(), and all threads within the thread block participate in the barrier.

A cuda::barrier is flexible in specifying how threads participate (split arrive/wait) and which threads participate. In contrast this\_thread\_block.sync() from cooperative groups or \_\_syncthreads() is applicable to whole-thread-block and \_\_syncwarp(mask) is a specified subset of a warp. If the intention of the user is to synchronize a full thread block or a full warp we recommend using \_\_syncthreads() and \_\_syncwarp(mask) respectively for performance reasons.

## 10.26.4. A Barrier’s Phase: Arrival, Countdown, Completion, and Reset

A cuda::barrier counts down from the expected arrival count to zero as participating threads call bar.arrive(). When the countdown reaches zero, a cuda::barrier is complete for the current phase. When the last call to bar.arrive() causes the countdown to reach zero, the countdown is automatically and atomically reset. The reset assigns the countdown to the expected arrival count, and moves the cuda::barrier to the next phase.

A token object of class cuda::barrier::arrival\_token, as returned from token=bar.arrive(), is associated with the current phase of the barrier. A call to bar.wait(std::move(token)) blocks the calling thread while the cuda::barrier is in the current phase, i.e., while the phase associated with the token matches the phase of the cuda::barrier. If the phase is advanced (because the countdown reaches zero) before the call to bar.wait(std::move(token)) then the thread does not block; if the phase is advanced while the thread is blocked in bar.wait(std::move(token)), the thread is unblocked.

It is essential to know when a reset could or could not occur, especially in non-trivial arrive/wait synchronization patterns.

1 A thread’s calls to token=bar.arrive() and bar.wait(std::move(token)) must be sequenced such that token=bar.arrive() occurs during the cuda::barrier’s current phase, and bar.wait(std::move(token)) occurs during the same or next phase.

A thread’s call to bar.arrive() must occur when the barrier’s counter is non-zero. After barrier initialization, if a thread’s call to bar.arrive() causes the countdown to reach zero then a call to bar.wait(std::move(token)) must happen before the barrier can be reused for a subsequent call to bar.arrive().

bar.wait() must only be called using a token object of the current phase or the immediately preceding phase. For any other values of the token object, the behavior is undefined.

For simple arrive/wait synchronization patterns, compliance with these usage rules is straightforward.

## 10.26.5. Spatial Partitioning (also known as Warp Specialization)

A thread block can be spatially partitioned such that warps are specialized to perform independent computations. Spatial partitioning is used in a producer or consumer pattern, where one subset of threads produces data that is concurrently consumed by the other (disjoint) subset of threads.

A producer/consumer spatial partitioning pattern requires two one sided synchronizations to manage a data bufer between the producer and consumer.

<table><tr><td>Producer</td><td>Consumer</td></tr><tr><td>wait for buffer to be ready to be filled</td><td>signal buffer is ready to be filled</td></tr><tr><td>produce data and fill the buffer</td><td></td></tr><tr><td>signal buffer is filled</td><td>wait for buffer to be filled</td></tr><tr><td></td><td>consume data in filled buffer</td></tr></table>

Producer threads wait for consumer threads to signal that the bufer is ready to be filled; however, consumer threads do not wait for this signal. Consumer threads wait for producer threads to signal that the bufer is filled; however, producer threads do not wait for this signal. For full producer/consumer concurrency this pattern has (at least) double bufering where each bufer requires two cuda::barriers.

```cpp
#include <cuda/barrier>
#include <cooperative_groups.h>

using barrier = cuda::barrier<cuda::thread_scope_block>;

__device__ void producer(barrier ready[], barrier filled[], float* buffer, float* in,
int N, int buffer_len)
{
    for (int i = 0; i < (N/buffer_len); ++i) {
        ready[i%2].arrive_and_wait(); /* wait for buffer_(i%2) to be ready to be filled
*/
        /* produce, i.e., fill in, buffer_(i%2) */
        barrier::arrival_token token = filled[i%2].arrive(); /* buffer_(i%2) is filled
*/
    }
}

__device__ void consumer(barrier ready[], barrier filled[], float* buffer, float* out,
int N, int buffer_len)
```

(continued from previous page)

```lisp
{
    barrier::arrival_token token1 = ready[0].arrive(); /* buffer_0 is ready for
initial fill */
    barrier::arrival_token token2 = ready[1].arrive(); /* buffer_1 is ready for
initial fill */
    for (int i = 0; i < (N/buffer_len); ++i) {
        filled[i%2].arrive_and_wait(); /* wait for buffer_(i%2) to be filled */
        /* consume buffer_(i%2) */
        barrier::arrival_token token = ready[i%2].arrive(); /* buffer_(i%2) is ready
to be re-filled */
    }
}

//N is the total number of float elements in arrays in and out
__global__ void producer_consumer_pattern(int N, int buffer_len, float* in, float*
out) {

    // Shared memory buffer declared below is of size 2 * buffer_len
    // so that we can alternatively work between two buffers.
    // buffer_0 = buffer and buffer_1 = buffer + buffer_len
    __shared__ extern float buffer[];

    // bar[0] and bar[1] track if buffers buffer_0 and buffer_1 are ready to be filled,
    // while bar[2] and bar[3] track if buffers buffer_0 and buffer_1 are filled-in
respectively
    __shared__ barrier bar[4];

    auto block = cooperative_groups::this_thread_block();
    if (block.thread_rank() < 4)
        init(bar + block.thread_rank(), block.size());
    block.sync();

    if (block.thread_rank() < warpSize)
        producer(bar, bar+2, buffer, in, N, buffer_len);
    else
        consumer(bar, bar+2, buffer, out, N, buffer_len);
}
```

In this example the first warp is specialized as the producer and the remaining warps are specialized as the consumer. All producer and consumer threads participate (call bar.arrive() or bar. arrive\_and\_wait()) in each of the four cuda::barriers so the expected arrival counts are equal to block.size().

A producer thread waits for the consumer threads to signal that the shared memory bufer can be filled. In order to wait for a cuda::barrier a producer thread must first arrive on that ready[i%2]. arrive() to get a token and then ready[i%2].wait(token) with that token. For simplicity ready[i%2].arrive\_and\_wait() combines these operations.

```javascript
bar.arrive_and_wait();
/* is equivalent to */
bar.wait(bar.arrive());
```

Producer threads compute and fill the ready bufer, they then signal that the bufer is filled by arriving on the filled barrier, filled[i%2].arrive(). A producer thread does not wait at this point, instead it waits until the next iteration’s bufer (double bufering) is ready to be filled.

A consumer thread begins by signaling that both bufers are ready to be filled. A consumer thread does not wait at this point, instead it waits for this iteration’s bufer to be filled, filled[i%2]. arrive\_and\_wait(). After the consumer threads consume the bufer they signal that the bufer is ready to be filled again, ready[i%2].arrive(), and then wait for the next iteration’s bufer to be filled.

## 10.26.6. Early Exit (Dropping out of Participation)

When a thread that is participating in a sequence of synchronizations must exit early from that sequence, that thread must explicitly drop out of participation before exiting. The remaining participating threads can proceed normally with subsequent cuda::barrier arrive and wait operations.

```cpp
#include <cuda/barrier>
#include <cooperative_groups.h>

__device__ bool condition_check();

__global__ void early_exit_kernel(int N) {
    using barrier = cuda::barrier<cuda::thread_scope_block>;
    __shared__ barrier bar;
    auto block = cooperative_groups::this_thread_block();

    if (block.thread_rank() == 0)
        init(&bar , block.size());
    block.sync();

    for (int i = 0; i < N; ++i) {
        if (condition_check()) {
            bar.arrive_and_drop();
            return;
        }
        /* other threads can proceed normally */
        barrier::arrival_token token = bar.arrive();
        /* code between arrive and wait */
        bar.wait(std::move(token)); /* wait for all threads to arrive */
        /* code after wait */
    }
}
```

This operation arrives on the cuda::barrier to fulfill the participating thread’s obligation to arrive in the current phase, and then decrements the expected arrival count for the next phase so that this thread is no longer expected to arrive on the barrier.

## 10.26.7. Completion Function

The CompletionFunction of cuda::barrier<Scope, CompletionFunction> is executed once per phase, after the last thread arrives and before any thread is unblocked from the wait. Memory operations performed by the threads that arrived at the barrier during the phase are visible to the thread executing the CompletionFunction, and all memory operations performed within the CompletionFunction are visible to all threads waiting at the barrier once they are unblocked from the wait.

```cpp
#include <cuda/barrier>
#include <cooperative_groups.h>
#include <functional>
namespace cg = cooperative_groups;

__device__ int divergent_compute(int*, int);
__device__ int independent_computation(int*, int);

__global__ void psum(int* data, int n, int* acc) {
    auto block = cg::this_thread_block();

    constexpr int BlockSize = 128;
    __shared__ int smem[BlockSize];
    assert(BlockSize == block.size());
    assert(n % 128 == 0);

    auto completion_fn = [&] {
        int sum = 0;
        for (int i = 0; i < 128; ++i) sum += smem[i];
        *acc += sum;
    };

    // Barrier storage
    // Note: the barrier is not default-constructible because
    //     completion_fn is not default-constructible due
    //     to the capture.
    using completion_fn_t = decltype(completion_fn);
    using barrier_t = cuda::barrier<cuda::thread_scope_block,
                             completion_fn_t>;
    __shared__ std::aligned_storage<sizeof(barrier_t),
                             alignof(barrier_t)> bar_storage;

    // Initialize barrier:
    barrier_t* bar = (barrier_t*)&bar_storage;
    if (block.thread_rank() == 0) {
        assert(*acc == 0);
        assert(blockDim.x == blockDim.y == blockDim.y == 1);
        new (bar) barrier_t{block.size(), completion_fn};
        // equivalent to: init(bar, block.size(), completion_fn);
    }
    block.sync();

    // Main loop
    for (int i = 0; i < n; i += block.size()) {
        smem[block.thread_rank()] = data[i] + *acc;
        auto t = bar->arrive();
        // We can do independent computation here
        bar->wait(std::move(t));
        // shared-memory is safe to re-use in the next iteration
        // since all threads are done with it, including the one
        // that did the reduction
    }
}
```

## 10.26.8. Memory Barrier Primitives Interface

Memory barrier primitives are C-like interfaces to cuda::barrier functionality. These primitives are available through including the <cuda\_awbarrier\_primitives.h> header

## 10.26.8.1 Data Types

```c
typedef /* implementation defined */ __mbarrier_t;
typedef /* implementation defined */ __mbarrier_token_t;
```

## 10.26.8.2 Memory Barrier Primitives API

```c
uint32_t __mbarrier_maximum_count();
void __mbarrier_init(__mbarrier_t* bar, uint32_t expected_count);
```

▶ bar must be a pointer to \_\_shared\_\_ memory.

expected\_count <= \_\_mbarrier\_maximum\_count()

▶ Initialize \*bar expected arrival count for the current and next phase to expected\_count.

```txt
void __mbarrier_inval(__mbarrier_t* bar);
```

▶ bar must be a pointer to the mbarrier object residing in shared memory.

▶ Invalidation of \*bar is required before the corresponding shared memory can be repurposed.

```txt
__mbarrier_token_t __mbarrier_arrive(__mbarrier_t* bar);
```

Initialization of \*bar must happen before this call.

Pending count must not be zero.

▶ Atomically decrement the pending count for the current phase of the barrier.

▶ Return an arrival token associated with the barrier state immediately prior to the decrement.

```txt
_mbarrier_token_t __mbarrier_arrive_and_drop(__mbarrier_t* bar);
```

▶ Initialization of \*bar must happen before this call.

▶ Pending count must not be zero.

▶ Atomically decrement the pending count for the current phase and expected count for the next phase of the barrier.

▶ Return an arrival token associated with the barrier state immediately prior to the decrement.

```txt
bool __mbarrier_test_wait(__mbarrier_t* bar, __mbarrier_token_t token);
```

token must be associated with the immediately preceding phase or current phase of \*this.

▶ Returns true if token is associated with the immediately preceding phase of \*bar, otherwise returns false.

```txt
//Note: This API has been deprecated in CUDA 11.1
uint32_t __mbarrier_pending_count(__mbarrier_token_t token);
```

## 10.27. Asynchronous Data Copies
