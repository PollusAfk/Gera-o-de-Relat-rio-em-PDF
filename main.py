"""
Módulo para cálculo de média, situação de alunos e geração de relatório em PDF.

Disciplina: Programação Estruturada - Atividade Avaliativa N3
Curso: Sistemas de Informação - 2º Período
Instituição: Universidade do Estado de Mato Grosso - UNEMAT
Professor: Prof. Me. Cides S. Bezerra

@Guilherme Lorrã Souza Guimarães
@Diego Da Silva Ferreira
"""

from fpdf import FPDF
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
from datetime import datetime
import os


def calcular_media(nota1, nota2):
    """Calcula a média aritmética entre duas notas.

    Args:
        nota1 (float): Primeira nota do aluno.
        nota2 (float): Segunda nota do aluno.

    Returns:
        float: Média aritmética entre nota1 e nota2.
    """
    return (nota1 + nota2) / 2


def definir_situacao(media):
    """Define a situação do aluno com base na média obtida.

    Args:
        media (float): Média final do aluno.

    Returns:
        str: 'Aprovado' se média >= 7.0, caso contrário 'Reprovado'.
    """
    if media >= 7.0:
        return "Aprovado"
    return "Reprovado"


def carregar_arquivo(arquivo_entrada):
    """Lê o arquivo de entrada contendo as notas dos alunos.

    Args:
        arquivo_entrada (str): Caminho do arquivo de entrada no formato
            'Nome;Nota1;Nota2' por linha.

    Returns:
        list[str]: Lista de linhas lidas do arquivo.
    """
    with open(arquivo_entrada, "r", encoding="utf-8") as arquivo:
        return arquivo.readlines()


def salvar_arquivo(arquivo_saida, resultados):
    """Salva os resultados processados no formato Nome;Média;Situação.

    Args:
        arquivo_saida (str): Caminho do arquivo de saída a ser gerado.
        resultados (list[str]): Lista de strings formatadas para gravação.
    """
    with open(arquivo_saida, "w", encoding="utf-8") as arquivo:
        for linha in resultados:
            arquivo.write(linha + "\n")


def processar_dados():
    """Coordena a leitura, processamento e gravação dos dados dos alunos.

    Lê o arquivo 'notas_alunos.txt', calcula média e situação de cada aluno
    e grava o resultado em 'resultado_final.txt'.
    """
    entrada = "notas_alunos.txt"
    saida = "resultado_final.txt"

    linhas = carregar_arquivo(entrada)
    resultados = []

    for linha in linhas:
        if linha.strip():
            nome, nota1, nota2 = linha.strip().split(";")
            nota1 = float(nota1)
            nota2 = float(nota2)

            media = calcular_media(nota1, nota2)
            situacao = definir_situacao(media)

            resultados.append(f"{nome};{media:.2f};{situacao}")

    salvar_arquivo(saida, resultados)


def calcular_estatisticas(arquivo_resultado):
    """Calcula as estatísticas gerais da turma a partir do arquivo de resultados.

    Args:
        arquivo_resultado (str): Caminho do arquivo com os resultados no
            formato 'Nome;Média;Situação'.

    Returns:
        dict: Dicionário com as chaves:
            - total (int): Total de alunos.
            - media_geral (float): Média geral da turma.
            - maior_nota (float): Maior média individual.
            - menor_nota (float): Menor média individual.
            - aprovados (int): Quantidade de aprovados.
            - reprovados (int): Quantidade de reprovados.
    """
    medias = []
    aprovados = 0
    reprovados = 0

    with open(arquivo_resultado, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            if linha.strip():
                _, media, situacao = linha.strip().split(";")
                medias.append(float(media))
                if situacao == "Aprovado":
                    aprovados += 1
                else:
                    reprovados += 1

    total = len(medias)
    return {
        "total": total,
        "media_geral": sum(medias) / total if total > 0 else 0,
        "maior_nota": max(medias) if medias else 0,
        "menor_nota": min(medias) if medias else 0,
        "aprovados": aprovados,
        "reprovados": reprovados,
    }


def gerar_grafico_pizza(aprovados, reprovados, caminho_imagem):
    """Gera um gráfico de pizza com a proporção de Aprovados e Reprovados.

    Utiliza a biblioteca matplotlib para criar o gráfico e salva como PNG
    para posterior inserção no PDF.

    Args:
        aprovados (int): Número de alunos aprovados.
        reprovados (int): Número de alunos reprovados.
        caminho_imagem (str): Caminho onde a imagem PNG será salva.
    """
    labels = ["Aprovados", "Reprovados"]
    valores = [aprovados, reprovados]
    cores = ["#4CAF50", "#F44336"]
    explode = (0.05, 0.05)

    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.pie(
        valores,
        labels=labels,
        colors=cores,
        explode=explode,
        autopct="%1.1f%%",
        startangle=90,
        textprops={"fontsize": 12},
    )
    ax.set_title("Aprovados vs Reprovados", fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(caminho_imagem, dpi=150, bbox_inches="tight")
    plt.close()


def desenhar_cabecalho(pdf, turma):
    """Desenha o cabeçalho institucional no topo da página atual do PDF.

    Exibe o nome da instituição, turma e a data/hora da geração do relatório.

    Args:
        pdf (FPDF): Instância do objeto FPDF em uso.
        turma (str): Identificação da turma (ex: 'Sistemas de Informação - 2º Período').
    """
    pdf.set_y(10)
    pdf.set_font("Arial", "B", 13)
    pdf.set_text_color(30, 30, 90)
    pdf.cell(0, 8, "Universidade do Estado de Mato Grosso - UNEMAT", ln=True, align="C")

    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 5, f"Turma: {turma}", ln=True, align="C")

    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    pdf.cell(0, 5, f"Gerado em: {agora}", ln=True, align="C")

    pdf.set_draw_color(30, 30, 90)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y() + 2, 200, pdf.get_y() + 2)
    pdf.ln(6)
    pdf.set_text_color(0, 0, 0)


