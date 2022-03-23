import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

from app import app
from dash import dcc
from dash import html
from dash import dash_table
from plotly import graph_objs as go
from dash.dependencies import Input, Output
from backend.functions import read_from_sql

""" Import data """
# Read data from SQL
cdc_df = read_from_sql('covid_viz_hub', 'cdc_out')

# age group
df_age = cdc_df.groupby(['age_group', 'death_yn']).size().reset_index(name='death_qt')
df_age_yes = df_age[df_age['death_yn'] == 'Yes']
df_age_yes.set_index('age_group', inplace=True)
df_age_bar = cdc_df.groupby(['age_group']).size().reset_index(name='age_qt')
# sex
df_sex = cdc_df.groupby(['sex', 'death_yn']).size().reset_index(name='death_qt')
df_sex_yes = df_sex[df_sex['death_yn'] == 'Yes']
df_sex_yes.set_index('sex', inplace=True)
# race
df_race = cdc_df.groupby(['race', 'death_yn']).size().reset_index(name='death_qt')
df_race_yes = df_race[df_race['death_yn'] == 'Yes']
df_race_yes.set_index('race', inplace=True)
df_race_bar = cdc_df.groupby(['race']).size().reset_index(name='race_qt')
# underlying
df_underlying = cdc_df.groupby(['underlying_conditions_yn', 'death_yn']).size().reset_index(name='death_qt')
df_underlying_yes = df_underlying[df_underlying['death_yn'] == 'Yes']
df_underlying_yes.set_index('underlying_conditions_yn', inplace=True)
df_underlying_bar = cdc_df.groupby(['underlying_conditions_yn']).size().reset_index(name='under_qt')
# hospital or ICU
df_hospital = cdc_df.groupby(['case_month', 'hosp_yn']).size().reset_index(name='hosp_qt')
df_hospital_bar = df_hospital[df_hospital['hosp_yn'] == 'Yes']
df_hospital_bar.set_index('case_month', inplace=True)
df_icu = cdc_df.groupby(['case_month', 'icu_yn']).size().reset_index(name='icu_qt')
df_icu_bar = df_icu[df_icu['icu_yn'] == 'Yes']
df_icu_bar.set_index('case_month', inplace=True)
df_local_hospital = pd.merge(df_hospital_bar, df_icu_bar, on='case_month').reset_index()

""" Create graphs """
fig_age = px.bar(df_age,
                 x='age_group',
                 y='death_qt',
                 color='death_yn',
                 barmode='stack',
                 title='Impact of Age on Covid-19 outcomes',
                 labels={'death_qt': 'Death quantity', 'age_group': 'Age Group', 'death_yn': 'death'})
fig_sex = px.bar(df_sex,
                 x='sex',
                 y='death_qt',
                 color='death_yn',
                 barmode='stack',
                 title='Impact of Gender on Covid-19 outcomes',
                 labels={'death_qt': 'Death quantity', 'sex': 'Sex', 'death_yn': 'death'})
fig_race = px.bar(df_race,
                  x='race',
                  y='death_qt',
                  color='death_yn',
                  barmode='stack',
                  title='Impact of Race on Covid-19 outcomes',
                  labels={'death_qt': 'death quantity', 'race': 'Race', 'death_yn': 'death'})
fig_underlying = px.bar(df_underlying,
                        x='underlying_conditions_yn',
                        y='death_qt',
                        color='death_yn',
                        barmode='stack',
                        title='Impact of Underlying Conditions on Covid-19 outcomes',
                        labels={'death_qt': 'death quantity', 'underlying_conditions_yn': 'Underlying condition',
                                'death_yn': 'death'})

fig_hospital = go.Figure()
fig_hospital.add_trace(go.Bar(x=df_local_hospital["case_month"],
                              y=df_local_hospital["hosp_qt"],
                              name='general wards'))
fig_hospital.add_trace(go.Bar(x=df_local_hospital["case_month"],
                              y=df_local_hospital["icu_qt"],
                              name='ICU'))
fig_hospital.update_layout(barmode='stack',
                           title_text='Situation in Local Hospital - Covid patients in hospitals and I.C.U.s',
                           colorway=['grey', 'red'])

layout = html.Div([
    dbc.Container([
        dbc.Row([dbc.Col(html.H1(children='COVID-19 Worldwide at a glance'), className="mb-2")]),
        dbc.Row([dbc.Col(html.H6(children='Visualising trends across the world'), className="mb-4")]),

        dbc.Row([dbc.Col(dbc.Card(html.H3(children='Latest Update', className="text-center text-light bg-dark"),
                                  body=True, color="dark"),
                         className="mb-4")]),
        dcc.RadioItems(id='table_type', options=[{'label': i, 'value': i} for i in ['Condensed table', 'Full table']],
                       value='Condensed table', labelStyle={'display': 'inline-block', "margin-right": "20px"},
                       style={"text-align": "center"}),
        dash_table.DataTable(id='datatable_cdc', style_table={'overflowX': 'scroll', 'padding': 10},
                             style_header={'backgroundColor': '#25597f', 'color': 'white'},
                             style_cell={'backgroundColor': 'white', 'color': 'black', 'fontSize': 13,
                                         'font-family': 'Nunito Sans', "text-align": "center"}),
        dbc.Row([dbc.Col(dbc.Card(html.H3(children='Fatality rate and biological differences',
                                          className="text-center text-light bg-dark"),
                                  body=True, color="dark"),
                         className="mt-4 mb-4")]),
        # bar charts
        dbc.Row([dbc.Col(html.Div([dcc.Graph(figure=fig_age)])),
                 dbc.Col(html.Div([dcc.Graph(figure=fig_sex)]))]),
        dbc.Row([dbc.Col(html.Div([dcc.Graph(figure=fig_race)])),
                 dbc.Col(html.Div([dcc.Graph(figure=fig_underlying)]))]),
        dbc.Row([dbc.Col(html.Div([dcc.Graph(figure=fig_hospital)]))])
    ])
])


# choose between condensed table and full table
@app.callback([Output('datatable_cdc', 'data'),
               Output('datatable_cdc', 'columns')],
              [Input('table_type', 'value')])
def update_columns(value):
    df = cdc_df.tail(1)

    condensed_col = ['res_state', 'age_group', 'sex', 'race', 'death_yn', 'underlying_conditions_yn']
    full_col = ['index', 'case_month', 'res_state', 'age_group', 'sex', 'race',
                'hosp_yn', 'icu_yn', 'death_yn', 'underlying_conditions_yn']

    columns = [{"name": i, "id": i} for i in full_col]
    data = df.to_dict('records')
    if value == 'Condensed table':
        columns = [{"name": i, "id": i} for i in condensed_col]
        data = df.to_dict('records')

    return data, columns
