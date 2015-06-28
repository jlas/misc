// vin.q
//
// author: Juan Lasheras <juan.lasheras@gmail.com>
//
// Written for the Kx Community Meetup competition
//   http://www.meetup.com/kx-nyc/events/223287679/
//


// make ascii to decimal array
ascii2dec:()
do[48;ascii2dec,:0]
ascii2dec,:til 10
do[7;ascii2dec,:0]
ascii2dec,:1 2 3 4 5 6 7 8 0 1 2 3 4 5 6 7 0 9 2 3 4 5 6 7 8 9

// make weights lookup array
// see http://people.virginia.edu/~sns5r/resint/empiostf/checkdigit.htm
weights:8 7 6 5 4 3 2 10 0 9 8 7 6 5 4 3 2f


validvin_atom:{[s]
 $[s[8] = "X"; [chkdgt: 10]; [chkdgt: ascii2dec["i"$s[8]]]];
 l2: {[x] "f"$ascii2dec["i"$x]} each s;
 dot:l2$weights;
 remain: dot mod 11;
 chkdgt = remain}

validvin:{[s]
 if[0h <> type s; s:enlist s];
 validvin_atom each s}