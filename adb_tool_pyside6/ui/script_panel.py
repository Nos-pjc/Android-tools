#!/usr/bin/env python3
"""
脚本面板模块
提供脚本管理和执行功能
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QTabWidget,
    QGroupBox, QLabel, QPushButton, QScrollArea, QMessageBox,
    QFrame, QSizePolicy, QDialog, QTextEdit, QLineEdit, QComboBox,
    QFormLayout
)
from PySide6.QtCore import Signal
from core.script_manager import ScriptManager, Script


class ScriptPanel(QWidget):
    """脚本面板"""
    
    script_executed = Signal(str, str)  # category, script_name
    
    def __init__(self, font_manager=None, theme_manager=None, parent=None):
        super().__init__(parent)
        self.font_manager = font_manager
        self.theme_manager = theme_manager
        self.script_manager = ScriptManager()
        self._init_ui()
    
    def _init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # 顶部按钮布局
        top_layout = QHBoxLayout()
        
        # 添加新脚本按钮
        add_script_btn = QPushButton("➕ 添加脚本")
        add_script_btn.setToolTip("添加新脚本")
        add_script_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
        """)
        add_script_btn.clicked.connect(self._add_new_script)
        if self.font_manager:
            add_script_btn.setFont(self.font_manager.get_button_font())
            # 让按钮根据文本内容自动调整大小
            add_script_btn.adjustSize()
        top_layout.addWidget(add_script_btn)
        
        # 加载脚本按钮
        load_script_btn = QPushButton("📂 加载脚本")
        load_script_btn.setToolTip("从文件加载脚本")
        load_script_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        load_script_btn.clicked.connect(self._load_script_from_file)
        if self.font_manager:
            load_script_btn.setFont(self.font_manager.get_button_font())
            # 让按钮根据文本内容自动调整大小
            load_script_btn.adjustSize()
        top_layout.addWidget(load_script_btn)
        
        top_layout.addStretch()
        layout.addLayout(top_layout)
        
        # 标签页
        self.tab_widget = QTabWidget()
        if self.font_manager:
            self.tab_widget.setFont(self.font_manager.get_tab_font())
        
        # 添加各个分类的标签页
        self._refresh_tabs()
        
        layout.addWidget(self.tab_widget)
    
    def _refresh_tabs(self):
        """刷新标签页"""
        # 清空现有标签页
        while self.tab_widget.count() > 0:
            self.tab_widget.removeTab(0)
        
        # 添加各个分类的标签页
        categories = self.script_manager.get_categories()
        for category in categories:
            tab = self._create_category_tab(category)
            self.tab_widget.addTab(tab, f"📁 {category}")
    
    def _create_category_tab(self, category: str) -> QWidget:
        """创建分类标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # 滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        scroll_content = QWidget()
        scroll_layout = QGridLayout(scroll_content)
        scroll_layout.setContentsMargins(5, 5, 5, 5)
        scroll_layout.setSpacing(15)
        
        # 获取该分类下的脚本
        scripts = self.script_manager.get_scripts_by_category(category)
        
        # 为每个脚本创建卡片
        row, col = 0, 0
        for script_name, script in scripts.items():
            script_card = self._create_script_card(script)
            scroll_layout.addWidget(script_card, row, col)
            col += 1
            if col >= 2:  # 每行2个卡片
                col = 0
                row += 1
        
        scroll_layout.setColumnStretch(0, 1)
        scroll_layout.setColumnStretch(1, 1)
        scroll_layout.setRowStretch(row + 1, 1)
        
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        
        return tab
    
    def _create_script_card(self, script: Script) -> QFrame:
        """创建脚本卡片"""
        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 5px;
            }
            QFrame:hover {
                background-color: #e8e8e8;
                border-color: #bbb;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # 标题行
        header_layout = QHBoxLayout()
        
        # 脚本名称
        name_label = QLabel(f"📜 {script.name}")
        name_label.setStyleSheet("font-weight: bold; color: #333;")
        if self.font_manager:
            name_label.setFont(self.font_manager.get_group_font())
        header_layout.addWidget(name_label)
        
        header_layout.addStretch()
        
        # 命令数量标签
        cmd_count = len(script.commands)
        count_label = QLabel(f"{cmd_count} 条命令")
        count_label.setStyleSheet("color: #666; font-size: 11px;")
        if self.font_manager:
            count_label.setFont(self.font_manager.get_label_font())
        header_layout.addWidget(count_label)
        
        layout.addLayout(header_layout)
        
        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #ddd;")
        layout.addWidget(line)
        
        # 描述
        desc_label = QLabel(script.description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #666;")
        if self.font_manager:
            desc_label.setFont(self.font_manager.get_label_font())
        layout.addWidget(desc_label)
        
        # 警告信息
        if script.warning:
            warning_frame = QFrame()
            warning_frame.setStyleSheet("""
                background-color: #FFF3E0;
                border: 1px solid #FF9800;
                border-radius: 4px;
            """)
            warning_layout = QHBoxLayout(warning_frame)
            warning_layout.setContentsMargins(8, 4, 8, 4)
            
            warning_label = QLabel(f"⚠️ {script.warning}")
            warning_label.setStyleSheet("color: #E65100;")
            if self.font_manager:
                warning_label.setFont(self.font_manager.get_label_font())
            warning_layout.addWidget(warning_label)
            
            layout.addWidget(warning_frame)
        
        # 按钮布局
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        
        # 执行按钮
        exec_btn = QPushButton("▶️ 执行")
        exec_btn.setToolTip("执行此脚本")
        exec_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        exec_btn.clicked.connect(lambda checked: self._execute_script(script))
        if self.font_manager:
            btn_width, btn_height = self.font_manager.get_button_size()
            exec_btn.setFixedSize(btn_width, btn_height)
            exec_btn.setFont(self.font_manager.get_button_font())
        btn_layout.addWidget(exec_btn)
        
        # 查看详情按钮
        detail_btn = QPushButton("📋 详情")
        detail_btn.setToolTip("查看脚本详情")
        detail_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        detail_btn.clicked.connect(lambda: self._show_script_detail(script))
        if self.font_manager:
            btn_width, btn_height = self.font_manager.get_button_size()
            detail_btn.setFixedSize(btn_width, btn_height)
            detail_btn.setFont(self.font_manager.get_button_font())
        btn_layout.addWidget(detail_btn)
        
        # 复制命令按钮
        copy_btn = QPushButton("📋 复制")
        copy_btn.setToolTip("复制所有命令到剪贴板")
        copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        copy_btn.clicked.connect(lambda: self._copy_commands(script))
        if self.font_manager:
            btn_width, btn_height = self.font_manager.get_button_size()
            copy_btn.setFixedSize(btn_width, btn_height)
            copy_btn.setFont(self.font_manager.get_button_font())
        btn_layout.addWidget(copy_btn)
        
        # 编辑按钮
        edit_btn = QPushButton("✏️ 编辑")
        edit_btn.setToolTip("编辑此脚本")
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        edit_btn.clicked.connect(lambda: self._edit_script(script))
        if self.font_manager:
            btn_width, btn_height = self.font_manager.get_button_size()
            edit_btn.setFixedSize(btn_width, btn_height)
            edit_btn.setFont(self.font_manager.get_button_font())
        btn_layout.addWidget(edit_btn)
        
        # 删除按钮
        delete_btn = QPushButton("🗑️ 删除")
        delete_btn.setToolTip("删除此脚本")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)
        delete_btn.clicked.connect(lambda: self._delete_script(script))
        if self.font_manager:
            btn_width, btn_height = self.font_manager.get_button_size()
            delete_btn.setFixedSize(btn_width, btn_height)
            delete_btn.setFont(self.font_manager.get_button_font())
        btn_layout.addWidget(delete_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        return card
    
    def _add_new_script(self):
        """添加新脚本"""
        self._show_script_dialog()
    
    def _edit_script(self, script: Script):
        """编辑脚本"""
        self._show_script_dialog(script)
    
    def _delete_script(self, script: Script):
        """删除脚本"""
        reply = QMessageBox.warning(
            self,
            "⚠️ 警告",
            f"确定要删除脚本 '{script.name}' 吗？\n此操作无法撤销。",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.script_manager.remove_script(script.category, script.name)
            self._refresh_tabs()
            
            main_window = self.window()
            if main_window and hasattr(main_window, 'log_panel'):
                main_window.log_panel.log_success(f"已删除脚本 '{script.name}'")
    
    def _show_script_dialog(self, script: Script = None):
        """显示脚本编辑对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("✏️ 编辑脚本" if script else "➕ 添加新脚本")
        dialog.resize(650, 550)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        
        # 表单布局
        form_layout = QFormLayout()
        
        # 脚本名称
        name_edit = QLineEdit()
        name_edit.setPlaceholderText("请输入脚本名称")
        if script:
            name_edit.setText(script.name)
        if self.font_manager:
            name_edit.setFont(self.font_manager.get_input_font())
        form_layout.addRow("脚本名称:", name_edit)
        
        # 分类
        category_edit = QLineEdit()
        category_edit.setPlaceholderText("请输入分类名称")
        if script:
            category_edit.setText(script.category)
        if self.font_manager:
            category_edit.setFont(self.font_manager.get_input_font())
        form_layout.addRow("分类:", category_edit)
        
        # 描述
        desc_edit = QLineEdit()
        desc_edit.setPlaceholderText("请输入脚本描述")
        if script:
            desc_edit.setText(script.description)
        if self.font_manager:
            desc_edit.setFont(self.font_manager.get_input_font())
        form_layout.addRow("描述:", desc_edit)
        
        # 警告
        warning_edit = QLineEdit()
        warning_edit.setPlaceholderText("可选：输入警告信息")
        if script and script.warning:
            warning_edit.setText(script.warning)
        if self.font_manager:
            warning_edit.setFont(self.font_manager.get_input_font())
        form_layout.addRow("警告:", warning_edit)
        
        # 将表单布局添加到主布局
        layout.addLayout(form_layout)
        
        # 命令列表
        cmd_label = QLabel("命令列表:")
        if self.font_manager:
            cmd_label.setFont(self.font_manager.get_label_font())
        layout.addWidget(cmd_label)
        
        cmd_text = QTextEdit()
        cmd_text.setPlaceholderText("请输入命令，每行一条\n例如:\nadb root\nadb shell setenforce 0")
        if script:
            cmd_text.setPlainText("\n".join(script.commands))
        if self.font_manager:
            cmd_text.setFont(self.font_manager.get_log_font())
        layout.addWidget(cmd_text)
        
        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("❌ 取消")
        cancel_btn.clicked.connect(dialog.close)
        if self.font_manager:
            cancel_btn.setFont(self.font_manager.get_button_font())
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("💾 保存")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        def save_script():
            from PySide6.QtWidgets import QFileDialog, QMessageBox
            
            name = name_edit.text().strip()
            category = category_edit.text().strip()
            description = desc_edit.text().strip()
            warning = warning_edit.text().strip() or None
            commands = [cmd.strip() for cmd in cmd_text.toPlainText().split('\n') if cmd.strip()]
            
            if not name:
                QMessageBox.warning(self, "错误", "请输入脚本名称")
                return
            if not category:
                QMessageBox.warning(self, "错误", "请输入分类名称")
                return
            if not description:
                QMessageBox.warning(self, "错误", "请输入脚本描述")
                return
            if not commands:
                QMessageBox.warning(self, "错误", "请至少输入一条命令")
                return
            
            # 提示用户选择保存路径
            # 建议保存路径
            import os
            import sys
            # 获取应用程序目录（支持PyInstaller打包后的路径）
            if getattr(sys, 'frozen', False):
                # 如果是打包后的EXE，使用EXE所在目录
                app_dir = os.path.dirname(sys.executable)
            else:
                # 如果是源代码运行，使用当前文件所在目录
                app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            script_dir = os.path.join(app_dir, "script")
            os.makedirs(script_dir, exist_ok=True)
            
            # 如果是编辑现有脚本且有路径，使用现有路径作为默认值
            default_path = script.path if script and script.path else os.path.join(script_dir, f"{name}.json")
            
            # 显示保存提示 - 使用相对路径
            QMessageBox.information(
                self,
                "保存提示",
                "建议将脚本保存在 script 文件夹中，这样可以确保脚本在应用启动时自动加载。\n\n"
                "例如: script/您的脚本.json"
            )
            
            path, _ = QFileDialog.getSaveFileName(
                self,
                "保存脚本",
                default_path,
                "JSON Files (*.json);;All Files (*)"
            )
            
            if not path:
                return  # 用户取消选择
            
            new_script = Script(
                name=name,
                description=description,
                commands=commands,
                warning=warning,
                category=category,
                path=path
            )
            
            if script:
                # 更新现有脚本
                if script.category == new_script.category and script.name == new_script.name:
                    # 分类和名称都没变，直接更新
                    self.script_manager.update_script(script.category, script.name, new_script)
                else:
                    # 分类或名称变了，先删除旧脚本，再添加新脚本
                    self.script_manager.remove_script(script.category, script.name)
                    self.script_manager.add_script(new_script)
                message = f"已更新脚本 '{name}'"
            else:
                # 添加新脚本
                self.script_manager.add_script(new_script)
                message = f"已添加新脚本 '{name}'"
            
            self._refresh_tabs()
            dialog.close()
            
            main_window = self.window()
            if main_window and hasattr(main_window, 'log_panel'):
                main_window.log_panel.log_success(message)
        
        save_btn.clicked.connect(save_script)
        if self.font_manager:
            save_btn.setFont(self.font_manager.get_button_font())
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
        
        dialog.exec()
    
    def _execute_script(self, script: Script):
        """执行脚本"""
        # 显示警告（如果有）
        if script.warning:
            reply = QMessageBox.warning(
                self,
                "⚠️ 警告",
                f"{script.warning}\n\n确定要继续执行吗？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
        
        # 执行脚本 - 获取MainWindow作为parent
        main_window = self.window()
        if main_window and hasattr(main_window, 'execute_script'):
            main_window.execute_script(script)
        self.script_executed.emit(script.category, script.name)
    
    def _show_script_detail(self, script: Script):
        """显示脚本详情"""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"📜 脚本详情 - {script.name}")
        dialog.resize(650, 500)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        
        # 标题
        title_label = QLabel(f"<h2>📜 {script.name}</h2>")
        title_label.setStyleSheet("color: #333;")
        if self.font_manager:
            title_label.setFont(self.font_manager.get_title_font())
        layout.addWidget(title_label)
        
        # 描述
        desc_label = QLabel(f"<b>描述:</b> {script.description}")
        desc_label.setWordWrap(True)
        if self.font_manager:
            desc_label.setFont(self.font_manager.get_label_font())
        layout.addWidget(desc_label)
        
        # 警告
        if script.warning:
            warning_label = QLabel(f"<b>⚠️ 警告:</b> <span style='color: #FF9800;'>{script.warning}</span>")
            warning_label.setWordWrap(True)
            if self.font_manager:
                warning_label.setFont(self.font_manager.get_label_font())
            layout.addWidget(warning_label)
        
        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #ddd;")
        layout.addWidget(line)
        
        # 命令列表
        cmd_label = QLabel("<b>📋 包含的命令:</b>")
        if self.font_manager:
            cmd_label.setFont(self.font_manager.get_label_font())
        layout.addWidget(cmd_label)
        
        cmd_text = QTextEdit()
        cmd_text.setReadOnly(True)
        cmd_text.setPlainText("\n".join(f"{i+1}. {cmd}" for i, cmd in enumerate(script.commands)))
        if self.font_manager:
            cmd_text.setFont(self.font_manager.get_log_font())
        layout.addWidget(cmd_text)
        
        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        close_btn = QPushButton("❌ 关闭")
        close_btn.clicked.connect(dialog.close)
        if self.font_manager:
            close_btn.setFont(self.font_manager.get_button_font())
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
        
        dialog.exec()
    
    def _copy_commands(self, script: Script):
        """复制命令到剪贴板"""
        from PySide6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText("\n".join(script.commands))
        
        main_window = self.window()
        if main_window and hasattr(main_window, 'log_panel'):
            main_window.log_panel.log_success(f"已复制脚本 '{script.name}' 的命令到剪贴板")
    
    def update_theme(self):
        """更新主题"""
        pass
    
    def update_fonts(self):
        """更新字体和控件尺寸"""
        if not self.font_manager:
            return
        
        # 递归更新所有脚本卡片中的按钮
        def update_recursive(widget):
            from PySide6.QtWidgets import QPushButton, QLabel, QTextEdit, QLineEdit
            
            if isinstance(widget, QPushButton):
                btn_width, btn_height = self.font_manager.get_button_size()
                widget.setFixedSize(btn_width, btn_height)
                widget.setFont(self.font_manager.get_button_font())
            elif isinstance(widget, QLabel):
                widget.setFont(self.font_manager.get_label_font())
            elif isinstance(widget, QTextEdit):
                widget.setFont(self.font_manager.get_log_font())
            elif isinstance(widget, QLineEdit):
                widget.setFont(self.font_manager.get_input_font())
            
            for child in widget.children():
                if hasattr(child, 'children'):
                    update_recursive(child)
        
        # 从tab_widget开始递归更新
        if hasattr(self, 'tab_widget'):
            update_recursive(self.tab_widget)
        
        # 更新标签页字体
        if hasattr(self, 'tab_widget'):
            self.tab_widget.setFont(self.font_manager.get_tab_font())
    
    def refresh_scripts(self):
        """刷新脚本列表，动态加载最新脚本"""
        # 重新加载脚本管理器
        self.script_manager = ScriptManager()
        # 刷新标签页
        self._refresh_tabs()
    
    def _load_script_from_file(self):
        """从文件加载脚本"""
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        
        # 打开文件选择对话框
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "加载脚本",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if not file_path:
            return  # 用户取消选择
        
        try:
            # 加载脚本文件
            import json
            with open(file_path, 'r', encoding='utf-8') as f:
                script_data = json.load(f)
            
            # 检查是否是有效的脚本文件
            if 'name' not in script_data or 'commands' not in script_data:
                QMessageBox.warning(self, "错误", "无效的脚本文件格式")
                return
            
            # 创建脚本对象
            from core.script_manager import Script
            script = Script.from_dict(script_data)
            script.path = file_path
            
            # 添加到脚本管理器
            self.script_manager.add_script(script)
            
            # 刷新标签页
            self._refresh_tabs()
            
            # 显示成功消息
            main_window = self.window()
            if main_window and hasattr(main_window, 'log_panel'):
                main_window.log_panel.log_success(f"已加载脚本 '{script.name}'")
                
        except Exception as e:
            QMessageBox.warning(self, "错误", f"加载脚本失败: {str(e)}")
    
    def showEvent(self, event):
        """显示事件"""
        # 每次显示时刷新脚本列表，确保加载最新的脚本
        self.refresh_scripts()
        super().showEvent(event)
