@echo off

set dqlu=%CD%
set outPath=%dqlu%/out

rem HelloWorld
set fileName_HelloWorld=%dqlu%/HelloWorld.mk

set fileName_Edit=%dqlu%/Edit.mk

call:runMakeFile %fileName_Edit%

pause
exit


rem 执行文件不带参数 make
:runMakeFile
	set mFileName=%1
	echo run make file %mFileName%
	call make -f %mFileName%
	goto:eof

rem 执行文件不带参数 cmake
:runCMakeFile
	set mFileName=%1
	echo run make file %mFileName%
	call cmake -f %mFileName%
	goto:eof

rem 执行文件带1个参数
:runMakeFileValueOne
	set mFileName=%1
	set value1=%2
	echo run make file %mFileName%  parameter=%value1%
	call make -f %mFileName% %value1%
	goto:eof

