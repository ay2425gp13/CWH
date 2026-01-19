@echo off
SETLOCAL

REM Simple launcher: tries Python first, then Node (npx serve).
REM Serves the repo root so frontend files are available at http://127.0.0.1:%PORT%/

SET PORT=8000
SET TARGET=http://127.0.0.1:%PORT%/frontend/platform-market.html

echo ------------------------------------------------------------
echo  Smile & Sunshine Toy - Local Preview
echo  Trying to start a static server on port %PORT% ...
echo ------------------------------------------------------------

REM Prefer Python if available
python -c "import sys" >NUL 2>&1
IF %ERRORLEVEL%==0 (
  echo Detected Python. Starting python -m http.server %PORT% ...
  start "" "%SystemRoot%\System32\cmd.exe" /c "python -m http.server %PORT%"
  goto open_browser
)

REM Fallback to Node npx serve (requires Node + npx)
npx --version >NUL 2>&1
IF %ERRORLEVEL%==0 (
  echo Python not found. Detected Node. Starting npx serve -l %PORT% ...
  start "" "%SystemRoot%\System32\cmd.exe" /c "npx serve -l %PORT% ."
  goto open_browser
)

echo.
echo No Python or Node environment detected.
echo Please install either Python 3 (recommended) or Node.js (with npx).
pause
goto end

:open_browser
REM Give the server a brief moment to start
ping 127.0.0.1 -n 3 >NUL
echo Opening %TARGET% ...
start "" "%TARGET%"
goto end

:end
ENDLOCAL

