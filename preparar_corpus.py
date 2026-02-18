import os

meus_livros = [
    'romances_project_gutemberg/domcasmurro.txt',
    'romances_project_gutemberg/esaujaco.txt',
    'romances_project_gutemberg/helena.txt',
    'romances_project_gutemberg/iaia.txt',
    'romances_project_gutemberg/maoluva.txt',
    'romances_project_gutemberg/memorialayres.txt',
    'romances_project_gutemberg/memoriaspostumas.txt',
    'romances_project_gutemberg/quincasborba.txt'
]

corpus_total = ""

print("Iniciando a unificação dos livros...")

for livro in meus_livros:

    try:

        with open(livro, 'r', encoding='utf-8') as arquivo:

            texto = arquivo.read()

            corpus_total += texto
            corpus_total += "\n\n\n"

            print(f"Livro '{livro}' adicionado com sucesso!")

    except FileNotFoundError:
        print(f"O arquivo '{livro}' não foi encontrado na pasta.")


with open('obra.txt', 'w', encoding='utf-8') as arquivo_final:
    arquivo_final.write(corpus_total)



print(f"\nO arquivo 'obra.txt' foi criado")