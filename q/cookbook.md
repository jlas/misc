# kdb+/q cookbook

### Setting items into a context from a dictionary

```q
/ d is some dictionary
((set) .) each (enlist each key[d]),'(enlist each value[d])

/ e.g.
q)t1:([] x:1 2 3; y:11 12 13)
q)t2:([] a:100 200 300; b:10 20 30)
q)d:`t1`t2!(t1;t2)
q)delete t1, t2 from `.
`.
q)t1
't1
  [0]  t1
       ^
q)t2
't2
  [0]  t2
q)((set) .) each (enlist each key[d]),'(enlist each value[d])
`t1`t2
q)t1
x y
----
1 11
2 12
3 13
q)t2
a   b
------
100 10
200 20
```

### Generate an identity matrix with dimension N
```q
ident_v1:{[N] reverse (`int$) each #[-1*N;] each (0b vs) each (`int$) each xexp[2;] each til N}
ident_v2:{[N] {(x#0),1,(y-x+1)#0}[;N] each til N}
ident_v3:{[N] rotate[;1,(N-1)#0] each -1*til N}

/ e.g.
q)ident_v1[3]
1 0 0
0 1 0
0 0 1
q)\ts ident_v1[100]
0 65312
q)\ts ident_v2[100]
0 105328
q)\ts ident_v3[100]
0 106400

/ Note: ident_v1 does not work when xexp[2;N] is too large to represent
```
### Extract diagonal from a matrix
```q
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
### Euclidean distance matrix (edm)
 * See https://arxiv.org/abs/1502.07541
```q
/ x is a square matrix (list of float vectors)
edm:{m:x mmu flip[x]; diag[m] + flip diag[m] - 2*m}

/ e.g.
q)t:(41.2317 98.77844 38.67353; 72.6781 40.46546 83.55065; 64.2737 58.30262 14.24935)
q)edm[t]
0        6403.236 2765.767
6403.236 0        5191.468
2765.767 5191.468 0
```
 * Double check with Python
```python
>>> import numpy as np
>>> from scipy.spatial.distance import pdist
>>> a = np.array([[41.2317, 98.77844, 38.67353],[72.6781, 40.46546, 83.55065],[64.2737, 58.30262, 14.24935]])
>>> pdist(a)**2
array([6403.23560893, 2765.76633734, 5191.46839792])
```
