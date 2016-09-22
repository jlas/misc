/
 * k nearest neighbors
 *
 * test:
 *   q)t:(`a`b`c!) each {3?100} each til 1000000
 *   q)\ts knn[t;1 1 1;5]
 *   2155 136389072
 *
 * iris test:
 *   q)iris:flip `sl`sw`pl`pw`class!("FFFFS";",") 0: `:iris.csv
 *   q)\ts kmeans[delete class from iris;3]
 *   25 77184
\
knn:{[t;p;k]
 dist:sqrt (+/) each xexp[;2] each (p -) each (value each t);
 k # `dist xasc update dist:dist from t}

/
 * k means clustering
\
hlpr:{[t;k;means]
 f:{[t;x] sqrt (+/) each xexp[;2] each (x -) each (value each t)};
 r:f[t;] each means;
 zipped:{[k;x] (til k) ,' x}[k;] each flip r;
 cluster:first flip ({$[last x < last y;x;y]} over) each zipped;
 / 1st column keeps count
 m2::(k;(1+count t[0]))#0;
 {m2[first x]+:1,1 _ x} each cluster ,' value each t;
 m2::flip m2;
 (flip 1 _ m2) % first m2}

kmeans:{[t;k]
 means:t[k?count t];
 diff:(k;count t[0])#1;
 while[any any diff;
  omeans:means;
  means:hlpr[t;k;means];
  diff:0.01<abs omeans-means];
 flip (cols t)!flip means}

/masks:{(x =) each cluster} each til k;
/(sum flip r * masks) % sum flip masks}
