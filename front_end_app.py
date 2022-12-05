#Import packages

from datetime import datetime
import blosc
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import pandas as pd
import pickle

#Import network raw data

with open(f"static/elements_m1.dat", "rb") as f:
    compressed_pickle = f.read()

    depressed_pickle = blosc.decompress(compressed_pickle)
    # turn bytes object back into data
    elements = pickle.loads(depressed_pickle)

df_export = pd.read_csv('static/export_graph_1309.csv', index_col=False, sep=',', engine='python')

#Setting Dash app

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'SEN-CodeX'

server = app.server
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

#Creation of Navbar

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(html.Img(src="static/network-svgrepo-com.svg", height="35px")),
        dbc.NavItem(
            dbc.Button(
                "Filters",
                color="primary",
                id='open-offcanvas-recherche',
                n_clicks=0
            ),
            style={"margin-left":"70px"}
        ),
        dbc.NavItem(
            dbc.NavLink(
                "Article",
                href="https://law.stanford.edu/codex-the-stanford-center-for-legal-informatics/computational-antitrust-publications/",
                target="_blank"
            ),
            style={"margin-left":"35px"}
        ),
        dbc.NavItem(
            dbc.NavLink(
                "Source Code",
                href="https://github.com/AutoriteDeLaConcurrence/publication_sen-codex_networkgraph",
                target="_blank"
            ),
            style={"margin-left":"35px"}
        ),
    ],
    brand="Digital Economy Unit   &   CodeX   :   Stable version 1",
    brand_href="/",
    color="PowderBlue",
    dark=False,
    style={"width": "100vw"}
)

#Filters

#Filter 1 : Slider per year

range_slider = dbc.Row(
    [
        dbc.Label("Choose a period of time below and it will show the subsequent graph consisting of all the publications of the FCA between this time period and the quotations to others FCA’s publications found in this subset."),
        dbc.Col(
        dcc.RangeSlider(id="my-range-slider", min=9,
                        max=21, step=None, value=[9, 21],
                        marks={
                            9: '2009',
                            10: '2010',
                            11: '2011',
                            12: '2012',
                            13: '2013',
                            14: '2014',
                            15: '2015',
                            16: '2016',
                            17: '2017',
                            18: '2018',
                            19: '2019',
                            20: '2020',
                            21: '2021',
                        }),
                        width=10
        ),
    ],
    className="mb-3",
)

#Filter 2 : sector dropdown

sector_dropdown = dbc.Row(
    [
        dbc.Label("Hightlight per sector(s)"),
        dbc.Col(
        dcc.Dropdown(
            id="sectors_dropdown",
            options=[
                {'label': 'Agriculture / Agri-food', 'value': 'Agriculture'},
                {'label': 'Art and culture', 'value': 'Art'},
                {'label': 'Bank / Insurance', 'value': 'Banque'},
                {'label': 'Construction', 'value': 'BTP'},
                {'label': 'Distribution', 'value': 'Distribution'},
                {'label': 'Energy / Environment', 'value': 'Energie'},
                {'label': 'Consumption', 'value': 'consommation'},
                {'label': 'Industry', 'value': 'Industrie'},
                {'label': 'Digital', 'value': 'Numérique'},
                {'label': 'Overseas', 'value': 'Outre'},
                {'label': 'Press / Media', 'value': 'Presse'},
                {'label': 'Regulated professions', 'value': 'Professions'},
                {'label': 'Health', 'value': 'Santé'},
                {'label': 'Services', 'value': 'Services'},
                {'label': 'Sport', 'value': 'Sport'},
                {'label': 'Telecoms', 'value': 'Télécoms'},
                {'label': 'Tourism / Hotel / Catering', 'value': 'Tourisme'},
                {'label': 'Transport', 'value': 'Transports'},
                {'label': "Life of the institution", 'value': 'institution'},
            ],
            persistence=True
            # multi=True,
        ),
        width=10,
        ),
    ],
    className="mb-3",
)

#Filter 3 : node input

node_dropdown = dbc.Row(
    [
        dbc.Label("Highlight publication(s) by its number (i.e. 09-D-06, 20-A-08, etc…) Only decisions, opinions and interim measures are available."),
        dbc.Col(
        dcc.Dropdown(df_export['Publication A'].unique(), id="dropdown_node"),
        width=10
        ),
    ],
    className="mb-3",
)

#Filter 4 : offcanvas research dropdown

