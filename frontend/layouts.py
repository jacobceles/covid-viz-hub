import plotly.express as px

from dash import dcc
from dash import html
from backend.functions import read_from_sql

####################################################################################################
# 000 - FORMATTING INFO
####################################################################################################

# Corporate css formatting
corporate_colors = {
    'dark-blue-grey': 'rgb(62, 64, 76)',
    'medium-blue-grey': 'rgb(77, 79, 91)',
    'superdark-green': 'rgb(41, 56, 55)',
    'dark-green': 'rgb(57, 81, 85)',
    'medium-green': 'rgb(93, 113, 120)',
    'light-green': 'rgb(186, 218, 212)',
    'pink-red': 'rgb(255, 101, 131)',
    'dark-pink-red': 'rgb(247, 80, 99)',
    'white': 'rgb(251, 251, 252)',
    'light-grey': 'rgb(208, 206, 206)'
}

navbarcurrentpage = {
    'text-decoration': 'underline',
    'text-decoration-color': corporate_colors['pink-red'],
    'text-shadow': '0px 0px 1px rgb(251, 251, 252)'
}


####################################################################################################
# 000 - IMPORT DATA
####################################################################################################

###########################
# Import SQL data
# Read data from SQL
deaths_us_normalized_df = read_from_sql('test', 'deaths_us_normalized')
deaths_global_df = read_from_sql('test', 'deaths_global')
deaths_us_df = read_from_sql('test', 'deaths_us')


####################################################################################################
# 000 - DEFINE REUSABLE COMPONENTS AS FUNCTIONS
####################################################################################################


def get_header():
    # Header with logo
    header = html.Div([
        html.Div([], className='col-2'),  # Same as img width, allowing to have the title centrally aligned
        html.Div([html.H1(children='Covid Viz-Hub', style={'textAlign': 'center'})],
                 className='col-8', style={'padding-top': '1%'})],
        className='row',
        style={'height': '4%', 'background-color': corporate_colors['superdark-green']}
    )

    return header


def get_navbar(p='global'):
    # Nav bar
    navbar_global = html.Div([
        html.Div([], className='col-3'),
        html.Div([dcc.Link(html.H4(children='Global', style=navbarcurrentpage), href='/apps/global')],
                 className='col-2'),
        html.Div([dcc.Link(html.H4(children='US'), href='/apps/us')], className='col-2'),
        html.Div([dcc.Link(html.H4(children='Individual'), href='/apps/individual')], className='col-2'),
        html.Div([], className='col-3')
    ], className='row', style={'background-color': corporate_colors['dark-green'],
                               'box-shadow': '2px 5px 5px 1px rgba(255, 101, 131, .5)'})

    navbar_us = html.Div([
        html.Div([], className='col-3'),
        html.Div([dcc.Link(html.H4(children='Global'), href='/apps/global')], className='col-2'),
        html.Div([dcc.Link(html.H4(children='US', style=navbarcurrentpage), href='/apps/us')], className='col-2'),
        html.Div([dcc.Link(html.H4(children='Individual'), href='/apps/individual')], className='col-2'),
        html.Div([], className='col-3')
    ], className='row', style={'background-color': corporate_colors['dark-green'],
                               'box-shadow': '2px 5px 5px 1px rgba(255, 101, 131, .5)'}
    )

    navbar_individual = html.Div([
        html.Div([], className='col-3'),
        html.Div([dcc.Link(html.H4(children='Global'), href='/apps/global')], className='col-2'),
        html.Div([dcc.Link(html.H4(children='US'), href='/apps/us')], className='col-2'),
        html.Div([dcc.Link(html.H4(children='Individual', style=navbarcurrentpage), href='/apps/individual')],
                 className='col-2'),
        html.Div([], className='col-3')
    ], className='row', style={'background-color': corporate_colors['dark-green'],
                               'box-shadow': '2px 5px 5px 1px rgba(255, 101, 131, .5)'}
    )

    if p == 'global':
        return navbar_global
    elif p == 'us':
        return navbar_us
    else:
        return navbar_individual


def get_empty_row(h='45px'):
    # Empty row
    empty_row = html.Div([
        html.Div([
            html.Br()
        ], className='col-12')
    ],
        className='row',
        style={'height': h})

    return empty_row


####################################################################################################
# 001 - Global
####################################################################################################

fig1 = px.choropleth(deaths_global_df,
                     locations="iso_alpha",
                     color="deaths",
                     hover_name="country/region",
                     animation_frame="time_period",
                     color_continuous_scale='agsunset',
                     title='Death Count',
                     height=600)

fig2 = px.choropleth(deaths_global_df,
                     locations="iso_alpha",
                     color="cumulative_deaths",
                     hover_name="country/region",
                     animation_frame="time_period",
                     color_continuous_scale='amp',
                     title='Cumulative Death Count',
                     height=600)

fig3 = px.choropleth(deaths_us_df,
                     locations='state_code',
                     color="deaths",
                     animation_frame="time_period",
                     color_continuous_scale="orrd",
                     locationmode='USA-states',
                     hover_name="province_state",
                     scope="usa",
                     range_color=(0, 20),
                     title='Deaths in US by State',
                     height=600)

fig4 = px.bar(deaths_us_normalized_df, x="death_percent", y="province_state", orientation='h')

states = ['Connecticut', 'Louisiana', 'Massachusetts', 'Mississippi', 'New York', 'New Jersey', 'Rhode Island']
fig5 = px.sunburst(deaths_us_df[deaths_us_df['province_state'].isin(states)],
                   path=['province_state', 'admin2'], values='deaths', height=600, template="plotly")

global_layout = html.Div([

    #####################
    # Row 1 : Header
    get_header(),

    #####################
    # Row 2 : Nav bar
    get_navbar('global'),

    #####################
    # Row 3
    get_empty_row(),

    #####################
    # Row 4 : Charts
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3),
    dcc.Graph(figure=fig4),
    dcc.Graph(figure=fig5)
])

####################################################################################################
# 002 - US
####################################################################################################

us_layout = html.Div([

    #####################
    # Row 1 : Header
    get_header(),

    #####################
    # Row 2 : Nav bar
    get_navbar('us'),

    #####################
    # Row 3
    get_empty_row(),

    #####################
    # Row 4 : Charts
])

####################################################################################################
# 003 - Individual
####################################################################################################

individual_layout = html.Div([

    #####################
    # Row 1 : Header
    get_header(),

    #####################
    # Row 2 : Nav bar
    get_navbar('individual'),

    #####################
    # Row 3
    get_empty_row(),

    #####################
    # Row 4 : Charts
])
