import numpy as np
import pandas as pd
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from app import app
from dash import dcc
from dash import html
from scipy.optimize import minimize
from plotly import graph_objs as go
from scipy.integrate import solve_ivp
from dash.dependencies import Input, Output

country = 'US'

# Confirmed cases
infected_df = pd.read_csv("/Users/jacobceles/stash/covid-viz-hub/backend/data/time_series_covid_19_confirmed.csv")
cols = infected_df.columns[4:]
infected = infected_df.loc[infected_df['Country/Region'] == country, cols].values.flatten()

# Deaths
deceased_df = pd.read_csv("/Users/jacobceles/stash/covid-viz-hub/backend/data/time_series_covid_19_deaths.csv")
deceased = deceased_df.loc[deceased_df['Country/Region'] == country, cols].values.flatten()

# Recovered
recovered_df = pd.read_csv('/Users/jacobceles/stash/covid-viz-hub/backend/data/time_series_covid_19_recovered.csv')
recovered = recovered_df.loc[recovered_df['Country/Region'] == country, cols].values.flatten()

dates = cols.values
x = [dt.datetime.strptime(d, '%m/%d/%y').date() for d in dates]
fig_actual = go.Figure()

image_path = 'assets/covid_fig1.png'
infected_clean = infected[30:]
deceased_clean = deceased[30:]
recovered_clean = recovered[30:]


def SEIR_q(t, y, beta, gamma, sigma, alpha, t_quarantine):
    """SEIR epidemic model.
        S: subsceptible
        E: exposed
        I: infected
        R: recovered

        N: total population (S+E+I+R)

        Social distancing is adopted when t>=t_quarantine.
    """
    S = y[0]
    E = y[1]
    I = y[2]
    R = y[3]

    if t > t_quarantine:
        beta_t = beta * np.exp(-alpha * (t - t_quarantine))
    else:
        beta_t = beta
    dS = -beta_t * S * I / N
    dE = beta_t * S * I / N - sigma * E
    dI = sigma * E - gamma * I
    dR = gamma * I
    return [dS, dE, dI, dR]


N = 100
beta, gamma, sigma, alpha = [2, 0.4, 0.1, 0.5]
t_q = 10
y0 = np.array([99, 0, 1, 0])
sol = solve_ivp(SEIR_q, [0, 100], y0, t_eval=np.arange(0, 100, 0.1), args=(beta, gamma, sigma, alpha, t_q))


# print(sol)
# fig_seir_model = go.Figure(data=go.Scatter(x=sol.t, y=sol.y[0], name='Susceptible, with intervention',
#                                line=dict(color=px.colors.qualitative.Plotly[0])))
# fig_seir_model.add_trace(go.Scatter(x=sol.t, y=sol.y[1], name='Exposed, with intervention',
#                         line=dict(color=px.colors.qualitative.Plotly[1])))
# fig_seir_model.add_trace(go.Scatter(x=sol.t, y=sol.y[2], name='Infected, with intervention',
#                         line=dict(color=px.colors.qualitative.Plotly[2])))
# fig_seir_model.add_trace(go.Scatter(x=sol.t, y=sol.y[3], name='Recovered, with intervention',
#                         line=dict(color=px.colors.qualitative.Plotly[3])))
#
#
# beta, gamma, sigma, alpha = [2, 0.4, 0.1, 0.0]
# t_q = 10
# y0 = np.array([99, 0, 1, 0])
# sol = solve_ivp(SEIR_q, [0, 100], y0, t_eval=np.arange(0, 100, 0.1), args=(beta, gamma, sigma, alpha, t_q))
#
# fig_seir_model.add_trace(go.Scatter(x=sol.t, y=sol.y[0], name='Susceptible, no intervention',
#                                line=dict(color=px.colors.qualitative.Plotly[0], dash='dash')))
# fig_seir_model.add_trace(go.Scatter(x=sol.t, y=sol.y[1], name='Exposed, no intervention',
#                         line=dict(color=px.colors.qualitative.Plotly[1], dash='dash')))
# fig_seir_model.add_trace(go.Scatter(x=sol.t, y=sol.y[2], name='Infected, no intervention',
#                         line=dict(color=px.colors.qualitative.Plotly[2], dash='dash')))
# fig_seir_model.add_trace(go.Scatter(x=sol.t, y=sol.y[3], name='Recovered, no intervention',
#                         line=dict(color=px.colors.qualitative.Plotly[3], dash='dash')))
#
# fig_seir_model.update_layout(title='SEIR epidemic model',
#                  xaxis_title='Days',
#                  yaxis_title='Percentage of population')
# fig_seir_model.show()


