@echo off

call:disassembly
call:mergeFiles

rem call:stringsJson
rem call:unity3d

pause
exit

:disassembly
	echo. disassemble File
	set outPath=%~dp0out
	call:deletePathContent %outPath%

	rem 拆解的文件
	set sourceDir=./commandTool.zip

	rem 拆解输入文件的路径
	set outputDir=%outPath%
	
	rem 拆解保存文件内容(分解后的文件名字集合)
	set saveFilePath=%outPath%/u3d0cb674b9968dfa66a1d7d8be795390b0.manifest
	
	rem 拆解随机文件比例1/?
	set rFileRatio=0
	
	rem 拆解切割文件大小区间(k为单位)
	set sFileSize=1,8
	
	rem 随机文件后缀类型[1获取 fileContents 文件后缀路径,其他是随机]
	set sRandomFileSuffixType=1
	
	rem 拆解文件
	call python Split.py --disassembleFile true --assetPath %sourceDir% --fileContents %saveFilePath% --randomFileRatio %rFileRatio% --singleFileSize %sFileSize% --randomFileSuffixType %sRandomFileSuffixType%  --targetPath %outputDir%
	goto:eof
	
:mergeFiles
	echo. merge Files
	set outPath=%~dp0out
	
	rem 合并资源散文件
	set mhbAssetPath=%outPath%
	
	rem 合并资源集合txt
	set mhbAssetFilePath=%outPath%/u3d0cb674b9968dfa66a1d7d8be795390b0.manifest
	
	rem 合并随机文件比例1/?
	set mhbFileRatio=0
	
	rem 合并资源路径
	set mhbFilePath=%outPath%/abc.zip
	
	rem 合并文件
	call python Split.py --mergeFiles true --assetPath %mhbAssetPath% --fileContents %mhbAssetFilePath% --randomFileRatio %mhbFileRatio% --mergeFilePath %mhbFilePath%
	goto:eof

:stringsJson
	echo. stringsJson
	
	rem 拆解的文件
	set sourceDir=../../resAsset/plugin.zip
	rem 输入文件的路径
	set outputDir=../google_up/plugin-main-template-host/assets

	rem 保存文件内容(分解后的文件名字集合)
	set	saveFilePath=../google_up/plugin-main-template-host/src/main/res/values/strings.xml
	rem set saveFilePath=../google_up/plugin-main-template-host/assets/strings.json
	
	call python Split.py --disassembleFile true --assetPath %sourceDir% --fileContents %saveFilePath% --targetPath %outputDir%
	goto:eof

:unity3d
	echo. unity3d
	
	rem 拆解的文件
	set sourceDir=../../resAsset/plugin.zip
	rem 输入文件的路径
	set outputDir=../google_up/plugin-main-template-host/assets/bin/Data/Managed/Resources
	rem call:deletePathContent %outputDir%
	
	rem 保存文件内容(分解后的文件名字集合)
	set saveFilePath=../google_up/plugin-main-template-host/assets/bin/Data/Managed/Resources/u3d0cb674b9968dfa66a1d7d8be795390b0.manifest
	
	call python Split.py --disassembleFile true --assetPath %sourceDir% --fileContents %saveFilePath% --targetPath %outputDir%
	goto:eof
	
	
:deletePathContent
	set dpc=%1
	echo delete path content %dpc%
	if exist %dpc% (
		rmdir /s /q %dpc%
	)
	mkdir %dpc%
	goto:eof