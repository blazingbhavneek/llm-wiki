# CUDA Module

CUDA modules are dynamically loadable packages of device code and data, akin to DLLs in Windows, that are output by `nvcc` [CUDA_C_Programming_Guide:L20172-L20176]. The names for all symbols, including functions, global variables, and texture or surface references, are maintained at module scope so that modules written by independent third parties may interoperate in the same CUDA context [CUDA_C_Programming_Guide:L20176-L20180].

## Loading and Execution

Modules can be loaded from existing PTX files or compiled and loaded directly from PTX source code. The Driver API provides functions such as `cuModuleLoad`, `cuModuleLoadData`, and `cuModuleLoadDataEx` for module management.

### Loading from PTX Files

A module can be loaded directly from a PTX file using `cuModuleLoad`, after which a specific kernel function can be retrieved using `cuModuleGetFunction` [CUDA_C_Programming_Guide:L20182-L20190].

```c
CUmodule cuModule;
cuModuleLoad(&cuModule, "myModule.ptx");
CUfunction myKernel;
cuModuleGetFunction(&myKernel, cuModule, "MyKernel");
```

### Compiling and Loading from PTX Code

Modules can be compiled and loaded from PTX code strings using `cuModuleLoadDataEx`. This function allows for the configuration of JIT compilation options, such as error logging buffers and target context specifications [CUDA_C_Programming_Guide:L20192-L20216].

```c
#define BUFFER_SIZE 8192
CUmodule cuModule;
CUjit_option options[3];
void* values[3];
char* PTXCode = "some PTX code";
char error_log[BUFFER_SIZE];
int err;
options[0] = CU_JIT_ERROR_LOG_BUFFER;
values[0] = (void*)error_log;
options[1] = CU_JIT_ERROR_LOG_BUFFER_SIZE_BYTES;
values[1] = (void*)BUFFER_SIZE;
options[2] = CU_JIT_TARGET_FROM_CUCONTEXT;
values[2] = 0;
err = cuModuleLoadDataEx(&cuModule, PTXCode, 3, options, values);
if (err != CUDA_SUCCESS)
    printf("Link error:\n%s\n", error_log);
```

### Linking Multiple PTX Sources

Multiple PTX sources can be compiled, linked, and loaded into a single module using the `cuLinkCreate`, `cuLinkAddData`, `cuLinkComplete`, and `cuModuleLoadData` functions. This process supports detailed logging of both information and errors, as well as timing the link operation [CUDA_C_Programming_Guide:L20218-L20256].

```c
#define BUFFER_SIZE 8192
CUmodule cuModule;
CUjit_option options[6];
void* values[6];
float walltime;
char error_log[BUFFER_SIZE], info_log[BUFFER_SIZE];
char* PTXCode0 = "some PTX code";
char* PTXCode1 = "some other PTX code";
CUlinkState linkState;
int err;
void* cubin;
size_t cubinSize;
options[0] = CU_JIT_WALL_TIME;
values[0] = (void*)&walltime;
options[1] = CU_JIT_INFO_LOG_BUFFER;
values[1] = (void*)info_log;
options[2] = CU_JIT_INFO_LOG_BUFFER_SIZE_BYTES;
values[2] = (void*)BUFFER_SIZE;
options[3] = CU_JIT_ERROR_LOG_BUFFER;
values[3] = (void*)error_log;
options[4] = CU_JIT_ERROR_LOG_BUFFER_SIZE_BYTES;
values[4] = (void*)BUFFER_SIZE;
options[5] = CU_JIT_LOG_VERBOSE;
values[5] = (void*)1;
cuLinkCreate(6, options, values, &linkState);
err = cuLinkAddData(linkState, CU_JIT_INPUT_PTX,
                    (void*)PTXCode0, strlen(PTXCode0) + 1, 0, 0, 0, 0);
if (err != CUDA_SUCCESS)
    printf("Link error:\n%s\n", error_log);
err = cuLinkAddData(linkState, CU_JIT_INPUT_PTX,
                    (void*)PTXCode1, strlen(PTXCode1) + 1, 0, 0, 0, 0);
if (err != CUDA_SUCCESS)
    printf("Link error:\n%s\n", error_log);
cuLinkComplete(linkState, &cubin, &cubinSize);
printf("Link completed in %fms. Linker Output:\n%s\n", walltime, info_log);
cuModuleLoadData(cuModule, cubin);
cuLinkDestroy(linkState);
```

Full code examples for these operations can be found in the `ptxjit` CUDA sample [CUDA_C_Programming_Guide:L20254-L20256].
