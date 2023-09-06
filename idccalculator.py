# idc-calculator
import streamlit as st
import datetime
import pandas as pd
import numpy as np
st.set_page_config(
    page_title="IDC Cost Calculator v0.2",
    page_icon='❇️',
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# A Cost Calculator of IDC. \n # This is an *Simple* app! \n by WangTao"
    }
)

idc_power_price_dct={}
with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        tj_line = st.number_input('天津/廊坊百G专线',value=10.5,step=1.0)*10000
        #st.write('天津/廊坊百G专线：', tj_line)

        hl_line = st.number_input('怀来百G专线',value=16.0,step=1.0)*10000
        #st.write('怀来百G专线：', hl_line)

        nm_line = st.number_input('内蒙百G专线',value=21.0,step=1.0)*10000
        #st.write('内蒙百G专线：', nm_line)

        bj_line = st.number_input('北京百G专线',value=5.0,step=1.0)*10000
        #st.write('北京百G专线：', bj_line)
    with col2:
        idc_power_price_dct['tj-4.4-price'] = st.number_input('天津/廊坊机柜',value=4470,step=100)
        idc_power_price_dct['hl-4.4-price'] = st.number_input('怀来机柜',value=4700,step=100)
        idc_power_price_dct['nm-4.4-price'] = st.number_input('内蒙机柜',value=2650,step=100)
        idc_power_price_dct['bj-4.4-price'] = st.number_input('北京机柜',value=6600,step=100)
        
    st.text('低速发展')
    low_tab_df = pd.DataFrame(
        [
            {'月':1,'S机型按月增加台数':0,'计算按月增加台数':0,'推理按月增加台数':0,'百G专线条数':0},
            {'月':2,'S机型按月增加台数':0,'计算按月增加台数':0,'推理按月增加台数':0,'百G专线条数':0},
        ]
    )
    low_edited_df = st.data_editor(low_tab_df,key="low",column_config={
            "S机型按月增加台数": st.column_config.Column(
                width="small",
            ),
            "计算按月增加台数": st.column_config.Column(
                width="small",
            ),
            "推理按月增加台数": st.column_config.Column(
                width="small",
            ),
            "百G专线条数": st.column_config.Column(
                width="small",
            ),
        },
        num_rows="dynamic",height=200)

    st.text('正常发展')
    tab_df = pd.DataFrame(
        [
            {'月':1,'S机型按月增加台数':0,'计算按月增加台数':0,'推理按月增加台数':0,'百G专线条数':0},
            {'月':2,'S机型按月增加台数':0,'计算按月增加台数':0,'推理按月增加台数':0,'百G专线条数':0},
        ]
    )
    edited_df = st.data_editor(tab_df,column_config={
            "S机型按月增加台数": st.column_config.Column(
                width="small",
            ),
            "计算按月增加台数": st.column_config.Column(
                width="small",
            ),
            "推理按月增加台数": st.column_config.Column(
                width="small",
            ),
            "百G专线条数": st.column_config.Column(
                width="small",
            ),
        },key="nor",
        num_rows="dynamic",height=200)
    
    st.text('高速发展')
    high_tab_df = pd.DataFrame(
        [
            {'月':1,'S机型按月增加台数':0,'计算按月增加台数':0,'推理按月增加台数':0,'百G专线条数':0},
            {'月':2,'S机型按月增加台数':0,'计算按月增加台数':0,'推理按月增加台数':0,'百G专线条数':0},
        ]
    )
    high_edited_df = st.data_editor(high_tab_df,key="high",column_config={
            "S机型按月增加台数": st.column_config.Column(
                width="small",
            ),
            "计算按月增加台数": st.column_config.Column(
                width="small",
            ),
            "推理按月增加台数": st.column_config.Column(
                width="small",
            ),
            "百G专线条数": st.column_config.Column(
                width="small",
            ),
        },
        num_rows="dynamic",height=200)
    



