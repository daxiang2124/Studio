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
import argparse
from os import path

#random name
m_capital=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
m_lowerCase=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
m_number=['0','1','2','3','4','5','6','7','8','9']
m_cln=[]
for i in range(len(m_capital)):
   m_cln.append(m_capital[i])
for i in range(len(m_lowerCase)):
   m_cln.append(m_lowerCase[i])
for i in range(len(m_number)):
   m_cln.append(m_number[i])


folder=''+time.strftime('%Y-%m-%d-%H%M%S',time.localtime(time.time()))
m_outputPath='../client_publish'
m_originalResourcePath='../client'
m_buildPath='../client/ciphercode'
m_outputChannelPath='../client_channel'
m_frameworksPath='../frameworks'

# Get parameter information
def getParameters(args):
   value={}
   index=0
   for v in args:
      value['args'+str(index)]=str(v)
      index=index+1
   return value

def getConfigurationTable(jsonFile):
   value={}
   f = open(''+jsonFile)
   data = json.load(f)
   for k, v in data.items():
      value[k]=v
      # print(k+':'+v)
   return value

# Get cut content "_~,_~,"
def getCutContent(value):
   vArray=[]
   vTable=str(value).split(',')
   for v in vTable:
      vvM=str(v).split('_')
      if len(vvM)==1:
         vvT=str(v).split('~')
         if len(vvT)==2:
            index=int(vvT[0])
            count=int(vvT[1])
            while(index<=count):
               vArray.append(str(index))
               index=index+1
         else:
            vArray.append(str(vvM[0]))
      else:
         for v1 in vvM:
            vArray.append(str(v1))
   return vArray

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
   
# Create a normal file
def makefileNormal(fileName,content):
   # print('Create '+fileName+' file')
   fo = open(fileName, "w+")
   fo.write(content)
   fo.close()
   print('Create file successfully '+fileName)

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

# Filter copied files
def filterCopiedFiles(path,content):
   to_ignore=[]
   for file_ in content:
      if file_ in ('.lua','.luac','/src/'):
         to_ignore.append(file_)
   return to_ignore

def svnCommand(command):
   command_str=''
   if command =='update':
      command_str='svn update'

   print('\t\tsvn command:'+command_str)
   if len(command_str)>1:
      echo_str=executeExternalCommands(command_str)
      print(echo_str)

def setVersion(big,samll):
   print('Modify version number big:'+str(big)+' samll:'+str(samll))
   filePath = m_originalResourcePath+'/base/src/app/models/AppDF.lua' #os.path.join(m_originalResourcePath, '/base/src/app/models/AppDF.lua')
   print('\tfilePath:'+filePath)
   f = open(filePath,'r+')
   all_lines = f.readlines()
   f.seek(0)
   f.truncate()

   origin_big_line = 'appdf.BASE_C_VERSION'
   update_big_line = 'appdf.BASE_C_VERSION = ' + str(big) + '--'
   origin_small_line = 'appdf.BASE_C_RESVERSION'
   update_small_line = 'appdf.BASE_C_RESVERSION  = ' + str(samll) + '--'

   localTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
   print('\t\tlocalTime:'+localTime)

   archive_time_line = 'appdf.ArchiveTime'
   update_archive_line = 'appdf.ArchiveTime = \"' + localTime +'\"'+ '--'
   for line in all_lines:
      line = line.replace(origin_big_line, update_big_line)
      line = line.replace(origin_small_line, update_small_line)
      line = line.replace(archive_time_line, update_archive_line)
      f.write(line)
   f.close()

def setChannel(value):
   print('Modify channel number:'+str(value))
   if value == None or str(value) == "0":
      print("\tno channel number")
   else:
      filePath = m_originalResourcePath+'/base/config.json' 
      fileObject = open(filePath,'r+')
      vDataJson = json.load(fileObject)
      # print("\tr config:"+json.dumps(vDataJson))
      fileObject.close()

      if vDataJson["init_cfg"].has_key("channelID"):
         del vDataJson["init_cfg"]["channelID"]

      vDataJson["init_cfg"]["channelID"] = int(value)
      xw = json.dumps(vDataJson)
      makefileNormal(filePath,xw)

