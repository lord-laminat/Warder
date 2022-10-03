(New-Object -ComObject Shell.Application).MinimizeAll()
Add-Type -AssemblyName System.Windows.Forms
$scr = [Windows.Forms.SystemInformation]::VirtualScreen
$filePath = $args[0] + ":/Warder/screenshots/$(Get-Date -Format 'yyyy/MM/dd' | ForEach-Object { $_ -replace '\.', '-' })"

while (1) {
    $bmp = New-Object Drawing.Bitmap $scr.Width, $scr.Height
    $gfx = [Drawing.Graphics]::FromImage($bmp)
    $gfx.CopyFromScreen($scr.Location, [Drawing.Point]::Empty, $scr.Size)
    $gfx.Dispose()
    $bmp.Save("$filePath/$(Get-Date -Format 'MM/dd/yyyy_HH-mm-ss' | ForEach-Object { $_ -replace '\.', '-' }).png")
    $bmp.Dispose()
    $counter = $counter + 1
    Start-Sleep 5
}