def make_final_df(df):

    df['S累计']=df['S机型按月增加台数'].cumsum()
    df['计算累计']=df['计算按月增加台数'].cumsum()
    df['推理累计']=df['推理按月增加台数'].cumsum()
    df['S机柜']=np.ceil(df['S累计']/10)
    df['计算机柜']=np.ceil(df['计算累计'])
    df['推理机柜']=np.ceil(df['推理累计']/3)
    df['百G专线']=np.ceil(df['百G专线条数'])
    #st.dataframe(df)

    jigui_df=df[['月','S机柜','计算机柜','推理机柜','百G专线']]
    #st.dataframe(jigui_df)

    nm_df=jigui_df[['月','S机柜','计算机柜','推理机柜','百G专线']]
    nm_df['机柜成本']=(jigui_df['S机柜']+jigui_df['计算机柜']+jigui_df['推理机柜'])*idc_power_price_dct['nm-4.4-price']
    nm_df['专线成本']=(jigui_df['百G专线'])*nm_line
    #st.text('nm_df')
    #st.dataframe(nm_df)

    tj_df=jigui_df[['月','S机柜','计算机柜','推理机柜','百G专线']]
    tj_df['机柜成本']=(jigui_df['S机柜']+jigui_df['计算机柜']+jigui_df['推理机柜'])*idc_power_price_dct['tj-4.4-price']
    tj_df['专线成本']=(jigui_df['百G专线'])*tj_line
    #st.text('tj_df')
    #st.dataframe(tj_df)

    hl_df=jigui_df[['月','S机柜','计算机柜','推理机柜','百G专线']]
    hl_df['机柜成本']=(jigui_df['S机柜']+jigui_df['计算机柜']+jigui_df['推理机柜'])*idc_power_price_dct['hl-4.4-price']
    hl_df['专线成本']=(jigui_df['百G专线'])*hl_line
    #st.text('hl_df')
    #st.dataframe(hl_df)

    bj_df=jigui_df[['月','S机柜','计算机柜','推理机柜','百G专线']]
    bj_df['机柜成本']=(jigui_df['S机柜']+jigui_df['计算机柜']+jigui_df['推理机柜'])*idc_power_price_dct['bj-4.4-price']
    bj_df['专线成本']=(jigui_df['百G专线'])*bj_line
    #st.text('bj_df')
    #st.dataframe(bj_df)


    all_diqu_df=pd.DataFrame()
    all_diqu_df['月']=nm_df['月']
    all_diqu_df['内蒙成本']=nm_df['机柜成本']+nm_df['专线成本']
    all_diqu_df['天津成本']=tj_df['机柜成本']+tj_df['专线成本']
    all_diqu_df['怀来成本']=hl_df['机柜成本']+hl_df['专线成本']
    all_diqu_df['北京成本']=bj_df['机柜成本']+bj_df['专线成本']
    #st.dataframe(all_diqu_df)

    return all_diqu_df,jigui_df

st.image("https://p.ipic.vip/priovl.png")


#--低速
low_diqu_df,low_jigui_df = make_final_df(low_edited_df)
low_chart_data = pd.DataFrame(
    low_diqu_df,
    columns=['内蒙成本', '天津成本', '怀来成本','北京成本'])


#--正常
all_diqu_df,jigui_df = make_final_df(edited_df)
chart_data = pd.DataFrame(
    all_diqu_df,
    columns=['内蒙成本', '天津成本', '怀来成本','北京成本'])


#--高速
high_diqu_df,high_jigui_df = make_final_df(high_edited_df)
high_chart_data = pd.DataFrame(
    high_diqu_df,
    columns=['内蒙成本', '天津成本', '怀来成本','北京成本'])


col1, col2, col3 = st.columns([3,1,1])
with col1:
    st.title(':red[低速]发展')
    st.line_chart(low_chart_data)
with col2:
    st.title('专线')
    #st.dataframe(low_jigui_df.tail(6))
    st.line_chart(low_jigui_df[['百G专线']])
with col3:
    st.title('机柜')
    st.line_chart(low_jigui_df[['S机柜','计算机柜','推理机柜','百G专线']]) 


col1, col2, col3 = st.columns([3,1,1])
with col1:
    st.title(':green[正常]发展')
    st.line_chart(chart_data)
with col2:
    st.title('专线')
    #st.dataframe(jigui_df.tail(6))
    st.line_chart(jigui_df[['百G专线']])
with col3:
    st.title('机柜')
    st.line_chart(jigui_df[['S机柜','计算机柜','推理机柜','百G专线']])

col1, col2, col3 = st.columns([3,1,1])
with col1:
    st.title(':blue[高速]发展')
    st.line_chart(high_chart_data)
with col2:
    st.title('专线')
    #st.dataframe(high_jigui_df.tail(6))
    st.line_chart(high_jigui_df[['百G专线']])
with col3:
    st.title('机柜')
    st.line_chart(high_jigui_df[['S机柜','计算机柜','推理机柜','百G专线']])