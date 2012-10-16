set xrange [20:100]
set xlabel "step"
set ylabel "error"
plot "data" using 1:4 with lines lw 2 title 'max', "data" using 1:2 with lines lw 2 title 'avg', "data" using 1:3 with lines lw 2 title 'min'