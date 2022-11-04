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

m_capital=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
m_lowerCase=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
m_number=['0','1','2','3','4','5','6','7','8','9']

m_cln=[]
for i in range(len(m_capital)):
	m_cln.append( m_capital[i] )
for i in range(len(m_lowerCase)):
	m_cln.append( m_lowerCase[i] )
for i in range(len(m_number)):
	m_cln.append( m_number[i] )

m_outPath=str(os.getcwd()+"/out").replace('\\','/')
# print('m_outPath:'+m_outPath)

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

# 判断路径是否存在
def isPathExists(name):
	if os.path.exists(name):
		return True
	return False

# 路径是文件或目录[0文件,1目录] 默认-1
def isFileDir(name):
	if os.path.isdir(name):
		return 1
	elif os.path.isfile(name):
		return 0
	return -1

def copyFileDir(vCn,vCt):
	vType=isFileDir(vCn)
	if vType==-1:
		print('\tcopyFileDir Failed to delete file:'+str(vCn))
		return
	
	if vType==0: #file
		executeExternalScript('command.bat copyFile '+vCn.replace("/", "\\")+" "+vCt.replace("/", "\\"))
	elif vType==1: #dir
		ef=executeExternalScript('command.bat copySpecifiedDirectory '+vCn.replace("/", "\\")+" "+vCt.replace("/", "\\"))
		print('ef:',ef)

def deleteFileDir(vpath):
	vType=isFileDir(vpath)
	if vType==-1:
		print('\tdeleteFileDir Failed to delete file:'+str(vpath))
		return

	if vType==0: #file
		executeExternalScript('command.bat deleteFile '+vpath.replace("/", "\\"))
	elif vType==1: #dir
		executeExternalScript('command.bat deleteDirectory '+vpath.replace("/", "\\"))

def getConfigurationTable(jsonFile):
	fo = open(''+jsonFile)
	data = json.load(fo)
	# print('type:',type(data))
	# value={}
	# for k, v in data.items():
	#	 value[k]=v
	#	 # print(k+':'+v)
	# return value
	fo.close()
	return data

# old project configuration file
def makefileNormal(fileName,content):
	print('\tCreate '+fileName+' file')
	fo = open(fileName, "w+")
	fo.write(content)
	fo.close()
	print('\t\tCreate file successfully '+fileName)

# old project configuration file
def makefileUtf8Normal(fileName,content):
	print('\tCreate '+fileName+' file')
	fo = open(fileName, "w+",)
	fo.write(str(content).decode('utf-8', 'ignore'))
	fo.close()
	print('\t\tCreate file successfully '+fileName)

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

def getParameterList(args):
	vTemp=getParameterContentList(args)
	vContent=[]
	for kv in vTemp:
		# print('type:',type(kv),' kv:',kv)
		if str(type(kv)) == "<type 'str'>":
			vContent.append(kv)
		elif str(type(kv))=="<type 'dict'>":
			for iv in range(0,kv['count']):
				vContent.append(kv[str(iv)])
	return vContent

def getPlatformList(platform,vConfig):
	vPlatform=getParameterList(platform)

	# ('vArrayPlatform:', '[{"1": "TeenpattiField", "0": "n_rummybest", "count": 2}]', ' len:', 1)
	# print('vPlatform:',json.dumps(vPlatform),' len:',len(vPlatform))

	allProjectList=vConfig['allProjectList']
	vProjectlist={}
	for kpf in vPlatform:
		isPlatform=vConfig.has_key(kpf)
		if str(kpf).lower() == "all": #全平台 kpf=="all" or kpf=="ALL"
			vProjectlist=allProjectList
			break
		elif isPlatform: #指定平台
			project=vConfig[kpf]
			vlist=project['project_list']
			for vky in vlist:
				vProjectlist[vky]=vlist[vky]
		else: #单个项目
			istPlatform=allProjectList.has_key(kpf)
			if istPlatform:
				vtj=allProjectList[kpf]
				vProjectlist[kpf]=vtj

	# print('---------------------------')
	# print('vProjectlist:',json.dumps(vProjectlist))
	# print('len:',len(vProjectlist))
	return vProjectlist

