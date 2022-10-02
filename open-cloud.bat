@echo off
SetLocal EnableDelayedExpansion

rem =============================
rem ====== admin variables ======
rem =============================

set CloudURL="https://webdav.cloud.mail.ru/"
set CloudPassword="vmxE2idv7wXdsdeR0f6D"
set CloudUser="rychkin06@mail.ru"

set LocalDriveLetter="O"

rem =============================
rem ======== open cloud =========
rem =============================

net use %LocalDriveLetter%: %CloudURL% %CloudPassword% /user:%CloudUser%

rem =============================
rem == create daily directory ===
rem ======== YYYY-MM-DD =========
rem =============================

set DailyDirFullPath="%LocalDriveLetter%:/Warder/screenshots/%date:~6,4%-%date:~3,2%-%date:~0,2%"
md %DailyDirFullPath%

rem =============================
rem === main process starting ===
rem =============================

Powershell.exe -executionpolicy remotesigned -File "screenshot.ps1" "%DailyDirFullPath%/"

rem =============================
rem ======= close cloud =========
rem =============================

net use %LocalDriveLetter%: /delete /y