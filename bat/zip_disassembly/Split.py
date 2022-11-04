# -*- coding: utf-8 -*
import json
import os
import shutil
import sys
import time
import zipfile
from os import path
import random
import string
import datetime
import io
from functools import cmp_to_key
import functools
import struct
import hashlib
import argparse

kilobytes = 1024 #(k为单位)
randomFileSize=[1000,3000] #随机拆解文件大小
rfeType = int(1) #随机文件后缀类型[1获取saveFilePath文件后缀路径,其他是随机]
tNamExtension='' #固定文件后缀名字

def getNumOfString(nameString):
	return sum(bytearray(nameString, "utf-8"))

# Create a normal file
def makefileNormal(vFileName,vContent,vMode):
	# print('Create '+fileName+' file')
	fo = open(vFileName,vMode)# "w+"
	fo.write(vContent)
	fo.close()
	# print('Create file successfully '+vFileName)

def getFileContent(vFilePath,vMode):
	fo = open(''+vFilePath,vMode)
	data = fo.read()
	fo.close()
	return data

def getFileJsonContent(vFilePath):
	fo = open(''+vFilePath)
	data = json.load(fo)
	# print('type:',type(data))
	# value={}
	# for k, v in data.items():
	#	 value[k]=v
	#	 # print(k+':'+v)
	# return value
	fo.close()
	return data

# List sort()
def string_compare(x, y):
	if len(x) != len(y):
		return len(x)-len(y)
	else:
		sum1 = 0
		for i in range(len(x)):
			sum1 = sum1+(ord(x[i]))
		sum2 = 0
		for i in range(len(y)):
			sum2 = sum2+(ord(y[i]))
		return sum1 - sum2

m_randIndex=0
def gen_randomName():
	global m_randIndex

	rMin=10
	rMax=30
	ida=rMin+3
	length = random.randint(rMin, rMax)
	charlist = [random.choice(string.ascii_lowercase) for i in range(length)]
	charlist.insert(ida, str(m_randIndex))
	svalue = ''.join(charlist)

	#前缀-随机几个
	length = 3
	kt_a = [random.choice(string.ascii_lowercase) for i in range(length)]
	kt_b = ''.join(kt_a)
	chars=kt_b+''+svalue #添加几个字母
	chars=kt_b+str(hashlib.md5(chars.encode('utf-8')).hexdigest())
	chars=str(chars).lower() #小写名字

	# print('-->m_randIndex:'+str(m_randIndex)+' chars:'+str(chars))
	m_randIndex=m_randIndex+1
	return chars

def get_nameList():
	nameList = []
	for i in range(1000):
		name = gen_randomName()
		if name[0].isalpha():
			nameList.append(name)
	nameList.sort()
	#print(nameList)
	return nameList

def gen_randomExtension():
	if rfeType == 1:
		return tNamExtension
		
	exList = ["png", "jpg", "wep", "mp3", "mp4", "tff", "wav", "ogg", "config", "package","json",'xml',"data"]
	index = random.randrange(0, len(exList)-1)
	return "."+exList[index]

#拆解文件
def setSplitFile(fromfile,todir,vNameList):
	global randomFileSize
	overAssetFileList = []
	if not os.path.exists(todir):  # check whether todir exists or not
		os.mkdir(todir)

	partnum = 0
	inputfile = open(fromfile, 'rb')  # open the fromfile
	while True:
		chunksize = int(random.randrange(int(randomFileSize[0]), int(randomFileSize[1]))*kilobytes)
		chunk = inputfile.read(chunksize)
		if not chunk:  # check the chunk is empty
			break

		namemidfulpath=""
		if vNameList: # 固定文件名字列表
			namemidfulpath=vNameList[partnum]+''+gen_randomExtension()
		else: # 随机文件名字
			namemidfulpath=gen_randomName()+''+gen_randomExtension()

		# filename = os.path.join(todir, namemidfulpath)
		filename = str(todir+'/'+namemidfulpath).replace('\\','/')
		overAssetFileList.append(namemidfulpath)
		makefileNormal(filename,chunk,'wb')
		partnum += 1
	return overAssetFileList

#文件内容拆解
def fileContentCut(vAssetPath,vOutPath):
	print('\tfile content cut vAssetPath:'+str(vAssetPath)+' outpath:'+str(vOutPath))
	#shutil.rmtree(vOutPath)
	isExists = os.path.exists(vOutPath)
	# 判断结果
	if isExists:
		shutil.rmtree(vOutPath)
	os.makedirs(vOutPath)
	# zipDir(vAssetPath, vOutPath+"/"+"asset.zip")
	vlist=setSplitFile(vAssetPath,vOutPath,False)
	# os.remove(vOutPath+"/"+"asset.zip")
	return vlist

