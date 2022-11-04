@echo off

rem call:CreateString
rem set str=HelloWorld
rem call:StringLen str strlen
rem echo %str% is %strlen% characters long

call:StringXXXX

pause
exit

:CreateString
	set message=Hello World 
	echo message=%message%
	
	rem 空字符串
	set a2=
	set b2=Hello
	if [%a2%]==[] (
		echo String A is empty
	)
	if [%b2%]==[] (
		echo String B is empty
	)
	
	rem 字符串连接
	set a3=Hello
	set b3=World
	set /A d3=50
	set c3=%a3% and %b3% %d3%
	echo c3=%c3%
	goto:eof
	
:StringLen
	setlocal enabledelayedexpansion
	:strLen_Loop
		if not "!%1:~%len%!"=="" (
			set /A len+=1 & goto:strLen_Loop
		)
	(endlocal & set %2=%len%)
	goto:eof
	
:StringXXXX
	set vvstr=This string    has    a  lot  of spaces
	echo %vvstr%
	set vvstr=%vvstr:=%
	echo %vvstr%
	goto:eof