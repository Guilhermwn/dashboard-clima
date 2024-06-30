import streamlit as st
import requests
import pandas as pd
import datetime as dt
import time

st.set_page_config(
    page_title="Seu clima",
    page_icon="cloud",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title('Verificador de Clima') # header H1

st.write("""
Este é um programa Python chamado `Verificador de Clima`, que permite verificar 
o clima de uma cidade específica. O programa utiliza a API OpenWeatherMap.org 
para obter informações climáticas em tempo real.
""")

df = pd.read_csv('cidadesBrasil.csv', sep=';') # Dados com os nomes das cidades

cidade_series = df['Municipio']
estado_series = df['UF']
cidade_UF_series = cidade_series.str.cat(estado_series, sep=' - ')

# CRIAÇÃO DO LINK DE VERIFICAÇÃO DA API OPENWEATHERMAP.ORG
api_clima_key = '9ed06dc6e0e2d16f22f237aba9d94702'
api_clima_link = f"http://api.openweathermap.org/data/2.5/weather?appid={api_clima_key}&lang=pt_br&units=metric&q="

# =================================================================

st.divider()

st.write("""
#### Primeiramente escolha na caixa de seleção abaixo, o nome da sua cidade, ou qualquer cidade que você deseja verificar o estado climático atual.
<br>
""", 
unsafe_allow_html=True)

escolha_cidade = st.selectbox('Escolha uma cidade',
    cidade_UF_series,
    index = None,
    placeholder = "Selecione a cidade desejada", 
    help = "Basta escrever o nome da cidade que você deseja"
)



if escolha_cidade == None:
    url_clima = api_clima_link + "Aracaju"
    
else:
    escolha_cidade = escolha_cidade.split(' - ')[0]
    url_clima = api_clima_link + escolha_cidade

# REQUEST DO ARQUIVO JSON GERADO PELA API
acessar = requests.get(url_clima).json()

if acessar['cod'] != 200:
    st.warning('A cidade não foi encontrada nos registros, tente escolher outra', icon="⚠️")
    st.toast(f':green[{escolha_cidade}] Não encontrada', icon='😱')
else:
    if escolha_cidade == None:
        st.toast(f'Cidade padrão definida: :green[Aracaju]', icon='👍')
        pass
    else:
        st.success('Cidade encontrada, exibindo clima', icon="✅")
        st.toast(f':green[{escolha_cidade}] Encontrada', icon='🥳')
    # DADOS RETIRADOS DO ARQUIVO JSON
    descricao_clima = acessar['weather'][0]['description']
    temperatura_atual = acessar['main']['temp']
    sensacao_termica = acessar['main']['feels_like']
    umidade = acessar['main']['humidity']
    velocidade_vento = acessar['wind']['speed']
    cidade_clima = acessar['name']
    pais = acessar['sys']['country']
    nascer_sol = acessar['sys']['sunrise']
    por_sol = acessar['sys']['sunset']

    # hora_atual = dt.datetime.now()
    hora_atual = acessar['dt'] 

# ======== TRATAMENTO DOS DADOS ========
    # Formatação da Temperatura atual
    temperatura_atual_formatada = f"{temperatura_atual:.0f}"
    
    # Lógica do valor do delta na exibição métrica
    temperatura_diferencial = sensacao_termica - temperatura_atual
    if temperatura_diferencial >= 0:
        delta_cor = "normal"
        delta_valor = f"Diminuiu {temperatura_diferencial:.0f} ºc"
    elif temperatura_diferencial < 0:
        delta_cor = "inverse"
        delta_valor = f"Aumentou {temperatura_diferencial:.0f} ºc"

    
    nascer_sol_obj = dt.datetime.fromtimestamp(nascer_sol).strftime("Às %H horas e %M minutos")
    por_sol_obj = dt.datetime.fromtimestamp(por_sol).strftime("Às %H horas e %M minutos")
    # hora_atual_obj = dt.datetime.fromtimestamp(hora_atual).strftime("Às %H horas e %M minutos")

    
    data_atual_obj = dt.datetime.fromtimestamp(hora_atual).strftime("Dia %d do mês %m de %Y")
    hora_atual_obj = dt.datetime.fromtimestamp(hora_atual).strftime("%Hh %M min %S seg")
# ======== TRATAMENTO DOS DADOS ========

    # Exibe o nome da cidade se foi escolhida uma cidade no selectbox, se não foi escolhida uma cidade ele exibe "Aracaju"
    st.write(f"## Cidade - {escolha_cidade}" if escolha_cidade is not None else "## Cidade - Aracaju")

    with st.spinner('Carregando...'):
        time.sleep(1)

    coluna_esquerda, coluna_centro, coluna_direita = st.columns(3)
    with coluna_esquerda:
        st.divider()
        st.write("#### Informações da Temperatura")
        st.metric(f"Temperatura atual em {escolha_cidade}" if escolha_cidade is not None else "Temperatura atual em Aracaju", 
        str(temperatura_atual_formatada)+" ºC", 
        delta = delta_valor,
        delta_color = delta_cor)
        
        
    
    with coluna_centro:
        st.divider()
        st.write("#### Informações do Clima")
        st.write(f"Descrição: :green[{descricao_clima}]")
        st.write(f"Umidade: :green[{umidade}%]  ")
        st.write(f"Velocidade do Vento: :green[{velocidade_vento} km/h]")

        
    
    with coluna_direita:
        st.divider()
        st.write(f"#### Informações de Horário em {escolha_cidade}" if escolha_cidade is not None else "#### Informações de Horário em Aracaju")
        st.write(f"Data: :green[{data_atual_obj}]")
        st.write(f"Nascer do sol: :green[{nascer_sol_obj}]")
        st.write(f"Pôr do sol: :green[{por_sol_obj}]")
        #st.write(f"Horário atual: :green[{hora_atual_obj}]")


st.divider()

# =================================================================