def getProjectPathIntegration(vconfig):
	m_config={}
	value=getConfigurationTable(vconfig)
	if not value:
		print('Getting file data error:'+str(vconfig))
		return m_config
	
	# 解析工作路径下的项目
	_projectsJson={}
	isprojectPath=value.has_key('projectPath')
	if isprojectPath:
		_projectPath=value['projectPath']['user_vs_path']
		# print('aabbcc:',json.dumps(_projectPath))
		for v in _projectPath:
			# print(''+_projectPath[v])
			if isPathExists(_projectPath[v]):
				# print('v:'+_projectPath[v])
				listDir=getConfigurationTable(_projectPath[v])
				if listDir:
					for iv in listDir:
						# "rootPath": "D://git//SvnLocal//client-dabao//Cocos2dx_lua_studio//n_teen_patti_royal",
						vTemp=str(iv['rootPath']).replace('\\','/')
						vTemp=str(vTemp).replace('//','/')
						split=vTemp.split('/')
						key=split[len(split)-1]
						if isPathExists(vTemp):
							_projectsJson[key]=vTemp
				# print('\tv:'+v+' '+json.dumps(_projectsJson))
	
	# 平台项目集合
	_projectlist={}
	_platformList=value['platformList']
	for v in _platformList:
		vTemp=value[v]
		if vTemp:
			vJson={}
			vJson['info']=vTemp['info']
			vList={}
			project_list=vTemp['project_list']
			for vkey in project_list:
				item=project_list[vkey]
				split=item['path'].split('/')
				key=split[len(split)-1]
				if isPathExists(item['path']):
					vList[key]=item
					_projectlist[key]=item
				else:
					isTempProject=_projectsJson.has_key(key)
					if isTempProject:
						# print('key:'+str(key)+' '+_projectsJson[key])
						item['path']=_projectsJson[key]
						vList[key]=item
						_projectlist[key]=item
			vJson['project_list']=vList
			m_config[v]=vJson

	m_config['allProjectList']=_projectlist
	# print('list:'+json.dumps(m_config))
	return m_config

def svnCommand(command):
	command_str=''
	if command =='update':
		command_str='svn update'

	print('\t\tsvn command:'+command_str)
	if len(command_str)>1:
		echo_c=executeExternalCommands(command_str)
		print(echo_c)

# 获取随机字符串(randNumber随机几个字符,xl唯一标识符)
def getRandString(randNumber,xl):
	outStrin=''
	isOpen=False
	ida=random.randint(0,randNumber)
	for i in range(randNumber):
		outStrin=m_cln[random.randint(0,len(m_cln)-1)]+outStrin
		if i==ida:
			outStrin=outStrin+str(xl)
			isOpen=True
	if not isOpen:
		outStrin=outStrin+str(xl)
	# print('\tget a random string number:'+str(randNumber)+' ida:'+str(ida)+' outStrin:'+str(outStrin))
	return outStrin
	
