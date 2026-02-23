import re
import random

# ==========================================
# 1. LEITURA DO ARQUIVO
# ==========================================

# Abre o arquivo 'obra.txt' que contém todos os 8 livros unificados
with open('obra.txt', 'r', encoding='utf-8') as arquivo:
    texto_do_arquivo = arquivo.read()


# ==========================================
# 2. LIMPEZA E TOKENIZAÇÃO
# ==========================================

# Esta função padroniza o texto, remove pontuação e trata as 
# particularidades de formatação do Project Gutenberg (como '--' e '_').
def limpeza_texto(texto_bruto):
    texto = texto_bruto.lower()
    texto = re.sub(r'[\n\t]', ' ', texto)
    texto = texto.replace('--', ' ')
    texto = re.sub(r'_', '', texto)
    texto = re.sub(r'[.!?,;:"\'()\[\]\-]', ' ', texto)
    tokens = texto.split()
    return tokens

# Adiciona os tokens artificiais de início ('<s>') baseando-se no valor de N
def add_pading(string, n):
    token = string
    for i in range(n-1):
        token = ['<s>'] + token
    return token


# ==========================================
# 3. TREINAMENTO DO MODELO (N-GRAMA)
# ==========================================

# Percorre a lista de tokens e conta as ocorrências de cada histórico 
# e de cada palavra que se segue a esse histórico.
def treinar_modelo(token, n):
    context_totals = {}
    counts = {}

    for i in range(len(token) - n + 1):
        janela = token[i:i+n]
        historico = janela[0:len(janela) - 1]
        palavra = janela[-1]
        
        chave_historico = tuple(historico)

        # 1. Conta quantas vezes este histórico (contexto) apareceu no total
        if chave_historico in context_totals:
            context_totals[chave_historico] += 1
        else:
            context_totals[chave_historico] = 1
    
        # 2. Conta quantas vezes a 'palavra' apareceu especificamente após este histórico
        if chave_historico not in counts:
            counts[chave_historico] = {}

        if palavra in counts[chave_historico]:
            counts[chave_historico][palavra] += 1
        else:
            counts[chave_historico][palavra] = 1

    return context_totals, counts


# ==========================================
# 4. CÁLCULO DE PROBABILIDADE
# ==========================================

# Aplica a fórmula matemática do N-Grama de forma explícita: 
def calcular_probabilidade(context_totals, counts, historico, palavra):
    if historico not in context_totals:
        return 0

    numerador = counts[historico][palavra]
    denominador = context_totals[historico]

    p = (numerador / denominador)
    return p


# ==========================================
# 5. GERAÇÃO DE TEXTO
# ==========================================

# Utiliza as probabilidades calculadas para prever e sortear as próximas palavras
def gerar_texto(context_totals, counts, historico_inicial, tamanho):
    texto_gerado = []
    historico_atual = historico_inicial

    for i in range(tamanho):
        
        # Se o histórico atual nunca foi visto nos livros, paramos a geração
        if historico_atual not in counts:
            break

        candidatos = list(counts[historico_atual].keys())
        pesos = [] 

        # Para cada palavra candidata, calculamos explicitamente a probabilidade
        for palavra in candidatos:
            prob = calcular_probabilidade(context_totals, counts, historico_atual, palavra)
            pesos.append(prob)

        # Sorteia a próxima palavra baseando-se nas probabilidades (pesos)
        proxima_palavra = random.choices(candidatos, weights=pesos)[0]

        texto_gerado.append(proxima_palavra)

        # Atualiza a janela do histórico deslizando uma posição para a direita
        historico_atual = historico_atual[1:] + (proxima_palavra,)

    return texto_gerado


# ==========================================
# 6. EXECUÇÃO PRINCIPAL
# ==========================================

# Definimos N
N = 4

# Preparamos os dados
tokens = add_pading(limpeza_texto(texto_do_arquivo), N)

# Treinamos o modelo extraindo as contagens
meu_context_totals, meu_counts = treinar_modelo(tokens, N)

# Definimos o ponto de partida dinâmico de acordo com o N
historico_inicial = tuple(['<s>'] * (N - 1))

# Geramos 1000 palavras
texto_produzido = gerar_texto(meu_context_totals, meu_counts, historico_inicial, 1000)

print("Texto gerado:", " ".join(texto_produzido))