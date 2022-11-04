#!/usr/bin/python
# -*- coding: UTF-8 -*- 
import json
import os
import subprocess
import shutil
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

# project = (sys.argv[1]) #project name
# fileType = (sys.argv[2]) #create file suffix(.json,.lua,.dat,...)
# readType = (sys.argv[3]) #delete file dir[0no,1yes]
# fileFgf=','
# print('creat project '+project+' fileType split("_")  '+fileType,' delete file dir[0no,1yes] ',readType)
# readFileListName='ffooeexxee_ww33zzz112233.dat'

m_outPath="out"
#execute external commands
def executeExternalCommands(value):
   print('execute external commands:'+str(value))
   m_cp=os.popen(value)
   f=m_cp.read()
   return f

#execute external script
def executeExternalScript(value):
   print('execute external script:'+str(value))
   return subprocess.call(value)

# old project configuration file
def makefileNormal(fileName,content):
   print('makefileNormal Create '+fileName+' file')
   fo = open(fileName, "w+")
   fo.write(content)
   fo.close()
   print('\tCreate file successfully makefileNormal '+fileName)

# old project configuration file
def makefileUtf8Normal(fileName,content):
   print('makefileUtf8Normal Create '+fileName+' file')
   fo = open(fileName, "w+",)
   fo.write(str(content).decode('utf-8', 'ignore'))
   fo.close()
   print('\tCreate file successfully makefileUtf8Normal '+fileName)

# Parameter content cutting(参数内容切割) def getFileName(vIndex,nameStringCount=10):
def getParameterContentList(parameter,nameStringCount=';'):
   splitBig=str(parameter).split(nameStringCount)
   return splitBig

def crc32asii(v):
	return '%08x' % (binascii.crc32(v) & 0xffffffff)
def crc2hex(v):
	return '%08x' % (binascii.crc32(binascii.a2b_hex(v)) & 0xffffffff)

def getDataNumberString(v):
	bStr=''
	vnumber=0
	if type(v) == type([]):
		vnumber=len(v)
	elif type(v) ==  type(1):
		vnumber=1

	if vnumber>0:
		for i in range(vnumber):
			bStr=bStr+'B'

	# print('getDataNumberString:',v,' type:',type(v), ' number:',vnumber,' bStr:',bStr)
	return bStr

def getStrList(v):
	vlist=[]
	if len(v) == 8 :
		vlist.append(int(v[0:2],16))
		vlist.append(int(v[2:2+2],16))
		vlist.append(int(v[4:4+2],16))
		vlist.append(int(v[6:6+2],16))
	return vlist

def getCrcList(v):
	va=crc32asii(v)
	vlist=getStrList(va)
	if len(vlist)==4:
		return [True,vlist]
	return [False,vlist]


#乱序字符串
def getStingName(nameStringCount=10):
	charlist = [random.choice(string.ascii_lowercase) for i in range(nameStringCount)]
	chars = ''.join(charlist)
	return chars

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

#乱序字符串(有序下标)
def getFileName(vIndex,nameStringCount=10):
	mz1=['a','b','c','d','e','f','g','h','i','j','k','m','l','n','o','p','q','r','s','t','u','v','w','x','y','z']
	mz2=['0','1','2','3','4','5','6','7','8','9']
	mz3=['a','b']

	nameTemp=''
	nameTemp=mz1[random.randint(0,len(mz1)-1)]+mz2[random.randint(0,len(mz2)-1)]+mz1[random.randint(0,len(mz1)-1)]+mz1[random.randint(0,len(mz1)-1)]+mz1[random.randint(0,len(mz1)-1)]

	nameCount=nameStringCount #random.randint(3,10)
	for i in range(nameCount):
		if i==0:
			nameTemp=nameTemp+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(vIndex)
		elif i== math.floor(nameCount/2):
			nameTemp=nameTemp+mz3[random.randint(0,len(mz3)-1)]
		else:
			nameTemp=nameTemp+mz1[random.randint(0,len(mz1)-1)]+mz2[random.randint(0,len(mz2)-1)]
	return nameTemp

#获字符串列表(乱序)
def getStringListOutofOrder(value):
	mlist=[]
	count=int(value)
	for i in range(count):
		name=getFileName(i,random.randint(3,6))
		vMd5obj = hashlib.md5(name)
		vHash = vMd5obj.hexdigest()
		vHash = getStingName(2)+vHash
		mlist.append(vHash)
	return mlist

