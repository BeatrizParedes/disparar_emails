# salvar como: limpar_emails.py
# uso:
#   python limpar_emails.py            # vai ler raw_emails.txt
#   python limpar_emails.py arquivo.txt

import re
import sys
from pathlib import Path
import pandas as pd

def extrair_emails(texto):
    # regex para capturar formatos comuns de e-mail
    padrao = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", re.UNICODE)
    encontrados = padrao.findall(texto)
    # limpar caracteres colados
    encontrados = [e.strip().strip(';,<>\"\'()[]') for e in encontrados]
    # normalizar para lowercase (opcional)
    encontrados = [e.lower() for e in encontrados]
    # remover duplicados preservando ordem
    vistos = set()
    res = []
    for e in encontrados:
        if e not in vistos:
            vistos.add(e)
            res.append(e)
    # validar com regex "âncora"
    pad_val = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")
    validados = [e for e in res if pad_val.match(e)]
    return validados

def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "raw_emails.txt"
    p = Path(arg)
    if not p.exists():
        print(f"Arquivo não encontrado: {p.resolve()}")
        print("Crie um arquivo chamado raw_emails.txt com o texto (cole o bloco que você postou) e rode o script.")
        return

    texto = p.read_text(encoding="utf-8", errors="ignore")
    emails = extrair_emails(texto)
    if not emails:
        print("Nenhum e-mail válido encontrado — verifique se o arquivo contém o texto bruto (não imagem).")
        return

    # salvar CSV, XLSX e TXT (um por linha)
    df = pd.DataFrame({"email": emails})
    csv_out = Path("emails_clean.csv")
    xlsx_out = Path("emails_clean.xlsx")
    txt_out = Path("emails_clean.txt")
    df.to_csv(csv_out, index=False, encoding="utf-8")
    df.to_excel(xlsx_out, index=False)
    txt_out.write_text("\n".join(emails), encoding="utf-8")

    print(f"{len(emails)} e-mails extraídos e salvos em:")
    print(f"  - {csv_out.resolve()}")
    print(f"  - {xlsx_out.resolve()}")
    print(f"  - {txt_out.resolve()}")
    print("\nAmostra (primeiros 20):")
    for e in emails[:20]:
        print("  ", e)

if __name__ == "__main__":
    main()
