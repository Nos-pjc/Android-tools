#!/usr/bin/env python3
"""
主题管理器模块
提供主题切换和应用功能
"""

from typing import Dict, Any
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal


class ThemeManager(QObject):
    """主题管理器"""
    
    theme_changed = Signal(str)
    
    def __init__(self):
        super().__init__()
        self._current_theme = 'light'
        self._themes = {
            'light': self._get_light_theme(),
            'dark': self._get_dark_theme(),
            'high_contrast': self._get_high_contrast_theme()
        }
    
    def _get_light_theme(self) -> Dict[str, Any]:
        """获取明亮主题"""
        return {
            'name': 'light',
            'colors': {
                'bg': '#f5f5f5',
                'fg': '#333333',
                'button_bg': '#4a90e2',
                'button_fg': 'white',
                'button_hover': '#357abd',
                'button_pressed': '#2a6299',
                'log_bg': '#ffffff',
                'log_fg': '#000000',
                'success': '#4CAF50',
                'error': '#F44336',
                'warning': '#FF9800',
                'info': '#2196F3',
                'running': '#FFC107',
                'text_bg': '#ffffff',
                'text_fg': '#000000',
                'frame_bg': '#f5f5f5',
                'entry_bg': '#ffffff',
                'entry_fg': '#000000',
                'border': '#cccccc',
                'tab_bg': '#e0e0e0',
                'tab_selected': '#ffffff',
                'menu_bg': '#f5f5f5',
                'menu_fg': '#333333',
                'group_bg': '#fafafa',
                'status_bg': '#e8e8e8',
                'status_fg': '#333333'
            },
            'qss': '''
                QMainWindow {
                    background-color: #f5f5f5;
                }
                QWidget {
                    background-color: #f5f5f5;
                    color: #333333;
                }
                QPushButton {
                    background-color: #4a90e2;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #357abd;
                }
                QPushButton:pressed {
                    background-color: #2a6299;
                }
                QPushButton:disabled {
                    background-color: #cccccc;
                    color: #888888;
                }
                QTextEdit, QPlainTextEdit {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                }
                QLineEdit {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                    padding: 4px;
                }
                QGroupBox {
                    background-color: #fafafa;
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                    margin-top: 10px;
                    padding-top: 10px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                }
                QTabWidget::pane {
                    border: 1px solid #cccccc;
                    background-color: #ffffff;
                }
                QTabBar::tab {
                    background-color: #e0e0e0;
                    padding: 8px 16px;
                    margin-right: 2px;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                }
                QTabBar::tab:selected {
                    background-color: #ffffff;
                    border-bottom: 2px solid #4a90e2;
                }
                QMenuBar {
                    background-color: #f5f5f5;
                }
                QMenu {
                    background-color: #f5f5f5;
                    border: 1px solid #cccccc;
                }
                QMenu::item:selected {
                    background-color: #4a90e2;
                    color: white;
                }
                QStatusBar {
                    background-color: #e8e8e8;
                    color: #333333;
                }
                QScrollBar:vertical {
                    background-color: #f0f0f0;
                    width: 12px;
                }
                QScrollBar::handle:vertical {
                    background-color: #c0c0c0;
                    border-radius: 6px;
                    min-height: 20px;
                }
                QScrollBar::handle:vertical:hover {
                    background-color: #a0a0a0;
                }
            '''
        }
    
    def _get_dark_theme(self) -> Dict[str, Any]:
        """获取深色主题"""
        return {
            'name': 'dark',
            'colors': {
                'bg': '#2b2b2b',
                'fg': '#e0e0e0',
                'button_bg': '#3a6ea5',
                'button_fg': 'white',
                'button_hover': '#4a7eb5',
                'button_pressed': '#2a5e95',
                'log_bg': '#1e1e1e',
                'log_fg': '#d4d4d4',
                'success': '#4CAF50',
                'error': '#F44336',
                'warning': '#FF9800',
                'info': '#2196F3',
                'running': '#FFC107',
                'text_bg': '#2b2b2b',
                'text_fg': '#e0e0e0',
                'frame_bg': '#2b2b2b',
                'entry_bg': '#3c3c3c',
                'entry_fg': '#ffffff',
                'border': '#555555',
                'tab_bg': '#3c3c3c',
                'tab_selected': '#2b2b2b',
                'menu_bg': '#2b2b2b',
                'menu_fg': '#e0e0e0',
                'group_bg': '#333333',
                'status_bg': '#1e1e1e',
                'status_fg': '#e0e0e0'
            },
            'qss': '''
                QMainWindow {
                    background-color: #2b2b2b;
                }
                QWidget {
                    background-color: #2b2b2b;
                    color: #e0e0e0;
                }
                QPushButton {
                    background-color: #3a6ea5;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #4a7eb5;
                }
                QPushButton:pressed {
                    background-color: #2a5e95;
                }
                QPushButton:disabled {
                    background-color: #444444;
                    color: #888888;
                }
                QTextEdit, QPlainTextEdit {
                    background-color: #1e1e1e;
                    color: #d4d4d4;
                    border: 1px solid #555555;
                    border-radius: 4px;
                }
                QLineEdit {
                    background-color: #3c3c3c;
                    color: #ffffff;
                    border: 1px solid #555555;
                    border-radius: 4px;
                    padding: 4px;
                }
                QGroupBox {
                    background-color: #333333;
                    border: 1px solid #555555;
                    border-radius: 4px;
                    margin-top: 10px;
                    padding-top: 10px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                    color: #e0e0e0;
                }
                QTabWidget::pane {
                    border: 1px solid #555555;
                    background-color: #2b2b2b;
                }
                QTabBar::tab {
                    background-color: #3c3c3c;
                    color: #e0e0e0;
                    padding: 8px 16px;
                    margin-right: 2px;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                }
                QTabBar::tab:selected {
                    background-color: #2b2b2b;
                    border-bottom: 2px solid #3a6ea5;
                }
                QMenuBar {
                    background-color: #2b2b2b;
                    color: #e0e0e0;
                }
                QMenu {
                    background-color: #2b2b2b;
                    border: 1px solid #555555;
                    color: #e0e0e0;
                }
                QMenu::item:selected {
                    background-color: #3a6ea5;
                    color: white;
                }
                QStatusBar {
                    background-color: #1e1e1e;
                    color: #e0e0e0;
                }
                QScrollBar:vertical {
                    background-color: #2b2b2b;
                    width: 12px;
                }
                QScrollBar::handle:vertical {
                    background-color: #555555;
                    border-radius: 6px;
                    min-height: 20px;
                }
                QScrollBar::handle:vertical:hover {
                    background-color: #666666;
                }
            '''
        }
    
    def _get_high_contrast_theme(self) -> Dict[str, Any]:
        """获取高对比度主题"""
        return {
            'name': 'high_contrast',
            'colors': {
                'bg': '#1a1a1a',
                'fg': '#ffffff',
                'button_bg': '#3498db',
                'button_fg': '#ffffff',
                'button_hover': '#2980b9',
                'button_pressed': '#1f618d',
                'log_bg': '#2c2c2c',
                'log_fg': '#e0e0e0',
                'success': '#27ae60',
                'error': '#e74c3c',
                'warning': '#f39c12',
                'info': '#3498db',
                'running': '#f39c12',
                'text_bg': '#2c2c2c',
                'text_fg': '#ffffff',
                'frame_bg': '#1a1a1a',
                'entry_bg': '#2c2c2c',
                'entry_fg': '#ffffff',
                'border': '#444444',
                'tab_bg': '#2c2c2c',
                'tab_selected': '#1a1a1a',
                'menu_bg': '#2c2c2c',
                'menu_fg': '#ffffff',
                'group_bg': '#2c2c2c',
                'status_bg': '#2c2c2c',
                'status_fg': '#ffffff'
            },
            'qss': '''
                QMainWindow {
                    background-color: #1a1a1a;
                }
                QWidget {
                    background-color: #1a1a1a;
                    color: #ffffff;
                }
                QPushButton {
                    background-color: #3498db;
                    color: #ffffff;
                    border: 2px solid #3498db;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                    border-color: #2980b9;
                }
                QPushButton:pressed {
                    background-color: #1f618d;
                    border-color: #1f618d;
                }
                QPushButton:disabled {
                    background-color: #444444;
                    color: #888888;
                    border: 2px solid #666666;
                }
                QTextEdit, QPlainTextEdit {
                    background-color: #2c2c2c;
                    color: #e0e0e0;
                    border: 2px solid #444444;
                    border-radius: 4px;
                }
                QLineEdit {
                    background-color: #2c2c2c;
                    color: #ffffff;
                    border: 2px solid #444444;
                    border-radius: 4px;
                    padding: 4px;
                }
                QGroupBox {
                    background-color: #2c2c2c;
                    border: 2px solid #444444;
                    border-radius: 4px;
                    margin-top: 10px;
                    padding-top: 10px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                    color: #ffffff;
                    font-weight: bold;
                }
                QTabWidget::pane {
                    border: 2px solid #444444;
                    background-color: #1a1a1a;
                    border-radius: 4px;
                }
                QTabBar::tab {
                    background-color: #2c2c2c;
                    color: #ffffff;
                    border: 2px solid #444444;
                    padding: 8px 16px;
                    margin-right: 2px;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                }
                QTabBar::tab:selected {
                    background-color: #1a1a1a;
                    color: #ffffff;
                    border: 2px solid #3498db;
                    border-bottom: 2px solid #1a1a1a;
                }
                QMenuBar {
                    background-color: #2c2c2c;
                    color: #ffffff;
                }
                QMenu {
                    background-color: #2c2c2c;
                    border: 2px solid #444444;
                    color: #ffffff;
                }
                QMenu::item:selected {
                    background-color: #3498db;
                    color: #ffffff;
                }
                QStatusBar {
                    background-color: #2c2c2c;
                    color: #ffffff;
                    border-top: 2px solid #444444;
                }
                QScrollBar:vertical {
                    background-color: #2c2c2c;
                    width: 16px;
                    border: 2px solid #444444;
                    border-radius: 8px;
                }
                QScrollBar::handle:vertical {
                    background-color: #3498db;
                    border-radius: 6px;
                    min-height: 20px;
                }
                QScrollBar::handle:vertical:hover {
                    background-color: #2980b9;
                }
            '''
        }
    
    def get_theme_names(self) -> list:
        """获取所有主题名称"""
        return list(self._themes.keys())
    
    def get_theme(self, theme_name: str) -> Dict[str, Any]:
        """获取指定主题"""
        return self._themes.get(theme_name, self._themes['light'])
    
    def get_current_theme(self) -> Dict[str, Any]:
        """获取当前主题"""
        return self.get_theme(self._current_theme)
    
    def get_colors(self, theme_name: str = None) -> Dict[str, str]:
        """获取主题颜色"""
        theme = self.get_theme(theme_name or self._current_theme)
        return theme.get('colors', {})
    
    def apply_theme(self, app: QApplication, theme_name: str):
        """应用主题到应用"""
        if theme_name not in self._themes:
            theme_name = 'light'
        
        self._current_theme = theme_name
        theme = self._themes[theme_name]
        
        # 应用QSS样式
        app.setStyleSheet(theme.get('qss', ''))
        
        # 发射主题变更信号
        self.theme_changed.emit(theme_name)
    
    def set_theme(self, theme_name: str) -> bool:
        """设置当前主题（不应用）"""
        if theme_name in self._themes:
            self._current_theme = theme_name
            return True
        return False
