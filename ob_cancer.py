#importando as bibliotecas
import pandas as pd
import streamlit as st
import pickle

st.set_page_config(  # Alternate names: setup_page, page, layout
	layout='wide',  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state='auto',  # Can be "auto", "expanded", "collapsed"
	page_title='Preditor Câncer Colorretal',  # String or None. Strings get appended with "• Streamlit". 
	page_icon=None,  # String, anything supported by st.image, or None.
)
st.write('# Colorretal - Óbito por Câncer') 

st.write('### Insira os dados abaixo para fazer a predição')

#dados dos usuários com a função
def get_user_data():
    col1, col2 = st.columns(2)
    escolari = col1.radio('Escolaridade', ['1 - Analfabeto', '2 - Ens. Fund. Incompleto', '3 - Ens. Fund. Completo', '4 - Ensino Médio', '5 - Superior'])
    if escolari == 'Analfabeto':
        escolari = 1
    elif escolari == 'Ens. Fund. Incompleto':
        escolari = 2
    elif escolari == 'Ens. Fund. Completo':
        escolari = 3
    elif escolari == 'Ensino Médio':
        escolari = 4
    else:
        escolari = 5

    idade = col1.number_input('Idade', min_value=0, max_value=110, format='%i')

    sexo = col1.radio('Sexo', ['1 - Masculino', '2 - Feminino'])
    if sexo == '1 - Masculino':
        sexo = 1
    else:
        sexo = 2

    ibge = col1.number_input('Código IBGE', value=1234567, format='%i')

    catatend = col1.radio('Categoria de atendimento', ['1 - Convênio', '2 - SUS', '3 - Particular', '9 - Sem Informação'])
    if catatend == '1 - Convênio':
        catatend = 1
    elif catatend == '2 - SUS':
        catatend = 2
    elif catatend == '3 - Particular':
        catatend = 3
    else:
        catatend = 9

    diagprev = col1.radio('Diagnóstico previo', ['1 - Sem diagnóstico/Sem tratamento', '2 - Com diagnóstico/Sem tratamento'])
    if diagprev == '1 - Sem diagnóstico/Sem tratamento':
        diagprev = 1
    else:
        diagprev = 2

    ec = col1.selectbox('Estadiamento Clínico', ['I', 'II', 'IIA', 'IIB', 'IIC', 'III', 'IIIA', 'IIIB', 'IIIC', 'IV', 'IVA', 'IVB', 'IVC'])
    trathosp = col1.selectbox('Tratamento no Hospital', ['A - Cirurgia', 'B - Radioterapia', 'C - Quimioterapia', 'D - Cirurgia + Radioterapia', 'E - Cirurgia + Quimioterapia', 'F - Radioterapia + Quimioterapia', 'G - Cirurgia + Radioterapia + Quimioterapia', 'H - Cirurgia + Radioterapia + Quimioterapia + Hormonioterapia', 'I - Outras', 'J - Nenhum'])
    if trathosp == 'A - Cirurgia':
        trathosp = 'A'
    elif trathosp == 'B - Radioterapia':
        trathosp = 'B'
    elif trathosp == 'C - Quimioterapia':
        trathosp = 'C'
    elif trathosp == 'D - Cirurgia + Radioterapia':
        trathosp = 'D'
    elif trathosp == 'E - Cirurgia + Quimioterapia':
        trathosp = 'E'
    elif trathosp == 'F - Radioterapia + Quimioterapia':
        trathosp = 'F'
    elif trathosp == 'G - Cirurgia + Radioterapia + Quimioterapia':
        trathosp = 'G'
    elif trathosp == 'H - Cirurgia + Radioterapia + Quimioterapia + Hormonioterapia':
        trathosp = 'H'
    elif trathosp == 'I - Outras':
        trathosp = 'I'
    else:
        trathosp = 'J'

    nenhum = col1.radio('Tratamento recebido = nenhum', [0, 1])
    cirur = col1.radio('Tratamento recebido = cirurgia', [0, 1])
    radio = col1.radio('Tratamento recebido = radioterapia', [0, 1])
    quimio = col1.radio('Tratamento recebido = quimioterapia', [0, 1])
    horm = col2.radio('Tratamento recebido = hormonioterapia', [0, 1])
    tmo = col2.radio('Tratamento recebido = TMO', [0, 1])
    imuno = col2.radio('Tratamento recebido = imunoterapia', [0, 1])
    outros = col2.radio('Tratamento recebido = outros', [0, 1])
    nenhumant = col2.radio('Tratamento recebido fora do hospital e antes da admissão = nenhum', [0, 1])
    consdiag = col2.number_input('Diferença entre consulta e diagnóstico (dias)', value=10, format='%i')
    tratcons = col2.number_input('Diferença entre consulta e tratamento (dias)', value=10, format='%i')
    diagtrat = col2.number_input('Diferença entre diagnóstico e tratamento (dias)', value=10, format='%i')
    anodiag = col2.slider('Ano do diagnóstico', 1999, 2022, 2010)
    drs = col2.slider('DRS', 1, 17, 1)
    rras = col2.slider('RRAS', 1, 17, 1)
    recnenhum = col2.radio('Sem recidiva', [0, 1])
    ibgeaten = col2.number_input('Código IBGE de atendimento', value=1234567, format='%i')

    #dicionário para receber informações
    user_data = {'IDADE': idade, 'SEXO': sexo, 'IBGE': ibge, 'CATEATEND': catatend, 'DIAGPREV': diagprev, 'EC': ec, 'TRATHOSP': trathosp, 'NENHUM': nenhum, 'CIRURGIA': cirur, 'RADIO': radio, 'QUIMIO': quimio, 'HORMONIO': horm, 'TMO': tmo, 'IMUNO': imuno, 'OUTROS': outros, 'NENHUMANT': nenhumant, 'CONSDIAG': consdiag, 'TRATCONS': tratcons, 'DIAGTRAT': diagtrat, 'ANODIAG': anodiag, 'DRS': drs, 'RRAS': rras, 'RECNENHUM': recnenhum, 'IBGEATEN': ibgeaten, 'ESCOLARI_2': escolari
    }
    
    features = pd.DataFrame(user_data, index=[0])

    return features

def test_preprocessing(df, enc, norm, encoder_type='LabelEncoder', pca=None):
    df_aux = df.copy()

    # df_aux.fillna(0, inplace=True)

    list_categorical = df_aux.select_dtypes(include='object').columns

    if encoder_type == 'LabelEncoder':
        for col in list_categorical:
            df_aux.loc[~df_aux[col].isin(enc[col].classes_), col] = -1 
            df_aux.loc[df_aux[col].isin(enc[col].classes_), col] = enc[col].transform(df_aux[col][df_aux[col].isin(enc[col].classes_)])

    df_aux = norm.transform(df_aux)

    if pca != None:
        df_aux = pca.transform(df_aux)

    return df_aux

feat = get_user_data()

with open('ob_cancer_models.pkl', 'rb') as f:
    models = pickle.load(f)

xgb = models['xgboost']
enc = models['encoder']
norm = models['normalizer']

x_test = test_preprocessing(feat, enc, norm)


col1, col2, col3, col4, col5 = st.columns(5)
if col3.button('Realizar Predição do Modelo'):
    pred = xgb.predict(x_test)[0]
    st.write(f'## Resultado da previsão do modelo: {pred}')
    if pred == 1:
        st.write('### Óbito por câncer')
    else:
        st.write('### Sobrevivência por câncer')
