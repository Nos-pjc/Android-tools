Write-Host "============================" -ForegroundColor Green
Write-Host "Building ADB Tool to EXE" -ForegroundColor Green
Write-Host "============================" -ForegroundColor Green

Write-Host "ADB Tool - One-click Build" -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor Cyan

# Check Python
try {
    python --version | Out-Null
} catch {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Step 1: Clean old build files..." -ForegroundColor Yellow
if (Test-Path "build") {
    Remove-Item -Path "build" -Recurse -Force
}
if (Test-Path "dist") {
    Remove-Item -Path "dist" -Recurse -Force
}
Get-ChildItem -Name "*.spec" | ForEach-Object {
    Remove-Item -Path $_ -Force
}

Write-Host "Step 2: Install dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Step 3: Install PyInstaller..." -ForegroundColor Yellow
pip install pyinstaller
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install PyInstaller" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Step 4: Build EXE file..." -ForegroundColor Yellow
Write-Host "Using icon: resources\app_icon.ico" -ForegroundColor Cyan
# 优化构建配置，减小EXE文件大小
pyinstaller main.py --name=ADB_Tool --onefile --windowed --clean --noconfirm --add-data="resources\styles.qss;resources" --add-data="resources\app_icon.ico;resources" --icon=resources\app_icon.ico --distpath=./dist --workpath=./build --exclude-module=tkinter --exclude-module=unittest --exclude-module=email --exclude-module=urllib3 --exclude-module=requests --exclude-module=pytest --exclude-module=setuptools --exclude-module=pip --exclude-module=wheel --exclude-module=docutils --exclude-module=jinja2 --exclude-module=markupsafe
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to build EXE" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "" -ForegroundColor White
Write-Host "Step 5: Verify build result..." -ForegroundColor Yellow
if (Test-Path "dist\ADB_Tool.exe") {
    Write-Host "Build successful!" -ForegroundColor Green
    Write-Host "EXE file location: $((Get-Location).Path)\dist\ADB_Tool.exe" -ForegroundColor Cyan
    $fileSize = (Get-Item "dist\ADB_Tool.exe").Length
    Write-Host "File size: $fileSize bytes" -ForegroundColor Cyan
} else {
    Write-Host "Build failed!" -ForegroundColor Red
}

Write-Host "" -ForegroundColor White
Write-Host "Step 6: Clean temporary files..." -ForegroundColor Yellow
if (Test-Path "build") {
    Remove-Item -Path "build" -Recurse -Force
}
Get-ChildItem -Name "*.spec" | ForEach-Object {
    Remove-Item -Path $_ -Force
}

Write-Host "" -ForegroundColor White
Write-Host "============================" -ForegroundColor Green
Write-Host "Build Complete!" -ForegroundColor Green
Write-Host "============================" -ForegroundColor Green
Write-Host "" -ForegroundColor White
Read-Host "Press Enter to exit"
