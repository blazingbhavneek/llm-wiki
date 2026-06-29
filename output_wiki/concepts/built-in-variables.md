# Built-in Variables

Built-in variables specify the grid and block dimensions and the block and thread indices. They are only valid within functions that are executed on the device [CUDA_C_Programming_Guide:L6851-L6852].

## gridDim

The `gridDim` variable is of type `dim3` and contains the dimensions of the grid [CUDA_C_Programming_Guide:L6855-L6856].

## blockIdx

The `blockIdx` variable is of type `uint3` and contains the block index within the grid [CUDA_C_Programming_Guide:L6859-L6860].
