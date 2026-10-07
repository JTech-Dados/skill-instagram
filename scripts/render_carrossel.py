#!/usr/bin/env python3
"""Renderiza os slides de um carrossel em PNG (1080x1350) a partir de slides.json.

Uso:
  python3 scripts/render_carrossel.py conteudo/2026-10-07-minha-peca

Requer: pip install playwright  (e um Chromium: `playwright install chromium`,
ou CHROMIUM_PATH apontando para o executável de um Chromium já instalado).
"""

import json
import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TEMPLATE = RAIZ / "templates" / "carrossel.html"


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    pasta = Path(sys.argv[1])
    dados = json.loads((pasta / "slides.json").read_text(encoding="utf-8"))
    slides = dados["slides"]

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("Playwright não instalado: pip install playwright")

    html = TEMPLATE.read_text(encoding="utf-8")
    with sync_playwright() as p:
        executavel = os.environ.get("CHROMIUM_PATH")
        browser = p.chromium.launch(executable_path=executavel) if executavel else p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1350})
        for n, slide in enumerate(slides, start=1):
            meta = {"conta": dados.get("conta", ""), "indice": n, "total": len(slides)}
            injecao = (
                f"<script>window.SLIDE={json.dumps(slide, ensure_ascii=False)};"
                f"window.TEMA={json.dumps(dados.get('tema', {}), ensure_ascii=False)};"
                f"window.META={json.dumps(meta, ensure_ascii=False)};</script>"
            )
            page.set_content(html.replace("<body>", "<body>" + injecao, 1), wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            saida = pasta / f"slide-{n:02d}.png"
            page.screenshot(path=str(saida))
            print(saida)
        browser.close()


if __name__ == "__main__":
    main()
