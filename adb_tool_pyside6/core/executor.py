#!/usr/bin/env python3
"""
ADB命令执行器模块
提供ADB命令的执行和结果处理功能
"""

import subprocess
from typing import Dict, Optional, Callable
from PySide6.QtCore import QObject, Signal, QThread


class CommandResult:
    """命令执行结果"""
    
    def __init__(self, success: bool, stdout: str = "", stderr: str = "", returncode: int = 0):
        self.success = success
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
    
    def __bool__(self):
        return self.success
    
    def __str__(self):
        if self.success:
            return f"Success (code={self.returncode}): {self.stdout[:100]}..."
        else:
            return f"Failed (code={self.returncode}): {self.stderr[:100]}..."


class ADBCommandExecutor(QObject):
    """ADB命令执行器"""
    
    command_started = Signal(str)
    command_finished = Signal(str, bool, str)
    command_progress = Signal(str, int, int)
    
    def __init__(self):
        super().__init__()
        self._running = False
        self._current_thread: Optional[QThread] = None
    
    @staticmethod
    def execute_command(cmd: str, timeout: int = 10) -> CommandResult:
        """执行命令"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                timeout=timeout
            )
            return CommandResult(
                success=result.returncode == 0,
                stdout=result.stdout,
                stderr=result.stderr,
                returncode=result.returncode
            )
        except subprocess.TimeoutExpired:
            return CommandResult(
                success=False,
                stderr=f'命令执行超时（{timeout}秒）',
                returncode=-1
            )
        except Exception as e:
            return CommandResult(
                success=False,
                stderr=f'执行错误: {str(e)}',
                returncode=-2
            )
    
    @classmethod
    def execute_adb_command(cls, adb_cmd: str, timeout: int = 10) -> CommandResult:
        """执行ADB命令"""
        full_cmd = f"adb {adb_cmd}" if not adb_cmd.startswith("adb ") else adb_cmd
        return cls.execute_command(full_cmd, timeout)
    
    def execute_commands_async(self, commands: list, 
                               progress_callback: Optional[Callable] = None,
                               finished_callback: Optional[Callable] = None):
        """异步执行命令列表"""
        self._running = True
        
        def run_commands():
            total = len(commands)
            for i, cmd in enumerate(commands, 1):
                if not self._running:
                    break
                
                self.command_started.emit(cmd)
                result = self.execute_command(cmd, timeout=15)
                self.command_finished.emit(cmd, result.success, 
                                           result.stdout if result.success else result.stderr)
                self.command_progress.emit(cmd, i, total)
                
                if progress_callback:
                    progress_callback(cmd, i, total, result)
            
            self._running = False
            if finished_callback:
                finished_callback()
        
        self._current_thread = QThread()
        self._current_thread.run = run_commands
        self._current_thread.start()
    
    def stop_execution(self):
        """停止执行"""
        self._running = False
    
    @property
    def is_running(self) -> bool:
        """是否正在执行"""
        return self._running
    
    @staticmethod
    def check_device_connection() -> CommandResult:
        """检查设备连接状态"""
        result = ADBCommandExecutor.execute_adb_command("devices -l", timeout=5)
        
        # 即使命令执行成功，也要检查是否有实际设备连接
        if result.success:
            # 解析输出，检查是否有设备
            lines = result.stdout.strip().split('\n')
            # 第一行是"List of devices attached"，后面是设备列表
            has_device = False
            for i, line in enumerate(lines):
                if i > 0 and line.strip() and not line.startswith('*'):
                    # 检查行中是否包含device关键字
                    if 'device' in line.lower():
                        has_device = True
                        break
            
            if not has_device:
                # 没有设备连接，将结果标记为失败
                result.success = False
                result.stderr = f"未检测到设备连接\n输出: {result.stdout}"
            else:
                # 有设备连接，在stderr中添加调试信息
                result.stderr = f"检测到设备连接\n输出: {result.stdout}"
        
        return result
    
    @staticmethod
    def get_device_info() -> Dict[str, str]:
        """获取设备信息"""
        info = {}
        
        # 设备型号
        result = ADBCommandExecutor.execute_adb_command(
            "shell getprop ro.product.model", timeout=5
        )
        if result.success:
            info['model'] = result.stdout.strip()
        
        # Android版本
        result = ADBCommandExecutor.execute_adb_command(
            "shell getprop ro.build.version.release", timeout=5
        )
        if result.success:
            info['android_version'] = result.stdout.strip()
        
        # SDK版本
        result = ADBCommandExecutor.execute_adb_command(
            "shell getprop ro.build.version.sdk", timeout=5
        )
        if result.success:
            info['sdk_version'] = result.stdout.strip()
        
        return info
    
    @staticmethod
    def adb_root() -> CommandResult:
        """执行ADB Root"""
        return ADBCommandExecutor.execute_adb_command("root", timeout=10)
    
    @staticmethod
    def adb_remount() -> CommandResult:
        """执行ADB Remount"""
        return ADBCommandExecutor.execute_adb_command("remount", timeout=10)
    
    @staticmethod
    def restart_adb_server() -> CommandResult:
        """重启ADB服务"""
        return ADBCommandExecutor.execute_command(
            "adb kill-server && adb start-server", timeout=15
        )
