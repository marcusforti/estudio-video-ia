#!/usr/bin/env python3
"""Estima o gasto de uma máquina alugada e compara com o teto aprovado pelo dono.

Uso:
  python estimar_gasto.py --preco-hora 1.10 --horas 2 --teto 5
Código de saída: 0 = dentro do teto, 2 = acima do teto, 1 = argumento inválido.
"""
import argparse
import sys


def main() -> int:
    for fluxo in (sys.stdout, sys.stderr):
        if hasattr(fluxo, "reconfigure"):
            fluxo.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Estimativa de gasto de GPU ou VM alugada (USD).")
    ap.add_argument("--preco-hora", type=float, required=True, help="preço por hora da oferta, em USD")
    ap.add_argument("--horas", type=float, required=True, help="horas estimadas com a máquina ligada")
    ap.add_argument("--extra", type=float, default=0.0,
                    help="USD de disco, banda ou outros itens fora do preço por hora")
    ap.add_argument("--folga", type=float, default=30.0,
                    help="margem de segurança em %% sobre o tempo (padrão: 30)")
    ap.add_argument("--teto", type=float, required=True, help="teto de gasto aprovado, em USD")
    args = ap.parse_args()

    if min(args.preco_hora, args.horas, args.extra, args.folga, args.teto) < 0:
        print("Erro: use valores iguais ou maiores que zero.", file=sys.stderr)
        return 1

    base = args.preco_hora * args.horas
    com_folga = base * (1 + args.folga / 100)
    total = com_folga + args.extra

    print(f"Máquina: US$ {args.preco_hora:.2f}/h x {args.horas:g} h = US$ {base:.2f}")
    print(f"Com folga de {args.folga:g}%: US$ {com_folga:.2f}")
    print(f"Extras (disco, banda): US$ {args.extra:.2f}")
    print(f"ESTIMATIVA TOTAL: US$ {total:.2f} | TETO: US$ {args.teto:.2f}")
    if total > args.teto:
        print("ACIMA DO TETO: não crie a máquina. Peça nova autorização ao dono com este valor.")
        return 2
    print("Dentro do teto. Mostre estes números ao dono e crie só depois do OK dele.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
