import dash as dash
import geojson as geojson
from dash import Dash
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from app import app
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests

#First, we get the current date to have graphs with the last informations

current_date = datetime.today() - timedelta(1)
current_date = current_date.strftime('%Y-%m-%d')

#Code to get last updated dataset from the French government
#To do this, we use BeautifulSoup to parse the website and find all links associated to the word "Télécharger".
# We saw that the order is always the same and so we just get the second link parsed that corresponds to the dataset that we want to use

page = requests.get("https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/")
soup = BeautifulSoup(page.text, 'html.parser')
links = soup.find_all('a', href = True, text = 'Télécharger')
dataset_link = links[1]['href']

print("Link dataset", dataset_link) #We display the link to be sure to get the good dataset. Then we just proceed normally with a .csv file


df = pd.read_csv(dataset_link, sep=";")


#This external_stylesheets is thez one that allow us to use something similar to Bootstrap for the disposition on the Dashboard
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


#These three lists will be used for the first graph displaying the global situation in France
#We will have the choice to choose between the number of Hospitalisations, Reanimations, Home returns eand Deceased displayed in function of the day. Basically, it's just to show
#the evolution of the pandemic in France since the beginning
liste_y = ['hosp', 'rea', 'rad', 'dc']
liste_x = ['jour']
liste_dep = ['dep']

#In the dataset, we add three values for the 'sexe' parameter : 0 for all,  1 for men and 2 for women. For cumulated values, we take only rows with the value 0 for 'sexe'

df_firstgraph = df[df['sexe'] == 0]
df_cumul_hosp = df_firstgraph

#Now, we create two new columns, one for the cumulated number of hospitalisations and one for the cumulated number of reanimations.

df_cumul_hosp['cumul_hosp'] = df_cumul_hosp.groupby(['jour'], as_index=False)['hosp'].cumsum()
df_cumul_hosp = df_cumul_hosp.groupby(['jour'], as_index=False).max()
df_cumul_hosp['cumul_rea'] = df_cumul_hosp.groupby(['jour'], as_index=False)['rea'].cumsum()
df_cumul_hosp = df_cumul_hosp.groupby(['jour'], as_index=False).max()

df_filtered = df[df['sexe'] != 0]
df_filtered['sexe_str'] = df_filtered['sexe'].apply(lambda x: "Homme" if x == 1 else "Femme")

df_new_filtered = df[df['sexe'] == 0].groupby('dep')

fig = px.pie(df_filtered, values="rea", names="sexe")


#This part concerns the last part of the dashboard, everything around the France map that we use.

with open('apps/departements.geojson') as file:
    geo = geojson.load(file)

#To get the current situation, we just get all the rows for the current date that we defined at the beginning.

df_map = df[(df['jour'] == current_date) & (df['sexe'] == 0)]
df_dep_reg = pd.read_csv('apps/departements-region.csv')

#We add the department and regions names.

df_map['dep_name'] = df_dep_reg['dep_name'].to_numpy()
df_map['region_name'] = df_dep_reg['region_name'].to_numpy()
df_curr_situation = df_map

#We create two new columns to group numbers by regions

df_curr_situation['total_hosp_per_region'] = df_curr_situation.groupby(['region_name'], as_index=False)['hosp'].cumsum()
df_curr_situation['total_rea_per_region'] = df_curr_situation.groupby(['region_name'], as_index=False)['rea'].cumsum()

df_curr_situation_fig_hosp = df_curr_situation.groupby(['region_name'], as_index=False).max()


#The first graph will be defined thanks to the app callback at the end of the code. Right now, we will defined all the graphs that will be coming after the first one.
#The order of definition here is the same order that we have in the final dashboard.

#Those graphs will show the cumulated number of Hospitalisations and reanimations. We used the dataset that we create that contains these two columns to do that.

total_hosp = px.scatter(df_cumul_hosp, x='jour', y='cumul_hosp',
                            title="Evolution of the number of people hospitalized in France")
total_rea = px.scatter(df_cumul_hosp, x='jour', y='cumul_rea',
                           title="Evolution of the number of people in reanimation in France")


#The next three graphs wil be all informations based on the gender: Hospitalisations, Reanimations and Deceased

gender_hosp = px.pie(df_filtered, values="hosp", names="sexe_str", title="Hospitalisations by Gender")
gender_hosp.update_traces(textposition='outside',
                            textinfo='percent+label',
                            marker=dict(line=dict(color='#000000',
                                                  width=2)),
                            pull=[0.05, 0, 0.03],
                            opacity=0.9,
                            # rotation=180
                            )

gender_rea = px.pie(df_filtered, values="rea", names="sexe_str", title="Reanimation by Gender")
gender_rea.update_traces(textposition='outside',
                           textinfo='percent+label',
                           marker=dict(line=dict(color='#000000',
                                                 width=2)),
                           pull=[0.05, 0, 0.03],
                           opacity=0.9,
                           # rotation=180
                           )

