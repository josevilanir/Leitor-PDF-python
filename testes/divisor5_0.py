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
                titulo_musica = musica.split('\n')[0].strip()
                # Encontrar o índice da próxima música ou o final do texto
                proximo_titulo_index = text.find('Título da Música:', text.find('Título da Música:') + 1)
                if proximo_titulo_index == -1:
                    proximo_titulo_index = len(text)
                # Conteúdo da música é tudo entre o título e o próximo título
                conteudo_musica = musica[:proximo_titulo_index].strip()
                # Nome do arquivo genérico para cada música, com base no número da página
                nome_arquivo_generico = f"{output_folder}/pagina_{page_num + 1}.pdf"
                # Salvar a música em um novo PDF separado
                with fitz.open() as nova_pagina:
                    nova_pagina.insert_pdf(pdf, from_page=page_num, to_page=page_num)
                    nova_pagina.save(nome_arquivo_generico)


extrair_musicas(r'C:\Users\Asus\OneDrive\Área de Trabalho\LIDER LOUVOR JVNS\PRINCIPAL.pdf', r'C:\Users\Asus\OneDrive\Área de Trabalho\LIDER LOUVOR JVNS')
