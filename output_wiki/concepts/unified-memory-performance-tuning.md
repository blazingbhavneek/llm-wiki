# Unified Memory Performance Tuning

To achieve good performance with Unified Memory, developers should focus on three key areas: understanding how paging works on the system and avoiding unnecessary page faults, utilizing mechanisms to keep data local to the accessing processor, and tuning the application for the granularity of memory transfers specific to the system [CUDA_C_Programming_Guide:L21603-L21615].

## Performance Hints

Performance Hints can provide improved performance, but they must be used correctly; incorrect usage may degrade performance compared to the default behavior [CUDA_C_Programming_Guide:L21603-L21615]. Additionally, every hint incurs a performance cost on the host. Therefore, a hint is only useful if the performance improvement it provides is sufficient to overcome this host-side cost [CUDA_C_Programming_Guide:L21603-L21615].

## Related Concepts

*   Memory Paging and Page Sizes
