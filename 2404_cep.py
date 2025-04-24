import streamlit as st
import requests
import json

# Configuração da página
st.set_page_config(page_title="Busca CEP", page_icon=":postbox:", layout="wide")
st.title("📬 Consulta de CEP")

# Função para buscar o CEP
def buscar_cep(cep):
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

# Função para exibir os dados
def exibir_resultado(data):
    st.subheader("📦 Resultado da Busca:")
    st.markdown(f"**CEP:** {data['cep']}")
    st.markdown(f"**Logradouro:** {data['logradouro']}")
    if data.get('complemento'):
        st.markdown(f"**Complemento:** {data['complemento']}")
    st.markdown(f"**Bairro:** {data['bairro']}")
    st.markdown(f"**Cidade:** {data['localidade']}")
    st.markdown(f"**UF:** {data['uf']}")
    st.markdown(f"**DDD:** {data['ddd']}")

# Estilo visual
st.markdown(
    """
    <style>
    .stTextInput > div > div > input {
        font-size: 18px;
        padding: 10px;
    }
    .stButton > button {
        font-size: 16px;
        padding: 8px 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Layout de entrada
col1, col2 = st.columns([2, 1])

with col1:
    entrada = st.text_input("Digite o CEP:", "", max_chars=9)
    cep_p = ''.join(filter(str.isdigit, entrada))[:8]  # Garante apenas até 8 dígitos numéricos

with col2:
    buscar_clicado = st.button("🔍 Buscar CEP")

# Histórico de buscas
if "historico" not in st.session_state:
    st.session_state.historico = []

# Quando o botão for clicado
if buscar_clicado:
    if cep_p and len(cep_p) == 8:
        with st.spinner("🔄 Buscando informações..."):
            resultado = buscar_cep(cep_p)

        if resultado and not resultado.get('erro'):
            exibir_resultado(resultado)

            if resultado['cep'] not in st.session_state.historico:
                st.session_state.historico.append(resultado['cep'])

        elif resultado and resultado.get('erro'):
            st.warning("🚫 CEP não encontrado.")
    elif cep_p:
        st.warning("⚠️ O CEP deve conter exatamente 8 números.")

# Histórico de CEPs consultados
if st.session_state.historico:
    st.markdown("### 🕘 Histórico de CEPs Consultados:")
    for cep in reversed(st.session_state.historico[-5:]):  # Mostra os últimos 5
        st.markdown(f"- {cep}")

# Rodapé
st.info("🔗 API utilizada: [ViaCEP](https://viacep.com.br/)")
