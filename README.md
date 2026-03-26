# 🏀 NBA Analytics Squad - AI Agents

Este projeto utiliza **Multi-Agent Systems (MAS)** através do framework **CrewAI** para realizar análises profundas e automatizadas de jogos e jogadores da NBA.

## 🤖 A Equipe de Agentes
O sistema é composto por três agentes especializados:
1. **Coletor de Dados:** Utiliza a `nba_api` para extrair estatísticas em tempo real.
2. **Analista Estatístico:** Processa dados brutos via `Pandas` e calcula métricas avançadas (TS%, eFG%, PIE).
3. **Redator Esportivo:** Transforma dados técnicos em relatórios envolventes em Markdown.

## 🛠️ Tecnologias Utilizadas
- **Python** & **Streamlit** (Interface Web)
- **CrewAI** (Orquestração de Agentes)
- **Google Gemini 2.5 Flash** (Cérebro das IAs)
- **Pandas** (Análise de Dados)
- **NBA API** (Fonte de dados oficial)

## 🚀 Como Executar
1. Clone o repositório.
2. Configure sua `GEMINI_API_KEY` no arquivo `.env`.
3. Instale as dependências: `pip install -r requirements.txt`.
4. Execute: `streamlit run app.py`.