def createKeystoreJks(keystoreName,keystoreAlias,keystorePassword,keystoreAliasPassword,keyRandomNumber,outPaht):
	print('create key')
	if not os.path.exists(outPaht):
		os.makedirs(outPaht)

	dname='''cn={cn},ou={ou},o={o},l={l},st={st},c={c}'''
	jksCommands='''keytool -genkey -v -keystore {keyName} -alias {alias} -storepass {storepass} -keypass {keypass} -keyalg RSA -keysize 2048 -validity 36500 -dname {dname}'''
	keystoreCommands='''keytool -genkey -v -keystore {keyName} -alias {alias} -storepass {storepass} -keypass {keypass} -keyalg RSA -validity 20000 -dname {dname}'''

	splitext=os.path.splitext(keystoreName)[-1]
	sun=int(keyRandomNumber) or 0
	print('\tkeyRandomNumber:'+str(keyRandomNumber)+' sun:'+str(sun)+' splitext:'+splitext)
	if sun>0:
		for i in range(sun):
			vKeyName=str(getRandString(9,i)).lower()+str(splitext)
			vAlias=str(getRandString(5,i)).lower()
			storePassword=str(getRandString(12,i)).lower()
			storeAliasPassword=storePassword

			key_dname_cn=str(getRandString(2,random.randint(1,9))).lower()
			key_dname_ou=str(getRandString(2,random.randint(1,9))).lower()
			key_dname_o=str(getRandString(2,random.randint(1,9))).lower()
			key_dname_l=str(getRandString(2,random.randint(1,9))).lower()
			key_dname_st=str(getRandString(2,random.randint(1,9))).lower()
			key_dname_c=str(getRandString(2,random.randint(1,9))).lower()
			outDname = dname.format(cn=str(key_dname_cn),ou=str(key_dname_ou),o=str(key_dname_o),l=str(key_dname_l),st=str(key_dname_st),c=str(key_dname_c))

			content=''+str(vKeyName)+'\n\tkeystoreAlias='+str(vAlias)+'\n\tkeystorePassword='+str(storePassword)+'\n\tkeystoreAliasPassword='+str(storeAliasPassword)+'\n\tdname="'+str(outDname+'"')
			print(str(i)+' content:'+content)
			
			outC=''
			if str(splitext) == '.jks':
				outC=jksCommands.format(keyName=str(outPaht+'/'+vKeyName),alias=str(vAlias),storepass=str(storePassword),keypass=str(storeAliasPassword),dname=str(outDname))
			elif str(splitext) == '.keystore':
				outC=keystoreCommands.format(keyName=str(outPaht+'/'+vKeyName),alias=str(vAlias),storepass=str(storePassword),keypass=str(storeAliasPassword),dname=str(outDname))

			# print('\tlen outC:'+str(len(outC)))
			if(len(outC)>0):
				pKeyName=str(outPaht+'/'+vKeyName+'.txt')
				if os.path.exists(pKeyName):
					print('\tThe file will not be created if it exists '+pKeyName)
					return
				makefileNormal(pKeyName,content)
				executeExternalCommands(outC)
			else:
				print('\tFailed to create file '+str(vKeyName)+' Command parameters:'+outC)
	else:
		vKeyName=''+keystoreName
		vAlias=''+keystoreAlias
		storePassword=''+keystorePassword
		storeAliasPassword=''+keystoreAliasPassword

		key_dname_cn=str(getRandString(2,random.randint(1,9))).lower()
		key_dname_ou=str(getRandString(2,random.randint(1,9))).lower()
		key_dname_o=str(getRandString(2,random.randint(1,9))).lower()
		key_dname_l=str(getRandString(2,random.randint(1,9))).lower()
		key_dname_st=str(getRandString(2,random.randint(1,9))).lower()
		key_dname_c=str(getRandString(2,random.randint(1,9))).lower()
		outDname = dname.format(cn=str(key_dname_cn),ou=str(key_dname_ou),o=str(key_dname_o),l=str(key_dname_l),st=str(key_dname_st),c=str(key_dname_c))

		content=''+str(vKeyName)+'\n\tkeystoreAlias='+str(vAlias)+'\n\tkeystorePassword='+str(storePassword)+'\n\tkeystoreAliasPassword='+str(storeAliasPassword)+'\n\tdname="'+str(outDname+'"')
		print('content:'+content)

		outC=''
		if str(splitext) == '.jks':
			outC=jksCommands.format(keyName=str(outPaht+'/'+vKeyName),alias=str(vAlias),storepass=str(storePassword),keypass=str(storeAliasPassword),dname=str(outDname))
		elif str(splitext) == '.keystore':
			outC=keystoreCommands.format(keyName=str(outPaht+'/'+vKeyName),alias=str(vAlias),storepass=str(storePassword),keypass=str(storeAliasPassword),dname=str(outDname))

		# print('\tlen outC:'+str(len(outC)))
		if(len(outC)>0):
			pKeyName=str(outPaht+'/'+vKeyName+'.txt')
			if os.path.exists(pKeyName):
				print('\tThe file will not be created if it exists '+pKeyName)
				return
			makefileNormal(pKeyName,content)
			executeExternalCommands(outC)
		else:
			print('\tFailed to create file '+str(vKeyName)+' Command parameters:'+outC)

# Compile the specified directory
def compileTheSpecifiedDirectory(project,singleGame,lck,lcv,name,outPath):
	print('Compile the specified directory')
	path=str(project["path"])
	projectName=str(project["name"])
	luacompile_key=project['luacompile_key']
	luacompile_value=project['luacompile_value']
	
	print('\tproject name:'+str(name)+' != '+projectName+' lua key:'+str(lck)+' lua value:'+str(lcv))
	if projectName != name:
		if luacompile_key == lck or luacompile_value == lcv:
			print('\tThe same can not be packaged :'+str(name))
			return

	outPath=outPath+'/'+name

	pathName=path+'/'+singleGame
	zzde=singleGame.split('/')
	gameName=zzde[len(zzde)-1]
	outPaht=outPath+'/'+gameName
	command_single='cocos luacompile -s '+pathName+' -d '+outPaht+' -e -k '+lck+' -b '+lcv+' --disable-compile'
	executeExternalCommands(command_single)

	executeExternalScript('command.bat copyDirectorySpecifiedDirectory '+pathName.replace("/", "\\")+' '+outPaht.replace("/", "\\"))
	executeExternalScript('command.bat createMd5File '+outPaht.replace("/", "\\"))

	outName=outPaht.replace("/", "\\")
	executeExternalScript('command.bat compressedFile '+outName+'.zip'+' '+outName)

