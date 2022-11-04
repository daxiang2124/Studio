@echo off

call:newFunction

pause
exit

:newFunction
	call python PythonCommand.py --iType 6
	goto:eof
	

