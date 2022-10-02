(New-Object -ComObject Shell.Application).MinimizeAll()
Add-Type -AssemblyName System.Windows.Forms
$scr = [Windows.Forms.SystemInformation]::VirtualScreen
$DailyDir = $args[0]

while (1) {
    $bmp = New-Object Drawing.Bitmap $scr.Width, $scr.Height
    $gfx = [Drawing.Graphics]::FromImage($bmp)
    $gfx.CopyFromScreen($scr.Location, [Drawing.Point]::Empty, $scr.Size)
    $gfx.Dispose()
    $bmp.Save("$DailyDir$(Get-Date -Format 'MM/dd/yyyy_HH-mm-ss' | ForEach-Object { $_ -replace '\.', '-' }).png")
    $bmp.Dispose()
    $counter = $counter + 1
    Start-Sleep 5
}