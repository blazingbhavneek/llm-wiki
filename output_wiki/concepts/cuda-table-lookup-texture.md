# CUDA Table Lookup Using Textures

This technique leverages CUDA texture filtering to implement a table lookup function $TL(x)$ where the input $x$ spans the interval $[0, R]$. By carefully mapping the input range to texture coordinates, the method ensures that boundary values are correctly retrieved from the texture array.

## Formula and Boundary Conditions

For a one-dimensional texture with $N$ elements, a table lookup $TL(x)$ where $x$ spans the interval $[0, R]$ can be implemented using the following formula:

$$ TL(x) = tex((N - 1) / R) x + 0.5) $$

This specific coordinate mapping ensures two critical boundary conditions are met:

1.  $TL(0) = T[0]$: The lookup at the start of the interval returns the first element of the texture.
2.  $TL(R) = T[N - 1]$: The lookup at the end of the interval returns the last element of the texture.

## Example Implementation

Figure 38 illustrates the use of texture filtering to implement a table lookup with $R=4$ or $R=1$ from a one-dimensional texture with $N=4$ using linear filtering [CUDA_C_Programming_Guide:L19429-L19437].

![One-Dimensional Table Lookup Using Linear Filtering](images/89e823f2e9056596055c9a6244f7035950127ee991ea576680a185263ab93230.jpg)

*Figure 38: One-Dimensional Table Lookup Using Linear Filtering [CUDA_C_Programming_Guide:L19429-L19437]*

## References

- [CUDA_C_Programming_Guide:L19429-L19437] CUDA C Programming Guide, Section 19.3. Table Lookup.
