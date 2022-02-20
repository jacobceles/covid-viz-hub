import pandas as pd
import plotly.graph_objs as go

from dash import dcc
from dash import html
from dash import dash_table

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

externalgraph_rowstyling = {
    'margin-left': '15px',
    'margin-right': '15px'
}

externalgraph_colstyling = {
    'border-radius': '10px',
    'border-style': 'solid',
    'border-width': '1px',
    'border-color': corporate_colors['superdark-green'],
    'background-color': corporate_colors['superdark-green'],
    'box-shadow': '0px 0px 17px 0px rgba(186, 218, 212, .5)',
    'padding-top': '10px'
}

filterdiv_borderstyling = {
    'border-radius': '0px 0px 10px 10px',
    'border-style': 'solid',
    'border-width': '1px',
    'border-color': corporate_colors['light-green'],
    'background-color': corporate_colors['light-green'],
    'box-shadow': '2px 5px 5px 1px rgba(255, 101, 131, .5)'
}

navbarcurrentpage = {
    'text-decoration': 'underline',
    'text-decoration-color': corporate_colors['pink-red'],
    'text-shadow': '0px 0px 1px rgb(251, 251, 252)'
}

recapdiv = {
    'border-radius': '10px',
    'border-style': 'solid',
    'border-width': '1px',
    'border-color': 'rgb(251, 251, 252, 0.1)',
    'margin-left': '15px',
    'margin-right': '15px',
    'margin-top': '15px',
    'margin-bottom': '15px',
    'padding-top': '5px',
    'padding-bottom': '5px',
    'background-color': 'rgb(251, 251, 252, 0.1)'
}

recapdiv_text = {
    'text-align': 'left',
    'font-weight': '350',
    'color': corporate_colors['white'],
    'font-size': '1.5rem',
    'letter-spacing': '0.04em'
}

# Corporate chart formatting

corporate_title = {
    'font': {
        'size': 16,
        'color': corporate_colors['white']}
}

corporate_xaxis = {
    'showgrid': False,
    'linecolor': corporate_colors['light-grey'],
    'color': corporate_colors['light-grey'],
    'tickangle': 315,
    'titlefont': {
        'size': 12,
        'color': corporate_colors['light-grey']},
    'tickfont': {
        'size': 11,
        'color': corporate_colors['light-grey']},
    'zeroline': False
}

corporate_yaxis = {
    'showgrid': True,
    'color': corporate_colors['light-grey'],
    'gridwidth': 0.5,
    'gridcolor': corporate_colors['dark-green'],
    'linecolor': corporate_colors['light-grey'],
    'titlefont': {
        'size': 12,
        'color': corporate_colors['light-grey']},
    'tickfont': {
        'size': 11,
        'color': corporate_colors['light-grey']},
    'zeroline': False
}

corporate_font_family = 'Dosis'

corporate_legend = {
    'orientation': 'h',
    'yanchor': 'bottom',
    'y': 1.01,
    'xanchor': 'right',
    'x': 1.05,
    'font': {'size': 9, 'color': corporate_colors['light-grey']}
}  # Legend will be on the top right, above the graph, horizontally

corporate_margins = {'l': 5, 'r': 5, 't': 45, 'b': 15}  # Set top margin to in case there is a legend

corporate_layout = go.Layout(
    font={'family': corporate_font_family},
    title=corporate_title,
    title_x=0.5,  # Align chart title to center
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=corporate_xaxis,
    yaxis=corporate_yaxis,
    height=270,
    legend=corporate_legend,
    margin=corporate_margins
)

####################################################################################################
# 000 - DATA MAPPING
####################################################################################################

# Sales mapping
sales_filepath = 'data/datasource.xlsx'

sales_fields = {
    'date': 'Date',
    'reporting_group_l1': 'Country',
    'reporting_group_l2': 'City',
    'sales': 'Sales Units',
    'revenues': 'Revenues',
    'sales target': 'Sales Targets',
    'rev target': 'Rev Targets',
    'num clients': 'nClients'
}
sales_formats = {
    sales_fields['date']: '%d/%m/%Y'
}

####################################################################################################
# 000 - IMPORT DATA
####################################################################################################

###########################
# Import sales data
xls = pd.ExcelFile(sales_filepath)
sales_import = xls.parse('Static')

# Format date field
sales_import[sales_fields['date']] = pd.to_datetime(sales_import[sales_fields['date']],
                                                    format=sales_formats[sales_fields['date']])
sales_import['date_2'] = sales_import[sales_fields['date']].dt.date
min_dt = sales_import['date_2'].min()
min_dt_str = str(min_dt)
max_dt = sales_import['date_2'].max()
max_dt_str = str(max_dt)

# Create L1 dropdown options
repo_groups_l1 = sales_import[sales_fields['reporting_group_l1']].unique()
repo_groups_l1_all_2 = [
    {'label': k, 'value': k} for k in sorted(repo_groups_l1)
]
repo_groups_l1_all_1 = [{'label': '(Select All)', 'value': 'All'}]
repo_groups_l1_all = repo_groups_l1_all_1 + repo_groups_l1_all_2

