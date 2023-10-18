import streamlit as st
import pandas as pd
import locale
import numpy as np




locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def try_convert_to_float(x):
    try:
        return float(x)
    except ValueError:  
        return x


features= ['TICKER', 'PRECO', 'DY', 'P/L',' VPA', ' LIQUIDEZ MEDIA DIARIA', ' LPA', 'ROE']

st.write('''
         
      # Faça o Upload do seu arquivo com as informações das ações 
            
         ''')

st.write('''## Importante!''')
st.write('O arquivo deve ter os seguintes valores de cada ação:')
st.write(f'{features}')




def uploader():
    # Interface para carregar o arquivo CSV
    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

    # Se um arquivo for carregado, leia o CSV e transforme-o em um dataframe
    if uploaded_file is not None:
        stocks = pd.read_csv(uploaded_file, sep=';')
        stocks = stocks[['TICKER', 'PRECO', 'DY', 'P/L',' VPA', ' LPA', 'ROE', ' LIQUIDEZ MEDIA DIARIA']]
        stocks=stocks.dropna()
        stocks['P/L'] = stocks['P/L'].apply(lambda x: locale.atof(x))

        stocks['DY'] = stocks['DY'].apply(lambda x: locale.atof(x))
        stocks['PRECO'] = stocks['PRECO'].apply(lambda x: locale.atof(x))
        stocks[' VPA'] = stocks[' VPA'].apply(lambda x: locale.atof(x))
        stocks[' LPA'] = stocks[' LPA'].apply(lambda x: locale.atof(x))
        stocks['ROE'] = stocks['ROE'].apply(lambda x: locale.atof(x))
        stocks=stocks[(stocks['P/L']>3) & (stocks['DY']>5) & (stocks[' LIQUIDEZ MEDIA DIARIA'].apply(lambda x: locale.atof(x))>10000000)]
        best_stocks = stocks.sort_values(by=['P/L']).head(30)
        best_stocks['PRECO ALVO']=np.sqrt(22.5*best_stocks[' VPA']*best_stocks[' LPA'])
        best_stocks['MARGEM DE SEGURANÇA'] = (best_stocks['PRECO ALVO']-best_stocks['PRECO'])/(best_stocks['PRECO ALVO'])
        best_stocks = best_stocks.sort_values(by='MARGEM DE SEGURANÇA', ascending=False)
        best_stocks['INDICACAO']=pd.qcut(best_stocks['MARGEM DE SEGURANÇA'], 4, labels=['Muito Barato','Barato', 'Preço OK', 'Caro'][::-1])
        best_stocks = best_stocks.applymap(try_convert_to_float)
        return best_stocks
        


df = uploader()


    
st.dataframe(df)

