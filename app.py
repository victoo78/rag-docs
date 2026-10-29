"""
Interface Streamlit do "Pergunte aos Documentos".
Rode com:  streamlit run app.py
"""

import os
import tempfile
from pathlib import Path

import streamlit as st

from rag import RAG, VectorStore, CLAUDE_MODEL

st.set_page_config(page_title="Pergunte aos Documentos", page_icon="📄", layout="wide")

EXEMPLOS = Path(__file__).parent / "exemplos"


@st.cache_resource(show_spinner="Carregando banco vetorial e modelo de embeddings...")
def get_rag():
    return RAG(VectorStore())


rag = get_rag()

# ---------------------------------------------------------------------------
# Barra lateral: configuração e documentos
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuração")
    if not os.getenv("ANTHROPIC_API_KEY"):
        key = st.text_input("Chave da API Anthropic", type="password",
                            help="Também pode ser definida no arquivo .env")
        if key:
            os.environ["ANTHROPIC_API_KEY"] = key
            rag._client = None
    else:
        st.success("Chave da API configurada", icon="🔑")

    rag.model = st.text_input("Modelo", value=rag.model or CLAUDE_MODEL)
    top_k = st.slider("Trechos recuperados (k)", 1, 10, 5)

    st.divider()
    st.header("📚 Documentos")

    uploads = st.file_uploader("Adicionar PDFs", type=["pdf", "txt", "md"],
                               accept_multiple_files=True)
    if uploads and st.button("Indexar arquivos", type="primary", use_container_width=True):
        with st.spinner("Lendo, dividindo e gerando embeddings..."):
            for up in uploads:
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(up.name).suffix) as tmp:
                    tmp.write(up.getbuffer())
                n = rag.store.add_file(tmp.name, display_name=up.name)
                os.unlink(tmp.name)
                st.toast(f"{up.name}: {n} trechos indexados")
        st.rerun()

    if EXEMPLOS.exists() and any(EXEMPLOS.glob("*.pdf")):
        if st.button("Carregar PDFs de exemplo (Brisa Tecnologia)", use_container_width=True):
            with st.spinner("Indexando exemplos..."):
                for pdf in sorted(EXEMPLOS.glob("*.pdf")):
                    rag.store.add_file(pdf)
            st.rerun()

    sources = rag.store.sources()
    if sources:
        st.caption("Indexados — marque para filtrar a busca (vazio = todos):")
        selected = []
        for name, n in sources.items():
            c1, c2 = st.columns([5, 1])
            if c1.checkbox(f"{name} · {n} trechos", key=f"src_{name}"):
                selected.append(name)
            if c2.button("🗑️", key=f"del_{name}", help="Remover do índice"):
                rag.store.delete_source(name)
                st.rerun()
        if st.button("Limpar índice inteiro", use_container_width=True):
            rag.store.reset()
            st.session_state.messages = []
            st.rerun()
    else:
        selected = []
        st.info("Nenhum documento indexado ainda.")

    if st.button("Nova conversa", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---------------------------------------------------------------------------
# Área principal: chat
# ---------------------------------------------------------------------------
st.title("📄 Pergunte aos Documentos")
st.caption("RAG com ChromaDB (banco vetorial) + Claude. As respostas citam os trechos usados como [n].")

if "messages" not in st.session_state:
    st.session_state.messages = []


def show_sources(hits):
    with st.expander(f"Fontes ({len(hits)} trechos)"):
        for i, h in enumerate(hits, start=1):
            st.markdown(f"**[{i}] {h['source']} — p. {h['page']}** · similaridade {h['score']:.2f}")
            st.caption(h["text"][:700] + ("…" if len(h["text"]) > 700 else ""))


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            show_sources(msg["sources"])

if not st.session_state.messages and sources:
    st.markdown("**Sugestões para os PDFs de exemplo:**")
    cols = st.columns(3)
    sugestoes = [
        "Posso dividir minhas férias em quantas partes?",
        "O que significa o erro E3 no purificador?",
        "Quanto é o auxílio home office e quem recebe?",
    ]
    for col, s in zip(cols, sugestoes):
        if col.button(s, use_container_width=True):
            st.session_state.pending = s
            st.rerun()

question = st.chat_input("Faça uma pergunta sobre os documentos...")
question = question or st.session_state.pop("pending", None)

if question:
    history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        hits = rag.retrieve(question, k=top_k, sources=selected or None, history=history)
        try:
            answer = st.write_stream(rag.answer_stream(question, hits, history))
        except Exception as e:  # chave ausente, modelo inválido, rede etc.
            answer = f"⚠️ Erro ao chamar o modelo: {e}"
            st.error(answer)
        if hits:
            show_sources(hits)
    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": hits})
