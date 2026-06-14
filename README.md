# 📊 Gerador de Relatório de Notas em PDF

Atividade Avaliativa N3 — Disciplina de Programação Estruturada  
**Curso:** Sistemas de Informação — 2º Período  
**Instituição:** Universidade do Estado de Mato Grosso — UNEMAT  
**Professor:** Prof. Me. Cides S. Bezerra  

**Desenvolvido por:**
- Guilherme Lorrã Souza Guimarães
- Diego Da Silva Ferreira

---

## 📋 Descrição

Sistema em Python para leitura de notas de alunos, cálculo de médias e geração de um relatório completo em PDF. O relatório inclui estatísticas da turma, gráfico de pizza com aprovados vs reprovados e tabela de alunos com destaque visual por situação.

---

## 📁 Estrutura dos Arquivos

```
Atividade_central/
├── main.py                # Código-fonte principal
├── main.html              # Documentação gerada pelo pydoc
├── notas_alunos.txt       # Arquivo de entrada com as notas
├── resultado_final.txt    # Arquivo de saída processado
└── relatorio_final.pdf    # Relatório gerado em PDF
```

---

## ▶️ Como Executar

### 1. Instalar dependências

```bash
pip install fpdf2 matplotlib
```

### 2. Preparar o arquivo de entrada

Crie o arquivo `notas_alunos.txt` no mesmo diretório, no formato:

```
Nome do Aluno;Nota1;Nota2
Ana Clara;8.5;9.0
Bruno Silva;5.0;6.0
```

### 3. Executar

```bash
python main.py
```

Isso gera automaticamente:
- `resultado_final.txt` — médias e situações calculadas
- `relatorio_final.pdf` — relatório completo em PDF

### 4. Gerar documentação HTML (pydoc)

```bash
python -m pydoc -w main
```

---

## ⚙️ Funções do Programa

| Função | Descrição |
|---|---|
| `calcular_media()` | Calcula a média aritmética entre duas notas |
| `definir_situacao()` | Retorna "Aprovado" (média ≥ 7.0) ou "Reprovado" |
| `carregar_arquivo()` | Lê o arquivo de entrada `.txt` |
| `salvar_arquivo()` | Salva os resultados em `.txt` |
| `processar_dados()` | Coordena leitura, cálculo e gravação |
| `calcular_estatisticas()` | Calcula total, média geral, maior/menor nota |
| `gerar_grafico_pizza()` | Gera gráfico de pizza com matplotlib |
| `desenhar_cabecalho()` | Cabeçalho institucional em cada página do PDF |
| `desenhar_rodape()` | Rodapé com "Página X de Y" e nomes dos autores |
| `desenhar_cabecalho_tabela()` | Linha de cabeçalho da tabela de alunos |
| `desenhar_bloco_estatisticas()` | Bloco visual com as estatísticas da turma |
| `gerar_pdf()` | Gera o relatório completo em PDF |

---

## 📄 Conteúdo do Relatório PDF

- **Cabeçalho** — nome da instituição, turma e data/hora de geração em todas as páginas
- **Estatísticas** — total de alunos, média geral da turma, maior e menor nota, contagem de aprovados e reprovados
- **Gráfico de pizza** — proporção visual de Aprovados (verde) vs Reprovados (vermelho)
- **Tabela de alunos** — nome, média e situação com texto colorido (🟢 verde / 🔴 vermelho) e quebra de página automática
- **Rodapé** — "Página X de Y" e nomes dos desenvolvedores em todas as páginas

---

## 🐍 Requisitos

- Python 3.8+
- [fpdf2](https://pypi.org/project/fpdf2/)
- [matplotlib](https://pypi.org/project/matplotlib/)
