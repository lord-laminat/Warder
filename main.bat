<# :
  @echo off
    powershell /nop /ex bypass^
    "&{[ScriptBlock]::Create((gc '%~f0') -join [Char]10).Invoke()}"
  exit /b
#>
(New-Object -ComObject Shell.Application).MinimizeAll()
Add-Type -AssemblyName System.Windows.Forms
$scr = [Windows.Forms.SystemInformation]::VirtualScreen


while (1) {
    $bmp = New-Object Drawing.Bitmap $scr.Width, $scr.Height
    $gfx = [Drawing.Graphics]::FromImage($bmp)
    $gfx.CopyFromScreen($scr.Location, [Drawing.Point]::Empty, $scr.Size)
    $gfx.Dispose()
    $bmp.Save("./scrsht_$(Get-Date -Format "MM/dd/yyyy_HH-mm-ss" | ForEach-Object { $_ -replace "\.", "-" }).png")
    $bmp.Dispose()
    $counter = $counter + 1
    Start-Sleep 5
}