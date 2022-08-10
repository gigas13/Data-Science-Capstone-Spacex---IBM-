# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import math

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

def round_up_to_nearest_1000(num):
    return math.ceil(num / 1000) * 1000

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(options=[{'label':'All Sites','value':'ALL'},
                                                      {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                                      {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},
                                                      {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                                      {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'}],
                                             id='site_dropdown',
                                             value='ALL',
                                             searchable=True,
                                             placeholder="Select a LaunchSite"),
                                html.Br(),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload_slider',min=min_payload, max=max_payload, step=None, value=[round_up_to_nearest_1000(min_payload),
                                                                                                                        round_up_to_nearest_1000(max_payload)]),
                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site_dropdown', component_property='value'))

def generate_chart(site_dropdown):
    if site_dropdown == 'ALL':
        fig = px.pie(data_frame = spacex_df, names='Launch Site', values='class' ,title='Total Launches for All Sites')
        return fig
    else:
        specific_df = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        fig = px.pie(data_frame = specific_df, names='class',title='Success Rate')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site_dropdown', component_property='value'),
    Input(component_id='payload_slider', component_property='value')])

def update_graph(site_dropdown, payload_slider):
    if site_dropdown != 'ALL':
        filtered_df=spacex_df.loc[spacex_df['Launch Site'] == site_dropdown,:]
    filtered_df = spacex_df.query("`Payload Mass (kg)` >= @payload_slider[0] and `Payload Mass (kg)` <= @payload_slider[1]")
    fig = px.scatter(data_frame=filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
