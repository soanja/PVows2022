import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def app():

	def load_data():
	    data = pd.read_csv('datasets/parcoursup_copie.csv', delimiter=';')
	    lowercase = lambda x: str(x).lower()
	    data.rename(lowercase, axis='columns', inplace=True)
	    return data


	st.header('1 - Introduction')
	st.write("Welcome to my app presenting the affectation of high school graduate of the year 2022. Hope you will enjoy this.")

	st.header('2 - Source of the data ')

	st.write("Here is a brief part of my dataset. The original dataset can be found following this link : https://www.data.gouv.fr/fr/datasets/parcoursup-2022-voeux-de-poursuite-detudes-et-de-reorientation-dans-lenseignement-superieur-et-reponses-des-etablissements/#/resources")
	# Create a text element and let the reader know the data is loading.
	data_load_state = st.text('Loading data...')
	# Load 10,000 rows of data into the dataframe.
	df = load_data()
	# Notify the reader that the data was successfully loaded.
	data_load_state.text('Loading data...done!')

	st.header('Quick Overview')
	st.dataframe(df)

	total_vows = df['voe_tot'].sum()
	total_places_available = df['capa_fin'].sum()
	average_vows_received = int(df['voe_tot'].mean())
	total_admitted_candidates = df['acc_tot'].sum()
	total_admitted_candidates = df['acc_tot'].sum()
	total_female_candidates = df['acc_tot_f'].sum()
	num_institutions = df['g_ea_lib_vx'].nunique()
	num_formations = df['lib_for_voe_ins'].nunique()
	if total_admitted_candidates > 0:
	    female_percentage = (total_female_candidates / total_admitted_candidates) * 100
	else:
	    female_percentage = 0


	st.header("Admissions Statistics")
	col1, col2, col3 = st.columns([2, 2, 2])
	col1.metric("Vows", total_vows)
	col1.metric("Places Available Overall", total_places_available)


	col2.metric("Number of institutions", num_institutions)
	col2.metric("Number of formations", num_formations)
	col2.metric("Average Vows for a Program", average_vows_received)

	col3.metric("Admitted Candidates", total_admitted_candidates)
	col3.metric("Of Female Candidates", total_female_candidates, f"{female_percentage:.2f}%")


	bac_sum_data = {'Bac Type': ['Bac General', 'Bac Technologique', 'Bac Professionnel', 'Autre'],
    'Total Admissions': [
        df['acc_bg'].sum(),
        df['acc_bt'].sum(),
        df['acc_bp'].sum(),
        df['acc_at'].sum()
    ]}

	bac_df = pd.DataFrame(bac_sum_data)
	fig_bac = go.Figure(data=go.Scatterpolar(r=bac_df['Total Admissions'],theta=bac_df['Bac Type'], fill='toself'))

	fig_bac.update_layout(
	    polar=dict(
	        radialaxis=dict(
	            visible=True,
	            range=[0, max(bac_df['Total Admissions'])]
	        )
	    ))


	mentions = ['acc_sansmention', 'acc_ab', 'acc_b', 'acc_tb']
	mention_sum_data = { 'Mention': mentions,
    'Total Admissions': [
        df['acc_sansmention'].sum(),
        df['acc_ab'].sum(),
        df['acc_b'].sum(),
        df['acc_tb'].sum(),
	]}
	mention_df = pd.DataFrame(mention_sum_data)

	fig_mention = go.Figure()
	fig_mention.add_trace(go.Scatterpolar(
    r=mention_df['Total Admissions'],
    theta=mention_df['Mention'],line=dict(color='red'), fill='toself',fillcolor='rgba(155, 0, 0, 0.3)'))

	fig_mention.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, max(mention_df['Total Admissions'])]
        )
    ))
	fig_bac.update_layout(width=400)
	fig_mention.update_layout(width=400) 

	col1, col2 = st.columns([2, 2])
	col1.subheader('Repartition of Admissions by Bac Type')
	col1.plotly_chart(fig_bac)

	col2.subheader('Repartition of Admissions by Mention')
	col2.plotly_chart(fig_mention)




	


