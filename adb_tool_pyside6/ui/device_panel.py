#!/usr/bin/env python3
"""
设备面板模块
提供设备连接状态和信息显示功能
"""

from PySide6.QtWidgets import (
    QTextEdit, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, 
    QLabel, QPushButton, QListWidget, QListWidgetItem, QFrame,
    QSizePolicy
)
from PySide6.QtCore import Signal, Qt, QTimer
from core.executor import ADBCommandExecutor


class DevicePanel(QWidget):
    """设备面板"""
    
    device_connected = Signal(str)
    device_disconnected = Signal()
    
    def __init__(self, font_manager=None, theme_manager=None, parent=None):
        super().__init__(parent)
        self.font_manager = font_manager
        self.theme_manager = theme_manager
        self.executor = ADBCommandExecutor()
        
        # 跟踪设备连接状态
        self._is_connected = False
        
        self._init_ui()
        
        # 定期检查设备连接状态（每5秒）
        self._connection_timer = QTimer(self)
        self._connection_timer.timeout.connect(self.check_device_connection)
        self._connection_timer.start(5000)
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 停止定时器
        if hasattr(self, '_connection_timer'):
            self._connection_timer.stop()
        super().closeEvent(event)
    
    def _init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # ========== 设备状态组 ==========
        status_group = QGroupBox("📱 设备状态")
        if self.font_manager:
            status_group.setFont(self.font_manager.get_group_font())
        
        status_layout = QVBoxLayout(status_group)
        status_layout.setSpacing(8)
        
        # 连接状态和刷新按钮
        status_header = QHBoxLayout()
        
        status_label = QLabel("连接状态:")
        if self.font_manager:
            status_label.setFont(self.font_manager.get_label_font())
        status_header.addWidget(status_label)
        
        self.status_value = QLabel("❌ 未连接")
        self.status_value.setStyleSheet("color: #F44336; font-weight: bold;")
        if self.font_manager:
            self.status_value.setFont(self.font_manager.get_label_font())
        status_header.addWidget(self.status_value)
        
        status_header.addStretch()
        
        # 刷新按钮
        self.refresh_btn = QPushButton("🔄 刷新")
        self.refresh_btn.setToolTip("检查设备连接状态")
        self.refresh_btn.clicked.connect(lambda: self.check_device_connection(force_reconnect=True))
        if self.font_manager:
            btn_width, btn_height = self.font_manager.get_button_size()
            self.refresh_btn.setFixedSize(btn_width + 20, btn_height)
            self.refresh_btn.setFont(self.font_manager.get_button_font())
        status_header.addWidget(self.refresh_btn)
        
        status_layout.addLayout(status_header)
        
        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #cccccc;")
        status_layout.addWidget(line)
        
        # 设备列表
        self.device_list = QListWidget()
        self.device_list.setMinimumHeight(80)
        self.device_list.setMaximumHeight(120)
        if self.font_manager:
            self.device_list.setFont(self.font_manager.get_label_font())
        status_layout.addWidget(self.device_list)
        
        layout.addWidget(status_group)
        
        # ========== 设备操作组 ==========
        action_group = QGroupBox("⚙️ 设备操作")
        if self.font_manager:
            action_group.setFont(self.font_manager.get_group_font())
        
        action_layout = QVBoxLayout(action_group)
        action_layout.setSpacing(8)
        
        # 操作按钮网格
        btn_grid = QGridLayout()
        btn_grid.setSpacing(8)
        
        # ADB Root按钮
        self.root_btn = QPushButton("🔑 ADB Root")
        self.root_btn.setToolTip("获取ADB Root权限")
        self.root_btn.clicked.connect(self.run_adb_root)
        if self.font_manager:
            btn_width, btn_height = self.font_manager.get_button_size()
            self.root_btn.setFixedSize(btn_width + 40, btn_height)
            self.root_btn.setFont(self.font_manager.get_button_font())
        btn_grid.addWidget(self.root_btn, 0, 0)
        
        # ADB Remount按钮
        self.remount_btn = QPushButton("💾 ADB Remount")
        self.remount_btn.setToolTip("重新挂载系统分区")
        self.remount_btn.clicked.connect(self.run_adb_remount)
        if self.font_manager:
            btn_width, btn_height = self.font_manager.get_button_size()
            self.remount_btn.setFixedSize(btn_width + 60, btn_height)
            self.remount_btn.setFont(self.font_manager.get_button_font())
        btn_grid.addWidget(self.remount_btn, 0, 1)
        
        # 重启ADB按钮
        self.restart_btn = QPushButton("🔄 重启ADB")
        self.restart_btn.setToolTip("重启ADB服务")
        self.restart_btn.clicked.connect(self.restart_adb_server)
        if self.font_manager:
            btn_width, btn_height = self.font_manager.get_button_size()
            self.restart_btn.setFixedSize(btn_width + 40, btn_height)
            self.restart_btn.setFont(self.font_manager.get_button_font())
        btn_grid.addWidget(self.restart_btn, 1, 0)
        
        action_layout.addLayout(btn_grid)
        action_layout.addStretch()
        
        layout.addWidget(action_group)
        
        # ========== 设备信息组 ==========
        info_group = QGroupBox("ℹ️ 设备信息")
        if self.font_manager:
            info_group.setFont(self.font_manager.get_group_font())
        
        info_layout = QGridLayout(info_group)
        info_layout.setSpacing(10)
        info_layout.setColumnStretch(1, 1)
        
        # 设备型号
        model_icon = QLabel("📱")
        info_layout.addWidget(model_icon, 0, 0)
        
        model_label = QLabel("设备型号:")
        if self.font_manager:
            model_label.setFont(self.font_manager.get_label_font())
        info_layout.addWidget(model_label, 0, 1)
        
        self.model_value = QLabel("未知")
        self.model_value.setStyleSheet("color: #2196F3; font-weight: bold;")
        if self.font_manager:
            self.model_value.setFont(self.font_manager.get_label_font())
        info_layout.addWidget(self.model_value, 0, 2)
        
        # Android版本
        version_icon = QLabel("🤖")
        info_layout.addWidget(version_icon, 1, 0)
        
        version_label = QLabel("Android版本:")
        if self.font_manager:
            version_label.setFont(self.font_manager.get_label_font())
        info_layout.addWidget(version_label, 1, 1)
        
        self.version_value = QLabel("未知")
        self.version_value.setStyleSheet("color: #4CAF50; font-weight: bold;")
        if self.font_manager:
            self.version_value.setFont(self.font_manager.get_label_font())
        info_layout.addWidget(self.version_value, 1, 2)
        
        # SDK版本
        sdk_icon = QLabel("📦")
        info_layout.addWidget(sdk_icon, 2, 0)
        
        sdk_label = QLabel("SDK版本:")
        if self.font_manager:
            sdk_label.setFont(self.font_manager.get_label_font())
        info_layout.addWidget(sdk_label, 2, 1)
        
        self.sdk_value = QLabel("未知")
        self.sdk_value.setStyleSheet("color: #FF9800; font-weight: bold;")
        if self.font_manager:
            self.sdk_value.setFont(self.font_manager.get_label_font())
        info_layout.addWidget(self.sdk_value, 2, 2)
        
        layout.addWidget(info_group)
        
        # ========== 命令历史组 ==========
        history_group = QGroupBox("📜 命令历史")
        if self.font_manager:
            history_group.setFont(self.font_manager.get_group_font())
        
        history_layout = QVBoxLayout(history_group)
        history_layout.setSpacing(8)
        
        self.history_list = QTextEdit()
        self.history_list.setReadOnly(True)
        self.history_list.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.history_list.setPlaceholderText("执行的命令将显示在这里...")
        if self.font_manager:
            self.history_list.setFont(self.font_manager.get_log_font())
        history_layout.addWidget(self.history_list)
        
        # 清除历史按钮
        clear_layout = QHBoxLayout()
        clear_layout.addStretch()
        
        clear_btn = QPushButton("🗑️ 清除历史")
        clear_btn.setToolTip("清除命令历史")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF5722;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 3px 8px;
            }
            QPushButton:hover {
                background-color: #E64A19;
            }
        """)
        clear_btn.clicked.connect(self.clear_history)
        if self.font_manager:
            clear_btn.setFont(self.font_manager.get_button_font())
        clear_layout.addWidget(clear_btn)
        
        history_layout.addLayout(clear_layout)
        
        layout.addWidget(history_group)
        layout.addStretch()
        
        # 初始检查由MainWindow在信号连接后调用
    
    def check_device_connection(self, force_reconnect=False):
        """检查设备连接状态
        
        Args:
            force_reconnect: 是否强制重新连接设备
        """
        # 首先检查当前设备连接状态
        result = self.executor.check_device_connection()
        is_connected = result.success
        
        # 如果是用户点击刷新按钮
        if force_reconnect:
            if is_connected:
                # 有设备连接时，先断开再重新连接
                # 先断开连接
                disconnect_result = self.executor.execute_adb_command("disconnect")
                # 然后重新连接
                reconnect_result = self.executor.execute_adb_command("connect")
                # 重新检查连接状态
                result = self.executor.check_device_connection()
                is_connected = result.success
            else:
                # 没有设备连接时，提示用户
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.warning(
                    self,
                    "⚠️ 未连接设备",
                    "请连接设备并确保已启用USB调试模式。",
                    QMessageBox.StandardButton.Ok
                )
        
        # 检查连接状态是否变化
        if is_connected != self._is_connected:
            self._is_connected = is_connected
            
            if is_connected:
                self.status_value.setText("✅ 已连接")
                self.status_value.setStyleSheet("color: #4CAF50; font-weight: bold;")
                
                # 解析设备列表
                self.device_list.clear()
                devices = result.stdout.strip().split('\n')
                for i, device in enumerate(devices):
                    if i > 0 and device:
                        item = QListWidgetItem(f"📱 {device}")
                        self.device_list.addItem(item)
                
                # 获取设备信息
                self._get_device_info()
                
                # 打印设备已连接
                main_window = self.window()
                if main_window and hasattr(main_window, 'log_panel'):
                    main_window.log_panel.log_success("设备已连接")
                
                self.device_connected.emit(result.stdout)
            else:
                self.status_value.setText("❌ 未连接")
                self.status_value.setStyleSheet("color: #F44336; font-weight: bold;")
                self.device_list.clear()
                # 添加提示信息
                no_device_item = QListWidgetItem("⚠️ 未检测到设备，请确保：")
                no_device_item.setToolTip("未检测到设备，请检查连接")
                self.device_list.addItem(no_device_item)
                tip_item1 = QListWidgetItem("  1. 设备已通过USB连接到电脑")
                self.device_list.addItem(tip_item1)
                tip_item2 = QListWidgetItem("  2. 已在设备上启用USB调试模式")
                self.device_list.addItem(tip_item2)
                tip_item3 = QListWidgetItem("  3. 已安装设备驱动程序")
                self.device_list.addItem(tip_item3)
                self._clear_device_info()
                self.device_disconnected.emit()
    
    def _get_device_info(self):
        """获取设备信息"""
        info = self.executor.get_device_info()
        
        self.model_value.setText(info.get('model', '未知'))
        self.version_value.setText(info.get('android_version', '未知'))
        self.sdk_value.setText(info.get('sdk_version', '未知'))
    
    def _clear_device_info(self):
        """清除设备信息"""
        self.model_value.setText("未知")
        self.version_value.setText("未知")
        self.sdk_value.setText("未知")
    
    def clear_history(self):
        """清除命令历史"""
        if hasattr(self, 'history_list'):
            self.history_list.clear()
    
    def add_to_history(self, command: str):
        """添加命令到历史"""
        from datetime import datetime
        if hasattr(self, 'history_list'):
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.history_list.append(f"[{timestamp}] {command}")
    
    def run_adb_root(self):
        """执行ADB Root"""
        result = self.executor.adb_root()
        if result.success:
            # 执行remount
            remount_result = self.executor.adb_remount()
            if remount_result.success:
                self.window().log_panel.log_success("ADB Root和Remount成功")
            else:
                self.window().log_panel.log_warning(f"ADB Root成功，但Remount失败: {remount_result.stderr}")
        else:
            self.window().log_panel.log_error(f"ADB Root失败: {result.stderr}")
    
    def run_adb_remount(self):
        """执行ADB Remount"""
        result = self.executor.adb_remount()
        if result.success:
            self.window().log_panel.log_success("ADB Remount成功")
        else:
            self.window().log_panel.log_error(f"ADB Remount失败: {result.stderr}")
    
    def restart_adb_server(self):
        """重启ADB服务"""
        result = self.executor.restart_adb_server()
        if result.success:
            self.window().log_panel.log_success("ADB服务重启成功")
            # 重新检查设备连接
            from PySide6.QtCore import QTimer
            QTimer.singleShot(2000, self.check_device_connection)
        else:
            self.window().log_panel.log_error(f"ADB服务重启失败: {result.stderr}")
    
    def update_theme(self):
        """更新主题"""
        pass
    
    def update_fonts(self):
        """更新字体和控件尺寸"""
        if not self.font_manager:
            return
        
        # 更新按钮尺寸和字体
        buttons = [
            ('refresh_btn', 20),  # 额外宽度
            ('root_btn', 40),
            ('remount_btn', 60),
            ('restart_btn', 40)
        ]
        
        for btn_name, extra_width in buttons:
            if hasattr(self, btn_name):
                btn = getattr(self, btn_name)
                btn_width, btn_height = self.font_manager.get_button_size()
                btn.setFixedSize(btn_width + extra_width, btn_height)
                btn.setFont(self.font_manager.get_button_font())
        
        # 更新其他控件字体
        if hasattr(self, 'status_value'):
            self.status_value.setFont(self.font_manager.get_label_font())
        if hasattr(self, 'model_value'):
            self.model_value.setFont(self.font_manager.get_label_font())
        if hasattr(self, 'version_value'):
            self.version_value.setFont(self.font_manager.get_label_font())
        if hasattr(self, 'sdk_value'):
            self.sdk_value.setFont(self.font_manager.get_label_font())
        if hasattr(self, 'device_list'):
            self.device_list.setFont(self.font_manager.get_label_font())