# package sub game
def packageSubGame(vCa,vConfig):
	print('package sub game:'+str(vCa.subgamePath))
	if not vCa.subgamePath:
		print('\tNo subgame path'+str(vCa.subgamePath))
		return

	targetPath=m_outPath
	if vCa.targetPath:
		targetPath=vCa.targetPath

	allProjectList=vConfig['allProjectList']
	project={}
	vProjectlist={}
	vArraySubgame=getParameterList(vCa.subgamePath)

	if vCa.projectName: #打包项目-子游戏
		isTempProject=allProjectList.has_key(vCa.projectName)
		if not isTempProject :
			print('\titem does not exist ->'+str(vCa.projectName))
			return

		project=allProjectList[vCa.projectName]
		pname=str(project["name"])
		ppath=str(project["path"])
		pm_configure=getConfigurationTable(ppath+"/info/PythonConfigure.json")
		pluacompile_key=pm_configure['luacompile_key']
		pluacompile_value=pm_configure['luacompile_value']
		value={
			"name":pname,
			"path":ppath,
			"luacompile_key":pluacompile_key,
			"luacompile_value":pluacompile_value,
		}
		print('\tprojectName:'+str(vCa.projectName)+' subgamePath:'+str(vCa.subgamePath))
		for kv in vArraySubgame:
			print('\t\tsubgamePath:'+kv)
			compileTheSpecifiedDirectory(value,kv,pluacompile_key,pluacompile_value,pname,targetPath)
	elif vCa.copyProject: #打包平台-子游戏
		project=allProjectList[vCa.copyProject]
		pname=str(project["name"])
		ppath=str(project["path"])
		pm_configure=getConfigurationTable(ppath+"/info/PythonConfigure.json")
		pluacompile_key=pm_configure['luacompile_key']
		pluacompile_value=pm_configure['luacompile_value']
		value={
			"name":pname,
			"path":ppath,
			"luacompile_key":pluacompile_key,
			"luacompile_value":pluacompile_value,
		}
		vProjectlist=getPlatformList(vCa.platform,vConfig)
		print('\tcopy project platform:'+str(vCa.platform)+' count:'+str(len(vProjectlist))+' subgamePath:'+str(vCa.subgamePath))
		for kv in vProjectlist:
			vItem=vProjectlist[kv]
			path=str(vItem["path"])
			name=str(vItem["name"])
			m_configure=getConfigurationTable(path+"/info/PythonConfigure.json")
			luacompile_key=m_configure['luacompile_key']
			luacompile_value=m_configure['luacompile_value']
			for vv in vArraySubgame:
				print('\t\tproject:'+str(kv)+' subgamePath:'+str(vv))
				compileTheSpecifiedDirectory(value,vv,luacompile_key,luacompile_value,name,targetPath)
	elif vCa.platform: #打包平台-子游戏
		vProjectlist=getPlatformList(vCa.platform,vConfig)
		print('\tplatform:'+str(vCa.platform)+' count:'+str(len(vProjectlist))+' subgamePath:'+str(vCa.subgamePath))
		for kv in vProjectlist:
			vItem=vProjectlist[kv]
			ppath=str(vItem["path"])
			pname=str(vItem["name"])
			m_configure=getConfigurationTable(ppath+"/info/PythonConfigure.json")
			pluacompile_key=m_configure['luacompile_key']
			pluacompile_value=m_configure['luacompile_value']
			value={
				"name":pname,
				"path":ppath,
				"luacompile_key":pluacompile_key,
				"luacompile_value":pluacompile_value,
			}
			for vv in vArraySubgame:
				print('\t\tproject:'+str(kv)+' subgamePath:'+str(vv))
				compileTheSpecifiedDirectory(value,vv,pluacompile_key,pluacompile_value,pname,targetPath)

