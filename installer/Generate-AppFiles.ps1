param(
    [Parameter(Mandatory = $true)]
    [string]$SourceDir,
    [Parameter(Mandatory = $true)]
    [string]$OutputFile
)

$ErrorActionPreference = "Stop"
$source = (Resolve-Path $SourceDir).Path

function Escape-Xml([string]$Value) {
    [System.Security.SecurityElement]::Escape($Value)
}

function Stable-Guid([string]$Value) {
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [Text.Encoding]::UTF8.GetBytes($Value.ToLowerInvariant())
        $hash = $sha.ComputeHash($bytes)
        $hex = -join ($hash | ForEach-Object { $_.ToString("x2") })
        return "{0}-{1}-{2}-{3}-{4}" -f $hex.Substring(0,8), $hex.Substring(8,4), $hex.Substring(12,4), $hex.Substring(16,4), $hex.Substring(20,12)
    }
    finally { $sha.Dispose() }
}

function Id-For([string]$Prefix, [string]$Value) {
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [Text.Encoding]::UTF8.GetBytes($Value.ToLowerInvariant())
        $hash = $sha.ComputeHash($bytes)
        $hex = -join ($hash | ForEach-Object { $_.ToString("x2") })
        return "${Prefix}_$($hex.Substring(0,24))"
    }
    finally { $sha.Dispose() }
}

$files = Get-ChildItem -LiteralPath $source -Recurse -File |
    Where-Object { $_.FullName -notmatch '\\(__pycache__|\.git)(\\|$)' } |
    Sort-Object FullName

$directories = @{}
foreach ($directory in (Get-ChildItem -LiteralPath $source -Recurse -Directory | Sort-Object FullName)) {
    if ($directory.FullName -match '\\(__pycache__|\.git)(\\|$)') { continue }
    $relative = [IO.Path]::GetRelativePath($source, $directory.FullName).Replace('/', '\\')
    $directories[$relative] = Id-For "D" $relative
}

$components = New-Object System.Collections.Generic.List[string]
$refs = New-Object System.Collections.Generic.List[string]

foreach ($file in $files) {
    $relative = [IO.Path]::GetRelativePath($source, $file.FullName).Replace('/', '\\')
    $relativeDir = [IO.Path]::GetDirectoryName($relative)
    if ([string]::IsNullOrWhiteSpace($relativeDir)) { $relativeDir = "." }

    $dirId = if ($relativeDir -eq ".") { "INSTALLFOLDER" } else { $directories[$relativeDir] }
    if (-not $dirId) { throw "Directory ID missing for $relativeDir" }

    $componentId = Id-For "C" $relative
    $fileId = Id-For "F" $relative
    $guid = Stable-Guid "component:$relative"
    $sourcePath = "`$(var.SourceDir)\\$relative"

    $components.Add(@"
      <Component Id="$componentId" Directory="$dirId" Guid="{$guid}">
        <File Id="$fileId" Source="$(Escape-Xml $sourcePath)" KeyPath="yes" />
      </Component>
"@)
    $refs.Add("      <ComponentRef Id=\"$componentId\" />")
}

function Build-DirectoryTree([string]$ParentRelative, [int]$Indent) {
    $parentPrefix = if ($ParentRelative) { "$ParentRelative\\" } else { "" }
    $children = $directories.Keys |
        Where-Object {
            $relative = $_
            if ($ParentRelative) {
                if (-not $relative.StartsWith($parentPrefix, [StringComparison]::OrdinalIgnoreCase)) { return $false }
                $rest = $relative.Substring($parentPrefix.Length)
            } else {
                $rest = $relative
            }
            return ($rest -notmatch '\\')
        } |
        Sort-Object

    $lines = New-Object System.Collections.Generic.List[string]
    foreach ($child in $children) {
        $name = if ($ParentRelative) { $child.Substring($parentPrefix.Length) } else { $child }
        $id = $directories[$child]
        $pad = " " * $Indent
        $lines.Add("${pad}<Directory Id=\"$id\" Name=\"$(Escape-Xml $name)\">")
        $nested = Build-DirectoryTree $child ($Indent + 2)
        if ($nested) { $lines.AddRange($nested) }
        $lines.Add("${pad}</Directory>")
    }
    return $lines
}

$tree = Build-DirectoryTree "" 6

$xml = @"
<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://wixtoolset.org/schemas/v4/wxs">
  <Fragment>
    <DirectoryRef Id="INSTALLFOLDER">
$($tree -join "`n")
$($components -join "`n")
    </DirectoryRef>
  </Fragment>
  <Fragment>
    <ComponentGroup Id="AppFiles">
$($refs -join "`n")
    </ComponentGroup>
  </Fragment>
</Wix>
"@

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $OutputFile) | Out-Null
[IO.File]::WriteAllText($OutputFile, $xml, [Text.UTF8Encoding]::new($false))
Write-Host "Generated $OutputFile with $($files.Count) files and $($directories.Count) directories."
