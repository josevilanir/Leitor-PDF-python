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
                # Nome do arquivo genérico para cada página, com base no número da página
                nome_arquivo_generico = f"{output_folder}/pagina_{page_num + 1}.pdf"
                # Salvar a página em um novo PDF separado
                with fitz.open() as nova_pagina:
                    nova_pagina.insert_pdf(pdf, from_page=page_num, to_page=page_num)
                    nova_pagina.save(nome_arquivo_generico)

# Substitua 'caminho_para_pdf_principal.pdf' pelo caminho para o seu PDF principal
# e 'caminho_para_output_folder' pelo caminho para a pasta onde você quer salvar os PDFs separados
extrair_musicas(r'C:\Users\Asus\OneDrive\Área de Trabalho\LIDER LOUVOR JVNS\PRINCIPAL.pdf', r'C:\Users\Asus\OneDrive\Área de Trabalho\LIDER LOUVOR JVNS')

