The following is a tutorial that I used to set up passwordless SSH. On this cluster, gsapp13 is the login node with a shared file system. We also have other compute nodes like gsappx1-4.

## connect the login node
```
ssh qiany@gsapp13.umd.edu
```

## generate an SSH key
```
ssh-keygen -t rsa -b 4096 -C "mpi_key"
```

## copy to gsappx1-4 nodes
```
ssh-copy-id qiany@gsappx1
ssh-copy-id qiany@gsappx2
ssh-copy-id qiany@gsappx3
ssh-copy-id qiany@gsappx4
```

## test if passwordless SSH is successfully
```
ssh gsappx2 hostname  # ✅ Should not ask for a password
```

Once that works, try:
```
mpirun -np 8 --host gsappx1,gsappx2 python hello_mpi.py
```

Note:
Currently, I do not have a home directory "/home/qiany" on gsappx4. I may need to contact the IT to use it gsappx4 on this cluster.