# Initialise L2 dropdown options
repo_groups_l2 = sales_import[sales_fields['reporting_group_l2']].unique()
repo_groups_l2_all_2 = [
    {'label': k, 'value': k} for k in sorted(repo_groups_l2)
]
repo_groups_l2_all_1 = [{'label': '(Select All)', 'value': 'All'}]
repo_groups_l2_all = repo_groups_l2_all_1 + repo_groups_l2_all_2
repo_groups_l1_l2 = {}
for l1 in repo_groups_l1:
    l2 = sales_import[sales_import[sales_fields['reporting_group_l1']] == l1][
        sales_fields['reporting_group_l2']].unique()
    repo_groups_l1_l2[l1] = l2


#######################################################################################################################

####################################################################################################
# 000 - DEFINE REUSABLE COMPONENTS AS FUNCTIONS
####################################################################################################

#####################
# Header with logo
def get_header():
    header = html.Div([
        html.Div([], className='col-2'),  # Same as img width, allowing to have the title centrally aligned
        html.Div([html.H1(children='Covid Viz-Hub', style={'textAlign': 'center'})],
                 className='col-8', style={'padding-top': '1%'})],
        className='row',
        style={'height': '4%', 'background-color': corporate_colors['superdark-green']}
    )

    return header


#####################
# Nav bar
def get_navbar(p='world'):
    navbar_world = html.Div([
        html.Div([], className='col-3'),
        html.Div([dcc.Link(html.H4(children='World', style=navbarcurrentpage), href='/apps/world')], className='col-2'),
        html.Div([dcc.Link(html.H4(children='US'), href='/apps/us')], className='col-2'),
        html.Div([dcc.Link(html.H4(children='Individual'), href='/apps/individual')], className='col-2'),
        html.Div([], className='col-3')
    ], className='row', style={'background-color': corporate_colors['dark-green'],
                               'box-shadow': '2px 5px 5px 1px rgba(255, 101, 131, .5)'})

    navbar_us = html.Div([
        html.Div([], className='col-3'),
        html.Div([dcc.Link(html.H4(children='World'), href='/apps/world')], className='col-2'),
        html.Div([dcc.Link(html.H4(children='US', style=navbarcurrentpage), href='/apps/us')], className='col-2'),
        html.Div([dcc.Link(html.H4(children='Individual'), href='/apps/individual')], className='col-2'),
        html.Div([], className='col-3')
    ], className='row', style={'background-color': corporate_colors['dark-green'],
                               'box-shadow': '2px 5px 5px 1px rgba(255, 101, 131, .5)'}
    )

    navbar_individual = html.Div([
        html.Div([], className='col-3'),
        html.Div([dcc.Link(html.H4(children='World'), href='/apps/world')], className='col-2'),
        html.Div([dcc.Link(html.H4(children='US'), href='/apps/us')], className='col-2'),
        html.Div([dcc.Link(html.H4(children='Individual', style=navbarcurrentpage), href='/apps/individual')],
                 className='col-2'),
        html.Div([], className='col-3')
    ], className='row', style={'background-color': corporate_colors['dark-green'],
                               'box-shadow': '2px 5px 5px 1px rgba(255, 101, 131, .5)'}
    )

    if p == 'world':
        return navbar_world
    elif p == 'us':
        return navbar_us
    else:
        return navbar_individual


#####################
# Empty row

def get_empty_row(h='45px'):
    """This returns an empty row of a defined height"""

    empty_row = html.Div([
        html.Div([
            html.Br()
        ], className='col-12')
    ],
        className='row',
        style={'height': h})

    return empty_row


####################################################################################################
# 001 - SALES
####################################################################################################

world = html.Div([

    #####################
    # Row 1 : Header
    get_header(),

    #####################
    # Row 2 : Nav bar
    # get_navbar('world'),

    #####################
    # Row 3
    get_empty_row(),

    #####################
    # Row 4 : Charts
    html.Iframe(src="assets/graphs/world_death_count.html",
                style={"height": "700px", "width": "100%"}, ),
    html.Iframe(src="assets/graphs/world_cumulative_death_count.html",
                style={"height": "700px", "width": "100%"}, ),
    html.Iframe(src="assets/graphs/us_death_count.html",
                style={"height": "700px", "width": "100%"}, ),
    html.Iframe(src="assets/graphs/us_states_death_count.html",
                style={"height": "700px", "width": "100%"}, ),
    html.Iframe(src="assets/graphs/us_provinces_death_count.html",
                style={"height": "700px", "width": "100%"}, ),
])

####################################################################################################
# 002 - Page 2
####################################################################################################

us = html.Div([

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
# 003 - Page 3
####################################################################################################

individual = html.Div([

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
