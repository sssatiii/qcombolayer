@echo off
echo ================================
echo   QcomboLayer Development Sync
echo ================================
echo.

REM Source and destination paths
set SOURCE="c:\iNFRA\proj-infra\DOH AI\Data\QGIS-proj\pyQGIS\qcombolayer"
set DEST="%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\QcomboLayer"

REM Sync files
echo Syncing plugin files...
robocopy %SOURCE% %DEST% /MIR /XD __pycache__ .git /XF *.pyc *.pyo

REM Check if sync was successful
if %errorlevel% leq 1 (
    echo.
    echo ✅ Sync completed successfully!
    echo.
    echo 📝 Next steps:
    echo 1. Open QGIS
    echo 2. Install "Plugin Reloader" if not installed yet
    echo 3. Press F5 or use Plugin Reloader to reload QcomboLayer
    echo.
) else (
    echo.
    echo ❌ Sync failed! Error level: %errorlevel%
    echo.
)

echo Press any key to exit...
pause >nul
