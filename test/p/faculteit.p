; niet-recursieve faculteitsberekening
ldc i 10	; dit is de beginwaarde waarvan we de faculteit willen berekenen
dpl i
start:
ldo i 0
ldc i 1
equ i
not
fjp einde
ldo i 0
ldc i 1
sub i
mul i
ldo i 0
ldc i 1
sub i
sro i 0
ujp start
einde:
hlt
