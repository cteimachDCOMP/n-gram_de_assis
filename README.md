# 🎩 Gerador de Textos - Machado de Assis (Modelo N-Grama)

**Desenvolvedor:** Cauan Teixeira Machado  
**Revisor:** João Felipe Quentino  

## 📖 Sobre o Projeto
Este projeto implementa um modelo de Inteligência Artificial baseado em **N-Gramas** capaz de gerar textos simulando o estilo literário do aclamado autor brasileiro Machado de Assis. 

O modelo foi treinado com um corpus composto por 8 obras clássicas extraídas do *Project Gutenberg*. Através da análise estatística das palavras e de amostragem inteligente, a aplicação consegue criar "fanfics" inéditas, misturando personagens e cenários de diferentes livros.

**Nota:** Todo o material literário utilizado para o treinamento deste modelo encontra-se em **domínio público**.

## ✨ Funcionalidades e Engenharia da IA

**Nota Importante de Arquitetura:** Para fins de avaliação acadêmica, o arquivo `codigo_fonte.py` foi mantido o mais fiel possível ao pseudocódigo fornecido no roteiro original da disciplina. As melhorias avançadas de amostragem e dinamismo foram implementadas exclusivamente na interface gráfica (`app.py`).

* **Limpeza de Dados Customizada:** O script trata particularidades do formato Gutenberg, convertendo marcações de itálico (`_`) e travessões duplos (`--`) para evitar ruídos na geração, além de tratar quebras de linha para não fundir palavras.
* **Cálculo Explícito de Probabilidades (Ambos):** A matemática estocástica foi implementada de forma transparente, calculando a probabilidade de uma palavra baseada no seu contexto:  
  $P(palavra|historico) = \frac{Contagem(historico + palavra)}{Contagem(historico)}$
* **Top-K (Apenas no app.py):** Para evitar que o modelo escolhesse palavras com probabilidade ínfima (o que gerava frases sem sentido), o algoritmo ordena as candidatas e sorteia apenas entre as 4 mais prováveis. Isso garante o equilíbrio perfeito entre **coerência** e **criatividade**.
* **Início Aleatório Dinâmico (Apenas no app.py):** Para evitar que o modelo começasse sempre a copiar as primeiras palavras do corpus, a aplicação web sorteia um contexto (`histórico`) aleatório de dentro da obra completa para dar o pontapé inicial na história.
* **Interface Web com Streamlit:** Uma interface amigável onde o usuário pode testar diferentes valores do N-Grama e definir o tamanho do texto gerado.

## 🧠 O Dilema do N (Overfitting vs. Underfitting)
O tamanho da "janela" de contexto afeta diretamente o resultado:

* **Valores Baixos (Sub-ajuste / Underfitting):** O modelo torna-se extremamente criativo, mas perde a coerência gramatical e o sentido lógico muito rapidamente, resultando em textos caóticos.
* **Valores Altos (Sobre-ajuste / Overfitting):** O modelo "decora" os dados de treino. Como o contexto exigido é muito longo e específico, ele perde o poder de escolha e limita-se a copiar trechos idênticos aos livros originais (plágio), perdendo a originalidade.
* **O Ponto Ideal (Generalização):** Encontra-se num valor intermediário onde o modelo aprende a estrutura gramatical do autor, ganhando a capacidade de **intertextualidade** — conseguindo misturar elementos de livros diferentes numa mesma frase perfeitamente estruturada.

## 📂 Estrutura dos Arquivos e Pastas

### Bases de Dados
* **`romances_pdfs/`**: Pasta que contém os livros originais em formato `.pdf`. Inicialmente, houve uma tentativa de extrair os textos utilizando a biblioteca `PyPDF2`. No entanto, essa abordagem foi descartada por não ter obtido muito sucesso, apresentando problemas com a formatação e a leitura de certos caracteres.
* **`romances_project_gutemberg/`**: Pasta definitiva contendo os textos dos 8 livros em formato `.txt` (com codificação UTF-8), extraídos diretamente do *Project Gutenberg*. Esta abordagem garantiu uma leitura limpa e padronizada para o treinamento da IA.

### Scripts Python
* **`preparar_corpus.py`**: Script de pré-processamento. Lê os arquivos `.txt` originais e os unifica num único arquivo gigante, inserindo quebras de linha entre eles para evitar vazamento de contexto entre o final de um livro e o começo de outro.
* **`codigo_fonte.py`**: O "motor" base do projeto. Contém as funções puras e foi construído seguindo estritamente a lógica do pseudocódigo acadêmico.
* **`app.py`**: A interface gráfica construída em Streamlit. Importa a lógica do N-Grama e expande-a com melhorias de PLN (Top-K e Sorteio Dinâmico) para interação robusta em tempo real no navegador.

### Arquivos Gerados
* **`obra.txt`**: Arquivo gerado automaticamente pelo `preparar_corpus.py` que serve de base de conhecimento unificada (Corpus) para o modelo.

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos
Certifique-se de ter o Python 3 instalado. Instale a biblioteca do Streamlit executando o comando abaixo no seu terminal:
```bash
pip install streamlit
```

### 2. Preparar os Dados
Antes de rodar a IA, é necessário compilar os livros. Certifique-se de que os textos `.txt` estão na pasta `romances_project_gutemberg/` e execute:
```bash
python3 preparar_corpus.py
```
*Isso irá gerar o arquivo `obra.txt` na raiz do projeto.*

### 3. Rodar a Interface Web (Recomendado)
Para abrir a aplicação gráfica no seu navegador com todas as melhorias de IA, execute:
```bash
streamlit run app.py
```

### 4. Rodar via Terminal
Se preferir testar a geração de texto base diretamente no terminal (sem as implementações do Streamlit), execute:
```bash
python3 codigo_fonte.py
```

***
*Desenvolvido como projeto acadêmico para a disciplina de Inteligência Artificial.*
