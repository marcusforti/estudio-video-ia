# Instala as skills do Estudio de Video com IA no Claude Code e no Codex (Windows).
# Uso: irm https://raw.githubusercontent.com/marcusforti/estudio-video-ia/main/instalar.ps1 | iex
$ErrorActionPreference = "Stop"
$repo = "marcusforti/estudio-video-ia"
$tmp = Join-Path ([IO.Path]::GetTempPath()) ("estudio-video-ia-" + [guid]::NewGuid().ToString("N"))

try {
    New-Item -ItemType Directory -Force $tmp | Out-Null
    $zip = Join-Path $tmp "repo.zip"
    Invoke-WebRequest "https://codeload.github.com/$repo/zip/refs/heads/main" -OutFile $zip -UseBasicParsing
    Expand-Archive $zip -DestinationPath $tmp -Force
    $origem = Get-ChildItem $tmp -Directory | Select-Object -First 1
    $skills = Get-ChildItem (Join-Path $origem.FullName "skills") -Directory
    $base = if ($env:ESTUDIO_HOME) { $env:ESTUDIO_HOME } else { $HOME }
    $carimbo = Get-Date -Format "yyyyMMdd-HHmmss"

    foreach ($destino in @((Join-Path $base ".claude\skills"), (Join-Path $base ".codex\skills"))) {
        New-Item -ItemType Directory -Force $destino | Out-Null
        foreach ($s in $skills) {
            $alvo = Join-Path $destino $s.Name
            if (Test-Path $alvo) {
                $copia = Join-Path $base (".estudio-video-ia-backup\" + $carimbo + "\" + (Split-Path (Split-Path $destino -Parent) -Leaf))
                New-Item -ItemType Directory -Force $copia | Out-Null
                Move-Item $alvo (Join-Path $copia $s.Name)
            }
            Copy-Item $s.FullName $alvo -Recurse
        }
        Write-Host "$($skills.Count) skills instaladas em $destino"
    }

    foreach ($ferramenta in @("ffmpeg", "python")) {
        if (-not (Get-Command $ferramenta -ErrorAction SilentlyContinue)) {
            Write-Host "Aviso: $ferramenta nao encontrado. Os scripts das skills precisam dele."
        }
    }
    Write-Host "Pronto. Abra uma sessao nova e chame /estudio-workflow."
}
finally {
    Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
}
