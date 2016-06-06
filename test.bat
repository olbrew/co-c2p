ECHO "Testing \`test/good.c\`, this should work."
python src/C2P.py tests/good.c output.p

ECHO "Testing \`test/bad.c\` files, these should give errors"
python src/C2P.py tests/bad1.c output.p

python src/C2P.py tests/bad2.c output.p

python src/C2P.py tests/bad3.c output.p

:: Keep the CLI open so the user can examine the output of this script
PAUSE
