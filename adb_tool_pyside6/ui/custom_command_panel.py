#!/usr/bin/env python3
"""
自定义命令面板模块
提供自定义ADB命令输入和执行功能
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, 
    QLabel, QLineEdit, QPushButton, QTextEdit, QFrame,
    QSizePolicy
)
from PySide6.QtCore import Signal, Qt
from functools import partial
from core.executor import ADBCommandExecutor


class CustomCommandPanel(QWidget):
    """自定义命令面板"""
    
    command_executed = Signal(str, bool, str)
    
    def __init__(self, font_manager=None, theme_manager=None, parent=None):
        super().__init__(parent)
        self.font_manager = font_manager
        self.theme_manager = theme_manager
        self.executor = ADBCommandExecutor()
        self._quick_command_buttons = []  # 保存常用命令按钮引用
        self._init_ui()
    
    def _init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # ========== 命令输入组 ==========
        cmd_group = QGroupBox("⌨️ 自定义命令")
        if self.font_manager:
            cmd_group.setFont(self.font_manager.get_group_font())
        
        cmd_layout = QVBoxLayout(cmd_group)
        cmd_layout.setSpacing(10)
        
        # 命令输入行
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        
        cmd_label = QLabel("ADB命令:")
        if self.font_manager:
            cmd_label.setFont(self.font_manager.get_label_font())
        input_layout.addWidget(cmd_label)
        
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText("输入ADB命令，例如: devices -l, shell, install app.apk 等...")
        if self.font_manager:
            self.cmd_input.setFont(self.font_manager.get_input_font())
        input_layout.addWidget(self.cmd_input)
        
        # 执行按钮
        self.exec_btn = QPushButton("▶️ 执行")
        self.exec_btn.setToolTip("执行自定义命令")
        self.exec_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 15px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.exec_btn.clicked.connect(self.execute_command)
        if self.font_manager:
            btn_width, btn_height = self.font_manager.get_button_size()
            self.exec_btn.setFixedSize(btn_width + 20, btn_height + 4)
            self.exec_btn.setFont(self.font_manager.get_button_font())
        input_layout.addWidget(self.exec_btn)
        
        cmd_layout.addLayout(input_layout)
        
        # 提示信息
        tip_label = QLabel("💡 提示: 可以直接输入adb命令，不需要加'adb'前缀。按Enter键快速执行。")
        tip_label.setStyleSheet("color: #666; font-size: 11px;")
        if self.font_manager:
            tip_label.setFont(self.font_manager.get_label_font())
        cmd_layout.addWidget(tip_label)
        
        # 连接回车键执行
        self.cmd_input.returnPressed.connect(self.execute_command)
        
        layout.addWidget(cmd_group)
        
        # ========== 常用命令组 ==========
        quick_group = QGroupBox("⚡ 常用命令")
        if self.font_manager:
            quick_group.setFont(self.font_manager.get_group_font())
        
        quick_layout = QVBoxLayout(quick_group)
        quick_layout.setSpacing(10)
        
        # 按钮网格
        btn_grid = QGridLayout()
        btn_grid.setSpacing(8)
        
        # 常用命令列表（带标识和说明）
        quick_commands = [
            ("📱 设备列表", "devices -l", "查看设备列表及详细信息"),
            ("📦 安装应用", "install ", "安装APK文件（需指定路径）"),
            ("🗑️ 卸载应用", "uninstall ", "卸载应用（需指定包名）"),
            ("📋 包名列表", "shell pm list packages", "列出所有已安装应用的包名"),
            ("🔋 电池状态", "shell dumpsys battery", "查看电池状态和电量信息"),
            ("💾 存储空间", "shell df -h", "查看设备存储空间使用情况"),
            ("🖥️ 屏幕截图", "shell screencap /sdcard/screenshot.png", "截取设备屏幕"),
            ("🎬 屏幕录制", "shell screenrecord /sdcard/record.mp4", "录制设备屏幕"),
            ("🔧 系统信息", "shell getprop", "查看设备系统属性信息"),
            ("🌐 网络信息", "shell ifconfig", "查看网络接口信息"),
            ("📊 进程列表", "shell ps", "查看运行中的进程列表"),
            ("🖥️ 内核版本", "shell cat /proc/version", "查看Linux内核版本")
        ]
        
        row, col = 0, 0
        for label, cmd, tooltip in quick_commands:
            btn = QPushButton(label)
            btn.setToolTip(f"命令: {cmd}\n{tooltip}")
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #E3F2FD;
                    color: #1976D2;
                    border: 1px solid #90CAF9;
                    border-radius: 4px;
                    padding: 5px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #BBDEFB;
                    color: #1565C0;
                    border-color: #64B5F6;
                }
            """)
            btn.clicked.connect(partial(self._insert_command, cmd))
            if self.font_manager:
                btn_width, btn_height = self.font_manager.get_button_size()
                btn.setFixedSize(btn_width + 80, btn_height + 4)
                btn.setFont(self.font_manager.get_button_font())
            btn_grid.addWidget(btn, row, col)
            # 保存按钮引用以便后续更新
            self._quick_command_buttons.append(btn)
            col += 1
            if col >= 3:  # 每行3个按钮
                col = 0
                row += 1
        
        quick_layout.addLayout(btn_grid)
        
        layout.addWidget(quick_group)
    
    def execute_command(self):
        """执行自定义命令"""
        command = self.cmd_input.text().strip()
        if not command:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "⚠️ 警告", "请输入ADB命令")
            return
        
        # 检查是否正在执行
        main_window = self.window()
        if main_window and hasattr(main_window, 'is_executing') and main_window.is_executing:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "⚠️ 警告", "当前有命令正在执行，请等待完成")
            return
        
        # 直接检查设备连接状态
        result = self.executor.check_device_connection()
        if not result.success:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "⚠️ 警告", "设备未连接，请先连接设备")
            return
        
        # 记录到历史
        self._add_to_history(command)
        
        # 保存命令后清除输入框
        self.cmd_input.clear()
        
        # 执行命令
        def run_command():
            if main_window:
                main_window.is_executing = True
                main_window.statusBar.showMessage(f"执行命令: {command}")
            
            if main_window and hasattr(main_window, 'log_panel'):
                main_window.log_panel.log_command(command)
            
            # 支持多命令执行（用分号分隔）
            commands = [cmd.strip() for cmd in command.split(';') if cmd.strip()]
            success_count = 0
            total_count = len(commands)
            
            for i, cmd in enumerate(commands, 1):
                if not main_window or not main_window.is_executing:
                    break
                
                if main_window:
                    main_window.statusBar.showMessage(f"执行中 ({i}/{total_count}): {cmd}")
                
                if main_window and hasattr(main_window, 'log_panel'):
                    main_window.log_panel.log_info(f"[{i}/{total_count}] {cmd}")
                
                result = self.executor.execute_command(f"adb {cmd}" if not cmd.startswith("adb ") else cmd, timeout=30)
                
                if main_window and hasattr(main_window, 'log_panel'):
                    if result.success:
                        main_window.log_panel.log_success("✅ 命令执行成功")
                        if result.stdout:
                            main_window.log_panel.log_info(f"输出:\n{result.stdout}")
                        success_count += 1
                    else:
                        main_window.log_panel.log_error(f"❌ 命令执行失败: {result.stderr}")
            
            if main_window:
                main_window.is_executing = False
                main_window.statusBar.showMessage(f"命令执行完成: {success_count}/{total_count} 个命令成功")
            
            if main_window and hasattr(main_window, 'log_panel'):
                main_window.log_panel.log_info(f"命令执行完成: {success_count}/{total_count} 个命令成功")
            
            self.command_executed.emit(command, success_count == total_count, f"{success_count}/{total_count} 个命令成功")
        
        # 在线程池中执行
        from PySide6.QtCore import QRunnable, QThreadPool
        
        class CommandRunnable(QRunnable):
            def __init__(self, window):
                super().__init__()
                self.window = window
            
            def run(self):
                try:
                    run_command()
                except Exception as e:
                    # 捕获异常，防止程序崩溃
                    import traceback
                    error_msg = f"命令执行异常: {str(e)}\n{traceback.format_exc()}"
                    if self.window and hasattr(self.window, 'log_panel'):
                        self.window.log_panel.log_error(error_msg)
                    if self.window and hasattr(self.window, 'is_executing'):
                        self.window.is_executing = False
                    if self.window and hasattr(self.window, 'statusBar'):
                        self.window.statusBar.showMessage("命令执行异常")
        
        runnable = CommandRunnable(main_window)
        QThreadPool.globalInstance().start(runnable)
    
    def _insert_command(self, command: str):
        """插入命令到输入框"""
        self.cmd_input.setText(command)
        self.cmd_input.setFocus()
        # 如果命令以空格结尾，将光标移到最后
        if command.endswith(' '):
            self.cmd_input.setCursorPosition(len(command))
    
    def _add_to_history(self, command: str):
        """添加命令到历史"""
        # 调用DevicePanel的add_to_history方法
        main_window = self.window()
        if main_window and hasattr(main_window, 'device_panel'):
            main_window.device_panel.add_to_history(command)
        if main_window and hasattr(main_window, 'log_panel'):
            main_window.log_panel.log_command(f"历史命令: {command}")
    
    def clear_history(self):
        """清除命令历史"""
        # 调用DevicePanel的clear_history方法
        main_window = self.window()
        if main_window and hasattr(main_window, 'device_panel'):
            main_window.device_panel.clear_history()
        if main_window and hasattr(main_window, 'log_panel'):
            main_window.log_panel.log_info("🗑️ 命令历史已清空")
    
    def set_command(self, command: str):
        """设置命令"""
        self.cmd_input.setText(command)
    
    def get_command(self) -> str:
        """获取当前命令"""
        return self.cmd_input.text().strip()
    
    def update_theme(self):
        """更新主题"""
        pass
    
    def update_fonts(self):
        """更新字体和控件尺寸"""
        if not self.font_manager:
            return
        
        # 更新所有常用命令按钮
        for btn in self._quick_command_buttons:
            btn_width, btn_height = self.font_manager.get_button_size()
            btn.setFixedSize(btn_width + 80, btn_height + 4)
            btn.setFont(self.font_manager.get_button_font())
        
        # 更新其他控件字体
        if hasattr(self, 'cmd_input'):
            self.cmd_input.setFont(self.font_manager.get_input_font())
        if hasattr(self, 'history_list'):
            self.history_list.setFont(self.font_manager.get_log_font())
        if hasattr(self, 'exec_btn'):
            self.exec_btn.setFont(self.font_manager.get_button_font())
            btn_width, btn_height = self.font_manager.get_button_size()
            self.exec_btn.setFixedSize(btn_width + 20, btn_height + 4)
