## Intra-Device and Inter-Device Data Transfers for MPI+OpenMP Programs

Some applications are just pure OpenMP programs where a single process uses all available GPU resources. But many other applications use a combination of MPI and OpenMP where multiple MPI ranks are used and each of these MPI ranks uses in turn OpenMP to access some of the GPU resources (either a full GPU or a GPU subdevice).

Typically, such applications will need at some point to exchange data between the GPU resources used by the different ranks. In order to do this, normally, first the data needs to be transferred from the GPU to the CPU that will do the MPI transfer, and once it is received by the target CPU, transferred again to the target GPU.

In principle, transferring data between subdevices of the same GPU should not require to transfer the data first back to the CPU. Also, for systems that use the Intel<sup>®</sup> X<sup>e</sup> Link which allows GPUs to exchange data directly this should not be necessary either.

Besides Intel<sup>®</sup> MPI Library, the Intel<sup>®</sup> Data Center GPU Max Series enabled MPICH library supports direct transfers between GPUs and GPU subdevices to improve communication efficiency.

The MPI primitives of this library are able to determine whether a pointer points to data that is in the GPU even from the CPU and, therefore, it can activate a different communication path that transfers the data directly between the GPU devices or subdevices without the need of transferring the data through the CPUs.

With this in mind, after installing the library, in order to take advantage of it we need to use OpenMP APIs and directives to obtain device pointers that we can then use in the MPI calls to activate the direct GPU communication path. There are two possible scenarios for this:

1. Data was directly allocated on the device by means of omp\_target\_alloc.

When the data is allocated on the device using the omp\_target\_alloc routine (or a similar routine), the returned pointer is a device pointer that can be used directly in the MPI calls. For example:

double \*dst\_buff = omp\_target\_alloc(device\_id, 1000 \* sizeof(double)); MPI\_Recv(dst\_buff,...);

1. Data that was mapped on the device.

If the data was allocated on the device using a map clause or some of OpenMP implicit mapping rules, then we need to use the use\_device\_ptr or use\_device\_addr clauses of the target data directive to get a device pointer that we can use on the MPI calls. For example:

```txt
#pragma omp target data map(dst_buff)
{
    #pragma omp target data use_device_addr(dst_buff)
    {
        MPI_Recv(dst_buff,...)
    }
}
```

Now take a look at a more complex example which allows the user to select by means of a flag if device pointers (in case the Intel<sup>®</sup> Data Center GPU Max Series enabled MPICH library is being used) or host pointers should be used in MPI calls. We will also use this code to showcase the performance difference that can be achieved by using device to device transfers. The code just keeps rotating some buffers across a number of MPI ranks while increasing their value.

We are going to control whether to use device to device transfers or regular MPI transfers by means of the mpi\_aware variable.

```c
int mpi_aware = 0;
if ( argc > 1 ) {
    mpi_aware = 1;
    printf("MPI device aware path enabled\n");
} // argc check
```

The application uses two buffers, buf1 and buf2, so we start by mapping them normally on the device by using a target data construct. Next we use a conditional target data construct to convert the addresses of buf1 and buf2 to device addresses only if mpi\_aware is true. So, if mpi\_aware is true, the curr and next pointers will hold device addresses. Otherwise, they will hold host addresses. This can be observed with the printf statement.

```c
#pragma omp target data map(buf1,buf2)
{
    #pragma omp target data use_device_addr(buf1,buf2) if(mpi_aware)
    {
        curr = buf1;
        next = buf2;
    }
    printf("curr=%p next=%p\n",curr,next);
```

If mpi\_aware is false, printf will print values similar to the following which are host addresses:

```txt
curr=0x7ffdffc11850 next=0x7ffdff470650
```

On the other hand, if mpi\_aware is true, printf will print values similar to the following which are device addresses:

```txt
curr=0xff00000000200000 next=0xff00000000a00000
```

Finally before and after the MPI communication calls we use two conditional target update constructs to update the GPU variables only if mpi\_aware was false as this is not needed if device to device transfers are used.

```c
if ( nranks > 1 ) {
    #pragma omp target update from(curr[0:N]) if(!mpi_aware)
    MPI_Request srq;
    MPI_Isend(curr,N,MPI_DOUBLE,next_rank,0,MPI_COMM_WORLD,&srq);
// we need to make sure that the MPI_Isend of the previous
// iteration finished before doing the MPI_Recv of this
// iteration
if ( step > 0 ) MPI_Wait(&psrq,MPI_STATUS_IGNORE);
psrq = srq;
    MPI_Recv(next,N,MPI_DOUBLE,prev_rank,0,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
    #pragma omp target update to(next[0:N]) if(!mpi_aware)
} // nranks
```

We, first, use this program to evaluate the performance difference in a system with a single GPU which is divided in two subdevices, one for each MPI rank. We can see a significant time difference that is a direct consequence of the reduction of the number of memory operations from the host to the device (M2D operations) and vice versa (D2M operations) which can be obtained with the unitrace tool.

2 MPI ranks

<table><tr><td>Version</td><td>Time (s.)</td><td>M2D operations (per rank)</td><td>D2M operations (per rank)</td></tr><tr><td>mpi_aware = 0</td><td>3.07</td><td>1002</td><td>1002</td></tr><tr><td>mpi_aware = 1</td><td>0.13</td><td>2</td><td>2</td></tr></table>

We can now use the same program to evaluate the performance difference in a system with two GPU devices connected with Intel<sup>®</sup> X<sup>e</sup> Link. In this case, there will be 4 MPI ranks as each GPU will be programmed as two subdevices. We can observe a similar reduction in time and number of memory operations between the host and the device as in the previous case.

4 MPI ranks

<table><tr><td>Version</td><td>Time (s.)</td><td>M2D operations (per rank)</td><td>D2M operations (per rank)</td></tr><tr><td>mpi_aware = 0</td><td>3.45</td><td>1002</td><td>1002</td></tr><tr><td>mpi_aware = 1</td><td>0.44</td><td>2</td><td>2</td></tr></table>

As we have seen a significant improvement in the communication efficiency between GPUs can be achieved when these are connected with the Intel<sup>®</sup> X<sup>e</sup> Link and the Intel<sup>®</sup> Data Center GPU Max Series enabled MPICH library is used.

Note: Using the mpi\_aware path with an MPI library that does not support device-to-device transfers may result in an abnormal termination of the program.