# Compile the specified Lobby
def compileTheSpecifiedLobby(project,outPath):
	print('Compile the specified Lobby')
	# print(json.dumps(project))
	path=str(project["path"])
	projectName=str(project["name"])

	m_configure=getConfigurationTable(path+"/info/PythonConfigure.json")
	luacompile_key=m_configure['luacompile_key']
	luacompile_value=m_configure['luacompile_value']
	
	vTempPath=str(outPath+'/'+projectName).replace("/", "\\")
	print('\tproject name:'+str(projectName)+' lua key:'+str(luacompile_key)+' lua value:'+str(luacompile_value)+' outPath:'+vTempPath)

	print('\tluacompile lua lobby')
	command_client='cocos luacompile -s '+path+'/client/client'+' -d '+vTempPath+'/client'+' -e -k '+luacompile_key+' -b '+luacompile_value+' --disable-compile'
	echo_client=executeExternalCommands(command_client)
	print(echo_client)

	command_base='cocos luacompile -s '+path+'/client/base'+' -d '+vTempPath+'/base'+' -e -k '+luacompile_key+' -b '+luacompile_value+' --disable-compile'
	echo_base=executeExternalCommands(command_base)
	print(echo_base)

	command_command='cocos luacompile -s '+path+'/client/command'+' -d '+vTempPath+'/command'+' -e -k '+luacompile_key+' -b '+luacompile_value+' --disable-compile'
	echo_command=executeExternalCommands(command_command)
	print(echo_command)
	
	ccddwwee=executeExternalScript('command.bat copyDirectoryBaseClient '+str(path).replace("/", "\\")+' '+str(vTempPath+'').replace("/", "\\"))
	print(ccddwwee)

	outClientPaht=vTempPath+'/client'
	echo_client_md5=executeExternalScript('command.bat createMd5File '+outClientPaht.replace("/", "\\"))
	print(echo_client_md5)

	mcl_a=vTempPath+'/base/res/client.zip'
	mcl_b=vTempPath+'/client'
	echo_cf=executeExternalScript('command.bat compressedFile '+mcl_a.replace("/", "\\")+' '+mcl_b.replace("/", "\\"))
	print(echo_cf)

	outBasePaht=vTempPath+'/base'
	echo_base_md5=executeExternalScript('command.bat createMd5File '+outBasePaht.replace("/", "\\"))
	print(echo_base_md5)

	zname=outPath+'/'+projectName+'.zip'
	# zname=vTempPath+'/'+projectName+'.zip'
	ysnr=vTempPath+'/base'+' '+vTempPath+'/client'+' '+vTempPath+'/command'
	echo_bcc=executeExternalScript('command.bat compressedFileArgs4 '+zname.replace("/", "\\")+' '+ysnr.replace("/", "\\"))
	print(echo_bcc)

# package lobby
def packageLobby(vCa,vConfig):
	cdir=os.getcwd()
	vProjectlist=getPlatformList(vCa.platform,vConfig)
	print('\tplatform:'+str(vCa.platform)+' count:'+str(len(vProjectlist)))
	targetPath=vCa.targetPath
	for kv in vProjectlist:
		vItem=vProjectlist[kv]
		path=str(vItem["path"])
		os.chdir(path)
		echo_svn_lobby_update=executeExternalCommands('svn update')
		print('\techo_svn_lobby_update:',echo_svn_lobby_update)
		os.chdir(cdir)
		compileTheSpecifiedLobby(vItem,targetPath)

# svn 命令解析
def svnCommandParse(vCa,vConfig):
	print('Svn Command Parse-----------------------------')
	vSvnCommand=str(vCa.svnCommand)
	# vSvnCommand='svn add *|svn commit -m "client"'
	# vSvnCommand='svn log'
	def runSvnCommand(vc):
		split=getParameterContentList(vc)
		for vk in split:
			echo_svn=executeExternalCommands(vk)
			print('echo_svn:',echo_svn)

	print("svn command parsing:"+vSvnCommand)
	cdir=os.getcwd()
	print('\tcurrent directory a:'+cdir)

	vProjectlist=getPlatformList(vCa.platform,vConfig)
	for kv in vProjectlist:
		name=vProjectlist[kv]
		path=str(name["path"])
		os.chdir(path)
		print('\tcurrent directory b:'+os.getcwd())
		runSvnCommand(vSvnCommand)

	os.chdir(cdir)
	print('\tcurrent directory c:'+os.getcwd())

