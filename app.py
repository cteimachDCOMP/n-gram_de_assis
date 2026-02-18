import streamlit as st
import re
import random

def limpeza_texto(texto_bruto):
    texto = texto_bruto.lower()
    texto = re.sub(r'[\n\t]', ' ', texto)
    texto = texto.replace('--', ' ')
    texto = re.sub(r'_', '', texto)
    texto = re.sub(r'[.!?,;:"\'()\[\]\-]', ' ', texto)
    tokens = texto.split()
    return tokens

def add_pading(tokens, n):
    return ['<s>'] * (n - 1) + tokens

def treinar_modelo(tokens, n):
    context_totals = {}
    counts = {}

    for i in range(len(tokens) - n + 1):
        janela = tokens[i:i+n]
        historico = tuple(janela[:-1])
        palavra = janela[-1]

        if historico in context_totals:
            context_totals[historico] += 1
        else:
            context_totals[historico] = 1

        if historico not in counts:
            counts[historico] = {}
        
        if palavra in counts[historico]:
            counts[historico][palavra] += 1
        else:
            counts[historico][palavra] = 1

    return context_totals, counts

def gerar_texto(counts, historico_inicial, tamanho):
    texto_gerado = []
    historico_atual = historico_inicial

    for _ in range(tamanho):
        if historico_atual not in counts:
            break

        melhores = sorted(counts[historico_atual].items(), key= lambda x: x[1], reverse=True)
        melhores = melhores[:4]

        candidatos = list()
        pesos = list()

        for tupla in melhores:
             candidatos.append(tupla[0])

        
        for tupla in melhores:
             pesos.append(tupla[1])


        proxima_palavra = random.choices(candidatos, weights=pesos)[0]

        texto_gerado.append(proxima_palavra)
        historico_atual = historico_atual[1:] + (proxima_palavra,)

    return texto_gerado



# Interface Gráfica

st.title("Gerador de Textos - Machado de Assis")
st.markdown("Esta aplicação utiliza **N-Gramas** para gerar textos baseados no estilo de Machado de Assis.")

st.sidebar.header("Configurações")

n_escolhido = st.sidebar.slider(
    "Nível de Coerência (N)",
    min_value=2,
    max_value=10,
    value=4,
    help="Valores baixos são mais criativos. Valores altos copiam mais o original."
)

tamanho_texto = st.sidebar.slider(
    "Quantidade de Palavras",
    min_value=50,
    max_value=10000,
    value=200
)


st.write("### O que o modelo vai escrever hoje?")


if st.button("🖊️ Escrever Fanfic"):
    
    
    with st.spinner('A ler os livros e a treinar o modelo...'):
        
        
        try:
            with open('obra.txt', 'r', encoding='utf-8') as arquivo:
                texto_do_arquivo = arquivo.read()
            
            tokens = limpeza_texto(texto_do_arquivo)
            
            
            tokens_pad = add_pading(tokens, n_escolhido)
            context_totals, counts = treinar_modelo(tokens_pad, n_escolhido)
            
            
            
            historico_inicial = tuple(['<s>'] * (n_escolhido - 1))
            
            texto_gerado = gerar_texto(counts, historico_inicial, tamanho_texto)
            
            
            resultado_final = " ".join(texto_gerado)
            
            st.success("Texto gerado com sucesso!")
            st.markdown(f"> *{resultado_final}*")
            
        except FileNotFoundError:
            st.error("Erro: O arquivo 'obra.txt' não foi encontrado. Certifique-se de que ele está na mesma pasta.")