def makefileOldInfoAppNameConfigurationFile(vConfig):
   releaseValue=vConfig['release']
   # value={
   #    "bundleid":releaseValue['bundleid'],#Package names
   #    "name": releaseValue['libName'],#name
   #    "jenkinsJobName": releaseValue['libName'],#jenkins name
   #    "keystorePath":  releaseValue['keystorePath'],#key name path(xx.jks)
   #    "keystoreAlias":  releaseValue['keystoreAlias'],
   #    "keystorePassword":  releaseValue['keystorePassword'],
   #    "keystoreAliasPassword": releaseValue['keystoreAliasPassword']
   # }
   # makefileNormal("info.txt",json.dumps(value))

   vPackageNames=releaseValue['bundleid']
   vName=releaseValue['libName']
   vJenkinsJobName=releaseValue['libName']
   vKeystorePath=releaseValue['keystorePath']
   vKeyAlias=releaseValue['keystoreAlias']
   vKeyPassword=releaseValue['keystorePassword']
   vKeyAliasPassword=releaseValue['keystoreAliasPassword']

   value='''"bundleid": "{packageNames}","name": "{name}","jenkinsJobName": "{jenkinsJobName}","keystorePath": "{keystorePath}","keystoreAlias": "{keyAlias}","keystorePassword": "{keyPassword}","keystoreAliasPassword": "{keyAliasPassword}"'''
   outStr = value.format(packageNames=str(vPackageNames),name=str(vName),jenkinsJobName=str(vJenkinsJobName),keystorePath=str(vKeystorePath),keyAlias=str(vKeyAlias),keyPassword=str(vKeyPassword),keyAliasPassword=str(vKeyAliasPassword))
   makefileNormal("info.txt",'{'+outStr+"}")

   makefileNormal("appName.txt",releaseValue['libName'])

   # game_list.txt
   # if os.path.exists("game_list.json"):
   #    print('\tThe file will not be created if it exists game_list.json')
   #    return
   
   # games file dir 
   tPathJson=['game/yule/','game/qipai/']
   c_json=[]
   list_txt='name={info},des={compilePath},ori={projectPath},folder={folderPath},zipped={zipPed},primode={priMode}'
   c_text='[name:Game Name, des:Compile Path, ori:Project Path,folder:Game Path,zipped:Zip Type, primode:Is Private Room]'
   for v in tPathJson:
      vDirPath='../client/'+str(v)
      # print('v:'+str(vDirPath))
      if not os.path.isdir(vDirPath):
         # print('not:'+str(vDirPath))
         continue

      list_dir = os.listdir(vDirPath)
      # print(json.dumps(list_dir))
      for vv in list_dir:
         t_t=list_txt.format(info=str(vv),compilePath=str('client/ciphercode/'+str(v)+str(vv)).replace('/','\\'),projectPath=str(str(v)+str(vv)).replace('/','\\'),folderPath=str(vv),zipPed=str(0),priMode=str(0))
         c_text=c_text+"\n"+t_t
         list_json={
            "name":str(vv),
            "des":str('client/ciphercode/'+str(v)+str(vv)),
            "ori":str(str(v)+str(vv)),
            "folder":str(vv),
            "zipped":str(0),
            "primode":str(0)
         }
         c_json.append(list_json)

   makefileNormal("game_list.txt",c_text)
   makefileNormal("game_list.json",'{"game_list":'+json.dumps(c_json)+'}')

