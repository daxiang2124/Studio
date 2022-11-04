@echo off
set outPath="%cd%\out"

set dirHdpi=mipmap-hdpi
set dirLdpi=mipmap-ldpi
set dirMdpi=mipmap-mdpi
set dirXhdpi=mipmap-xhdpi
set dirXxhdpi=mipmap-xxhdpi
set dirXxxhdpi=mipmap-xxxhdpi

call:createDirectory %outPath%

call:createDirectory %outPath%\%dirHdpi%
call:coypFile %dirHdpi%\ic_launcher-72.png %outPath%\%dirHdpi%\ic_launcher.png
call:coypFile %dirHdpi%\ic_launcher.png %outPath%\%dirHdpi%\ic_launcher.png

call:createDirectory %outPath%\%dirLdpi%
call:coypFile %dirLdpi%\ic_launcher-36.png %outPath%\%dirLdpi%\ic_launcher.png
call:coypFile %dirLdpi%\ic_launcher.png %outPath%\%dirLdpi%\ic_launcher.png

call:createDirectory %outPath%\%dirMdpi%
call:coypFile %dirMdpi%\ic_launcher-48.png %outPath%\%dirMdpi%\ic_launcher.png
call:coypFile %dirMdpi%\ic_launcher.png %outPath%\%dirMdpi%\ic_launcher.png

call:createDirectory %outPath%\%dirXhdpi%
call:coypFile %dirXhdpi%\ic_launcher-96.png %outPath%\%dirXhdpi%\ic_launcher.png
call:coypFile %dirXhdpi%\ic_launcher.png %outPath%\%dirXhdpi%\ic_launcher.png

call:createDirectory %outPath%\%dirXxhdpi%
call:coypFile %dirXxhdpi%\ic_launcher-144.png %outPath%\%dirXxhdpi%\ic_launcher.png
call:coypFile %dirXxhdpi%\ic_launcher.png %outPath%\%dirXxhdpi%\ic_launcher.png

call:createDirectory %outPath%\%dirXxxhdpi%
call:coypFile %dirXxxhdpi%\ic_launcher-192.png %outPath%\%dirXxxhdpi%\ic_launcher.png


pause
exit

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
	
	if exist %cPath% (
		copy /y %cPath% %rPath%
	) else (
		echo. failed to copy file %dirPath%
	)
	goto:eof

