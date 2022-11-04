@echo off

rem call:TraverseDirectoryValueNull rem 遍历当前目录下的所有文件
rem call:FUNCTIONARGS 11 22 33

rem set abc=12
rem call:FUNCTIONARGS_RETURN %abc% 22

rem call:Display


set value1=1
set value2=2
echo value1=%value1%
echo value2=%value2%
call:SetValue value1,value2
echo value1=%value1%
echo value2=%value2%

pause
exit

:SetValue
	set "%~1=5"
	set "%~2=10"
	goto:eof

:Display
	set /A index=2 
	echo The value of index is %index% 
	goto:eof

:FUNCTIONARGS
	set args1=%1
	set args2=%2
	set args3=%3
	
	echo args1=%1 %args1%
	echo args2=%2 %args2%
	echo args3=%3 %args3%
	
	echo return:%return%
	goto:eof

:FUNCTIONARGS_RETURN
	echo myFuncReturnValue
	echo myFuncReturnValue First para:%1
	echo myFuncReturnValue Second para:%2
	set "%~1=%2%"
	goto:eof


rem 遍历当前目录下的所有文件
:TraverseDirectoryValueNull
	rem 无参 遍历当前目录下的所有文件
	for %%i in (*) do (
		echo %%i
	)
	
	rem 无参指定路径
	rem set dirFile=%CD%
	rem echo dirFile=%dirFile%
	rem for %%i in (%dirFile%\*.*) do (
	rem 	echo      %%i
	rem )
	goto:eof
	
rem 遍历指定目录下的所有文件夹，%%i 指向每个子文件夹的绝对路径
:TraverseDirectory
	echo aa
	for %%i in (*.*) do (
		echo %%i
	)
	echo bb
	for /d /r %%i in (*.*) do (
		echo %%i
	)
	goto:eof

rem 等效于 java 中的 for (int i = 1; i <= 5; i++)语句，起始值，递增或递减，终止值都可自行设置
:FUNCTION
	for /r %%i in (*.bat) do ( 
		echo %%i
	)

	for /l %%i in (1, 1, 5) do (
		echo   %%i
	)
	goto:eof
