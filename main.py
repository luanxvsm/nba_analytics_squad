"""
NBA Analytics Squad — Ponto de Entrada.

Carrega variáveis de ambiente e executa o pipeline completo
da equipe de agentes autônomos.
"""

import sys
from pathlib import Path
from dotenv import load_dotenv


def main() -> None:
    """Função principal do projeto."""
    # Carregar variáveis de ambiente do .env
    env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(dotenv_path=env_path)

    # Verificar se a API key está configurada
    import os
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key or api_key.startswith("sk-your"):
        print("❌  Erro: GEMINI_API_KEY não configurada.")
        print("   Copie .env.example para .env e preencha sua chave.")
        print("   Exemplo: cp .env.example .env")
        sys.exit(1)

    # Importar e executar a Crew
    from src.crew import NbaAnalyticsCrew

    squad = NbaAnalyticsCrew()
    result = squad.run()

    print("\n📋  Resultado final:")
    print(result)


if __name__ == "__main__":
    main()