gender_dec = px.pie(df_filtered, values="dc", names="sexe_str", title="Deceased by Gender")
gender_dec.update_traces(textposition='outside',
                    textinfo='percent+label',
                    marker=dict(line=dict(color='#000000',
                                          width=2)),
                    pull=[0.05, 0, 0.03],
                    opacity=0.9,
                    # rotation=180
                    )

#We create a map of France to get a better representaion of the current situation. The color will be the total number of deaths per department.
#When using the map, each department will have the current number of people in hospitalisation and reanimation

france_map = px.choropleth(df_map, geojson=geo, locations='dep', featureidkey="properties.code", color='dc',
                        labels={'dc': 'Total décès'}, color_continuous_scale="Viridis", scope="europe",
                        hover_name='dep_name', hover_data=['hosp', 'rea'])
france_map.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations")
# france_map.update_layout(margin={"r":50,"t":50,"l":50,"b":50})
france_map.update_layout(width=1000, height=1000)

#Two graphs to see percentages of hospitalisation and reanimation in France for each region

fig_region = px.pie(df_curr_situation_fig_hosp, values='total_hosp_per_region', names='region_name',
                    title="Hospitalisation by region")
fig_region_rea = px.pie(df_curr_situation_fig_hosp, values='total_rea_per_region', names='region_name',
                        title="Reanimation by region")

#Now that our graphs are defined, we can define the layout for the Dashboard

#First, let's explain how the .css file that we used is working.
#Like Bootstrap, this extension considers the screen as 12 columns of same length. We can structure the elements like we want by specifying the number of columns that we want for our element.
#For example, we can decide to get the text on four columns and the graph on eight to have more space for the graph.
# We can also divide the screen in three, four columns for each element, to display three graphs on the same 'row'.

layout = html.Div([
    html.H1('Covid Data in France', style={"textAlign": "center"}),

    #Here, we will have the first graph showing the evolution of the pandemic in France (you can choose to see number of hospitalisations, reanimations, home returns or deceased

    html.Div([
        html.Div([
            html.H4('Global evolution in France', style={"color": "white", "textAlign": "center"}),
            html.Br(),
            html.P('Here we can choose the parameter that we want to see across time',
                   style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.P(
                'We can see the number of hospitalisations every day, number of reanimation and deaths (cumulated)\n',
                style={"textAlign": "justify", "color": "white"}),
            html.Br(),
            html.Div(dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in liste_y],
                value='hosp'
            )),
        ], className="three columns", style={"padding": "3%"}), #We use a syntax similar to Bootstrap to structure the page. We can do this thanks to the external stylesheet that we dl before

        html.Div([
            dcc.Graph(id='first_graph', figure={})
        ], className="nine columns")

    ], className='row', style={"backgroundColor": "#313131"}),

    html.Br(),
    html.Br(),

    html.Div([

        #We define here a column that will have the two graphs concerning the evolution of hospitalisations and reanimations

        html.Div([
            dcc.Graph(
                id='graph1',
                figure=total_hosp
            ),

            html.Br(),

            dcc.Graph(
                id='graph4',
                figure=total_rea),
        ], className='six columns'),

        html.Div([
            html.Br()
        ], className="one columns"),

        #We define a zone of text to describe the graphs

        html.Div([
            html.H4('Hospitalisations and Reanimations', style={"color": "white", "textAlign": "center"}),
            html.Br(),
            html.P(
                "Now let's have a look at the total number of people who were hospitalized and who were in reanimation",
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

        ], className="six columns", style={"backgroundColor": "#313131", "padding": "3%"}),

        # dcc.Graph(id = 'third-graph', figure= gender_hosp, className='three columns'),
        # dcc.Graph(id = 'fourth-graph', figure= gender_hosp, className='three columns')
    ], className="row", style={"border": "solid", "padding": "2%"}),


    #New block to display the graphs concerning the gender informations

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

        #We put the three graphs on the same row

        html.Div([
            html.Div([
                dcc.Graph(
                    id='graph2',
                    figure=gender_hosp
                ),
            ], className='four columns'),

            html.Div([
                dcc.Graph(
                    id='graph3',
                    figure=gender_rea
                ),
            ], className='four columns'),

            html.Div([
                dcc.Graph(
                    id='graph15',
                    figure=gender_dec
                ),
            ], className='four columns'),

        ], className="row"),

    ], style={"padding": "3%", "border": "solid"}),


    #Finally, we display the map of France with the graphs per region at the right side.

    html.Div([
        html.H2('Current COVID-19 situation in France', style={"color": "white", "textAlign": "center"}),
    ], className="row", style={"backgroundColor": "#313131", "padding": "3%"}),

    html.Div([

        html.Div([
            dcc.Graph(
                id='graph8',
                figure=france_map),
        ], className="seven columns", style={"height": "100%"}),

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

        ], className="five columns", style={"backgroundColor": "#313131", "padding": "3%"}),

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

#We run the app in the main.py file
# if __name__ == '__main__':
#   app.run_server(debug=False)
