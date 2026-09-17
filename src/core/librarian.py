import os
import hashlib
from datetime import datetime

import chromadb


class Librarian:
    """
    Wrapper unificado sobre ChromaDB com suporte a:
    - Coleção mestre (research_master) + coleções por sessão
    - Busca semântica
    - Exportação para Obsidian

    Substitui o KnowledgeHub original.
    """

    def __init__(self, collection_name: str = "research_master", obsidian_path: str | None = None):
        db_path = os.getenv("DB_PATH", "./data/chroma")
        if not os.path.isabs(db_path):
            db_path = os.path.abspath(db_path)

        os.makedirs(db_path, exist_ok=True)

        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.obsidian_path = obsidian_path or os.getenv("OBSIDIAN_PATH", "")

    # ---- Escrita ----

    def add_paper(self, text: str, metadata: dict) -> str:
        """Adiciona um paper ao banco. Retorna o ID."""
        doc_id = hashlib.sha256(text.encode()).hexdigest()[:16]
        self.collection.add(
            documents=[text],
            metadatas=[{**metadata, "stored_at": datetime.now().isoformat()}],
            ids=[doc_id],
        )
        return doc_id

    def add_papers(self, papers: list[dict]) -> list[str]:
        """Adiciona múltiplos papers de uma vez."""
        ids = []
        for p in papers:
            text = f"Title: {p.get('title', '')}\nSummary: {p.get('summary', p.get('abstract', ''))}"
            meta = {
                "url": p.get("url", ""),
                "doi": p.get("doi", ""),
                "source": p.get("source", "unknown"),
                "topic": p.get("topic", ""),
                "relevance_score": p.get("Relevance_Score", 0),
                "year": p.get("year", ""),
                "citations": p.get("citations", 0),
                "authors": p.get("authors", ""),
            }
            ids.append(self.add_paper(text, meta))
        return ids

    # ---- Leitura ----

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """Busca semântica no ChromaDB."""
        results = self.collection.query(query_texts=[query], n_results=top_k)

        docs = []
        for i, doc in enumerate(results["documents"][0]):
            docs.append({
                "text": doc,
                "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                "id": results["ids"][0][i],
                "distance": results["distances"][0][i] if results.get("distances") else None,
            })
        return docs

    def count(self) -> int:
        return self.collection.count()

    # ---- Obsidian ----

    def export_to_obsidian(self, topic: str, content: str, tags: list[str] | None = None) -> str | None:
        """
        Exporta um relatório para o vault Obsidian.
        Retorna o caminho do arquivo criado, ou None se não configurado.
        """
        if not self.obsidian_path:
            return None

        vault_path = os.path.join(self.obsidian_path, "Research_Squad")
        os.makedirs(vault_path, exist_ok=True)

        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{date_str} - {topic.replace('/', '-')}.md"
        filepath = os.path.join(vault_path, filename)

        tag_line = ""
        if tags:
            tag_line = " ".join(f"#{t}" for t in tags) + "\n\n"

        with open(filepath, "w") as f:
            f.write(f"# {topic}\n\n")
            f.write(tag_line)
            f.write(content)

        return filepath

    # ---- Estatísticas ----

    def stats(self) -> dict:
        return {
            "collection": self.collection.name,
            "total_docs": self.count(),
            "obsidian_path": self.obsidian_path or "not configured",
        }
