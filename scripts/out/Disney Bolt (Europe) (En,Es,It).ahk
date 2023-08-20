;###################################################################################################
; AHKv1 script that extract an Encrypted ISO file, decrypt using PS3Dec.exe, then mount it.
; Author: dsync89
; Date: 2023-Aug-20
;###################################################################################################

; Get the full path of the script
scriptFullPath := A_ScriptFullPath
scriptDirectory := StrReplace(scriptPath, A_ScriptName, "")

; Read the config.txt file
configFile := scriptDirectory . ".config.ini"

; Read values from the config.txt file
IniRead, daemonToolsCLIPath, %configFile%, Settings, DaemonToolsCLIPath
IniRead, targetVirtualDriveLetter, %configFile%, Settings, TargetVirtualDriveLetter
IniRead, emuPath, %configFile%, Settings, EmuPath
IniRead, utilsPath, %configFile%, Settings, UtilsPath
IniRead, sourceRomDir, %configFile%, RomPath, SourceRomDir
IniRead, extractedRomDir, %configFile%, RomPath, ExtractedRomDir

; MsgBox, DaemonTools CLI Path: %daemonToolsCLIPath%
; MsgBox, Target Virtual Drive Letter: %targetVirtualDriveLetter%
; MsgBox, Emu Path: %emuPath%
; MsgBox, Utils Path: %utilsPath%

; ==============================
; DO NOT MODIFY
; ==============================

; Remove .ahk extension and add .iso extension
isoFilePath := SubStr(scriptFullPath, 1, StrLen(scriptFullPath) - 4) . ".iso"
; MsgBox % "ISO File Path: " isoFilePath

; Check if the ISO file path exists
if !FileExist(isoFilePath)
{
	sourceRomZipFileName := SubStr(A_ScriptName, 1, StrLen(A_ScriptName) - 4) . ".zip"
	sourceRomZipFilePath := sourceRomDir . "\" . sourceRomZipFileName
	; MsgBox, %sourceRomZipFilePath% 
	
	pythonPath := utilsPath . "\auto_decrypt.py"
	
	; MsgBox, %pythonPath%
	
    pythonCommand := "python " . Chr(34) . pythonPath . Chr(34) . " " . Chr(34) . sourceRomZipFilePath . Chr(34) . " " . Chr(34) . extractedRomDir . Chr(34)	
   	
	; MsgBox, %pythonCommand%
	
    ; Run the Python script and wait until it finishes
    RunWait, %pythonCommand%,,
	
    exitCode := ErrorLevel

    ; Check the exit code and print the result
    if (exitCode = 0)
    {
        ; MsgBox OK
    }
    else
    {
		MsgBox %exitCode%
        MsgBox Fail to decrypt %isoFilePath%
    }
}

else {
	; MsgBox, %isoFilePath% already exist and decrypted, mounting it next!
}

; Check drive
commandToExecute := """" . daemonToolsCLIPath . """ -G --type dt --number 0"

; Run the Daemon Tools Lite CLI command to get drive information
WshShell := ComObjCreate("Wscript.Shell")
exec := WshShell.Exec(commandToExecute)
output := exec.StdOut.ReadAll()
; MsgBox %output%

searchString := "Letter: " . targetVirtualDriveLetter
if InStr(output, searchString) {
    ; MsgBox, Drive 0 is assigned the letter Q. Using --mount_to command to mount ISO
	RunWait, "%daemonToolsCLIPath%" --mount_to --letter %targetVirtualDriveLetter% --path "%isoFilePath%", , Hide	

} else {
    ; MsgBox, Drive 0 is not assigned the letter Q. Using --mount command to mount ISO
	RunWait, "%daemonToolsCLIPath%" --mount --letter %targetVirtualDriveLetter% --path "%isoFilePath%", , Hide
}

Sleep, 1000 ; wait 1 sec

; Prepare to start game

driveWithSemiColon := targetVirtualDriveLetter . ":"
Run, %emuPath% --no-gui %driveWithSemiColon%

; RunWait, "%daemonToolsCLIPath%" --unmount --letter %targetVirtualDriveLetter%

Escape::
	Process, Close, rpcs3.exe
	Sleep, 1000 ; wait for 1s before unmounting
	; MsgBox, Unmounting ISO from %targetVirtualDriveLetter%
	RunWait, "%daemonToolsCLIPath%" --unmount --letter %targetVirtualDriveLetter%, , Hide
	ExitApp

ExitApp