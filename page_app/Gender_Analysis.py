import streamlit as st
import plotly.express as px
import pandas as pd


def app():
    st.title('Gender Analysis')
    def load_data():
        data = pd.read_csv('datasets/parcoursup_copie.csv', delimiter=';')
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        return data
    df = load_data()
    

    total_voeux = df['voe_tot'].sum()
    total_voeux_filles = df['voe_tot_f'].sum()
    total_acc = df['acc_tot'].sum()
    total_acc_filles = df['acc_tot_f'].sum()
    totals_data = {
    'Category': ['Girls', 'Boys'],
    'Total Vows': [total_voeux_filles, total_voeux - total_voeux_filles],
    'Total Accepted': [total_acc_filles, total_acc - total_acc_filles]
    }

    # pie chart - Girls VS Boys 
    df_totals = pd.DataFrame(totals_data)

    # total vows
    fig_vows = px.pie(df_totals, names='Category', values='Total Vows', title='Proportion of Girls vs Boys for Total Vows')
    # accepted
    fig_accepted = px.pie(df_totals, names='Category', values='Total Accepted', title='Proportion of Girls vs Boys for Total Accepted')

    fig_vows.update_layout(width=400)
    fig_accepted.update_layout(width=400) 
    st.header('Proportion of Girls vs Boys')

    #division page in 2 
    col1, col2 = st.columns([1, 1])
    col1.plotly_chart(fig_vows)
    col2.plotly_chart(fig_accepted)

    # histogram - proportion of girls and scholarships student in each formation
    st.header('Girls and Boursiers Accepted by Filière')
    fig = px.bar(df, x='fili', y=['acc_tot_f', 'acc_brs'], title='Girls and Boursiers Accepted by Filière',
                 labels={'fili': 'Formations', 'value': 'Number of Students', 'acc_tot_f': 'Rate of female students', 'acc_brs': 'Rate of scholarship students'},
                 color_discrete_sequence=['#FF9B98','#C1F7D0'])
    fig.update_layout(barmode='group')
    st.plotly_chart(fig)


    df['acc_tot_b'] = df['acc_tot'] - df['acc_tot_f']
    st.header('Girls and Boys Accepted by Filière')
    fig = px.bar(df, x='fili', y=['acc_tot_f', 'acc_tot_b'], title='Girls and Boys Accepted by Filière',
                 labels={'fili': 'Formations', 'value': 'Number of Students', 'acc_tot_f': 'Rate of female students', 'acc_tot_b': 'Rate of boys students'},
                 color_discrete_sequence=['#84C9FF','#FCFF8B'])
    fig.update_layout(barmode='group')
    st.plotly_chart(fig)

    # pie - proportion of woman in private institutions
    public_values = ['Public']
    private_values = ['Privé sous contrat d\'association', 'Privé enseignement supérieur', 'Privé hors contrat']
    public_df = df[df['contrat_etab'].isin(public_values)]
    private_df = df[df['contrat_etab'].isin(private_values)]
    private_df['contrat_etab'].replace({
        'Privé sous contrat d\'association': 'Privé',
        'Privé enseignement supérieur': 'Privé',
        'Privé hors contrat': 'Privé'
    }, inplace=True)

    private_institutions = private_df[private_df['contrat_etab'] == 'Privé']
    total_female_students_private = private_institutions['acc_tot_f'].sum()
    total_students_private = private_institutions['acc_tot'].sum()
    proportion_female_private = total_female_students_private / total_students_private
    fig = px.pie(
        names=['Female Students', 'Male Students'],
        values=[proportion_female_private, 1 - proportion_female_private],
        title='Proportion of Females in Private Institutions',
    )

    st.write(fig)







    