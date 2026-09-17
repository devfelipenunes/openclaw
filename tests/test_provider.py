import os
from src.core.provider import ProviderManager


def test_provider_routing_defaults():
    """Test that the default model values are correctly returned."""
    for key in ["MODEL_SCAN", "MODEL_ANALYZE", "MODEL_DEBATE", "MODEL_REVIEW", "MODEL_WRITE"]:
        os.environ.pop(key, None)
    os.environ.pop("LLM_API_KEY", None)

    pm = ProviderManager()
    assert pm.get_model("scan") == "deepseek-chat"
    assert pm.get_model("analyze") == "deepseek-chat"
    assert pm.get_model("debate") == "deepseek-chat"
    assert pm.get_model("review") == "deepseek-chat"
    assert pm.get_model("write") == "deepseek-chat"


def test_provider_routing_env_override():
    """Test that model values can be overridden by environment variables."""
    os.environ["MODEL_SCAN"] = "deepseek-custom-scan"
    os.environ["MODEL_ANALYZE"] = "deepseek-custom-analyze"

    pm = ProviderManager()
    assert pm.get_model("scan") == "deepseek-custom-scan"
    assert pm.get_model("analyze") == "deepseek-custom-analyze"

    del os.environ["MODEL_SCAN"]
    del os.environ["MODEL_ANALYZE"]


def test_provider_routing_fallback():
    """Test that an unknown task type falls back to the default."""
    pm = ProviderManager()
    assert pm.get_model("unknown_task") == "deepseek-chat"


def test_provider_base_url_default():
    """Test that default base_url points to DeepSeek."""
    pm = ProviderManager()
    assert "deepseek" in pm.get_base_url()
