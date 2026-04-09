#!/usr/bin/env python3
"""
主窗口模块
应用的主界面
"""

from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, 
    QSplitter, QStatusBar, QMenuBar, QMenu,
    QMessageBox, QTabWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from ui.log_panel import LogPanel
from ui.device_panel import DevicePanel
from ui.script_panel import ScriptPanel
from ui.custom_command_panel import CustomCommandPanel
from core.executor import ADBCommandExecutor
from core.script_manager import Script


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self, theme_manager, font_manager, parent=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.font_manager = font_manager
        self.executor = ADBCommandExecutor()
        self.is_executing = False
        self.device_connected = True  # 暂时强制设置为已连接，用于测试
        self._init_ui()
    
    def _init_ui(self):
        """初始化界面"""
        # 设置窗口属性
        self.setWindowTitle("Android ADB调试工具 v3.0")
        self.setGeometry(100, 100, 1300, 750)
        self.setMinimumSize(900, 700)
        
        # 将窗口显示在屏幕顶部
        from PySide6.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        # 计算水平居中位置
        x = (screen_geometry.width() - self.width()) // 2
        # 设置y坐标为20，使窗口显示在屏幕顶部
        y = 0
        self.move(x, y)
        
        # 设置窗口图标
        from PySide6.QtGui import QIcon
        import os
        icon_path = os.path.join(os.path.dirname(__file__), "..", "resources", "app_icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # 创建菜单
        self._create_menu()
        
        # 创建状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("就绪")
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 水平分割器（左侧设备面板，右侧内容标签页）
        left_right_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 设备信息区域（左侧）
        self.device_panel = DevicePanel(
            font_manager=self.font_manager,
            theme_manager=self.theme_manager,
            parent=self
        )
        left_right_splitter.addWidget(self.device_panel)
        
        # 右侧垂直分割器（顶部内容标签页，底部日志区域）
        top_bottom_splitter = QSplitter(Qt.Orientation.Vertical)
        
        # 内容标签页（右侧顶部）
        content_tab = QTabWidget()
        if self.font_manager:
            content_tab.setFont(self.font_manager.get_tab_font())
        
        # 脚本面板
        self.script_panel = ScriptPanel(
            font_manager=self.font_manager,
            theme_manager=self.theme_manager,
            parent=self
        )
        content_tab.addTab(self.script_panel, "脚本管理")
        
        # 自定义命令面板
        self.custom_panel = CustomCommandPanel(
            font_manager=self.font_manager,
            theme_manager=self.theme_manager,
            parent=self
        )
        content_tab.addTab(self.custom_panel, "自定义命令")
        
        top_bottom_splitter.addWidget(content_tab)
        
        # 日志区域（右侧底部）
        self.log_panel = LogPanel(
            font_manager=self.font_manager,
            theme_manager=self.theme_manager,
            parent=self
        )
        top_bottom_splitter.addWidget(self.log_panel)
        
        # 设置分割器尺寸
        left_right_splitter.setSizes([400, 1000])  # 左侧设备面板稍微宽一点，容纳命令历史
        top_bottom_splitter.setSizes([400, 500])  # 减少脚本管理区域，增加执行日志区域
        
        # 添加到分割器
        left_right_splitter.addWidget(top_bottom_splitter)
        main_layout.addWidget(left_right_splitter)
        
        # 连接信号
        self._connect_signals()
    
    def _create_menu(self):
        """创建菜单"""
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)
        
        # 文件菜单
        file_menu = QMenu("文件")
        if self.font_manager:
            file_menu.setFont(self.font_manager.get_menu_font())
        menu_bar.addMenu(file_menu)
        
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        if self.font_manager:
            exit_action.setFont(self.font_manager.get_menu_font())
        file_menu.addAction(exit_action)
        
        # 视图菜单
        view_menu = QMenu("视图")
        if self.font_manager:
            view_menu.setFont(self.font_manager.get_menu_font())
        menu_bar.addMenu(view_menu)
        
        # 主题子菜单
        theme_menu = QMenu("主题")
        if self.font_manager:
            theme_menu.setFont(self.font_manager.get_menu_font())
        view_menu.addMenu(theme_menu)
        
        for theme in self.theme_manager.get_theme_names():
            action = QAction(theme, self)
            action.triggered.connect(lambda checked=True, t=theme: self._set_theme(t))
            if self.font_manager:
                action.setFont(self.font_manager.get_menu_font())
            theme_menu.addAction(action)
        
        # 字体子菜单
        font_menu = QMenu("字体大小")
        if self.font_manager:
            font_menu.setFont(self.font_manager.get_menu_font())
        view_menu.addMenu(font_menu)
        
        for scale_name in self.font_manager.SCALE_OPTIONS.keys():
            action = QAction(scale_name, self)
            action.triggered.connect(lambda checked=True, s=scale_name: self._set_font_scale(s))
            if self.font_manager:
                action.setFont(self.font_manager.get_menu_font())
            font_menu.addAction(action)
        
        # 帮助菜单
        help_menu = QMenu("帮助")
        if self.font_manager:
            help_menu.setFont(self.font_manager.get_menu_font())
        menu_bar.addMenu(help_menu)
        
        help_action = QAction("使用说明", self)
        help_action.triggered.connect(self.show_help)
        if self.font_manager:
            help_action.setFont(self.font_manager.get_menu_font())
        help_menu.addAction(help_action)
        
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        if self.font_manager:
            about_action.setFont(self.font_manager.get_menu_font())
        help_menu.addAction(about_action)
    
    def _connect_signals(self):
        """连接信号"""
        # 主题变更信号
        self.theme_manager.theme_changed.connect(self._on_theme_changed)
        
        # 字体缩放变更信号
        self.font_manager.font_scale_changed.connect(self._on_font_scale_changed)
        
        # 设备连接信号
        self.device_panel.device_connected.connect(self._on_device_connected)
        self.device_panel.device_disconnected.connect(self._on_device_disconnected)
        
        # 直接调用设备连接回调，模拟设备连接状态
        self._on_device_connected("测试设备连接")
        
        # 连接信号后手动检查一次设备连接状态
        self.device_panel.check_device_connection()
    
    def _set_theme(self, theme_name):
        """设置主题"""
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        self.theme_manager.apply_theme(app, theme_name)
        self.statusBar.showMessage(f"已切换到{theme_name}主题")
        
        # 更新面板主题
        self.log_panel.update_theme()
        self.script_panel.update_theme()
        self.custom_panel.update_theme()
        self.device_panel.update_theme()
    
    def _set_font_scale(self, scale_name):
        """设置字体缩放"""
        self.font_manager.set_font_scale_by_name(scale_name)
        self.statusBar.showMessage(f"已设置字体大小: {scale_name}")
    
    def _on_theme_changed(self, theme_name):
        """主题变更回调"""
        self.statusBar.showMessage(f"主题已切换到: {theme_name}")
    
    def _on_font_scale_changed(self, scale):
        """字体缩放变更回调"""
        # 更新所有控件字体
        self._update_fonts()
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 停止设备面板的定时器
        if hasattr(self, 'device_panel') and hasattr(self.device_panel, '_connection_timer'):
            self.device_panel._connection_timer.stop()
        
        # 确保所有线程都已停止
        self.is_executing = False
        
        # 停止命令执行
        if hasattr(self, 'executor'):
            self.executor.stop_execution()
        
        super().closeEvent(event)
    
    def _update_fonts(self):
        """更新字体"""
        # 更新菜单字体
        if self.font_manager:
            for action in self.menuBar().actions():
                if hasattr(action, 'font'):
                    action.setFont(self.font_manager.get_menu_font())
        
        # 更新状态栏字体
        if self.font_manager:
            self.statusBar.setFont(self.font_manager.get_status_font())
        
        # 更新所有面板的字体
        if self.font_manager:
            # 更新日志面板字体
            if self.log_panel:
                self.log_panel.set_font(self.font_manager.get_log_font())
            
            # 更新设备面板字体
            if self.device_panel:
                self._update_panel_fonts(self.device_panel)
            
            # 更新脚本面板字体
            if self.script_panel:
                self._update_panel_fonts(self.script_panel)
            
            # 更新自定义命令面板字体
            if hasattr(self, 'custom_panel') and self.custom_panel:
                if hasattr(self.custom_panel, 'update_fonts'):
                    self.custom_panel.update_fonts()
                else:
                    self._update_panel_fonts(self.custom_panel)
    
    def _update_panel_fonts(self, panel):
        """更新面板字体"""
        if not self.font_manager:
            return
        
        # 优先调用面板的update_fonts方法（如果存在）
        if hasattr(panel, 'update_fonts'):
            panel.update_fonts()
            return
        
        # 通用递归更新（备用）
        def update_recursive(widget):
            from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QListWidget, QGroupBox, QTabWidget
            
            # 根据控件类型设置字体
            if isinstance(widget, QPushButton):
                widget.setFont(self.font_manager.get_button_font())
            elif isinstance(widget, QLabel):
                widget.setFont(self.font_manager.get_label_font())
            elif isinstance(widget, QLineEdit):
                widget.setFont(self.font_manager.get_input_font())
            elif isinstance(widget, QTextEdit):
                widget.setFont(self.font_manager.get_log_font())
            elif isinstance(widget, QListWidget):
                widget.setFont(self.font_manager.get_label_font())
            elif isinstance(widget, QGroupBox):
                widget.setFont(self.font_manager.get_group_font())
            elif isinstance(widget, QTabWidget):
                widget.setFont(self.font_manager.get_tab_font())
            
            # 递归处理子控件
            for child in widget.children():
                if isinstance(child, QWidget):
                    update_recursive(child)
        
        update_recursive(panel)
    
    def _on_device_connected(self, device_info):
        """设备连接回调"""
        self.device_connected = True
        self.statusBar.showMessage("设备已连接")
        self.log_panel.log_success("设备已连接")
    
    def _on_device_disconnected(self):
        """设备断开回调"""
        self.device_connected = False
        self.statusBar.showMessage("设备已断开")
        self.log_panel.log_warning("设备已断开")
    
    def check_device_connection(self):
        """检查设备连接状态"""
        self.device_panel.check_device_connection()
    
    def execute_script(self, script: Script):
        """执行脚本"""
        if self.is_executing:
            QMessageBox.warning(self, "警告", "当前有命令正在执行，请等待完成")
            return
        
        # 直接检查设备连接状态
        result = self.executor.check_device_connection()
        if not result.success:
            QMessageBox.warning(self, "⚠️ 警告", "设备未连接，请先连接设备")
            return
        
        self.is_executing = True
        self.statusBar.showMessage(f"正在执行脚本: {script.name}")
        
        self.log_panel.log_info(f"开始执行脚本: {script.name}")
        self.log_panel.log_info(f"描述: {script.description}")
        
        # 执行命令
        def run_commands():
            success_count = 0
            total_count = len(script.commands)
            
            for i, cmd in enumerate(script.commands, 1):
                if not main_window.is_executing:
                    break
                
                main_window.statusBar.showMessage(f"执行中 ({i}/{total_count})")
                if hasattr(main_window, 'log_panel'):
                    main_window.log_panel.log_command(f"[{i}/{total_count}] {cmd}")
                
                result = main_window.executor.execute_command(cmd, timeout=15)
                
                if result.success:
                    if hasattr(main_window, 'log_panel'):
                        main_window.log_panel.log_success("命令执行成功")
                    success_count += 1
                else:
                    if hasattr(main_window, 'log_panel'):
                        main_window.log_panel.log_error(f"命令执行失败: {result.stderr}")
            
            if hasattr(main_window, 'is_executing'):
                main_window.is_executing = False
            if hasattr(main_window, 'statusBar'):
                main_window.statusBar.showMessage(f"脚本执行完成: {success_count}/{total_count} 个命令成功")
            if hasattr(main_window, 'log_panel'):
                main_window.log_panel.log_info(f"脚本执行完成: {success_count}/{total_count} 个命令成功")
        
        # 在线程池中执行
        from PySide6.QtCore import QRunnable, QThreadPool
        
        # 保存MainWindow实例引用
        main_window = self
        
        class ScriptRunnable(QRunnable):
            def run(self):
                try:
                    run_commands()
                except Exception as e:
                    # 捕获异常，防止程序崩溃
                    import traceback
                    error_msg = f"脚本执行异常: {str(e)}\n{traceback.format_exc()}"
                    if main_window and hasattr(main_window, 'log_panel'):
                        main_window.log_panel.log_error(error_msg)
                    if main_window:
                        main_window.is_executing = False
                        main_window.statusBar.showMessage("脚本执行异常")
        
        runnable = ScriptRunnable()
        QThreadPool.globalInstance().start(runnable)
    
    def show_help(self):
        """显示使用说明"""
        help_text = """
        Android ADB调试工具 使用说明

        1. 设备连接
        - 确保Android设备已启用USB调试
        - 通过USB线连接设备到电脑
        - 点击"设备状态"中的"刷新"按钮检查设备状态

        2. 功能使用
        - 脚本管理：选择分类标签页，点击脚本按钮执行对应功能
        - 自定义命令：在输入框中输入ADB命令并执行
        - 常用命令：点击快捷按钮快速执行常用ADB命令

        3. 字体调节
        - 通过"视图"菜单调整字体大小
        - 支持5种字体大小：80%、100%、120%、140%、160%

        4. 主题切换
        - 提供3种主题：明亮、深色、高对比度
        - 可根据使用环境选择合适的主题

        5. 日志管理
        - 执行日志显示所有命令的执行结果
        - 支持清空日志和导出日志到文件
        - 不同级别的日志用不同颜色显示

        6. 快捷操作
        - ADB Root：获取Root权限
        - ADB Remount：重新挂载系统分区
        - 重启ADB：重启ADB服务
        """
        
        QMessageBox.information(self, "使用说明", help_text)
    
    def show_about(self):
        """显示关于信息"""
        about_text = """
        Android ADB调试工具 v3.0

        功能：集成所有ADB调试脚本，提供图形化界面
        技术：Python 3.x + PySide6

        主要功能模块：
        1. 日志调试模块
        2. 数据抓取模块
        3. 系统追踪模块
        4. 设备管理模块
        5. 设备信息模块

        特点：
        - 支持主题切换
        - 支持字体大小调节
        - 分文件设计，结构清晰
        - 多线程执行命令，界面响应流畅

        版权所有 © 2026
        """
        
        QMessageBox.about(self, "关于", about_text)
    
    def closeEvent(self, event):
        """关闭事件"""
        if self.is_executing:
            reply = QMessageBox.question(
                self,
                "警告",
                "当前有命令正在执行，确定要退出吗？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                event.ignore()
                return
        event.accept()
