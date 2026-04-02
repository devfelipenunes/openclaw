from src.agents.nova import NovaAgent
from src.agents.atlas import AtlasAgent
from src.agents.aria import AriaAgent
from src.agents.rex import RexAgent

def main():
    print("Iniciando Esquadrão OpenClaw P&D Blockchain...")
    nova = NovaAgent()
    atlas = AtlasAgent()
    aria = AriaAgent()
    rex = RexAgent()
    
    # Exemplo de fluxo
    discovery = nova.scan_arxiv("Zk-Rollups")
    analysis = atlas.analyze_paper(discovery)
    spec = aria.write_spec(analysis)
    
    print(spec)
    print(rex.watch_github("ethereum/EIPs"))

if __name__ == "__main__":
    main()