# 同步内容
def syncContent(vCa,vConfig):
	print('Sync content-----------------------------')
	cdir=os.getcwd()
	if vCa.platform:
		syncContent=getParameterContentList(vCa.syncContent)
		print('\tsyncContent:'+json.dumps(syncContent)+' len:'+str(len(syncContent)))
		if len(syncContent)<=0:
			print('\tno copy command')
			return

		allProjectList=vConfig['allProjectList']
		isProject=allProjectList.has_key(vCa.copyProject)
		if not isProject:
			print("\tSync content-Copy the project path nil "+vCa.copyProject)
			return
		copyProject=allProjectList[vCa.copyProject]
		copyProjectPath=copyProject['path']
		print('\tcopy project path:'+copyProjectPath)

		vProjectlist=getPlatformList(vCa.platform,vConfig)
		print('\tplatform:'+str(vCa.platform)+' count:'+str(len(vProjectlist)))
		for kv in vProjectlist:
			name=vProjectlist[kv]
			path=str(name["path"])
			if path != copyProjectPath:
				os.chdir(path)
				print('\tplatform path:'+path)
				print('\tcurrent directory:'+os.getcwd())
				echo_svn_update=executeExternalCommands('svn update')
				print('\techo_svn_update:',echo_svn_update)
				os.chdir(cdir)
				svnInfo={"open":False,'info':'','listType':[]}
				for ikey in syncContent:
					print('\t\tiko:'+ikey['0']+' ik1:'+ikey['1'])
					sPath=path+"/"+ikey['0']
					if not isPathExists(copyProjectPath+"/"+ikey['0']):
						print('\tno copy directory'+str(copyProjectPath+"/"+ikey['0']))
						return
					iFileType=isFileDir(copyProjectPath+"/"+ikey['0'])
					print('\t\tset content:'+sPath+' [0file,1dir]:'+str(isFileDir(sPath)))
					deleteFileDir(sPath)
					print('\t\tcopyProjectPath:'+copyProjectPath+"/"+ikey['0']+' '+path+"/"+ikey['1'])
					copyFileDir(copyProjectPath+"/"+ikey['0'],path+"/"+ikey['1'])
					if iFileType==0:
						os.chdir(path)
						echo_svn_add_file=executeExternalCommands('svn add '+ikey['0'])
						print('\techo_svn_add_file:',echo_svn_add_file)
						svnInfo["open"]=True
						svnInfo["info"]="add "+str(ikey['0'])+" "+svnInfo["info"]
						svnInfo["listType"].append('file')
						os.chdir(cdir)
					elif iFileType==1:
						os.chdir(path)
						echo_svn_add_dir=executeExternalCommands('svn add '+ikey['1']+' --parents')
						print('\techo_svn_add_dir:',echo_svn_add_dir)
						svnInfo["open"]=ikey['0']
						svnInfo["info"]="add "+str(ikey['0'])+" "+svnInfo["info"]
						svnInfo["listType"].append('dir')
						os.chdir(cdir)
				
					if svnInfo["open"]:
						os.chdir(path)
						message="command run "+str(svnInfo["info"])
						vcs='svn commit -m "'+message+'"'
						if (len(svnInfo["listType"])>1):
							vcs='svn commit -m "'+message+'" *'
						echo_svn_commit=executeExternalCommands(vcs)
						print('\techo_svn_commit value:'+str(vcs)+' commit:'+str(echo_svn_commit))
						os.chdir(cdir)
						svnInfo["open"]=False
						svnInfo["info"]=""

	os.chdir(cdir)

# 签名Eclipse包
def apkSignName(vCa,vConfig):
	print('apk signature-----------------------------')
	channelList=[]
	apkPath=str(vCa.signApkName).replace('\\','/')
	apkName=os.path.splitext(os.path.split(apkPath)[-1])[0]
	apkNamExtension=os.path.splitext(apkPath)[-1]
	print('\tapkName:'+apkName + ' '+apkNamExtension+' path:'+apkPath)

	if vCa.channel:
		channelList=str(vCa.channel).split('_')

	vKeyName=vCa.keystoreName
	splitext=os.path.splitext(vKeyName)[-1]
	vAlias=vCa.keystoreAlias
	vStorePassword=vCa.keystorePassword
	vStoreAliasPassword=vCa.keystoreAliasPassword

	print('\tchannel list:',json.dumps(channelList))
	for kv in channelList:
		outApkName=apkName+'-channel-'+kv+'-'+apkNamExtension
		executeExternalScript('command.bat signApkEclipse '+kv+' '+apkPath.replace("/", "\\")+' '+outApkName+' '+vKeyName+' '+vAlias+' '+vStorePassword+' '+vStoreAliasPassword +' '+m_outPath)

#获取文件md5
def fileMd5(filePath):
	if not os.path.isfile(filePath):
		return False
	with open(filePath,'rb') as f:
		md5obj = hashlib.md5(f.read())
		# md5obj.update(f.read())
		hash = md5obj.hexdigest()
		# print(filePath+" md5:"+hash)
		return hash

