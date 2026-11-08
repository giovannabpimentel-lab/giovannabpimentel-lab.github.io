# giovannabpimentel-lab.github.io

Site pessoal de Giovanna Pimentel, servido pelo GitHub Pages.

## O que tem aqui

- `index.html` — placeholder da raiz. Existe para que o Jekyll não publique este README como
  página inicial do site, o que aconteceu no primeiro deploy e expôs, numa página indexável, o
  caminho que era para circular só por QR code.
- A pasta da tabela-resumo dos mecanismos de ação de antibióticos naturais, destino do QR code
  do seminário (PPGQ/FURB, 12/11/2026). Página única, sem dependência externa, com filtro de
  busca. **Gerada por script, não editada à mão:** a fonte é `fontes-tabela.xlsx`.
- `.nojekyll` — desliga o Jekyll. O site é HTML pronto; não há o que processar, e com o Jekyll
  ligado qualquer `.md` solto no repositório vira página pública.

## Refazer a página depois de mexer na planilha

```powershell
uv run --with openpyxl python build/gerar-tabela.py fontes-tabela.xlsx
```

O script reescreve `mecanismos/index.html` inteiro. Editar o HTML direto se perde na próxima
geração.

## Decisões

- **`noindex`** na página: o combinado é que chegue só quem tem o link. O repositório é público,
  porque o GitHub Pages gratuito exige isso; "só quem tem o link" aqui é endereço não divulgado,
  não controle de acesso. Nada aqui é sigiloso — a tabela resume um artigo publicado na Nature.
- **Identidade visual** igual à do deck do seminário (degradê menta/lilás, Inter), para quem
  escaneia o QR reconhecer que chegou ao lugar certo.
- **Tabela de verdade**, a pedido da Giovanna: `<table>` com cabeçalho fixo no topo e a coluna
  do nome fixa na horizontal. Seis colunas de texto corrido não cabem na largura de um telefone,
  e o QR vai ser lido no telefone, então lá ela rola para o lado com o nome sempre à vista.

## Por fazer

- Página de currículo na raiz, no lugar do placeholder. Quando entrar, tirar o `noindex` do
  `index.html`.
- Conteúdo de pesquisa (scripts de R das análises estatísticas).
