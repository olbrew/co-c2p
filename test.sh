#! /bin/bash

printf "Testing \`test/good.c\`, this should work.\n"
python3 src/C2P.py tests/good.c output.p
printf "\n"

printf "Testing \`test/bad.c\` files, these should give errors\n"
python3 src/C2P.py tests/bad1.c output.p
printf "\n"
python3 src/C2P.py tests/bad2.c output.p
printf "\n"
python3 src/C2P.py tests/bad3.c output.p
