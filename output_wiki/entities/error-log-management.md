# Error Log Management

Describes the Error Log Management mechanism for reporting CUDA API errors in plain-English format, including activation via CUDA_LOG_FILE, log output format, and APIs like cuLogsRegisterCallback and cuLogsDumpToMemory.

> Deterministic fallback: the normal synthesis path could not be verified. This page preserves the full source evidence verbatim with original line citations.
> Reason: page agent failed: Connection error.

## Source CUDA_C_Programming_Guide:L20661-L20753

Citation: [CUDA_C_Programming_Guide:L20661-L20753]

````text
# Chapter 23. Error Log Management

Warning: This document has been replaced by a new CUDA Programming Guide. The information in this document should be considered legacy, and this document is no longer being updated as of CUDA 13.0. Please refer to the CUDA Programming Guide for up-to-date information on CUDA.

The Error Log Management mechanism allows for CUDA API errors to be reported to developers in a plain-English format that describes the cause of the issue.

## 23.1. Background

Traditionally, the only indication of a failed CUDA API call is the return of a non-zero code. As of CUDA Toolkit 12.9, the CUDA Runtime defines over 100 diferent return codes for error conditions, but many of them are generic and give the developer no assistance with debugging the cause.

## 23.2. Activation

Set the CUDA\_LOG\_FILE environment variable. Acceptable values are stdout, stderr, or a valid path on the system to write a file. The log bufer can be dumped via API even if CUDA\_LOG\_FILE was not set before program execution. NOTE: An error-free execution may not print any logs.

## 23.3. Output

Logs are output in the following format:

```powershell
[Time][TID][Source][Severity][API Entry Point] Message
```

The following line is an actual error message that is generated if the developer tries to dump the Error Log Management logs to an unallocated bufer:

```txt
[22:21:32.099][25642][CUDA][E][cuLogsDumpToMemory] buffer cannot be NULL
```

Where before, all the developer would have gotten is CUDA\_ERROR\_INVALID\_VALUE in the return code and possibly “invalid argument” if cuGetErrorString is called.

## 23.4. API Description

The CUDA Driver provides APIs in two categories for interacting with the Error Log Management feature.

This feature allows developers to register callback functions to be used whenever an error log is generated, where the callback signature is:

```txt
void callbackFunc(void *data, CUlogLevel logLevel, char *message, size_t length)
```

Callbacks are registered with this API:

```txt
CUresult cuLogsRegisterCallback(CUlogsCallback callbackFunc, void *userData,
    CUlogsCallbackHandle *callback_out)
```

Where userData is passed to the callback function without modifications. callback\_out should be stored by the caller for use in cuLogsUnregisterCallback.

```txt
CUresult cuLogsUnregisterCallback(CUlogsCallbackHandle callback)
```

The other set of API functions are for managing the output of logs. An important concept is the log iterator, which points to the current end of the bufer:

```txt
CUresult cuLogsCurrent(CUlogIterator *iterator_out, unsigned int flags)
```

The iterator position can be kept by the calling software in situations where a dump of the entire log bufer is not desired. Currently, the flags parameter must be 0, with additional options reserved for future CUDA releases.

At any time, the error log bufer can be dumped to either a file or memory with these functions:

```txt
CUresult cuLogsDumpToFile(CUlogIterator *iterator, const char *pathToFile, unsigned int flags)
CUresult cuLogsDumpToMemory(CUlogIterator *iterator, char *buffer, size_t *size, unsigned int flags)
```

If iterator is NULL, the entire bufer will be dumped, up to the maximum of 100 entries. If iterator is not NULL, logs will be dumped starting from that entry and the value of iterator will be updated to the current end of the logs, as if cuLogsCurrent had been called. If there have been more than 100 log entries into the bufer, a note will be added at the start of the dump noting this.

The flags parameter must be 0, with additional options reserved for future CUDA releases.

The cuLogsDumpToMemory function has additional considerations:

1. The bufer itself will be null-terminated, but each individual log entry will only be separated by a newline (n) character.

2. The maximum size of the bufer is 25600 bytes.

3. If the value provided in size is not suficient to store all desired logs, a note will be added as the first entry and the oldest entries that do not fit will not be dumped.

4. After returning, size will contain the actual number of bytes written to the provided bufer.

## 23.5. Limitations and Known Issues

1. The log bufer is limited to 100 entries. After this limit is reached, the oldest entries will be replaced and log dumps will contain a line noting the rollover.

2. Not all CUDA APIs are covered yet. This is an ongoing project to provide better usage error reporting for all APIs.

3. The Error Log Management log location (if given) will not be tested for validity until/unless a log is generated.

4. The Error Log Management APIs are currently only available via the CUDA Driver. Equivalent APIs will be added to the CUDA Runtime in a future release.

5. The log messages are not localized to any language and all provided logs are in US English.
````
