# Memory Barrier Primitives (__mbarrier)

Memory barrier primitives are C-like interfaces to `cuda::barrier` functionality. These primitives are available through including the `<cuda_awbarrier_primitives.h>` header [CUDA_C_Programming_Guide:L9467-L9537].

## Data Types

The following implementation-defined types are used to represent barrier states and tokens:

```c
typedef /* implementation defined */ __mbarrier_t;
typedef /* implementation defined */ __mbarrier_token_t;
```

[ CUDA_C_Programming_Guide:L9467-L9537 ]

## API Reference

### Initialization and Configuration

#### `__mbarrier_maximum_count`

```c
uint32_t __mbarrier_maximum_count();
```

Returns the maximum count supported by the barrier implementation [CUDA_C_Programming_Guide:L9467-L9537].

#### `__mbarrier_init`

```c
void __mbarrier_init(__mbarrier_t* bar, uint32_t expected_count);
```

Initializes `*bar` with an expected arrival count for the current and next phase [CUDA_C_Programming_Guide:L9467-L9537].

**Constraints:**
*   `bar` must be a pointer to `__shared__` memory [CUDA_C_Programming_Guide:L9467-L9537].
*   `expected_count` must be less than or equal to `__mbarrier_maximum_count()` [CUDA_C_Programming_Guide:L9467-L9537].

[ CUDA_C_Programming_Guide:L9467-L9537 ]

### Invalidation

#### `__mbarrier_inval`

```c
void __mbarrier_inval(__mbarrier_t* bar);
```

Invalidates `*bar`. This is required before the corresponding shared memory can be repurposed [CUDA_C_Programming_Guide:L9467-L9537].

**Constraints:**
*   `bar` must be a pointer to the mbarrier object residing in shared memory [CUDA_C_Programming_Guide:L9467-L9537].

[ CUDA_C_Programming_Guide:L9467-L9537 ]

### Arrival and Tokens

#### `__mbarrier_arrive`

```c
__mbarrier_token_t __mbarrier_arrive(__mbarrier_t* bar);
```

Atomically decrements the pending count for the current phase of the barrier and returns an arrival token associated with the barrier state immediately prior to the decrement [CUDA_C_Programming_Guide:L9467-L9537].

**Constraints:**
*   Initialization of `*bar` must happen before this call [CUDA_C_Programming_Guide:L9467-L9537].
*   Pending count must not be zero [CUDA_C_Programming_Guide:L9467-L9537].

[ CUDA_C_Programming_Guide:L9467-L9537 ]

#### `__mbarrier_arrive_and_drop`

```c
__mbarrier_token_t __mbarrier_arrive_and_drop(__mbarrier_t* bar);
```

Atomically decrements the pending count for the current phase and the expected count for the next phase of the barrier. Returns an arrival token associated with the barrier state immediately prior to the decrement [CUDA_C_Programming_Guide:L9467-L9537].

**Constraints:**
*   Initialization of `*bar` must happen before this call [CUDA_C_Programming_Guide:L9467-L9537].
*   Pending count must not be zero [CUDA_C_Programming_Guide:L9467-L9537].

[ CUDA_C_Programming_Guide:L9467-L9537 ]

### Testing and Waiting

#### `__mbarrier_test_wait`

```c
bool __mbarrier_test_wait(__mbarrier_t* bar, __mbarrier_token_t token);
```

Returns `true` if `token` is associated with the immediately preceding phase of `*bar`, otherwise returns `false` [CUDA_C_Programming_Guide:L9467-L9537].

**Constraints:**
*   `token` must be associated with the immediately preceding phase or current phase of `*bar` [CUDA_C_Programming_Guide:L9467-L9537].

[ CUDA_C_Programming_Guide:L9467-L9537 ]

### Deprecated APIs

#### `__mbarrier_pending_count`

```c
uint32_t __mbarrier_pending_count(__mbarrier_token_t token);
```

**Note:** This API has been deprecated in CUDA 11.1 [CUDA_C_Programming_Guide:L9467-L9537].

[ CUDA_C_Programming_Guide:L9467-L9537 ]
