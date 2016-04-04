param NJ;
param NK;
param NI;

set J := 0 .. NJ;
set K := 1 .. NK;
set I := 1 .. NI;

param wdc;
param wic;
param wcc;
param r{I} default 0;
param deltadc{K,J} default 0.0;
param deltacc{K,J} default 0.0;
param deltaIC{J,J} default 0.0;


var y{K,J} binary;
var x{I,J} binary;


minimize v: wdc*sum{k in K, j in J} (deltadc[k,j] * y[k,j])+ wcc*sum{k in K, j in J} (deltacc[k,j] * y[k,j])+wic*sum{i in I, j in J} (deltaIC[r[i],j] * x[i,j]);
s.t. capacity{j in J}: sum{i in I} x[i,j] <= sum{k in K} y[k,j];
s.t. assign{i in I}: sum{j in J: j >= r[i]} x[i,j] = 1;
s.t. fixtozero{j in J, k in K: k < NK}: y[k,j] >= y[k+1,j];
s.t.  checkD{i in I}: sum{j in J} x[i,j] =1;

solve;
display y;
display v;
display x;
printf "FILIPPO: %f\n",sum{k in K, j in J} (deltadc[k,j] * y[k,j])+ sum{k in K, j in J} (deltacc[k,j] * y[k,j])+sum{i in I, j in J} (deltaIC[r[i],j] * x[i,j]);