offcanvas_research= html.Div(
    [
        dbc.Offcanvas(
            dbc.Form([node_dropdown, sector_dropdown, range_slider]),
            id='offcanvas-recherche',
            title='Explore the complex network',
            is_open=False,
            keyboard=True,
            style={'width': '60vh', 'margin-top':'55px', 'background-color':'white'}
        )
    ]
)

#Default stylesheet of the network graph

default_stylesheet = [
    {
        "selector": 'node', 
        'style': {
            "opacity": 0.9,
            "label": "data(label)",
            "width": "data(node_size)",
            "height": "data(node_size)",
            "background-color": "#07ABA0",
            "color": "#008B80" 
        }
    },
    {
        "selector": 'edge',
        "style": {
            "target-arrow-color": "#C5D3E2",
            "target-arrow-shape": "triangle",
            "line-color": "#C5D3E2",
            "background-color": "#07ABA0",
            'arrow-scale': 2,
            'curve-style': 'bezier'
        },
    },
]

# Setting the main app layout : describes what the app looks like and is a hierarchical tree of components

app.layout = html.Div([
    navbar,
    offcanvas_research,
    cyto.Cytoscape(
        id='cytoscape-layout',
        elements=elements,
        style={'width': '100vw', 'height': '74.5vh'},
        layout={
            'name': 'preset',
            'animate': True,
            'animationDuration': 2000,
        },
        stylesheet=default_stylesheet,
        minZoom=0.10,
        maxZoom=1
    ),
    dbc.Row(
        [
            dbc.Alert(
                id="elements-data",
                children="Click on a node or edge to see its details here",
                color="secondary",
                style={"width": "100vw",'height': '19.5vh', "margin-bottom": "0px", "margin-left": "10px"}
            )
        ]
    ),
], style={"height": "96vh", "width": "99.3vw"})


# Callback decorators : allow to update / create user interaction


# Callback 1 : Open main offcanvas when clicking "Filters" button

@app.callback(
    Output("offcanvas-recherche", "is_open"),
    Input("open-offcanvas-recherche", "n_clicks"),
    [State("offcanvas-recherche", "is_open")]
)
def toogle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

# Callback 2 : Main interaction when clicking on a node or edge

@app.callback(
    Output("elements-data",
           "children"),
    [Input("cytoscape-layout", "selectedNodeData"),
     Input('cytoscape-layout', 'selectedEdgeData')],
)
def display_nodedata(node_attr, edge_attr):
    contents = "Click on a node or an edge to see its details here"
    if node_attr:
        contents = []
        data = node_attr[-1]
        if len(data) > 3:
            contents.append(html.A(f'{data["id"] + " : " + data["type_doc"].title() + " " + data["titre"]}', href=f'https://www.autoritedelaconcurrence.fr/fr/liste-des-decisions-et-avis?search_api_fulltext={data["id"]}&sort_by=search_api_relevance&created%5Bmin%5D=&created%5Bmax%5D=', target="_blank"))
            contents.append(html.Br())
            contents.append(html.Br())
            contents.append(
                html.P(
                    "Secteur: "
                    + data["secteur"].title()
                ),
            )
            contents.append(
                html.P(
                    "Date: "
                    + datetime.strptime(data["datetime"],
                                        "%Y-%m-%dT%H:%M:%SZ").strftime('%d/%m/%Y')
                )
            )
            contents.append(
                html.P(
                    [
                    dbc.Button("Download data", id="btn_xlsx", color="primary", size="sm"),
                    dcc.Download(id="download-dataframe-xlsx")
                    ]
                )
            )
        else:
            contents.append(html.H5("Not available"))
            contents.append(html.Br())
            contents.append(html.Br())
            contents.append(html.Br())
            contents.append(html.Br())
            contents.append(html.Br())

    elif edge_attr:
        contents = []
        data = edge_attr[-1]
        contents.append(html.H5("Connexion :"))
        contents.append(
            html.P("Source : " + data['source']))
        contents.append(
            html.P("Target : " + data['target']))
        contents.append(
            html.P("Number of citations : " + str(data['cited_occurences'])))

    else:
        contents = "Click on a node or an edge to see its details here"

    return contents

# Callback 3 : Update the network graph when range slider (years) changes

@ app.callback(
    Output('cytoscape-layout', 'elements'),
    [Input('my-range-slider', 'value')],
    [State('cytoscape-layout', 'elements')])
