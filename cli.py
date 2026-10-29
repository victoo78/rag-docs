"""
Uso pelo terminal:
  python cli.py indexar arquivo1.pdf arquivo2.pdf
  python cli.py perguntar "sua pergunta"
  python cli.py buscar "termo"          (só busca vetorial, sem chamar o modelo)
  python cli.py listar
"""

import sys

from rag import RAG, VectorStore


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    cmd, args = sys.argv[1], sys.argv[2:]
    store = VectorStore()

    if cmd == "indexar":
        for path in args:
            print(f"{path}: {store.add_file(path)} trechos")
    elif cmd == "listar":
        for name, n in store.sources().items():
            print(f"{n:5d}  {name}")
    elif cmd == "buscar":
        for h in store.search(" ".join(args), k=5):
            print(f"\n[{h['score']:.2f}] {h['source']} p.{h['page']}\n  {h['text'][:250]}...")
    elif cmd == "perguntar":
        rag = RAG(store)
        q = " ".join(args)
        hits = rag.retrieve(q)
        for piece in rag.answer_stream(q, hits):
            print(piece, end="", flush=True)
        print("\n\nFontes:")
        for i, h in enumerate(hits, 1):
            print(f"  [{i}] {h['source']} p.{h['page']} (similaridade {h['score']:.2f})")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
