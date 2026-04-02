from src.agents.nova import NovaAgent
from src.agents.atlas import AtlasAgent
from src.agents.aria import AriaAgent
from src.agents.rex import RexAgent
from src.core.memory import KnowledgeHub

def main():
    print("Iniciando Esquadrão OpenClaw P&D Blockchain...")
    hub = KnowledgeHub()
    nova = NovaAgent()
    atlas = AtlasAgent()
    aria = AriaAgent()
    rex = RexAgent()
    
    topic = "Zk-Rollups"
    print(f"Buscando papers sobre: {topic}")
    raw_papers = nova.scan_arxiv(topic)
    print(f"Encontrados {len(raw_papers)} papers. Filtrando os mais relevantes...")
    filtered_papers = nova.filter_relevant_papers(raw_papers, topic)
    
    print(f"Persistindo {len(filtered_papers)} papers no Knowledge Hub...")
    for paper in filtered_papers:
        hub.add_document(
            text=f"Title: {paper['title']}\nSummary: {paper['summary']}",
            metadata={"url": paper['url'], "source": "arxiv", "topic": topic}
        )
    
    # Exemplo de fluxo para demonstrar o restante (ainda mockado nos outros agentes no Task 3)
    # No Task 4 eles serão atualizados
    # analysis = atlas.analyze_paper(filtered_papers)
    # spec = aria.write_spec(analysis)
    # print(spec)
    print("Processamento concluído.")

if __name__ == "__main__":
    main()