#获字符串列表(序列)
def getStringListSequence(value,isSm=False):
	uppercase=random.choice(string.ascii_uppercase)
	mlist=[]
	count=int(value)
	for i in range(count):
		name=getGlobalStingName(count)
		if isSm:
			name=str(uppercase[random.randint(0,len(uppercase)-1)])+name
		
		vMd5obj = hashlib.md5(name)
		vHash = vMd5obj.hexdigest()
		vHash = getStingName(2)+vHash
		mlist.append(vHash)
	return mlist

def readListDeleteFile(todir,safileName,fileFgf):
	filePath = todir+'\\'+safileName
	isFile=os.path.isfile(filePath)
	# print('read List Delete File:',filePath,' is file:',isFile)
	if isFile :
		maxsize=os.path.getsize(filePath)
		inputfile = open(filePath,'rb')
		data = inputfile.read(maxsize*4)
		inputfile.close()
		vList=data.split(fileFgf)
		# print('read vList:',vList)
		for i in vList:
			isFile=os.path.isfile(todir+'\\'+i)
			# print('i:',i, ' is file:',isFile,' dir:',todir+'\\'+i)
			if isFile :
				os.remove(todir+'\\'+i)
		return vList
	return []

def writeListFile(listData,todir,saName,fileFgf):
	filePath = todir+'\\'+saName
	# print('write List Delete File todir:',todir,' saName:',saName,' filePath:',filePath)
	vindex=0
	vStringCode=''
	# print('write listData:',listData)
	for i in listData:
		vode=i
		if vindex!=len(listData)-1:
			vode=vode+fileFgf
		vStringCode=vStringCode+vode
		vindex=vindex+1

	# print('strCode:',vStringCode)
	isFile=os.path.isfile(filePath)
	inputfile = open(filePath,'wb')
	inputfile.write(vStringCode) 
	inputfile.close()

#创建png格式
def createPngFile():
	sfile=''
	#
	datalist=[137,80,78,71,13,10,26,10] # 0x[89 50 4E 47 0D 0A 1A 0A]
	bcode= struct.pack(getDataNumberString(datalist), *datalist)
	sfile=sfile+bcode

	# IHDR
	# datalist=[00,00,00,13] #[00 00 00 0D]
	# bcode= struct.pack(getDataNumberString(datalist), *datalist)
	bcode= struct.pack('!I', 13) # 10[00,00,00,13] 16[00 00 00 0D]
	sfile=sfile+bcode

	width=random.randint(1,50) #image width
	height=random.randint(1,50) #image height

	bitDepth=4 #Bit depth
	colorType=3 #Color Type
	# print('image width:',width,' image height:',height,' Bit Depth:',bitDepth,' Color Type:',colorType)

	dist=[
		73,72,68,82,#IHDR type code [49 48 44 52]
		0,0,0,width,
		0,0,0,height,
		bitDepth,
		colorType,
		0,
		0,
		0,
	]
	# print('dist:',dist)
	bcode= struct.pack(getDataNumberString(dist), *dist)
	sfile=sfile+bcode

	# print('IHDR data:',bcode)
	datalist=getCrcList(bcode)
	# print('IHDR code:',datalist[0],' list:',datalist[1])
	if datalist[0]==True:
		bcode=struct.pack(getDataNumberString(datalist[1]), *datalist[1])
		sfile=sfile+bcode
	
	# PLTE
	randNumber=random.randint(10,255/colorType)*colorType
	# print('randNumber:',randNumber,' colorType:',colorType,' color number:',randNumber/colorType)

	datalist=[00,00,00,randNumber]
	# print('data:',datalist,' str:',getDataNumberString(datalist))
	bcode= struct.pack(getDataNumberString(datalist), *datalist)
	sfile=sfile+bcode

	dist=[80,76,84,69] #0x[50 4C 54 45]
	count=randNumber/colorType
	for i in range(count):
		dist.extend([random.randint(0,255),random.randint(0,255),random.randint(0,255)])
	
	# print('PLTE data:',dist)
	bcode= struct.pack(getDataNumberString(dist), *dist)
	sfile=sfile+bcode

	datalist=getCrcList(bcode)
	# print('PLTE code:',datalist[0],' list:',datalist[1])
	if datalist[0]==True:
		bcode=struct.pack(getDataNumberString(datalist[1]), *datalist[1])
		sfile=sfile+bcode
	
	# IDAT
	dist=[73,68,65,84] #0x[49,44,41,54]
	count=randNumber/colorType
	# for i in range(count):
	# 	dist.extend([random.randint(0,255),random.randint(0,255),random.randint(0,255)])
	datalist=[]
	for i in range(width):
		for j in range(height):
			datalist.extend([random.randint(0,255),random.randint(0,255),random.randint(0,255)])
	
	dist.extend(datalist)
	# print('dist:',dist)
	idCound=width*height
	bcode= struct.pack('!I', idCound)
	sfile=sfile+bcode

	# print('IDAT data:',dist)
	bcode= struct.pack(getDataNumberString(dist), *dist)
	sfile=sfile+bcode

	datalist=getCrcList(bcode)
	# print('IDAT code:',datalist[0],' list:',datalist[1])
	if datalist[0]==True:
		bcode=struct.pack(getDataNumberString(datalist[1]), *datalist[1])
		sfile=sfile+bcode

	# IEND
	dist=[#0x[00 00 00 00 49 45 4E 44 AE 42 60 82]
		00,00,00,00,
		73,69,78,68,#IEND class code
		174,66,96,130 #crc
	]
	bcode=struct.pack(getDataNumberString(dist), *dist)
	sfile=sfile+bcode
	return sfile

