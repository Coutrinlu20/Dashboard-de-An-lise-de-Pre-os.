from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
import pandas as pd

# Initialize the app with suppress_callback_exceptions=True
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Styles
url_theme1 = dbc.themes.VAPOR
url_theme2 = dbc.themes.FLATLY
template_theme1 = 'vapor'
template_theme2 = 'flatly'

# Data
df = pd.read_excel('user_transactions_report.xlsx')
state_options = [{'label': x, 'value': x} for x in df['type'].unique()]

# Layout
app.layout = dbc.Container([
    # Row 1
    dbc.Row([
        dbc.Col([
            ThemeSwitchAIO(aio_id='theme', themes=[url_theme1, url_theme2]),
            html.H3('Tipo x Valor'),
            dcc.Dropdown(
                id='type',
                value=[state['label'] for state in state_options[:3]],
                multi=True,
                options=state_options
            ),
            dcc.Graph(id='line_graph'),
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='type1',
                value=state_options[0]['label'],
                options=state_options
            )
        ], sm=12,md=6),
        dbc.Col([
            dcc.Dropdown(
                id='type2',
                value=state_options[1]['label'],
                options=state_options
            )
        ],sm=12,md=6),
        dbc.Col([
            dcc.Graph(id='indicator1')
        ]),
        dbc.Col([
             dcc.Graph(id='indicator2')
        ])

    ])
])

# Callbacks
@app.callback(
    Output('line_graph', 'figure'),
    Input('type', 'value'),
    Input(ThemeSwitchAIO.ids.switch('theme'),('value'))
)
def line(type, toggle):
    template = template_theme1 if toggle else template_theme2
    df_data = df.copy(deep=True)
    mask = df_data['type'].isin(type)
    fig = px.line(df_data[mask], x='time', y='amount', color='type', template=template)
    return fig

 #indicators
@app.callback(
    Output('indicator1', 'figure'),
    Output('indicator2','figure'),
    Input('type1','value'),
    Input('type2','value'),
    Input(ThemeSwitchAIO.ids.switch('theme'),('value'))
)
def indicatord (type1,type2, toggle ):
    template = template_theme1 if toggle else template_theme2
    df_data = df.copy(deep=True)
    df_type1 =df_data[df_data['type'].isin([type1])]
    df_type2=df_data[df_data['type'].isin([type2])]

    initial_date = str(int(df_data['time'].min()) -1)
    final_date = df_data['time'].max()

    iterable = [(type1,data_type1),(type2,data_type2)]
    indicators = []

    for type , data in iterable:
        fig = go.figure()
        fig.add_trace(go.Indicator(
            mode= 'number',
            title={'text': f"<span>{type}</span><br><span>{initial_date} -{final_date}</span>"},
            value=data.at[data.index[-1],'amount'],
            number={'prefix': 'R$', 'valueformat':'.2f'},
            delta={'relative': True, 'valueformat': '.1%', 'reference':data.at[data.index[0],'amount'] }
        ))

        fig.update_layout(template=template)
        indicators.append(fig)
    return indicators

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True, port=8080)

# from dash import Dash, dcc, html, Input, Output
# import plotly.express as px
# import plotly.graph_objects as go
# import pandas as pd
# from pandas import read_excel

# from app import *
# from dash_bootstrap_templates import ThemeSwitchAIO
# #Styles
# url_theme1 = dbc.themes.VAPOR
# url_theme2 = dbc.themes.FLATLY
# template_theme1 = 'vapor'
# template_theme2 = 'flatly'

# #### dados
# df = pd.read_excel('transactions_output.xlsx')
# state_options = [{'label': x, 'value': x} for x in  df ['source'].unique()]

# #layout
# app.layout = dbc.Container([
#     #row1
#    dbc.Row([
#        dbc.Col([
#            ThemeSwitchAIO(aio_id='theme', themes=[url_theme1, url_theme2]),
#            html.H3('source x Crypto'),
#            dcc.Dropdown(
#                id='Crypto',
#                value=[state['label'] for state in state_options[:3]],
#                multi=True,
#                options=state_options
#            ),
#            dcc.Graph(id='line_graph')
#        ])
#    ]),
#    #row2
# ])
# #collabacks==================
# @app.callback(
#    Output('line_graph', 'figure'),
#     Input('source', 'value')
# )
# def line(source):
#     df_data = df.copy(deep=True)
#     mask = df_data['SOURCE'].isin(source)
#     fig = px.line(df_data[mask], x='creation_time',y='Crypto',
#                 color='source')
#     return fig
# # Rodar o servidor
# if __name__ == '__main__':
#     app.run_server(debug=True, port='8080')

