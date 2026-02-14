import re
import random

with open('obra.txt', 'r', encoding='utf-8') as arquivo:
    texto_do_arquivo = arquivo.read()

def limpeza_texto(texto_bruto):

    texto = texto_bruto
    texto = texto.lower()

    texto = re.sub(r'[.!?,\n-]', '', texto)

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


def calcular_probabilidade(context_totals, counts, historico, palavra):

    if historico not in context_totals:
        return 0


    numerador = counts[historico][palavra]
    denominador = context_totals[historico]



    p = (numerador/denominador)

    return p

        
def gerar_texto(counts, historico_atual, tamanho):


    texto_gerado = []

    for i in range(tamanho):

        if historico_atual not in counts:
            break

        candidatos = list(counts[historico_atual].keys())
        pesos = list(counts[historico_atual].values())

        proxima_palavra = random.choices(candidatos, weights=pesos)[0]

        texto_gerado.append(proxima_palavra)

        historico_atual = historico_atual[1:] + (proxima_palavra,)

    return texto_gerado




tokens = add_pading(limpeza_texto(texto_do_arquivo), 3)

meu_context_totals, meu_counts = treinar_modelo(tokens, 3)

texto_produzido = gerar_texto(meu_counts, ('<s>', '<s>'), 1000)

print("Texto gerado:", " ".join(texto_produzido))