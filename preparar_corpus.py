from PyPDF2 import PdfReader

meus_livros = ['romances/casaVelha.pdf', 
               'romances/domCasmurro.pdf', 
               'romances/esau.pdf', 
               'romances/helena.pdf', 
               'romances/iaia.pdf', 
               'romances/maoLuva.pdf', 
               'romances/memorial-de-aires.pdf', 
               'romances/memoriasBras.pdf', 
               'romances/quincas.pdf',
               'romances/ressurreicao.pdf']

corpus_total = ""

for livro in meus_livros:

    with open(livro, 'rb') as arquivo:
        leitor_pdf = PdfReader(arquivo)

        texto_completo = ""

        for pagina in leitor_pdf.pages:
            texto_da_pagina = pagina.extract_text()

            texto_completo += texto_da_pagina


        posicao_inicio = texto_completo.find("CAPÍTULO")

        if posicao_inicio != -1:
            
            texto_completo = texto_completo[posicao_inicio:]
        else:
            pass


        corpus_total += texto_completo


with open('obra.txt', 'w', encoding='utf-8') as arquivo:
    arquivo.write(corpus_total)