def fit_to_data(vec, t_q, N, test_size):
    beta, gamma, sigma, alpha = vec

    sol = solve_ivp(SEIR_q, [0, t_f], y0, args=(beta, gamma, sigma, alpha, t_q), t_eval=t_eval)

    split = int((1 - test_size) * infected_clean.shape[0])

    error = (
                    np.sum(
                        5 * (deceased_clean[:split] - sol.y[3][:split]) ** 2) +
                    np.sum(
                        (infected_clean[:split] - np.cumsum(sol.y[1][:split] + sol.y[2][:split])) ** 2)
            ) / split

    return error


N = 60e6 / (10 / 1.1)
N = int(N)
t_q = 7  # quarantine takes place
t_f = infected_clean.shape[0]
y0 = [N - infected_clean[0], 0, infected_clean[0], 0]
t_eval = np.arange(0, t_f, 1)
test_size = 0.1

test_size = 0

opt = minimize(fit_to_data, [2, 1, 0.8, 0.3], method='Nelder-Mead', args=(t_q, N, test_size))
beta, gamma, sigma, alpha = opt.x
sol = solve_ivp(SEIR_q, [0, t_f], y0, args=(beta, gamma, sigma, alpha, t_q), t_eval=t_eval)

fig_predic_model = go.Figure(data=go.Scatter(x=x[30:], y=np.cumsum(sol.y[1] + sol.y[2]), name='E+I',
                                             marker_color=px.colors.qualitative.Plotly[0]))
fig_predic_model.add_trace(go.Scatter(x=x[30:], y=infected_clean, name='Infected', mode='markers',
                                      marker_color=px.colors.qualitative.Plotly[0]))
fig_predic_model.add_trace(go.Scatter(x=x[30:], y=sol.y[3], name='R', mode='lines',
                                      marker_color=px.colors.qualitative.Plotly[1]))
# fig_predic_model.add_trace(go.Scatter(x=x[30:], y=deceased_clean+recovered_clean, name='Deceased+recovered',
#                          mode='markers',
#                          marker_color=px.colors.qualitative.Plotly[1]))
# fig_predic_model.add_trace(go.Scatter(x=[x[37], x[37]], y=[0, 100000], name='Quarantine', mode='lines',
#                         marker_color='darkgrey'))
fig_predic_model.update_layout(title='''Model's fit to US-Infected data''',
                               xaxis_title='Days',
                               yaxis_title='Number of individuals')

R_0 = beta / gamma
incubation = 1 / sigma


def SEIR_q_stop(t, y, beta, gamma, sigma, alpha, t_quarantine, t_stop):
    """SEIR epidemic model.
        S: subsceptible
        E: exposed
        I: infected
        R: recovered

        N: total population (S+E+I+R)

        Social distancing is adopted when t>t_quarantine and t<=t_stop.
    """
    S = y[0]
    E = y[1]
    I = y[2]
    R = y[3]

    if (t > t_quarantine and t <= t_stop):
        beta_t = beta * np.exp(-alpha * (t - t_quarantine))
    else:
        beta_t = beta
    dS = -beta_t * S * I / N
    dE = beta_t * S * I / N - sigma * E
    dI = sigma * E - gamma * I
    dR = gamma * I
    return [dS, dE, dI, dR]


N = 100
beta, gamma, sigma, alpha = [2, 0.4, 0.1, 0.5]
t_q = 10
t_stop = 30
y0 = np.array([99, 0, 1, 0])
sol = solve_ivp(SEIR_q_stop, [0, 100], y0, t_eval=np.arange(0, 100, 0.1), args=(beta, gamma, sigma, alpha, t_q, t_stop))

fig_soc_dist_model = go.Figure(data=go.Scatter(x=sol.t, y=sol.y[0], name='Susceptible, interrupted',
                                               line=dict(color=px.colors.qualitative.Plotly[0])))
fig_soc_dist_model.add_trace(go.Scatter(x=sol.t, y=sol.y[1], name='Exposed, interrupted',
                                        line=dict(color=px.colors.qualitative.Plotly[1])))
fig_soc_dist_model.add_trace(go.Scatter(x=sol.t, y=sol.y[2], name='Infected, interrupted',
                                        line=dict(color=px.colors.qualitative.Plotly[2])))
fig_soc_dist_model.add_trace(go.Scatter(x=sol.t, y=sol.y[3], name='Recovered, interrupted',
                                        line=dict(color=px.colors.qualitative.Plotly[3])))

t_stop = 200
sol = solve_ivp(SEIR_q_stop, [0, 100], y0, t_eval=np.arange(0, 100, 0.1), args=(beta, gamma, sigma, alpha, t_q, t_stop))

fig_soc_dist_model.add_trace(go.Scatter(x=sol.t, y=sol.y[0], name='Susceptible, continuous',
                                        line=dict(color=px.colors.qualitative.Plotly[0], dash='dash')))
