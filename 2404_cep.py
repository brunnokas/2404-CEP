import streamlit as st
import requests
import json

st.set_page_config(page_title="Busca CEP", page_icon=":postbox:", layout="wide")
st.title("Consulta de CEP")

def buscar_cep(cep):
    """
    Busca informações de um CEP usando a API ViaCEP.
    Veja em https://viacep.com.br/ para mais detalhes sobre a API.
    Retorna um dicionário com os dados do CEP ou None em caso de erro.
    """
    try:
        r = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        r.raise_for_status()
        data = r.json()
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Erro na requisição: {e}")
        return None
    except json.JSONDecodeError:
        st.error("Erro ao decodificar a resposta JSON.")
        return None

def exibir_resultado(data):
    """Exibe os dados do CEP de forma elegante."""
    st.subheader("Resultado da Busca:")
    st.markdown(f"**CEP:** {data['cep']}")
    st.markdown(f"**Logradouro:** {data['logradouro']}")
    if data.get('complemento'):
        st.markdown(f"**Complemento:** {data['complemento']}")
    st.markdown(f"**Bairro:** {data['bairro']}")
    st.markdown(f"**Cidade:** {data['localidade']}")
    st.markdown(f"**UF:** {data['uf']}")

coll, col2 = st.columns([2, 1])

with coll:
    cep_p = st.text_input("Digite o CEP:", "", max_chars=8)

with col2:
    buscar_clicado = st.button("Buscar CEP")

if buscar_clicado:
    if cep_p.isdigit() and len(cep_p) == 8:
        resultado = buscar_cep(cep_p)
        if resultado and not resultado.get('erro'):
            exibir_resultado(resultado)
        elif resultado and resultado.get('erro'):
            st.warning("CEP não encontrado.")
    elif cep_p:
        st.warning("Digite um CEP válido com 8 dígitos.")

st.info("API de consulta de CEP utilizada: ViaCEP")
