#!/usr/bin/env bash
# Instala as skills do Estudio de Video com IA no Claude Code e no Codex (Linux e macOS).
# Uso: curl -fsSL https://raw.githubusercontent.com/marcusforti/estudio-video-ia/main/instalar.sh | bash
set -euo pipefail

repo="marcusforti/estudio-video-ia"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

curl -fsSL "https://codeload.github.com/$repo/tar.gz/refs/heads/main" | tar -xz -C "$tmp"
origem="$(find "$tmp" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
base="${ESTUDIO_HOME:-$HOME}"
carimbo="$(date +%Y%m%d-%H%M%S)"

for destino in "$base/.claude/skills" "$base/.codex/skills"; do
  mkdir -p "$destino"
  total=0
  for pasta in "$origem"/skills/*/; do
    nome="$(basename "$pasta")"
    if [ -e "$destino/$nome" ]; then
      copia="$base/.estudio-video-ia-backup/$carimbo/$(basename "$(dirname "$destino")")"
      mkdir -p "$copia"
      mv "$destino/$nome" "$copia/$nome"
    fi
    cp -R "$pasta" "$destino/$nome"
    total=$((total + 1))
  done
  echo "$total skills instaladas em $destino"
done

for ferramenta in ffmpeg python3; do
  command -v "$ferramenta" >/dev/null 2>&1 || echo "Aviso: $ferramenta nao encontrado. Os scripts das skills precisam dele."
done
echo "Pronto. Abra uma sessao nova e chame /estudio-workflow."