# old project configuration file(Project.bat)
def makefileOldProjectConfigurationFile(vConfig):
   vpname='Project.bat'
   print('old project configuration file(Project.bat)')
   # if os.path.exists(pname):
   #    print('\tThe file will not be created if it exists '+pname)
   #    return

   vProjectValue=vConfig['ProjectValue']
   vluacompile_key=vConfig['luacompile_key']
   vluacompile_value=vConfig['luacompile_value']
   vpaythonPath=vConfig['paythonPath']

   vfolderDataName="%date:~0,4%%date:~5,2%%date:~8,2%%h%%time:~3,2%"
   vfolderName="%date:~0,4%-%date:~5,2%-%date:~8,2%-%h%%time:~3,2%-%time:~6,2%%time:~9,2%"

   value='''@echo off\n\nset ProjectValue={ProjectValue}\nset luacompile_key={luacompile_key}\nset luacompile_value={luacompile_value}\n\nset paythonPath={paythonPath}\n\nset h=%time:~0,2%\nset h=%h: =0%\nset folderDataName={folderDataName}\nset folderName={folderName}\n'''
   outStr = value.format(ProjectValue=str(vProjectValue),luacompile_key=str(vluacompile_key),luacompile_value=str(vluacompile_value),paythonPath=str(vpaythonPath.replace("/", "\\")),folderDataName=str(vfolderDataName),folderName=str(vfolderName))
   makefileNormal(vpname,outStr)

   makefileOldInfoAppNameConfigurationFile(vConfig)

   
# Create settings.gradle file
def makefileSetTingsGradle(vLibname,v2dxLibPath):
   inPath='settings.gradle'
   print('Create settings.gradle file')

   # if os.path.exists(inPath):
   #    print('\tThe file will not be created if it exists '+inPath)
   #    return

   value='''include '::libcocos2dx',':{libname}'\nproject(':libcocos2dx').projectDir = new File({pathPath})\nproject(':{libname}').projectDir = new File(settingsDir, 'app')'''
   outStr = value.format(libname=str(vLibname),pathPath=str(v2dxLibPath))
   makefileNormal(inPath,outStr)
   return outStr

# Create gradle.properties file
def makefileGradleProperties(args):
   gradleFileName="gradle.properties"
   print('Create gradle.properties file')
   # if os.path.exists(gradleFileName):
   #    print('\tThe file will not be created if it exists gradle.properties')
   #    return

   value='''# Project-wide Gradle settings.\n\n# IDE (e.g. Android Studio) users:\n# Gradle settings configured through the IDE *will override*\n# any settings specified in this file.\n\n# For more details on how to configure your build environment visit\n# http://www.gradle.org/docs/current/userguide/build_environment.html\n\n# Specifies the JVM arguments used for the daemon process.\n# The setting is particularly useful for tweaking memory settings.\n# Default value: -Xmx10248m -XX:MaxPermSize=256m\n# org.gradle.jvmargs=-Xmx2048m -XX:MaxPermSize=512m -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8\n\n# When configured, Gradle will run in incubating parallel mode.\n# This option should only be used with decoupled projects. More details, visit\n# http://www.gradle.org/docs/current/userguide/multi_project_builds.html#sec:decoupled_projects\n# org.gradle.parallel=true\n
android.useAndroidX=true
android.enableJetifier=true
android.injected.testOnly=false

# Android SDK version that will be used as the compile project
PROP_COMPILE_SDK_VERSION=30

# Android SDK version that will be used as the earliest version of android this application can run on
PROP_MIN_SDK_VERSION=21


# Android SDK version that will be used as the latest version of android this application has been tested on
PROP_TARGET_SDK_VERSION=30

# Android Build Tools version that will be used as the compile project
PROP_BUILD_TOOLS_VERSION=30.0.2

PROP_NDK_PATH={ndkPath}


# Application ID
APPLICATION_ID={bundleid}

# List of CPU Archtexture to build that application with
# Available architextures (armeabi-v7a | arm64-v8a | x86)
# To build for multiple architexture, use the `:` between them
# Example - PROP_APP_ABI=armeabi-v7a:arm64-v8a
PROP_APP_ABI={appAbi}

# fill in sign information for release mode
RELEASE_STORE_FILE={keystorePath}
RELEASE_STORE_PASSWORD={keystorePassword}
RELEASE_KEY_ALIAS={keystoreAlias}
RELEASE_KEY_PASSWORD={keystoreAliasPassword}
'''
   
   vbundleid=args['bundleid']
   vkeyName=args['keystorePath']
   vkeystoreAlias=args['keystoreAlias']
   vkeystorePassword=args['keystorePassword']
   vkeystoreAliasPassword=args['keystoreAliasPassword']
   vndkPath=args['ndkPath']
   vappAbi=args['appAbi']
   outStr= value.format(ndkPath=vndkPath,bundleid=vbundleid,appAbi=vappAbi,keystorePath=vkeyName,keystorePassword=vkeystorePassword,keystoreAlias=vkeystoreAlias,keystoreAliasPassword=vkeystoreAliasPassword)
   makefileNormal(gradleFileName,outStr)
   return outStr

