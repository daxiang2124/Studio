@echo off
rem 帮助文档|案例
rem https://www.jianshu.com/p/dbe579f6cc84
rem https://zhuanlan.zhihu.com/p/389584833


rem 输出路径
set outPath=%~dp0out

rem apk名字
set apkName=%~dp0apk\pakistan.apk

call:apktool
rem call:dex2jar

pause
exit

:apktool
	rem apk进行反编译
	echo apk-path=%apkName%
	echo out-path=%outPath%
	call:cleanDirectory %outPath%
	
	rem apktool路径
	set apktool=%cd%\apktool_2.6.1.jar
	call java -jar %apktool% d -f %apkName% -o %outPath%
	echo decompilation succeed
	
	goto:eof

:dex2jar
	set dex2jar=%cd%\dex2jar-2.0\d2j-jar2dex.bat
	echo dex2jar=%dex2jar%
	call %dex2jar% classes.dex
	goto:eof

:cleanDirectory
	echo cleanDirectory------------------------------------------
	set m_dir=%1
	echo. clean Directory m_dir=%m_dir%
	
	if exist %m_dir% (
	   rmdir /s /q %m_dir%
	)
	mkdir %m_dir%
	echo. clean Directory success %m_dir%
	goto:eof	
	
:createDirectorys
	echo createDirectorys------------------------------------------
	set m_dir=%1
	echo. created directory m_dir=%m_dir%
	if not exist %m_dir% (
		mkdir %m_dir%
	) else (
		echo. directory exists %m_dir%
	)
	goto:eof
	




