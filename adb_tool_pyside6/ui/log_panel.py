#!/usr/bin/env python3
"""
日志面板模块
提供日志显示和导出功能
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QFileDialog, QComboBox, QLineEdit, QFrame,
    QCheckBox, QMenu
)
from PySide6.QtGui import QTextCharFormat, QColor, QFont, QTextCursor
from PySide6.QtCore import Qt
from datetime import datetime


class LogPanel(QWidget):
    """日志面板"""
    
    def __init__(self, font_manager=None, theme_manager=None, parent=None):
        super().__init__(parent)
        self.font_manager = font_manager
        self.theme_manager = theme_manager
        self._init_ui()
        self._log_entries = []  # 存储所有日志条目
        self._filter_level = "全部"
        self._search_text = ""
    
    def _init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # ========== 工具栏 ==========
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(10)
        
        # 标题
        title_label = QLabel("📋 执行日志")
        title_label.setStyleSheet("font-weight: bold; color: #333;")
        if self.font_manager:
            title_label.setFont(self.font_manager.get_label_font())
        toolbar_layout.addWidget(title_label)
        
        # 分隔线
        line1 = QFrame()
        line1.setFrameShape(QFrame.Shape.VLine)
        line1.setStyleSheet("color: #ddd;")
        toolbar_layout.addWidget(line1)
        
        # 日志级别筛选
        filter_label = QLabel("筛选:")
        if self.font_manager:
            filter_label.setFont(self.font_manager.get_label_font())
        toolbar_layout.addWidget(filter_label)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["全部", "命令", "成功", "错误", "警告", "信息"])
        self.filter_combo.currentTextChanged.connect(self._on_filter_changed)
        if self.font_manager:
            self.filter_combo.setFont(self.font_manager.get_label_font())
        toolbar_layout.addWidget(self.filter_combo)
        
        # 分隔线
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.VLine)
        line2.setStyleSheet("color: #ddd;")
        toolbar_layout.addWidget(line2)
        
        # 搜索框
        search_label = QLabel("🔍 搜索:")
        if self.font_manager:
            search_label.setFont(self.font_manager.get_label_font())
        toolbar_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索日志内容...")
        self.search_input.setMaximumWidth(200)
        self.search_input.textChanged.connect(self._on_search_changed)
        if self.font_manager:
            self.search_input.setFont(self.font_manager.get_input_font())
        toolbar_layout.addWidget(self.search_input)
        
        toolbar_layout.addStretch()
        
        # 自动滚动复选框
        self.auto_scroll_check = QCheckBox("自动滚动")
        self.auto_scroll_check.setChecked(True)
        if self.font_manager:
            self.auto_scroll_check.setFont(self.font_manager.get_label_font())
        toolbar_layout.addWidget(self.auto_scroll_check)
        
        # 分隔线
        line3 = QFrame()
        line3.setFrameShape(QFrame.Shape.VLine)
        line3.setStyleSheet("color: #ddd;")
        toolbar_layout.addWidget(line3)
        
        # 清空按钮
        self.clear_btn = QPushButton("🗑️ 清空")
        self.clear_btn.setToolTip("清空所有日志内容")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF5722;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #E64A19;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_log)
        if self.font_manager:
            self.clear_btn.setFont(self.font_manager.get_button_font())
        toolbar_layout.addWidget(self.clear_btn)
        
        # 导出按钮
        self.export_btn = QPushButton("💾 导出")
        self.export_btn.setToolTip("将日志导出到文件")
        self.export_btn.setStyleSheet("""
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
        self.export_btn.clicked.connect(self.export_log)
        if self.font_manager:
            self.export_btn.setFont(self.font_manager.get_button_font())
        toolbar_layout.addWidget(self.export_btn)
        
        layout.addLayout(toolbar_layout)
        
        # ========== 日志文本框 ==========
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.log_text.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.log_text.customContextMenuRequested.connect(self._show_context_menu)
        
        if self.font_manager:
            self.log_text.setFont(self.font_manager.get_log_font())
        else:
            self.log_text.setFont(QFont("Consolas", 10))
        
        layout.addWidget(self.log_text)
        
        # 初始化颜色格式
        self._init_formats()
    
    def _init_formats(self):
        """初始化文本格式"""
        self.formats = {}
        
        # 获取主题颜色
        if self.theme_manager:
            colors = self.theme_manager.get_colors()
        else:
            colors = {
                'success': '#4CAF50',
                'error': '#F44336',
                'warning': '#FF9800',
                'info': '#2196F3',
                'command': '#9C27B0',
                'log_fg': '#000000'
            }
        
        # 成功格式
        fmt_success = QTextCharFormat()
        fmt_success.setForeground(QColor(colors.get('success', '#4CAF50')))
        self.formats['success'] = fmt_success
        
        # 错误格式
        fmt_error = QTextCharFormat()
        fmt_error.setForeground(QColor(colors.get('error', '#F44336')))
        self.formats['error'] = fmt_error
        
        # 警告格式
        fmt_warning = QTextCharFormat()
        fmt_warning.setForeground(QColor(colors.get('warning', '#FF9800')))
        self.formats['warning'] = fmt_warning
        
        # 信息格式
        fmt_info = QTextCharFormat()
        fmt_info.setForeground(QColor(colors.get('info', '#2196F3')))
        self.formats['info'] = fmt_info
        
        # 命令格式
        fmt_command = QTextCharFormat()
        fmt_command.setForeground(QColor(colors.get('command', '#9C27B0')))
        fmt_command.setFontWeight(QFont.Weight.Bold)
        self.formats['command'] = fmt_command
        
        # 普通格式
        fmt_normal = QTextCharFormat()
        fmt_normal.setForeground(QColor(colors.get('log_fg', '#000000')))
        self.formats['normal'] = fmt_normal
    
    def _add_log_entry(self, level: str, message: str):
        """添加日志条目到内部列表"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = {
            'timestamp': timestamp,
            'level': level,
            'message': message
        }
        self._log_entries.append(entry)
        return entry
    
    def _should_show_entry(self, entry: dict) -> bool:
        """检查日志条目是否应该显示"""
        # 级别筛选
        if self._filter_level != "全部":
            level_map = {
                "命令": "command",
                "成功": "success",
                "错误": "error",
                "警告": "warning",
                "信息": "info"
            }
            if entry['level'] != level_map.get(self._filter_level, ""):
                return False
        
        # 文本搜索
        if self._search_text:
            search_lower = self._search_text.lower()
            message_lower = entry['message'].lower()
            result = search_lower in message_lower
            print(f"[DEBUG] Searching '{search_lower}' in '{message_lower[:50]}...' -> {result}")
            if not result:
                return False
        
        return True
    
    def _refresh_display(self):
        """刷新日志显示"""
        self.log_text.clear()
        
        for entry in self._log_entries:
            if self._should_show_entry(entry):
                self._append_entry_to_display(entry)
        
        # 自动滚动到底部
        if self.auto_scroll_check.isChecked():
            self.log_text.moveCursor(QTextCursor.MoveOperation.End)
    
    def _append_entry_to_display(self, entry: dict):
        """将条目追加到显示"""
        timestamp = entry['timestamp']
        level = entry['level']
        message = entry['message']
        
        # 格式化日志行
        level_icons = {
            'success': '✅',
            'error': '❌',
            'warning': '⚠️',
            'info': 'ℹ️',
            'command': '▶️',
            'normal': '📝'
        }
        
        icon = level_icons.get(level, '📝')
        log_line = f"[{timestamp}] {icon} {message}\n"
        
        # 插入带格式的文本
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        fmt = self.formats.get(level, self.formats['normal'])
        cursor.insertText(log_line, fmt)
    
    def _on_filter_changed(self, filter_text: str):
        """筛选条件改变"""
        self._filter_level = filter_text
        self._refresh_display()
    
    def _on_search_changed(self, search_text: str):
        """搜索文本改变"""
        self._search_text = search_text.strip()
        print(f"[DEBUG] Search text changed: '{self._search_text}'")
        print(f"[DEBUG] Total entries: {len(self._log_entries)}")
        # 打印所有日志条目的消息内容（用于调试）
        for i, entry in enumerate(self._log_entries[:5]):  # 只打印前5条
            print(f"[DEBUG] Entry {i}: {entry.get('message', 'N/A')[:50]}")
        self._refresh_display()
    
    def _show_context_menu(self, position):
        """显示右键菜单"""
        menu = QMenu(self)
        
        copy_action = menu.addAction("📋 复制")
        copy_action.triggered.connect(self._copy_selected)
        
        copy_all_action = menu.addAction("📋 复制全部")
        copy_all_action.triggered.connect(self._copy_all)
        
        menu.addSeparator()
        
        select_all_action = menu.addAction("☑️ 全选")
        select_all_action.triggered.connect(self.log_text.selectAll)
        
        menu.exec(self.log_text.mapToGlobal(position))
    
    def _copy_selected(self):
        """复制选中的文本"""
        self.log_text.copy()
    
    def _copy_all(self):
        """复制全部文本"""
        self.log_text.selectAll()
        self.log_text.copy()
        # 恢复光标位置
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.log_text.setTextCursor(cursor)
    
    def log_message(self, message: str, level: str = 'normal'):
        """记录日志消息"""
        entry = self._add_log_entry(level, message)
        if self._should_show_entry(entry):
            self._append_entry_to_display(entry)
            
            # 自动滚动到底部
            if self.auto_scroll_check.isChecked():
                self.log_text.moveCursor(QTextCursor.MoveOperation.End)
    
    def log_success(self, message: str):
        """记录成功消息"""
        self.log_message(message, 'success')
    
    def log_error(self, message: str):
        """记录错误消息"""
        self.log_message(message, 'error')
    
    def log_warning(self, message: str):
        """记录警告消息"""
        self.log_message(message, 'warning')
    
    def log_info(self, message: str):
        """记录信息消息"""
        self.log_message(message, 'info')
    
    def log_command(self, command: str):
        """记录命令"""
        self.log_message(command, 'command')
    
    def clear_log(self):
        """清空日志"""
        self.log_text.clear()
        self._log_entries.clear()
    
    def export_log(self):
        """导出日志到文件"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "导出日志",
            f"adb_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "文本文件 (*.txt);;所有文件 (*.*)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    for entry in self._log_entries:
                        timestamp = entry['timestamp']
                        level = entry['level']
                        message = entry['message']
                        f.write(f"[{timestamp}] [{level.upper()}] {message}\n")
                
                self.log_success(f"✅ 日志已导出到: {filename}")
            except Exception as e:
                self.log_error(f"❌ 导出日志失败: {str(e)}")
    
    def set_font(self, font: QFont):
        """设置字体"""
        self.log_text.setFont(font)
    
    def update_theme(self):
        """更新主题"""
        self._init_formats()
        self._refresh_display()
