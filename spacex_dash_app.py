# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

slider_min = 0
slider_max = 10000
slider_middle = int(0.5*slider_max)

# Create a dash application
app = dash.Dash(__name__)


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                  dcc.Dropdown(id='site-dropdown',
                                                options=[
                                               {'label': 'All Sites', 'value': 'ALL'},
                                               {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                               {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                               {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                               {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                               ],
                                               value='ALL',
                                               placeholder="place holder here",
                                               searchable=True
                                               ),
                                  html.Br(),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # Function decorator to specify function input and output
                                 
                                    # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                  html.Div(dcc.Graph(id='success-pie-chart')),
                                  html.Br(),

                                  html.P("Payload range (Kg):"),
                                    # TASK 3: Add a slider to select payload range
                                    
                                  dcc.RangeSlider(id='payload-slider', 
                                                  min=slider_min, 
                                                  max=slider_max, 
                                                  step=1000, 
                                                  marks={slider_min: str(slider_min), 
                                                         slider_middle: str(slider_middle), 
                                                         slider_max: str(slider_max)}, 
                                                  value=[min_payload, max_payload]),

                                    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                  html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
  #  print('spacex_df:', spacex_df)
    print('spacex_df columns:', spacex_df.columns)
    filtered_df = spacex_df
   # print('filtered_df:', filtered_df)
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches by Site')
        return fig
    else:
        filtered_df_site = spacex_df[spacex_df['Launch Site'] == entered_site].reset_index()
        class_proportions = filtered_df_site['class'].value_counts(normalize=True)
        fig = px.pie(names=class_proportions.index,
                     values=class_proportions.values,
                     title='Total Success Launches for Site {}'.format(entered_site),
                     labels={'names': 'Class'})
        return fig
        
        # return the outcomes piechart for a selected site     

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'), 
             [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value")])

def get_scatter_plot(entered_site, payload_range):
    
    if entered_site == 'ALL':
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    
    min_payload, max_payload = payload_range
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= min_payload) &
                              (filtered_df['Payload Mass (kg)'] <= max_payload)]
    
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                     title='Payload vs. Launch Outcome', 
                     color="Booster Version Category", 
                     labels={'Payload Mass (kg)': 'Payload Mass (kg)', 'class': 'class'})
        
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
