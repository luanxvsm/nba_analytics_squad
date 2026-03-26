"""
Tasks — Definição das 3 tarefas da NBA Analytics Squad.

Cada tarefa é vinculada ao seu agente correspondente e configurada
a partir do YAML em config/tasks.yaml.
"""

from __future__ import annotations

import yaml
from pathlib import Path
from crewai import Task, Agent


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _load_tasks_config() -> dict:
    """Carrega a configuração das tarefas do YAML."""
    config_path = Path(__file__).resolve().parent.parent / "config" / "tasks.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ──────────────────────────────────────────────
# Fábrica de Tarefas
# ──────────────────────────────────────────────

def create_collect_data_task(agent: Agent) -> Task:
    """Cria a tarefa de coleta de dados NBA."""
    cfg = _load_tasks_config()["collect_data"]
    return Task(
        description=cfg["description"],
        expected_output=cfg["expected_output"],
        agent=agent,
    )


def create_analyze_data_task(agent: Agent) -> Task:
    """Cria a tarefa de análise estatística."""
    cfg = _load_tasks_config()["analyze_data"]
    return Task(
        description=cfg["description"],
        expected_output=cfg["expected_output"],
        agent=agent,
    )


def create_write_report_task(agent: Agent, output_file: str) -> Task:
    """Cria a tarefa de redação do relatório."""
    cfg = _load_tasks_config()["write_report"]
    return Task(
        description=cfg["description"],
        expected_output=cfg["expected_output"],
        agent=agent,
        output_file=output_file,
    )