def update_output(value, existing_state):
    new_elements = []
    if value[0] == 9 and value[1] == 21:
        return existing_state
    elif value[0] == 21 and value[1] == 21:
        with open(f"static/elements_m1_21.dat", "rb") as f:
            compressed_pickle = f.read()

            depressed_pickle = blosc.decompress(compressed_pickle)
            # turn bytes object back into data
            elements = pickle.loads(depressed_pickle)
            new_elements.extend(elements)
        return new_elements
    elif value[0] == 9 and value[1] == 9:
        with open(f"static/elements_m1_9.dat", "rb") as f:
            compressed_pickle = f.read()
            depressed_pickle = blosc.decompress(compressed_pickle)
            # turn bytes object back into data
            elements = pickle.loads(depressed_pickle)
            new_elements.extend(elements)
        return new_elements
    else:
        for i in range(value[0], value[1]+1):
            with open(f"static/elements_m1_{i}.dat", "rb") as f:
                compressed_pickle = f.read()

                depressed_pickle = blosc.decompress(compressed_pickle)
                # turn bytes object back into data
                elements = pickle.loads(depressed_pickle)
                new_elements.extend(elements)
            new_elements = [i for n, i in enumerate(
                new_elements) if i not in new_elements[n + 1:]]
        return new_elements

# Callback 4 : Update network graph when filters are activated

@app.callback(Output('cytoscape-layout', 'stylesheet'),
              [Input('cytoscape-layout', 'tapNode'), Input(component_id='sectors_dropdown', component_property='value'),
              Input(component_id='dropdown_node', component_property='value')])
