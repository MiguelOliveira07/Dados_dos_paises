import streamlit as st
import requests
import pandas as pd
from translate import Translator

# Configuração da página
st.set_page_config(page_title="Mundo em Dados", page_icon="🌍", layout="wide")
st.text('Esse site é programado para te ajudar a descobrir um pouco mais sobre diversos países!')

# Campos relevantes
campos_relevantes = {
    "name": "Name",
    "region": "Região",
    "population": "População (Milhões)",
    "capital": "Capital",
    "currency": "Moeda",
    "gdp": "PIB (USD)",
    "gdp_per_capita": "PIB per capita (USD)",
    "life_expectancy_male": "Expectativa de vida (homens)",
    "life_expectancy_female": "Expectativa de vida (mulheres)",
    "internet_users": "Usuários de internet (%)"
}

# Função para traduzir o nome do país
def traduzir_pais(nome_pt):
    try:
        translator = Translator(from_lang="pt", to_lang="en")
        return translator.translate(nome_pt).strip()
    except Exception:
        return None

# Função para obter dados da API
def obter_dados_pais(nome_ingles):
    url = f'https://api.api-ninjas.com/v1/country?name={nome_ingles}'
    response = requests.get(url, headers={'X-Api-Key': st.secrets["API_KEY"]})
    
    if response.status_code == 200:
        dados = response.json()
        return dados[0] if dados else None
    else:
        return None

# Obter URL da bandeira usando a REST Countries API
def obter_bandeira_url(nome_ingles):
    try:
        response = requests.get(f"https://restcountries.com/v3.1/name/{nome_ingles}")
        if response.status_code == 200:
            data = response.json()
            return data[0]["flags"]["png"]  # ou "svg" se preferir vetorial
    except Exception:
        return None

# Formatar valores numéricos
def formatar_valor(valor):
    if isinstance(valor, (int, float)):
        return f"{valor:,.3f}".replace(",", ".")
    return valor

# Filtrar e formatar dados relevantes
def filtrar_dados_relevantes(dados_api):
    return {
        campos_relevantes[i]: formatar_valor(dados_api.get(i, "N/A"))
        for i in campos_relevantes if i in dados_api
    }

# Exibir dados em formato de tabela
def exibir_tabela_dados(dados_filtrados):
    df = pd.DataFrame(dados_filtrados.items(), columns=["Dados", "Valores"])
    st.table(df)

# Interface principal
def main():
    pais_pt = st.text_input('Digite o nome do país:').strip().title()

    if pais_pt:
        pais_en = traduzir_pais(pais_pt)

        if not pais_en:
            st.warning("Não foi possível traduzir o nome do país ou Verifique a ortografia. Tente Novamente.")
            return

        st.write(f"Buscando informações sobre: **{pais_pt}**")

        # Mostrar bandeira
        url_bandeira = obter_bandeira_url(pais_en)
        if url_bandeira:
            st.image(url_bandeira, caption=f'Bandeira de {pais_pt}', width=200)
        else:
            st.info("Não foi possível carregar a bandeira.")

        # Buscar e exibir dados
        dados = obter_dados_pais(pais_en)
        if dados:
            dados_filtrados = filtrar_dados_relevantes(dados)
            exibir_tabela_dados(dados_filtrados)
        else:
            st.warning("País não encontrado na base de dados. Tente outro nome ou verifique a ortografia.")

# Executa o app
if __name__ == "__main__":
    main()
