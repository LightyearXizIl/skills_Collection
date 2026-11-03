[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$InputVideo,
    [Parameter(Mandatory)][string]$AssPath,
    [Parameter(Mandatory)][string]$OutputVideo,
    [string]$FfmpegPath='C:\Users\16054\Documents\ComfyUI\tools\ffmpeg\ffmpeg.exe',
    [string]$FontPath='C:\Windows\Fonts\NotoSerifSC-VF.ttf',
    [ValidateRange(0,51)][int]$Crf=18,
    [ValidateSet('ultrafast','superfast','veryfast','faster','fast','medium','slow','slower','veryslow')][string]$Preset='slow',
    [switch]$Force
)
$ErrorActionPreference='Stop'
$inputResolved=(Resolve-Path -LiteralPath $InputVideo).Path
$assResolved=(Resolve-Path -LiteralPath $AssPath).Path
$ff=(Resolve-Path -LiteralPath $FfmpegPath).Path
$font=(Resolve-Path -LiteralPath $FontPath).Path
$outputFull=[IO.Path]::GetFullPath($OutputVideo)
$logPath=$outputFull+'.render.log'
if ($outputFull -in @($inputResolved,$assResolved,$font,$ff)) {throw 'Output must not overwrite any input.'}
if ((Test-Path -LiteralPath $outputFull) -and -not $Force) {throw "Output already exists: $outputFull"}
if (Test-Path -LiteralPath $logPath) {throw "Render log already exists: $logPath"}
if ([IO.Path]::GetExtension($outputFull) -ine '.mp4') {throw 'Output must be an MP4 file.'}
[IO.Directory]::CreateDirectory((Split-Path -Parent $outputFull)) | Out-Null
$tempBase=[IO.Path]::GetFullPath([IO.Path]::GetTempPath())
$temp=Join-Path $tempBase ('ly-sub-'+[guid]::NewGuid().ToString('N'))
if ($temp -match '[^\x00-\x7F]') {throw "An ASCII temporary base is required: $tempBase"}
[IO.Directory]::CreateDirectory($temp) | Out-Null
$fonts=Join-Path $temp 'fonts'
[IO.Directory]::CreateDirectory($fonts) | Out-Null
$tempAss=Join-Path $temp 'sub.ass'
$tempFont=Join-Path $fonts 'NotoSerifSC.ttf'
[IO.File]::Copy($assResolved,$tempAss,$false)
[IO.File]::Copy($font,$tempFont,$false)
$ffArgs=@('-hide_banner','-loglevel','info')
$ffArgs += if ($Force) {'-y'} else {'-n'}
$ffArgs += @('-i',$inputResolved,'-vf','ass=sub.ass:fontsdir=fonts','-map','0:v:0','-map','0:a',
    '-c:v','libx264','-preset',$Preset,'-crf',[string]$Crf,'-pix_fmt','yuv420p','-fps_mode','passthrough',
    '-c:a','copy','-movflags','+faststart',$outputFull)
Push-Location -LiteralPath $temp
try {
    & $ff @ffArgs 2> $logPath
    if ($LASTEXITCODE -ne 0) {throw "ffmpeg failed ($LASTEXITCODE). Inspect $logPath"}
} finally {
    Pop-Location
    # Only remove the two known files and empty directories created by this invocation.
    $resolvedTemp=[IO.Path]::GetFullPath($temp)
    if (-not $resolvedTemp.StartsWith($tempBase,[StringComparison]::OrdinalIgnoreCase)) {throw 'Unexpected cleanup path.'}
    Remove-Item -LiteralPath $tempAss,$tempFont -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $fonts -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $temp -ErrorAction SilentlyContinue
}
[pscustomobject]@{output=$outputFull;render_log=$logPath;font=$font;font_sha256=(Get-FileHash -LiteralPath $font -Algorithm SHA256).Hash} | ConvertTo-Json
