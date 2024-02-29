import PyPDF2

def extrair_musicas(pdf_principal, output_folder):
    with open(pdf_principal, 'rb') as principal_file:
        reader = PyPDF2.PdfReader(principal_file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            # Supondo que cada música está separada por uma linha de texto contendo o título da música
            musicas = text.split('TITULA DA MÚSICA')
            for idx, musica in enumerate(musicas[1:], start=1):
                nome_musica = f"{output_folder}/musica_{idx}.pdf"
                with open(nome_musica, 'wb') as output_file:
                    writer = PyPDF2.PdfWriter()
                    nova_pagina = writer.add_blank_page(width=page.width, height=page.height)
                    nova_pagina.merge_page(page)
                    writer.write(output_file)


extrair_musicas(r'C:\Users\Asus\OneDrive\Área de Trabalho\LIDER LOUVOR JVNS\PRINCIPAL.pdf', r'C:\Users\Asus\OneDrive\Área de Trabalho\LIDER LOUVOR JVNS')