#获取文件路径信息[key文件名字,文件路径,修改后名字]
def getFileNameInfo(value,replacePath):
	tmd5=fileMd5(value)
	tempPath=str(value).split('/')[-1]
	tPath=str(tempPath).replace('\\','/')
	tName=os.path.splitext(os.path.split(tPath)[-1])[0]
	tNamExtension=os.path.splitext(tPath)[-1]
	tPath=tPath.replace(str(tName)+''+str(tNamExtension),'')

	tPath=tPath.replace(str(replacePath),'')
	# print('\tapkName:'+tName + ' '+tNamExtension+' path:'+tPath)
	return {'name':str(tName)+''+str(tNamExtension),'extension':tNamExtension,'path':tPath,'md5':tmd5}

#遍历目录md5(路径fileName,保存的md5值列表形式addMd5)
def fileDirMd5(fileName,addMd5,replacePath):
	if os.path.isdir(fileName):
		fileList=os.listdir(fileName)
		# print('fileList:',json.dumps(fileList))
		for value in fileList:
			# print('\tvalue:'+value)
			fileDir=os.path.dirname(os.path.join(fileName,value))
			path=os.path.join(fileDir,value)
			if os.path.isfile(path):
					vTemp=getFileNameInfo(path,replacePath)
					addMd5.append({"path":vTemp['path'],"name":vTemp['name'],"md5":vTemp['md5']})
			else:
					tempDir=os.path.join(fileDir,value)
					fileDirMd5(tempDir,addMd5,replacePath)
	else:
		fileDir=os.path.dirname(fileName)
		path=os.path.join(fileDir,fileName)
		vTemp=getFileNameInfo(path,replacePath)
		addMd5.append({"path":vTemp['path'],"name":vTemp['name'],"md5":vTemp['md5']})

def createMd5File(tPath):
	print('createMd5File Md5-----------------------------')
	dirPath=os.path.abspath(str(tPath).replace('\\','/'))
	# print('dirMd5:'+dirPath)
	jsArray=str(dirPath).split('\\')
	# print('json0:',json.dumps(jsArray))
	jsArray.pop(len(jsArray)-1)
	# print('json1:',json.dumps(jsArray))
	tcopy='/'.join(jsArray)+'/'
	# print('tcopy:'+tcopy)

	cdir=os.getcwd()
	os.chdir(dirPath)
	manifest= []
	fileDirMd5(dirPath,manifest,tcopy)
	os.chdir(cdir)
	manifest.append({"allcount": len(manifest)})
	filemd5List={}
	filemd5List['listdata']=manifest
	# print(json.dumps(filemd5List))
	makefileUtf8Normal(str(dirPath+'/res/filemd5List.json').replace('\\','/'),json.dumps(filemd5List))

def dirMd5(vCa,vConfig):
	print('dirMd5 Md5-----------------------------')
	createMd5File(vCa.dirMd5)

# Create game_list.txt file
def makefileGamelist(args,vfileName):
	inPath=vfileName #'settings.gradle'
	print('Create '+str(inPath)+' file')

	# if os.path.exists(inPath):
	#	 print('\tThe file will not be created if it exists '+inPath)
	#	 return

	outStr='[name:Chinese name of the game,des:md5 path(Used to generate md5 version files),ori:source path(for copying),zipped:whether to add to the compressed list,folder:content(Used to compress the specified game),primode:Is there a private room]'
	value='''name={gameInfo},des={cPath},ori={path},folder={folder},zipped={zipped},primode={primode}'''

	v=args[0]
	name=v['name'].decode('utf-8').encode('utf-8')
	print('name:'+name)

	# for v in args:
	#	 print(v)
	#	 temp=value.format(gameInfo=str(v['name']).decode('ascii'),cPath=str(v['des']).replace('/','\\'),path=str(v['ori']).replace('/','\\'),folder=v['folder'],zipped=int(v['zipped']),primode=int(v['primode']))
	#	 print(temp)
	# makefileNormal(inPath,outStr)

def makefileProjectConfiguration(vCa,vConfig):
	print('create project configuration-----------------------------')

