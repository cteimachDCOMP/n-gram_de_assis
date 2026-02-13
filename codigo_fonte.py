import re

txt = "Olha, Bentinho! Que olhos de cigana oblíqua e dissimulada."

def limpeza_texto(texto_bruto):

    texto = texto_bruto
    texto = texto.lower()

    texto = re.sub(r'[.!?,]', '', texto)

    texto = texto.split()

    return texto



def add_pading(string, n):

    token = string

    for i in range(n-1):
        token = ['<s>'] + token

    return token



def treinar_modelo(token, n):

    context_totals = {}
    counts = {}

    for i in range(len(token) - n + 1):

        janela = token[i:i+n]
        historico = janela[0:len(janela) - 1]
        palavra = janela[-1]
        


        chave_historico = tuple(historico)

        if chave_historico in context_totals:
            context_totals[chave_historico] += 1

        else:
            context_totals[chave_historico] = 1
    

        if chave_historico not in counts:
            counts[chave_historico] = {}

        if palavra in counts[chave_historico]:
            counts[chave_historico][palavra] += 1
        
        else:
            counts[chave_historico][palavra] = 1

            

    return context_totals, counts

        



print(treinar_modelo(add_pading(limpeza_texto(txt), 3), 3))