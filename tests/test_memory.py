from src.core.librarian import Librarian


def test_librarian_persistence():
    lib = Librarian(collection_name="test_research")
    lib.add_paper("Ethereum EIP-1559 introduces a base fee.", {"source": "eip-1559"})
    results = lib.search("base fee")
    assert len(results) > 0
    assert "EIP-1559" in results[0]["text"]
