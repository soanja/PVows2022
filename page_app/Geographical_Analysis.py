import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

def app():
    st.title('Geographical Analysis')
    def load_data():
        data = pd.read_csv('datasets/parcoursup_copie.csv', delimiter=';')
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        return data
    df = load_data()


    # DROPDOWN 
    # dashboard - for each region 

    #dropdown 
    selected_region = st.selectbox("Select Region", df['region_etab_aff'].unique())
    filtered_data_region = df[df['region_etab_aff'] == selected_region]
    nb_institution = filtered_data_region['g_ea_lib_vx'].nunique()
    nb_formation = filtered_data_region['form_lib_voe_acc'].nunique()
    nb_seats = filtered_data_region['capa_fin'].sum()


    # division of page in 5 columns
    st.markdown("<h3 style='text-align: center;'>What formation do we offer ?</h3>", unsafe_allow_html=True)
    col0, col1, col2, col3 , col4= st.columns([4, 2, 2, 3, 3])

    col1.image("assets/school.png", width=70)
    col1.metric(" ",nb_institution)
    col1.write("Institutions", text_align="center")


    col2.image("assets/cap.png", width=70)
    col2.metric(" ",nb_formation)
    col2.write("Formations", text_align="center")


    col3.image("assets/chair.png", width=70)
    col3.metric(" ",nb_seats)
    col3.write("Seats", text_align="center")


    # barh - Places disp pour chaque formation dans cette region
    st.markdown("<h5 style='text-align: center;'>Available seats by Formation</h5>", unsafe_allow_html=True)
    places_by_filiere = filtered_data_region.groupby('fili')['capa_fin'].sum().reset_index()
    chart = alt.Chart(places_by_filiere).mark_bar().encode(
        y=alt.Y('fili:O', title='Formations'),
        x=alt.X('capa_fin:Q', title='Total seats'),
        color=alt.value('#FF2B2B')
    ).properties(
        width=600,
        height=400
    )
    st.altair_chart(chart)


    st.markdown("<h3 style='text-align: center;'>A formation for who ?</h3>", unsafe_allow_html=True)

    # division of page in 3 columns
    col0, col1, col2= st.columns([1, 2, 2])
    total_acc_bg = filtered_data_region['acc_bg'].sum()
    total_acc_bt = filtered_data_region['acc_bt'].sum()
    total_acc_bp = filtered_data_region['acc_bp'].sum()
    total_admitted = total_acc_bg + total_acc_bt + total_acc_bp
    plot_df = pd.DataFrame({
        'Bac Type': ['acc_bg', 'acc_bt', 'acc_bp'],
        'Total Admitted': [total_acc_bg, total_acc_bt, total_acc_bp]
    })

    fig = px.pie(plot_df, names='Bac Type', values='Total Admitted',
                 title='Total Admitted by Bac Type', hole=.8)
    fig.update_layout(legend_title_text='Bac Types', width=400, height=400)
    # total number of admissions in center of pie
    fig.add_annotation(
        text=f"{total_admitted}",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=40)
    )

    mean_pct_aca_orig = filtered_data_region['pct_aca_orig'].mean()
    mean_pct_aca_orig = mean_pct_aca_orig.round(2)    

    col0.write(fig)

    col2.metric("Students accepted from the same academy", f"{mean_pct_aca_orig}%")



    # drop down - number of applications by regions for each formations 
    selected_filiere = st.selectbox("Select Formation Type", df['fili'].unique())
    filtered_data = df[df['fili'] == selected_filiere]
    fig = px.bar(filtered_data, x='capa_fin', y='region_etab_aff',
                 title=f'Applications per Place for {selected_filiere}',
                 labels={'capa_fin': 'Applications per Place', 'region_etab_aff': "French Regions"},
                 color='region_etab_aff',
                 color_discrete_sequence=px.colors.qualitative.Plotly)
    fig.update_layout(legend_title_text='French Region')
    st.plotly_chart(fig)

    #map - clustering all the institutions accross France
    clustered_data = df.groupby(['region_etab_aff', 'lib_for_voe_ins'], as_index=False).agg({
    'lat': 'mean',
    'long': 'mean',
    'capa_fin': 'sum',
    'pct_f': 'mean'
})

    fig = px.scatter_mapbox(
        clustered_data,
        lat='lat',
        lon='long',
        size='capa_fin',
        color='pct_f',
        hover_name='lib_for_voe_ins',
        hover_data=['capa_fin', 'pct_f'],
        color_continuous_scale='Viridis',
        title='Clusters of Formation Types by Region',
        zoom=5, 
    )

    fig.update_layout(mapbox_style='carto-positron',mapbox_zoom=5, width=1000, height=1000) 

    st.write(fig)












    