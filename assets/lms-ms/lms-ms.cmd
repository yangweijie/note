@echo off
rem lms-ms - Windows global launcher
rem 1. Put this file next to lms-ms.py
rem 2. Add that folder to PATH
rem 3. If modelscope is installed in a specific interpreter (e.g. Anaconda),
rem    set LMS_MS_PYTHON to the full path of that python.exe

if defined LMS_MS_PYTHON (
    "%LMS_MS_PYTHON%" "%~dp0lms-ms.py" %*
) else (
    py -3 "%~dp0lms-ms.py" %*
)
exit /b %errorlevel%
