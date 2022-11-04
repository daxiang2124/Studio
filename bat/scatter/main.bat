@echo off
set outPath="%cd%\out"

call:randImage

pause
exit

:randImage
	call:createDirectory %outPath%
	
	@REM 资源路径
	set vFilePath=D:\git\ListTheGame\scatter

	@REM 随机数量
	set vImageCount=13

	@REM 名字前缀
	set vFileNamePrefix="bgtr_"

	@REM 过滤的目录
	set vFilterDirectory="main;four_directions;hide;card"

	call python main.py --filePath %vFilePath% --imageCount %vImageCount% --fileNamePrefix %vFileNamePrefix% --filterDirectory %vFilterDirectory% --targetPath %outPath%

	goto:eof

:createDirectory
	echo createDirectory------------------------------------------
	set dirPath=%1
	echo. dirPath=%dirPath%
	
	if exist %dirPath% (
		rmdir /s /q %dirPath%
		echo. deleteDirectory Directory success %dirPath%
	) else (
		echo. deleteDirectory no such directory %dirPath%
	)
	mkdir %dirPath%
	goto:eof
	
:coypFile
	echo coypFile------------------------------------------
	set cPath=%1
	set rPath=%2
	echo. cPath=%cPath% rPath=%rPath%
	
	copy /y %cPath% %rPath%
	goto:eof