def createFile(saveDir,vName,vfT,cRand):
	#create file data
	vFileContent=''
	randnumber=cRand #内容 多少
	# vfT='.xml'
	if vfT == '.json':
		vFileContent=''
		for i in range(randnumber):
			sxd=[
				'\n\t{\n\t\t"type": "cc.SceneAsset",\n\t\t"_name": "",\n\t\t"_objFlags": 0,\n\t\t"_native": "",\n\t\t"scene": {\n\t\t\t"id": 1\n\t\t},\n\t\t"asyncLoadAssets": false\n\t}',
				'\n\t{\n\t\t"type": "cc.Scene",\n\t\t"_name": "",\n\t\t"_objFlags": 0,\n\t\t"_parent": null,\n\t\t"_children": [\n\t\t\t{\n\t\t\t\t"id": 2\n\t\t\t},\n\t\t\t{\n\t\t\t\t"id": 45\n\t\t\t}\n\t\t],\n\t\t"_active": true,\n\t\t"_components": [],\n\t\t"_prefab": null,\n\t\t"autoReleaseAssets": false,\n\t\t"_globals": {\n\t\t\t"id": 72\n\t\t},\n\t\t"_id": "46a04763-41bc-4a54-8f0c-eecd70b143ca"\n\t}'
			]
			if len(vFileContent)>0:
				vFileContent=vFileContent+','+sxd[random.randint(0,len(sxd)-1)]
			else:
				vFileContent=vFileContent+''+sxd[random.randint(0,len(sxd)-1)]
		vFileContent='['+vFileContent+'\n]'
	elif vfT == '.png' or vfT == '.jpg' or vfT == '.gif':
		vFileContent=createPngFile()
	elif vfT == '.resourcesStringXml':
		vFileContent='<resources>\n'
		for i in range(randnumber):
			vFileContent=vFileContent+'\t<string name="'+getFileName(i,2)+'">'+getFileName(i,random.randint(3,9))+'</string>\n'
		vFileContent=vFileContent+'</resources>'
		vfT = '.xml'
	elif vfT == '.resourcesColorXml':
		vFileContent='<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
		for i in range(randnumber):
			colorList=['0','1','2','3','4','5','6','7','8','9','a','b','c','e','f']
			color=colorList[random.randint(0,len(colorList)-1)]+colorList[random.randint(0,len(colorList)-1)]+colorList[random.randint(0,len(colorList)-1)]+colorList[random.randint(0,len(colorList)-1)]+colorList[random.randint(0,len(colorList)-1)]+colorList[random.randint(0,len(colorList)-1)]
			vFileContent=vFileContent+'\t<color name="'+getFileName(i,2)+'">#'+color.upper()+'</color>\n'
		vFileContent=vFileContent+'</resources>'
		vfT = '.xml'
	elif vfT == '.xml':
		viewportWidthHeight=random.randint(30,90)
		vFileContent='<?xml version="1.0" encoding="utf-8"?>\n<vector xmlns:android="http://schemas.android.com/apk/res/android"\n\tandroid:width="'+viewportWidthHeight+'dp"\n\tandroid:height="'+viewportWidthHeight+'dp"\n\tandroid:viewportWidth="'+viewportWidthHeight+'"\n\tandroid:viewportHeight="'+viewportWidthHeight+'">\n'
		for i in range(randnumber):
			colorList=['0','1','2','3','4','5','6','7','8','9','a','b','c','e','f']
			color=colorList[random.randint(0,len(colorList)-1)]+colorList[random.randint(0,len(colorList)-1)]+colorList[random.randint(0,len(colorList)-1)]+colorList[random.randint(0,len(colorList)-1)]+colorList[random.randint(0,len(colorList)-1)]+colorList[random.randint(0,len(colorList)-1)]
			vpathData='M0,0h108v108h-108z'
			# M(x y) 把画笔移动到x,y,要准备在这个地方画图了。
			# L(x y) 直线连到x,y,还有简化命令H(x) 水平连接、V(y)垂直连接。
			# Z没有参数,连接起点和终点
			# C(x1 y1 x2 y2 x y),控制点(x1,y1) (x2,y2)终点x,y
			# Q(x1 y1 x y),控制点(x1,y1),终点x,y
			# C和Q会在下文做简单对比。
			# A(rx ry(椭圆半径) x-axis-rotation(轴旋转角度) large-arc-flag(为0时表示取小弧度，1时取大弧度) sweep-flag(取逆时针方向,1取顺时针方向) x y)
			# pd_m='M'+str(random.randint(0,viewportWidthHeight))+','+str(random.randint(0,viewportWidthHeight))
			# vlist=[
			# 	'a'+str(random.randint(0,viewportWidthHeight))+','+str(random.randint(0,viewportWidthHeight))+' 1,1 0 1,0',
			# 	'L'+str(random.randint(0,viewportWidthHeight))+','+str(random.randint(0,viewportWidthHeight))+' '+str(random.randint(0,viewportWidthHeight))+','+str(random.randint(0,viewportWidthHeight))+'',
			# 	'c0,0 '+str(random.randint(0,viewportWidthHeight))+','+str(random.randint(0,viewportWidthHeight))+' '+str(random.randint(0,viewportWidthHeight))+','+str(random.randint(0,viewportWidthHeight))+''
			# ]
			vFileContent=vFileContent+'\t<path\n\t\tandroid:fillColor="#'+color+'"\n\t\tandroid:pathData="zzzsd"/>\n'
		vFileContent=vFileContent+'\n</vector>'

		# vFileContent='<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
		# xmlList=['string','subchild','message','note','title','book','author','year','price','color']
		# sxList=['name','lang','category']
		# for i in range(randnumber):
		# 	xmlkey=xmlList[random.randint(0,len(xmlList)-1)]
		# 	if xmlkey == 'color' :
		# 		colorList=['0','1','2','3','4','5','6','7','8','9','a','b','c','e','f']
		# 		color=colorList[random.randint(0,len(colorList)-1)]+colorList[random.randint(0,len(colorList)-1)]+colorList[random.randint(0,len(colorList)-1)]+colorList[random.randint(0,len(colorList)-1)]+colorList[random.randint(0,len(colorList)-1)]+colorList[random.randint(0,len(colorList)-1)]
		# 		vFileContent=vFileContent+'\t<'+xmlkey+' name="'+getFileName(i,2)+'">#'+color.upper()+'</'+xmlkey+'>\n'
		# 	else:
		# 		vFileContent=vFileContent+'\t<'+xmlkey+' '+sxList[random.randint(0,len(sxList)-1)]+'="'+getFileName(i,2)+'">'+getFileName(i,2)+'</'+xmlkey+'>'
		# vFileContent=vFileContent+'\n</resources>'
	else:
		vFileContent=''
		for i in range(randnumber):
			datalist=[random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(0,255),random.randint(0,255), random.randint(0,255)]
			abc= struct.pack("!BBBBBBBB", *datalist)
			# print('i:'+str(i)+' '+abc+' type:',type(abc))
			vFileContent=vFileContent+abc

	fileName=str(saveDir+'/'+vName+vfT).replace('\\','/')
	makefileNormal(fileName,vFileContent)

