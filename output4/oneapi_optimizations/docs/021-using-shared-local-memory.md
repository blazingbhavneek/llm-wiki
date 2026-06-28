
## Using Shared Local Memory

If the number of histogram bins gets larger than, for example, 1024, there will not be enough register space for private bins even the private bins are shared in the same sub-group. To reduce memory traffic, the loca histogram bins can be allocated in the shared local memory and shared by work items in the same workgroup. Refer to the “Shared Local Memory” chapter and see how it is done in the histogram example there.
