# kdb+/q cookbook
* Generate an identity matrix with dimension N
```
diag_v1:{[N] reverse (`int$) each #[-1*N;] each (0b vs) each (`int$) each xexp[2;] each til N}
diag_v2:{[N] {(x#0),1,(y-x+1)#0}[;N] each til N}
```
* e.g.
```
q)diag_v1[3]
1 0 0
0 1 0
0 0 1
q)\ts diag_v1[100]
0 65312
q)\ts diag_v2[100]
0 105328
```
