

l:()
do[48;l,:0]
l,:til 10
do[7;l,:0]
l,:1 2 3 4 5 6 7 8 0 1 2 3 4 5 6 7 0 9 2 3 4 5 6 7 8 9

weights:8 7 6 5 4 3 2 10 0 9 8 7 6 5 4 3 2f

validvin_atom:{[s]
 $[s[8] = "X"; [chkdgt: 10]; [chkdgt: l["i"$s[8]]]];
 l2: {[x] "f"$l["i"$x]} each s;
 dot:l2$weights;
 remain: dot mod 11;
 chkdgt = remain}

validvin:{[s]
 if[0h <> type s; s:enlist s];
 validvin_atom each s}