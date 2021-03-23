import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import test, vacci

#Here we will launch the app and define the layout. We have something to add, which is the links for the COVID 19 informations or the vaccination informations


app.layout = html.Div([
    html.H1('Evolution of the COVID-19 situation in France', style={"textAlign": "center"}),
    dcc.Location(id='url', refresh=False),

    html.Div([
        html.Br(),
    ], className="three columns"),

    #Here we defined links to click on to siplay COVID-19 informations or vaccination informations. We can switch from one to another at any moment

    html.Div([
        dcc.Link('Covid-19 in France',className="three columns", href='/apps/test', #We defined the links to display the COVID-19 layout here
                 style={"font":"bold 30px Arial", "text_decoration":"none", "padding":"2px 6px 2px 6px", "color":"#333333", "background-color":"EEEEEE", "textAlign":"center"}),
        dcc.Link('Vaccination in France',className="three columns", href='/apps/vacci',
                 style={"font": "bold 30px Arial", "text_decoration": "none", "padding": "2px 6px 2px 6px",
                        "color": "#333333", "background-color": "EEEEEE"}
                 ),
    ], className="row"),
    html.Div(id='page-content', children=[])
])

#We retrun the layouts based on what is asked by the user
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/test':
        return test.layout
    if pathname == '/apps/vacci':
        return vacci.layout
    else:
        return ""


if __name__ == '__main__':
    app.run_server(debug=False)