# fileType
def forInFile(vSavePath,vFileCount,value):
	zhList=['json','png','xml']
	for kv in range(vFileCount):
		name=getStingName(int(vFileCount/vFileCount))+str(kv)+getStingName(int(vFileCount/vFileCount))
		createFile(vSavePath,name,'.'+zhList[random.randint(0,len(zhList)-1)],random.randint(100,300))

# 创建函数
def createMethod(methodName):
	purviewList=['public','private','protected'] #权限
	typeList={ # 基础类型
		# 'byte':{'size':"Byte.SIZE",'min':"Byte.MIN_VALUE",'max':"Byte.MAX_VALUE",'default':"0"},
		# 'short':{'size':"Short.SIZE",'min':"Short.MIN_VALUE",'max':"Short.MAX_VALUE",'default':"0"},
		'int':{'size':"Integer.SIZE",'min':"Integer.MIN_VALUE",'max':"Integer.MAX_VALUE",'default':"0"},
		'long':{'size':"Long.SIZE",'min':"Long.MIN_VALUE",'max':"Long.MAX_VALUE",'default':"0L"},
		'float':{'size':"Float.SIZE",'min':"Float.MIN_VALUE",'max':"Float.MAX_VALUE",'default':'0.01f'},
		'double':{'size':"Double.SIZE",'min':"Double.MIN_VALUE",'max':"Double.MAX_VALUE",'default':'0.01f'},
		'String':{'size':"Character.SIZE",'min':"(int)Character.MIN_VALUE",'max':"(int)Character.MAX_VALUE",'default':'""'},
		'boolean':{'size':"2",'min':"0",'max':"1",'default':"false"},
		'void':{'size':'','min':'','max':'','default':''},
	}

	vTypeKey=typeList.keys() # 随机类型
	for i in range(8):
		vTypeKey.append('void')

	# 权限
	vPurview=purviewList[random.randint(0,len(purviewList)-1)]
	# 返回值类型
	vReturnType=vTypeKey[random.randint(0,len(vTypeKey)-1)]

	#参数类型
	vsArgs=''
	vArgsList=[]
	argsContent=[vTypeKey[random.randint(0,len(vTypeKey)-1)],vTypeKey[random.randint(0,len(vTypeKey)-1)],vTypeKey[random.randint(0,len(vTypeKey)-1)],vTypeKey[random.randint(0,len(vTypeKey)-1)],vTypeKey[random.randint(0,len(vTypeKey)-1)],vTypeKey[random.randint(0,len(vTypeKey)-1)],vTypeKey[random.randint(0,len(vTypeKey)-1)],vTypeKey[random.randint(0,len(vTypeKey)-1)]]
	for akv in argsContent:
		if akv != "void":
			vArgsList.append(akv)
			if(len(vsArgs)<=0):
				vsArgs=vsArgs+akv+' '+getStingName(len(akv))+str(random.randint(0,9))
			else:
				vsArgs=vsArgs+','+akv+' '+getStingName(len(akv))+str(random.randint(0,9))

	vContent='\t'+vPurview+' '+vReturnType+' '+methodName+'('+vsArgs+'){\n'
	vJk=random.randint(0,7)
	if vJk==0:
		via=getStingName(3)+str(random.randint(0,10))
		vrid=random.randint(1,9)
		vContent=vContent+'\t\tint '+via+' = 0;\n\t\tfor (int i = 0; i < '+str(vrid)+'; i++) {\n\t\t\t'+via+' += i;\n\t\t}\n'
	elif vJk==1:
		vContent=vContent+'\t\tSystem.out.println("'+getStingName(random.randint(3,9))+'");\n'
	elif vJk==2:
		v2ina=getStingName(4)+str(random.randint(0,10))
		v2inb=getStingName(5)+str(random.randint(0,10))
		v2inc=getStingName(6)+str(random.randint(0,10))
		vContent=vContent+'\t\tString '+v2ina+'="'+getStingName(random.randint(1,9))+'";\n\t\tString '+v2inb+'="'+getStingName(random.randint(1,9))+'";\n\t\tString '+v2inc+'='+v2ina+'+'+v2inb+';\n\t\tSystem.out.println(""+'+v2inc+');\n'
	elif vJk==3:
		vi3b=getStingName(4)+str(random.randint(0,10))
		vContent=vContent+'\t\tlong '+vi3b+' = System.currentTimeMillis();\n\t\tif (System.currentTimeMillis() < '+vi3b+') {\n\t\t\tSystem.out.println("'+getStingName(random.randint(3,9))+'");\n\t\t} else if (System.currentTimeMillis() == '+vi3b+') {\n\t\t\tSystem.out.println("'+getStingName(random.randint(3,9))+'");\n\t\t} else {\n\t\t\tSystem.out.println("'+getStingName(random.randint(3,9))+'"); \n\t\t}\n'
	elif vJk==4:
		v4ina=getStingName(4)+str(random.randint(0,10))
		v4inb=getStingName(5)+str(random.randint(0,10))
		v4inc=getStingName(6)+str(random.randint(0,10))
		vContent=vContent+'\t\tint '+v4ina+'='+str(random.randint(0,10))+';\n\t\tint '+v4inb+'='+str(random.randint(0,10))+';\n\t\tint '+v4inc+'='+v4ina+'+'+v4inb+';\n'
	elif vJk==5:
		v5ina=getStingName(4)+str(random.randint(0,10))
		v5inb=getStingName(5)+str(random.randint(0,10))
		v5inc=getStingName(6)+str(random.randint(0,10))
		vContent=vContent+'\t\tint '+v5ina+'='+str(random.randint(0,10))+';\n\t\tint '+v5inb+'='+str(random.randint(0,10))+';\n\t\tint '+v5inc+'='+v5ina+'-'+v5inb+';\n'
	elif vJk==6:
		v6ina=getStingName(4)+str(random.randint(0,10))
		v6inb=getStingName(5)+str(random.randint(0,10))
		v6inc=getStingName(6)+str(random.randint(0,10))
		vContent=vContent+'\t\tint '+v6ina+'='+str(random.randint(0,10))+';\n\t\tint '+v6inb+'='+str(random.randint(0,10))+';\n\t\tint '+v6inc+'='+v6ina+'*'+v6inb+';\n'
	elif vJk==7:
		v7ina=getStingName(4)+str(random.randint(0,10))
		v7inb=getStingName(5)+str(random.randint(0,10))
		v7inc=getStingName(6)+str(random.randint(0,10))
		vContent=vContent+'\t\tint '+v7ina+'='+str(random.randint(0,10))+';\n\t\tint '+v7inb+'='+str(random.randint(1,10))+';\n\t\tint '+v7inc+'='+v7ina+'%'+v7inb+';\n'

	if vReturnType != "void":
		vContent=vContent+'\t\treturn '+typeList[vReturnType]['default']+';\n'

	vContent=vContent+'\t}\n'

	vJson={
		'name':methodName,# 函数名字
		'argsList':vArgsList,# 参数列表
		'returnType':vReturnType,# 返回类型
		'purview':vPurview,# 函数权限
		'content':vContent,# 函数内容
		'baseType':typeList # 基础类型
	}
	return vJson

