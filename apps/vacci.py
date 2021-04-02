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

### DISCLAIMER : A lot of code is similar that we used in the covid.py file for graphs. Only the dataset and de varialbes to display change.

#Concerning the vaccination dataset, the recent changes made on the available dataset are not working with what we defined here so we kept the original dataset that we had

df = pd.read_csv("apps/vacsi-s-dep-2021-03-02-20h15.csv", sep=",")
df = df.iloc[8:]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#server = app.server

df = df.rename(columns={'n_dose1': 'dose_1', 'n_dose2': 'dose_2', 'jour':'day', 'n_cum_dose1':'cumulated_dose_1', 'n_cum_dose2':'cumulated_dose_2', 'dep':'department'})

liste_y = ['dose_1', 'dose_2', 'cumulated_dose_1', 'cumulated_dose_2']
liste_x = ['day']
liste_dep = ['department']

df_firstgraph = df[df['sexe'] == 0]
df_filtered = df[df['sexe'] != 0]
df_filtered['sexe_str'] = df_filtered['sexe'].apply(lambda x: "Men" if x == 1 else "Women")

df_new_filtered = df[df['sexe'] == 0].groupby('department')

with open('apps/departements.geojson') as file:
    geo = geojson.load(file)

#This time for the map, we set the date to the last date in the dataset which is March, 1st since we took the dataset of March 2nd

df_map = df[(df['day'] == '2021-03-01') & (df['sexe'] == 0)]
df_map.drop(df_map.tail(1).index, inplace=True)

df_dep_reg = pd.read_csv('apps/departements-region.csv')

df_map['dep_name'] = df_dep_reg['dep_name'].to_numpy()
df_map['region_name'] = df_dep_reg['region_name'].to_numpy()

df_curr_situation_vac_hosp = df_map.groupby(['region_name'], as_index=False).max()

df_daily_vac = df.groupby(['day'], as_index=False).sum()
france_map = px.choropleth(df_map, geojson=geo, locations='department', featureidkey="properties.code", color='cumulated_dose_1',
                        labels={'dc': 'Total vaccination'}, color_continuous_scale="Viridis", scope="europe",
                        hover_name='dep_name', hover_data=['dose_1', 'dose_2'])
france_map.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations")
# france_map.update_layout(margin={"r":50,"t":50,"l":50,"b":50})
france_map.update_layout(width=1000, height=1000)

#This time we define the graph to represent the vaccination per gender for first dose

fig_vacci_gender = px.pie(df_filtered, values="dose_1", names="sexe_str", title="Vaccination 1 by Gender")
fig_vacci_gender.update_traces(textposition='outside',
                            textinfo='percent+label',
                            marker=dict(line=dict(color='#000000',
                                                  width=2)),
                            pull=[0.05, 0, 0.03],
                            opacity=0.9,
                            # rotation=180
                            )


#Graphs for total and daily administration of vaccine (by dose)

fig_total_vac1 = px.scatter(df_daily_vac, x="day", y='cumulated_dose_1',
                            title="Evolution of the cumulated number of people vaccinated stage 1 in France")
fig_total_vac2 = px.scatter(df_daily_vac, x="day", y='cumulated_dose_2',
                            title="Evolution of the cumulated number of people vaccinated stage 2 in France")
fig_daily_vac1 = px.scatter(df_daily_vac, x="day", y='dose_1',
                            title="Evolution of the number of people vaccinated stage 1 in France each day")
fig_daily_vac2 = px.scatter(df_daily_vac, x="day", y='dose_2',
                            title="Evolution of the number of people vaccinated stage 2 in France each day")

#For the definition of the layout, we kept the same structure as the one for the covid information. We just change the graphs that are displayed.

layout = html.Div([
    html.H1('Covid Vaccination Data in France', style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.H4('Global evolution in France', style={"color": "white", "textAlign": "center"}),
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
                value='cumulated_dose_1'
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

        # dcc.Graph(id = 'third-graph', figure= fig_vacci_gender, className='three columns'),
        # dcc.Graph(id = 'fourth-graph', figure= fig_vacci_gender, className='three columns')
    ], className="row", style={"border": "solid", "padding": "2%"}),

    html.Div([

        html.Div([
            html.Div([
                html.H2('Vaccination across Gender', style={"color": "white", "textAlign": "center"}),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),

                html.P('Let\'s have a look at the proportion of the first dose by gender',
                       style={"textAlign": "center", "color": "white"}),
                html.Br(),
                html.Br(),

            ], className="six columns", style={"padding": "3%"}),

            html.Div([
                dcc.Graph(id='pie_graph', figure=fig_vacci_gender)
            ], className="six columns")

        ], className='row', style={"backgroundColor": "#313131"}),

    ], style={"padding": "3%", "border": "solid"}),

    html.Div([

        html.Div([
            dcc.Graph(
                id='graph823',
                figure=france_map),
        ], className="seven columns", style={"height": "100%"}),

        html.Div([
            html.H4('Informations for each department', style={"color": "white", "textAlign": "center"}),
            html.Br(),

            html.P('You can have a look on the situation of every department with the map',
                   style={"textAlign": "center", "color": "white"}),
            html.Br(),
            html.Br(),

        ], className="five columns", style={"backgroundColor": "#313131", "padding": "3%"}),

    ], className="row", style={"padding": "3%", "border": "solid"}),


], style={"padding": "3%"})


@app.callback(
    Output('first_graph23', 'figure'),
    [Input("yaxis-column23", "value")]
)
def update_figure(yaxis_column_name):
    return px.scatter(
        df_firstgraph, x=df_firstgraph['day'], y=df_firstgraph[yaxis_column_name], color='department',
        render_mode="webgl", title="Evolution of the COVID-19 vaccination in France"
    )


#if __name__ == '__main__':
 #   app.run_server(debug=False)