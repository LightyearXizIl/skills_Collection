[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$InputVideo,
    [Parameter(Mandatory)][string]$OutputVideo,
    [string]$ReportPath,
    [string]$FfmpegPath='C:\Users\16054\Documents\ComfyUI\tools\ffmpeg\ffmpeg.exe',
    [string]$FfprobePath='C:\Users\16054\Documents\ComfyUI\tools\ffmpeg\ffprobe.exe',
    [ValidateRange(0,1)][double]$DurationToleranceSeconds=0.05
)
$ErrorActionPreference='Stop'
$ff=(Resolve-Path -LiteralPath $FfmpegPath).Path
$fp=(Resolve-Path -LiteralPath $FfprobePath).Path
$inputResolved=(Resolve-Path -LiteralPath $InputVideo).Path
$outputResolved=(Resolve-Path -LiteralPath $OutputVideo).Path
if ($inputResolved -eq $outputResolved) {throw 'Input and output must differ.'}
if ($ReportPath) {
    $reportFull=[IO.Path]::GetFullPath($ReportPath)
    if ($reportFull -in @($inputResolved,$outputResolved,$ff,$fp) -or (Test-Path -LiteralPath $reportFull)) {throw 'Report path must be a new file distinct from inputs.'}
}
function Get-Probe([string]$Path) {
    $json=& $fp -v error -count_frames -show_entries 'format=duration,size:stream=index,codec_name,codec_type,width,height,pix_fmt,r_frame_rate,avg_frame_rate,sample_rate,channels,nb_read_frames,duration' -of json $Path
    if ($LASTEXITCODE -ne 0) {throw "ffprobe failed: $Path"}
    return ($json -join "`n" | ConvertFrom-Json)
}
function Get-AudioHashes([string]$Path,[object[]]$Streams) {
    $result=@()
    for($i=0;$i -lt $Streams.Count;$i++) {
        $hash=& $ff -v error -i $Path -map "0:a:$i" -c copy -f hash -hash sha256 - 2>&1
        if ($LASTEXITCODE -ne 0) {throw "Audio hash failed: $Path stream $i"}
        $line=@($hash | ForEach-Object {"$_"} | Where-Object {$_ -match '^SHA256='})
        if ($line.Count -ne 1) {throw "Missing audio hash: $Path stream $i"}
        $result += $line[0].Trim()
    }
    return $result
}
$src=Get-Probe $inputResolved
$dst=Get-Probe $outputResolved
$sv=@($src.streams | Where-Object codec_type -eq 'video')
$dv=@($dst.streams | Where-Object codec_type -eq 'video')
if ($sv.Count -lt 1 -or $dv.Count -lt 1) {throw 'Both files must contain video.'}
$sa=@($src.streams | Where-Object codec_type -eq 'audio')
$da=@($dst.streams | Where-Object codec_type -eq 'audio')
$sh=@(Get-AudioHashes $inputResolved $sa)
$dh=@(Get-AudioHashes $outputResolved $da)
$audioMatches=($sa.Count -gt 0 -and $sa.Count -eq $da.Count)
if ($audioMatches) {
    for($i=0;$i -lt $sa.Count;$i++) {
        if ($sh[$i] -ne $dh[$i] -or $sa[$i].codec_name -ne $da[$i].codec_name -or $sa[$i].sample_rate -ne $da[$i].sample_rate -or $sa[$i].channels -ne $da[$i].channels) {$audioMatches=$false}
    }
}
$decodeLog=(& $ff -v error -i $outputResolved -map '0:v:0' -map '0:a' -f null NUL 2>&1 | Out-String).Trim()
$decodeExit=$LASTEXITCODE
$delta=[math]::Abs([double]$src.format.duration-[double]$dst.format.duration)
$framesValid=($null -ne $sv[0].nb_read_frames -and $null -ne $dv[0].nb_read_frames -and
    [string]$sv[0].nb_read_frames -match '^\d+$' -and [string]$dv[0].nb_read_frames -match '^\d+$')
$checks=[ordered]@{
    decode_ok=($decodeExit -eq 0 -and [string]::IsNullOrWhiteSpace($decodeLog))
    width_matches=($sv[0].width -eq $dv[0].width)
    height_matches=($sv[0].height -eq $dv[0].height)
    frame_rate_matches=($sv[0].r_frame_rate -eq $dv[0].r_frame_rate -and $sv[0].avg_frame_rate -eq $dv[0].avg_frame_rate)
    frame_count_matches=($framesValid -and $sv[0].nb_read_frames -eq $dv[0].nb_read_frames)
    pixel_format_yuv420p=($dv[0].pix_fmt -eq 'yuv420p')
    duration_within_tolerance=($delta -le $DurationToleranceSeconds)
    original_audio_stream_hash_matches=$audioMatches
}
$report=[ordered]@{schema_version=2;passed=(-not ($checks.Values -contains $false));
    input=$inputResolved;output=$outputResolved;output_sha256=(Get-FileHash -LiteralPath $outputResolved -Algorithm SHA256).Hash;
    duration_difference_seconds=$delta;input_audio_hashes=$sh;output_audio_hashes=$dh;checks=$checks;
    input_probe=$src;output_probe=$dst;decode_log=$decodeLog;visual_review='pending';user_review='pending'}
$json=$report | ConvertTo-Json -Depth 10
if ($ReportPath) {
    [IO.Directory]::CreateDirectory((Split-Path -Parent $reportFull)) | Out-Null
    [IO.File]::WriteAllText($reportFull,$json,[Text.UTF8Encoding]::new($false))
}
$json
if (-not $report.passed) {exit 1}
