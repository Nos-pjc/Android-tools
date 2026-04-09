#!/usr/bin/env python3
"""
Android ADB调试工具 v3.0 - PySide6版本
功能: 使用PySide6重构的ADB调试工具,分文件设计
"""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from ui.main_window import MainWindow
from utils.theme_manager import ThemeManager
from utils.font_manager import FontManager


def main():
    """主函数"""
    # 启用高DPI支持
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # 创建应用
    app = QApplication(sys.argv)
    app.setApplicationName("Android ADB调试工具")
    app.setApplicationVersion("3.0")
    
    # 初始化管理器
    theme_manager = ThemeManager()
    font_manager = FontManager()
    
    # 应用主题
    theme_manager.apply_theme(app, 'light')
    
    # 创建主窗口
    window = MainWindow(theme_manager, font_manager)
    window.show()
    
    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
