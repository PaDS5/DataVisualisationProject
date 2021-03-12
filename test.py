import dash as dash
from dash import Dash
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

df = pd.read_csv("donnees-hospitalieres.csv", sep = ";")
print(df.head())

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
server = app.server

liste_y = ['hosp', 'rea', 'rad', 'dc']
liste_x = ['jour']
liste_dep = ['dep']

test = df.groupby('dep')
print(test.head())

df_firstgraph = df[df['sexe'] == 0]
df_filtered = df[df['sexe'] != 0]

df_new_filtered = df[df['sexe'] == 0].groupby('dep')

fig = px.pie(df_filtered, values="rea", names="sexe")

fig_bot_right = px.pie(df_filtered, values="hosp", names="sexe", title = "Hospitalisations by Gender")
fig_bot_left = px.pie(df_filtered, values="rea", names="sexe", title = "Reanimation by Gender")


app.layout = html.Div([
    html.H1('Covid Data in France', style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.H4('First graph', style={"color": "white", "textAlign":"center"}),
            html.Br(),
            html.P('Here we can choose the parameter that we want to see across time', style={"textAlign" : "justify", "color": "white"}),
            html.Br(),
            html.P('We can see the number of hospitalisations every day, number of reanimation and deaths (cumulated)\n', style={"textAlign" : "justify", "color": "white"}),
            html.Br(),
            html.Div(dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in liste_y],
                value='hosp'
            )),
        ], className= "three columns", style={"padding" : "3%"}),

        html.Div([
            dcc.Graph(id = 'first_graph', figure = {})
        ], className= "nine columns")

    ], className= 'row', style={"backgroundColor": "#313131"}),

    html.Div([
        html.Div([
            html.H1(children='Hello Dash'),

            html.Div(children='''
        Dash: A web application framework for Python.
    '''),

            dcc.Graph(
                id='graph1',
                figure=fig_bot_left
            ),
        ], className='three columns'),
        html.Div([
            html.H1(children='Hello Dash'),

            html.Div(children='''
        Dash: A web application framework for Python.
    '''),

            dcc.Graph(
                id='graph2',
                figure=fig_bot_right
            ),
        ], className='three columns'),
        #dcc.Graph(id = 'third-graph', figure= fig_bot_right, className='three columns'),
        #dcc.Graph(id = 'fourth-graph', figure= fig_bot_right, className='three columns')
    ],className="row", style={"backgroundColor": "#800081", "border": "solid"})



], style={"padding": "3%", "border": "solid"})

@app.callback(
    Output('first_graph', 'figure'),
    [Input("yaxis-column", "value")]
)
def update_figure(yaxis_column_name):
    return px.scatter(
        df_firstgraph, x=df_firstgraph['jour'], y=df_firstgraph[yaxis_column_name], color='dep',
        render_mode="webgl", title="Evolution of the COVID-19 situation in France"
    )


if __name__ == '__main__':
    # app4.run_server(mode = 'inline')
    app.run_server(debug=False)
