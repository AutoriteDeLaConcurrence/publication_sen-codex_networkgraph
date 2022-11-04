#Import packages

from datetime import datetime
import blosc
import dash
from dash import dcc, html, Input, Output, State
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

df_export = pd.read_csv('static/export_graph_1309.csv', index_col=None, sep=';', engine='python')

#Setting Dash app

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'SEN-CodeX'

server = app.server

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
                href="https://github.com/AutoriteDeLaConcurrence",
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
        dbc.Label("Filter per year"),
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
        dbc.Label("Filter per sector(s)"),
        dbc.Col(
        dcc.Dropdown(
            id="sectors_dropdown",
            options=[
                {'label': 'Agriculture / Agro-alimentaire', 'value': 'Agriculture'},
                {'label': 'Art et culture', 'value': 'Art'},
                {'label': 'Banque / Assurance', 'value': 'Banque'},
                {'label': 'BTP', 'value': 'BTP'},
                {'label': 'Distribution', 'value': 'Distribution'},
                {'label': 'Energie / Environnement', 'value': 'Energie'},
                {'label': 'Grande consommation', 'value': 'consommation'},
                {'label': 'Industrie', 'value': 'Industrie'},
                {'label': 'Numérique', 'value': 'Numérique'},
                {'label': 'Outre-mer', 'value': 'Outre'},
                {'label': 'Presse / Médias', 'value': 'Presse'},
                {'label': 'Proféssions réglementées', 'value': 'Professions'},
                {'label': 'Santé', 'value': 'Santé'},
                {'label': 'Services', 'value': 'Services'},
                {'label': 'Sport', 'value': 'Sport'},
                {'label': 'Télécoms', 'value': 'Télécoms'},
                {'label': 'Tourisme / Hôtellerie / Restauration', 'value': 'Tourisme'},
                {'label': 'Transports', 'value': 'Transports'},
                {'label': "Vie de l'institution", 'value': 'institution'},
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

node_input = dbc.Row(
    [
        dbc.Label("Highlight publication(s)"),
        dbc.Col(
        dcc.Input(id="input_node", type="text"),
        width=10
        ),
    ],
    className="mb-3",
)

#Filter 4 : offcanvas research dropdown

offcanvas_research= html.Div(
    [
        dbc.Offcanvas(
            dbc.Form([node_input, sector_dropdown, range_slider]),
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
              Input(component_id='input_node', component_property='value')])
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
                    'background-color': 'red',
                    "border-color": "red",
                    "border-width": 2,
                    "border-opacity": 1,
                    "opacity": 1,

                    "label": "data(label)",
                    "color": "red", 
                    "text-opacity": 1,
                    "font-size": 12,
                    'z-index': 9999
                }
            }]

        for edge in node['edgesData']:
            if edge['source'] == node['data']['id']:
                stylesheet.append({
                    "selector": 'node[id = "{}"]'.format(edge['target']),
                    "style": {
                        'background-color': '#FFC857',
                        'opacity': 0.9
                    }
                })
                stylesheet.append({
                    "selector": 'edge[id= "{}"]'.format(edge['id']),
                    "style": {
                        "mid-target-arrow-color": '#FFC857',
                        "mid-target-arrow-shape": "vee",
                        "line-color": '#FFC857',
                        'opacity': 0.9,
                        'z-index': 5000
                    }
                })

            if edge['target'] == node['data']['id']:
                stylesheet.append({
                    "selector": 'node[id = "{}"]'.format(edge['source']),
                    "style": {
                        'background-color': '#A997DF',
                        'opacity': 0.9,
                        'z-index': 9999
                    }
                })
                stylesheet.append({
                    "selector": 'edge[id= "{}"]'.format(edge['id']),
                    "style": {
                        "mid-target-arrow-color": '#A997DF',
                        "mid-target-arrow-shape": "vee",
                        "line-color": '#A997DF',
                        'opacity': 1,
                        'z-index': 5000
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
                    'background-color': 'red',
                    "border-color": "red",
                    "border-width": 2,
                    "border-opacity": 1,
                    "opacity": 1,

                    "label": "data(label)",
                    "color": "red",
                    "text-opacity": 1,
                    "font-size": 12,
                    'z-index': 9999
                }
            },
                        {
                'selector': f'[secteur ^= "{sector}"]',
                'style': {
                    'background-color': 'red',
                }
            }
            ]

        for edge in node['edgesData']:
            if edge['source'] == node['data']['id']:
                stylesheet.append({
                    "selector": 'node[id = "{}"]'.format(edge['target']),
                    "style": {
                        'background-color': '#FFC857',
                        'opacity': 0.9
                    }
                })
                stylesheet.append({
                    "selector": 'edge[id= "{}"]'.format(edge['id']),
                    "style": {
                        "mid-target-arrow-color": '#FFC857',
                        "mid-target-arrow-shape": "vee",
                        "line-color": '#FFC857',
                        'opacity': 0.9,
                        'z-index': 5000
                    }
                })

            if edge['target'] == node['data']['id']:
                stylesheet.append({
                    "selector": 'node[id = "{}"]'.format(edge['source']),
                    "style": {
                        'background-color': '#A997DF',
                        'opacity': 0.9,
                        'z-index': 9999
                    }
                })
                stylesheet.append({
                    "selector": 'edge[id= "{}"]'.format(edge['id']),
                    "style": {
                        "mid-target-arrow-color": '#A997DF',
                        "mid-target-arrow-shape": "vee",
                        "line-color": '#A997DF',
                        'opacity': 1,
                        'z-index': 5000
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
                    'background-color': 'red',
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
                    'background-color': 'red',
                    "border-color": "red",
                    "border-width": 2,
                    "border-opacity": 1,
                    "opacity": 1,
                    "label": "data(label)",
                    "color": "red",
                    "text-opacity": 1,
                    "font-size": 12,
                    'z-index': 9999
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
    app.run_server(debug=True)
