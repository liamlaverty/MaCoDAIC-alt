"""
Configuration settings for the image-ablation-tests project.

This module contains all configurable parameters for VLM queries.
Settings are loaded from environment variables where possible; copy
.env.example to .env and fill in your API keys.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# PROJECT PATHS
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
GLOBAL_PROMPT_LOG_DIR = PROJECT_ROOT / "_logs" / "prompt_logs"
GLOBAL_ECONOMY_LOG_DIR = PROJECT_ROOT / "_logs" / "economy_logs"


# ============================================================================
# PROVIDER CONFIGURATION
# ============================================================================

# Provider selection: "anthropic", "mistral", or "lmstudio"
PROVIDER = os.getenv("PROVIDER", "anthropic")

# Mistral API settings
MISTRAL_BASE_URL = "https://api.mistral.ai/v1"
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
MISTRAL_DEFAULT_MODEL = "mistral-large-latest"
MISTRAL_VLM_MODEL = "mistral-large-latest"
MISTRAL_EVALUATION_VLM_MODEL = "mistral-large-latest"

# LMStudio API settings (for local development)
LMSTUDIO_BASE_URL = "http://localhost:1234/v1"
LMSTUDIO_MODEL = "local-model"
LMSTUDIO_VLM_MODEL = "lmistralai/ministral-3-3b"
LMSTUDIO_EVALUATION_VLM_MODEL = "lmistralai/ministral-3-3b"

# Anthropic API settings
ANTHROPIC_BASE_URL = "https://api.anthropic.com/v1"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_DEFAULT_MODEL = "claude-"
ANTHROPIC_VLM_MODEL = "claude-"
ANTHROPIC_EVALUATION_VLM_MODEL = "claude-sonnet-4-6"
ANTHROPIC_PLANNER_MODEL = "claude-"
ANTHROPIC_VERSION = "2023-06-01"

# Planner model settings
MISTRAL_PLANNER_MODEL = "mistral-large-latest"
LMSTUDIO_PLANNER_MODEL = "local-model"

# Resolved settings based on active provider
if PROVIDER == "mistral":
    API_BASE_URL = MISTRAL_BASE_URL
    API_KEY = MISTRAL_API_KEY
    DEFAULT_MODEL = MISTRAL_DEFAULT_MODEL
    VLM_MODEL = MISTRAL_VLM_MODEL
    EVALUATION_VLM_MODEL = MISTRAL_EVALUATION_VLM_MODEL
    PLANNER_MODEL = MISTRAL_PLANNER_MODEL
elif PROVIDER == "anthropic":
    API_BASE_URL = ANTHROPIC_BASE_URL
    API_KEY = ANTHROPIC_API_KEY
    DEFAULT_MODEL = ANTHROPIC_DEFAULT_MODEL
    VLM_MODEL = ANTHROPIC_VLM_MODEL
    EVALUATION_VLM_MODEL = ANTHROPIC_EVALUATION_VLM_MODEL
    PLANNER_MODEL = ANTHROPIC_PLANNER_MODEL
else:  # lmstudio
    API_BASE_URL = LMSTUDIO_BASE_URL
    API_KEY = ""  # No auth for LMStudio
    DEFAULT_MODEL = LMSTUDIO_MODEL
    VLM_MODEL = LMSTUDIO_VLM_MODEL
    EVALUATION_VLM_MODEL = LMSTUDIO_EVALUATION_VLM_MODEL
    PLANNER_MODEL = LMSTUDIO_PLANNER_MODEL

# Request settings
REQUEST_TIMEOUT = 300  # seconds
MAX_TOKENS = 8192
VLM_TIMEOUT = 300  # seconds (VLMs are slower than text-only LLMs)
