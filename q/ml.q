/
 * k nearest neighbors
 *
 * test:
 *   q)t:(`a`b`c!) each {3?100} each til 1000000
 *   q)\ts knn[t;1 1 1;5]
 *   2155 136389072
\
knn:{[t;p;k]
 dist:sqrt (+/) each xexp[;2] each (p -) each (value each t);
 k # `dist xasc update dist:dist from t}
