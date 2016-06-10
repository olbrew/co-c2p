@echo OFF

ECHO "Testing good c files. These should work."
for %%f in (tests\good\*.c) do (
        ECHO "Testing " %%~nf "..."
        python3 c2p/C2P.py %%~nf output.p
        ECHO "SUCCES"
)
ECHO.

printf "Testing bad c files. These should give errors."
for %%f in (tests\bad\*.c) do (
        ECHO "Testing " %%~nf "..."
        python3 c2p/C2P.py %%~nf output.p
        ECHO.
)

:: Keep the CLI open so the user can examine the output of this script
PAUSE
