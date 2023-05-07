import pandas as pd
import plotly.express as px
import streamlit as st
from numerize.numerize import numerize
from sqlalchemy import create_engine
import sqlalchemy
import random

def get_data(Postgre= False): 
    if not Postgre: 
        df= pd.read_csv("dataset_transacc_tdc_tdd_20230309.csv")
    else: 
        engine = sqlalchemy.create_engine('postgresql://alvaro_test:datathon@localhost:5432/Datathon')
        dbConnection = engine.connect();
        df = pd.read_sql("SELECT * FROM dataset_transacc_tdc_tdd", dbConnection);
    
    df["fecha_transaccion"]= pd.to_datetime(df["fecha_transaccion"])
    df["fecha_transaccion_date"]= df["fecha_transaccion"].dt.date
    df["fecha_transaccion_month"]= df['fecha_transaccion'].dt.month
    df["fecha_transaccion_year"]= df['fecha_transaccion'].dt.year
    return(df)

st.set_page_config(page_title="Dashboard for Banking User", 
                   layout= "wide", 
                   initial_sidebar_state= "expanded")
id= int(input("Introduce tu ID de Cliente: "))
df= get_data(Postgre=True)
df= df[df["id_cliente"]==id]


header_left, header_mid, header_right = st.columns ( [1, 3, 1] , gap = 'large')

with header_mid: 
    st.title("¡Bienvenido!\nConoce más sobre tus Hábitos Financieros.")

with st.sidebar:
    Campaign_filter= st.multiselect(label="Select Store Type", 
                                    options= df["giro_nombre"].unique(), 
                                    default= df["giro_nombre"].unique())
    Card_filter= st.multiselect(label="Select Card Used", 
                                    options= df["tipo_transaccion"].unique(), 
                                    default= df["tipo_transaccion"].unique())
    Month_filter= st.multiselect(label="Select Month Period", 
                                    options= df["fecha_transaccion_month"].unique(), 
                                    default= df["fecha_transaccion_month"].unique())
    Year_filter= st.multiselect(label="Select Year Period", 
                                    options= df["fecha_transaccion_year"].unique(), 
                                    default= df["fecha_transaccion_year"].unique())
    
    
df1= df.query('giro_nombre == @Campaign_filter & tipo_transaccion == @Card_filter & fecha_transaccion_month == @Month_filter & fecha_transaccion_year == @Year_filter')
total_transactions= float(df1["monto_transaccion"].count())
total_spent= float(df1["monto_transaccion"].sum())
total1, total2 = st.columns (2,gap='large')

with total1: 
    st.image("transac.png", use_column_width= "Auto")
    st.metric(label= "Total Transactions", value= numerize(total_transactions))
    
with total2: 
    st.image("total_amount.png", use_column_width= "Auto")
    st.metric(label= "Total Spent", value= numerize(total_spent))
    


df_grouped_date= df.groupby("fecha_transaccion_date").sum()[["monto_transaccion"]].reset_index()
st.title("Gasto Por Día")
st.line_chart(data=df_grouped_date, x="fecha_transaccion_date", y="monto_transaccion", use_container_width=True)

df_grouped_date_cum= df[["monto_transaccion", "fecha_transaccion_date"]].groupby("fecha_transaccion_date").sum().reset_index()
df_grouped_date_cum= df_grouped_date_cum.sort_values("fecha_transaccion_date", ascending= 1)
df_grouped_date_cum['monto_transaccion'] = df_grouped_date_cum['monto_transaccion'].cumsum()
st.title("Gasto Acumulado")
st.line_chart(data=df_grouped_date_cum, x="fecha_transaccion_date", y="monto_transaccion", use_container_width=True)

# Desarrollo futuro pendiente