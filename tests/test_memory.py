from src.core.memory import KnowledgeHub

def test_knowledge_persistence():
    hub = KnowledgeHub(collection_name="test_rd")
    hub.add_document("Ethereum EIP-1559 introduces a base fee.", {"source": "eip-1559"})
    results = hub.search("base fee")
    assert len(results) > 0
    assert "EIP-1559" in results[0]
