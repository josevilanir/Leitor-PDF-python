from flask import Flask, request, render_template
import fitz  # PyMuPDF
import os
import re
import webbrowser

app = Flask(__name__, template_folder='templates')


def limpar_nome(nome):
    # Remover caracteres especiais do nome do arquivo
    return re.sub(r'[^\w\s]', '', nome)

def extrair_musicas(pdf_principal, output_folder):
    with fitz.open(pdf_principal) as pdf:
        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)
            text = page.get_text()
            # Supondo que cada música está separada por uma linha de texto contendo o título da música
            musicas = text.split('Título da Música:')
            for idx, musica in enumerate(musicas[1:], start=1):
                # Encontrar o índice da próxima música ou o final do texto
                proximo_titulo_index = text.find('Título da Música:', text.find('Título da Música:') + 1)
                if proximo_titulo_index == -1:
                    proximo_titulo_index = len(text)
                # Conteúdo da música é tudo entre o título e o próximo título
                conteudo_musica = musica[:proximo_titulo_index].strip()
                # Encontrar o nome da música
                linhas = musica.strip().split('\n')
                nome_musica = limpar_nome(linhas[0].strip()) if linhas else f"musica_{page_num}_{idx}"
                # Nome do arquivo para cada música, com base no nome da música
                nome_arquivo = f"{output_folder}/{nome_musica}.pdf"
                # Criar um novo PDF com todas as páginas da música
                with fitz.open() as novo_pdf:
                    # Adicionar a página atual ao novo PDF
                    novo_pdf.insert_pdf(pdf, from_page=page_num, to_page=page_num)
                    # Adicionar páginas subsequentes até encontrar a próxima música
                    proxima_pagina = page_num + 1
                    while proxima_pagina < len(pdf):
                        proxima_page = pdf.load_page(proxima_pagina)
                        proximo_texto = proxima_page.get_text()
                        if 'Título da Música:' in proximo_texto:
                            break
                        novo_pdf.insert_pdf(pdf, from_page=proxima_pagina, to_page=proxima_pagina)
                        proxima_pagina += 1
                    # Salvar o novo PDF com todas as páginas da música
                    novo_pdf.save(nome_arquivo)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extrair_musicas', methods=['POST'])
def extrair_musicas_route():
    pdf_file = request.files['pdf_file']
    if pdf_file:
        pdf_file.save('temp.pdf')  # Salvando temporariamente o arquivo enviado
        output_folder = os.path.join(os.getcwd(), 'output')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        extrair_musicas('temp.pdf', output_folder)
        os.remove('temp.pdf')  # Removendo o arquivo temporário
        return 'Músicas extraídas com sucesso!'
    else:
        return 'Nenhum arquivo PDF foi enviado.'


if __name__ == "__main__":
    # Abrir o navegador com a página HTML apenas se o script for executado diretamente
    webbrowser.open('http://localhost:5000')

    # Iniciar o servidor Flask
    app.run(debug=True)
