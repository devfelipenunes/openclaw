from src.agents.nova import NovaAgent
from src.agents.atlas import AtlasAgent
from src.agents.aria import AriaAgent
from src.core.memory import KnowledgeHub
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    print("=== OpenClaw: Blockchain R&D Squadron ===")
    
    hub = KnowledgeHub()
    nova = NovaAgent()
    atlas = AtlasAgent()
    aria = AriaAgent()
    
    topic = "Zk-Rollups"
    print(f"[*] Task (Nova): Scanning arXiv for {topic}...")
    
    raw_papers = nova.scan_arxiv(topic)
    print(f"[*] Task (Nova): Found {len(raw_papers)} papers. Filtering for relevance...")
    
    filtered_papers = nova.filter_relevant_papers(raw_papers, topic)
    print(f"[*] Task (Memory): Persistence of {len(filtered_papers)} papers...")
    
    for paper in filtered_papers:
        hub.add_document(
            text=f"Title: {paper['title']}\nSummary: {paper['summary']}",
            metadata={"url": paper['url'], "source": "arxiv", "topic": topic}
        )
    
    print(f"[*] Task (Atlas): Analyzing architectural insights from RAG context...")
    context = hub.search(topic, n_results=3)
    analysis = atlas.analyze_papers(context)
    
    print(f"[*] Task (Aria): Generating technical implementation specification...")
    spec = aria.write_spec(analysis, topic)
    
    print("\n" + "="*50)
    print(f"FINAL SPECIFICATION FOR: {topic}")
    print("="*50)
    print(spec)
    print("="*50)
    print("\n[✔] Process complete.")

if __name__ == "__main__":
    main()
