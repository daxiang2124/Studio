#!/usr/bin/python
# -*- coding: UTF-8 -*- 
from fileinput import filename
import json
import os
import subprocess
import shutil
from shutil import copyfile
import sys
import time
import struct
import random
import base64
import array
import math
import string
import binascii
import hashlib
from os import path 
import argparse

m_outPath="out"

# old project configuration file
def makefileUtf8Normal(fileName,content):
	print('Create '+fileName+' file')
	fo = open(fileName, "w+",)
	fo.write(str(content).decode('utf-8', 'ignore'))
	fo.close()
	print('\tCreate file successfully '+fileName)

# Parameter content cutting(参数内容切割)
def getParameterContentList(parameter):
	big_delimiter=';'
	small_delimiter='|'
	m_list=[]
	splitBig=str(parameter).split(big_delimiter)
	for kv in splitBig:
		splitSmall=str(kv).split(small_delimiter)
		# print('\t'+kv+':'+json.dumps(splitSmall)+' len:'+str(len(splitSmall)))
		if(len(splitSmall)>1):
			vindex=0
			dict={}
			for ikv in splitSmall:
				# dict[str(vindex)]=str(ikv).replace('\\','/')
				dict[str(vindex)]=ikv
				vindex=vindex+1
			dict['count']=vindex
			m_list.append(dict)
		else:
			m_list.append(kv)
	return m_list
	
#乱序字符串(统一下标)
m_randIndex=0
def getGlobalStingName(nameStringCount=10):
	global m_randIndex

	vCount=len(''+str(m_randIndex))
	# print("vCount:"+str(vCount))

	randNumber=nameStringCount-vCount
	ida = random.randint(0, randNumber)

	charlist = [random.choice(string.ascii_lowercase) for i in range(randNumber)]
	charlist.insert(ida, str(m_randIndex))
	chars = ''.join(charlist)
	# print("chars:"+str(chars))
	m_randIndex=m_randIndex+1
	return chars


#获取文件路径信息[key文件名字,文件路径,修改后名字]
def getFileNameInfo(value):
	tempPath=str(value).split('/')[-1]
	tPath=str(tempPath).replace('\\','/')
	tName=os.path.splitext(os.path.split(tPath)[-1])[0]
	tNamExtension=os.path.splitext(tPath)[-1]
	tPath=tPath.replace(str(tName)+''+str(tNamExtension),'')

	# tPath=tPath.replace(str(replacePath),'')
	# print('\tapkName:'+tName + ' '+tNamExtension+' path:'+tPath)
	return {
		'fileName':str(tName)+''+str(tNamExtension),
		'name':str(tName),
		'extension':str(tNamExtension)
	}


#拷贝文件(src拷贝路径,dest目标路径)
def copyFile(src, dest):
	buff = ""
	with open(src, 'rb') as f: #以二进制格式打开一个文件用于只读。文件指针将会放在文件的开头。这是默认模式。一般用于非文本文件如图片等。
		buff = f.read()
	with open(dest, 'wb+') as f:#以二进制格式打开一个文件只用于写入。如果该文件已存在则打开文件,并从开头开始编辑,即原有内容会被删除。如果该文件不存在,创建新文件。一般用于非文本文件如图片等。
		f.write(buff)

#过滤目录(vName目录名字,vFilterFileList过滤列表)
def isFilterFileList(vName,vFilterFileList):
	isOpen=True

	splitBig=str(vName).split('.')
	#print('\t\tvName:'+vName+" :"+str(len(splitBig)))
	if len(splitBig)>1:
		return isOpen

	for kv in vFilterFileList:
		if str(kv)==str(vName):
			isOpen=False

	return isOpen

#遍历目录md5(路径vPath,保存的md5值列表形式addMd5)
def fileDir(vPath,vAdd,vfilteredDirectoryList):
	if os.path.isfile(vPath):
		vAdd.append(vPath)
	else:
		tFileList = os.listdir(vPath)
		for value in tFileList:
			if isFilterFileList(value,vfilteredDirectoryList):
				vDir=os.path.dirname(os.path.join(vPath,value))
				tPath=os.path.join(vDir,value)
				# print('\tvalue name:'+str(value)+" path:"+str(tPath))
				if os.path.isdir(tPath):
					# print('\tdir value:'+tPath+" "+value)
					fileDir(tPath,vAdd,vfilteredDirectoryList)
				else:
					# vTemp=getFileNameInfo(tPath,'')
					vAdd.append(tPath)
					# print('\tfile path:'+value)
			else:
				print("\tfiltered directory:"+str(value))

def randomResourceGenerator(value):
	vFilePath=str(value.filePath)
	# vFileUpPath=os.path.abspath(os.path.dirname(vFilePath))
	vImageCount=int(value.imageCount) or 0
	vfileNamePrefix=str(value.fileNamePrefix) or ""
	
	print("path:",vFilePath)
	# print("pathUp:",vFileUpPath)
	print("quantity:",vImageCount)
	print("output path:",m_outPath)
	print("file prefix:",vfileNamePrefix)

	filteredDirectoryList=getParameterContentList(value.filterDirectory)
	print("filtered directory:",value.filterDirectory,' JsonList:',json.dumps(filteredDirectoryList))

	manifest= []
	fileDir(vFilePath,manifest,filteredDirectoryList)
	
	outJsonList=[]
	vCount=len(manifest)
	print('current quantity:'+str(vImageCount)+" total size:"+str(vCount))
	for i in range(vImageCount):
		vid=random.randint(0,vCount)
		vTempName=getFileNameInfo(manifest[vid])
		# name=str(vfileNamePrefix+vTempName['fileName']).lower()
		name=str(vfileNamePrefix+getGlobalStingName()+''+vTempName['extension']).lower()
		vJson="key:"+str(vid)+"\t\tvalue:"+manifest[vid]+"\tname:"+name
		print(vJson)
		outJsonList.append(str(vJson))
		copyFile(manifest[vid],m_outPath+"/"+name)

	txtFile=str(m_outPath+"/ainfo.txt").replace('\\','/')
	makefileUtf8Normal(txtFile,json.dumps(outJsonList))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Project batch tool")
	parser.add_argument("-filePath", "--filePath", help="file Path(文件路径)", default="")

	parser.add_argument("-imageCount", "--imageCount", help="image count(图片数量)", default=0)
	parser.add_argument("-fileNamePrefix", "--fileNamePrefix", help="file name prefix(文件名前缀)", default="")
	parser.add_argument("-filterDirectory", "--filterDirectory", help="filter files(过滤目录)", default="")

	parser.add_argument("-targetPath", "--targetPath", help="target path(目标/输出路径)", default=False)

	args = parser.parse_args()
	if args.targetPath:
		m_outPath=args.targetPath

	randomResourceGenerator(args)
