import os
from typing import Dict

# ---------------------------------------------------------
# LLM Provider Configuration
# ---------------------------------------------------------

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "auto").lower()

# NVIDIA Build API Settings (Nemotron)
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")
NVIDIA_API_URL = os.getenv("NVIDIA_API_URL", "https://integrate.api.nvidia.com/v1/chat/completions")
NVIDIA_MODEL = os.getenv("NVIDIA_MODEL", "meta/llama-3.2-11b-vision-instruct")

# Ollama Endpoint Settings (IBM Granite / Nemotron)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "granite4.1:3b")


def get_active_llm_info() -> Dict[str, str]:
    """
    Auto-detects and returns the active LLM provider, model name, and endpoint.
    """
    api_key = os.getenv("NVIDIA_API_KEY", "")
    if LLM_PROVIDER == "granite":
        return {
            "provider": "IBM Granite (Ollama)",
            "model": OLLAMA_MODEL,
            "endpoint": f"{OLLAMA_BASE_URL}/api/generate",
            "type": "ollama"
        }
    elif LLM_PROVIDER == "nvidia" or (LLM_PROVIDER == "auto" and api_key):
        return {
            "provider": "NVIDIA Build API",
            "model": "meta/llama-3.2-11b-vision-instruct",
            "endpoint": os.getenv("NVIDIA_API_URL", "https://integrate.api.nvidia.com/v1/chat/completions"),
            "api_key": api_key,
            "type": "nvidia"
        }
    elif LLM_PROVIDER in ("ollama", "auto"):
        return {
            "provider": "Ollama Local",
            "model": OLLAMA_MODEL,
            "endpoint": f"{OLLAMA_BASE_URL}/api/generate",
            "type": "ollama"
        }
    else:
        return {
            "provider": "Deterministic Fallback",
            "model": "state-machine",
            "endpoint": "none",
            "type": "none"
        }


def set_active_llm_provider(provider_name: str) -> None:
    """
    Updates the active LLM provider dynamically at runtime.
    """
    global LLM_PROVIDER
    LLM_PROVIDER = provider_name.lower()

