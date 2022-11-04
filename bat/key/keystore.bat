@echo off

set outPath=%~dp0out

PUSHD ..\
	echo Create keystore
	
	rem key的信息
	set keyName=ckeys.keystore
	set keyAlias=aaaa
	set keyPassword=112233
	set keyAliasPassword=112233
	
	rem 随机数量(多个key)
	set keyRNumber=3
	
	echo. keyName=%keyName%
	echo. keyAlias=%keyAlias%
	echo. keyPassword=%keyPassword%
	echo. keyAliasPassword=%keyAliasPassword%
	echo. keyRNumber=%keyRNumber%
	echo. 
	
	rem 单个key
	call python command.py --keystoreName %keyName% --keystoreAlias %keyAlias% --keystorePassword %keyPassword% --keystoreAliasPassword %keyAliasPassword% --targetPath %outPath%
	
	rem 多个key
	rem call python command.py --keyRandomNumber %keyRNumber% --keystoreName %keyName% --keystoreAlias %keyAlias% --keystorePassword %keyPassword% --keystoreAliasPassword %keyAliasPassword% --targetPath %outPath%
	
POPD

pause
exit




set keystore=bbbbcc
set fileextension=.keystore

set keystoreAlias=csdfsdfs
set key_password=adfafassafd23e41234
set store_password=adfafassafd23e41234
set dname="cn=aaa,ou=bbbb,o=ccc,l=ddd,st=eee,c=fffcsdf"

set keySaveName=key.txt

set vdir=.\out
if exist %vdir% (
	rmdir /s /q %vdir%
)
mkdir %vdir%


call:CreateAkey
rem call:CreateMultipleKeys 2

pause
exit

:CreateAkey
	call:CreatekeystoreKey %vdir%\%keystore%%fileextension% %keystoreAlias% %store_password% %key_password% %dname%
	goto:eof

:CreateMultipleKeys
	set count=%1
	setlocal enabledelayedexpansion
	FOR /L %%G IN (1,1,%count%) DO (
		call:CreatekeystoreKey %vdir%\%keystore%%%G%fileextension% %keystoreAlias%%%G %store_password% %key_password% %dname%
	)
	endlocal
	goto:eof
	
:CreatekeystoreKey
	set name=%1
	set alias=%2
	set storePassword=%3
	set keyPassword=%4
	set vDname=%5
	
	set fileName=""
	set fileSuffix=""
	for %%i in (%name%) do (
		set fileName=%%~ni
		set fileSuffix=%%~xi
	)
	
	echo keystore=%fileName%%fileSuffix% >> %name%.txt
	echo alias=%alias%  >> %name%.txt
	echo storepass=%storePassword%  >> %name%.txt
	echo storepass=%keyPassword%  >> %name%.txt
	echo dname=%vDname%  >> %name%.txt
	
	call keytool -genkey -v -keystore %name% -alias %alias% -storepass %storePassword% -keypass %keyPassword% -keyalg RSA -validity 20000 -dname %vDname%
	goto:eof