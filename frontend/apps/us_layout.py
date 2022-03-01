import plotly.express as px
import dash_bootstrap_components as dbc

from app import app
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
from backend.functions import read_from_sql


""" Import data """
# Read data from SQL
deaths_us_df = read_from_sql('test', 'deaths_us')
available_states = deaths_us_df['state'].unique()
deaths_us_states_df = deaths_us_df.groupby(['state', 'time_period', 'state_code'], as_index=False).sum()
deaths_us_normalized_df = read_from_sql('test', 'deaths_us_normalized')
deaths_us_ts_df = deaths_us_df.groupby('time_period', as_index=False).sum()

""" Create graphs """
deaths_choropleth = px.choropleth(deaths_us_states_df,
                                  locations='state_code',
                                  color="deaths",
                                  animation_frame="time_period",
                                  color_continuous_scale="orrd",
                                  locationmode='USA-states',
                                  hover_name="state",
                                  scope="usa",
                                  labels={'state_code': 'State Code', 'deaths': 'Death Count', 'time_period': 'Month'},
                                  height=600)
cumulative_deaths_choropleth = px.choropleth(deaths_us_states_df,
                                             locations='state_code',
                                             color="cumulative_deaths",
                                             animation_frame="time_period",
                                             color_continuous_scale="orrd",
                                             locationmode='USA-states',
                                             hover_name="state",
                                             scope="usa",
                                             labels={'state_code': 'State Code',
                                                     'cumulative_deaths': 'Cumulative Death Count',
                                                     'time_period': 'Month'},
                                             height=600)

"""" Layout"""
layout = html.Div([
    dbc.Container([
        dbc.Row([dbc.Col(html.H1(children='Covid-19 in the USA at a glance'), className="mb-2")]),
        dbc.Row([dbc.Col(html.H6(children='visualising trends across the different stages of '
                                          'the covid-19 outbreak in the USA'), className="mb-4")]),

        dbc.Row([dbc.Col(dbc.Card(html.H3(children='Latest Update', className="text-center text-light bg-dark"),
                                  body=True, color="dark"),
                         className="mb-4")]),
        dcc.RadioItems(id='table_type', options=[{'label': i, 'value': i} for i in ['Condensed table', 'Full table']],
                       value='Condensed table', labelStyle={'display': 'inline-block', "margin-right": "20px"},
                       style={"text-align": "center"}),
        dash_table.DataTable(id='datatable_us', style_table={'overflowX': 'scroll', 'padding': 10},
                             style_header={'backgroundColor': '#25597f', 'color': 'white'},
                             style_cell={'backgroundColor': 'white', 'color': 'black', 'fontSize': 13,
                                         'font-family': 'Nunito Sans', "text-align": "center"}),

        dbc.Row([dbc.Col(dbc.Card(html.H3(children='Situation across different periods of the outbreak',
                                          className="text-center text-light bg-dark"),
                                  body=True, color="dark"),
                         className="mt-4 mb-4")]),
        dcc.Dropdown(id='covid_period', options=[
                    {'label': 'First half of 2020', 'value': '2020,01,06'},
                    {'label': 'Second half of 2020', 'value': '2020,07,12'},
                    {'label': 'First half of 2021', 'value': '2021,01,06'},
                    {'label': 'Second half of 2021', 'value': '2021,07,12'}],
                     value='2021,07,12', style={'width': '65%', 'margin-left': '5px'}),
        dbc.Row([dbc.Col(html.H5(children='Daily COVID-19 cases in the USA', className="text-center"),
                         className="mt-4")]),
        dcc.Graph(id='graph_by_period', hoverData={'points': [{'x': '11-May'}]}),

        dbc.Row([dbc.Col(dbc.Card(html.H3(children='Figures by states', className="text-center text-light bg-dark"),
                                  body=True, color="dark"),
                         className="mb-4")]),
        dbc.Row([dbc.Col(html.H5(children='Progress of covid deaths across states in the USA', className="text-center"),
                         className="mt-4"), ]),
        dbc.Row([html.Div([dcc.Graph(figure=deaths_choropleth)])]),
        dbc.Row([html.Div([dcc.Graph(figure=cumulative_deaths_choropleth)])]),

        dbc.Row([dbc.Col(dbc.Card(html.H3(children='Comparison between states',
                                          className="text-center text-light bg-dark"),
                                  body=True, color="dark"), className="mb-4")]),
        dcc.Dropdown(id='states', options=[{'label': i, 'value': i} for i in available_states],
                     value=['Mississippi', 'Arizona', 'California', 'Kentucky'], multi=True,
                     style={'width': '70%', 'margin-left': '5px', 'align': 'center'}),
        dcc.Graph(id='deaths_us_states_bar'),
        dcc.Graph(id='deaths_us_sunburst')
    ])
])


# choose between condensed table and full table
@app.callback([Output('datatable_us', 'data'),
               Output('datatable_us', 'columns')],
              [Input('table_type', 'value')])
def update_columns(value):
    df = deaths_us_df.tail(1)

    condensed_col = ['state', 'province', 'population', 'time_period', 'deaths', 'cumulative_deaths']
    full_col = ['index', 'province', 'state', 'population', 'time_period', 'cumulative_deaths', 'deaths', 'state_code']

    columns = [{"name": i, "id": i} for i in full_col]
    data = df.to_dict('records')
    if value == 'Condensed table':
        columns = [{"name": i, "id": i} for i in condensed_col]
        data = df.to_dict('records')

    return data, columns


# allow for easy sieving of data to see how the situation has changed.
# can observe whether government measures are effective in reducing the number of cases.
@app.callback(Output('graph_by_period', 'figure'),
              [Input('covid_period', 'value')])
def update_graph(covid_period_dates):
    year, month_start, month_end = covid_period_dates.split(",")
    months_list = [(year+'-'+'{:02}').format(month) for month in range(int(month_start), int(month_end)+1)]
    dfc = deaths_us_ts_df[deaths_us_ts_df['time_period'].isin(months_list)]
    return px.line(dfc, x="time_period", y="deaths", markers=True, labels={'time_period': 'Month', 'deaths': 'Deaths'})


# to allow comparison of cases or deaths among states
@app.callback([Output('deaths_us_states_bar', 'figure'),
               Output('deaths_us_sunburst', 'figure')],
              [Input('states', 'value')])
def update_graph(states_name):
    dfc = deaths_us_normalized_df.copy()
    dfc = dfc[dfc['state'].isin(states_name)]
    deaths_us_states_bar = px.bar(dfc, x="state", y="death_percent",
                                  labels={'state': 'State', 'death_percent': 'Percentage of deaths'})

    deaths_us_sunburst = px.sunburst(deaths_us_df[deaths_us_df['state'].isin(states_name)],
                                     path=['state', 'province'], values='deaths', height=600, template="plotly",
                                     labels={'state': 'State', 'province': 'Provinces', 'deaths': 'Death Count'})
    return deaths_us_states_bar, deaths_us_sunburst
