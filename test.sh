#! /bin/sh

printf "Testing good c files. These should work.\n"
for GOOD in tests/good/*.c
do
        printf "Testing %s ...\n" "$GOOD"
        python3 c2p/C2P.py "$GOOD" output.p
        printf "SUCCES\n\n"
done
printf "\n"

printf "Testing bad c files. These should give errors.\n"
for BAD in tests/bad/*.c
do
        printf "Testing %s ...\n" "$BAD"
        python3 c2p/C2P.py "$BAD" output.p
        printf "\n"
done
