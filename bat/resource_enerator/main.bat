@echo off

set outPath=%~dp0out

call:createProguardFile

pause
exit

:createProguardFile
	call:deletePathContent %outPath%

	@REM 包名
	set vPackageName="aa.bb.cc.dd"
	
	@REM 类名 前缀
	set vClassPrefix="Casino1078"
	
	@REM 调用类名字
	set vCallingClassName=%vClassPrefix%OnlineCardDomeMain

	@REM activity .R 默认是packageName
	set vActivityClassR=""
	
	@REM activity 数量
	set vActivityCount=60

	@REM 普通类 数量
	set vClassCount=99

	@REM 方法数量
	set vMethodCount=80

	@REM 资源drawable目录数量
	set vAssetsDrawableCount=5

	@REM 资源values/strings.xml目录数量
	set vStringCount=20

	@REM 资源values/colors.xml目录数量
	set vColorCount=20

	PUSHD ..\
		call python generator.py --packageName %vPackageName% --activityCount %vActivityCount% --activityClassR %vActivityClassR% --classCount %vClassCount% --methodCount %vMethodCount% --assetsDrawableCount %vAssetsDrawableCount% --callingClassName %vCallingClassName% --classPrefix %vClassPrefix% --stringCount %vStringCount% --colorCount %vColorCount% --targetPath %outPath%
	POPD
	goto:eof
	
:deletePathContent
	set dpc=%1
	echo delete path content
	if exist %dpc% (
	   rmdir /s /q %dpc%
	)
	mkdir %dpc%
	goto:eof

:createPathContent
	set dpc=%1
	echo delete path content
	if not exist %dpc% (
		mkdir %dpc%
	)
	goto:eof