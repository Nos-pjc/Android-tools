@echo off

:: 设置编码为UTF-8
chcp 65001 >nul

echo ================================
echo Building ADB Tool to EXE
echo ================================

echo ADB Tool - One-click Build
echo ================================

:: Check Python
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
echo Using icon: resources\app_icon.ico
:: 优化构建配置，减小EXE文件大小
pyinstaller main.py --name=ADB_Tool --onefile --windowed --clean --noconfirm --add-data="resources\styles.qss;resources" --add-data="resources\app_icon.ico;resources" --add-data="README.md;." --add-data="data;data" --icon=resources\app_icon.ico --distpath=./dist --workpath=./build --exclude-module=tkinter --exclude-module=unittest --exclude-module=email --exclude-module=urllib3 --exclude-module=requests --exclude-module=pytest --exclude-module=setuptools --exclude-module=pip --exclude-module=wheel --exclude-module=docutils --exclude-module=jinja2 --exclude-module=markupsafe
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
)

echo.
echo Step 6: Clean temporary files...
rmdir /s /q build 2>nul
del *.spec 2>nul

echo.
echo ================================
echo Build Complete!
echo ================================
echo.
pause