# Create key.jks|keystore file
def makefileJksKeystore(args):
   print('Create key.jks|keystore file')
   vOutPath='./key'
   vKeyName=args['keystorePath']
   vAlias=args['keystoreAlias']
   storePassword=args['keystorePassword']
   storeAliasPassword=args['keystoreAliasPassword']

   if True:
      if not os.path.exists(vOutPath):
         os.makedirs(vOutPath)

      if os.path.exists(vOutPath+'/'+vKeyName):
         print('\tThe key file will not be generated if it exists '+vKeyName)
         return

      dname='''cn={cn},ou={ou},o={o},l={l},st={st},c={c}'''
      jksCommands='''keytool -genkey -v -keystore {keyName} -alias {alias} -storepass {storepass} -keypass {keypass} -keyalg RSA -keysize 2048 -validity 36500 -dname {dname}'''
      keystoreCommands='''keytool -genkey -v -keystore {keyName} -alias {alias} -storepass {storepass} -keypass {keypass} -keyalg RSA -validity 20000 -dname {dname}'''

      splitext=os.path.splitext(vKeyName)[-1]

      key_dname_cn=''+getRandString(2,1)
      key_dname_ou=''+getRandString(2,1)
      key_dname_o=''+getRandString(2,1)
      key_dname_l=''+getRandString(2,1)
      key_dname_st=''+getRandString(2,1)
      key_dname_c=''+getRandString(2,1)
      outDname = dname.format(cn=str(key_dname_cn),ou=str(key_dname_ou),o=str(key_dname_o),l=str(key_dname_l),st=str(key_dname_st),c=str(key_dname_c))

      content=''+str(vKeyName)+'\n\tkeystoreAlias='+str(vAlias)+'\n\tkeystorePassword='+str(storePassword)+'\n\tkeystoreAliasPassword='+str(storeAliasPassword)+'\n\tdname="'+str(outDname+'"')
      print('content:'+content)


      outC=''
      if str(splitext) == '.jks':
         outC=jksCommands.format(keyName=str(vOutPath+'/'+vKeyName),alias=str(vAlias),storepass=str(storePassword),keypass=str(storeAliasPassword),dname=str(outDname))
      elif str(splitext) == '.keystore':
         outC=keystoreCommands.format(keyName=str(vOutPath+'/'+vKeyName),alias=str(vAlias),storepass=str(storePassword),keypass=str(storeAliasPassword),dname=str(outDname))

      if(len(outC)>0):
         makefileNormal(str(vOutPath+'/'+vKeyName+'.txt'),content)
         executeExternalCommands(outC)
      else:
         print('Failed to create file '+str(vKeyName)+' Command parameters:'+outC)

   else:
      outC=' '+str(vKeyName)+' '+str(vAlias)+' '+str(storePassword)+' '+str(storeAliasPassword)
      echo_cf=executeExternalScript('PythonCommand.bat makefileJksKeystore '+vOutPath.replace("/", "\\")+outC)
      print(echo_cf)

