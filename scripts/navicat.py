# -*- coding: utf-8 -*-
"""
navicat试用期延长脚本
适用于Linux系统
相关软件仅供学习研究软件之用，不得用于商业用途，请大家购买正版，支持正版软件，请认准官方正版网站
"""
import os
import re
import subprocess
import time


def get_path():
    navicat_path = os.path.isfile('./navicat.path')
    path = ""
    if not navicat_path:
        print("查找navicat启动文件。")
        command = "find / -name start_navicat"
        opt = subprocess.getoutput(command)
        results = re.findall(r'/.*?/start_navicat', opt)
        _filter = ["/mnt", "/media", "/misc"]   # 排除挂载目录
        for result in results:
            flag = True
            for f in _filter:
                if result.startswith(f):
                    flag = False
            if flag:
                path = result
                with open('./navicat.path', 'w') as f:
                    f.write(path)
                break
    else:
        with open('./navicat.path', 'r') as f:
            path = f.read()
    return path


def matching(reg: str):

    classes = re.findall('.Software.*?Classes.*?Info] [0-9]{10}\n#time=.*?\n".*?"=".*?"', reg)
    premium = re.findall('.Software.*?PremiumSoft.*?Info] [0-9]{10}\n#time=.*?\n".*?"=".*?"', reg)

    return classes, premium


def replace(old: str, new: str) -> str:
    new_classes, new_premium = matching(new)
    old_classes, old_premium = matching(old)

    for i, string in enumerate(new_classes):
        old = old.replace(old_classes[i], string)
    for i, string in enumerate(new_premium):
        old = old.replace(old_premium[i], string)

    return old


def start_cat(path):
    subprocess.Popen(path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def kill_cat():
    command = "ps -ef | grep navicat/Navicat/Navicat.exe | grep -v grep | awk '{print $2}'"
    pid = subprocess.getoutput(command)
    subprocess.run(['kill', pid])


def run():
    file = os.path.join(os.path.expanduser('~'), '.navicat64', 'user.reg')      # 配置文件路径
    file_bak = f'{file}.bak'
    start_path = get_path()     # 启动路径  start_navicat
    """检查文件是否存在，通常来讲都在这个路径下"""
    if not os.path.isfile(file):
        print('配置文件路径有误，请手动修改为绝对路径。')
        return
    if not os.path.isfile(start_path):
        print('启动路径有误，请手动修改navicat.path路径或删除待程序自动查找。')
        return
    if os.path.isfile(file_bak):
        """清掉之前的备份文件"""
        os.remove(file_bak)
    print("备份原文件。")
    os.rename(file, file_bak)
    print("重新生成文件。")
    start_cat(start_path)
    """检查文件是否已生成 生成完毕后可关闭"""
    timeout = 60
    while not os.path.isfile(file):
        time.sleep(1)
        timeout -= 1
        if not timeout:
            print("生成配置文件超时，开始数据恢复。")
            kill_cat()
            os.rename(file_bak, file)
            print("数据恢复完成。")
            return
    kill_cat()
    """读文件"""
    with open(file, 'r') as f:
        new_file = f.read()
    with open(file_bak, 'r') as f:
        old_file = f.read()
    print("延长试用时限。")
    old_file = replace(old_file, new_file)
    """覆盖新文件 备份暂时不删，方便错误时恢复"""
    with open(file, 'w') as f:
        f.write(old_file)
    print("结束～")


if __name__ == '__main__':
    run()