def createObfuscatedFile(args):
	fileName=str(args.fileName)
	print('Create Obfuscated File-----------------------------fileName:'+fileName)
	charsList=getParameterContentList(args.chars)
	print("\tchars:",str(charsList))

	nobCount=int(args.numberOfObfuscations) or 12000
	print("\tobfuscated entry:"+str(nobCount))

	keyValue={}
	vType=1

	if vType==1:
		keyValue={}
		vlen=random.randint(8,10)
		# print("\tleng:"+str(vlen))
		def getString(vCount,vList):
			vstr=""
			charsLen=len(vList)
			for ii in range(vCount):
				vstr=vstr+str(vList[random.randint(0,charsLen-1)])
			return vstr

		for i in range(nobCount):
			rsun = random.randint(1,vlen)
			vstr=getString(rsun,charsList)
			if not keyValue.get(''+vstr):
				keyValue[vstr]=vstr
			else:
				vstr=getString(rsun,charsList)
				if not keyValue.get(''+vstr):
					keyValue[vstr]=vstr
	elif vType==2:
		keyValue=[]
		cLeng=len(charsList)
		count=nobCount or cLeng*cLeng
		isOpen=True
		index=0
		while isOpen:
			for i in range(count):
				lx=math.floor(i/cLeng)
				ly=i%cLeng
				vstr=charsList[ly]
				# print('lx:'+str(lx)+' ly:'+str(ly)+' vstr:'+str(vstr))
				if lx>0 :
					vstr=charsList[int(lx-1)]+vstr
				keyValue.append(vstr)
				index=index+1
			if index>2000:
				isOpen=False

	content=""
	for k in keyValue:
		content=content+k+"\n"
	
	makefileNormal(str(m_outPath+"/"+fileName).replace('\\','/'),content)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Project batch tool")
	parser.add_argument("-platform", "--platform", help="Platform project(平台项目)", default='')

	parser.add_argument("-projectName", "--projectName", help="project name(项目名字)", default=False)
	parser.add_argument("-subgamePath", "--subgamePath", help="subgame path(子游戏路径)", default=False)
	parser.add_argument("-packageLobby", "--packageLobby", help="package lobby(打包大厅)", default=False)

	#文件同步
	parser.add_argument("-syncContent", "--syncContent", help="Sync content(同步内容,分隔符'|;')", default=False)

	# keystore|jks
	parser.add_argument("-keystoreName", "--keystoreName", help="create keystoreName(创建后缀 .keystore|jks文件)", default=False)
	parser.add_argument("-keystoreAlias", "--keystoreAlias", help="create keystoreAlias", default=False)
	parser.add_argument("-keystorePassword", "--keystorePassword", help="create keystorePassword", default=False)
	parser.add_argument("-keystoreAliasPassword", "--keystoreAliasPassword", help="create keystoreAliasPassword", default=False)
	parser.add_argument("-keyRandomNumber", "--keyRandomNumber", help="random key", default=0)

	# svn
	parser.add_argument("-svnCommand", "--svnCommand", help="Execute the svm command(执行svm命令,分隔符'|;')", default=False)
	parser.add_argument("-svnMessage", "--svnMessage", help="svn submit Instructions(提交说明,分隔符'|;')", default=False)

	# 签名apk
	parser.add_argument("-signApkName", "--signApkName", help="signed apk name", default=False)
	parser.add_argument("-channel", "--channel", help="channel number", default=False)

	parser.add_argument("-copyProject", "--copyProject", help="copy Path", default=False)
	parser.add_argument("-copyPath", "--copyPath", help="copy Path", default=False)
	parser.add_argument("-targetPath", "--targetPath", help="Target path(目标/输出路径)", default=False)

	# md5
	parser.add_argument("-dirMd5", "--dirMd5", help="dir Md5", default=False)

	parser.add_argument("-cProjectConfig", "--cProjectConfig", help="create project configuration", default=False)

	# proguard
	parser.add_argument("-proguard", "--proguard", help="混淆开关", default=False)
	parser.add_argument("-fileName", "--fileName", help="文件名字", default=False)
	parser.add_argument("-chars", "--chars", help="混淆字符以分隔|;", default=False)
	parser.add_argument("-numberOfObfuscations", "--numberOfObfuscations", help="混淆数量", default=0)

	args = parser.parse_args()
	if args.targetPath:
		m_outPath=args.targetPath

	m_configure=getProjectPathIntegration('config.json')
	if args.subgamePath: # 打包子游戏
		packageSubGame(args,m_configure)
	elif args.packageLobby:#打包大厅
		packageLobby(args,m_configure)
	elif args.signApkName:
		apkSignName(args,m_configure)
	elif args.keystoreName: # keystore|jks
		createKeystoreJks(args.keystoreName,args.keystoreAlias,args.keystorePassword,args.keystoreAliasPassword,args.keyRandomNumber,args.targetPath)
	elif args.svnCommand:
		svnCommandParse(args,m_configure)
	elif args.syncContent:
		syncContent(args,m_configure)
	elif args.dirMd5:
		dirMd5(args,m_configure)
	elif args.cProjectConfig:
		makefileProjectConfiguration(args,m_configure)
	elif args.proguard:
		createObfuscatedFile(args)
	

