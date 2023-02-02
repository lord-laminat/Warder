#define MyAppName "Warder"
#define MyAppVersion "0.1.3"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{27AA509C-EFF0-4945-A1F9-3FBEC5AEDD17}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
DefaultDirName={pf}\Warder 0.1.3
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputBaseFilename=warder-setup
Compression=lzma/ultra64
SolidCompression=yes
InternalCompressLevel=ultra64
AppPublisher=Yopta Game Maker
VersionInfoProductVersion=0.1.3

[Components]
Name: server_files; Description: "Server files"; ExtraDiskSpaceRequired: 4800
Name: client_files; Description: "Client files"; ExtraDiskSpaceRequired: 4800

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Files]
Source: "..\client_files\client_script.exe"; DestDir: "{app}/client_files"; Flags: ignoreversion; Components: client_files
Source: "..\client_files\configs.json"; DestDir: "{app}/client_files"; Flags: ignoreversion; Components: client_files
Source: "..\server_files\server_script.exe"; DestDir: "{app}/server_files"; Flags: ignoreversion; Components: server_files
Source: "..\server_files\users.json"; DestDir: "{app}/server_files"; Flags: ignoreversion; Components: server_files
; NOTE: Don't use "Flags: ignoreversion" on any shared system files
