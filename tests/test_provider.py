import os
from src.core.provider import ProviderManager

def test_provider_routing_defaults():
    """Test that the default model values are correctly returned."""
    # Ensure environment variables are not interfering with defaults
    if "MODEL_SCAN" in os.environ:
        del os.environ["MODEL_SCAN"]
    if "MODEL_ANALYZE" in os.environ:
        del os.environ["MODEL_ANALYZE"]

    pm = ProviderManager()
    assert pm.get_model("scan") == "gpt-4o-mini"
    assert pm.get_model("analyze") == "gpt-4o"

def test_provider_routing_env_override():
    """Test that model values can be overridden by environment variables."""
    os.environ["MODEL_SCAN"] = "custom-scan-model"
    os.environ["MODEL_ANALYZE"] = "custom-analyze-model"

    pm = ProviderManager()
    assert pm.get_model("scan") == "custom-scan-model"
    assert pm.get_model("analyze") == "custom-analyze-model"

    # Cleanup environment
    del os.environ["MODEL_SCAN"]
    del os.environ["MODEL_ANALYZE"]

def test_provider_routing_fallback():
    """Test that an unknown task type falls back to the default scan model."""
    pm = ProviderManager()
    assert pm.get_model("unknown_task") == "gpt-4o-mini"
