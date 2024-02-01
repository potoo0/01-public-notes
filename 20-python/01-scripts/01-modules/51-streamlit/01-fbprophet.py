import numpy as np
import pandas as pd
from prophet import Prophet

import streamlit as st
from prophet.plot import plot_plotly, plot_components_plotly


# run: streamlit run .\01-fbprophet.py
data_num = 100


@st.cache
def read_data(data_num):
    # df = pd.read_csv(
    #     csv,
    #     sep=r'\s+',
    #     names=[1, 'y', 2, 'ds', 3]
    # ).drop(columns=[1, 2, 3])
    idx = np.arange(1, data_num, np.pi / 10)
    df = pd.DataFrame(
        data={'y': np.sin(idx) * 10},
        index=idx
    )
    return df


@st.cache(hash_funcs={Prophet: id})
def train(df):
    # 训练
    m = Prophet()
    m.fit(df)

    return m


@st.cache(allow_output_mutation=True)
def pred(m, period):
    # 预测
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    return forecast


df = read_data(data_num)
m = train(df)

st.title('plot prophet res')

periods = st.slider('Select days')

forecast = pred(m, periods)

st.write(plot_plotly(m, forecast))