# Compile the specified directory
def compileTheSpecifiedDirectory(proPath,singleGame,lck,lcv,outPath):
   print('Compile the specified directory')
   pathName=proPath+'/'+singleGame
   zzde=singleGame.split('/')
   gameName=zzde[len(zzde)-1]
   outPaht=outPath+'/'+gameName
   # print('\tproject path:'+proPath)
   # print('\tsingle Game path:'+singleGame)
   # print('\toutput path:'+outPaht)
   # print('\t\t\tluacompile lua single game:'+pathName)
   # print('\t\t\toutPaht:'+outPaht+' '+json.dumps(zzde)+' gameName:'+gameName)
   command_single='cocos luacompile -s '+pathName+' -d '+outPaht+' -e -k '+lck+' -b '+lcv+' --disable-compile'
   echo_single=executeExternalCommands(command_single)
   print(echo_single)

   echo_copyDf=executeExternalScript('PythonCommand.bat copyDirectorySpecifiedDirectory '+pathName.replace("/", "\\")+' '+outPaht.replace("/", "\\"))
   print(echo_copyDf)

   echo_md5=executeExternalScript('PythonCommand.bat createMd5File '+outPaht.replace("/", "\\"))
   print(echo_md5)

   outName=outPaht.replace("/", "\\")
   echo_cf=executeExternalScript('PythonCommand.bat compressedFile '+outName+'.zip'+' '+outName)
   print(echo_cf)

# Packaging resources
def packagingResources(vType,lck,lcv,singleGame):
   if vType=='0' or vType=='1':
      print('\t\t\tluacompile lua lobby')
      command_client='cocos luacompile -s '+m_originalResourcePath+'/client'+' -d '+m_buildPath+'/client'+' -e -k '+lck+' -b '+lcv+' --disable-compile'
      echo_client=executeExternalCommands(command_client)
      print(echo_client)

      command_base='cocos luacompile -s '+m_originalResourcePath+'/base'+' -d '+m_buildPath+'/base'+' -e -k '+lck+' -b '+lcv+' --disable-compile'
      echo_base=executeExternalCommands(command_base)
      print(echo_base)

      command_command='cocos luacompile -s '+m_originalResourcePath+'/command'+' -d '+m_buildPath+'/command'+' -e -k '+lck+' -b '+lcv+' --disable-compile'
      echo_command=executeExternalCommands(command_command)
      print(echo_command)
      
      ccddwwee=executeExternalScript('PythonCommand.bat copyDirectoryBaseClient')
      print(ccddwwee)

      outBasePaht=m_buildPath+'/base'
      echo_base_md5=executeExternalScript('PythonCommand.bat createMd5File '+outBasePaht.replace("/", "\\"))
      print(echo_base_md5)

      outClientPaht=m_buildPath+'/client'
      echo_client_md5=executeExternalScript('PythonCommand.bat createMd5File '+outClientPaht.replace("/", "\\"))
      print(echo_client_md5)

      mcl_a=m_buildPath+'/base/res/client.zip'
      mcl_b=m_buildPath+'/client'
      echo_cf=executeExternalScript('PythonCommand.bat compressedFile '+mcl_a.replace("/", "\\")+' '+mcl_b.replace("/", "\\"))
      print(echo_cf)

   if vType=='1' or vType=='2':
      print('\t\t\tluacompile lua game all')
      command_game='cocos luacompile -s '+m_originalResourcePath+'/game'+' -d '+m_buildPath+'/game'+' -e -k '+lck+' -b '+lcv+' --disable-compile'
      echo_game=executeExternalCommands(command_game)
      print(echo_game)

      ccddwwee=executeExternalScript('PythonCommand.bat copyDirectoryGame')
      print(ccddwwee)

   if vType=='3':
      compileTheSpecifiedDirectory(m_originalResourcePath,singleGame,lck,lcv,m_outputPath+'/'+folder)

