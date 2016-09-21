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

/
 * k means clustering
\
hlpr:{[t;k;means]
 f:{sqrt (+/) each xexp[;2] each (x -) each (value each t)};
 r:f each means;
 zipped:{[k;x] (til k) ,' x}[k;] each flip r;
 cluster:first flip ({$[last x < last y;x;y]} over) each zipped;
 / 1st column keeps count
 m2::(k;(1+count t[0]))#0;
 {m2[first x]+:1,1 _ x} each cluster ,' value each t;
 m2::flip m2;
 (flip 1 _ m2) % first m2}

kmeans:{[t;k]
 means:t[k?count t];
 hlpr[t;k;means]}

/masks:{(x =) each cluster} each til k;
/(sum flip r * masks) % sum flip masks}