# 创建java类-调用类
def createJavaGatherClass(className,GatherA,GatherB,value):
	packageName=str(value.packageName)
	fileExtension='.java'
	content=''

	content='package '+packageName+';\n\n'
	content=content+'public class '+className+' {\n\n'

	# 调用函数
	content=content+'\tpublic void main(){\n'
	for kv in GatherA:
		vasu=''
		content=content+'\t\tnew '+str(value.classPrefix+kv)+'('+str(vasu)+').toMethod();\n'
	for kv in GatherB:
		vasu=''
		content=content+'\t\tnew '+str(value.classPrefix+kv)+'('+str(vasu)+').toMethod();\n'
	content=content+'\t}\n'

	content=content+'}'
	packagePath=str(packageName).replace('.','/')
	firName=value.targetPath+'/'+packagePath+"/"+className
	# print("Create java class - call class:"+firName)
	makefileNormal(firName+fileExtension,content)

# 创建java类-基础
def createJavaClass(className,methodList,extendsClass,value):
	packageName=str(value.packageName)

	print('create Java Class ----------------packageName:'+str(packageName)+" className:"+str(className)+" extendsClass:"+extendsClass)
	fileExtension='.java'
	content=''
	if len(extendsClass)>0:#有继承类
		vClassR=str(value.activityClassR)
		if len(vClassR)<=0:
			vClassR=packageName

		content='package '+packageName+';\n\n'
		content=content+'import '+vClassR+'.R;\n'
		content=content+'import android.app.Activity;\n'
		content=content+'import android.os.Bundle;\n'

		content=content+'import java.lang.Exception;\n'
		content=content+'import java.lang.Override;\n'
		content=content+'import java.lang.RuntimeException;\n'
		content=content+'import java.lang.String;\n'
		content=content+'import java.lang.System;\n'
		content=content+'import java.util.Date;\n\n'

		content=content+'public class '+className+' extends '+extendsClass+' {\n\n'
		content=content+'\t@Override\n'
		content=content+'\tprotected void onCreate(Bundle savedInstanceState) {\n'
		content=content+'\t\tsuper.onCreate(savedInstanceState);\n'
		content=content+'\t\tsetContentView(R.layout.activity_'+className.lower()+');\n'
		content=content+'\t}\n'
	else:
		content='package '+packageName+';\n'
		content=content+'public class '+className+' {\n'

	listMethod=[]
	# 函数内容
	for kv in methodList:
		vMethod=createMethod(kv)
		listMethod.append(vMethod)
		content=content+vMethod['content']

	# 调用函数
	content=content+'\tpublic void toMethod(){\n'
	for kv in listMethod:
		baseType=kv['baseType']
		vasu=''
		# print('argsList:'+json.dumps(kv['argsList']))
		for ak in kv['argsList']: # 参数列表
			vcs=str(baseType[''+ak]['default'])
			if(len(vasu)<=0):
				vasu=vasu+vcs
			else:
				vasu=vasu+','+vcs
		content=content+'\t\t'+str(kv['name'])+'('+str(vasu)+');\n'
	content=content+'\t}\n'

	content=content+'}'

	packagePath=str(packageName).replace('.','/')
	makefileNormal(value.targetPath+'/'+packagePath+"/"+className+fileExtension,content)

