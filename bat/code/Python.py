#!/usr/bin/python
# -*- coding: UTF-8 -*- 
import math
import os
import shutil
import subprocess
import sys
import time
import json
import zipfile
import random
import string
import datetime
import io
import hashlib
from os import path
import argparse

# 是否是质数
def isPrimeNumber(value):
    vNumber = abs(value)
    vCount = int(math.floor(vNumber/2)+1)
    # print('value:'+str(value)+' vCount:'+str(vCount))
    if vCount>1:
        for i in range(2,vCount):
            if vNumber % i == 0:
                return False
        
    return True

# 获取1到某数之间的质数
def getPrimeNumber(vCount):
    vList=[]
    for i in range(1,vCount):
        if isPrimeNumber(i):
            vList.append(i)
    return vList
        
# vPn=getPrimeNumber(10000)
# print('Prime Number:',json.dumps(vPn))

c_1=10/3
c_2=10//3
d=10%3
print('c_1:',c_1)
print('c_2:',c_2)
print('d:',d)




