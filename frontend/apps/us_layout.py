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
deaths_us_normalized_df = read_from_sql('test', 'deaths_us_normalized')
# deaths_us_ts_df = deaths_us_df.groupby('time_period', as_index=False).sum()

""" Create graphs """
deaths_choropleth = px.choropleth(deaths_us_df,
                                  locations='state_code',
                                  color="deaths",
                                  animation_frame="time_period",
                                  color_continuous_scale="orrd",
                                  locationmode='USA-states',
                                  hover_name="state",
                                  scope="usa",
                                  range_color=(0, 1000000),
                                  labels={'state_code': 'State', 'deaths': 'Death Count', 'time_period': 'Month'},
                                  height=600)

deaths_us_bar = px.bar(deaths_us_normalized_df, x="death_percent", y="state", orientation='h',
                       labels={'state': 'State', 'death_percent': 'Percentage of deaths'})

states = ['Connecticut', 'Louisiana', 'Massachusetts', 'Mississippi', 'New York', 'New Jersey', 'Rhode Island']
deaths_us_sunburst = px.sunburst(deaths_us_df[deaths_us_df['state'].isin(states)],
                                 path=['state', 'province'], values='deaths', height=600, template="plotly",
                                 labels={'state': 'State', 'province': 'Provinces', 'deaths': 'Death Count'})


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
        dbc.Row([dbc.Col(html.H5(children='Daily COVID-19 cases in the USA', className="text-center"),
                         className="mt-4")]),
        dcc.Graph(id='graph_by_period', hoverData={'points': [{'x': '11-May'}]}),

        dbc.Row([dbc.Col(dbc.Card(html.H3(children='Figures by states', className="text-center text-light bg-dark"),
                                  body=True, color="dark"),
                         className="mb-4")]),
        dbc.Row([dbc.Col(html.H5(children='Progress of covid deaths across states in the USA', className="text-center"),
                         className="mt-4"), ]),
        dbc.Row([html.Div([dcc.Graph(figure=deaths_choropleth)])]),
        dbc.Row([html.Div([dcc.Graph(figure=deaths_us_bar)])]),
        dbc.Row([html.Div([dcc.Graph(figure=deaths_us_sunburst)])]),
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
def update_graph(covid_period_name):
    # dff = deaths_us_ts_df[deaths_us_ts_df.Period == covid_period_name]
    # # not sure why this doesn't work, Daily Confirmed is an invalid key
    # col = ['Daily Imported', 'Daily Local transmission']
    # dff['total'] = dff[col].sum(axis=1)
    # data = [go.Scatter(x=dff['Date'], y=dff['total'],
    #                    mode='lines+markers',name='Daily confirmed')]
    # layout = go.Layout(
    #     yaxis={'title': "Cases"},
    #     paper_bgcolor = 'rgba(0,0,0,0)',
    #     plot_bgcolor = 'rgba(0,0,0,0)',
    #     template = "seaborn",
    #     margin=dict(t=20)
    # )
    # return {'data': data, 'layout': layout}
    return None
