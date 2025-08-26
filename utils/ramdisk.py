import os
import sys
import tempfile
import subprocess
import atexit
import shutil
import string

RamDisk_PATH = None

def get_RamDisk_PATH():
    return RamDisk_PATH

class RamDisk:
    def __init__(self, size="100M", drive_letter="R:"):
        """
        :param size: RAM Disk 大小，例如 "100M"、"1G"
        :param drive_letter: Windows 下的首选盘符，例如 "R:"
        """
        self.size = size
        self.is_windows = sys.platform.startswith("win")
        self.mount_point = None
        self._mounted = False

        if self.is_windows:
            self.drive_letter = self._find_free_drive(drive_letter)
        else:
            self.drive_letter = None  # Linux 下用临时目录挂载

    def _find_free_drive(self, preferred):
        """从后往前选择空闲盘符"""
        used = {d.upper() for d in self._get_used_drives()}
        # 先尝试首选盘符
        if preferred.upper() not in used:
            return preferred.upper()
        # 从 Z: 到 A: 反向查找
        for d in reversed(string.ascii_uppercase):
            drive = f"{d}:"
            if drive not in used:
                return drive
        raise RuntimeError("没有可用盘符挂载 RAM Disk")

    def _get_used_drives(self):
        """获取当前系统已使用的盘符列表"""
        return [f"{d}:" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]

    def mount(self):
        global RamDisk_PATH
        """主动挂载，返回挂载路径"""
        if not self._mounted:
            if self.is_windows:
                self._mount_windows()
            else:
                self._mount_linux()
            self._mounted = True
        RamDisk_PATH = self.mount_point
        return RamDisk_PATH

    def unmount(self):
        """主动卸载"""
        if self._mounted:
            self.cleanup()
            self._mounted = False

    def __enter__(self):
        return self.mount()  # 支持 with 语法返回 path

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unmount()       # 支持 with 语法自动卸载

    def _mount_linux(self):
        self.mount_point = tempfile.mkdtemp(prefix="ramdisk_")
        subprocess.run([
            "mount", "-t", "tmpfs", "-o", f"size={self.size}",
            "tmpfs", self.mount_point
        ], check=True)
        atexit.register(self.cleanup)

    def _mount_windows(self):
        self.mount_point = self.drive_letter
        subprocess.run([
            "imdisk", "-a", "-s", self.size, "-m", self.drive_letter,
            "-p", "/fs:ntfs /q /y"
        ], check=True)
        atexit.register(self.cleanup)

    def cleanup(self):
        if self.mount_point:
            try:
                if self.is_windows:
                    subprocess.run(["imdisk", "-D", "-m", self.drive_letter],
                                   check=True)
                else:
                    subprocess.run(["umount", self.mount_point], check=True)
                    shutil.rmtree(self.mount_point)
            finally:
                self.mount_point = None
