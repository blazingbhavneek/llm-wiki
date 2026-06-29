# Error Log Management

**Warning:** This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA [CUDA_C_Programming_Guide:L20660-L20663].

The Error Log Management mechanism allows for CUDA API errors to be reported to developers in a plain-English format that describes the cause of the issue [CUDA_C_Programming_Guide:L20664-L20666].

## Background

Traditionally, the only indication of a failed CUDA API call is the return of a non-zero code. As of CUDA Toolkit 12.9, the CUDA Runtime defines over 100 different return codes for error conditions, but many of them are generic and give the developer no assistance with debugging the cause [CUDA_C_Programming_Guide:L20667-L20673].

## Activation

Logs can be activated by setting the `CUDA_LOG_FILE` environment variable. Acceptable values are `stdout`, `stderr`, or a valid path on the system to write a file [CUDA_C_Programming_Guide:L20667-L20673]. The log buffer can be dumped via API even if `CUDA_LOG_FILE` was not set before program execution [CUDA_C_Programming_Guide:L20667-L20673]. Note that an error-free execution may not print any logs [CUDA_C_Programming_Guide:L20667-L20673].

## Output Format

Logs are output in the following format:

```powershell
[Time][TID][Source][Severity][API Entry Point] Message
```

For example, if a developer tries to dump the Error Log Management logs to an unallocated buffer, the generated error message is:

```txt
[22:21:32.099][25642][CUDA][E][cuLogsDumpToMemory] buffer cannot be NULL
```

Previously, the developer would have received only `CUDA_ERROR_INVALID_VALUE` in the return code and possibly "invalid argument" if `cuGetErrorString` is called [CUDA_C_Programming_Guide:L20674-L20689].

## API Description

The CUDA Driver provides APIs in two categories for interacting with the Error Log Management feature [CUDA_C_Programming_Guide:L20690-L20731].

### Callback Registration

This feature allows developers to register callback functions to be used whenever an error log is generated. The callback signature is:

```txt
void callbackFunc(void *data, CUlogLevel logLevel, char *message, size_t length)
```

Callbacks are registered with the following API:

```txt
CUresult cuLogsRegisterCallback(CUlogsCallback callbackFunc, void *userData,
    CUlogsCallbackHandle *callback_out)
```

Where `userData` is passed to the callback function without modifications. `callback_out` should be stored by the caller for use in `cuLogsUnregisterCallback` [CUDA_C_Programming_Guide:L20690-L20731].

Unregistration is performed via:

```txt
CUresult cuLogsUnregisterCallback(CUlogsCallbackHandle callback)
```

### Log Management

The other set of API functions are for managing the output of logs. An important concept is the log iterator, which points to the current end of the buffer [CUDA_C_Programming_Guide:L20690-L20731].

```txt
CUresult cuLogsCurrent(CUlogIterator *iterator_out, unsigned int flags)
```

The iterator position can be kept by the calling software in situations where a dump of the entire log buffer is not desired. Currently, the `flags` parameter must be 0, with additional options reserved for future CUDA releases [CUDA_C_Programming_Guide:L20690-L20731].

At any time, the error log buffer can be dumped to either a file or memory with these functions:

```txt
CUresult cuLogsDumpToFile(CUlogIterator *iterator, const char *pathToFile, unsigned int flags)
CUresult cuLogsDumpToMemory(CUlogIterator *iterator, char *buffer, size_t *size, unsigned int flags)
```

If `iterator` is NULL, the entire buffer will be dumped, up to the maximum of 100 entries. If `iterator` is not NULL, logs will be dumped starting from that entry and the value of `iterator` will be updated to the current end of the logs, as if `cuLogsCurrent` had been called. If there have been more than 100 log entries into the buffer, a note will be added at the start of the dump noting this [CUDA_C_Programming_Guide:L20690-L20731].

The `flags` parameter must be 0, with additional options reserved for future CUDA releases [CUDA_C_Programming_Guide:L20690-L20731].

### Memory Dump Considerations

The `cuLogsDumpToMemory` function has additional considerations [CUDA_C_Programming_Guide:L20732-L20754]:

1. The buffer itself will be null-terminated, but each individual log entry will only be separated by a newline (`\n`) character [CUDA_C_Programming_Guide:L20732-L20754].
2. The maximum size of the buffer is 25600 bytes [CUDA_C_Programming_Guide:L20732-L20754].
3. If the value provided in `size` is not sufficient to store all desired logs, a note will be added as the first entry and the oldest entries that do not fit will not be dumped [CUDA_C_Programming_Guide:L20732-L20754].
4. After returning, `size` will contain the actual number of bytes written to the provided buffer [CUDA_C_Programming_Guide:L20732-L20754].

## Limitations and Known Issues

1. The log buffer is limited to 100 entries. After this limit is reached, the oldest entries will be replaced and log dumps will contain a line noting the rollover [CUDA_C_Programming_Guide:L20732-L20754].
2. Not all CUDA APIs are covered yet. This is an ongoing project to provide better usage error reporting for all APIs [CUDA_C_Programming_Guide:L20732-L20754].
3. The Error Log Management log location (if given) will not be tested for validity until/unless a log is generated [CUDA_C_Programming_Guide:L20732-L20754].
4. The Error Log Management APIs are currently only available via the CUDA Driver. Equivalent APIs will be added to the CUDA Runtime in a future release [CUDA_C_Programming_Guide:L20732-L20754].
5. The log messages are not localized to any language and all provided logs are in US English [CUDA_C_Programming_Guide:L20732-L20754].
