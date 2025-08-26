from utils.ramdisk import RamDisk,get_RamDisk_PATH
import os
import logging
from utils.decorators import skip

@skip
def run():
    # # ================= 使用示例(自动卸载) =================
    # with RamDisk(size="50M") as path:
    #     print("RAM Disk 挂载在:", path)
    #     if path.endswith(":"):  # Windows 盘符
    #         path += os.sep
    #         test_file = os.path.join(path, "test.txt")
    #     with open(test_file, "w") as f:
    #         f.write("Hello RAM Disk!")

    #     print("文件已写入:", test_file)

    # print("RAM Disk 已卸载")
    global RamDisk_PATH
    ramdisk = RamDisk(size="1024M")
    ramdisk.mount()
    logging.info(f"RAM Disk 挂载在:{get_RamDisk_PATH()}")