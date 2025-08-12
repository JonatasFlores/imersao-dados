import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
def configurar_pagina():
    st.set_page_config(
        page_title="Dashboard de Salários na Área de Dados",
        page_icon="📊",
        layout="wide",
    )

# --- Carregamento dos dados ---
@st.cache_data
def carregar_dados():
    df = df = pd.read_csv("dados/dados-imersao-final.csv")

    return df

# --- Filtros ---
def aplicar_filtros(df):
    st.sidebar.header("🔍 Filtros")

    anos = st.sidebar.multiselect("Ano", sorted(df['ano'].unique()), default=sorted(df['ano'].unique()))
    senioridades = st.sidebar.multiselect("Senioridade", sorted(df['senioridade'].unique()), default=sorted(df['senioridade'].unique()))
    contratos = st.sidebar.multiselect("Tipo de Contrato", sorted(df['contrato'].unique()), default=sorted(df['contrato'].unique()))
    tamanhos = st.sidebar.multiselect("Tamanho da Empresa", sorted(df['tamanho_empresa'].unique()), default=sorted(df['tamanho_empresa'].unique()))

    df_filtrado = df[
        (df['ano'].isin(anos)) &
        (df['senioridade'].isin(senioridades)) &
        (df['contrato'].isin(contratos)) &
        (df['tamanho_empresa'].isin(tamanhos))
    ]
    return df_filtrado

# --- Métricas ---
def mostrar_metricas(df):
    st.subheader("Métricas gerais (Salário anual em USD)")
    if not df.empty:
        salario_medio = df['usd'].mean()
        salario_maximo = df['usd'].max()
        total_registros = df.shape[0]
        cargo_mais_frequente = df["cargo"].mode()[0]
    else:
        salario_medio = salario_maximo = total_registros = 0
        cargo_mais_frequente = ""

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Salário médio", f"${salario_medio:,.0f}")
    col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
    col3.metric("Total de registros", f"{total_registros:,}")
    col4.metric("Cargo mais frequente", cargo_mais_frequente)
    st.markdown("---")

# --- Gráficos ---
def mostrar_graficos(df):
    st.subheader("Gráficos")
    col1, col2 = st.columns(2)

    with col1:
        if not df.empty:
            top_cargos = df.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
            fig = px.bar(top_cargos, x='usd', y='cargo', orientation='h',
                         title="Top 10 cargos por salário médio",
                         labels={'usd': 'Média salarial anual (USD)', 'cargo': ''})
            fig.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Nenhum dado para exibir no gráfico de cargos.")

    with col2:
        if not df.empty:
            fig = px.histogram(df, x='usd', nbins=30,
                               title="Distribuição de salários anuais",
                               labels={'usd': 'Faixa salarial (USD)', 'count': ''})
            fig.update_layout(title_x=0.1)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Nenhum dado para exibir no gráfico de distribuição.")

    col3, col4 = st.columns(2)

    with col3:
        if not df.empty:
            remoto = df['remoto'].value_counts().reset_index()
            remoto.columns = ['tipo_trabalho', 'quantidade']
            fig = px.pie(remoto, names='tipo_trabalho', values='quantidade',
                         title='Proporção dos tipos de trabalho', hole=0.5)
            fig.update_traces(textinfo='percent+label')
            fig.update_layout(title_x=0.1)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

    with col4:
        if not df.empty:
            df_ds = df[df['cargo'] == 'Data Scientist']
            media_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
            fig = px.choropleth(media_pais, locations='residencia_iso3', color='usd',
                                color_continuous_scale='rdylgn',
                                title='Salário médio de Cientista de Dados por país',
                                labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'})
            fig.update_layout(title_x=0.1)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Nenhum dado para exibir no gráfico de países.")

# --- Tabela ---
def mostrar_tabela(df):
    st.subheader("Dados Detalhados")
    st.dataframe(df)

# --- Execução principal ---
def main():
    configurar_pagina()
    df = carregar_dados()
    df_filtrado = aplicar_filtros(df)

    st.title("🎲 Dashboard de Análise de Salários na Área de Dados")
    st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise.")

    mostrar_metricas(df_filtrado)
    mostrar_graficos(df_filtrado)
    mostrar_tabela(df_filtrado)

if __name__ == "__main__":
    main()
