#!/usr/bin/env python3
"""Confere se a lista de instâncias alugadas está vazia (o fim real do ciclo).

Entrada: o JSON de `vastai show instances --raw`, por arquivo ou pela entrada padrão.
  vastai show instances --raw | python lista_vazia.py
  vastai show instances --raw | python lista_vazia.py --meu-id 12345678

Códigos de saída:
  0 = lista vazia (ou, com --meu-id, os seus IDs sumiram)
  1 = ainda existe instância (a sua, ou qualquer uma se não usar --meu-id)
  3 = entrada ilegível: NÃO conclua que está vazia; rode o comando de novo
"""
import argparse
import json
import sys


def carregar(texto: str):
    dados = json.loads(texto)
    if isinstance(dados, dict):
        dados = dados.get("instances", [dados] if "id" in dados else [])
    if not isinstance(dados, list):
        raise ValueError("o JSON não é uma lista de instâncias")
    return dados


def descrever(item) -> str:
    if not isinstance(item, dict):
        return str(item)
    partes = [f"id={item.get('id')}"]
    for chave in ("label", "actual_status", "status"):
        if item.get(chave):
            partes.append(f"{chave}={item[chave]}")
    return " ".join(partes)


def main() -> int:
    for fluxo in (sys.stdout, sys.stderr):
        if hasattr(fluxo, "reconfigure"):
            fluxo.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Confere se não sobrou máquina alugada.")
    ap.add_argument("arquivo", nargs="?", help="JSON salvo; sem ele, lê a entrada padrão")
    ap.add_argument("--meu-id", action="append", default=[],
                    help="ID que você criou; repita para vários. Instâncias de outras sessões não são tocadas")
    args = ap.parse_args()

    texto = open(args.arquivo, encoding="utf-8").read() if args.arquivo else sys.stdin.read()
    if not texto.strip():
        print("ERRO: entrada vazia. O comando de listagem falhou? Rode de novo antes de concluir.")
        return 3
    try:
        itens = carregar(texto)
    except (ValueError, json.JSONDecodeError) as erro:
        print(f"ERRO: não consegui ler a lista ({erro}). Rode o comando de novo antes de concluir.")
        return 3

    meus = {str(i) for i in args.meu_id}
    if not args.meu_id:
        if not itens:
            print("OK: lista vazia. Nenhuma máquina alugada.")
            return 0
        print(f"AINDA EXISTEM {len(itens)} instância(s):")
        for item in itens:
            print("  " + descrever(item))
        return 1

    restam = [i for i in itens if isinstance(i, dict) and str(i.get("id")) in meus]
    outras = [i for i in itens if i not in restam]
    if restam:
        print("AINDA EXISTE a sua instância:")
        for item in restam:
            print("  " + descrever(item))
        return 1
    print("OK: os IDs informados não estão mais na lista.")
    if outras:
        print(f"Aviso: há {len(outras)} instância(s) que não são suas. Não mexa; avise o dono:")
        for item in outras:
            print("  " + descrever(item))
    return 0


if __name__ == "__main__":
    sys.exit(main())
