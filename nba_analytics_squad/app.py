"""
NBA Analytics Squad — Dashboard Streamlit.

Interface web para interagir com a equipe de agentes CrewAI.
Execute com: streamlit run app.py
"""

import sys
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# ── Carregar .env antes de qualquer import que use a key ──
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# ──────────────────────────────────────────────
# Page Config
# ──────────────────────────────────────────────

st.set_page_config(
    page_title="NBA Analytics Squad",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
# Custom CSS
# ──────────────────────────────────────────────

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Global ── */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* ── Hero header ── */
    .hero {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 40%, #0f3460 100%);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.06);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    .hero h1 {
        color: #ffffff;
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    .hero p {
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 300;
        max-width: 640px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* ── Agent cards ── */
    .agent-card {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1.5rem;
        text-align: center;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        height: 100%;
    }
    .agent-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.35);
    }
    .agent-icon {
        font-size: 2.4rem;
        margin-bottom: 0.6rem;
    }
    .agent-card h3 {
        color: #e2e8f0;
        font-size: 1.05rem;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }
    .agent-card p {
        color: #64748b;
        font-size: 0.85rem;
        line-height: 1.5;
    }

    /* ── Status pill ── */
    .status-pill {
        display: inline-block;
        padding: 0.3rem 1rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .status-ready {
        background: rgba(34, 197, 94, 0.15);
        color: #22c55e;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }
    .status-error {
        background: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    /* ── Report container ── */
    .report-container {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 2rem;
        margin-top: 1rem;
    }
    .report-container h1, .report-container h2, .report-container h3 {
        color: #e2e8f0;
    }
    .report-container p, .report-container li {
        color: #cbd5e1;
        line-height: 1.7;
    }
    .report-container table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
    }
    .report-container th {
        background: rgba(255, 255, 255, 0.05);
        color: #e2e8f0;
        padding: 0.6rem 1rem;
        text-align: left;
    }
    .report-container td {
        color: #cbd5e1;
        padding: 0.5rem 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* ── Button override ── */
    .stButton > button {
        background: linear-gradient(135deg, #e65100, #ff6d00) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.75rem 2.5rem !important;
        border: none !important;
        border-radius: 50px !important;
        letter-spacing: 0.3px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(230, 81, 0, 0.4) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(230, 81, 0, 0.55) !important;
    }

    /* ── Divider ── */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Hero Section
# ──────────────────────────────────────────────

st.markdown("""
<div class="hero">
    <h1>🏀 NBA Analytics Squad</h1>
    <p>
        Equipe de agentes autônomos que coleta dados em tempo real da NBA,
        calcula métricas avançadas de eficiência e gera relatórios
        profissionais — tudo com um clique.
    </p>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Agent Cards
# ──────────────────────────────────────────────

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="agent-card">
        <div class="agent-icon">📡</div>
        <h3>Agente Coletor</h3>
        <p>Extrai dados brutos de jogos recentes e estatísticas de jogadores via <strong>nba_api</strong>.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="agent-card">
        <div class="agent-icon">📊</div>
        <h3>Agente Analista</h3>
        <p>Calcula métricas avançadas como <strong>TS%</strong>, <strong>eFG%</strong>, <strong>AST/TO</strong> e <strong>PIE</strong> com pandas.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="agent-card">
        <div class="agent-icon">✍️</div>
        <h3>Agente Redator</h3>
        <p>Transforma a análise em um <strong>boletim Markdown</strong> profissional e envolvente.</p>
    </div>
    """, unsafe_allow_html=True)


st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────
# API Key Check
# ──────────────────────────────────────────────

api_key = os.getenv("GEMINI_API_KEY", "")
key_ok = bool(api_key) and not api_key.startswith("sk-your")

if key_ok:
    st.markdown(
        '<div style="text-align:center;">'
        '<span class="status-pill status-ready">● GEMINI API KEY CONFIGURADA</span>'
        '</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<div style="text-align:center;">'
        '<span class="status-pill status-error">● GEMINI_API_KEY NÃO ENCONTRADA</span>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.warning(
        "Configure a variável `GEMINI_API_KEY` no arquivo `.env` "
        "na raiz do projeto antes de gerar um relatório."
    )


# ──────────────────────────────────────────────
# Action Button
# ──────────────────────────────────────────────

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    generate_clicked = st.button(
        "🚀  Gerar Novo Relatório",
        use_container_width=True,
        disabled=not key_ok,
    )


# ──────────────────────────────────────────────
# Execution
# ──────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_FILE = PROJECT_ROOT / "output" / "report.md"


def run_crew() -> str:
    """Importa e executa a NbaAnalyticsCrew, retornando o resultado."""
    from src.crew import NbaAnalyticsCrew

    squad = NbaAnalyticsCrew(output_dir=str(PROJECT_ROOT / "output"))
    result = squad.run()
    return str(result)


if generate_clicked:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    with st.status("🏀 Agentes trabalhando...", expanded=True) as status:
        st.write("📡  **Agente Coletor** buscando dados da NBA...")
        st.write("📊  **Agente Analista** calculando métricas avançadas...")
        st.write("✍️  **Agente Redator** escrevendo o relatório...")

        try:
            result = run_crew()
            status.update(
                label="✅ Relatório gerado com sucesso!",
                state="complete",
                expanded=False,
            )
        except Exception as e:
            status.update(
                label="❌ Erro durante a execução",
                state="error",
                expanded=True,
            )
            st.error(f"Erro: {e}")
            st.stop()

    # ── Display report ──
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📋 Relatório Gerado")

    report_content = ""
    if OUTPUT_FILE.exists():
        report_content = OUTPUT_FILE.read_text(encoding="utf-8")
    else:
        report_content = str(result)

    st.markdown(
        f'<div class="report-container">{""}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(report_content)

    # ── Download button ──
    st.download_button(
        label="⬇️  Baixar report.md",
        data=report_content,
        file_name="nba_analytics_report.md",
        mime="text/markdown",
    )


# ──────────────────────────────────────────────
# Previous Report (if exists)
# ──────────────────────────────────────────────

elif OUTPUT_FILE.exists():
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📋 Último Relatório Gerado")

    report_content = OUTPUT_FILE.read_text(encoding="utf-8")
    st.markdown(report_content)

    st.download_button(
        label="⬇️  Baixar report.md",
        data=report_content,
        file_name="nba_analytics_report.md",
        mime="text/markdown",
    )


# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center; color:#475569; font-size:0.8rem;">'
    'NBA Analytics Squad · Powered by CrewAI + nba_api + Streamlit'
    '</p>',
    unsafe_allow_html=True,
)
