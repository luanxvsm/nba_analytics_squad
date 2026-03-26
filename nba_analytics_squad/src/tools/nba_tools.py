"""
NBA Tools — Ferramentas customizadas para coleta de dados via nba_api.

Cada ferramenta herda de BaseTool (CrewAI) e encapsula chamadas à API
pública da NBA, retornando dados estruturados prontos para análise.
"""

from __future__ import annotations

import json
from typing import Type

import pandas as pd
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


# ──────────────────────────────────────────────
# Schemas de entrada (Pydantic)
# ──────────────────────────────────────────────

class RecentGamesInput(BaseModel):
    """Input para FetchRecentGamesTool."""
    num_games: int = Field(
        default=5,
        description="Número de jogos recentes a buscar (padrão: 5).",
    )


class PlayerStatsInput(BaseModel):
    """Input para FetchPlayerStatsTool."""
    player_name: str = Field(
        description="Nome completo do jogador (ex: 'LeBron James').",
    )
    season: str = Field(
        default="2025-26",
        description="Temporada no formato 'YYYY-YY' (ex: '2025-26').",
    )
    last_n_games: int = Field(
        default=5,
        description="Número de jogos recentes do jogador a retornar.",
    )


# ──────────────────────────────────────────────
# Tools
# ──────────────────────────────────────────────

class FetchRecentGamesTool(BaseTool):
    """Busca os jogos mais recentes da NBA com placares e equipes."""

    name: str = "fetch_recent_nba_games"
    description: str = (
        "Busca os N jogos mais recentes da NBA, retornando times, "
        "placares, datas e estatísticas básicas do jogo. "
        "Parâmetro de entrada: num_games (int, padrão 5)."
    )
    args_schema: Type[BaseModel] = RecentGamesInput

    def _run(self, num_games: int = 5) -> str:
        """Executa a busca de jogos recentes via nba_api."""
        try:
            from nba_api.stats.endpoints import leaguegamefinder

            game_finder = leaguegamefinder.LeagueGameFinder(
                league_id_nullable="00",  # NBA
                season_nullable="2025-26",
                season_type_nullable="Regular Season",
            )
            games_df: pd.DataFrame = game_finder.get_data_frames()[0]

            # Pegar os jogos mais recentes (2 linhas por jogo — home/away)
            recent = games_df.head(num_games * 2)

            columns_of_interest = [
                "GAME_ID", "GAME_DATE", "TEAM_NAME", "TEAM_ABBREVIATION",
                "MATCHUP", "WL", "PTS", "REB", "AST", "FGM", "FGA",
                "FG3M", "FG3A", "FTM", "FTA", "STL", "BLK", "TOV",
                "PLUS_MINUS",
            ]
            available_cols = [c for c in columns_of_interest if c in recent.columns]
            recent = recent[available_cols]
            
            # FILTRO ADICIONADO AQUI: Substitui NaN por "N/A" para não quebrar o JSON
            recent = recent.fillna("N/A")

            return json.dumps(
                {
                    "status": "success",
                    "total_rows": len(recent),
                    "data": recent.to_dict(orient="records"),
                },
                ensure_ascii=False,
                default=str,
            )

        except Exception as e:
            return json.dumps(
                {"status": "error", "message": str(e)},
                ensure_ascii=False,
            )


class FetchPlayerStatsTool(BaseTool):
    """Busca estatísticas recentes de um jogador específico da NBA."""

    name: str = "fetch_player_stats"
    description: str = (
        "Busca o game log de um jogador específico da NBA na temporada "
        "informada. Parâmetros: player_name (str), season (str, padrão "
        "'2025-26'), last_n_games (int, padrão 5)."
    )
    args_schema: Type[BaseModel] = PlayerStatsInput

    def _run(
        self,
        player_name: str,
        season: str = "2025-26",
        last_n_games: int = 5,
    ) -> str:
        """Executa a busca de estatísticas do jogador via nba_api."""
        try:
            from nba_api.stats.static import players
            from nba_api.stats.endpoints import playergamelog

            # Buscar ID do jogador pelo nome
            player_list = players.find_players_by_full_name(player_name)
            if not player_list:
                return json.dumps(
                    {
                        "status": "error",
                        "message": f"Jogador '{player_name}' não encontrado.",
                    },
                    ensure_ascii=False,
                )

            player_id = player_list[0]["id"]
            player_full_name = player_list[0]["full_name"]

            game_log = playergamelog.PlayerGameLog(
                player_id=player_id,
                season=season,
                season_type_all_star="Regular Season",
            )
            log_df: pd.DataFrame = game_log.get_data_frames()[0]

            # Limitar aos últimos N jogos
            recent_log = log_df.head(last_n_games)

            columns_of_interest = [
                "GAME_DATE", "MATCHUP", "WL", "MIN", "PTS", "REB",
                "OREB", "DREB", "AST", "FGM", "FGA", "FG_PCT",
                "FG3M", "FG3A", "FG3_PCT", "FTM", "FTA", "FT_PCT",
                "STL", "BLK", "TOV", "PLUS_MINUS",
            ]
            available_cols = [c for c in columns_of_interest if c in recent_log.columns]
            recent_log = recent_log[available_cols]
            
            # FILTRO ADICIONADO AQUI: Substitui NaN por "N/A" para não quebrar o JSON
            recent_log = recent_log.fillna("N/A")

            return json.dumps(
                {
                    "status": "success",
                    "player": player_full_name,
                    "season": season,
                    "games_returned": len(recent_log),
                    "data": recent_log.to_dict(orient="records"),
                },
                ensure_ascii=False,
                default=str,
            )

        except Exception as e:
            return json.dumps(
                {"status": "error", "message": str(e)},
                ensure_ascii=False,
            )