def generate_stylesheet(node, sector, input):
    if not node and not sector and not input:
        return default_stylesheet
    elif node and not sector:
        stylesheet = [
            {
                "selector": 'node',
                'style': {
                    "opacity": 0.9,
                    "label": "data(label)", 
                    "width": "data(node_size)",
                    "height": "data(node_size)",
                    "background-color": "#07ABA0",
                    "color": "#008B80"  
                }
            },
            {
                "selector": 'edge', 
                "style": {
                    "target-arrow-color": "#C5D3E2", 
                    "target-arrow-shape": "triangle", 
                    "line-color": "#C5D3E2", 
                    "background-color": "#07ABA0", 
                    'arrow-scale': 2, 
                    'curve-style': 'bezier' 
                },
            },
            {
                "selector": 'node[id = "{}"]'.format(node['data']['id']),
                "style": {
                    'background-color': '#920000',
                    "border-color": "#920000",
                    "border-width": 2,
                    "border-opacity": 1,
                    "opacity": 1,
                    "label": "data(label)",
                    "color": "#920000", 
                    "text-opacity": 1,
                    "font-size": 12,
                }
            }]

        for edge in node['edgesData']:
            if edge['source'] == node['data']['id']:
                stylesheet.append({
                    "selector": 'node[id = "{}"]'.format(edge['target']),
                    "style": {
                        'background-color': '#ffdf4d',
                        'opacity': 0.9
                    }
                })
                stylesheet.append({
                    "selector": 'edge[id= "{}"]'.format(edge['id']),
                    "style": {
                        "mid-target-arrow-color": '#ffdf4d',
                        "mid-target-arrow-shape": "vee",
                        "line-color": '#ffdf4d',
                        'opacity': 0.9,
                    }
                })

            if edge['target'] == node['data']['id']:
                stylesheet.append({
                    "selector": 'node[id = "{}"]'.format(edge['source']),
                    "style": {
                        'background-color': '#b66dff ',
                        'opacity': 0.9,
                    }
                })
                stylesheet.append({
                    "selector": 'edge[id= "{}"]'.format(edge['id']),
                    "style": {
                        "mid-target-arrow-color": '#b66dff ',
                        "mid-target-arrow-shape": "vee",
                        "line-color": '#b66dff ',
                        'opacity': 1,
                    }
                })

        return stylesheet

    elif node and sector:
        stylesheet = [
            {
                "selector": 'node',
                'style': {
                    "opacity": 0.9,
                    "label": "data(label)",
                    "width": "data(node_size)",
                    "height": "data(node_size)",
                    "background-color": "#07ABA0",
                    "color": "#008B80"
                }
            },
            {
                "selector": 'edge',
                "style": {
                    "target-arrow-color": "#C5D3E2",
                    "target-arrow-shape": "triangle",
                    "line-color": "#C5D3E2",
                    "background-color": "#07ABA0",
                    'arrow-scale': 2,
                    'curve-style': 'bezier'
                },
            },
            {
                "selector": 'node[id = "{}"]'.format(node['data']['id']),
                "style": {
                    'background-color': '#920000',
                    "border-color": "#920000",
                    "border-width": 2,
                    "border-opacity": 1,
                    "opacity": 1,
                    "label": "data(label)",
                    "color": "#920000",
                    "text-opacity": 1,
                    "font-size": 12,
                }
            },
                        {
                'selector': f'[secteur ^= "{sector}"]',
                'style': {
                    'background-color': '#920000',
                }
            }
            ]

        for edge in node['edgesData']:
            if edge['source'] == node['data']['id']:
                stylesheet.append({
                    "selector": 'node[id = "{}"]'.format(edge['target']),
                    "style": {
                        'background-color': '#ffdf4d',
                        'opacity': 0.9
                    }
                })
                stylesheet.append({
                    "selector": 'edge[id= "{}"]'.format(edge['id']),
                    "style": {
                        "mid-target-arrow-color": '#ffdf4d',
                        "mid-target-arrow-shape": "vee",
                        "line-color": '#ffdf4d',
                        'opacity': 0.9,
                    }
                })

            if edge['target'] == node['data']['id']:
                stylesheet.append({
                    "selector": 'node[id = "{}"]'.format(edge['source']),
                    "style": {
                        'background-color': '#b66dff ',
                        'opacity': 0.9,
                    }
                })
                stylesheet.append({
                    "selector": 'edge[id= "{}"]'.format(edge['id']),
                    "style": {
                        "mid-target-arrow-color": '#b66dff ',
                        "mid-target-arrow-shape": "vee",
                        "line-color": '#b66dff ',
                        'opacity': 1,
                    }
                })

        return stylesheet

    elif sector:
        stylesheet = [
            {
                "selector": 'node',
                'style': {
                    "opacity": 0.9,
                    "label": "data(label)",
                    "width": "data(node_size)",
                    "height": "data(node_size)",
                    "background-color": "#07ABA0",
                    "color": "#008B80"
                }
            },
            {
                "selector": 'edge',
                "style": {
                    "target-arrow-color": "#C5D3E2",
                    "target-arrow-shape": "triangle",
                    "line-color": "#C5D3E2",
                    "background-color": "#07ABA0",
                    'arrow-scale': 2,
                    'curve-style': 'bezier'
                },
            },
            {
                'selector': f'[secteur ^= "{sector}"]',
                'style': {
                    'background-color': '#920000',
                }
            }
        ]
        return stylesheet

    elif input:
        stylesheet = [
            {
                "selector": 'node',
                'style': {
                    "opacity": 0.9,
                    "label": "data(label)",
                    "width": "data(node_size)",
                    "height": "data(node_size)",
                    "background-color": "#07ABA0",
                    "color": "#008B80"
                }
            },
            {
                "selector": 'edge',
                "style": {
                    "target-arrow-color": "#C5D3E2",
                    "target-arrow-shape": "triangle",
                    "line-color": "#C5D3E2",
                    "background-color": "#07ABA0",
                    'arrow-scale': 2,
                    'curve-style': 'bezier'
                },
            },
            {
                "selector": f'[id ^= "{input}"]',
                "style": {
                    'background-color': '#920000',
                    "border-color": "#920000",
                    
                    "border-width": 2,
                    "border-opacity": 1,
                    "opacity": 1,
                    "width": "200px",
                    "height": "200px",
                    "label": "data(label)",
                    "color": "#920000",
                    "text-opacity": 1,
                    "font-size": 12,
                }
            },
        ]
        return stylesheet
    

# Callback 5 : Download data (xlsx format) when clicking on "Download data"

@app.callback(
    Output("download-dataframe-xlsx", "data"),
    Input("btn_xlsx", "n_clicks"),
    State("cytoscape-layout", "selectedNodeData"),
    prevent_initial_call=True,
)
def func(n_clicks, elements):
    for element in elements:
        data = df_export[(df_export['Publication A'] == element['id']) | (df_export['Publication B'] == element['id'])].reset_index()
        return dcc.send_data_frame(data.to_excel, f"export_details_{element['id']}.xlsx", sheet_name="data")

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=False )