[CmdletBinding(DefaultParameterSetName='Workspace')]
param(
    [Parameter(Mandatory,ParameterSetName='Workspace')][string]$WorkspaceRoot,
    [Parameter(Mandatory,ParameterSetName='Projects')][string]$ProjectsRoot,
    [Parameter(Mandatory)][ValidateRange(1,99)][int]$ItemNumber,
    [Parameter(Mandatory)][string]$SongTitle,
    [Parameter(Mandatory)][string]$VideoPath,
    [Parameter(Mandatory)][string]$DryVocalPath,
    [Parameter(Mandatory)][string]$FullMixPath,
    [Parameter(Mandatory)][datetime]$ProjectDate,
    [switch]$MoveSources
)
$ErrorActionPreference='Stop'

function Assert-OrdinaryPath([string]$Path) {
    $full=[IO.Path]::GetFullPath($Path)
    while ($full) {
        if (Test-Path -LiteralPath $full) {
            $item=Get-Item -LiteralPath $full -Force
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Reparse path is not supported: $full" }
        }
        $parent=Split-Path -Parent $full
        if ($parent -eq $full) {break}
        $full=$parent
    }
}

$safeTitle=$SongTitle.Trim()
foreach($ch in [IO.Path]::GetInvalidFileNameChars()) { $safeTitle=$safeTitle.Replace([string]$ch,'_') }
if ([string]::IsNullOrWhiteSpace($safeTitle) -or $safeTitle -in @('.','..') -or $safeTitle.EndsWith('.')) {
    throw 'SongTitle does not form a valid project name.'
}
if ($PSCmdlet.ParameterSetName -eq 'Workspace') {
    $workspace=(Resolve-Path -LiteralPath $WorkspaceRoot).Path
    if ((Split-Path -Leaf $workspace) -eq '01_视频项目') {throw 'Use -ProjectsRoot for the 01_视频项目 directory.'}
    $projects=[IO.Path]::GetFullPath((Join-Path $workspace '01_视频项目'))
} else { $projects=(Resolve-Path -LiteralPath $ProjectsRoot).Path }
Assert-OrdinaryPath $projects
$project=Join-Path $projects ('{0}_第{1:D2}条_{2}' -f $ProjectDate.ToString('yyyy-MM-dd'),$ItemNumber,$safeTitle)
Assert-OrdinaryPath $project
$manifestPath=Join-Path $project '02_输入素材\素材清单.json'
if (Test-Path -LiteralPath $manifestPath) {throw "Project already initialized; inspect its manifest before reuse: $manifestPath"}

$specs=@(
    @{source=$VideoPath;role='无字幕视频';relative="02_输入素材\01_视频源\${safeTitle}_无字幕版.mp4";extension='.mp4'},
    @{source=$DryVocalPath;role='干声';relative="02_输入素材\02_音频源\${safeTitle}_干声.flac";extension='.flac'},
    @{source=$FullMixPath;role='完整带音乐版';relative="02_输入素材\02_音频源\${safeTitle}_完整带音乐版.flac";extension='.flac'}
)
$seen=@{}
# Resolve and hash all sources and collision targets before the first mutation.
foreach($spec in $specs) {
    $src=(Resolve-Path -LiteralPath $spec.source).Path
    Assert-OrdinaryPath $src
    if ((Get-Item -LiteralPath $src).PSIsContainer -or [IO.Path]::GetExtension($src) -ine $spec.extension) {throw "Invalid source: $src"}
    if ($seen.ContainsKey($src)) {throw "A source was assigned to multiple roles: $src"}
    $seen[$src]=$true
    $dest=Join-Path $project $spec.relative
    Assert-OrdinaryPath $dest
    if ($MoveSources -and [IO.Path]::GetPathRoot($src) -ine [IO.Path]::GetPathRoot($dest)) {throw 'MoveSources requires the same drive.'}
    $spec.source=$src; $spec.destination=$dest
    $spec.sha256=(Get-FileHash -LiteralPath $src -Algorithm SHA256).Hash
    if ((Test-Path -LiteralPath $dest) -and (Get-FileHash -LiteralPath $dest -Algorithm SHA256).Hash -ne $spec.sha256) {throw "Destination has different content: $dest"}
}
$plainCopy=Join-Path $project "05_最终成品\01_无字幕版\${safeTitle}_无字幕版.mp4"
Assert-OrdinaryPath $plainCopy
if ((Test-Path -LiteralPath $plainCopy) -and (Get-FileHash -LiteralPath $plainCopy -Algorithm SHA256).Hash -ne $specs[0].sha256) {throw "Different no-subtitle copy already exists: $plainCopy"}

$dirs=@('01_项目说明','02_输入素材\01_视频源','02_输入素材\02_音频源','03_生成过程',
    '04_剪辑字幕工程\01_字幕与识别','04_剪辑字幕工程\02_检查图','04_剪辑字幕工程\03_工具脚本',
    '04_剪辑字幕工程\04_工作副本与备份','04_剪辑字幕工程\05_字体授权','05_最终成品\01_无字幕版','05_最终成品\02_字幕版')
foreach($dir in $dirs) {
    $path=Join-Path $project $dir
    Assert-OrdinaryPath $path
    [IO.Directory]::CreateDirectory($path) | Out-Null
}
$records=@()
foreach($spec in $specs) {
    $status='reused-identical-source-retained'
    if (-not (Test-Path -LiteralPath $spec.destination)) {
        if ($MoveSources) {
            [IO.File]::Move($spec.source,$spec.destination)
            $status='moved'
        } else {
            [IO.File]::Copy($spec.source,$spec.destination,$false)
            $status='copied'
        }
    }
    if ((Get-FileHash -LiteralPath $spec.destination -Algorithm SHA256).Hash -ne $spec.sha256) {
        throw "SHA-256 mismatch; retain all files for inspection: $($spec.destination)"
    }
    $records += [pscustomobject]@{role=$spec.role;source=$spec.source;archived=$spec.destination;
        bytes=(Get-Item -LiteralPath $spec.destination).Length;sha256=$spec.sha256;status=$status}
}
if (-not (Test-Path -LiteralPath $plainCopy)) {[IO.File]::Copy($specs[0].destination,$plainCopy,$false)}
if ((Get-FileHash -LiteralPath $plainCopy -Algorithm SHA256).Hash -ne $specs[0].sha256) {throw 'No-subtitle copy hash mismatch.'}
$manifest=[ordered]@{schema_version=2;created_at=[datetimeoffset]::Now.ToString('o');project_root=$project;
    song_title=$SongTitle;item_number=$ItemNumber;project_date=$ProjectDate.ToString('yyyy-MM-dd');
    source_files_preserved=(-not ($records.status -contains 'moved'));files=$records;no_subtitle_copy=$plainCopy}
$utf8=[Text.UTF8Encoding]::new($false)
[IO.File]::WriteAllText($manifestPath,($manifest | ConvertTo-Json -Depth 6),$utf8)
$mdPath=Join-Path $project '02_输入素材\素材清单.md'
if (-not (Test-Path -LiteralPath $mdPath)) {
    $md=@('# 素材清单', '', "正式歌名：$SongTitle", '', '参数探测与素材对应关系需在项目验收时补充。', '')
    foreach($r in $records) {$md += @("用途：$($r.role)","原路径：$($r.source)","归档路径：$($r.archived)","SHA-256：$($r.sha256)","状态：$($r.status)",'')}
    [IO.File]::WriteAllText($mdPath,($md -join "`n"),$utf8)
}
[pscustomobject]@{project_root=$project;manifest=$manifestPath;files=$records.Count} | ConvertTo-Json
