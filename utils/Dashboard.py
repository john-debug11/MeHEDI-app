import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
#import altair as alt
from htbuilder import div, big, h2, styles
from htbuilder.units import rem
import datetime

#from streamlit_elements import elements, mui, html, sync, lazy
#from streamlit_elements import nivo

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image


def dashboard_patient_satisf():
    img = Image.open('images/dashboard1_logo.png')
    st.image(img) 
    image3 = Image.open('images/Mehedi_logo2.png')
    
    color1 = "#1919e6"
    color2 = "#89CFF0"
    
    #serve per allargare margini da block-container
    st.markdown("""
    <style>
           .css-k1ih3n {
                padding-top: 0rem;
                padding-bottom: 4rem;
                padding-left: 4em;
                padding-right: 4rem;
            }
    </style>
    """, unsafe_allow_html=True)
    
    hide_img_fs = '''
        <style>
        button[title="View fullscreen"]{
            visibility: hidden;}
        </style>
        '''
    st.markdown(hide_img_fs, unsafe_allow_html=True)
   
    def display_dial(title, value, color):
     st.markdown(
         div(
             style=styles(
                 text_align="center",
                 color=color,
                 padding=(rem(0.8), 0, rem(3), 0),
             )
         )(
             h2(style=styles(font_size=rem(0.8), font_weight=600, padding=0))(title),
             big(style=styles(font_size=rem(3), font_weight=800, line_height=1))(
                 value
             ),
         ),
         unsafe_allow_html=True,
     )
    
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    #reading gsheet to dataframe
    sheet_url = "https://docs.google.com/spreadsheets/d/1OBEMIUloci4WV80D-yLhhoLMVQymy-TYlh7jwGXmND8/edit#gid=0"
    url_1 = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")
    df=pd.read_csv(url_1)
    
    #SIDEBAR
    st.sidebar.markdown("""<hr style="height:5px;border:none;color:#bfbfbf;background-color:#bfbfbf;" /> """, unsafe_allow_html=True)
    st.sidebar.info(
    """
    Questa è una webapp creata da che consente di valutare la Patient Satisfaction
    
    Web App URL: <https://xxx.streamlitapp.com>
    """
    )

    st.sidebar.title("Support")
    st.sidebar.info(
        """
        Per eventuali problemi nell'utilizzo app rivolgersi a: matteoballabio99@gmail.com
        """
    )
    a, b, c = st.sidebar.columns([0.2,1,0.2])
    with a:
        st.write("")
    with b:
        st.image(image3, width=170)
    with c:
        st.write("")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write("🔁 Filtra ciò che ti interessa")
    with col2:  
        st.multiselect("Fasce di età", df["Range_Età"].unique())
    with col3:
        st.multiselect("Sesso", df["Sesso"].unique())
    with col4:
        format = "%Y-%m-%d %H:%M:%S"  # format output
        current_time = datetime.datetime.now()
        slider = st.slider('Select date', 0, 100, 1)
    
    """
    #processi - strutture
    quality_str_m=df["Qualità struttura"].mean()
    quality_pro_m=df["Qualità processi"].mean()
    kpi_qua_str=round((quality_str_m+quality_pro_m)/2, 1)
    #kpi_qua_str=str(kpi_qua_str)*"%"
    df["KPI Percezione Strutturale"]=kpi_qua_str
    
    #sicurezza - qualità
    sicurezza=df["Sicurezza"].mean()
    quality_per=df["Qualità personale"].mean()
    pulizia=df["Pulizia"].mean()
    kpi_saf_str=round((sicurezza+quality_per+pulizia)/3, 1)
    #kpi_saf_str=str(kpi_saf_str)+"%"
    df["KPI Percezione Ambienti"]=kpi_saf_str
    
    #relational
    empatia=df["Empatia"].mean()
    chiare=df["Chiarezza"].mean()
    kpi_relazi=round((empatia+chiare)/2, 1)
    #kpi_relazi=str(kpi_relazi)+"%"
    df["KPI Percezione Relazionale"]=kpi_relazi
    
    #PSI
    kpi_psi=round((kpi_qua_str+kpi_saf_str+kpi_relazi)/3,1)
    
    #conditionally color kpi (rosso under 60)
    #l=[kpi_qua_str,kpi_saf_str,kpi_relazi,kpi_psi]
    #for i in l:
    
    g1, g2, g3, g4, g5 = st.columns(5)
    with g1:
        if kpi_qua_str < 65:
            color1="#EE4B2B"
        elif kpi_qua_str > 80:
            color1="#32CD32"
        else:
            color1 = "#1919e6"
        display_dial("KPI Percezione strutturale", str(kpi_qua_str)+"%", color1)
    with g2:
        if kpi_saf_str < 65:
            color1="#EE4B2B"
        elif kpi_saf_str > 80:
            color1="#32CD32"
        else:
            color1 = "#1919e6"
        display_dial("KPI Percezione ambienti", str(kpi_saf_str)+"%", color1)
    with g3:
        if kpi_relazi < 65:
            color1="#EE4B2B"
        elif kpi_relazi > 80:
            color1="#32CD32"
        else:
            color1 = "#1919e6"
        display_dial("KPI Percezione relazione", str(kpi_relazi)+"%", color1)
    with g4:
        if kpi_psi < 65:
            color1="#EE4B2B"
        elif kpi_psi > 80:
            color1="#32CD32"
        else:
            color1 = "#1919e6"
        display_dial("PSI (Patient Satisfaction Index)", str(kpi_psi)+"%", color1)
    with g5:
        display_dial("Numero Report inviati", str(len(df))+" rep", color1)
    
    
    css='''
    [data-testid="metric-container"] {
        width: fit-content;
        margin: auto;
    }
    
    [data-testid="metric-container"] > div {
        width: fit-content;
        margin: auto;
    }
    
    [data-testid="metric-container"] label {
        width: fit-content;
        margin: auto;
    }
    '''
    # I usually dump any scripts at the bottom of the page to avoid adding unwanted blank lines
    st.markdown(f'<style>{css}</style>',unsafe_allow_html=True)
        
     
    import matplotlib.pyplot as plt

    # data
    label = ["A", "B", "C"]
    val = [1,2,3]
    
    # append data and assign color
    label.append("")
    val.append(sum(val))  # 50% blank
    colors = ['red', 'blue', 'green', 'white']
    
    # plot
    fig = plt.figure(figsize=(8,6),dpi=100)
    ax = fig.add_subplot(1,1,1)
    ax.pie(val, labels=label, colors=colors)
    ax.add_artist(plt.Circle((0, 0), 0.6, color='white'))
    fig.show()
    
    
    col1, col2 = st.columns(2)
    with col1:
        st.header("Word Cloud Patient Form")
        text = Healthcare, hospital, sanità, monitoraggio, empatia, relazioni, sanità, pulizia,
                goals, health, sanità pubblica, esperienza, bene, healthcare, sanità, ambiente,
                pulito, sicuro, ospedale, ambulatorio, ambulatorio, healthcare, healthcare, sanità,
                dottori, professionisti, settore in crescita, medicina generale, cardiologia,
                radiologia, sanità, sanitario, health, health

        # Create and generate a word cloud image:
        wordcloud = WordCloud(
            background_color="#E4E3E3", width=450, height=500, colormap="Blues").generate(text)

        # Display the generated image:
        fig, ax = plt.subplots(facecolor="#E4E3E3")
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.subplots_adjust(left=-5, right=-2, top=-2, bottom=-5)
        plt.show()
        st.pyplot(fig)
   
    with col2:
        st.header("Health data")
        st.image("https://www.slideteam.net/media/catalog/product/cache/1280x720/p/a/patient_satisfaction_measurement_dashboard_service_ppt_show_vector_slide01.jpg")
     """
    df=st.write(df)
