import streamlit as st

st.set_page_config(page_title = "Forecast App", initial_sidebar_state = "collapsed")

with st.sidebar:
    st.subheader("Selecionar dados")
    input = st.file_uploader('')
    input = True

    if input:
        with st.spinner('Loading data...'):
            df = 'DataFrame'
            columns = ['col_data','col_value']

            col1, col2 = st.beta_columns(2)
            with col1:
                date_col = st.selectbox("Seleciona a coluna de data",index=0,options=columns,key="date")
            with col2:
                metric_col = st.selectbox("Seleciona a coluna de metrica",index=1,options=columns,key="values")

    st.subheader("Parametros")
    with st.beta_expander("Horizon"):
        periods_input = st.number_input("Selecione quantos periodos futuros para previsão", min_value=1, max_value=366, value=30)

    with st.beta_expander("Seasonality"):
        seasonality = st.radio(label='Seasonality', options=['additive','multiplicative'])

    with st.beta_expander("Trend"):
        daily = st.checkbox("Daily")
        weekly = st.checkbox("Weekly")
        monthly = st.checkbox("Monthly")
        yearly = st.checkbox("Yearly")

    with st.beta_expander("Growth Model"):
        growth = st.radio(label="",options=['linear','logistic'])

        if growth == 'linear':
            growth_settings={
                'cap':1,
                'floor':0
            }
            cap = 1
            floor = 1
            #df['cap']=1
            #df['floor']=0

        if growth == 'logistic':
            st.info('Configure a saturacao')

            step = 0.05
            floor= st.slider('Floor',min_value=0.0,max_value=1.0,step=0.05)
            cap = st.slider('Cap',min_value=0.05,max_value=1.0,step=0.05)

            if floor >= cap:
                st.error('Configuracao invalida, Cap deve ser maior que o Floor')
                growth_settings={}
            else:
                growth_settings = {
                    'cap': cap,
                    'floor': floor
                }
                #df['cap']=cap
                #df['floor']=floor

    with st.beta_expander('Holidays'):
        holidays = st.checkbox('(Beta) Adicionar feriados ao modelo')

    with st.beta_expander('Hyperparameter'):
        seasonality_scale_values=[0.1, 1.0, 5.0, 10.0]
        changepoint_scale_values=[0.01, 0.1, 0.5, 1.0]

        changepoint_scale = st.select_slider(label='Changepoint prior scale',options=changepoint_scale_values)
        seasonality_scale = st.select_slider(label='Seasonality prior scale',options=seasonality_scale_values)