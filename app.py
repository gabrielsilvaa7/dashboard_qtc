import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da Página
st.set_page_config(page_title="Dashboard - Quero te Conhecer", layout="wide", initial_sidebar_state="collapsed")

# 2. Injeção de CSS Customizado (Dark Mode + Neon Azul e Rosa)
st.markdown("""
    <style>
        /* Fundo principal escuro */
        .stApp {
            background-color: #0d1117;
            color: #ffffff;
        }
        
        /* Títulos com efeito Neon */
        h1, h2, h3 {
            color: #ffffff;
            text-shadow: 0 0 5px #00E5FF, 0 0 10px #00E5FF, 0 0 20px #00E5FF;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            text-align: center;
        }
        
        h2 {
            text-shadow: 0 0 5px #FF00FF, 0 0 10px #FF00FF;
            margin-top: 2rem;
        }

        /* Estilização dos Cartões de KPI */
        div[data-testid="metric-container"] {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 229, 255, 0.2);
            text-align: center;
            transition: 0.3s;
        }
        
        div[data-testid="metric-container"]:hover {
            border-color: #FF00FF;
            box-shadow: 0 0 15px rgba(255, 0, 255, 0.5);
        }

        /* Cor do valor do KPI */
        div[data-testid="metric-container"] > div > div > div {
            color: #00E5FF !important;
            font-size: 2.5rem !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Carregamento dos Dados (Cache de 15 segundos para "Real-Time")
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSS9faCvsxi4P_mQ-2CNqUJ8H9m9onYcMwOlBonyqT_wFe-BACv_aLuD1ZD8fBgCTdRN8qsm4oGANHt/pub?gid=949734563&single=true&output=csv"

@st.cache_data(ttl=15)
def load_data():
    try:
        # Lê o CSV diretamente do Google Sheets
        df = pd.read_csv(SHEET_CSV_URL)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

df = load_data()

# 4. Construção da Interface
st.title("📊 Dashboard - Quero te Conhecer")
st.markdown("Monitoramento em tempo real de novos usuários e avaliações do app.")

if not df.empty:
    # Separação dos dados
    df_avaliacoes = df[df['Métrica'].str.contains('Avaliaç')]
    df_usuarios = df[~df['Métrica'].str.contains('Avaliaç')]

    # Cálculos dos KPIs
    total_avaliacoes = df_avaliacoes['Quantidade'].sum()
    total_usuarios = df_usuarios['Quantidade'].sum()

    st.markdown("---")
    
    # Linha 1: KPIs Principais
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total de Novos Usuários", value=int(total_usuarios))
    with col2:
        st.metric(label="Total de Avaliações", value=int(total_avaliacoes))

    # Paleta de cores Neon para os gráficos
    neon_colors = ['#00E5FF', '#FF00FF', '#B000FF', '#007BFF']

    # Linha 2: Gráficos de Rosca (Detalhamento)
    st.markdown("## Detalhamento Geral")
    col3, col4 = st.columns(2)
    
    with col3:
        # Gráfico de Usuários
        fig_users = px.pie(
            df_usuarios, values='Quantidade', names='Métrica', 
            hole=0.5, title="Distribuição de Novos Usuários"
        )
        fig_users.update_traces(marker=dict(colors=neon_colors), textinfo='percent+label', textfont_size=14)
        fig_users.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig_users, use_container_width=True)

    with col4:
        # Gráfico de Avaliações
        fig_avals = px.pie(
            df_avaliacoes, values='Quantidade', names='Métrica', 
            hole=0.5, title="Distribuição de Avaliações"
        )
        fig_avals.update_traces(marker=dict(colors=['#00E5FF', '#FF00FF']), textinfo='percent+label', textfont_size=14)
        fig_avals.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig_avals, use_container_width=True)

    # Linha 3: Gráfico de Barras por Cidade/Bairro
    st.markdown("## Desempenho por Localidade")
    
    # Agrupando dados totais por Cidade e Bairro
    df_agrupado = df.groupby(['Cidade', 'Bairro'])['Quantidade'].sum().reset_index()
    df_agrupado = df_agrupado.sort_values(by='Quantidade', ascending=True)

    fig_bar = px.bar(
        df_agrupado, x='Quantidade', y='Bairro', color='Cidade',
        orientation='h', title="Total Geral (Usuários + Avaliações) por Bairro",
        color_discrete_sequence=neon_colors
    )
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
        font_color="white", showlegend=True, height=500
    )
    st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.warning("Aguardando o carregamento dos dados da planilha...")