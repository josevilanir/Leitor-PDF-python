import fitz  # PyMuPDF

def extrair_musicas(pdf_principal, output_folder):
    with fitz.open(pdf_principal) as pdf:
        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)
            text = page.get_text()
            # Supondo que cada música está separada por uma linha de texto contendo o título da música
            musicas = text.split('Título da Música:')
            for idx, musica in enumerate(musicas[1:], start=1):
                # Extrair o título da música (primeira linha após o separador)
                titulo_musica = musica.split('Título da Música:')[0].strip()
                # Conteúdo da música é tudo que está entre o título e o próximo título (ou o final do texto)
                proximo_titulo_index = musica.find('Título da Música:', 1)
                if proximo_titulo_index != -1:
                    conteudo_musica = musica[len(titulo_musica):proximo_titulo_index].strip()
                else:
                    conteudo_musica = musica[len(titulo_musica):].strip()
                # Nome do arquivo para cada música, baseado no título da música
                nome_arquivo = f"{output_folder}/pagina_{page_num + 1}.pdf"
                # Salvar o conteúdo da música em um novo PDF separado
                with fitz.open() as nova_pagina:
                    nova_pagina.insert_pdf(pdf, from_page=page_num, to_page=page_num+len(conteudo_musica))
                    nova_pagina.save(nome_arquivo)
                # Avançar o número da página
                page_num += len(conteudo_musica.split('Título da Música:'))

# Substitua 'caminho_para_pdf_principal.pdf' pelo caminho para o seu PDF principal
# e 'caminho_para_output_folder' pelo caminho para a pasta onde você quer salvar os PDFs separados
extrair_musicas(r'C:\Users\Asus\OneDrive\Área de Trabalho\LIDER LOUVOR JVNS\PRINCIPAL.pdf', r'C:\Users\Asus\OneDrive\Área de Trabalho\LIDER LOUVOR JVNS')
