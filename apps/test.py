import dash as dash
import geojson as geojson
from dash import Dash
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from app import app

now = datetime.now()
if(now.hour <19 and now.minute < 54):
    current_date = datetime.today() - timedelta(1)
else:
    current_date = datetime.today()

#current_date = datetime.today() - timedelta(1)

current_date = current_date.strftime('%Y-%m-%d')
print(current_date)
df = pd.read_csv("apps/donnees-hospitalieres.csv", sep =";")
print(df.head())

stringtolook = "https://static.data.gouv.fr/resources/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/20210320-185421/donnees-hospitalieres-covid19-"
stringend = "-18h54.csv"
link = stringtolook + current_date + stringend
print("tes  %s", link)
test_dataset = link
#test_dataset = "https://static.data.gouv.fr/resources/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/20210320-185421/donnees-hospitalieres-covid19-2021-03-20-18h54.csv"
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
#server = app.server

dffre = pd.read_csv(test_dataset, sep=";")
dffre = dffre.drop(['HospConv', 'SSR_USLD', 'autres'], axis=1)
print("test")
print(dffre.head())

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

with open('apps/departements.geojson') as file:
    geo = geojson.load(file)

df_map = df[(df['jour'] == '2021-03-02') & (df['sexe'] == 0)]
df_dep_reg = pd.read_csv('apps/departements-region.csv')

df_map['dep_name'] = df_dep_reg['dep_name'].to_numpy()
df_map['region_name'] = df_dep_reg['region_name'].to_numpy()
df_curr_situation = df_map
df_curr_situation['total_hosp_per_region'] = df_curr_situation.groupby(['region_name'], as_index=False)['hosp'].cumsum()
df_curr_situation['total_rea_per_region'] = df_curr_situation.groupby(['region_name'], as_index=False)['rea'].cumsum()

df_curr_situation_fig_hosp = df_curr_situation.groupby(['region_name'], as_index=False).max()


figtest = px.choropleth(df_map, geojson= geo, locations='dep', featureidkey="properties.code", color='dc',labels={'dc': 'Total décès'}, color_continuous_scale="Viridis", scope="europe",hover_name='dep_name' ,hover_data=['hosp', 'rea'])
figtest.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations")
#figtest.update_layout(margin={"r":50,"t":50,"l":50,"b":50})
figtest.update_layout(width = 1000, height = 1000)

fig_region = px.pie(df_curr_situation_fig_hosp, values='total_hosp_per_region', names='region_name', title="Hospitalisation by region")
fig_region_rea = px.pie(df_curr_situation_fig_hosp, values='total_rea_per_region', names='region_name', title="Reanimation by region")

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
fig_bot_left.update_traces(textposition='outside',
                                  textinfo='percent+label',
                                  marker=dict(line=dict(color='#000000',
                                                        width=2)),
                                  pull=[0.05, 0, 0.03],
                                  opacity=0.9,
                                  # rotation=180
                            )

fig_t = px.pie(df_filtered, values="dc", names="sexe_str", title="Deceased by Gender")
fig_t.update_traces(textposition='outside',
                                  textinfo='percent+label',
                                  marker=dict(line=dict(color='#000000',
                                                        width=2)),
                                  pull=[0.05, 0, 0.03],
                                  opacity=0.9,
                                  # rotation=180
                            )

fig_total_hosp = px.scatter(df_cumul_hosp, x ='jour', y='cumul_hosp', title="Evolution of the number of people hospitalized in France")
fig_total_rea = px.scatter(df_cumul_hosp, x ='jour', y='cumul_rea', title="Evolution of the number of people in reanimation in France")

layout = html.Div([
    html.H1('Covid Data in France', style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.H4('Global evolution in France', style={"color": "white", "textAlign":"center"}),
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
            html.H4('Hospitalisations and Reanimations', style={"color": "white", "textAlign": "center"}),
            html.Br(),
            html.P("Now let's have a look at the total number of people who were hospitalized and who were in reanimation",
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P(
                'We can see the number of hospitalisations every day and number of reanimation (these results are cumulated)\n',
                style={"textAlign": "justify", "color": "white"}),
            html.Br(),

            html.P("",
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P("",
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P("",
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P("",
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P("",
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P("",
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P("",
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P("",
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P("",
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P("",
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),


        ], className="six columns", style={"backgroundColor": "#313131","padding": "3%"}),


        #dcc.Graph(id = 'third-graph', figure= fig_bot_right, className='three columns'),
        #dcc.Graph(id = 'fourth-graph', figure= fig_bot_right, className='three columns')
    ],className="row", style={"border": "solid", "padding":"2%"}),

    html.Div([


        html.Div([
            html.H4('Analysis per Gender', style={"color": "white", "textAlign": "center"}),
            html.Br(),
            html.P(
                "Now let's have a look at the influence of the gender on the different aspects of the pandemic",
                style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P(
                'We can see total number of hospitalisations, reanimations and deceased per gender to see the impact of it\n',
                style={"textAlign": "justify", "color": "white"}),
            html.Br(),

        ], className="row", style={"backgroundColor": "#313131", "padding": "3%"}),


        html.Div([
            html.Div([
                dcc.Graph(
                    id='graph2',
                    figure=fig_bot_right
                ),
            ], className='four columns'),

            html.Div([
                dcc.Graph(
                    id='graph3',
                    figure=fig_bot_left
                ),
            ], className='four columns'),

            html.Div([
                dcc.Graph(
                    id='graph15',
                    figure=fig_t
                ),
            ], className='four columns'),

        ], className="row"),


    ], style={"padding": "3%", "border": "solid"}),

    html.Div([
        html.H2('Current COVID-19 situation in France', style={"color": "white", "textAlign": "center"}),
    ], className="row", style={"backgroundColor": "#313131", "padding": "3%"}),

    html.Div([



        html.Div([
            dcc.Graph(
                id='graph8',
                figure=figtest),
        ], className="seven columns", style={"height":"100%"}),

        html.Div([

            html.Div([
                dcc.Graph(
                    id='graph861',
                    figure=fig_region),
            ], style={"height": "100%"}),

            html.Div([
                dcc.Graph(
                    id='graph871',
                    figure=fig_region_rea),
            ], style={"height": "100%"}),

        ], className="five columns", style={"backgroundColor": "#313131", "padding":"3%"}),

    ], className="row", style={"padding": "3%", "border": "solid"}),



], style={"padding": "3%"})

@app.callback(
    Output('first_graph', 'figure'),
    [Input("yaxis-column", "value")]
)
def update_figure(yaxis_column_name):
    return px.scatter(
        df_firstgraph, x=df_firstgraph['jour'], y=df_firstgraph[yaxis_column_name], color='dep',
        render_mode="webgl", title="Evolution of the COVID-19 situation in France"
    )


#if __name__ == '__main__':
 #   app.run_server(debug=False)
