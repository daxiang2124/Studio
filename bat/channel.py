# -*- coding: utf-8 -*
import os
import shutil
import sys
import json
import zipfile
#本地文件的路径
filePath = sys.argv[1]
#渠道号
channelCode = (sys.argv[2])


with open(filePath, "r") as f:
    config_data = json.load(f)

def inplace_change():
    x = None
    if config_data["init_cfg"].has_key("channelID"):
        del config_data["init_cfg"]["channelID"]
    if channelCode == None or channelCode == 0 or channelCode == "0":
        print("channel Code 不存在")
    else:
        config_data["init_cfg"]["channelID"] = channelCode
    x = json.dumps(config_data)
    print("config 内容:"+x)
    with open(filePath, "wt") as file:
        file.write(x)


inplace_change()
