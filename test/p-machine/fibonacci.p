ssp 5
ujp  l5
l2:
ssp 6
ujp  l4
l4:
lod i 0 5
ldc i 0
equ i
fjp  l3
ldc i 0
str i 0 0
retf
ujp  l6
l3:
lod i 0 5
ldc i 1
equ i
fjp  l1
ldc i 1
str i 0 0
retf
ujp  l6
l1:
mst 1
lod i 0 5
ldc i 1
sub i
cup 1 l2
mst 1
lod i 0 5
ldc i 2
sub i
cup 1 l2
add i
str i 0 0
retf
l6:
retf
l5:
mst 0
in i
cup 1 l2
out i
ldc c '\n'
out c
hlt
