# Nanosleep Function

Verbatim source-backed fallback page for Nanosleep Function.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L8814-L8847

Citation: [CUDA_C_Programming_Guide:L8814-L8847]

````text

## 10.23. Nanosleep Function

## 10.23.1. Synopsis

```txt
void __nanosleep(unsigned ns);
```

## 10.23.2. Description

\_\_nanosleep(ns) suspends the thread for a sleep duration of approximately ns nanoseconds. The maximum sleep duration is approximately 1 millisecond.

It is supported with compute capability 7.0 or higher.

## 10.23.3. Example

The following code implements a mutex with exponential back-of.

```txt
__device__ void mutex_lock(unsigned int *mutex) {
    unsigned int ns = 8;
    while (atomicCAS(mutex, 0, 1) == 1) {
        __nanosleep(ns);
        if (ns < 256) {
            ns *= 2;
        }
    }
}

__device__ void mutex_unlock(unsigned int *mutex) {
    atomicExch(mutex, 0);
}
```
````
