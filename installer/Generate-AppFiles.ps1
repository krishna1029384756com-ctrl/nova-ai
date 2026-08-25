param(
    [Parameter(Mandatory = $true)]
    [string]$SourceDir,
    [Parameter(Mandatory = $true)]
    [string]$OutputFile
)

$ErrorActionPreference = "Stop"
$source = (Resolve-Path $SourceDir).Path

function Escape-Xml([string]$Value) {
    return [System.Security.SecurityElement]::Escape($Value)
}

function Stable-Guid([string]$Value) {
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [Text.Encoding]::UTF8.GetBytes($Value.ToLowerInvariant())
        $hash = $sha.ComputeHash($bytes)
        $hex = -join ($hash | ForEach-Object { $_.ToString("x2") })
        return "{0}-{1}-{2}-{3}-{4}" -f $hex.Substring(0,8),$hex.Substring(8,4),$hex.Substring(12,4),$hex.Substring(16,4),$hex.Substring(20,12)
    }
    finally {
        $sha.Dispose()
    }
}

function Id-For([string]$Prefix, [string]$Value) {
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [Text.Encoding]::UTF8.GetBytes($Value.ToLowerInvariant())
        $hash = $sha.ComputeHash($bytes)
        $hex = -join ($hash | ForEach-Object { $_.ToString("x2") })
        return "${Prefix}_$($hex.Substring(0,24))"
    }
    finally {
        $sha.Dispose()
    }
}

$files = Get-ChildItem -LiteralPath $source -Recurse -File |
    Where-Object { $_.FullName -notmatch '\\(__pycache__|\.git)(\\|$)' } |
    Sort-Object FullName

$components = New-Object System.Collections.Generic.List[string]
$refs = New-Object System.Collections.Generic.List[string]
$directories = @{}

foreach ($file in $files) {
    $relative = [IO.Path]::GetRelativePath($source, $file.FullName).Replace('/', '\\')
    $relativeDir = [IO.Path]::GetDirectoryName($relative)
    if ([string]::IsNullOrWhiteSpace($relativeDir)) { $relativeDir = "." }

    $dirId = "INSTALLFOLDER"
    if ($relativeDir -ne ".") {
        $parts = $relativeDir -split '\\'
        $currentPath = ""
        foreach ($part in $parts) {
            $currentPath = if ($currentPath) { "$currentPath\\$part" } else { $part }
            if (-not $directories.ContainsKey($currentPath)) {
                $directories[$currentPath] = Id-For "D" $currentPath
            }
        }
        $dirId = $directories[$relativeDir]
    }

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

$dirNodes = New-Object System.Collections.Generic.List[string]
$dirsByDepth = $directories.Keys | Sort-Object { ($_ -split '\\').Count }, { $_ }

foreach ($dirPath in $dirsByDepth) {
    $parts = $dirPath -split '\\'
    $name = $parts[-1]
    $dirId = $directories[$dirPath]
    $parentPath = if ($parts.Count -gt 1) { ($parts[0..($parts.Count-2)] -join '\\') } else { "." }
    $parentId = if ($parentPath -eq ".") { "INSTALLFOLDER" } else { $directories[$parentPath] }
    $dirNodes.Add("      <Directory Id=\"$dirId\" Name=\"$(Escape-Xml $name)\" Parent=\"$parentId\" />")
}

$xml = @"
<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://wixtoolset.org/schemas/v4/wxs">
  <Fragment>
    <DirectoryRef Id="INSTALLFOLDER">
$($dirNodes -join "`n")
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
[IO.File]::WriteAllText((Resolve-Path $OutputFile -ErrorAction SilentlyContinue).Path ?? $OutputFile, $xml, [Text.UTF8Encoding]::new($false))
Write-Host "Generated $OutputFile with $($files.Count) files."
