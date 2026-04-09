#!/usr/bin/env python3
"""
脚本管理器模块
整合所有ADB脚本功能
"""

import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Script:
    """脚本数据类"""
    name: str
    description: str
    commands: List[str]
    warning: Optional[str] = None
    category: str = ""
    path: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "name": self.name,
            "description": self.description,
            "commands": self.commands,
            "warning": self.warning,
            "category": self.category,
            "path": self.path
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Script':
        """从字典创建脚本"""
        return cls(
            name=data.get("name"),
            description=data.get("description"),
            commands=data.get("commands", []),
            warning=data.get("warning"),
            category=data.get("category"),
            path=data.get("path")
        )


class ScriptManager:
    """脚本管理器"""
    
    def __init__(self):
        self._scripts: Dict[str, Dict[str, Script]] = {}
        # 获取应用程序目录（支持PyInstaller打包后的路径）
        import sys
        if getattr(sys, 'frozen', False):
            # 如果是打包后的EXE，使用EXE所在目录
            app_dir = os.path.dirname(sys.executable)
        else:
            # 如果是源代码运行，使用当前文件所在目录
            app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._scripts_file = os.path.join(app_dir, "script", "scripts.json")
        self._init_scripts()
    
    def _init_scripts(self):
        """初始化所有脚本"""
        # 加载保存的脚本
        self._load_scripts()
        
        # 如果没有保存的脚本，初始化默认脚本
        if not self._scripts:
            # 日志调试模块
            self._scripts["日志调试"] = {
                "D级日志": Script(
                    name="D级日志",
                    description="启用D级日志，设置相机调试参数",
                    category="日志调试",
                    commands=[
                        "adb root",
                        "adb remount",
                        'adb shell "start logd"',
                        "adb shell setenforce 0",
                        "adb shell setprop persist.vendor.mtk.camera.log_level 3",
                        "adb shell setprop vendor.debug.camera.ulog.mode 2",
                        "adb shell setprop persist.vendor.debug.camera.log 3",
                        'adb shell "setprop vendor.debug.camera.ulog.mode 0x11"',
                        'adb shell "setprop vendor.debug.camera.ulog.filter 0xfffff"',
                        'adb shell "setprop vendor.debug.camera.ulog.func 1"',
                        'adb shell "setprop vendor.mtk.c2.venc.async.systrace 1"',
                        'adb shell "setprop vendor.debug.hal3av3.systrace 1"',
                        'adb shell "setprop vendor.camera.gce_time_cmd.en 1"',
                        "adb shell setprop persist.log.ratelimit 0",
                        'adb shell "echo 8 > /proc/sys/kernel/printk"',
                        "adb shell setprop vendor.debug.camera.log.pipeline.fbm 3",
                        "adb shell \"ps -e | grep camera* | awk '{print $2}' | xargs kill\"",
                        "adb shell pkill camera*"
                    ]
                ),
                "PowerHAL日志": Script(
                    name="PowerHAL日志",
                    description="启用PowerHAL相关日志",
                    category="日志调试",
                    commands=[
                        "adb root",
                        'adb shell "setprop log.tag.libPowerHal D"',
                        'adb shell "setprop persist.log.tag.libPowerHal D"',
                        'adb shell "setprop log.tag.powerd D"',
                        'adb shell "setprop persist.log.tag.powerd D"',
                        'adb shell "setprop log.tag.mtkpower@1.0-impl D"',
                        'adb shell "setprop persist.log.tag.mtkpower@1.0-impl D"',
                        'adb shell "setprop log.tag.legacy_power@2.1-impl D"',
                        'adb shell "setprop persist.log.tag.legacy_power@2.1-impl D"',
                        'adb shell "setprop log.tag.power@1.3-impl D"',
                        'adb shell "setprop persist.log.tag.power@1.3-impl D"',
                        'adb shell "setprop log.tag.PowerWrap D"',
                        'adb shell "setprop persist.log.tag.PowerWrap D"',
                        'adb shell "setprop log.tag.mtkperf_client D"',
                        'adb shell "setprop persist.log.tag.mtkperf_client D"',
                        "adb shell setprop persist.vendor.mtk.camera.log_level 3",
                        "adb shell \"ps -e | grep camera* | awk '{print $2}' | xargs kill\"",
                        "adb shell pkill camera*"
                    ]
                ),
                "FD日志": Script(
                    name="FD日志",
                    description="启用人脸检测(FD)相关日志",
                    category="日志调试",
                    commands=[
                        "adb root",
                        "adb shell setenforce 0",
                        "adb shell setprop vendor.debug.camera.fd.detail.log 1",
                        "adb shell setprop vendor.debug.camera.log.FDNode 1",
                        "adb shell setprop vendor.debug.fpipe.force.printio 1",
                        "adb shell setprop vendor.debug.tpi.s.log 1",
                        "adb shell setprop vendor.debug.mtkcam.p2.log 1",
                        "adb shell setprop vendor.debug.fpipe.force.printmdp 1",
                        "adb shell setprop vendor.debug.trace.p2.Cropper 1",
                        "adb shell setprop persist.vendor.mtk.camera.log_level 3",
                        "adb shell pkill camera*"
                    ]
                ),
                "基础日志": Script(
                    name="基础日志",
                    description="启用基础相机日志和调试功能",
                    category="日志调试",
                    commands=[
                        "adb root",
                        "adb shell setenforce 0",
                        "adb shell setprop persist.vendor.mtk.camera.log_level 3",
                        "adb shell setprop vendor.debug.camera.log 3",
                        "adb shell setprop vendor.debug.camera.log.p1node 3",
                        "adb shell setprop vendor.debug.camera.p1.dumpCrop 1",
                        "adb shell setprop debug.cam.drawid 1",
                        "adb shell setprop vendor.debug.aaa.pvlog.enable 1",
                        "adb shell pkill camera*",
                        "adb shell logcat -c"
                    ]
                ),
                "Metadata日志": Script(
                    name="Metadata日志",
                    description="启用相机日志（针对Metadata下发调试）",
                    category="日志调试",
                    commands=[
                        "adb root",
                        "adb shell setenforce 0",
                        "adb shell setprop persist.vendor.mtk.camera.log_level 3",
                        "adb shell setprop vendor.debug.camera.log 3",
                        "adb shell setprop vendor.debug.camera.log.p1node 3",
                        "adb shell setprop vendor.debug.camera.p1.dumpCrop 1",
                        "adb shell pkill camera*"
                    ]
                )
            }
            
            # 数据抓取模块
            self._scripts["数据抓取"] = {
                "ISP7抓取": Script(
                    name="ISP7抓取",
                    description="启用ISP7相机数据抓取",
                    category="数据抓取",
                    commands=[
                        "adb root",
                        "adb shell setenforce 0",
                        "adb shell setprop vendor.debug.camera.p2.dump 1",
                        "adb shell setprop vendor.debug.camera.img3o.dump 1",
                        "adb shell setprop vendor.debug.camera.dump.campipe 1",
                        "adb shell setprop vendor.debug.camera.dump.JpegNode 1",
                        "adb shell pkill camera*"
                    ]
                ),
                "ISP6S抓取": Script(
                    name="ISP6S抓取",
                    description="启用ISP6S相机数据抓取（包含jiigan_sdk）",
                    category="数据抓取",
                    commands=[
                        "adb root",
                        "adb shell setenforce 0",
                        "adb shell setprop vendor.debug.camera.p2.dump 1",
                        "adb shell setprop vendor.debug.camera.img3o.dump 1",
                        "adb shell setprop vendor.debug.camera.dump.campipe 1",
                        "adb shell setprop vendor.debug.camera.dump.JpegNode 1",
                        "adb shell mkdir /data/vendor/camera/jiigan_sdk_dump/ -p",
                        "adb shell setprop vendor.camera.siq.dump_input_output 1",
                        "adb shell pkill camera*"
                    ]
                ),
                "P2S输入输出": Script(
                    name="P2S输入输出",
                    description="抓取P2S节点输入输出数据",
                    category="数据抓取",
                    commands=[
                        "adb root",
                        "adb shell setenforce 0",
                        "adb shell setprop debug.cam.drawid 1",
                        "adb shell setprop vendor.debug.fpipe.force.img3o 1",
                        "adb shell rm -rf /data/vendor/camera_dump/*",
                        "adb shell setprop vendor.debug.p2f.dump.enable 1",
                        "adb shell setprop vendor.debug.p2f.dump.mode 1",
                        "adb shell setprop vendor.debug.camera.preview.dump 1",
                        "adb shell setprop vendor.debug.camera.dump.en 1",
                        "adb shell setprop vendor.debug.feature.forceEnableIMGO 1",
                        "adb shell setprop vendor.debug.camera.dump.p1.imgo 1",
                        "adb shell setprop vendor.debug.camera.p2.dump 1",
                        "adb shell setprop vendor.debug.camera.img3o.dump 1",
                        "adb shell setprop vendor.debug.camera.dump.campipe 1",
                        "adb shell setprop vendor.debug.camera.dump.JpegNode 1",
                        "adb shell pkill camera*"
                    ]
                ),
                "P2流节点": Script(
                    name="P2流节点",
                    description="抓取P2流节点数据",
                    category="数据抓取",
                    commands=[
                        "adb root",
                        "adb shell setenforce 0",
                        "adb shell setprop debug.cam.drawid 1",
                        "adb shell setprop vendor.debug.fpipe.force.img3o 1",
                        "adb shell rm -rf /data/vendor/camera_dump/*",
                        "adb shell rm -rf /data/vendor/dump/*",
                        "adb shell mkdir /data/vendor/dump",
                        "adb shell setprop vendor.debug.p2f.dump.enable 1",
                        "adb shell setprop vendor.debug.p2f.dump.mode 1",
                        "adb shell setprop vendor.debug.p2f.dump.in 0xff",
                        "adb shell setprop vendor.debug.p2f.dump.out 0xff",
                        "adb shell setprop vendor.debug.camera.preview.dump 1",
                        "adb shell setprop vendor.debug.camera.dump.en 1",
                        "adb shell setprop vendor.debug.feature.forceEnableIMGO 1",
                        "adb shell setprop vendor.debug.camera.dump.p1.imgo 1",
                        "adb shell setprop vendor.debug.tpi.s 1",
                        "adb shell setprop vendor.debug.tpi.s.dump 1"
                    ]
                ),
                "TPI数据": Script(
                    name="TPI数据",
                    description="抓取TPI（图像处理接口）数据",
                    category="数据抓取",
                    commands=[
                        "adb root",
                        "adb shell setenforce 0",
                        "adb shell setprop debug.cam.drawid 1",
                        "adb shell rm -rf /data/vendor/dump/*",
                        "adb shell mkdir /data/vendor/dump",
                        "adb shell setprop vendor.debug.tpi.s 1",
                        "adb shell setprop vendor.debug.tpi.s.dump 1"
                    ]
                )
            }
            
            # 系统追踪模块
            self._scripts["系统追踪"] = {
                "Systrace": Script(
                    name="Systrace",
                    description="启用系统追踪(Systrace)功能",
                    category="系统追踪",
                    commands=[
                        "adb root",
                        "adb shell setenforce 0",
                        "adb shell setprop vendor.systrace.camera.Dispatcher 1",
                        "adb shell setprop debug.atrace.tags.enableflags 1024"
                    ]
                )
            }
            
            # 设备管理模块
            self._scripts["设备管理"] = {
                "跳过向导": Script(
                    name="跳过向导",
                    description="跳过Android设置向导",
                    category="设备管理",
                    commands=[
                        "adb shell pm disable com.google.android.setupwizard",
                        "adb shell settings put secure user_setup_complete 1",
                        "adb shell settings put global device_provisioned 1"
                    ]
                ),
                "OEM解锁": Script(
                    name="OEM解锁",
                    description="执行OEM解锁和用户数据擦除（警告：会清除数据！）",
                    category="设备管理",
                    warning="⚠️ 警告：此操作会清除所有用户数据！",
                    commands=[
                        "adb root",
                        "adb reboot bootloader",
                        "fastboot oem tran_skip_confirm_key",
                        "fastboot flashing unlock",
                        "fastboot erase userdata",
                        "fastboot erase metadata",
                        "fastboot reboot"
                    ]
                )
            }
            
            # 设备信息模块
            self._scripts["设备信息"] = {
                "设备信息": Script(
                    name="设备信息",
                    description="获取设备基本信息",
                    category="设备信息",
                    commands=[
                        "adb devices -l",
                        "adb shell getprop ro.product.model",
                        "adb shell getprop ro.build.version.release",
                        "adb shell getprop ro.build.version.sdk"
                    ]
                )
            }
            
            # 保存默认脚本
            self._save_scripts()
    
    def _load_scripts(self):
        """加载保存的脚本"""
        try:
            # 1. 加载主配置文件中的脚本
            if os.path.exists(self._scripts_file):
                with open(self._scripts_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for category, scripts_data in data.items():
                        self._scripts[category] = {}
                        for script_name, script_data in scripts_data.items():
                            # 首先创建脚本对象
                            script = Script.from_dict(script_data)
                            # 无论脚本是否有指定路径，都尝试从文件加载最新版本
                            # 1. 检查脚本是否有指定路径
                            if script.path and os.path.exists(script.path):
                                try:
                                    with open(script.path, 'r', encoding='utf-8') as script_file:
                                        script_data_from_path = json.load(script_file)
                                        script = Script.from_dict(script_data_from_path)
                                except Exception as e:
                                    print(f"从指定路径加载脚本失败: {e}")
                            # 2. 如果是保存过的脚本（有name），也尝试动态加载
                            elif script.name:
                                # 可以在这里添加其他动态加载逻辑
                                pass
                            
                            self._scripts[category][script_name] = script
            
            # 2. 自动扫描script目录下的脚本文件
            self._scan_script_directory()
        except Exception as e:
            print(f"加载脚本失败: {e}")
    
    def _scan_script_directory(self):
        """扫描script目录下的脚本文件"""
        try:
            script_dir = os.path.dirname(self._scripts_file)
            if os.path.exists(script_dir):
                for filename in os.listdir(script_dir):
                    if filename.endswith('.json') and filename != 'scripts.json':
                        file_path = os.path.join(script_dir, filename)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                script_data = json.load(f)
                                # 检查是否是有效的脚本文件
                                if 'name' in script_data and 'commands' in script_data:
                                    script = Script.from_dict(script_data)
                                    # 设置脚本路径
                                    script.path = file_path
                                    # 确保分类存在
                                    category = script.category or '未分类'
                                    if category not in self._scripts:
                                        self._scripts[category] = {}
                                    # 检查脚本是否已存在
                                    if script.name not in self._scripts[category]:
                                        self._scripts[category][script.name] = script
                                        print(f"自动加载脚本: {script.name}")
                        except Exception as e:
                            print(f"加载脚本文件 {filename} 失败: {e}")
        except Exception as e:
            print(f"扫描script目录失败: {e}")
    
    def _save_scripts(self):
        """保存脚本"""
        try:
            # 确保script目录存在
            os.makedirs(os.path.dirname(self._scripts_file), exist_ok=True)
            
            # 转换脚本为字典
            data = {}
            for category, scripts in self._scripts.items():
                data[category] = {}
                for script_name, script in scripts.items():
                    # 保存到脚本指定的路径（如果有）
                    if script.path:
                        try:
                            # 确保目录存在
                            os.makedirs(os.path.dirname(script.path), exist_ok=True)
                            # 保存到指定路径
                            with open(script.path, 'w', encoding='utf-8') as script_file:
                                json.dump(script.to_dict(), script_file, ensure_ascii=False, indent=2)
                        except Exception as e:
                            print(f"保存脚本到指定路径失败: {e}")
                    # 添加到主数据中
                    data[category][script_name] = script.to_dict()
            
            # 保存到主文件
            with open(self._scripts_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存脚本失败: {e}")
    
    def add_script(self, script: Script):
        """添加脚本"""
        if script.category not in self._scripts:
            self._scripts[script.category] = {}
        self._scripts[script.category][script.name] = script
        self._save_scripts()
    
    def remove_script(self, category: str, name: str):
        """删除脚本"""
        if category in self._scripts and name in self._scripts[category]:
            # 获取脚本对象
            script = self._scripts[category][name]
            # 删除对应的脚本文件（如果有）
            if script.path and os.path.exists(script.path):
                try:
                    os.remove(script.path)
                except Exception as e:
                    print(f"删除脚本文件失败: {e}")
            # 删除内存中的脚本
            del self._scripts[category][name]
            # 如果分类为空，删除分类
            if not self._scripts[category]:
                del self._scripts[category]
            self._save_scripts()
    
    def update_script(self, category: str, name: str, script: Script):
        """更新脚本"""
        if category in self._scripts:
            self._scripts[category][name] = script
            self._save_scripts()
    
    def get_categories(self) -> List[str]:
        """获取所有分类"""
        return list(self._scripts.keys())
    
    def get_scripts_by_category(self, category: str) -> Dict[str, Script]:
        """获取指定分类下的所有脚本"""
        return self._scripts.get(category, {})
    
    def get_script(self, category: str, name: str) -> Optional[Script]:
        """获取指定脚本"""
        category_scripts = self._scripts.get(category, {})
        script = category_scripts.get(name)
        
        # 检查脚本文件是否存在，如果存在则重新加载（确保文件移动后能动态加载）
        if script and script.path:
            if os.path.exists(script.path):
                try:
                    with open(script.path, 'r', encoding='utf-8') as script_file:
                        script_data = json.load(script_file)
                        script = Script.from_dict(script_data)
                        # 更新内存中的脚本
                        category_scripts[name] = script
                except Exception as e:
                    print(f"重新加载脚本失败: {e}")
            else:
                print(f"脚本文件不存在: {script.path}")
        
        return script
    
    def get_all_scripts(self) -> Dict[str, Dict[str, Script]]:
        """获取所有脚本"""
        return self._scripts.copy()
    
    def search_scripts(self, keyword: str) -> List[Script]:
        """搜索脚本"""
        results = []
        keyword_lower = keyword.lower()
        
        for category, scripts in self._scripts.items():
            for name, script in scripts.items():
                if (keyword_lower in name.lower() or 
                    keyword_lower in script.description.lower()):
                    results.append(script)
        
        return results