fig_soc_dist_model.add_trace(go.Scatter(x=sol.t, y=sol.y[1], name='Exposed, continuous',
                                        line=dict(color=px.colors.qualitative.Plotly[1], dash='dash')))
fig_soc_dist_model.add_trace(go.Scatter(x=sol.t, y=sol.y[2], name='Infected, continuous',
                                        line=dict(color=px.colors.qualitative.Plotly[2], dash='dash')))
fig_soc_dist_model.add_trace(go.Scatter(x=sol.t, y=sol.y[3], name='Recovered, continuous',
                                        line=dict(color=px.colors.qualitative.Plotly[3], dash='dash')))

fig_soc_dist_model.update_layout(title='SEIR epidemic model - effect of social-distancing',
                                 xaxis_title='Days',
                                 yaxis_title='Percentage of population')
# fig_soc_dist_model.show()
available_countries = ['India', 'US', 'China', 'Germany', 'Brazil']

layout = html.Div([
    dbc.Container([
        dbc.Row([dbc.Col(html.H1(children='SEIR MODEL'), className="mb-2", style={'textAlign': 'center'})]),
        # dbc.Row([dbc.Col(html.H6(children='Visualising trends across the world'), className="mb-4")]),
        dbc.Row([dbc.Col(html.Img(src=image_path, style={'align': 'center'}), style={'textAlign': 'center'})]),
        dbc.Row([dbc.Col(html.Img(src='/assets/seir_model.png', style={'align': 'center'}),
                         style={'textAlign': 'center'})]),
        dbc.Row([dbc.Col(
            dbc.Card(html.H3(children='COVID ANALYTICS with SEIR MODEL', className="text-center text-light bg-dark"),
                     body=True, color="dark"),
            className="mb-4")]),

        dcc.Dropdown(id='countries', options=[{'label': i, 'value': i} for i in available_countries],
                     value='US', multi=False,
                     style={'width': '70%', 'margin-left': '5px', 'align': 'center'}),
        dcc.Graph(id='fig_actual'),
        # bar charts
        # dbc.Row([dbc.Col(html.Div([dcc.Graph(figure=fig_actual)]))]),
        # dcc.RangeSlider(min=0, max=1.0, step=0.01, value=0.160, description='𝜎',id='my-range-slider'),
        # dbc.Row([dbc.Col(html.Div([dcc.Graph(figure=fig_seir_model)]))]),
        dbc.Row([dbc.Col(html.Div([dcc.Graph(figure=fig_predic_model)]))]),
        # input multiple dropdowns
        dbc.Row([dbc.Col(html.Div([
            html.Label(" alpha", style={'width': '100%', 'margin-left': '5px', 'align': 'center'}),
            dcc.Dropdown(id="alpha-filter",
                         options=[{"label": alpha, "value": alpha} for alpha in
                                  [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]],
                         value=0.3, clearable=False, className="dropdown",
                         style={'width': '100%', 'margin-left': '5px', 'align': 'center'})])),
            dbc.Col(html.Div([
                html.Label(" beta"),
                dcc.Dropdown(id="beta-filter",
                             options=[{"label": beta, "value": beta} for beta in
                                      [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]],
                             value=0.2, clearable=False, className="dropdown",
                             style={'width': '100%', 'margin-left': '5px', 'align': 'center'}, )])),
            dbc.Col(html.Div([
                html.Label(" gamma"),
                dcc.Dropdown(id="gamma-filter",
                             options=[{"label": gamma, "value": gamma} for gamma in
                                      [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]],
                             value=0.1, clearable=False, className="dropdown",
                             style={'width': '100%', 'margin-left': '5px', 'align': 'center'}, )]))
            ,
            dbc.Col(html.Div([
                html.Label(" sigma"),
                dcc.Dropdown(id="sigma-filter",
                             options=[{"label": sigma, "value": sigma} for sigma in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]],
                             value=0.0, clearable=False, className="dropdown",
                             style={'width': '100%', 'margin-left': '5px', 'align': 'center'}, )]))
        ], style={'display': 'flex'}),
        dcc.Graph(id='fig_seir_model'),
        dbc.Row([dbc.Col(html.Div([dcc.Graph(figure=fig_soc_dist_model)]))])
    ])
])


@app.callback(Output('fig_actual', 'figure'),
              [Input('countries', 'value')])
def update_graph(country_name):
    infected = infected_df.loc[infected_df['Country/Region'].isin([country_name]), cols].values.flatten()
    deceased = deceased_df.loc[deceased_df['Country/Region'].isin([country_name]), cols].values.flatten()
    recovered = recovered_df.loc[recovered_df['Country/Region'].isin([country_name]), cols].values.flatten()
    dates = cols.values
    x = [dt.datetime.strptime(d, '%m/%d/%y').date() for d in dates]
    # fig_actual = go.Figure()
    fig_actual = go.Figure(data=go.Scatter(x=x, y=infected,
                                           mode='lines+markers',
                                           name='Infected'))
    fig_actual.add_trace(go.Scatter(x=x, y=deceased,
                                    mode='lines+markers',
                                    name='Deceased'))
    fig_actual.add_trace(go.Scatter(x=x, y=recovered,
                                    mode='lines+markers',
                                    name='Recovered'))
    fig_actual.update_layout(title='COVID-19 spread in US',
                             xaxis_title='Days',
                             yaxis_title='Number of individuals')

    return fig_actual


