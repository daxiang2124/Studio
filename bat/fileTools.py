#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import sys;
import os;
import hashlib;
import shutil;

#拼接目录路径
def joinDir(root, *dirs):
    for item in dirs:
        root = os.path.join(root, item)
    return root

#拷贝文件或目录(src拷贝路径,dest目标路径)
def copyDir(src, dest):
    for item in os.listdir(src):
        if "." == item[0]: # ignore hidden files
            continue
        nSrc = joinDir(src, item) #当前文件
        nDest = joinDir(dest, item) #拷贝到目标文件
        if os.path.isfile(nSrc): #是否是文件
            copyFile(nSrc, nDest)
        else:
            if not os.path.exists(nDest): #文件或目录否存在
                os.mkdir(nDest)
            copyDir(nSrc, nDest)

#读取文件内容
def readFile(src):
    buff = ""
    with open(src, 'rb') as f: #以二进制格式打开一个文件用于只读。文件指针将会放在文件的开头。这是默认模式。一般用于非文本文件如图片等。
        buff = f.read()
    return buff

#拷贝文件(src拷贝路径,dest目标路径)
def copyFile(src, dest):
    buff = ""
    with open(src, 'rb') as f: #以二进制格式打开一个文件用于只读。文件指针将会放在文件的开头。这是默认模式。一般用于非文本文件如图片等。
        buff = f.read()
    with open(dest, 'wb+') as f:#以二进制格式打开一个文件只用于写入。如果该文件已存在则打开文件,并从开头开始编辑,即原有内容会被删除。如果该文件不存在,创建新文件。一般用于非文本文件如图片等。
        f.write(buff)

#递归删除目录下的文件(子文件夹不删除)
def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)

#递归删除目录
def del_dir(path):
     shutil.rmtree(path)

#返回文件大小(以字节为单位)
def fileSize(filePath):
    filePath = unicode(filePath,'utf8')
    fsize = os.path.getsize(filePath)
    sv= int(''+bytes(fsize))
    return sv

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

#修改文件名字[key文件名字,文件路径,修改后名字]
def setFileName(path,md5):
    vvcc=path.replace('\\','/')
    vList=vvcc.split('/')
    tempName=vList[len(vList)-1]
    new_name = "" + md5 + "__" + tempName
    ragdir=vvcc[0:len(vvcc)-len(tempName)]+new_name
    os.rename(vvcc, ragdir)
    jqstr="./remote-assets/"
    name=ragdir[len(jqstr):len(ragdir)]
    return [name,ragdir,new_name]

#获取文件路径信息[key文件名字,文件路径,修改后名字]
def getFileNameInfo(value):
    tmd5=fileMd5(value)
    tempPath=str(value).split('/')[-1]
    tPath=str(tempPath).replace('\\','/')
    tName=os.path.splitext(os.path.split(tPath)[-1])[0]
    tNamExtension=os.path.splitext(tPath)[-1]
    tPath=tPath.replace(str(tName)+''+str(tNamExtension),'')

    # print('\tapkName:'+tName + ' '+tNamExtension+' path:'+tPath)
    return {'name':str(tName)+''+str(tNamExtension),'extension':tNamExtension,'path':tPath,'md5':tmd5}

#遍历目录md5(路径fileName,保存的md5值列表形式addMd5)
def fileDirMd5(fileName,addMd5):
    if os.path.isdir(fileName):
        fileList=os.listdir(fileName)
        # print('fileList:',json.dumps(fileList))
        for value in fileList:
            # print('\tvalue:'+value)
            fileDir=os.path.dirname(os.path.join(fileName,value))
            path=os.path.join(fileDir,value)
            if os.path.isfile(path):
                vTemp=getFileNameInfo(path)
                addMd5.append({"path":vTemp['path'],"name":vTemp['name'],"md5":vTemp['md5']})
            else:
                tempDir=os.path.join(fileDir,value)
                fileDirMd5(tempDir,addMd5)
    else:
        fileDir=os.path.dirname(fileName)
        path=os.path.join(fileDir,fileName)
        vTemp=getFileNameInfo(path)
        addMd5.append({"path":vTemp['path'],"name":vTemp['name'],"md5":vTemp['md5']})