def commandResource(args,configureArsg):
   iType=str(args['itype'])
   print('\tpackaging resources[0 lobby,1 lobby or game,2 game all,3 single game]:'+iType)
   
   luacompile_key=configureArsg['luacompile_key']
   luacompile_value=configureArsg['luacompile_value']

   ccddwwee=executeExternalScript('PythonCommand.bat cleanDirectory '+m_buildPath.replace("/", "\\"))
   print(ccddwwee)

   if os.path.exists("game_list.json"):
      configureArsg['game_list']=[]
      vList=getConfigurationTable("game_list.json")
      configureArsg['game_list']=vList['game_list']

   if iType=='0' or iType=='1' or iType=='2' or iType=='3':
      gameNamePath=''
      if iType=='3':
         gameNamePath=str(args['gameNamePath']) or ''

      packagingResources(iType,luacompile_key,luacompile_value,gameNamePath)

      #base/res game.zip
      if iType=='0' or iType=='1':
         bgIndex=0
         for item in configureArsg['game_list']:
            if str(item['zipped']) == '1':
               bgIndex=bgIndex+1
               pathName=m_originalResourcePath+'/'+item['ori']
               outPaht=m_buildPath+'/base/res/'+item['ori']
               command_single='cocos luacompile -s '+pathName+' -d '+outPaht+' -e -k '+luacompile_key+' -b '+luacompile_value+' --disable-compile'
               echo_single=executeExternalCommands(command_single)
               print(echo_single)

               echo_copyDf=executeExternalScript('PythonCommand.bat copyDirectorySpecifiedDirectory '+pathName.replace("/", "\\")+' '+outPaht.replace("/", "\\"))
               print(echo_copyDf)
               
               echo_md5=executeExternalScript('PythonCommand.bat createMd5File '+outPaht.replace("/", "\\"))
               print(echo_md5)

         if bgIndex>0 :
            outPaht=m_buildPath+'/base/res/game'
            echo_compressed=executeExternalScript('PythonCommand.bat compressedFile '+outPaht.replace("/", "\\")+'.zip'+' '+outPaht.replace("/", "\\"))
            print(echo_compressed)
            echo_df=executeExternalScript('PythonCommand.bat deleteDirectory '+outPaht.replace("/", "\\"))
            print(echo_df)

      if iType=='0' or iType=='1':
         zsdfsd=m_outputPath+'/'+folder
         echo_cfcf=executeExternalScript('PythonCommand.bat copyFileOrCompressedFile '+m_buildPath.replace("/", "\\")+' '+zsdfsd.replace("/", "\\")+' '+str(0))
         print(echo_cfcf)

         m_zip=zsdfsd+'/'+folder+'.zip'
         m_bcc=m_buildPath+'/base '+m_buildPath+'/command '+m_buildPath+'/client'
         echo_cf=executeExternalScript('PythonCommand.bat compressedFileBCC '+m_zip.replace("/", "\\")+' '+m_bcc.replace("/", "\\"))
         print(echo_cf)

      if iType=='1' or iType=='2':
         # md5
         for item in configureArsg['game_list']:
            outPaht=m_buildPath+'/'+item['ori']
            echo_game=executeExternalScript('PythonCommand.bat createMd5File '+outPaht.replace("/", "\\"))
            print(echo_game)

         # zip
         allOutPath=m_outputPath+'/'+folder
         executeExternalScript('PythonCommand.bat createDirectorys '+str(allOutPath).replace("/", "\\"))
         gamerar=m_buildPath+'/gamerar'
         executeExternalScript('PythonCommand.bat createDirectorys '+gamerar.replace("/", "\\"))  
         for item in configureArsg['game_list']:
            zipName=str(gamerar+'/'+item['folder']+'.zip').replace("/", "\\")
            zipPath=str(m_buildPath+'/'+item['ori']).replace("/", "\\")
            echo_zip=executeExternalScript('PythonCommand.bat compressedFile '+zipName+' '+zipPath)
            print(echo_zip)

         # copy the compiled files
         # command_game='PythonCommand.bat copyTheCompiledGameFile'+' '+folder
         command_game='PythonCommand.bat copyFileOrCompressedFile '+m_buildPath.replace("/", "\\")+' '+allOutPath.replace("/", "\\")+' '+str(0)
         echo_game=executeExternalScript(command_game)
         print(echo_game)

