#!/usr/bin/env python3
"""
字体管理器模块
提供字体大小调节功能
"""

from typing import Dict
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtCore import QObject, Signal


class FontManager(QObject):
    """字体管理器"""
    
    font_scale_changed = Signal(float)
    
    # 字体缩放选项
    SCALE_OPTIONS = {
        '80%': 0.8,
        '100%': 1.0,
        '120%': 1.2,
        '140%': 1.4,
        '160%': 1.6
    }
    
    def __init__(self):
        super().__init__()
        self._default_fonts = {
            'title': ('Microsoft YaHei', 12, QFont.Weight.Bold),
            'button': ('Microsoft YaHei', 10, QFont.Weight.Normal),
            'log': ('Consolas', 10, QFont.Weight.Normal),
            'status': ('Microsoft YaHei', 9, QFont.Weight.Normal),
            'label': ('Microsoft YaHei', 9, QFont.Weight.Normal),
            'menu': ('Microsoft YaHei', 9, QFont.Weight.Normal),
            'tab': ('Microsoft YaHei', 10, QFont.Weight.Normal),
            'group': ('Microsoft YaHei', 10, QFont.Weight.Bold),
            'input': ('Microsoft YaHei', 10, QFont.Weight.Normal)
        }
        
        self._font_scale = 1.0
        self._cached_fonts: Dict[str, QFont] = {}
        
        # 初始化缓存
        self._update_cached_fonts()
    
    def _create_font(self, family: str, size: int, weight: QFont.Weight) -> QFont:
        """创建字体"""
        font = QFont(family, int(size * self._font_scale), weight)
        return font
    
    def _update_cached_fonts(self):
        """更新缓存的字体"""
        self._cached_fonts.clear()
        for name, (family, size, weight) in self._default_fonts.items():
            self._cached_fonts[name] = self._create_font(family, size, weight)
    
    def get_font(self, font_type: str) -> QFont:
        """获取指定类型的字体"""
        if font_type not in self._cached_fonts:
            # 返回默认字体
            return QFont('Microsoft YaHei', int(10 * self._font_scale))
        return self._cached_fonts[font_type]
    
    def set_font_scale(self, scale: float):
        """设置字体缩放因子"""
        self._font_scale = max(0.5, min(2.0, scale))
        self._update_cached_fonts()
        self.font_scale_changed.emit(self._font_scale)
    
    def set_font_scale_by_name(self, scale_name: str):
        """通过名称设置字体缩放"""
        if scale_name in self.SCALE_OPTIONS:
            self.set_font_scale(self.SCALE_OPTIONS[scale_name])
    
    def get_font_scale(self) -> float:
        """获取当前字体缩放因子"""
        return self._font_scale
    
    def get_scale_percentage(self) -> str:
        """获取缩放百分比字符串"""
        for name, scale in self.SCALE_OPTIONS.items():
            if abs(scale - self._font_scale) < 0.01:
                return name
        return f"{int(self._font_scale * 100)}%"
    
    def reset_fonts(self):
        """重置字体为默认大小"""
        self.set_font_scale(1.0)
    
    def get_scaled_size(self, base_size: int) -> int:
        """获取缩放后的尺寸"""
        return int(base_size * self._font_scale)
    
    def get_button_size(self) -> tuple:
        """获取按钮尺寸"""
        base_width = 80
        base_height = 30
        return (self.get_scaled_size(base_width), self.get_scaled_size(base_height))
    
    def get_title_font(self) -> QFont:
        """获取标题字体"""
        return self.get_font('title')
    
    def get_button_font(self) -> QFont:
        """获取按钮字体"""
        return self.get_font('button')
    
    def get_log_font(self) -> QFont:
        """获取日志字体"""
        return self.get_font('log')
    
    def get_status_font(self) -> QFont:
        """获取状态栏字体"""
        return self.get_font('status')
    
    def get_label_font(self) -> QFont:
        """获取标签字体"""
        return self.get_font('label')
    
    def get_menu_font(self) -> QFont:
        """获取菜单字体"""
        return self.get_font('menu')
    
    def get_tab_font(self) -> QFont:
        """获取标签页字体"""
        return self.get_font('tab')
    
    def get_group_font(self) -> QFont:
        """获取分组框字体"""
        return self.get_font('group')
    
    def get_input_font(self) -> QFont:
        """获取输入框字体"""
        return self.get_font('input')
    
    def apply_font_to_widget(self, widget, font_type: str):
        """应用字体到控件"""
        font = self.get_font(font_type)
        widget.setFont(font)
    
    @staticmethod
    def get_system_fonts() -> list:
        """获取系统可用字体列表"""
        font_db = QFontDatabase()
        return font_db.families()
    
    @staticmethod
    def is_font_available(font_name: str) -> bool:
        """检查字体是否可用"""
        font_db = QFontDatabase()
        return font_name in font_db.families()
