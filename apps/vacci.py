import dash as dash
import geojson as geojson
from dash import Dash
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
from app import app

df = pd.read_csv("apps/vacsi-s-dep-2021-03-02-20h15.csv", sep=",")
df = df.iloc[8:]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#server = app.server

liste_y = ['n_dose1', 'n_dose2', 'n_cum_dose1', 'n_cum_dose2']
liste_x = ['jour']
liste_dep = ['dep']

df_firstgraph = df[df['sexe'] == 0]
df_filtered = df[df['sexe'] != 0]
df_filtered['sexe_str'] = df_filtered['sexe'].apply(lambda x: "Homme" if x == 1 else "Femme")

df_new_filtered = df[df['sexe'] == 0].groupby('dep')

with open('apps/departements.geojson') as file:
    geo = geojson.load(file)

df_map = df[(df['jour'] == '2021-03-01') & (df['sexe'] == 0)]
df_map.drop(df_map.tail(1).index, inplace=True)

df_dep_reg = pd.read_csv('apps/departements-region.csv')

df_map['dep_name'] = df_dep_reg['dep_name'].to_numpy()
df_map['region_name'] = df_dep_reg['region_name'].to_numpy()

df_curr_situation_vac_hosp = df_map.groupby(['region_name'], as_index=False).max()

df_daily_vac = df.groupby(['jour'], as_index=False).sum()
figtest = px.choropleth(df_map, geojson=geo, locations='dep', featureidkey="properties.code",
                        labels={'dc': 'Total vaccination'}, color_continuous_scale="Viridis", scope="europe",
                        hover_name='dep_name', hover_data=['n_dose1', 'n_dose2'])
figtest.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations")
# figtest.update_layout(margin={"r":50,"t":50,"l":50,"b":50})
figtest.update_layout(width=1000, height=1000)

fig_region = px.pie(df_curr_situation_vac_hosp, values='n_cum_dose1', names='region_name', title="region")

fig_bot_right = px.pie(df_filtered, values="n_dose1", names="sexe_str", title="accination 1 by Gender")
fig_bot_right.update_traces(textposition='outside',
                            textinfo='percent+label',
                            marker=dict(line=dict(color='#000000',
                                                  width=2)),
                            pull=[0.05, 0, 0.03],
                            opacity=0.9,
                            # rotation=180
                            )
fig_bot_left = px.pie(df_filtered, values="n_dose1", names="sexe_str", title="vaccination 2 by Gender")
fig_bot_left.update_traces(textposition='outside',
                           textinfo='percent+label',
                           marker=dict(line=dict(color='#000000',
                                                 width=2)),
                           pull=[0.05, 0, 0.03],
                           opacity=0.9,
                           # rotation=180
                           )

fig_t = px.pie(df_filtered, values="n_cum_dose1", names="sexe_str", title="Deceased by Gender")
fig_t.update_traces(textposition='outside',
                    textinfo='percent+label',
                    marker=dict(line=dict(color='#000000',
                                          width=2)),
                    pull=[0.05, 0, 0.03],
                    opacity=0.9,
                    # rotation=180
                    )

fig_total_vac1 = px.scatter(df_map, x=df_daily_vac["jour"], y=df_daily_vac['n_cum_dose1'],
                            title="Evolution of the cumulated number of people vaccinated stage 1 in France")
fig_total_vac2 = px.scatter(df_map, x=df_daily_vac["jour"], y=df_daily_vac['n_cum_dose2'],
                            title="Evolution of the cumulated number of people vaccinated stage 2 in France")
fig_daily_vac1 = px.scatter(df_map, x=df_daily_vac["jour"], y=df_daily_vac['n_dose1'],
                            title="Evolution of the number of people vaccinated stage 1 in France each day")
fig_daily_vac2 = px.scatter(df_map, x=df_daily_vac["jour"], y=df_daily_vac['n_dose2'],
                            title="Evolution of the number of people vaccinated stage 2 in France each day")

layout = html.Div([
    html.H1('Covid Vaccination Data in France', style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.H4('First graph', style={"color": "white", "textAlign": "center"}),
            html.Br(),
            html.P('Here we can choose the parameter that we want to see across time',
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P('We can see the number of vaccination every day\n',
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.Div(dcc.Dropdown(
                id='yaxis-column23',
                options=[{'label': i, 'value': i} for i in liste_y],
                value='n_dose1'
            )),
        ], className="three columns", style={"padding": "3%"}),

        html.Div([
            dcc.Graph(id='first_graph23', figure={})
        ], className="nine columns")

    ], className='row', style={"backgroundColor": "#313131"}),

    html.Br(),
    html.Br(),

    html.Div([

        html.Div([
            dcc.Graph(
                id='graph123',
                figure=fig_total_vac1
            ),

            html.Br(),

            dcc.Graph(
                id='graph423',
                figure=fig_total_vac2),
        ], className='six columns'),

        html.Div([
            dcc.Graph(
                id='graph30000',
                figure=fig_daily_vac1
            ),

            html.Br(),

            dcc.Graph(
                id='graph20000',
                figure=fig_daily_vac2),
        ], className='six columns'),

        # dcc.Graph(id = 'third-graph', figure= fig_bot_right, className='three columns'),
        # dcc.Graph(id = 'fourth-graph', figure= fig_bot_right, className='three columns')
    ], className="row", style={"border": "solid", "padding": "2%"}),

    html.Div([

        html.Div([
            html.Div([
                html.H4('First graph', style={"color": "white", "textAlign": "center"}),
                html.Br(),
                html.P('Here we can choose the parameter that we want to see across time',
                       style={"textAlign": "justify", "color": "white"}),
                html.Br(),
                html.P('We can see the number of vaccination every day\n',
                       style={"textAlign": "justify", "color": "white"}),
                html.Br(),

            ], className="six columns", style={"padding": "3%"}),

            html.Div([
                dcc.Graph(id='pie_graph', figure=fig_bot_right)
            ], className="six columns")

        ], className='row', style={"backgroundColor": "#313131"}),

    ], style={"padding": "3%", "border": "solid"}),

    html.Div([

        html.Div([
            dcc.Graph(
                id='graph823',
                figure=figtest),
        ], className="seven columns", style={"height": "100%"}),

    ], className="row", style={"padding": "3%", "border": "solid"}),

    html.Div([
        html.Div([
            dcc.Graph(
                id='graph8623',
                figure=fig_region),
        ], className="seven columns", style={"height": "100%"}),
    ], className="row", style={"padding": "3%"})

], style={"padding": "3%"})


@app.callback(
    Output('first_graph23', 'figure'),
    [Input("yaxis-column23", "value")]
)
def update_figure(yaxis_column_name):
    return px.scatter(
        df_firstgraph, x=df_firstgraph['jour'], y=df_firstgraph[yaxis_column_name], color='dep',
        render_mode="webgl", title="Evolution of the COVID-19 vaccination in France"
    )


#if __name__ == '__main__':
 #   app.run_server(debug=False)