Windows下的开发不可避免的会用到bat脚本来做一些重复的工作，尤其是需要注册的插件dll这块。现在大家的开发机一般都是win7或win10，为了和用户环境比较一致，一般都不会关掉UAC的功能。
双击bat脚本执行自动注册或自动运行服务会很方便开发，但是在vista以上的系统经常需要以管理员权限来启动这个脚本，一般都是右键选择管理员权限运行，要是分发给其他人员测试的时候还要特地叮嘱下，要是bat能实现自动检测需要管理员权限，然后弹出这个提权的申请框，在提权完成之后再进行工作就好了。
抱着这个需求，找到了stackoverflow，果然不负众望，有人给出了一个解决方案，这里把这个bat脚本贴出来，给有需要的人士。


```
::::::::::::::::::::::::::::::::::::::::::::
:: Elevate.cmd - Version 2
:: Automatically check & get admin rights
::::::::::::::::::::::::::::::::::::::::::::
@echo off
CLS
ECHO.
ECHO =============================
ECHO Running Admin shell
ECHO =============================

:init
setlocal DisableDelayedExpansion
set "batchPath=%~0"
for %%k in (%0) do set batchName=%%~nk
set "vbsGetPrivileges=%temp%\OEgetPriv_%batchName%.vbs"
setlocal EnableDelayedExpansion

:checkPrivileges
NET FILE 1>NUL 2>NUL
if '%errorlevel%' == '0' ( goto gotPrivileges ) else ( goto getPrivileges )

:getPrivileges
if '%1'=='ELEV' (echo ELEV & shift /1 & goto gotPrivileges)
ECHO.
ECHO **************************************
ECHO Invoking UAC for Privilege Escalation
ECHO **************************************

ECHO Set UAC = CreateObject^("Shell.Application"^) > "%vbsGetPrivileges%"
ECHO args = "ELEV " >> "%vbsGetPrivileges%"
ECHO For Each strArg in WScript.Arguments >> "%vbsGetPrivileges%"
ECHO args = args ^& strArg ^& " "  >> "%vbsGetPrivileges%"
ECHO Next >> "%vbsGetPrivileges%"
ECHO UAC.ShellExecute "!batchPath!", args, "", "runas", 1 >> "%vbsGetPrivileges%"
"%SystemRoot%\System32\WScript.exe" "%vbsGetPrivileges%" %*
exit /B

:gotPrivileges
setlocal & pushd .
cd /d %~dp0
if '%1'=='ELEV' (del "%vbsGetPrivileges%" 1>nul 2>nul  &  shift /1)

::::::::::::::::::::::::::::
::START
::::::::::::::::::::::::::::
REM Run shell as admin (example) - put here code as you like
ECHO %batchName% Arguments: %1 %2 %3 %4 %5 %6 %7 %8 %9
```

作者：mercurygear
链接：https://www.jianshu.com/p/81a140d3c8d7
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。