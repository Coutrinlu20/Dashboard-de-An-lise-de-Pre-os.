from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from app import *
from dash_bootstrap_templates import ThemeSwitchAIO
#Styles
url_theme1 = dbc.themes.VAPOR
url_theme2 = dbc.themes.FLATLY
template_theme1 = 'vapor'
template_theme2 = 'flatly'

#### dados
df = pd.read_csv('transactions_output.csv')
state_options = [{'label': x, 'value': x} for x in  df ['source'].unique()]

#layout
app.layout = dbc.Container([
   dbc.Row([
       dbc.Col([
           ThemeSwitchAIO(aio_id='theme', themes=[url_theme1, url_theme2]),
           html.H3('source x Crypto'),
           dcc.Dropdown(
               id='Crypto',
               value=[state['label'] for state in state_options[:3]],
               multi=True,
               options=state_options
           ),
           dcc.Graph(id='line_graph')
       ])
   ]),
   dbc.Row([
       dbc.Col([
           
       ])
   ])
])
# Rodar o servidor
if __name__ == '__main__':
    app.run_server(debug=True, port='8080')

