@echo off
rem 批处理文件中有两种类型的变量。 其中一个参数是在调用批处理文件时可以传递的参数，另一个是通过set命令完成的。

rem call:CommandLineArguments 1 2 3

rem call:UseNumericValues

rem call:LocalAndGlobalVariables

call:EnvironmentVariable

pause
exit

:CommandLineArguments
	echo args1:%1 args2:%2 args3:%3
	goto:eof
	
:UseNumericValues
	set /A a=5
	set /A b=10
	echo a=%a% b=%b% +-*/
	
	set /A c=%a% + %b%
	echo       a+b=%c%
	set /A c=%a% - %b%
	echo       a-b=%c%
	set /A c=%b% / %a%
	echo       a/b=%c%
	set /A c=%b% * %a%
	echo       a*b=%c%
	goto:eof
	
:LocalAndGlobalVariables
	set globalvar=5
	SETLOCAL
		set var=1
		set /A var=%var% + 5
		echo var=%var%
		set /A globalvar=%globalvar% + %var%
		echo globalvar=%globalvar%
	ENDLOCAL
	
	echo var=%var%
	echo globalvar=%globalvar%
	goto:eof
	
:EnvironmentVariable
	echo temp=%temp%

	rem 设置用户环境变量
	set CurrentPath=%~dp0
	setx JAVA_HOME "%CurrentPath%jdk1.8.0_162"
	setx path "%%JAVA_HOME%%\bin;%%JAVA_HOME%%\jre\bin;"
	
	goto:eof