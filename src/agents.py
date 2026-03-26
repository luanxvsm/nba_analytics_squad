"""
Agents — Definição dos 3 agentes da NBA Analytics Squad.

Os agentes são configurados a partir do YAML em config/agents.yaml
e instanciados com os atributos e ferramentas correspondentes.
"""

from __future__ import annotations

import os
import yaml
from pathlib import Path
from crewai import Agent, LLM

from src.tools.nba_tools import FetchRecentGamesTool, FetchPlayerStatsTool

gemini_llm = LLM(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY")
)

# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _load_agents_config() -> dict:
    """Carrega a configuração dos agentes do YAML."""
    config_path = Path(__file__).resolve().parent.parent / "config" / "agents.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ──────────────────────────────────────────────
# Fábrica de Agentes
# ──────────────────────────────────────────────

def create_data_collector() -> Agent:
    """Cria o Agente Coletor de Dados NBA."""
    cfg = _load_agents_config()["data_collector"]
    return Agent(
        role=cfg["role"],
        goal=cfg["goal"],
        backstory=cfg["backstory"],
        tools=[FetchRecentGamesTool(), FetchPlayerStatsTool()],
        verbose=True,
        allow_delegation=False,
        llm=gemini_llm
    )


def create_data_analyst() -> Agent:
    """Cria o Agente Analista Estatístico NBA."""
    cfg = _load_agents_config()["data_analyst"]
    return Agent(
        role=cfg["role"],
        goal=cfg["goal"],
        backstory=cfg["backstory"],
        tools=[],
        verbose=True,
        allow_delegation=False,
        llm=gemini_llm
    )


def create_report_writer() -> Agent:
    """Cria o Agente Redator Esportivo."""
    cfg = _load_agents_config()["report_writer"]
    return Agent(
        role=cfg["role"],
        goal=cfg["goal"],
        backstory=cfg["backstory"],
        tools=[],
        verbose=True,
        allow_delegation=False,
        llm=gemini_llm
    )
