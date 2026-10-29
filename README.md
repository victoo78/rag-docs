# 📄 Pergunte aos Documentos — RAG com Claude + ChromaDB

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-app-FF4B4B)
![ChromaDB](https://img.shields.io/badge/ChromaDB-vector%20store-orange)
![Claude](https://img.shields.io/badge/LLM-Claude-8A63D2)

Sistema de perguntas e respostas sobre PDFs (manuais, políticas internas etc.)
usando **RAG** (Retrieval-Augmented Generation): o texto dos documentos é
indexado em um **banco vetorial (ChromaDB)** e, a cada pergunta, os trechos mais
relevantes são enviados ao **Claude**, que responde citando as fontes.

O repositório inclui PDFs de exemplo de uma empresa fictícia, a **Brisa Tecnologia**
(fabricante de purificadores de ar): manual do colaborador, manual do produto e
política de segurança da informação.

## ✨ Funcionalidades

- Upload de PDFs pela interface web ou indexação pelo terminal
- Busca semântica com embeddings multilíngues (bons para português)
- Respostas em streaming, com citações numeradas `[1]`, `[2]` apontando arquivo e página
- Filtro de busca por documento
- Perguntas de acompanhamento no chat ("e para estagiários?")
- Admite quando a resposta não está nos documentos, em vez de inventar

## 🧠 Como funciona

```
 PDF ──► extração de texto ──► chunks (~900 caracteres, sobreposição de 150)
                                        │
                                        ▼
                              embeddings ──► ChromaDB (persistido em ./chroma_db)
                                                   │
 Pergunta ──► embedding ──► busca top-k por similaridade de cosseno
                                                   │
                                                   ▼
                     prompt = instruções + trechos numerados + pergunta
                                                   │
                                                   ▼
                              Claude (streaming) ──► resposta com [1], [2]...
```

## 📁 Estrutura

```
rag-docs/
├── rag.py                  # Núcleo: leitura de PDF, chunking, VectorStore (ChromaDB), RAG (busca + Claude)
├── app.py                  # Interface Streamlit: upload, filtro por documento, chat com fontes
├── cli.py                  # Uso pelo terminal (indexar, buscar, perguntar)
├── gerar_pdfs_exemplo.py   # Gera os PDFs da empresa fictícia em ./exemplos
├── exemplos/               # PDFs de exemplo
├── requirements.txt
└── .env.example            # Modelo de configuração
```

## 🚀 Instalação

Requer **Python 3.10+** e uma chave da [API da Anthropic](https://console.anthropic.com/).

```bash
git clone https://github.com/victoo78/rag-docs.git
cd rag-docs

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install sentence-transformers  # recomendado: embeddings em português

cp .env.example .env               # Windows: copy .env.example .env
# edite o .env e coloque sua ANTHROPIC_API_KEY
```

> **Sobre os embeddings:** com `sentence-transformers` instalado, o sistema usa
> automaticamente o modelo multilíngue `paraphrase-multilingual-MiniLM-L12-v2`.
> Sem ele, o ChromaDB usa o modelo padrão (`all-MiniLM-L6-v2`, treinado em inglês),
> que funciona, mas com busca menos precisa. **Se trocar de modelo, apague a pasta
> `chroma_db/`**, pois embeddings de modelos diferentes não se misturam.

## ⚙️ Configuração (`.env`)

| Variável | Padrão | Descrição |
|---|---|---|
| `ANTHROPIC_API_KEY` | — | Chave da API da Anthropic (obrigatória para gerar respostas) |
| `CLAUDE_MODEL` | `claude-sonnet-5-5` | Modelo do Claude usado nas respostas |
| `EMBED_MODEL` | multilíngue MiniLM | Modelo de embeddings (sentence-transformers) |
| `CHUNK_SIZE` | `900` | Tamanho de cada trecho, em caracteres |
| `CHUNK_OVERLAP` | `150` | Sobreposição entre trechos |
| `RAG_DB_DIR` | `./chroma_db` | Pasta do banco vetorial |
| `RAG_COLLECTION` | `documentos` | Nome da coleção no ChromaDB |

## 💻 Uso

### Interface web

```bash
streamlit run app.py
```

Abra http://localhost:8501, clique em **Carregar PDFs de exemplo** (ou envie os
seus) e pergunte, por exemplo:

- "Posso dividir minhas férias em quantas partes?"
- "O que fazer quando o purificador mostra o erro E3?"
- "Como estendo a garantia para 3 anos?"
- "Qual o limite de alimentação em viagem para Recife?"
- "Qual o salário do CEO?" → o sistema deve dizer que não encontrou.

### Terminal

```bash
python cli.py indexar exemplos/*.pdf
python cli.py listar                       # documentos indexados
python cli.py buscar "home office"         # só a busca vetorial, sem LLM
python cli.py perguntar "Quanto custa o refil do filtro?"
```

Para recriar os PDFs de exemplo: `python gerar_pdfs_exemplo.py`.

## 🛠️ Decisões de projeto

- **Resposta ancorada:** o prompt de sistema obriga o modelo a usar só os trechos
  recuperados, citar `[n]` e admitir quando não sabe, o que reduz alucinação.
- **Proteção contra prompt injection:** os trechos vão dentro de tags `<trecho>` e o
  modelo é instruído a tratá-los como dados, não como comandos.
- **Perguntas de acompanhamento:** perguntas curtas são combinadas com a pergunta
  anterior antes da busca, e as últimas trocas do chat vão junto para o modelo.
- **Reindexação idempotente:** enviar de novo um arquivo com o mesmo nome
  substitui a versão anterior no índice.
- **Filtro por documento:** marque arquivos na barra lateral para restringir a busca.

## 🔭 Limitações e próximos passos

- PDFs escaneados (imagem) não têm texto extraível; seria preciso OCR (ex.: `pytesseract`).
- Tabelas viram texto linha a linha; para documentos com muitas tabelas, vale
  usar `pdfplumber` ou um parser de layout.
- Melhorias possíveis: busca híbrida (BM25 + vetorial), reranking dos trechos e
  avaliação automática com um conjunto de perguntas e respostas esperadas.