def desenhar_rodape(pdf, pagina_atual, total_paginas):
    """Desenha o rodapé com número de página e nomes dos desenvolvedores.

    Args:
        pdf (FPDF): Instância do objeto FPDF em uso.
        pagina_atual (int): Número da página corrente.
        total_paginas (int): Total de páginas do documento.
    """
    pdf.set_y(-15)
    pdf.set_draw_color(30, 30, 90)
    pdf.set_line_width(0.3)
    pdf.line(10, pdf.get_y() - 2, 200, pdf.get_y() - 2)

    pdf.set_font("Arial", "I", 8)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5, f"Página {pagina_atual} de {total_paginas}", align="C", ln=True)
    pdf.cell(
        0,
        4,
        "Desenvolvido por: Guilherme Lorrã Souza Guimarães | Diego Da Silva Ferreira",
        align="C",
    )
    pdf.set_text_color(0, 0, 0)


def desenhar_cabecalho_tabela(pdf):
    """Desenha a linha de cabeçalho da tabela de alunos no PDF.

    Args:
        pdf (FPDF): Instância do objeto FPDF em uso.
    """
    pdf.set_font("Arial", "B", 10)
    pdf.set_fill_color(30, 30, 90)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(85, 9, "Nome", border=1, fill=True, align="C")
    pdf.cell(55, 9, "Média", border=1, fill=True, align="C")
    pdf.cell(50, 9, "Situação", border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(0, 0, 0)


def desenhar_bloco_estatisticas(pdf, stats):
    """Desenha o bloco de estatísticas gerais da turma no PDF.

    Exibe total de alunos, média geral, maior e menor nota em um bloco
    destacado antes da tabela principal.

    Args:
        pdf (FPDF): Instância do objeto FPDF em uso.
        stats (dict): Dicionário retornado por calcular_estatisticas().
    """
    pdf.set_font("Arial", "B", 11)
    pdf.set_text_color(30, 30, 90)
    pdf.cell(0, 8, "Estatísticas da Turma", ln=True)

    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_fill_color(240, 240, 250)

    largura_celula = 95

    pdf.cell(largura_celula, 8, f"  Total de alunos: {stats['total']}", border=1, fill=True)
    pdf.cell(largura_celula, 8, f"  Média geral da turma: {stats['media_geral']:.2f}", border=1, fill=True, ln=True)
    pdf.cell(largura_celula, 8, f"  Maior nota: {stats['maior_nota']:.2f}", border=1, fill=True)
    pdf.cell(largura_celula, 8, f"  Menor nota: {stats['menor_nota']:.2f}", border=1, fill=True, ln=True)
    pdf.cell(largura_celula, 8, f"  Aprovados: {stats['aprovados']}", border=1, fill=True)
    pdf.cell(largura_celula, 8, f"  Reprovados: {stats['reprovados']}", border=1, fill=True, ln=True)
    pdf.ln(6)


# ---------------------------------------------------------------------------
# Função principal de geração do PDF
# ---------------------------------------------------------------------------

def gerar_pdf():
    """Gera o relatório completo em PDF com estatísticas, gráfico e tabela de alunos.

    Lê os resultados do arquivo 'resultado_final.txt' e produz o arquivo
    'relatorio_final.pdf' contendo:
        - Cabeçalho institucional em cada página.
        - Rodapé com número de página e nomes dos desenvolvedores.
        - Bloco de estatísticas gerais da turma.
        - Gráfico de pizza de Aprovados vs Reprovados.
        - Tabela de alunos com cor condicional na situação e quebra de página manual.
    """
    ARQUIVO_RESULTADO = "resultado_final.txt"
    TURMA = "Sistemas de Informação - 2º Período"
    LINHAS_POR_PAGINA = 22
    GRAFICO_PATH = "/tmp/grafico_pizza.png"

    # --- Coleta de dados ---
    stats = calcular_estatisticas(ARQUIVO_RESULTADO)
    gerar_grafico_pizza(stats["aprovados"], stats["reprovados"], GRAFICO_PATH)

    alunos = []
    with open(ARQUIVO_RESULTADO, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            if linha.strip():
                nome, media, situacao = linha.strip().split(";")
                alunos.append((nome, media, situacao))

    # --- Pré-calcular total de páginas ---
    # Página 1: estatísticas + gráfico + primeiras linhas da tabela
    LINHAS_PAG1 = 10
    if len(alunos) <= LINHAS_PAG1:
        total_paginas = 1
    else:
        restantes = len(alunos) - LINHAS_PAG1
        total_paginas = 1 + -(-restantes // LINHAS_POR_PAGINA)  # ceil division

    # --- Montar PDF ---
    pdf = FPDF()
    pdf.set_auto_page_break(auto=False)
    pdf.add_page()

    # Página 1: cabeçalho
    desenhar_cabecalho(pdf, TURMA)

    # Título do relatório
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(30, 30, 90)
    pdf.cell(0, 10, "Relatório Final de Notas", ln=True, align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)

    # Bloco de estatísticas
    desenhar_bloco_estatisticas(pdf, stats)

    # Gráfico de pizza
    pdf.image(GRAFICO_PATH, x=55, w=100)
    pdf.ln(4)

    # Cabeçalho da tabela
    pdf.set_font("Arial", "B", 11)
    pdf.set_text_color(30, 30, 90)
    pdf.cell(0, 7, "Tabela de Alunos", ln=True)
    pdf.set_text_color(0, 0, 0)
    desenhar_cabecalho_tabela(pdf)

    # --- Linhas da tabela com quebra de página manual ---
    pagina_atual = 1
    contador_linha = 0

    for i, (nome, media, situacao) in enumerate(alunos):
        limite = LINHAS_PAG1 if pagina_atual == 1 else LINHAS_POR_PAGINA

        # Quebra de página
        if contador_linha >= limite:
            desenhar_rodape(pdf, pagina_atual, total_paginas)
            pagina_atual += 1
            pdf.add_page()
            desenhar_cabecalho(pdf, TURMA)
            pdf.set_font("Arial", "B", 11)
            pdf.set_text_color(30, 30, 90)
            pdf.cell(0, 7, "Tabela de Alunos (continuação)", ln=True)
            pdf.set_text_color(0, 0, 0)
            desenhar_cabecalho_tabela(pdf)
            contador_linha = 0

        # Cor alternada de fundo para linhas
        if contador_linha % 2 == 0:
            pdf.set_fill_color(245, 245, 255)
        else:
            pdf.set_fill_color(255, 255, 255)

        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(85, 8, nome, border=1, fill=True)
        pdf.cell(55, 8, media, border=1, fill=True, align="C")

        # Cor do texto da situação
        if situacao == "Aprovado":
            pdf.set_text_color(0, 130, 0)
        else:
            pdf.set_text_color(200, 0, 0)

        pdf.set_font("Arial", "B", 10)
        pdf.cell(50, 8, situacao, border=1, fill=True, align="C")
        pdf.ln()

        pdf.set_text_color(0, 0, 0)
        contador_linha += 1

    # Rodapé da última página
    desenhar_rodape(pdf, pagina_atual, total_paginas)

    pdf.output("relatorio_final.pdf")
    print("PDF gerado: relatorio_final.pdf")

    # Limpar imagem temporária
    if os.path.exists(GRAFICO_PATH):
        os.remove(GRAFICO_PATH)


# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    processar_dados()
    gerar_pdf()