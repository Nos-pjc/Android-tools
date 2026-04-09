@echo off

chcp 65001 >nul

echo ================================
echo Building ADB Tool Package
echo ================================

python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Step 1: Clean old build files...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del *.spec 2>nul

echo Step 2: Install dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo Step 3: Install PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo Error: Failed to install PyInstaller
    pause
    exit /b 1
)

echo Step 4: Build EXE file...
pyinstaller main.py --name=ADB_Tool --onefile --windowed --clean --noconfirm --add-data="resources\styles.qss;resources" --add-data="resources\app_icon.ico;resources" --icon=resources\app_icon.ico --distpath=./dist --workpath=./build --exclude-module=tkinter --exclude-module=unittest --exclude-module=email --exclude-module=urllib3 --exclude-module=requests --exclude-module=pytest --exclude-module=setuptools --exclude-module=pip --exclude-module=wheel --exclude-module=docutils --exclude-module=jinja2 --exclude-module=markupsafe
if errorlevel 1 (
    echo Error: Failed to build EXE
    pause
    exit /b 1
)

echo.
echo Step 5: Verify build result...
if exist "dist\ADB_Tool.exe" (
    echo Build successful!
    echo EXE file location: %cd%\dist\ADB_Tool.exe
    for %%A in ("dist\ADB_Tool.exe") do echo File size: %%~zA bytes
) else (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Step 6: Prepare package files...

set "PACKAGE_DIR=ADB_Tool_Package"
rmdir /s /q %PACKAGE_DIR% 2>nul
mkdir %PACKAGE_DIR%

copy "dist\ADB_Tool.exe" "%PACKAGE_DIR%\"
copy "README.md" "%PACKAGE_DIR%\"
mkdir "%PACKAGE_DIR%\script"

if exist "script\*.json" (
    copy "script\*.json" "%PACKAGE_DIR%\script\"
)

echo.
echo Step 7: Create ZIP package...

powershell -Command "Compress-Archive -Path '%PACKAGE_DIR%' -DestinationPath 'ADB_Tool_Package.zip' -Force"

if exist "ADB_Tool_Package.zip" (
    echo ZIP package created successfully!
    echo Package location: %cd%\ADB_Tool_Package.zip
) else (
    echo Failed to create ZIP package!
)

echo.
echo Step 8: Clean temporary files...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del *.spec 2>nul
rmdir /s /q %PACKAGE_DIR% 2>nul

echo.
echo ================================
echo Package Build Complete!
echo ================================
echo.
echo Package contents:
echo - ADB_Tool.exe
echo - README.md
echo - script/ (folder)
echo.
pause
