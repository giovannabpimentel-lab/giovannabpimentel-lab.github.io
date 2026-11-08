# Gera mecanismos/index.html a partir da planilha da Giovanna.
#
# A página é o destino do QR code do seminário da FURB (12/11/2026): abre no celular, sem login
# e sem baixar nada. Por isso duas decisões: tabela em cartões no celular e em grade no desktop
# (sete colunas de texto corrido não cabem num telefone), e `noindex`, porque o combinado é que
# só chegue quem tem o link.
#
# Uso: uv run --with openpyxl python build/gerar-tabela.py <planilha.xlsx>
import html
import sys
from pathlib import Path

from openpyxl import load_workbook

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "mecanismos" / "index.html"
planilha = Path(sys.argv[1])

livro = load_workbook(planilha, data_only=True)
aba = livro.worksheets[0]
linhas = [list(r) for r in aba.iter_rows(values_only=True) if any(c is not None for c in r)]
cabecalho = [str(c or "").strip() for c in linhas[0]]
dados = linhas[1:]

# A última coluna é um índice numérico para a aba de referências; a fonte é uma só e vai no rodapé.
if cabecalho and cabecalho[-1].lower().startswith("fonte"):
    cabecalho = cabecalho[:-1]
    dados = [linha[:-1] for linha in dados]

campos = cabecalho[1:]          # o primeiro é o nome, que vira título do cartão
e = html.escape


def celula(valor):
    return e(str(valor).strip()) if valor is not None else "—"


cartoes = []
for linha in dados:
    nome = celula(linha[0])
    itens = "".join(
        f'<div class="campo"><dt>{e(rotulo)}</dt><dd>{celula(valor)}</dd></div>'
        for rotulo, valor in zip(campos, linha[1:])
    )
    busca = " ".join(celula(v) for v in linha).lower()
    cartoes.append(f'<article class="ficha" data-busca="{e(busca)}">'
                   f'<h2>{nome}</h2><dl>{itens}</dl></article>')

pagina = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Mecanismos de ação de antibióticos naturais</title>
<style>
:root {{
  --menta: #DCFEEE; --agua: #E4FAFF; --lilas-claro: #E3DDFF;
  --turquesa: #28D0D3; --lilas: #8992E1;
  --tinta: #0B0B0C; --tinta-suave: #3C3F45; --tinta-fraca: #6B7079;
  --papel: #FFFFFF;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0; padding: 0 16px 72px;
  background: linear-gradient(140deg, var(--menta), var(--agua) 45%, var(--lilas-claro));
  background-attachment: fixed;
  color: var(--tinta);
  font: 400 17px/1.5 Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
}}
.envelope {{ max-width: 1180px; margin: 0 auto; }}
header {{ padding: 44px 0 20px; }}
h1 {{ margin: 0 0 10px; font-size: clamp(28px, 5vw, 44px); line-height: 1.12; letter-spacing: -.02em; }}
.linhafina {{ margin: 0; color: var(--tinta-suave); font-size: clamp(15px, 2.4vw, 19px); }}
.procura {{
  width: 100%; margin: 26px 0 10px; padding: 14px 18px;
  border: 2px solid transparent; border-radius: 14px;
  background: var(--papel); color: inherit; font: inherit;
  box-shadow: 0 2px 18px #0b0b0c12;
}}
.procura:focus {{ outline: none; border-color: var(--turquesa); }}
.conta {{ margin: 0 0 20px; color: var(--tinta-fraca); font-size: 15px; }}
.fichas {{ display: grid; gap: 18px; }}
.ficha {{
  background: var(--papel); border-radius: 20px; padding: 22px;
  box-shadow: 0 2px 20px #0b0b0c12;
}}
.ficha[hidden] {{ display: none; }}
.ficha h2 {{
  margin: 0 0 16px; font-size: 22px; line-height: 1.2;
  padding-bottom: 12px; border-bottom: 2px solid var(--menta);
}}
dl {{ margin: 0; display: grid; gap: 14px; }}
.campo {{ display: grid; gap: 3px; }}
dt {{
  font-size: 12px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase;
  color: var(--lilas);
}}
dd {{ margin: 0; color: var(--tinta-suave); }}
@media (min-width: 900px) {{
  .ficha {{ padding: 26px 30px; }}
  dl {{ grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px 36px; }}
  .campo:first-child, .campo:nth-child(3) {{ grid-column: span 1; }}
}}
footer {{
  margin-top: 40px; padding-top: 22px; border-top: 1px solid #0b0b0c1a;
  color: var(--tinta-fraca); font-size: 14px;
}}
footer p {{ margin: 0 0 8px; }}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --papel: #16181C; --tinta: #F2F3F5; --tinta-suave: #C7CAD1; --tinta-fraca: #8E939C;
  }}
  :root:not([data-theme="light"]) body {{
    background: linear-gradient(140deg, #0E1A18, #101A1E 45%, #16142A);
  }}
  :root:not([data-theme="light"]) .ficha {{ box-shadow: 0 2px 20px #0003; }}
  :root:not([data-theme="light"]) .ficha h2 {{ border-bottom-color: #2A3D38; }}
}}
</style>
</head>
<body>
<div class="envelope">
<header>
  <h1>Mecanismos de ação de antibióticos naturais</h1>
  <p class="linhafina">Tabela-resumo do seminário de Giovanna Pimentel, da disciplina
  Tópicos em Avaliação Antimicrobiana de Produtos Naturais (PPGQ&nbsp;/&nbsp;FURB), em
  novembro de 2026.</p>
</header>

<label class="visually-hidden" for="procura" hidden>Filtrar</label>
<input id="procura" class="procura" type="search" autocomplete="off"
       placeholder="Filtrar por antibiótico, alvo, organismo…">
<p class="conta" id="conta"></p>

<main class="fichas" id="fichas">
{"".join(cartoes)}
</main>

<footer>
  <p><strong>Fonte:</strong> LEWIS, K. et al. Sophisticated natural products as antibiotics.
  <em>Nature</em>, v.&nbsp;632, p.&nbsp;39–49, 2024. DOI&nbsp;10.1038/s41586-024-07530-w.</p>
  <p>Tabela organizada por Giovanna Pimentel a partir do artigo. Página sem indexação em
  buscadores.</p>
</footer>
</div>

<script>
// Filtro simples: esconde a ficha cujo texto não contém o que foi digitado.
(function () {{
  var campo = document.getElementById("procura");
  var fichas = Array.prototype.slice.call(document.querySelectorAll(".ficha"));
  var conta = document.getElementById("conta");
  function atualizar() {{
    var termo = campo.value.trim().toLowerCase();
    var vistas = 0;
    fichas.forEach(function (f) {{
      var mostra = !termo || f.dataset.busca.indexOf(termo) !== -1;
      f.hidden = !mostra;
      if (mostra) vistas++;
    }});
    conta.textContent = vistas === fichas.length
      ? fichas.length + " antibióticos"
      : vistas + " de " + fichas.length + " antibióticos";
  }}
  campo.addEventListener("input", atualizar);
  atualizar();
}})();
</script>
</body>
</html>
"""

SAIDA.parent.mkdir(parents=True, exist_ok=True)
SAIDA.write_text(pagina, encoding="utf-8")
print(f"{SAIDA} — {len(dados)} antibióticos, {len(campos)} campos, {len(pagina) / 1024:.1f} KB")
