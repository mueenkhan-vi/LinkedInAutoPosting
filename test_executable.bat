@echo off
setlocal enabledelayedexpansion

cd /d "c:\Users\mueen\OneDrive\Desktop\VSCode\LinkedIn\installer"

echo.
echo ============================================================
echo Testing LinkedIn Agent Executable
echo ============================================================
echo.

echo This will test the executable with a dummy topic.
echo Please wait...
echo.

REM Create a test input file
(
    echo test_topic_for_linkedin
    echo no
) > test_input.txt

REM Run the executable with input
LinkedInAgent.exe < test_input.txt

REM Clean up
del test_input.txt

echo.
echo ============================================================
echo Test complete!
echo ============================================================
