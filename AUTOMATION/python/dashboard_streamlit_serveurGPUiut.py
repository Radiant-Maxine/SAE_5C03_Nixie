#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenWEC Logs Dashboard - Streamlit App with IUT GPU Server
Analyse des logs Windows Event Collector avec Qwen via Ollama (IUT)
Lecture directe depuis le serveur OpenWEC
"""

import streamlit as st
import pandas as pd
import json
import requests
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
import logging
from pathlib import Path

# Configuration Streamlit
st.set_page_config(
    page_title="OpenWEC Logs Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Style CSS personnalisé
st.markdown("""
    <style>
    .main-header {
        color: #38bdf8;
        font-size: 2.5em;
        margin-bottom: 10px;
    }
    .stat-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #38bdf8;
        margin: 10px 0;
    }
    .threat-alert {
        background-color: rgba(239, 68, 68, 0.1);
        border-left: 4px solid #ef4444;
        padding: 15px;
        border-radius: 6px;
        color: #fca5a5;
    }
    .success-box {
        background-color: rgba(34, 197, 94, 0.1);
        border-left: 4px solid #22c55e;
        padding: 15px;
        border-radius: 6px;
        color: #86efac;
    }
    .info-box {
        background-color: rgba(56, 189, 248, 0.1);
        border-left: 4px solid #38bdf8;
        padding: 15px;
        border-radius: 6px;
        color: #7dd3fc;
    }
    .gpu-server-info {
        background-color: rgba(168, 85, 247, 0.1);
        border-left: 4px solid #a855f7;
        padding: 15px;
        border-radius: 6px;
        color: #e9d5ff;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNCTIONS
# ============================================================================

def parse_json_lines(file_content: str) -> list:
    """Parse JSONL format logs"""
    logs = []
    for line in file_content.split('\n'):
        if line.strip():
            try:
                logs.append(json.loads(line))
            except json.JSONDecodeError as e:
                logger.warning(f"JSON parse error: {e}")
                continue
    return logs

def load_logs_from_server(file_path: str = "/opt/openwec/data_openwec/sysmon_events.json") -> list:
    """Load logs directly from OpenWEC server"""
    try:
        if not Path(file_path).exists():
            st.error(f"❌ Fichier non trouvé: {file_path}")
            return []

        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()

        logs = parse_json_lines(file_content)
        st.success(f"✅ {len(logs)} logs chargés depuis {file_path}")
        return logs

    except PermissionError:
        st.error(f"❌ Erreur de permissions pour accéder à {file_path}")
        return []
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement: {str(e)}")
        return []

def load_logs_from_upload(uploaded_file) -> list:
    """Load logs from uploaded file"""
    try:
        file_content = uploaded_file.read().decode('utf-8')
        logs = parse_json_lines(file_content)
        return logs
    except Exception as e:
        st.error(f"❌ Erreur lors du parsing: {str(e)}")
        return []

def get_event_type(event_data: dict) -> str:
    """Detect Sysmon event type"""
    if not event_data:
        return 'Unknown'
    if 'CommandLine' in event_data:
        return 'ProcessCreation'
    elif 'SourcePort' in event_data or 'DestinationPort' in event_data:
        return 'NetworkConnection'
    elif 'TargetFilename' in event_data:
        return 'FileCreate'
    elif 'SourceIp' in event_data or 'Dns' in event_data:
        return 'DNSQuery'
    elif 'Image' in event_data:
        return 'ProcessTerminated'
    elif 'RegistryPath' in event_data:
        return 'RegistryEvent'
    else:
        return 'Other'

def prepare_logs_dataframe(logs: list) -> pd.DataFrame:
    """Convert logs to DataFrame for display"""
    data = []
    for log in logs:
        system = log.get('System', {})
        event_data = log.get('EventData', {})

        data.append({
            'Timestamp': system.get('TimeCreated', 'N/A'),
            'Computer': system.get('Computer', 'Unknown'),
            'User': event_data.get('User', 'System'),
            'EventType': get_event_type(event_data),
            'EventID': system.get('EventID', 'N/A'),
            'Details': event_data.get('CommandLine') or event_data.get('Image') or event_data.get('TargetFilename') or 'N/A',
            'RawLog': json.dumps(event_data, indent=2)
        })

    return pd.DataFrame(data)

def get_statistics(df: pd.DataFrame) -> dict:
    """Calculate statistics from logs"""
    return {
        'total_logs': len(df),
        'unique_computers': df['Computer'].nunique(),
        'unique_users': df['User'].nunique(),
        'event_types': df['EventType'].nunique(),
        'top_events': df['EventType'].value_counts().head(5),
        'top_computers': df['Computer'].value_counts().head(5),
        'top_users': df['User'].value_counts().head(5)
    }

def check_iut_server(endpoint: str) -> tuple[bool, str]:
    """Check if IUT server is accessible and return available models"""
    try:
        response = requests.get(
            f"{endpoint}/api/tags",
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()
            models = [m['name'] for m in data.get('models', [])]
            return True, models
        else:
            return False, f"Erreur serveur: {response.status_code}"

    except requests.exceptions.ConnectionError:
        return False, f"Impossible de se connecter à {endpoint}"
    except requests.exceptions.Timeout:
        return False, "Timeout lors de la connexion au serveur"
    except Exception as e:
        return False, f"Erreur: {str(e)}"

def query_iut_server(prompt: str, endpoint: str, model: str) -> str:
    """Query IUT GPU server via Ollama API"""
    try:
        response = requests.post(
            f"{endpoint}/api/chat",
            json={
                "model": model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            },
            timeout=600  # 10 minutes timeout for GPU server
        )

        if response.status_code == 200:
            data = response.json()
            return data.get('message', {}).get('content', 'Pas de réponse')
        else:
            return f"❌ Erreur API: {response.status_code}\n{response.text}"

    except requests.exceptions.ConnectionError:
        return f"❌ Impossible de se connecter au serveur IUT\nVérifiez: http://openwebui.iutbeziers.fr:11434"
    except requests.exceptions.Timeout:
        return "❌ Timeout (10 min): Le serveur GPU prend trop de temps. Essayez avec moins de logs."
    except Exception as e:
        return f"❌ Erreur: {str(e)}"

def build_threat_analysis_prompt(logs: list) -> str:
    """Build threat detection prompt"""
    logs_json = json.dumps(logs, indent=2)
    return f"""Tu es un analyste SOC expert. Analyse ces logs Sysmon/Windows Event Collector.

INSTRUCTIONS:
1. Identifie UNIQUEMENT les menaces critiques et anomalies de sécurité
2. Sois précis et technique
3. Indique la RAISON pour laquelle c'est une menace
4. Formate clairement tes trouvailles

Si aucune menace: répondre "✅ Aucune menace critique détectée"
Si menaces trouvées: commencer par "🚨 MENACES DÉTECTÉES:"

LOGS À ANALYSER:
{logs_json}

Analyse détaillée:"""

def build_summary_prompt(logs: list) -> str:
    """Build activity summary prompt"""
    logs_json = json.dumps(logs, indent=2)
    return f"""Résume l'activité Windows globale de ces logs en 3-5 points clés.
Sois concis et focus sur les informations pertinentes.

LOGS:
{logs_json}

Résumé:"""

def build_anomaly_prompt(logs: list) -> str:
    """Build anomaly detection prompt"""
    logs_json = json.dumps(logs, indent=2)
    return f"""Identifie les anomalies et comportements suspects dans ces logs.
Pour chaque anomalie trouvée, explique pourquoi c'est suspect.

LOGS:
{logs_json}

Anomalies détectées:"""

# ============================================================================
# STREAMLIT INTERFACE
# ============================================================================

# Header
st.markdown("""
    <div class="main-header">
        🛡️ OpenWEC Logs Dashboard
    </div>
    <p>Analyse des logs Windows Event Collector avec IA du serveur GPU IUT</p>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    # IUT GPU Server Configuration
    st.subheader("🚀 Serveur GPU IUT")
    iut_endpoint = st.text_input(
        "Endpoint Ollama (IUT)",
        value="http://openwebui.iutbeziers.fr:11434",
        help="URL du serveur Ollama de l'IUT"
    )

    # Check server connectivity
    if st.button("🔍 Vérifier connexion au serveur", use_container_width=True):
        with st.spinner("Vérification en cours..."):
            is_connected, result = check_iut_server(iut_endpoint)
            if is_connected:
                st.success(f"✅ Serveur accessible!")
                st.markdown(f'<div class="gpu-server-info">📊 **{len(result)} modèles disponibles**</div>', unsafe_allow_html=True)
                with st.expander("Voir les modèles disponibles"):
                    for model in result:
                        st.code(model, language=None)
            else:
                st.error(f"❌ Erreur de connexion: {result}")

    st.divider()

    # Model Selection with recommendations
    st.subheader("🤖 Sélection du Modèle")

    recommended_models = [
        ("qwen2.5-coder:14b", "⭐ Recommandé - Rapide & Fiable"),
        ("mistral-small:latest", "⭐ Rapide - Bon pour analyses rapides"),
        ("llama3.3:70b", "🔥 Puissant - Analyses détaillées (plus lent)"),
    ]

    model_display = [f"{name} - {desc}" for name, desc in recommended_models]
    selected_display = st.selectbox(
        "Modèle à utiliser",
        options=model_display,
        help="Choisir un modèle pour l'analyse"
    )

    # Extract model name from display
    llm_model = selected_display.split(" - ")[0]

    # Show model info
    if "qwen2.5-coder" in llm_model:
        st.info("✅ Choix optimal: Rapide (30-60s pour 50 logs) et précis pour les analyses de sécurité")
    elif "mistral-small" in llm_model:
        st.info("⚡ Très rapide: Idéal pour les analyses rapides (10-30s)")
    else:
        st.warning("⏳ Puissant mais lent: Peut prendre 2-5 minutes pour analyses détaillées")

    st.divider()

    # Server Configuration
    st.subheader("🗂️ Configuration OpenWEC")
    openwec_path = st.text_input(
        "Chemin fichier logs OpenWEC",
        value="/opt/openwec/data_openwec/sysmon_events.json",
        help="Chemin complet du fichier logs"
    )

    st.divider()
    st.subheader("ℹ️ Informations")
    st.markdown("""
    **Serveur GPU IUT:**
    - Endpoint: `http://openwebui.iutbeziers.fr:11434`
    - Modèles disponibles: Qwen, Mistral, Llama, etc.
    - Accès pour les étudiants de l'IUT

    **Modèles Recommandés:**
    1. `qwen2.5-coder:14b` ⭐ (Meilleur rapport vitesse/qualité)
    2. `mistral-small:latest` ⚡ (Plus rapide)
    3. `llama3.3:70b` 🔥 (Plus puissant mais lent)

    **Timeout:** 10 minutes pour les analyses GPU
    """)

# Main Content
tab1, tab2, tab3 = st.tabs(["📊 Tableau de Bord", "📋 Tableau Logs", "🤖 Analyse LLM"])

# ============================================================================
# TAB 1: DASHBOARD
# ============================================================================
with tab1:
    col1, col2, col3 = st.columns([2, 2, 2])

    with col1:
        if st.button("📂 Charger depuis le serveur", type="primary", use_container_width=True):
            logs = load_logs_from_server(openwec_path)
            if logs:
                st.session_state.logs = logs
                st.session_state.source = "serveur"
                st.rerun()

    with col2:
        uploaded_file = st.file_uploader(
            "📁 Ou charger fichier JSON",
            type=["json"],
            help="Format JSONL (une ligne = un log)"
        )
        if uploaded_file is not None:
            logs = load_logs_from_upload(uploaded_file)
            if logs:
                st.session_state.logs = logs
                st.session_state.source = "upload"
                st.rerun()

    with col3:
        if st.button("🗑️ Effacer les données", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    if 'logs' in st.session_state and st.session_state.logs:
        # Show data source
        source_text = "Serveur OpenWEC" if st.session_state.source == "serveur" else "Fichier uploadé"
        st.markdown(f'<div class="info-box">📍 Source: <strong>{source_text}</strong></div>', unsafe_allow_html=True)

        df = prepare_logs_dataframe(st.session_state.logs)
        stats = get_statistics(df)

        # Statistics Cards
        cols = st.columns(4)
        with cols[0]:
            st.metric("📊 Logs Chargés", stats['total_logs'])
        with cols[1]:
            st.metric("💻 Machines Uniques", stats['unique_computers'])
        with cols[2]:
            st.metric("👤 Utilisateurs Uniques", stats['unique_users'])
        with cols[3]:
            st.metric("🎯 Types d'Événements", stats['event_types'])

        st.divider()

        # Visualizations
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📈 Événements par Type")
            fig = px.pie(
                values=stats['top_events'].values,
                names=stats['top_events'].index,
                color_discrete_sequence=px.colors.sequential.Blues
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("💻 Top 5 Machines")
            fig = px.bar(
                x=stats['top_computers'].values,
                y=stats['top_computers'].index,
                orientation='h',
                color_discrete_sequence=['#38bdf8']
            )
            st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("👤 Top 5 Utilisateurs")
            fig = px.bar(
                x=stats['top_users'].values,
                y=stats['top_users'].index,
                orientation='h',
                color_discrete_sequence=['#22c55e']
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("📅 Timeline des Logs")
            df['Hour'] = pd.to_datetime(df['Timestamp'], errors='coerce').dt.hour
            timeline = df['Hour'].value_counts().sort_index()
            fig = px.line(
                x=timeline.index,
                y=timeline.values,
                markers=True,
                labels={'x': 'Heure', 'y': 'Nombre de Logs'}
            )
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("📭 Chargez les logs depuis le serveur ou uploadez un fichier")

# ============================================================================
# TAB 2: LOGS TABLE
# ============================================================================
with tab2:
    if 'logs' in st.session_state and st.session_state.logs:
        df = prepare_logs_dataframe(st.session_state.logs)

        # Filters
        col1, col2, col3 = st.columns(3)

        with col1:
            event_filter = st.multiselect(
                "Filtrer par Type d'Événement",
                options=sorted(df['EventType'].unique()),
                default=sorted(df['EventType'].unique())
            )

        with col2:
            computer_filter = st.multiselect(
                "Filtrer par Machine",
                options=sorted(df['Computer'].unique()),
                default=sorted(df['Computer'].unique())
            )

        with col3:
            user_filter = st.multiselect(
                "Filtrer par Utilisateur",
                options=sorted(df['User'].unique()),
                default=sorted(df['User'].unique())
            )

        # Apply filters
        filtered_df = df[
            (df['EventType'].isin(event_filter)) &
            (df['Computer'].isin(computer_filter)) &
            (df['User'].isin(user_filter))
        ].copy()

        st.subheader(f"📋 Logs ({len(filtered_df)}/{len(df)})")

        # Display table
        display_df = filtered_df[['Timestamp', 'Computer', 'User', 'EventType', 'EventID', 'Details']]
        st.dataframe(display_df, use_container_width=True, height=400)

        # Export option
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Télécharger CSV",
            data=csv,
            file_name=f"openwec_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

    else:
        st.info("📭 Chargez d'abord les logs depuis le serveur ou uploadez un fichier")

# ============================================================================
# TAB 3: LLM ANALYSIS
# ============================================================================
with tab3:
    if 'logs' in st.session_state and st.session_state.logs:
        st.markdown(f'<div class="gpu-server-info">🚀 Analyse avec le serveur GPU IUT - Modèle: <strong>{llm_model}</strong></div>', unsafe_allow_html=True)

        # Control number of logs to analyze
        st.markdown("### 📊 Sélection des logs")
        col1, col2 = st.columns(2)

        with col1:
            num_logs = st.radio(
                "Nombre de logs à analyser:",
                options=[10, 50, 100],
                format_func=lambda x: f"🔍 {x} derniers logs (rapide ~30s)" if x == 10 else (f"📋 {x} derniers logs (moyen ~2min)" if x == 50 else f"📈 {x} derniers logs (long ~5min)")
            )

        with col2:
            st.info(f"⏱️ Temps estimé pour **{num_logs}** logs avec `{llm_model.split(':')[0]}`")

        logs_to_analyze = st.session_state.logs[-num_logs:]

        analysis_type = st.radio(
            "Type d'analyse:",
            options=[
                ("🚨 Détection de menaces", "threat"),
                ("📊 Résumé des activités", "summary"),
                ("⚠️ Détection d'anomalies", "anomalies"),
                ("✍️ Analyse personnalisée", "custom")
            ],
            format_func=lambda x: x[0],
            horizontal=True
        )

        custom_prompt = None
        if analysis_type[1] == "custom":
            custom_prompt = st.text_area(
                "Votre question:",
                placeholder="Ex: Quels sont les ProcessCreation suspects?",
                height=100
            )

        col1, col2 = st.columns([3, 1])
        with col1:
            analyze_btn = st.button("🤖 Analyser avec le serveur GPU IUT", type="primary", use_container_width=True)

        with col2:
            clear_analysis = st.button("🗑️ Effacer", use_container_width=True)

        if clear_analysis:
            if 'analysis_result' in st.session_state:
                del st.session_state.analysis_result
            st.rerun()

        if analyze_btn:
            if analysis_type[1] == "custom" and not custom_prompt:
                st.error("❌ Écrivez une question personnalisée")
            else:
                with st.spinner(f"⏳ Analyse en cours avec le serveur GPU IUT ({num_logs} logs)..."):
                    # Build prompt
                    if analysis_type[1] == "threat":
                        prompt = build_threat_analysis_prompt(logs_to_analyze)
                    elif analysis_type[1] == "summary":
                        prompt = build_summary_prompt(logs_to_analyze)
                    elif analysis_type[1] == "anomalies":
                        prompt = build_anomaly_prompt(logs_to_analyze)
                    else:
                        prompt = f"{custom_prompt}\n\nContexte - Logs à analyser:\n{json.dumps(logs_to_analyze, indent=2)}"

                    # Query IUT GPU server
                    result = query_iut_server(prompt, iut_endpoint, llm_model)
                    st.session_state.analysis_result = result

        # Display results
        if 'analysis_result' in st.session_state:
            st.divider()

            if "❌" in st.session_state.analysis_result:
                st.markdown(f'<div class="threat-alert">{st.session_state.analysis_result}</div>', unsafe_allow_html=True)
            elif "✅" in st.session_state.analysis_result:
                st.markdown(f'<div class="success-box">{st.session_state.analysis_result}</div>', unsafe_allow_html=True)
            else:
                st.markdown("### 📝 Résultats de l'Analyse")
                st.write(st.session_state.analysis_result)

            # Copy to clipboard helper
            st.download_button(
                label="📥 Télécharger analyse",
                data=st.session_state.analysis_result,
                file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

    else:
        st.info("📭 Chargez d'abord les logs pour analyser")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #cbd5e1; font-size: 0.9em;'>
        🛡️ OpenWEC Dashboard | GPU Server IUT | Made with ❤️ by Nixie
    </div>
""", unsafe_allow_html=True)
