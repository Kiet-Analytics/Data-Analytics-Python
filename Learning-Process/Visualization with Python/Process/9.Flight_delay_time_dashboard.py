import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


#Task1: Read the data
airline_data = pd.read_csv('airline_data.csv',
                             encoding='ISO-8859-1',
                             dtype ={'Div1Airport': str, 'Div1TailNum': str,
                                      'Div2Airpot': str, 'Div2TailNum': str}
                           )

#Task2: Create dash application and get the layout skeleton, update it.
app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('Flight Delay Time Statistics'),
                                 html.Div(['Input Year: ', dcc.Input(id='input-year', value='2010',
                                                                     type='number', style={'height':'50px', 'font-size':35})
                                           ], style={'font_size':30}),
                                 html.Br(),
                                 html.Br(),
                                 html.Div([
                                     html.Div(dcc.Graph(id='carrier-plot')),
                                     html.Div(dcc.Graph(id='weather-plot'))
                                           ], style={'display':'flex'}),
                                 html.Div([
                                     html.Div(dcc.Graph(id='nas-plot')),
                                     html.Div(dcc.Graph(id='security-plot'))
                                           ], style ={'display':'flex'}),
                                 html.Div(dcc.Graph(id='late-plot'), style={'Width' : '65%'})
                                 ])


#Task3: review and supporting functions
def compute_info(airline_data, entered_year):
    # Select data
    df =  airline_data[airline_data['Year']==int(entered_year)]
    # Compute delay averages
    avg_car = df.groupby(['Month','Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    avg_weather = df.groupby(['Month','Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    avg_NAS = df.groupby(['Month','Reporting_Airline'])['NASDelay'].mean().reset_index()
    avg_sec = df.groupby(['Month','Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    avg_late = df.groupby(['Month','Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()
    return avg_car, avg_weather, avg_NAS, avg_sec, avg_late
                                 
#Task4: Add the application callback function
@app.callback([
    Output(component_id='carrier-plot', component_property='figure'),
    Output(component_id='weather-plot', component_property='figure'),
    Output(component_id='nas-plot', component_property='figure'),
    Output(component_id='security-plot', component_property='figure'),
    Output(component_id='late-plot', component_property='figure')
    ], Input(component_id='input-year', component_property='value'))


# Computation to callback function and return graph
def get_graph(entered_year):
    
    # Compute required information for creating graph from the data
    avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_info(airline_data, entered_year)
    
    # Line plot for carrier delay
    carrier_fig = px.line(avg_car, x='Month', y='CarrierDelay', color='Reporting_Airline', title='Average carrrier delay time (minutes) by airline')
    
    # Line plot for weather delay
    weather_fig = px.line(avg_weather, x='Month', y='WeatherDelay', color='Reporting_Airline', title='Average weather delay time (minutes) by airline')
    
    # Line plot for nas delay
    nas_fig = px.line(avg_NAS, x='Month', y='NASDelay', color='Reporting_Airline', title='Average NAS delay time (minutes) by airline')
    
    # Line plot for security delay
    sec_fig = px.line(avg_sec, x='Month', y='SecurityDelay', color='Reporting_Airline', title='Average security delay time (minutes) by airline')

    # Line plot for late aircraft delay
    late_fig = px.line(avg_late, x='Month', y='LateAircraftDelay', color='Reporting_Airline', title='Average late aircraft delay time (minutes) by airline')
            
    return [carrier_fig, weather_fig, nas_fig, sec_fig, late_fig]

#Task5: run App
if __name__ == '__main__':
    app.run_server()







                                 
    