def packageApk(configureArsg,pName,libName,debugOrrelease,big,small,channel):
   print('package apk')
   echo_cmd=executeExternalScript('PythonCommand.bat cleanDirectory '+m_outputPath.replace("/", "\\"))
   print(echo_cmd)

   setVersion(big,small)
   setChannel(channel)
   args={'itype':0,'gameNamePath':''}
   commandResource(args,configureArsg)

   debugOrRelease='release'
   if str(debugOrrelease)=='true':
      debugOrRelease='debug'
   
   # vqd='-channel-'+channel
   # if channel=='0':
   #    vqd=''

   dirName=m_outputPath+'/'+folder
   echo_cmd=executeExternalScript('PythonCommand.bat createDirectorys '+dirName.replace("/", "\\"))
   print(echo_cmd)

   outApkPath=dirName+'/'+folder
   packagingType=int(configureArsg['packagingType']) or 1
   print(str(configureArsg['packagingInfo'])+":"+str(packagingType))
   echo_cmd=''
   if packagingType==1:
      echo_cmd=executeExternalScript('PythonCommand.bat copyAndStudioGoogleOutApk '+debugOrRelease+' '+libName+' '+outApkPath)
   elif packagingType==2:
      echo_cmd=executeExternalScript('PythonCommand.bat copyAndStudioCustomerOutApk '+debugOrRelease+' '+libName+' '+outApkPath)
   elif packagingType==3:
      echo_cmd=executeExternalScript('PythonCommand.bat copyAndStudioQmdlOutApk '+debugOrRelease+' '+libName+' '+outApkPath)
   print(echo_cmd)

   if channel !='0':
      outPaht='../client_channel'
      echo_cmd=executeExternalScript('PythonCommand.bat copyFileOrCompressedFile '+m_outputPath.replace("/", "\\")+' '+outPaht.replace("/", "\\")+' '+str(0))
      print(echo_cmd)

# clean Project File
def cleanProjectFile():
   print('clean Project File---------------------')
   if os.path.exists(m_buildPath):
      executeExternalScript('PythonCommand.bat deleteDirectory '+m_buildPath.replace("/", "\\"))

   basePath=m_originalResourcePath+'/base'
   if os.path.exists(basePath):
      executeExternalScript('PythonCommand.bat deleteDirectory '+basePath.replace("/", "\\"))

   # asValuesPath=m_frameworksPath+'/runtime-src/pro.androidstudio/app/res/values'
   # if os.path.exists(asValuesPath):
   #    executeExternalScript('PythonCommand.bat deleteDirectory '+asValuesPath.replace("/", "\\"))

   # asBuildPath=m_frameworksPath+'/runtime-src/pro.androidstudio/app/build'
   # if os.path.exists(asBuildPath):
   #    executeExternalScript('PythonCommand.bat deleteDirectory '+asBuildPath.replace("/", "\\"))

