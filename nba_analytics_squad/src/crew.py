"""
Crew — Orquestração da NBA Analytics Squad.

Monta a equipe de agentes, define as tarefas em ordem sequencial
e expõe o método run() para execução completa do pipeline.
"""

from __future__ import annotations

from pathlib import Path
from crewai import Crew, Process

from src.agents import (
    create_data_collector,
    create_data_analyst,
    create_report_writer,
)
from src.tasks import (
    create_collect_data_task,
    create_analyze_data_task,
    create_write_report_task,
)


class NbaAnalyticsCrew:
    """Equipe de agentes autônomos para análise de dados da NBA."""

    def __init__(self, output_dir: str | None = None):
        # Diretório de saída
        if output_dir is None:
            output_dir = str(
                Path(__file__).resolve().parent.parent / "output"
            )
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.output_file = str(self.output_dir / "report.md")

        # Instanciar agentes
        self.collector = create_data_collector()
        self.analyst = create_data_analyst()
        self.writer = create_report_writer()

        # Instanciar tarefas (ordem sequencial)
        self.collect_task = create_collect_data_task(self.collector)
        self.analyze_task = create_analyze_data_task(self.analyst)
        self.write_task = create_write_report_task(
            self.writer, self.output_file
        )

        # Montar a Crew
        self.crew = Crew(
            agents=[self.collector, self.analyst, self.writer],
            tasks=[self.collect_task, self.analyze_task, self.write_task],
            process=Process.sequential,
            verbose=True,
        )

    def run(self) -> str:
        """Executa o pipeline completo e retorna o resultado final."""
        print("\n" + "=" * 60)
        print("🏀  NBA Analytics Squad — Iniciando pipeline...")
        print("=" * 60 + "\n")

        result = self.crew.kickoff()

        print("\n" + "=" * 60)
        print(f"✅  Relatório salvo em: {self.output_file}")
        print("=" * 60 + "\n")

        return result