def saveJsonFile(vList,vOutPath,vProportion):
	global randomFileSize
	# print('\tsave file json file rand file Count')
	# print('\trand file count:'+str(vProportion))
	# print('read resource contentA:'+json.dumps(vList))
	tempList = []
	for i in vList:
		print('\twrite path ->:'+str(vOutPath+'/'+i).replace('\\','/'))
		tempList.append(i)
		if vProportion>0:
			for i in range(vProportion):
				vSize=int(random.randrange(int(randomFileSize[0]),int(randomFileSize[1])))*kilobytes/8
				randName=gen_randomName()+''+gen_randomExtension()
				saveBinaryFile(str(vOutPath+'/'+randName).replace('\\','/'),vSize)
				tempList.append(randName)

	new_string = json.dumps(tempList)
	# print('read resource contentB:'+new_string)
	return new_string

# 保存二进制
def saveBinaryFile(vOutPath,vLength):
	vFileContent=''
	for iv in range(vLength):
		datalist=[random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(0,255),random.randint(0,255), random.randint(0,255)]
		abc= struct.pack("!BBBBBBBB", *datalist)
		# print('i:'+str(i)+' '+abc+' type:',type(abc))
		vFileContent=vFileContent+abc

	makefileNormal(vOutPath,vFileContent, 'wb')

def saveStringsXMLFile(vsaveFilePath,vList):
	print('\tsave file xml file path:'+str(vsaveFilePath))
	old_string = "pythonFileJsonString"
	# print('read resource contentA:'+json.dumps(vList))
	new_string = json.dumps(vList)
	with io.open(vsaveFilePath, "rt") as file:
		x = file.read()
		with io.open(vsaveFilePath, "wt", encoding='UTF-8') as file:
			x = x.replace(old_string, new_string)
			file.write(x)
	# print('read resource contentB:'+new_string)

#拆解文件
def onDisassembleFile(vArag):
	print('disassemble File-------------------')
	vAssetFileList=fileContentCut(vArag.assetPath,m_outPath)
	vFileContent=saveJsonFile(vAssetFileList,m_outPath,int(vArag.randomFileRatio))
	makefileNormal(str(vArag.fileContents).replace('\\','/'),vFileContent,"w+")

#合并文件
def onMergeFiles(vArag):
	print('merge Files-------------------')
	vFileList=getFileJsonContent(vArag.fileContents)
	vrFileRatio=int(vArag.randomFileRatio)
	vIndex=0
	vRfilelist=[]
	for v in vFileList:
		vTpath=str(vArag.assetPath+'/'+str(v)).replace('\\','/')
		if vrFileRatio>0:
			if vIndex%(vrFileRatio+1)==0:
				vRfilelist.append(vTpath)
				# print('i:'+str(vIndex)+'->'+str(vTpath))
		else:
			vRfilelist.append(vTpath)
		vIndex=vIndex+1

	sfilePath=str(vArag.mergeFilePath).replace('\\','/')
	vType=2
	if vType==1:
		saveFile = open(sfilePath,"wb")
		for v in vRfilelist:
			print('\tread path 0->'+str(v))
			vfo = open(v,'rb')
			data = vfo.read()
			saveFile.write(data)
			vfo.close()
		saveFile.close()
	elif vType==2:
		vStrContent=''
		for v in vRfilelist:
			print('\tread path 1->'+str(v))
			if len(vStrContent)==0:
				vStrContent=getFileContent(v,'rb')
			else:
				vStrContent=vStrContent+getFileContent(v,'rb')
		makefileNormal(sfilePath,vStrContent,"wb")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Disassemble and merge tool")
	parser.add_argument("-assetPath", "--assetPath", help="资源路径", default='')
	parser.add_argument("-fileContents", "--fileContents", help="文件内容", default='')
	parser.add_argument("-iSortType", "--iSortType", help="内容图集排序[1排序,其他是不排序]", default=1)

	parser.add_argument("-singleFileSize", "--singleFileSize", help="单个文件大小", default='1000,3000')

	parser.add_argument("-randomFileRatio", "--randomFileRatio", help="随机文件比例", default=0)
	parser.add_argument("-randomFileSuffixType", "--randomFileSuffixType", help="随机文件后缀类型[1获取fileContents文件后缀路径,其他是随机]", default=1)

	parser.add_argument("-disassembleFile", "--disassembleFile", help="拆解文件", default=False)
	parser.add_argument("-mergeFiles", "--mergeFiles", help="合并文件", default=False)
	parser.add_argument("-mergeFilePath", "--mergeFilePath", help="合并文件路径", default='')

	parser.add_argument("-targetPath", "--targetPath", help="Target path(目标/输出路径)", default=False)

	args = parser.parse_args()
	if args.targetPath:
		m_outPath=args.targetPath

	rfeType=int(args.randomFileSuffixType)
	if rfeType == 1:
		tNamExtension=os.path.splitext(str(args.fileContents))[-1]  #固定文件后缀名字

	randomFileSize=str(args.singleFileSize).split(',') #随机拆解文件大小
	# print('singleFileSize:',json.dumps(randomFileSize))

	if args.disassembleFile: #拆解文件
		onDisassembleFile(args)
	elif args.mergeFiles: #合并文件
		onMergeFiles(args)

		
	
	


