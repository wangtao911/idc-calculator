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
        A_line = st.number_input('A机房百G专线',value=10.5,step=1.0)*10000
        #st.write('A机房百G专线：', A_line)

        B_line = st.number_input('B机房百G专线',value=16.0,step=1.0)*10000
        #st.write('B机房百G专线：', B_line)

        C_line = st.number_input('C机房百G专线',value=21.0,step=1.0)*10000
        #st.write('C机房百G专线：', C_line)

        D_line = st.number_input('D机房百G专线',value=5.0,step=1.0)*10000
        #st.write('D机房百G专线：', D_line)
    with col2:
        idc_power_price_dct['A-4.4-price'] = st.number_input('A机房机柜',value=4470,step=100)
        idc_power_price_dct['B-4.4-price'] = st.number_input('B机房机柜',value=4700,step=100)
        idc_power_price_dct['C-4.4-price'] = st.number_input('C机房机柜',value=2650,step=100)
        idc_power_price_dct['D-4.4-price'] = st.number_input('D机房机柜',value=6600,step=100)
        
    st.text('低速发展')
    low_tab_df = pd.DataFrame(
        [
            {'月':1,'440w服务器月增数':0,'4000w服务器月增数':0,'1500w服务器月增数':0,'百G专线条数':0},
            {'月':2,'440w服务器月增数':0,'4000w服务器月增数':0,'1500w服务器月增数':0,'百G专线条数':0},
        ]
    )
    low_edited_df = st.data_editor(low_tab_df,key="low",column_config={
            "440w服务器月增数": st.column_config.Column(
                width="small",
            ),
            "4000w服务器月增数": st.column_config.Column(
                width="small",
            ),
            "1500w服务器月增数": st.column_config.Column(
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
            {'月':1,'440w服务器月增数':0,'4000w服务器月增数':0,'1500w服务器月增数':0,'百G专线条数':0},
            {'月':2,'440w服务器月增数':0,'4000w服务器月增数':0,'1500w服务器月增数':0,'百G专线条数':0},
        ]
    )
    edited_df = st.data_editor(tab_df,column_config={
            "440w服务器月增数": st.column_config.Column(
                width="small",
            ),
            "4000w服务器月增数": st.column_config.Column(
                width="small",
            ),
            "1500w服务器月增数": st.column_config.Column(
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
            {'月':1,'440w服务器月增数':0,'4000w服务器月增数':0,'1500w服务器月增数':0,'百G专线条数':0},
            {'月':2,'440w服务器月增数':0,'4000w服务器月增数':0,'1500w服务器月增数':0,'百G专线条数':0},
        ]
    )
    high_edited_df = st.data_editor(high_tab_df,key="high",column_config={
            "440w服务器月增数": st.column_config.Column(
                width="small",
            ),
            "4000w服务器月增数": st.column_config.Column(
                width="small",
            ),
            "1500w服务器月增数": st.column_config.Column(
                width="small",
            ),
            "百G专线条数": st.column_config.Column(
                width="small",
            ),
        },
        num_rows="dynamic",height=200)
    



def make_final_df(df):

    df['S累计']=df['440w服务器月增数'].cumsum()
    df['计算累计']=df['4000w服务器月增数'].cumsum()
    df['推理累计']=df['1500w服务器月增数'].cumsum()
    df['S机柜']=np.ceil(df['S累计']/10)
    df['计算机柜']=np.ceil(df['计算累计'])
    df['推理机柜']=np.ceil(df['推理累计']/3)
    df['百G专线']=np.ceil(df['百G专线条数'])
    #st.dataframe(df)

    jigui_df=df[['月','S机柜','计算机柜','推理机柜','百G专线']]
    #st.dataframe(jigui_df)

    A_df=jigui_df[['月','S机柜','计算机柜','推理机柜','百G专线']]
    A_df['机柜成本']=(jigui_df['S机柜']+jigui_df['计算机柜']+jigui_df['推理机柜'])*idc_power_price_dct['A-4.4-price']
    A_df['专线成本']=(jigui_df['百G专线'])*A_line
    #st.text('A_df')
    #st.dataframe(A_df)

    B_df=jigui_df[['月','S机柜','计算机柜','推理机柜','百G专线']]
    B_df['机柜成本']=(jigui_df['S机柜']+jigui_df['计算机柜']+jigui_df['推理机柜'])*idc_power_price_dct['B-4.4-price']
    B_df['专线成本']=(jigui_df['百G专线'])*B_line
    #st.text('B_df')
    #st.dataframe(B_df)

    C_df=jigui_df[['月','S机柜','计算机柜','推理机柜','百G专线']]
    C_df['机柜成本']=(jigui_df['S机柜']+jigui_df['计算机柜']+jigui_df['推理机柜'])*idc_power_price_dct['C-4.4-price']
    C_df['专线成本']=(jigui_df['百G专线'])*C_line
    #st.text('C_df')
    #st.dataframe(C_df)

    D_df=jigui_df[['月','S机柜','计算机柜','推理机柜','百G专线']]
    D_df['机柜成本']=(jigui_df['S机柜']+jigui_df['计算机柜']+jigui_df['推理机柜'])*idc_power_price_dct['D-4.4-price']
    D_df['专线成本']=(jigui_df['百G专线'])*D_line
    #st.text('D_df')
    #st.dataframe(D_df)


    all_diqu_df=pd.DataFrame()
    all_diqu_df['月']=C_df['月']
    all_diqu_df['A机房成本']=A_df['机柜成本']+A_df['专线成本']
    all_diqu_df['B机房成本']=B_df['机柜成本']+B_df['专线成本']
    all_diqu_df['C机房成本']=C_df['机柜成本']+C_df['专线成本']
    all_diqu_df['D机房成本']=D_df['机柜成本']+D_df['专线成本']
    #st.dataframe(all_diqu_df)

    return all_diqu_df,jigui_df

st.image("https://p.ipic.vip/priovl.png")


#--低速
low_diqu_df,low_jigui_df = make_final_df(low_edited_df)
low_chart_data = pd.DataFrame(
    low_diqu_df,
    columns=['C机房成本', 'A机房成本', 'B机房成本','D机房成本'])


#--正常
all_diqu_df,jigui_df = make_final_df(edited_df)
chart_data = pd.DataFrame(
    all_diqu_df,
    columns=['C机房成本', 'A机房成本', 'B机房成本','D机房成本'])


#--高速
high_diqu_df,high_jigui_df = make_final_df(high_edited_df)
high_chart_data = pd.DataFrame(
    high_diqu_df,
    columns=['C机房成本', 'A机房成本', 'B机房成本','D机房成本'])


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