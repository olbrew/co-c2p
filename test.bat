ECHO "Testing \`test/good.c\`, this should work."
python src/C2P.py test/good.c output.p

ECHO "Testing \`test/bad.c\` files, these should give errors"
python src/C2P.py test/bad1.c output.p

python src/C2P.py test/bad2.c output.p

python src/C2P.py test/bad3.c output.p

:: Keep the CLI open so the user can examine the output of this script
PAUSE
