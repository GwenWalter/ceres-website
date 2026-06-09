import streamlit as st


import pandas as pd
import requests

'''
# 🌾​ Ceres AI
### Prédiction du rendement de blé en France par département grâce au machine learning
'''
st.set_page_config(
    page_title="Prediction Blé", # => Quick reference - Streamlit
    page_icon="​🌾​",
    layout="centered", # wide
    initial_sidebar_state="auto") # collapsed

########### COUPLES(dept/annee) DISPO DANS X_test ###########

couples = [{'DEPT_ID': '30', 'harvest_year': 2014},
 {'DEPT_ID': '44', 'harvest_year': 2016},
 {'DEPT_ID': '27', 'harvest_year': 2013},
 {'DEPT_ID': '77', 'harvest_year': 2012},
 {'DEPT_ID': '87', 'harvest_year': 2012},
 {'DEPT_ID': '53', 'harvest_year': 2016},
 {'DEPT_ID': '26', 'harvest_year': 2010},
 {'DEPT_ID': '48', 'harvest_year': 2017},
 {'DEPT_ID': '22', 'harvest_year': 2014},
 {'DEPT_ID': '72', 'harvest_year': 2010},
 {'DEPT_ID': '60', 'harvest_year': 2021},
 {'DEPT_ID': '42', 'harvest_year': 2022},
 {'DEPT_ID': '16', 'harvest_year': 2012},
 {'DEPT_ID': '65', 'harvest_year': 2019},
 {'DEPT_ID': '35', 'harvest_year': 2013},
 {'DEPT_ID': '31', 'harvest_year': 2018},
 {'DEPT_ID': '70', 'harvest_year': 2019},
 {'DEPT_ID': '73', 'harvest_year': 2021},
 {'DEPT_ID': '30', 'harvest_year': 2019},
 {'DEPT_ID': '50', 'harvest_year': 2020},
 {'DEPT_ID': '34', 'harvest_year': 2010},
 {'DEPT_ID': '47', 'harvest_year': 2013},
 {'DEPT_ID': '15', 'harvest_year': 2021},
 {'DEPT_ID': '91', 'harvest_year': 2016},
 {'DEPT_ID': '07', 'harvest_year': 2020},
 {'DEPT_ID': '09', 'harvest_year': 2017},
 {'DEPT_ID': '39', 'harvest_year': 2013},
 {'DEPT_ID': '44', 'harvest_year': 2018},
 {'DEPT_ID': '16', 'harvest_year': 2016},
 {'DEPT_ID': '32', 'harvest_year': 2014},
 {'DEPT_ID': '72', 'harvest_year': 2022},
 {'DEPT_ID': '67', 'harvest_year': 2013},
 {'DEPT_ID': '36', 'harvest_year': 2012},
 {'DEPT_ID': '25', 'harvest_year': 2022},
 {'DEPT_ID': '47', 'harvest_year': 2023},
 {'DEPT_ID': '07', 'harvest_year': 2010},
 {'DEPT_ID': '41', 'harvest_year': 2020},
 {'DEPT_ID': '37', 'harvest_year': 2020},
 {'DEPT_ID': '42', 'harvest_year': 2018},
 {'DEPT_ID': '16', 'harvest_year': 2010},
 {'DEPT_ID': '39', 'harvest_year': 2014},
 {'DEPT_ID': '71', 'harvest_year': 2024},
 {'DEPT_ID': '90', 'harvest_year': 2020},
 {'DEPT_ID': '34', 'harvest_year': 2014},
 {'DEPT_ID': '38', 'harvest_year': 2023},
 {'DEPT_ID': '66', 'harvest_year': 2019},
 {'DEPT_ID': '36', 'harvest_year': 2020},
 {'DEPT_ID': '69', 'harvest_year': 2011},
 {'DEPT_ID': '55', 'harvest_year': 2016},
 {'DEPT_ID': '54', 'harvest_year': 2019},
 {'DEPT_ID': '19', 'harvest_year': 2016},
 {'DEPT_ID': '19', 'harvest_year': 2010},
 {'DEPT_ID': '02', 'harvest_year': 2015},
 {'DEPT_ID': '62', 'harvest_year': 2015},
 {'DEPT_ID': '50', 'harvest_year': 2017},
 {'DEPT_ID': '89', 'harvest_year': 2020},
 {'DEPT_ID': '62', 'harvest_year': 2014},
 {'DEPT_ID': '51', 'harvest_year': 2010},
 {'DEPT_ID': '41', 'harvest_year': 2016},
 {'DEPT_ID': '84', 'harvest_year': 2017},
 {'DEPT_ID': '82', 'harvest_year': 2023},
 {'DEPT_ID': '31', 'harvest_year': 2010},
 {'DEPT_ID': '55', 'harvest_year': 2021},
 {'DEPT_ID': '77', 'harvest_year': 2014},
 {'DEPT_ID': '07', 'harvest_year': 2011},
 {'DEPT_ID': '18', 'harvest_year': 2018},
 {'DEPT_ID': '04', 'harvest_year': 2013},
 {'DEPT_ID': '30', 'harvest_year': 2013},
 {'DEPT_ID': '36', 'harvest_year': 2014},
 {'DEPT_ID': '95', 'harvest_year': 2024},
 {'DEPT_ID': '59', 'harvest_year': 2022},
 {'DEPT_ID': '66', 'harvest_year': 2011},
 {'DEPT_ID': '56', 'harvest_year': 2024},
 {'DEPT_ID': '49', 'harvest_year': 2013},
 {'DEPT_ID': '05', 'harvest_year': 2021},
 {'DEPT_ID': '07', 'harvest_year': 2013},
 {'DEPT_ID': '27', 'harvest_year': 2017},
 {'DEPT_ID': '38', 'harvest_year': 2018},
 {'DEPT_ID': '33', 'harvest_year': 2020},
 {'DEPT_ID': '05', 'harvest_year': 2018},
 {'DEPT_ID': '46', 'harvest_year': 2021},
 {'DEPT_ID': '12', 'harvest_year': 2010},
 {'DEPT_ID': '83', 'harvest_year': 2023},
 {'DEPT_ID': '48', 'harvest_year': 2015},
 {'DEPT_ID': '61', 'harvest_year': 2016},
 {'DEPT_ID': '21', 'harvest_year': 2016},
 {'DEPT_ID': '85', 'harvest_year': 2010},
 {'DEPT_ID': '95', 'harvest_year': 2019},
 {'DEPT_ID': '95', 'harvest_year': 2020},
 {'DEPT_ID': '59', 'harvest_year': 2017},
 {'DEPT_ID': '07', 'harvest_year': 2017},
 {'DEPT_ID': '03', 'harvest_year': 2012},
 {'DEPT_ID': '88', 'harvest_year': 2018},
 {'DEPT_ID': '49', 'harvest_year': 2023},
 {'DEPT_ID': '52', 'harvest_year': 2015},
 {'DEPT_ID': '68', 'harvest_year': 2023},
 {'DEPT_ID': '39', 'harvest_year': 2022},
 {'DEPT_ID': '10', 'harvest_year': 2013},
 {'DEPT_ID': '40', 'harvest_year': 2012},
 {'DEPT_ID': '61', 'harvest_year': 2011},
 {'DEPT_ID': '86', 'harvest_year': 2019},
 {'DEPT_ID': '37', 'harvest_year': 2011},
 {'DEPT_ID': '39', 'harvest_year': 2015},
 {'DEPT_ID': '35', 'harvest_year': 2014},
 {'DEPT_ID': '03', 'harvest_year': 2020},
 {'DEPT_ID': '29', 'harvest_year': 2016},
 {'DEPT_ID': '77', 'harvest_year': 2016},
 {'DEPT_ID': '63', 'harvest_year': 2021},
 {'DEPT_ID': '54', 'harvest_year': 2020},
 {'DEPT_ID': '50', 'harvest_year': 2022},
 {'DEPT_ID': '63', 'harvest_year': 2018},
 {'DEPT_ID': '44', 'harvest_year': 2021},
 {'DEPT_ID': '16', 'harvest_year': 2015},
 {'DEPT_ID': '28', 'harvest_year': 2020},
 {'DEPT_ID': '78', 'harvest_year': 2020},
 {'DEPT_ID': '23', 'harvest_year': 2023},
 {'DEPT_ID': '07', 'harvest_year': 2016},
 {'DEPT_ID': '51', 'harvest_year': 2023},
 {'DEPT_ID': '78', 'harvest_year': 2024},
 {'DEPT_ID': '21', 'harvest_year': 2018},
 {'DEPT_ID': '73', 'harvest_year': 2024},
 {'DEPT_ID': '50', 'harvest_year': 2015},
 {'DEPT_ID': '79', 'harvest_year': 2024},
 {'DEPT_ID': '89', 'harvest_year': 2016},
 {'DEPT_ID': '32', 'harvest_year': 2024},
 {'DEPT_ID': '94', 'harvest_year': 2017},
 {'DEPT_ID': '72', 'harvest_year': 2021},
 {'DEPT_ID': '10', 'harvest_year': 2024},
 {'DEPT_ID': '43', 'harvest_year': 2012},
 {'DEPT_ID': '34', 'harvest_year': 2021},
 {'DEPT_ID': '03', 'harvest_year': 2018},
 {'DEPT_ID': '54', 'harvest_year': 2017},
 {'DEPT_ID': '54', 'harvest_year': 2012},
 {'DEPT_ID': '24', 'harvest_year': 2012},
 {'DEPT_ID': '04', 'harvest_year': 2012},
 {'DEPT_ID': '79', 'harvest_year': 2010},
 {'DEPT_ID': '08', 'harvest_year': 2022},
 {'DEPT_ID': '65', 'harvest_year': 2012},
 {'DEPT_ID': '61', 'harvest_year': 2010},
 {'DEPT_ID': '58', 'harvest_year': 2011},
 {'DEPT_ID': '02', 'harvest_year': 2016},
 {'DEPT_ID': '10', 'harvest_year': 2017},
 {'DEPT_ID': '87', 'harvest_year': 2022},
 {'DEPT_ID': '86', 'harvest_year': 2014},
 {'DEPT_ID': '49', 'harvest_year': 2019},
 {'DEPT_ID': '93', 'harvest_year': 2022},
 {'DEPT_ID': '13', 'harvest_year': 2019},
 {'DEPT_ID': '23', 'harvest_year': 2020},
 {'DEPT_ID': '50', 'harvest_year': 2023},
 {'DEPT_ID': '94', 'harvest_year': 2015},
 {'DEPT_ID': '49', 'harvest_year': 2021},
 {'DEPT_ID': '21', 'harvest_year': 2021},
 {'DEPT_ID': '16', 'harvest_year': 2018},
 {'DEPT_ID': '47', 'harvest_year': 2014},
 {'DEPT_ID': '79', 'harvest_year': 2022},
 {'DEPT_ID': '43', 'harvest_year': 2010},
 {'DEPT_ID': '66', 'harvest_year': 2018},
 {'DEPT_ID': '45', 'harvest_year': 2017},
 {'DEPT_ID': '26', 'harvest_year': 2016},
 {'DEPT_ID': '85', 'harvest_year': 2014},
 {'DEPT_ID': '15', 'harvest_year': 2018},
 {'DEPT_ID': '03', 'harvest_year': 2022},
 {'DEPT_ID': '26', 'harvest_year': 2018},
 {'DEPT_ID': '32', 'harvest_year': 2019},
 {'DEPT_ID': '04', 'harvest_year': 2023},
 {'DEPT_ID': '47', 'harvest_year': 2012},
 {'DEPT_ID': '01', 'harvest_year': 2024},
 {'DEPT_ID': '84', 'harvest_year': 2015},
 {'DEPT_ID': '21', 'harvest_year': 2012},
 {'DEPT_ID': '21', 'harvest_year': 2017},
 {'DEPT_ID': '76', 'harvest_year': 2014},
 {'DEPT_ID': '83', 'harvest_year': 2013},
 {'DEPT_ID': '63', 'harvest_year': 2016},
 {'DEPT_ID': '28', 'harvest_year': 2022},
 {'DEPT_ID': '08', 'harvest_year': 2016},
 {'DEPT_ID': '12', 'harvest_year': 2012},
 {'DEPT_ID': '43', 'harvest_year': 2024},
 {'DEPT_ID': '29', 'harvest_year': 2019},
 {'DEPT_ID': '57', 'harvest_year': 2016},
 {'DEPT_ID': '54', 'harvest_year': 2013},
 {'DEPT_ID': '34', 'harvest_year': 2016},
 {'DEPT_ID': '45', 'harvest_year': 2014},
 {'DEPT_ID': '69', 'harvest_year': 2022},
 {'DEPT_ID': '50', 'harvest_year': 2013},
 {'DEPT_ID': '66', 'harvest_year': 2023},
 {'DEPT_ID': '83', 'harvest_year': 2016},
 {'DEPT_ID': '16', 'harvest_year': 2024},
 {'DEPT_ID': '43', 'harvest_year': 2022},
 {'DEPT_ID': '69', 'harvest_year': 2013},
 {'DEPT_ID': '47', 'harvest_year': 2010},
 {'DEPT_ID': '04', 'harvest_year': 2024},
 {'DEPT_ID': '76', 'harvest_year': 2012},
 {'DEPT_ID': '49', 'harvest_year': 2016},
 {'DEPT_ID': '07', 'harvest_year': 2023},
 {'DEPT_ID': '11', 'harvest_year': 2023},
 {'DEPT_ID': '19', 'harvest_year': 2020},
 {'DEPT_ID': '62', 'harvest_year': 2023},
 {'DEPT_ID': '04', 'harvest_year': 2010},
 {'DEPT_ID': '10', 'harvest_year': 2011},
 {'DEPT_ID': '50', 'harvest_year': 2024},
 {'DEPT_ID': '54', 'harvest_year': 2022},
 {'DEPT_ID': '22', 'harvest_year': 2024},
 {'DEPT_ID': '34', 'harvest_year': 2013},
 {'DEPT_ID': '35', 'harvest_year': 2012},
 {'DEPT_ID': '26', 'harvest_year': 2024},
 {'DEPT_ID': '85', 'harvest_year': 2022},
 {'DEPT_ID': '67', 'harvest_year': 2023},
 {'DEPT_ID': '85', 'harvest_year': 2024},
 {'DEPT_ID': '25', 'harvest_year': 2016},
 {'DEPT_ID': '57', 'harvest_year': 2011},
 {'DEPT_ID': '80', 'harvest_year': 2017},
 {'DEPT_ID': '57', 'harvest_year': 2015},
 {'DEPT_ID': '70', 'harvest_year': 2014},
 {'DEPT_ID': '65', 'harvest_year': 2016},
 {'DEPT_ID': '27', 'harvest_year': 2011},
 {'DEPT_ID': '05', 'harvest_year': 2014},
 {'DEPT_ID': '15', 'harvest_year': 2017},
 {'DEPT_ID': '63', 'harvest_year': 2011},
 {'DEPT_ID': '03', 'harvest_year': 2024},
 {'DEPT_ID': '12', 'harvest_year': 2019},
 {'DEPT_ID': '34', 'harvest_year': 2024},
 {'DEPT_ID': '03', 'harvest_year': 2021},
 {'DEPT_ID': '59', 'harvest_year': 2019},
 {'DEPT_ID': '12', 'harvest_year': 2014},
 {'DEPT_ID': '78', 'harvest_year': 2019},
 {'DEPT_ID': '80', 'harvest_year': 2010},
 {'DEPT_ID': '57', 'harvest_year': 2012},
 {'DEPT_ID': '76', 'harvest_year': 2020},
 {'DEPT_ID': '54', 'harvest_year': 2024},
 {'DEPT_ID': '08', 'harvest_year': 2023},
 {'DEPT_ID': '78', 'harvest_year': 2022},
 {'DEPT_ID': '10', 'harvest_year': 2010},
 {'DEPT_ID': '48', 'harvest_year': 2021},
 {'DEPT_ID': '59', 'harvest_year': 2012},
 {'DEPT_ID': '60', 'harvest_year': 2020},
 {'DEPT_ID': '30', 'harvest_year': 2023},
 {'DEPT_ID': '14', 'harvest_year': 2021},
 {'DEPT_ID': '43', 'harvest_year': 2018},
 {'DEPT_ID': '67', 'harvest_year': 2012},
 {'DEPT_ID': '16', 'harvest_year': 2014},
 {'DEPT_ID': '44', 'harvest_year': 2017},
 {'DEPT_ID': '04', 'harvest_year': 2019},
 {'DEPT_ID': '65', 'harvest_year': 2010},
 {'DEPT_ID': '76', 'harvest_year': 2023},
 {'DEPT_ID': '35', 'harvest_year': 2018},
 {'DEPT_ID': '01', 'harvest_year': 2020},
 {'DEPT_ID': '64', 'harvest_year': 2014},
 {'DEPT_ID': '76', 'harvest_year': 2015},
 {'DEPT_ID': '48', 'harvest_year': 2013},
 {'DEPT_ID': '06', 'harvest_year': 2016},
 {'DEPT_ID': '47', 'harvest_year': 2015},
 {'DEPT_ID': '15', 'harvest_year': 2012},
 {'DEPT_ID': '52', 'harvest_year': 2023},
 {'DEPT_ID': '09', 'harvest_year': 2014},
 {'DEPT_ID': '94', 'harvest_year': 2020},
 {'DEPT_ID': '39', 'harvest_year': 2012},
 {'DEPT_ID': '56', 'harvest_year': 2010},
 {'DEPT_ID': '12', 'harvest_year': 2011},
 {'DEPT_ID': '57', 'harvest_year': 2019},
 {'DEPT_ID': '88', 'harvest_year': 2022},
 {'DEPT_ID': '91', 'harvest_year': 2013},
 {'DEPT_ID': '68', 'harvest_year': 2017},
 {'DEPT_ID': '82', 'harvest_year': 2014},
 {'DEPT_ID': '04', 'harvest_year': 2018},
 {'DEPT_ID': '51', 'harvest_year': 2020},
 {'DEPT_ID': '77', 'harvest_year': 2013},
 {'DEPT_ID': '71', 'harvest_year': 2020},
 {'DEPT_ID': '66', 'harvest_year': 2015},
 {'DEPT_ID': '07', 'harvest_year': 2024},
 {'DEPT_ID': '81', 'harvest_year': 2021},
 {'DEPT_ID': '09', 'harvest_year': 2024},
 {'DEPT_ID': '91', 'harvest_year': 2022},
 {'DEPT_ID': '81', 'harvest_year': 2016},
 {'DEPT_ID': '48', 'harvest_year': 2016},
 {'DEPT_ID': '33', 'harvest_year': 2016}]