@app.callback(Output('fig_seir_model', 'figure'),
              [Input('alpha-filter', 'value'),
               Input('beta-filter', 'value'),
               Input('gamma-filter', 'value'),
               Input('sigma-filter', 'value')])
def update_graph(alpha_f, beta_f, gamma_f, sigma_f):
    N = 100
    alpha_f = alpha_f
    beta_f = beta_f
    gamma_f = gamma_f
    sigma_f = sigma_f

    beta, gamma, sigma, alpha = [alpha_f, beta_f, gamma_f, sigma_f]
    t_q = 10
    y0 = np.array([99, 0, 1, 0])
    sol = solve_ivp(SEIR_q, [0, 100], y0, t_eval=np.arange(0, 100, 0.1), args=(beta, gamma, sigma, alpha, t_q))

    fig_seir_model = go.Figure(data=go.Scatter(x=sol.t, y=sol.y[0], name='Susceptible, with intervention',
                                               line=dict(color=px.colors.qualitative.Plotly[0])))
    fig_seir_model.add_trace(go.Scatter(x=sol.t, y=sol.y[1], name='Exposed, with intervention',
                                        line=dict(color=px.colors.qualitative.Plotly[1])))
    fig_seir_model.add_trace(go.Scatter(x=sol.t, y=sol.y[2], name='Infected, with intervention',
                                        line=dict(color=px.colors.qualitative.Plotly[2])))
    fig_seir_model.add_trace(go.Scatter(x=sol.t, y=sol.y[3], name='Recovered, with intervention',
                                        line=dict(color=px.colors.qualitative.Plotly[3])))

    fig_seir_model.update_layout(title='SEIR epidemic model',
                                 xaxis_title='Days',
                                 yaxis_title='Percentage of population')

    beta, gamma, sigma, alpha = [2, 0.4, 0.1, 0.0]
    t_q = 10
    y0 = np.array([99, 0, 1, 0])
    sol = solve_ivp(SEIR_q, [0, 100], y0, t_eval=np.arange(0, 100, 0.1), args=(beta, gamma, sigma, alpha, t_q))

    fig_seir_model.add_trace(go.Scatter(x=sol.t, y=sol.y[0], name='Susceptible, no intervention',
                                        line=dict(color=px.colors.qualitative.Plotly[0], dash='dash')))
    fig_seir_model.add_trace(go.Scatter(x=sol.t, y=sol.y[1], name='Exposed, no intervention',
                                        line=dict(color=px.colors.qualitative.Plotly[1], dash='dash')))
    fig_seir_model.add_trace(go.Scatter(x=sol.t, y=sol.y[2], name='Infected, no intervention',
                                        line=dict(color=px.colors.qualitative.Plotly[2], dash='dash')))
    fig_seir_model.add_trace(go.Scatter(x=sol.t, y=sol.y[3], name='Recovered, no intervention',
                                        line=dict(color=px.colors.qualitative.Plotly[3], dash='dash')))
    return fig_seir_model

# if __name__ == '__main__':
#     app.run_server(port = 8000)

# @app.callback(Output('fig_seir_model', 'figure'),
#               [Input('countries', 'value')])
# def update_graph(country_name):
#     infected = infected_df.loc[infected_df['Country/Region'].isin([country_name]), cols].values.flatten()
#     deceased = deceased_df.loc[deceased_df['Country/Region'].isin([country_name]), cols].values.flatten()
#     recovered = recovered_df.loc[recovered_df['Country/Region'].isin([country_name]), cols].values.flatten()
#     dates = cols.values
#     x = [dt.datetime.strptime(d, '%m/%d/%y').date() for d in dates]
#     #fig_actual = go.Figure()
#     fig_actual = go.Figure(data=go.Scatter(x=x, y=infected,
#                                    mode='lines+markers',
#                                    name='Infected'))
#     fig_actual.add_trace(go.Scatter(x=x, y=deceased,
#                                     mode='lines+markers',
#                                     name='Deceased'))
#     fig_actual.add_trace(go.Scatter(x=x, y=recovered,
#                                     mode='lines+markers',
#                                     name='Recovered'))
#     fig_actual.update_layout(title='COVID-19 spread in US',
#                              xaxis_title='Days',
#                              yaxis_title='Number of individuals')
#
#     return fig_seir_model
