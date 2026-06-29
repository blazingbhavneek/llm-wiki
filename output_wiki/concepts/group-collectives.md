# Group Collectives

The Cooperative Groups library provides a set of collective operations that can be performed by a group of threads. These operations require participation of all threads in the specified group in order to complete the operation [CUDA_C_Programming_Guide:L12561-L12565].

All threads in the group need to pass the same values for corresponding arguments to each collective call, unless different values are explicitly allowed in the argument description. Otherwise, the behavior of the call is undefined [CUDA_C_Programming_Guide:L12561-L12565].
