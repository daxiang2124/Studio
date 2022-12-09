@echo off
echo .

rem 创建垃圾文件(拷贝多次目录)

set h=%time:~0,2%
set h=%h: =0%
set folder=%date:~0,4%-%date:~5,2%-%date:~8,2%-%h%%time:~3,2%

set copyCount=999999999999999
set copyDir=.\mode
set targetDir=.\text

rem copy mode .\text\%folder%

setlocal enabledelayedexpansion
	for /l %%i in (1,1,%copyCount%) do (
		mkdir .\text\%folder%-%%i
		copy %copyDir% %targetDir%\%folder%-%%i
	)
endlocal


pause