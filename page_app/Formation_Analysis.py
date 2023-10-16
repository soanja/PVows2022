import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt

def app():
    st.title('Formation Analysis')
    def load_data():
        data = pd.read_csv('datasets/parcoursup_copie.csv', delimiter=';')
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        return data
    df = load_data()


    #bubble plot -  overview of all formations and sub formations 
    hierarchical_data = df.groupby(['fili', 'form_lib_voe_acc', 'fil_lib_voe_acc']).size().reset_index(name='count')
    st.subheader('Hierarchical Bubble Chart')
    fig = px.sunburst(hierarchical_data, path=['fili', 'form_lib_voe_acc', 'fil_lib_voe_acc'], values='count')
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    st.plotly_chart(fig)


    #stacked histogram - total  admission  for each bac type
    name=['Bac General', 'Bac Technologique', 'Bac Professionnel', 'Autre']
    st.subheader('Admitted Students by Bac Type and Formation Type')
    fig = px.bar(df, x='fili', y=['acc_bg', 'acc_bp', 'acc_bt', 'acc_at'],
             title='Admitted Students by Bac Type and Formation Type',
             labels={'fili': 'Formation Type', 'value': 'Rate of Admitted Students', 'variable': 'Bac Type'},
             color_discrete_sequence=['#C999A7', '#F1F988', '#33B5AC', '#331C72'],
             barmode='stack')
    fig.update_layout(legend_title_text='Bac Type')
    st.plotly_chart(fig)


    #boxplot -  admission ratio by each French region 
    df['admission_ratio'] = df['acc_tot'] / df['voe_tot']
    filtered_df = df[df['admission_ratio'] < 0.6]
    box_plot = px.box(filtered_df, x='region_etab_aff', y='admission_ratio', title='Admission Ratio by Region', color='region_etab_aff')
    st.header('Admission Ratio Analysis')
    st.plotly_chart(box_plot)

    # *************************************************************************************************** #

    #barplot - percentage of admission in public VS private institutions
    grouped_data_private = df.groupby(['fili', 'contrat_etab'])['pct_acc_debutpp'].mean().reset_index()
    plt.figure(figsize=(12, 6))
    sns.barplot(data=grouped_data_private, x='fili', y='pct_acc_debutpp', hue='contrat_etab', palette={"Public": "#F4976E", 
        "Privé hors contrat":"#E63B3E", "Privé sous contrat d'association":"#A6175A",
        "Privé enseignement supérieur": "#3B1A41"})
    plt.xlabel("Formation Type")
    plt.ylabel("Percentage of Admission")
    plt.title("Percentage of Admission by Formation Type (Public vs. Private)")
    plt.xticks(rotation=45)
    st.pyplot(plt)


    # *************************************************************************************************** #
    st.header("Capacity Analysis")
    # *************************************************************************************************** #

    # barh - capacity VS actual allocated seats by formation
    grouped = df.groupby('fili')[['capa_fin', 'acc_tot']].sum()
    colors = ['#84C9FF', '#FF2B2B']
    st.subheader('Number of Allocated Places and Actual Allocated Seats by Formation Type')
    fig, ax = plt.subplots(figsize=(10, 6))
    grouped.plot(kind='barh', stacked=False, ax=ax, color=colors)
    ax.set_xlabel('Number of Seats')
    ax.set_ylabel('Type of Formation')
    ax.legend(["Actual Allocated Seats","Allocated Places"])
    st.pyplot(fig)


    df['overcrowded'] = df['acc_tot'] - df['capa_fin']
    overcrowded_df = df[df['overcrowded'] > 0]

    # barplot - overcrowding by region
    st.subheader('Overcrowded Formations by Region')
    region_counts = overcrowded_df['region_etab_aff'].value_counts().reset_index()
    region_counts.columns = ['Region', 'Overcrowded Count']
    chart = alt.Chart(region_counts).mark_bar().encode(
        x=alt.X('Region:N', title='Region'),
        y=alt.Y('Overcrowded Count:Q', title='Overcrowded Count'),
        color=alt.Color('Region:N', title='Region'),
        tooltip=['Region', 'Overcrowded Count']
    ).properties(width=600)
    st.altair_chart(chart, use_container_width=True)



    # barplot - public VS private Capacity
    public_values = ['Public']
    private_values = ['Privé sous contrat d\'association', 'Privé enseignement supérieur', 'Privé hors contrat']
    public_df = df[df['contrat_etab'].isin(public_values)]
    private_df = df[df['contrat_etab'].isin(private_values)]
    private_df['contrat_etab'].replace({
        'Privé sous contrat d\'association': 'Privé',
        'Privé enseignement supérieur': 'Privé',
        'Privé hors contrat': 'Privé'
    }, inplace=True)
    public_capacity = public_df['capa_fin'].sum()
    private_capacity = private_df['capa_fin'].sum()
    st.subheader('Comparison of Public and Private Overall Capacity')
    data = pd.DataFrame({
        'Category': ['Public', 'Private'],
        'Overall Capacity': [public_capacity, private_capacity]
    })

    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Category:N', title='Institution Type'),
        y=alt.Y('Overall Capacity:Q', title='Overall Capacity'),
        color=alt.value(colors[0])
    )
    st.altair_chart(chart, use_container_width=True)



    