m_xmlIndex=0
def createActivityXml(className,savePath,value):
	global m_xmlIndex

	orientation=['vertical','horizontal']
	gravity=['center','left','right','top','bottom']
	controls=['TextView','ImageView','ImageButton','Button']

	fileName='activity_'+str(className).lower()+'.xml'
	content='<?xml version="1.0" encoding="utf-8"?>\n'
	content=content+'<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"\n'
	content=content+'\tandroid:layout_width="match_parent"\n'
	content=content+'\tandroid:layout_height="match_parent"\n'
	content=content+'\tandroid:orientation="'+orientation[random.randint(0,len(orientation)-1)]+'">\n'

	idrand=getStingName(random.randint(1,3))+str(m_xmlIndex)+'_'+getStingName(random.randint(3,9))
	content=content+'\t<'+controls[random.randint(0,len(controls)-1)]+'\n'
	content=content+'\t\tandroid:id="@+id/'+idrand+'"\n'
	content=content+'\t\tandroid:layout_width="wrap_content"\n'
	content=content+'\t\tandroid:layout_height="wrap_content"\n'
	content=content+'\t\tandroid:layout_gravity="'+gravity[random.randint(0,len(gravity)-1)]+'" />\n'

	content=content+'</LinearLayout>'
	makefileNormal(savePath+'/'+fileName,content)

	m_xmlIndex=m_xmlIndex+1