# df_couples contient les couples disponibles
df_couples = pd.DataFrame(couples)

# Années disponibles
annees = sorted(df_couples["harvest_year"].unique())


########### SELECT BOXES ###########

annee = st.selectbox(
    "📅​ Choisis une année",
    options=annees
)

# Départements disponibles pour l'année choisie
departements = sorted(
    df_couples.loc[
        df_couples["harvest_year"] == annee,
        "DEPT_ID"
    ].unique()
)

departement = st.selectbox(
    "🇫🇷​ Choisis un département",
    options=departements
)


########### ENVOIE DE LA REQUETE A L'API ############

api_url = st.secrets["API_URL"]

if st.button("Lancer le test"):
    payload = {
        "harvest_year": int(annee),
        "DEPT_ID": departement
    }

########### RECEPTION DES REPONSES ############

    #response = requests.get(
        #api_url,
        #params=payload
    #).json()

    response_test = {'prediction':1000, 'reel':200}

    prediction = response_test["prediction"]
    reel = response_test["reel"]

########### AFFICHAGE RESULTATS ###########

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("🔮 Prédiction")
            st.metric(
                label="Rendement estimé",
                value=f"{prediction} tonnes"
            )

    with col2:
        with st.container(border=True):
            st.subheader("🌾 Réel")
            st.metric(
                label="Rendement observé",
                value=f"{reel} tonnes"
            )

    ########### ANALYSE ###########

    diff = prediction - reel
    erreur_pct = (diff / reel) * 100

    st.divider()

    with st.container(border=True):
        st.subheader("📊 Analyse de la performance")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="📉 Écart (Prédiction - Réel)",
            value=f"{diff:.1f} tonnes",
            delta=f"{erreur_pct:.1f}%"
        )

    with col2:
        st.metric(
            label="📊 Erreur relative",
            value=f"{abs(erreur_pct):.2f} %"
        )

    ########### METRIQUES MODELE ###########

    st.divider()

    with st.container(border=True):
        st.subheader("🧠 Performance du modèle")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="MAE (erreur moyenne)",
            value="4.72 tonnes"
        )
        st.caption("En moyenne, le modèle se trompe de 4.72 tonnes")

    with col2:
        st.metric(
            label="R² (explication des variations)",
            value="85%"
        )
        st.caption("Le modèle explique 85% des variations du rendement")
