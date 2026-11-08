# Gera mecanismos/index.html a partir da planilha da Giovanna.
#
# A página é o destino do QR code do seminário da FURB (12/11/2026): abre no celular, sem login
# e sem baixar nada.
#
# A Giovanna pediu TABELA, e é tabela de verdade: um <table> com cabeçalho fixo e a coluna do
# nome fixa na horizontal. Num telefone, sete colunas de texto corrido não cabem na largura, e a
# saída não é descaracterizar a tabela, é deixá-la rolar para o lado com o nome sempre à vista.
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

# A última coluna é um índice para a aba de referências; a fonte é uma só e vai no rodapé.
if cabecalho and cabecalho[-1].lower().startswith("fonte"):
    cabecalho = cabecalho[:-1]
    dados = [linha[:-1] for linha in dados]

e = html.escape


def celula(valor):
    return e(str(valor).strip()) if valor is not None else "—"


cabecalhos = "".join(f"<th scope='col'>{e(c)}</th>" for c in cabecalho)
corpo = []
for linha in dados:
    busca = " ".join(celula(v) for v in linha).lower()
    celulas = f"<th scope='row'>{celula(linha[0])}</th>" + "".join(
        f"<td>{celula(v)}</td>" for v in linha[1:]
    )
    corpo.append(f"<tr data-busca=\"{e(busca)}\">{celulas}</tr>")

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
  --papel: #FFFFFF; --risca: #E7E9EE; --zebra: #FAFBFC;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0; padding: 0 16px 72px;
  background: linear-gradient(140deg, var(--menta), var(--agua) 45%, var(--lilas-claro));
  background-attachment: fixed;
  color: var(--tinta);
  font: 400 16px/1.5 Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
}}
.envelope {{ max-width: 1680px; margin: 0 auto; }}
header {{ padding: 40px 0 16px; }}
h1 {{ margin: 0 0 10px; font-size: clamp(26px, 4.6vw, 42px); line-height: 1.12; letter-spacing: -.02em; }}
.linhafina {{ margin: 0; max-width: 70ch; color: var(--tinta-suave); font-size: clamp(15px, 2.2vw, 18px); }}
.procura {{
  width: 100%; max-width: 560px; margin: 24px 0 8px; padding: 13px 18px;
  border: 2px solid transparent; border-radius: 14px;
  background: var(--papel); color: inherit; font: inherit;
  box-shadow: 0 2px 18px #0b0b0c12;
}}
.procura:focus {{ outline: none; border-color: var(--turquesa); }}
.conta {{ margin: 0 0 6px; color: var(--tinta-fraca); font-size: 15px; }}
.dica {{ margin: 0 0 16px; color: var(--tinta-fraca); font-size: 14px; }}
@media (min-width: 1100px) {{ .dica {{ display: none; }} }}

.moldura {{
  background: var(--papel); border-radius: 20px; box-shadow: 0 2px 22px #0b0b0c14;
  overflow: auto; max-height: 78vh;
  overscroll-behavior-x: contain; -webkit-overflow-scrolling: touch;
}}
table {{ border-collapse: separate; border-spacing: 0; width: max-content; min-width: 100%; }}
caption {{ position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }}
th, td {{
  padding: 14px 18px; text-align: left; vertical-align: top;
  border-bottom: 1px solid var(--risca); min-width: 260px;
}}
thead th {{
  position: sticky; top: 0; z-index: 3;
  background: var(--papel); color: var(--lilas);
  font-size: 12px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase;
  border-bottom: 2px solid var(--turquesa); white-space: nowrap;
}}
tbody th {{
  position: sticky; left: 0; z-index: 2;
  background: var(--papel); min-width: 200px; max-width: 230px;
  font-weight: 700; border-right: 1px solid var(--risca);
}}
thead th:first-child {{ z-index: 4; left: 0; }}
tbody tr:nth-child(even) th, tbody tr:nth-child(even) td {{ background: var(--zebra); }}
tbody td {{ color: var(--tinta-suave); max-width: 420px; }}
tbody tr:hover th, tbody tr:hover td {{ background: #EFFBF8; }}
tr[hidden] {{ display: none; }}

/* No telefone a coluna fixa do nome comia metade da tela e sobrava pouco para o conteúdo. */
@media (max-width: 700px) {{
  th, td {{ padding: 12px 14px; min-width: 230px; }}
  tbody th {{ min-width: 136px; max-width: 150px; }}
}}

footer {{
  margin-top: 28px; padding-top: 20px; border-top: 1px solid #0b0b0c1a;
  color: var(--tinta-fraca); font-size: 14px;
}}
footer p {{ margin: 0 0 8px; max-width: 80ch; }}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --papel: #16181C; --tinta: #F2F3F5; --tinta-suave: #C7CAD1; --tinta-fraca: #8E939C;
    --risca: #272B31; --zebra: #1A1D22;
  }}
  :root:not([data-theme="light"]) body {{
    background: linear-gradient(140deg, #0E1A18, #101A1E 45%, #16142A);
  }}
  :root:not([data-theme="light"]) tbody tr:hover th,
  :root:not([data-theme="light"]) tbody tr:hover td {{ background: #1F2A2B; }}
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

<input id="procura" class="procura" type="search" autocomplete="off"
       aria-label="Filtrar a tabela"
       placeholder="Filtrar por antibiótico, alvo, organismo…">
<p class="conta" id="conta"></p>
<p class="dica">Arraste a tabela para o lado para ver todas as colunas.</p>

<div class="moldura">
  <table>
    <caption>Mecanismos de ação de antibióticos naturais descritos em Lewis et al. (2024)</caption>
    <thead><tr>{cabecalhos}</tr></thead>
    <tbody id="corpo">
{"".join(corpo)}
    </tbody>
  </table>
</div>

<footer>
  <p><strong>Fonte:</strong> LEWIS, K. et al. Sophisticated natural products as antibiotics.
  <em>Nature</em>, v.&nbsp;632, p.&nbsp;39–49, 2024. DOI&nbsp;10.1038/s41586-024-07530-w.</p>
  <p>Tabela organizada por Giovanna Pimentel a partir do artigo. Página sem indexação em
  buscadores.</p>
</footer>
</div>

<script>
// Filtro: esconde a linha cujo texto não contém o que foi digitado.
(function () {{
  var campo = document.getElementById("procura");
  var linhas = Array.prototype.slice.call(document.querySelectorAll("#corpo tr"));
  var conta = document.getElementById("conta");
  function atualizar() {{
    var termo = campo.value.trim().toLowerCase();
    var vistas = 0;
    linhas.forEach(function (l) {{
      var mostra = !termo || l.dataset.busca.indexOf(termo) !== -1;
      l.hidden = !mostra;
      if (mostra) vistas++;
    }});
    conta.textContent = vistas === linhas.length
      ? linhas.length + " antibióticos"
      : vistas + " de " + linhas.length + " antibióticos";
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
print(f"{SAIDA} — {len(dados)} linhas, {len(cabecalho)} colunas, {len(pagina) / 1024:.1f} KB")