# 创建 AndroidManifest.xml 文件
def createActivityManifestXml(vActivityList,savePathName,value):
	packageName=str(value.packageName)
	content='<manifest xmlns:android="http://schemas.android.com/apk/res/android">\n'
	content=content+'\t<application>\n'
	varAdd=' android:screenOrientation="landscape" android:configChanges="orientation|keyboardHidden|screenSize" android:launchMode="singleTask" android:taskAffinity="'+str(packageName)+'"'
	for kv in vActivityList:
		content=content+'\t\t<activity android:name="'+packageName+'.'+str(''+value.classPrefix+''+kv)+'"'+varAdd+'/>\n'

	content=content+'\t</application>\n'
	content=content+'</manifest>'
	makefileNormal(savePathName,content)

def randomResourceGenerator(value):
	packageName=str(value.packageName).replace('.','/')
	packagePath=str(value.targetPath+'/'+packageName).replace('\\','/')
	drawablePath=str(value.targetPath+'/res/drawable').replace('\\','/')
	layoutPath=str(value.targetPath+'/res/layout').replace('\\','/')
	valuesPath=str(value.targetPath+'/res/values').replace('\\','/')

	if not os.path.exists(packagePath):
		os.makedirs(packagePath)
	if not os.path.exists(drawablePath):
		os.makedirs(drawablePath)
	if not os.path.exists(layoutPath):
		os.makedirs(layoutPath)
	if not os.path.exists(valuesPath):
		os.makedirs(valuesPath)

	print("\tCreate directory successfully")
	
	# activityCount(activity数量)
	vActivityClassName=[]
	if value.activityCount and int(value.activityCount)>0:
		vActivityClassName=getStringListSequence(value.activityCount,True) #获字符串列表(序列)
		for kv in vActivityClassName:
			methodList=getStringListOutofOrder(value.methodCount) #获字符串列表(乱序)
			createJavaClass(value.classPrefix+kv,methodList,'Activity',value)
			createActivityXml(value.classPrefix+kv,layoutPath,value)

		createActivityManifestXml(vActivityClassName,str(value.targetPath+'/AndroidManifest.xml').replace('\\','/'),value)

	# classCount(类数量)
	vClassName=[] #获字符串列表(序列)
	if value.classCount and int(value.classCount)>0:
		vClassName=getStringListSequence(value.classCount,True) #获字符串列表(序列)
		for kv in vClassName:
			methodList=getStringListOutofOrder(value.methodCount) #获字符串列表(乱序)
			createJavaClass(value.classPrefix+kv,methodList,'',value)
	
	# calling class Name(调用类名字)
	if value.callingClassName and len(value.callingClassName)>0:
		createJavaGatherClass(str(value.callingClassName),vActivityClassName,vClassName,value)

	# assetsDrawableCount(资源drawable目录数量)
	# if value.assetsDrawableCount and int(value.assetsDrawableCount)>0:
	# 	forInFile(drawablePath,int(value.assetsDrawableCount),value)

	# 资源values/strings.xml目录数量
	if value.stringCount and int(value.stringCount)>0:
		createFile(valuesPath,'strings','.resourcesStringXml',int(value.stringCount))

	# 资源values/colors.xml目录数量
	if value.colorCount and int(value.colorCount)>0:
		createFile(valuesPath,'colors','.resourcesColorXml',int(value.colorCount))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Project batch tool")
	parser.add_argument("-packageName", "--packageName", help="packageName(包名)", default=False)
	parser.add_argument("-packageCount", "--packageCount", help="packageCount(包名数量)", default=0)
	parser.add_argument("-activityCount", "--activityCount", help="activityCount(activity数量)", default=0)
	parser.add_argument("-activityClassR", "--activityClassR", help="activityClassR(.R文件)", default="")
    
	parser.add_argument("-classCount", "--classCount", help="classCount(类数量)", default=0)
	parser.add_argument("-methodCount", "--methodCount", help="methodCount(方法数量)", default=0)
	parser.add_argument("-assetsDrawableCount", "--assetsDrawableCount", help="assetsDrawableCount(资源drawable目录数量)", default=0)

	parser.add_argument("-stringCount", "--stringCount", help="stringCount(资源values/strings.xml目录数量)", default=0)
	parser.add_argument("-colorCount", "--colorCount", help="colorCount(资源values/colors.xml目录数量)", default=0)

	parser.add_argument("-classPrefix", "--classPrefix", help="class Prefix(类名前缀)", default='')

	parser.add_argument("-callingClassName", "--callingClassName", help="calling class Name(调用类名字)", default=False)

	parser.add_argument("-targetPath", "--targetPath", help="target path(目标/输出路径)", default=False)

	args = parser.parse_args()
	if args.targetPath:
		m_outPath=args.targetPath

	randomResourceGenerator(args)
