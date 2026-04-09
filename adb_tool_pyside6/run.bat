@echo off

setlocal

:: 进入脚本所在目录
cd /d "%~dp0"

:: 检查是否存在EXE文件
if exist "dist\ADB_Tool.exe" (
    echo 启动ADB工具...
    "dist\ADB_Tool.exe"
) else if exist "main.py" (
    echo 未找到EXE文件，使用Python直接运行...
    python main.py
) else (
    echo 错误：未找到可执行文件
    pause
    exit /b 1
)