# Execute command parameters
def runCommand(commandArgs,configureArsg):
   print('Execute command parameters')
   global folder
   folder=str(configureArsg['ProjectValue'])+'-'+time.strftime('%Y-%m-%d-%H%M%S',time.localtime(time.time()))

   iType=''+str(commandArgs.iType)
   print('\t[0123 res,10]:'+iType)

   makefileOldProjectConfigurationFile(configureArsg)
   if iType=='0' or iType=='1' or iType=='2' or iType=='3':
      echo_cmd=executeExternalScript('PythonCommand.bat createDirectorys '+m_outputPath.replace("/", "\\"))
      print(echo_cmd)
      value={}
      value['itype']=iType
      value['gameNamePath']=commandArgs.subgamePath
      print('value:'+json.dumps(value))
      commandResource(value,configureArsg)
   elif iType=='6':
      debugOrRelease=configureArsg['release']
      vGpStr=makefileGradleProperties(debugOrRelease)
      vagradle='../frameworks/runtime-src/pro.androidstudio/gradle.properties'
      # if os.path.exists(vagradle):
      makefileNormal(vagradle,vGpStr)
         
      vLibName=str(debugOrRelease['libName'])
      vSStr=makefileSetTingsGradle(vLibName,debugOrRelease['libcocos2dx'])

      vagsettings='../frameworks/runtime-src/pro.androidstudio/settings.gradle'
      # if os.path.exists(vagsettings):
      makefileNormal(vagsettings,vSStr)

      makefileJksKeystore(debugOrRelease)
   elif iType=='10':
      NAME_PROJECT=commandArgs.projectName
      BIG_VERSION=commandArgs.versionBig
      SMALL_VERSION=commandArgs.versionSmall
      CHANNEl_ID=str(commandArgs.channelID)
      DEBUG_OR_RELEASE=commandArgs.debugOrRelease
      Lobby=commandArgs.lobby

      debugOrRelease=''
      print('\t[true debug,false release]:'+str(DEBUG_OR_RELEASE))
      if str(DEBUG_OR_RELEASE)=='true':
         debugOrRelease=configureArsg['debug']
      else:
         debugOrRelease=configureArsg['release']

      makefileGradleProperties(debugOrRelease)
      makefileJksKeystore(debugOrRelease)

      if str(Lobby)=='true':
         print('\tLobby == true ')
         vLibName=str(debugOrRelease['libName'])
         makefileSetTingsGradle(vLibName,debugOrRelease['libcocos2dx'])
         if CHANNEl_ID=='0':
            print('\t\tchannel number == 0 ')
            folder=str(NAME_PROJECT)+'-'+time.strftime('%Y-%m-%d-%H%M%S',time.localtime(time.time()))+'-v'+BIG_VERSION+'.'+SMALL_VERSION
            packageApk(configureArsg,NAME_PROJECT,vLibName,DEBUG_OR_RELEASE,BIG_VERSION,SMALL_VERSION,CHANNEl_ID)
         else:
            print('\t\tchannel number != 0 ')
            executeExternalScript('PythonCommand.bat cleanDirectory '+m_outputChannelPath.replace("/", "\\"))
            # varray=CHANNEl_ID.split('_')
            varray=getCutContent(CHANNEl_ID)
            print('\tchannel info:'+json.dumps(varray))
            for v in varray:
               folder=str(NAME_PROJECT)+'-'+time.strftime('%Y-%m-%d-%H%M%S',time.localtime(time.time()))+'-channel-'+str(v)+'-v'+BIG_VERSION+'.'+SMALL_VERSION
               print('\t\t\tchannel number =='+str(v)+' '+folder)
               packageApk(configureArsg,NAME_PROJECT,vLibName,DEBUG_OR_RELEASE,BIG_VERSION,SMALL_VERSION,v)
      
         cleanProjectFile()
      else:
         print('\tLobby == false ')
         args={'itype':2,'gameNamePath':''}
         commandResource(args,configureArsg)

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description="Project batch tool")
   parser.add_argument("-iType", "--iType", help="[0~3res,10apk]", default='false')
   parser.add_argument("-projectName", "--projectName", help="project name", default='false')
   parser.add_argument("-versionBig", "--versionBig", help="big version", default='1')
   parser.add_argument("-versionSmall", "--versionSmall", help="small version", default='0')
   parser.add_argument("-channelID", "--channelID", help="channel id", default='0')
   parser.add_argument("-debugOrRelease", "--debugOrRelease", help="debug or release", default='false')
   parser.add_argument("-lobby", "--lobby", help="lobby or games", default='true')

   parser.add_argument("-subgamePath", "--subgamePath", help="subgame path", default='false')
   args = parser.parse_args()

   m_configure=getConfigurationTable("PythonConfigure.json")
   print('iType[0123 res,6projectConfig,...,10apk]:'+args.iType)
   if args.iType != 'false':
      runCommand(args,m_configure)








