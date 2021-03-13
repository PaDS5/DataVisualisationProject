import dash as dash
import geojson as geojson
from dash import Dash
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np

df = pd.read_csv("donnees-hospitalieres.csv", sep = ";")
print(df.head())


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
server = app.server


liste_y = ['hosp', 'rea', 'rad', 'dc']
liste_x = ['jour']
liste_dep = ['dep']


df_firstgraph = df[df['sexe'] == 0]
df_cumul_hosp = df_firstgraph
df_cumul_hosp['cumul_hosp'] = df_cumul_hosp.groupby(['jour'], as_index=False)['hosp'].cumsum()
df_cumul_hosp = df_cumul_hosp.groupby(['jour'], as_index=False).max()
df_cumul_hosp['cumul_rea'] = df_cumul_hosp.groupby(['jour'], as_index=False)['rea'].cumsum()
df_cumul_hosp = df_cumul_hosp.groupby(['jour'], as_index = False).max()

df_filtered = df[df['sexe'] != 0]
df_filtered['sexe_str'] = df_filtered['sexe'].apply(lambda x: "Homme" if x == 1 else "Femme")


df_new_filtered = df[df['sexe'] == 0].groupby('dep')

fig = px.pie(df_filtered, values="rea", names="sexe")

with open('departements.geojson') as file:
    geo = geojson.load(file)

figtest = px.choropleth(df, geojson= geo, locations='dep', featureidkey="properties.code", color_continuous_scale="Viridis", scope="europe")
figtest.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations")
#figtest.update_layout(margin={"r":50,"t":50,"l":50,"b":50})
figtest.update_layout(width = 1000, height = 1000)

fig_bot_right = px.pie(df_filtered, values="hosp", names="sexe_str", title = "Hospitalisations by Gender")
fig_bot_right.update_traces(textposition='outside',
                                  textinfo='percent+label',
                                  marker=dict(line=dict(color='#000000',
                                                        width=2)),
                                  pull=[0.05, 0, 0.03],
                                  opacity=0.9,
                                  # rotation=180
                            )

fig_bot_left = px.pie(df_filtered, values="rea", names="sexe_str", title = "Reanimation by Gender")

fig_total_hosp = px.scatter(df_cumul_hosp, x ='jour', y='cumul_hosp', title="Evolution of the number of people hospitalized in France")
fig_total_rea = px.scatter(df_cumul_hosp, x ='jour', y='cumul_rea', title="Evolution of the number of people in reanimation in France")

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

    html.Br(),
    html.Br(),

    html.Div([

        html.Div([
            dcc.Graph(
                id='graph1',
                figure=fig_total_hosp
            ),

            html.Br(),

            dcc.Graph(
                id='graph4',
                figure=fig_total_rea),
        ], className='six columns'),

        html.Div([
            html.Br()
        ], className="one columns"),

        html.Div([
            html.H4('Second paragraph', style={"color": "white", "textAlign": "center"}),
            html.Br(),
            html.P("Now let's have a look at the total number of people who were hospitalized and who were in reanimation",
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P(
                'We can see the number of hospitalisations every day, number of reanimation and deaths (cumulated)\n',
                style={"textAlign": "justify", "color": "white"}),
            html.Br(),

            html.P("Now let's have a look at the total number of people who were hospitalized and who were in reanimation",
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P("Now let's have a look at the total number of people who were hospitalized and who were in reanimation",
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P("Now let's have a look at the total number of people who were hospitalized and who were in reanimation",
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P("Now let's have a look at the total number of people who were hospitalized and who were in reanimation",
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P("Now let's have a look at the total number of people who were hospitalized and who were in reanimation",
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P("Now let's have a look at the total number of people who were hospitalized and who were in reanimation",
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P("Now let's have a look at the total number of people who were hospitalized and who were in reanimation",
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P("Now let's have a look at the total number of people who were hospitalized and who were in reanimation",
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P("Now let's have a look at the total number of people who were hospitalized and who were in reanimation",
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P("Now let's have a look at the total number of people who were hospitalized and who were in reanimation",
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),


        ], className="six columns", style={"backgroundColor": "#313131","padding": "3%"}),


        #dcc.Graph(id = 'third-graph', figure= fig_bot_right, className='three columns'),
        #dcc.Graph(id = 'fourth-graph', figure= fig_bot_right, className='three columns')
    ],className="row", style={"border": "solid", "padding":"2%"}),

    html.Div([


        html.Div([
            html.H4('Second paragraph', style={"color": "white", "textAlign": "center"}),
            html.Br(),
            html.P(
                "Now let's have a look at the total number of people who were hospitalized and who were in reanimation",
                style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P(
                'We can see the number of hospitalisations every day, number of reanimation and deaths (cumulated)\n',
                style={"textAlign": "justify", "color": "white"}),
            html.Br(),

        ], className="seven columns", style={"backgroundColor": "#313131", "padding": "3%"}),

        html.Div([
            html.Br()
        ], className="one columns"),

        html.Div([
            dcc.Graph(
                id='graph2',
                figure=fig_bot_right),

            html.Br(),

            dcc.Graph(
                id='graph3',
                figure=fig_bot_left),
        ], className="four columns"),


    ], className="row", style={"padding": "3%", "border": "solid"}),

    html.Div([

        html.Div([
            dcc.Graph(
                id='graph8',
                figure=figtest),
        ], className="seven columns", style={"height":"100%"}),

        html.Div([
            html.H4('Second paragraph', style={"color": "white", "textAlign": "center"}),
            html.Br(),
            html.P(
                "Now let's have a look at the total number of people who were hospitalized and who were in reanimation",
                style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P(
                'We can see the number of hospitalisations every day, number of reanimation and deaths (cumulated)\n',
                style={"textAlign": "justify", "color": "white"}),
            html.Br(),

        ], className="five columns", style={"backgroundColor": "#313131"}),

    ])

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
    app.run_server(debug=False)
