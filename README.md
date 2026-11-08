# giovannabpimentel-lab.github.io

Site pessoal de Giovanna Pimentel, servido pelo GitHub Pages.

## O que tem aqui

- `mecanismos/` — tabela-resumo dos mecanismos de ação de antibióticos naturais, destino do
  QR code do seminário da disciplina Tópicos em Avaliação Antimicrobiana de Produtos Naturais
  (PPGQ/FURB, 12/11/2026). Página única, sem dependência externa, com filtro de busca.
  **Gerada por script, não editada à mão:** a fonte é `fontes-tabela.xlsx`.

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
- **Cartões no celular, duas colunas no desktop.** Sete colunas de texto corrido não cabem num
  telefone, e o QR vai ser lido no telefone.

## Por fazer

- Página de currículo na raiz. Hoje `/` devolve 404; só `/mecanismos/` existe.
- Conteúdo de pesquisa (scripts de R das análises estatísticas).
