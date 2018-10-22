# kdb+/q cookbook
### Generate an identity matrix with dimension N
```
ident_v1:{[N] reverse (`int$) each #[-1*N;] each (0b vs) each (`int$) each xexp[2;] each til N}
ident_v2:{[N] {(x#0),1,(y-x+1)#0}[;N] each til N}

/ e.g.
q)ident_v1[3]
1 0 0
0 1 0
0 0 1
q)\ts ident_v1[100]
0 65312
q)\ts ident_v2[100]
0 105328
```
### Extract diagonal from a matrix
```
diag:{(x .) each til[count x],'til count[x]}

/ e.g.
q)t:{3?100f} each til 3
q)t
41.2317 98.77844 38.67353
72.6781 40.46546 83.55065
64.2737 58.30262 14.24935
q)diag[t]
41.2317 40.46546 14.24935
```

